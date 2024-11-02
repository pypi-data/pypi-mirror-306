"""
The scoop template engine (ste) is meant to facilitate the preparation of LaTeX
documents to abide to the formatting standards for various scientific
journals. Please visit
https://gitlab.com/scoopgroup-public/scoop-template-engine
for a full description of the features.
"""

# Resolve the dependencies.
import argparse
import datetime
import glob
import importlib.metadata
import importlib.resources
import importlib.util
import inspect
import itertools
import operator
import os
import packaging.version
import pathlib
import platform
import re
import shutil
import stat
import sys
import yaml
from subprocess import run, check_output, CalledProcessError, STDOUT, DEVNULL
from multiprocessing import Pool, cpu_count


def removePrefix(text, prefix):
    """
    removes a prefix from a string when present.
    """
    if text.startswith(prefix):
        return text[len(prefix):]
    else:
        return text


def extractTemplateDescription(text, templateBaseName):
    """
    extracts the template description present in the form
      <<TemplateDescription templateBaseName: description>> or else
      <<TemplateDescription: description>>
    from the text.
    """
    # Try and find a template specific description first.
    templateDescription = re.findall('<<TemplateDescription ' + templateBaseName + ':\s*(.*?)>>|$', text)[0]
    # If that did not turn up anything, try and find a generic template description.
    if not templateDescription:
        templateDescription = re.findall('<<TemplateDescription:\s*(.*?)>>|$', text)[0]
    return templateDescription


def extractDependencies(text, templateBaseName):
    """
    extracts the dependencies present in the form
      <<Dependency templateBaseName: file>> and
      <<Dependency: file>>
    from the text.
    """
    # Try and find template specific depencies first.
    dependencies = list(filter(None, re.findall('<<Dependency ' + templateBaseName + ':\s*(.*?)>>|$', text)))
    # In addition, try and find generic depencies.
    dependencies = dependencies + list(filter(None, re.findall('<<Dependency:\s*(.*?)>>|$', text)))
    return dependencies


def extractVersionRequirement(text):
    """
    extracts the version requirement as a string from the text string,
    specified in the form <<MinimumVersion: 1.2.3>>
    """
    # Try to find a minimum version requirement, if any.
    minimumVersion = re.search('<<MinimumVersion:\s*([0-9.]*)>>|$', text).group(1)
    return minimumVersion


def checkTemplateInitialized(text, templateDirectory, stampFileName):
    """
    verifies whether the template's resources have been initialized with a
    version of the scoop template engine recent enough to meet the minimum
    version requirements.
    """

    # Extract the template's minimum version requirement (if any).
    minimumVersion = extractVersionRequirement(text)
    if not minimumVersion:
        return True

    # Convert the version string to a Version type that can be compared.
    minimumVersion = packaging.version.Version(minimumVersion)

    # Get the version used to initialize the template's resources.
    stampFile = templateDirectory + '/' + stampFileName
    try:
        with open(stampFile) as stampFileStream:
            stampFileData = stampFileStream.read()
    except:
        return False

    versionInitialized = packaging.version.Version(stampFileData.split('\n')[0])

    # Verify whether the version requirement is met.
    if versionInitialized < minimumVersion:
        return False
    else:
        return True


def getTemplateList(baseDirectory, templatePrefix, filterString, stampFileName):
    """
    Find all template files matching the filter regular expression, together with
    their descriptions, Bib(La)TeX usage information, relative path, and link status.
    """
    # Find all template files in any of the directories underneath the baseDirectory.
    templateFiles = glob.glob(baseDirectory + '/**/' + templatePrefix + '*.tex', recursive = True)

    # Create a list of templates with relevant information.
    templateList = []
    for templateFile in templateFiles:
        # Determine whether the template file is a regular file or a link.
        templateFileIsLink = os.path.islink(templateFile)

        # Open the template file.
        try:
            with open(templateFile) as templateFileStream:
                templateFileData = templateFileStream.read()
        except IOError:
            print()
            print('ERROR: Template file {file:s} is not readable.'.format(file = templateFile))
            print()
            sys.exit(1)

        # Extract the template decription from the template.
        templateBaseName = re.findall('.*' + templatePrefix + '(.*?)\.tex', templateFile)[0]
        templateDescription = extractTemplateDescription(templateFileData, templateBaseName)

        # Verify whether the template uses BibLaTeX or BibTeX.
        templateUsesBibLaTeX = '<<BibLaTeXResources>>' in templateFileData
        templateUsesBibTeX = '<<CustomBibliography' in templateFileData

        # Determine the initialization status of the template.
        templateDirectory = os.path.dirname(templateFile)
        templateIsInitialized = checkTemplateInitialized(templateFileData, templateDirectory, stampFileName)

        # Get the relative path of the template file to the base directory.
        relativePath = str(pathlib.Path(templateFile).relative_to(baseDirectory))

        # If the the filter expression is found as a substring of the
        # relative path, add the template to the template list.
        # Also filter out the 'bibgenerator' template at this time.
        if re.search(filterString, relativePath) and not re.search('template-bibgenerator.tex', relativePath):
            templateList.append([
                templateBaseName,
                templateUsesBibLaTeX,
                templateUsesBibTeX,
                templateDescription,
                relativePath,
                templateFileIsLink,
                templateIsInitialized
                ])

    return templateList


def getSchemeList(schemeBaseDirectory, filterString):
    """
    Find all scheme directories matching the filter regular expression, together with
    their relative path.
    """
    # Compile a list of scheme base directories, starting with the scoop
    # template engine's scheme directory, and append all directories specified
    # through the environment variable STE_SCHEME_DIRS.
    schemeUserDirectories = os.environ.get("STE_SCHEME_DIRS", "") or ""
    if schemeUserDirectories:
        schemeDirectories = [schemeBaseDirectory] + schemeUserDirectories.split(os.pathsep)
    else:
        schemeDirectories = [schemeBaseDirectory]

    # Create a list of schemes with relevant information.
    schemeList = []

    # Find all scheme directories, i.e., leaf directories underneath any of the schemeBaseDirectories.
    # Directories are considered leaf directories if they do not contain any subdirectories except possibly
    # hidden subdirectories, starting with '.'.
    for schemeDirectory in schemeDirectories:
        for directory, subdirectoryList, fileList in os.walk(schemeDirectory, topdown = True, followlinks = True):
            # Exclude hidden subdirectories from the subdirectoryList.
            # https://stackoverflow.com/questions/19859840/excluding-directories-in-os-walk/19859907#19859907
            subdirectoryList[:] = [d for d in subdirectoryList if not d.startswith('.')]
            if not subdirectoryList:
                schemeList.append(directory)

    # Filter the complete directory path according to the filter.
    regex = re.compile(filterString)
    schemeList = list(filter(regex.search, schemeList))

    # Split each directory into its path up to the leaf directory, and the leaf directory.
    schemeList = [os.path.split(os.path.normpath(scheme)) for scheme in schemeList]

    return schemeList


def init(data, baseDirectory):
    """
    runs a script (typically init.py) and catches its stdout and stderr in a .log file.
    """
    # Construct the absolute path of the init.py file under consideration.
    folder = data[0]
    scriptname = data[1]
    scriptnameAbsolutePath = os.path.abspath(os.path.join(f'{folder}', f'{scriptname}'))
    scriptnameRelativePath = os.path.relpath(scriptnameAbsolutePath, start = baseDirectory)

    # Create the .log file with file name derived from the scriptname file name.
    logfilename = os.path.splitext(scriptnameAbsolutePath)[0] + '.log'
    print('Running {0:s}'.format(scriptnameRelativePath))
    with open(logfilename, 'w') as logfile:
        # Run the scriptname, capture its stdout and stderr and return value.
        # There is a timeout of 60 seconds.
        returnValue = run([sys.executable, scriptnameAbsolutePath], cwd = folder, stdout = logfile, stderr = STDOUT, timeout = 60)

    # Remember the script in case of failure.
    if returnValue.returncode != 0:
        return (False, folder, scriptname, logfilename)
    return (True, )

def main():
    """
    implements the user interface to the Scoop Template Engine.
    """

    # Remember who we are and how we were called.
    thisScriptName = os.path.basename(sys.argv[0])
    thisScriptAbsolutePath = os.path.abspath(sys.argv[0])
    thisScriptCallSummary = " ".join([thisScriptName] + sys.argv[1:])
    thisScriptAbsolutePathCallSummary = " ".join(sys.argv)
    baseDirectory = str(importlib.resources.files("ste"))
    scoopTemplateEngineName = "Scoop Template Engine"
    scoopTemplateEngineURL = "https://pypi.org/project/scoop-template-engine/"

    # Get the version number.
    try:
        scoopTemplateEngineVersion = importlib.metadata.version("scoop-template-engine")
    except:
        scoopTemplateEngineVersion = "VERSION ERROR"

    # Specify some default values.
    dataFile = None
    outFileSuffix = True

    # Define some constants.
    templatePrefix = "template-"
    stampFileName = "SCOOP-STAMP"

    # Define a description field for the command line argument parser.
    description = """
The scoop template engine facilitates the preparation of LaTeX documents by allowing the separation of layout from content.

Available commands:

    {prog:s} help                         show this help message and exit
    {prog:s} doc                          show the documentation
    {prog:s} version                      show the version information and exit
    {prog:s} list [options] [filter]      list available templates or schemes
    {prog:s} init [filter]                download and initialize template resources
    {prog:s} start [filter]               create files to start a new document according to a scheme
    {prog:s} prepare [options]            prepare a document for LaTeX compilation

    [filter] is a Python regular expression.
    A 'template' is a description of a specific format, e.g., for a particular journal.
    Templates are pre-defined in the scoop template engine.
    A 'scheme' is a collection of files to help start a new publication.
    Custom schemes can be added by the user.

Commands with options:

    {prog:s} prepare [options]

        -d file.yaml, --datafile file.yaml   YAML file containing document data
                                             (default: the unique .yaml or .yml file in the current directory)
        -t template, --template template     name of template to be used
        -o directory, --outdir directory     generated files will be written to this directory
                                             (default: current directory)
        -p prefix, --prefix prefix           <prefix>-<template>.tex file will be generated
                                             (default: derived from YAML file)
        -ns, --nosuffix                      generate <prefix>.tex rather than <prefix>-<template>.tex
        -nc, --nocustombib                   do not generate a custom .bib file
        -nb, --nobib                         do not use any .bib files
        -q, --quiet                          report only errors

        Examples:

        {prog:s} prepare --template siopt         prepare a document for 'SIAM Journal on Optimization'


    {prog:s} list [options] [filter]

        -t [filter], --template [filter]     display all available templates matching the optional regular expression [filter].
        -s [filter], --scheme [filter]       display all available schemes matching the optional regular expression [filter].

        Examples:

        {prog:s} list --template                  list all available templates
        {prog:s} list --template Springer         list all available templates matching 'Springer'
        {prog:s} list --scheme                    list all available schemes
        {prog:s} list --scheme preprint           list all available schemes matching 'preprint'


    {prog:s} start [filter]

        Examples:

        {prog:s} start amspreprint                start a new publication according to the 'amspreprint' scheme


    {prog:s} init [filter]

        Examples:

        {prog:s} init SIAM                        download and initialize template resources matching 'SIAM'

Example workflow:

    {prog:s} start amspreprint                    start a new publication according to the 'maspreprint' scheme
    <edit manuscript.yaml>                   adjust title, authors etc.

    {prog:s} prepare                              create 'manuscript-amspreprint.tex'
    ⎢ pdflatex manuscript-amspreprint.tex    enter the usual compile - edit loop
    ⎣ <edit content.tex>                     (use your favorite LaTeX editing system)

    {prog:s} prepare -t siopt                     create the same document for 'SIAM Journal on Optimization'
    ⎢ pdflatex manuscript-amspreprint.tex    enter the usual compile - edit loop
    ⎣ <edit content.tex>                     (use your favorite LaTeX editing system)
        \n
""".format(prog = thisScriptName)

    # Define the command line argument parser.
    parser = argparse.ArgumentParser(
            description = description,
            formatter_class = lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position = 40),
            usage = '%(prog)s <command> [filter] [options]',
            add_help = False,
            )

    # Add command as the first positional argument.
    commandList = ['help', 'doc', 'version', 'list', 'init', 'start', 'prepare']
    parser.add_argument('command',
            choices = commandList,
            help = argparse.SUPPRESS,
            default = 'help',
            metavar = 'command',
            nargs = '?')

    # Add filter as an optional second positional argument.
    parser.add_argument('filter',
            help = argparse.SUPPRESS,
            default = '',
            metavar = 'filter',
            nargs = '?')

    # Add --datafile as an optional argument.
    parser.add_argument('-d', '--datafile',
            metavar = 'file.yaml',
            help = argparse.SUPPRESS,
            action = 'store')

    # Add --template as an optional argument.
    parser.add_argument('-t', '--template',
            metavar = 'template',
            help = argparse.SUPPRESS,
            nargs = '?',
            default = None,
            const = '.*')

    # Add --outdir as an optional argument.
    parser.add_argument('-o', '--outdir',
            metavar = 'directory',
            help = argparse.SUPPRESS,
            default = None)

    # Add --prefix as an optional argument.
    parser.add_argument('-p', '--prefix',
            metavar = 'prefix',
            help = argparse.SUPPRESS,
            default = None)

    # Add --nosuffix as an optional argument.
    parser.add_argument('-ns', '--nosuffix',
            help = argparse.SUPPRESS,
            action = 'store_true')

    # Add --nocustombib as an optional argument.
    parser.add_argument('-nc', '--nocustombib',
            help = argparse.SUPPRESS,
            action = 'store_true')

    # Add --nobib as an optional argument.
    parser.add_argument('-nb', '--nobib',
            help = argparse.SUPPRESS,
            action = 'store_true')

    # Add --quiet as an optional argument.
    parser.add_argument('-q', '--quiet',
            help = argparse.SUPPRESS,
            action = 'store_true')

    # Add --scheme as an optional argument.
    parser.add_argument('-s', '--scheme',
            metavar = 'scheme',
            help = argparse.SUPPRESS,
            nargs = '?',
            default = None,
            const = '.*')

    # Parse the command line arguments.
    args = parser.parse_args()

    # Define a print function which honors the --quiet option.
    quietprint = print if not args.quiet else lambda *args, **kwargs: None

    # If the command is 'help', print the help and exit.
    if args.command == 'help':
        parser.print_help()
        sys.exit(0)

    # If the command is 'doc', launch the system's default viewer on the doc file and exit.
    if args.command == 'doc':
        # Specify the relevant doc file.
        docfile = importlib.resources.files("doc").joinpath("scoop-template-engine.pdf")
        # Launch the system's default viewer.
        if platform.system() == 'Darwin':
            try:
                output = check_output(['open', docfile], stderr = STDOUT)
            except CalledProcessError as exception:
                print('ERROR: {prog:s} doc failed to show the documentation.'.format(prog = thisScriptName))
                print('Your system\'s errror message follows:')
                print(exception.output)
                print()

        elif platform.system() == 'Windows':
            os.startfile(docfile)

        elif platform.system() == 'Linux':
            try:
                output = check_output(['xdg-open', docfile], stderr = STDOUT)
            except CalledProcessError as exception:
                print('ERROR: {prog:s} doc failed to show the documentation.'.format(prog = thisScriptName))
                print('Your system\'s errror message follows:')
                print(exception.output)
                print()
        else:
            print('Unknown platform. Don\'t know how to launch a pdf viewer.')
            print()
        sys.exit(0)

    # If the command is 'version', print the version number and exit.
    if args.command == 'version':
        print(scoopTemplateEngineVersion)
        sys.exit(0)

    # If the command is 'init', run all manuscripts/**/init.py scripts matching the filter and exit.
    if args.command == 'init':
        print('Initializing the template resources in {filter:s}...'.format(filter = args.filter))
        # Collect the init.py files to be executed, and the absolute names of
        # the folders they are in.
        fileList = []

        # Find all init.py files relative to the base directory.
        # If the the filter expression is found as a substring of the
        # relative path, add the init.py file to the list of files to be processed.
        initFiles = glob.glob(baseDirectory + '/**/init.py', recursive = True)
        for initFile in initFiles:
            relativePath = str(pathlib.Path(initFile).relative_to(baseDirectory))
            if re.search(args.filter, relativePath):
                scriptname = os.path.basename(initFile)
                folder = os.path.dirname(initFile)
                fileList.append((folder, scriptname))

        # Get the number of CPUs for parallel processing.
        nCPU = cpu_count()

        # Execute all scripts in parallel (by calling the init function) and catch
        # their return values.
        with Pool(nCPU) as p:
            returnValues = p.starmap(init, zip(fileList, itertools.cycle([baseDirectory])))

            # Filter the return values for failed scripts.
            failedList = [(x[1], x[2], x[3]) for x in returnValues if not x[0]]

            # Try again on the scripts which failed.
            returnValues = p.starmap(init, zip(failedList, itertools.cycle([baseDirectory])))

            # Filter the return values for failed scripts.
            failedList = [(x[1], x[2], x[3]) for x in returnValues if not x[0]]

            # Show the scripts which failed twice.
            if len(failedList) > 0:
                print()
                print('The following scripts failed twice:')
                for item in failedList:
                    print('{0:s}/{1:s}'.format(item[0], item[1]))
                    print('See {0:s} for details.'.format(item[2]))
                print('Associated templates will not be available.')
        sys.exit(0)


    # If the command is 'list', list all templates or schemes matching the filter, along with their descriptions and exit.
    if args.command == 'list':

        # Get and process the --template argument from the parser.
        templateBaseName = args.template

        # Get and process the --scheme argument from the parser.
        schemeBaseName = args.scheme

        # Make sure exactly one of --template or --scheme is given.
        if (not templateBaseName and not schemeBaseName) or (templateBaseName and schemeBaseName):
            print()
            print('ERROR: {prog:s} list requires either --template or --scheme'.format(prog = thisScriptName))
            print()
            sys.exit(1)

        # In case --template is given, obtain the list of templates matching the filter.
        if templateBaseName:
            filterString = templateBaseName
            templateList = getTemplateList(baseDirectory, templatePrefix, filterString, stampFileName)

            # Find the maximal lengths of the entries in each column of the
            # template list, and create a customized format string from it.
            if not templateList:
                sys.exit(0)
            formatString = ""
            formatString = formatString + "{template:" + str(max([len(item[0]) for item in templateList])) + "s}"
            formatString = formatString + "  {BibLaTeX:" + "1s}"
            formatString = formatString + "  {isLink:" + "1s}"
            formatString = formatString + "  {isInitialized:" + "1s}"
            formatString = formatString + "  {description:" + str(max([len(item[3]) for item in templateList])) + "s}"
            formatString = formatString + "  {file:" + str(max([len(item[4]) for item in templateList])) + "s}"

            # Print the list of templates, sorted by template description.
            templateList.sort(key = operator.itemgetter(2))
            for template in templateList:
                print(formatString.format(
                    template = template[0],
                    BibLaTeX = 'B' if template[1] else 'b' if template[2] else '-',
                    isLink = 'L' if template[5]  else 'F',
                    isInitialized = 'Y' if template[6]  else 'N',
                    description = template[3],
                    file = template[4]))
            sys.exit(0)

        # In case --scheme is given, obtain the list of schemes matching the filter.
        if schemeBaseName:
            filterString = schemeBaseName
            schemeBaseDirectory = os.path.join(baseDirectory , 'schemes')
            schemeList = getSchemeList(schemeBaseDirectory, filterString)

            # Find the maximal lengths of the entries in each column of the
            # scheme list, and create a customized format string from it.
            if not schemeList:
                sys.exit(0)
            formatString = ""
            formatString = formatString + "{scheme:" + str(max([len(item[1]) for item in schemeList])) + "s}"
            formatString = formatString + "  {dir:" + str(max([len(item[0]) for item in schemeList])) + "s}"

            # Print the list of schemes, without explicit sorting.
            for scheme in schemeList:
                print(formatString.format(
                    scheme = scheme[1],
                    dir = scheme[0]))
            sys.exit(0)


    # If the command is 'start', then locate the scheme specified by the filter, and copy the files
    # pertaining to the scheme to the current directory (but do not overwrite).
    if args.command == 'start':

        # Locate the scheme specified by the filter.
        filterString = args.filter
        schemeBaseDirectory = os.path.join(baseDirectory , 'schemes')
        schemeList = getSchemeList(schemeBaseDirectory, filterString)

        # Make sure the filter uniquely specifies the scheme.
        if len(schemeList) == 0:
            print()
            print("ERROR: {prog:s} start {filterString:s} returned no matching scheme".format(prog = thisScriptName, filterString = filterString))
            print("Aborting. No files were created.")
            print()
            sys.exit(1)
        if len(schemeList) != 1:
            print()
            print('ERROR: {prog:s} start {filterString:s} returned more than one match matching scheme.'.format(prog = thisScriptName, filterString = filterString))
            print("Please specify the scheme unambiguously.")
            print("Aborting. No files were created.")
            print()
            quietprint("The following matching schemes were found:")
            quietprint('\n'.join(scheme[1] for scheme in schemeList))
            quietprint()
            sys.exit(1)

        # Find the source directory.
        sourceDirectory = os.path.join(schemeList[0][0], schemeList[0][1])

        # Find the target (current) directory.
        targetDirectory = os.getcwd()

        # Get a list of the files to be copied.
        # Do not recurse into subdirectories, but explicitly include hidden files.
        fileList = itertools.chain(glob.iglob(sourceDirectory + '/*', recursive = False), glob.iglob(sourceDirectory + '/.*', recursive = False))
        fileList = list(filter(os.path.isfile, fileList))

        # Verify that none of the files exists (as a file or directory) in the target directory.
        filesExisting = []
        for file in fileList:
            relativePath = pathlib.Path(file).relative_to(sourceDirectory)
            if os.path.exists(relativePath):
                filesExisting.append(relativePath)
        if filesExisting:
            print()
            print("ERROR: The following files already exist in the current directory:")
            print([str(file) for file in filesExisting])
            print("Aborting. No files were created.")
            print()
            sys.exit(1)

        # Copy the files pertaining to the scheme to the target directory.
        for file in fileList:
            relativePath = pathlib.Path(file).relative_to(sourceDirectory)
            print('Copying {file:s} to ./'.format(file = str(relativePath)))
            shutil.copy(file, targetDirectory)
        sys.exit(0)


    # From here on, the command is 'prepare'.
    # Print a greeting.
    quietprint()
    quietprint('The scoop template engine (version {version:s}).'.format(version = scoopTemplateEngineVersion))
    quietprint()

    # Get and process the --datafile argument from the parser.
    dataFile = args.datafile
    if not dataFile:
        # Try to locate the unique .yaml or .yml file in the current directory.
        dataFile = glob.glob('*.yaml') + glob.glob('*.yml')
        if len(dataFile) == 0:
            print()
            print("No .yaml or .yml file found was found in the current directory.")
            print("Please specify the YAML document data file to use via --datafile.")
            print("Aborting. No output was produced.")
            print()
            sys.exit(1)
        if len(dataFile) != 1:
            print()
            print("More than one .yaml or .yml file was found in the current directory.")
            print("Please specify the YAML document data file to use via --datafile.")
            quietprint("The following .yaml or .yml data files were found:")
            quietprint('\n'.join(dataFile))
            print("Aborting. No output was produced.")
            print()
            sys.exit(1)
        dataFile = dataFile[0]

    # Get and process the --template argument from the parser.
    templateBaseName = args.template

    # Get and process the --scheme argument from the parser.
    schemeBaseName = args.scheme

    # Get and process the --prefix argument from the parser.
    outFileBaseName = args.prefix

    # Get and process the --outdir argument from the parser.
    outDirectory = args.outdir

    # Get and process the --nocustombib argument from the parser.
    customBib = not args.nocustombib

    # Get and process the --nobib argument from the parser.
    noBib = args.nobib

    # Report the data file to the user.
    quietprint("Using data file:      {file:s}".format(file = dataFile))

    # Read the .yaml data file.
    try:
        with open(dataFile) as dataFileStream:
            dataFileData = yaml.safe_load(dataFileStream)
            if not dataFileData:
                dataFileData = {}
    except IOError:
        print()
        print("ERROR: Data file {file:s} is not readable.".format(file = dataFile))
        print("Aborting. No output was produced.")
        print()
        sys.exit(1)

    # Process and remove the "outdir" key from the data file, unless we already have it from the command line.
    if not outDirectory:
        outDirectory = dataFileData.get("control", {}).get("outdir")
    dataFileData.pop("outdir", None)
    if not outDirectory:
        outDirectory = "./"

    # Process and remove the "prefix" key from the data file, unless we alredy have it from the command line.
    if not outFileBaseName:
        outFileBaseName = dataFileData.get("control", {}).get("prefix")
    if not outFileBaseName:
        outFileBaseName = os.path.splitext(dataFile)[0]
    dataFileData.pop("prefix", None)

    # Process and remove the "nocustombib" key from the data file, unless we alredy have it from the command line.
    if customBib:
        if dataFileData.get("control", {}).get("nocustombib"):
            customBib = False
    dataFileData.pop("nocustombib", None)

    # Process and remove the "nobib" key from the data file, unless we alredy have it from the command line.
    if not noBib:
        if dataFileData.get("control", {}).get("nobib"):
            noBib = True
    dataFileData.pop("nobib", None)

    # Process and remove the "template" key from the data file, unless we already have it from the command line.
    if not templateBaseName:
        templateBaseName = dataFileData.get("control", {}).get("template")
    dataFileData.pop("template", None)

    # Report the template name in use to the user.
    quietprint("Using template:       {template:s}".format(template = templateBaseName))

    # Make sure we have a template file.
    if not templateBaseName:
        print()
        print("You need to specify a template file via '--template' or via the 'template' key in the datafile.")
        print("Aborting. No output was produced.")
        print()
        sys.exit(1)

    # Assemble the full name of the template file.
    templateFile = templatePrefix + templateBaseName

    # Try to locate the unique .tex template file to be used.
    templateFile = glob.glob(baseDirectory + '/**/' + templateFile + '.tex', recursive = True)
    if len(templateFile) == 0:
        print()
        print("No template file matching '{templateBaseName:s}' was found.".format(templateBaseName = templateBaseName))
        print("Please specify the template via --template.")
        print("Aborting. No output was produced.")
        print()
        sys.exit(1)
    if len(templateFile) != 1:
        print()
        print("More than one .tex file is matching the pattern.")
        print("Please specify the template via --template unambiguously.")
        print("Aborting. No output was produced.")
        print()
        quietprint("The following matching template files were found:")
        quietprint('\n'.join(templateFile))
        quietprint()
        sys.exit(1)
    templateFile = templateFile[0]
    templateFileExtension = os.path.splitext(templateFile)[1]
    templateDirectory = os.path.dirname(templateFile)

    # Infer the top-level component (such as 'manuscripts') of the directory the template resides in.
    templateTopLevelDirectory = pathlib.Path(templateFile).relative_to(baseDirectory).parts[0]
    templateInitDirectory = pathlib.Path(templateFile).relative_to(baseDirectory).parts[1]

    # Report the template file to the user.
    quietprint("Using template file:  {file:s}".format(file = os.path.relpath(templateFile, start = baseDirectory)))

    # Infer the rules file from the template file.
    rulesFile = os.path.join(baseDirectory, templateTopLevelDirectory, templateTopLevelDirectory + '.py')

    # Report the rules file to the user.
    quietprint("Using rules file:     {file:s}".format(file = os.path.relpath(rulesFile, start = baseDirectory)))

    # Process the --nosuffix argument from the parser.
    if args.nosuffix:
        outFileSuffix = False

    # Process and remove the "nosuffix" key from the data file.
    if dataFileData.get("control", {}).get("nosuffix"):
        outFileSuffix = False
    dataFileData.pop("nosuffix", None)

    # Assemble the output file name.
    if outFileSuffix:
        outFileBaseName = outFileBaseName + '-' + templateBaseName + templateFileExtension
    else:
        outFileBaseName = outFileBaseName + templateFileExtension
    outFile = os.path.join(outDirectory, outFileBaseName)

    # Read the template file.
    try:
        with open(templateFile) as templateFileStream:
            templateFileData = templateFileStream.read()
    except IOError:
        print()
        print('ERROR: Template file {file:s} is not readable.'.format(file = templateFile))
        print("Aborting. No output was produced.")
        print()
        sys.exit(1)

    if not checkTemplateInitialized(templateFileData, templateDirectory, stampFileName):
        print()
        print('ERROR: The resources for template {template:s} have not been initialized or are outdated.'.format(template = templateBaseName))
        print('Please run')
        print('  {scriptName:s} init {dirName:s}'.format(scriptName = thisScriptName, dirName = templateInitDirectory))
        print('to initialize the resources for the {template:s} template.'.format(template = templateBaseName))
        print()
        sys.exit(1)

    # Remove all version tags from the template.
    templateFileData = re.sub(r'<<MinimumVersion.*>>.*\n', '', templateFileData)

    # Find the dependencies in the template.
    dependencies = extractDependencies(templateFileData, templateBaseName)

    # Copy all dependencies of the template to the outDirectory and make them
    # write protected.
    for dependency in dependencies:
        sourceFile = templateDirectory + "/" + dependency
        sourceFileRelativePath = os.path.relpath(sourceFile, start = baseDirectory)
        destinationFile = outDirectory + "/" + dependency
        quietprint("Copying dependency    {sourceFile:s} to {outDirectory:s}".format(sourceFile = sourceFileRelativePath, outDirectory = outDirectory))
        os.makedirs(os.path.dirname(destinationFile), exist_ok = True)
        # Make the destination writable (in case it exists).
        try:
            os.chmod(destinationFile, stat.S_IWRITE)
        except:
            pass
        shutil.copy(sourceFile, destinationFile, follow_symlinks = True)
        try:
            os.chmod(destinationFile, stat.S_IREAD)
        except:
            pass

    # Remove all dependency tags from the template.
    templateFileData = re.sub(r'<<Dependency.*>>.*\n', '', templateFileData)

    # Find the switches for the creation of a custom bibliography in the template.
    customBibliographySwitches = " ".join(re.findall('<<CreateCustomBibliography:\s*(.*?)>>', templateFileData))

    # Remove all custom bibliography creation tags from the template.
    templateFileData = re.sub(r'<<CreateCustomBibliography.*>>.*\n', '', templateFileData)

    # Find the template description in the template.
    templateDescription = extractTemplateDescription(templateFileData, templateBaseName)

    # Remove all template description tags from the template.
    templateFileData = re.sub(r'<<TemplateDescription.*>>.*\n', '', templateFileData)

    # Remove all comment tags from the template.
    templateFileData = re.sub(r'<<%.*>>.*\n', '', templateFileData)

    # Report the template description to the user.
    quietprint("Template description: {description:s}".format(description = templateDescription))

    # Import the rules file, which is supposed to provide functions to fill in the placeholders present in the template.
    spec = importlib.util.spec_from_file_location("scoop template engine rules", rulesFile)
    rules = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rules)

    # Create an instance of a parserObject.
    from collections import namedtuple
    parserInfoStructure = namedtuple('parserInfo', ['dataFileData', 'outDirectory', 'outFileBaseName', 'templateBaseName', 'templateDescription', 'scoopTemplateEngineVersion', 'thisScriptAbsolutePathCallSummary', 'customBibliographySwitches', 'customBib', 'noBib'])
    parserInfo = parserInfoStructure(
        dataFileData = dataFileData,
        outDirectory = outDirectory,
        outFileBaseName = outFileBaseName,
        templateBaseName = templateBaseName,
        templateDescription = templateDescription,
        scoopTemplateEngineVersion = scoopTemplateEngineVersion,
        thisScriptAbsolutePathCallSummary = thisScriptAbsolutePathCallSummary,
        customBibliographySwitches = customBibliographySwitches,
        customBib = customBib,
        noBib = noBib)
    parserFunctions = rules.parserObject(parserInfo)

    # Create a dictionary of substitutions to be performed on the template, recognized by the pattern '<<...>>'.
    substitutions = re.findall('<<(.*?)>>', templateFileData)
    substitutions = dict(zip(substitutions, [getattr(parserFunctions, substitution)() for substitution in substitutions]))

    # Apply the substitutions to the template.
    templateSpecialized = templateFileData
    for (replaceSource, replaceTarget) in substitutions.items():
        if replaceTarget is not None:
            templateSpecialized = templateSpecialized.replace("<<" + replaceSource + ">>", replaceTarget)

    # Prepend generation info including a time stamp.
    stampString = """% Generated by the {engineName:s} (version {engineVersion:s})
% {engineURL:s}
% on {dateTime:s} using
% {callSummary:s}

""".format(
        engineName = scoopTemplateEngineName,
        engineURL = scoopTemplateEngineURL,
        engineVersion = scoopTemplateEngineVersion,
        dateTime = datetime.datetime.utcnow().strftime("%Y%m%d-%H:%M:%S UTC"),
        callSummary = thisScriptCallSummary)
    templateSpecialized = stampString + templateSpecialized

    # In case the leaf directory of templateDirectory is 'stdout',
    # we ignore the destination outFile and write to stdout instead.
    if os.path.split(templateDirectory)[1] == 'stdout':
        outFile = 'stdout'

    # Report the output file to the user.
    quietprint("Writing output file:  {file:s}".format(file = outFile))

    # Distinguish writing to stdout from writing to a file.
    if outFile == 'stdout':
        # Write to stdout.
        sys.stdout.write(templateSpecialized)

    else:
        # Make the output file writable (in case it exists).
        try:
            os.chmod(outFile, stat.S_IWRITE)
        except:
            pass

        # Write the output file.
        try:
            with open(outFile, "w") as outFileStream:
                outFileData = outFileStream.write(templateSpecialized)
        except IOError:
            print()
            print('ERROR: outFile file {file:s} is not writable.'.format(file = outFile))
            print()
            sys.exit(1)

        # Make the output file write protected.
        try:
            os.chmod(outFile, stat.S_IREAD)
        except:
            pass


if __name__ == "__main__":
    sys.exit(main())

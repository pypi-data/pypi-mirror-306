"""
The Scoop Prepare Bibtex File (spbf) tool prepares a legacy BibTeX file from a
BibTeX or BibLaTeX source. In particular, it
* converts UTF8 characters into their BibTeX transcriptions and
* converts entry types such as @THESIS into BibTeX compatible types,
 depending on command line parameters.
This tool can operate
* in a document oriented mode, where the bibliography is drawn from a
 document's .bcf file (using the data source(s) declared there), or
* in a database oriented mode, where an entire .bib file is
 processed.
"""

# Resolve the dependencies.
import argparse
import bibtexparser
import datetime
import importlib.metadata
import importlib.resources
import os
import platform
import re
import subprocess
import sys
import tempfile
from bibtexparser.model import Field


def main():
    """
    implements the user interface to the Scoop Prepare Bibtex File tool.
    """

    # Remember who we are and how we were called.
    thisScriptName = os.path.basename(sys.argv[0])
    thisScriptAbsolutePath = os.path.abspath(sys.argv[0])
    thisScriptCallSummary = " ".join([thisScriptName] + sys.argv[1:])
    scoopTemplateEngineName = "Scoop Template Engine"
    scoopTemplateEngineURL = "https://pypi.org/project/scoop-template-engine/"

    # Get the version number.
    try:
        scoopTemplateEngineVersion = importlib.metadata.version("scoop-template-engine")
    except:
        scoopTemplateEngineVersion = "VERSION ERROR"

    # Define a description field for the command line argument parser.
    description = """
The scoop prepare bibtex file tool prepares a legacy BibTeX file from a BibTeX or BibLaTeX source.

    {prog:s} help                                show this help message and exit
    {prog:s} doc                                 show the documentation
    {prog:s} version                             show the version information and exit
    {prog:s} convert [options] infile [outfile]  convert 'infile' to a legacy bibtex file 'outfile'

The 'infile' can be
* a BibTeX or BibLaTeX (.bib) file - database mode
* a BibLaTeX control (.bcf) file   - document mode
In document mode, your 'biber' command must be version 2.10 or newer.

Examples:

    {prog:s} convert my.bib             convert 'my.bib' into a legacy bibtex file and write it to stdout
    {prog:s} convert my.bib legacy.bib  same but write to 'legacy.bib'
    {prog:s} convert my.bcf legacy.bib  convert the references used in my.bcf into a legacy bibtex file
                                    and write it to 'legacy.bib'
""".format(prog = thisScriptName)

    # Define the command line argument parser.
    parser = argparse.ArgumentParser(
            description = description,
            formatter_class = lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position = 41),
            usage = '%(prog)s <command> [options] infile [outfile]',
            add_help = False,
            )

    # Add command as the first positional argument.
    commandList = ['help', 'doc', 'version', 'convert']
    parser.add_argument('command',
            choices = commandList,
            help = argparse.SUPPRESS,
            default = 'help',
            metavar = 'command',
            nargs = '?')

    # Add infile as the second, optional positional argument.
    parser.add_argument('infile',
            help = argparse.SUPPRESS,
            default = None,
            metavar = 'infile',
            nargs = '?')

    # Add outfile as the third, optional positional argument.
    parser.add_argument('outfile',
            help = argparse.SUPPRESS,
            default = None,
            metavar = 'outfile',
            nargs = '?')

    # Add --giveninits as an optional argument.
    parser.add_argument('-gi', '--giveninits',
            help = 'abbreviate authors\' and editors\' given names',
            action = 'store_true')

    # Add --protectfamilynames as an optional argument.
    parser.add_argument('-pf', '--protectfamilynames',
            help = 'protect authors\' and editors\' multi-part family names',
            action = 'store_true')

    # Add --onlinetotechreport as an optional argument.
    parser.add_argument('-o2t', '--onlinetotechreport',
            help = 'transcribe @ONLINE entries into @TECHREPORT',
            action = 'store_true')

    # Add --proceedingstocollection as an optional argument.
    parser.add_argument('-p2c', '--proceedingstocollection',
            help = 'transcribe @PROCEEDINGS entries into @COLLECTION',
            action = 'store_true')

    # Add --doitonote as an optional argument.
    parser.add_argument('-d2n', '--doitonote',
            help = 'transcribe DOI into NOTE fields, with a link to https://doi.org/doi',
            action = 'store_true')

    # Add --doitourl as an optional argument.
    parser.add_argument('-d2u', '--doitourl',
            help = 'transcribe DOI into URL fields, pointing to https://doi.org/doi',
            action = 'store_true')

    # Add --urltonote as an optional argument.
    parser.add_argument('-u2n', '--urltonote',
            help = 'transcribe URL into NOTE fields, with a link to the url',
            action = 'store_true')

    # Add --arxivtotypeornote as an optional argument.
    parser.add_argument('-arxiv2tn', '--arxivtotypeornote',
            help = 'transcribe EPRINTTYPE = {arxiv} into a TYPE (for @TECHREPORTs) or NOTE field',
            action = 'store_true')

    # Add --haltotypeornote as an optional argument.
    parser.add_argument('-hal2tn', '--haltotypeornote',
            help = 'transcribe EPRINTTYPE = {HAL} into a TYPE (for @TECHREPORTs) or NOTE field',
            action = 'store_true')

    # Add --urntonote as an optional argument.
    parser.add_argument('-urn2n', '--urntonote',
            help = 'transcribe EPRINTTYPE = {urn} into a NOTE field',
            action = 'store_true')

    # Add --proceedingstitletobooktitle as an optional argument.
    parser.add_argument('-pt2bt', '--proceedingstitletobooktitle',
            help = 'transcribe TITLE into a BOOKTITLE field for @PROCEEDINGS',
            action = 'store_true')

    # Add --quiet as an optional argument.
    parser.add_argument('-q', '--quiet',
            help = 'report only errors',
            action = 'store_true')

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
        docfile = importlib.resources.files("doc").joinpath("scoop-prepare-bibtex-file.pdf")
        # Launch the system's default viewer.
        if platform.system() == 'Darwin':
            subprocess.run(['open', docfile], stderr = subprocess.STDOUT, stdout = subprocess.DEVNULL)
        elif platform.system() == 'Windows':
            os.startfile(docfile)
        elif platform.system() == 'Linux':
            subprocess.run(['xdg-open', docfile], stderr = subprocess.STDOUT, stdout = subprocess.DEVNULL)
        else:
            print('Unknown platform. Don\'t know how to launch a pdf viewer.')
        sys.exit(0)

    # If the command is 'version', print the version number and exit.
    if args.command == 'version':
        print(scoopTemplateEngineVersion)
        sys.exit(0)


    # From here on, the command is 'convert'.
    # Make sure the input file exists and is readable.
    if args.infile is None:
        print()
        print('\'{prog:s} convert\' requires an input file to be specified.'.format(prog = thisScriptName))
        print('See \'{prog:s} help\' for details.'.format(prog = thisScriptName))
        sys.exit(1)
    try:
        with open(args.infile) as infileStream:
            infileData = infileStream.read()
    except IOError:
        print()
        print('ERROR: Input file {file:s} is not readable.'.format(file = args.infile))
        sys.exit(1)

    # Determine whether we are in document or database oriented mode.
    infileExtension = os.path.splitext(args.infile)[1]
    if infileExtension == '.bcf':
        mode = 'document'
    elif infileExtension == '.bib':
        mode = 'database'
    else:
        print()
        print('ERROR: Input file {file:s} must have .bcf or .bib extension.'.format(file = args.infile))
        sys.exit(1)

    # Prepare a temporary output .bib file in the /tmp directory.
    temporaryOutfile = tempfile.NamedTemporaryFile(suffix = '.bib')

    # Invoke biber to prepare an initial output .bib file, with UTF8 characters
    # replaced by their LaTeX equivalents. Notice that biber also pretty-prints
    # the output, making sure all fields are on one line and white spaces are
    # trimmed.
    # Assemble the biber command line string.
    commandString = 'biber --quiet'
    if mode == 'database':
        commandString += ' --tool'
    commandString += (' --output-safechars --output-format=bibtex --output-file={outfilename:s} {infilename:s}').format(outfilename = temporaryOutfile.name, infilename = args.infile)

    # Invoke biber and make sure its run was successful.
    returnValue = subprocess.run(commandString, shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    try:
        returnValue.check_returncode()
    except subprocess.CalledProcessError:
        print('WARNING: {commandString:s} failed.\n'.format(commandString = commandString))


    # Read the .bib file into a library.
    if os.path.getsize(temporaryOutfile.name) == 0:
        print('NOTICE: The input file is empty, either because your document contains no citations, or due to an error.', file = sys.stderr)
        sys.exit(0)
    bibData = bibtexparser.parse_file(temporaryOutfile.name)

    # Iterate over the bibData entries and modify them as required.
    for entry in bibData.entries:
        # entry.ID represents the cite key as a string.
        # entry.ENTRYTYPE represents the record's type (such as 'ARTICLE').

        # Convert all DATE to YEAR fields, preserving the first four digits of the
        # actual date.
        if entry.fields_dict.get('DATE') is not None:
            field = entry.pop('DATE')
            field.key = 'YEAR'
            field.value = field.value[:4]
            entry.set_field(field)

        # Replace all LOCATION (BibLaTeX) by ADDRESS (BibTeX) fields.
        if entry.fields_dict.get('LOCATION') is not None:
            field = entry.pop('LOCATION')
            field.key = 'ADDRESS'
            entry.set_field(field)

        # Replace all JOURNALTITLE (BibLaTeX) by JOURNAL (BibTeX) fields.
        if entry.fields_dict.get('JOURNALTITLE') is not None:
            field = entry.pop('JOURNALTITLE')
            field.key = 'JOURNAL'
            entry.set_field(field)

        # Replace all ORGANIZATION (BibLaTeX) by PUBLISHER (BibTeX) fields.
        if entry.fields_dict.get('ORGANIZATION') is not None:
            field = entry.pop('ORGANIZATION')
            field.key = 'PUBLISHER'
            entry.set_field(field)

        # Append the content of SUBTITLE (BibLaTeX) field to the TITLE (BibTeX) field.
        # Leave SUBTITLE in since it does no harm.
        if entry.fields_dict.get('SUBTITLE') is not None:
            field = entry.fields_dict.get('TITLE') or Field(key = 'TITLE', value = None)
            field.value = '. '.join(filter(None, [field.value, entry.fields_dict.get('SUBTITLE').value]))
            entry.set_field(field)

        # Replace all @REPORT (BibLaTeX) by @TECHREPORT (BibTeX) entries.
        if entry.entry_type == 'report':
           entry.entry_type = 'techreport'

        # Replace all @COLLECTION (BibLaTeX) by @BOOK (BibTeX) entries.
        if entry.entry_type == 'collection':
            entry.entry_type = 'book'

        # Convert @THESIS with TYPE = "Bachelor thesis" (and similar) to @MASTERSTHESIS, and modify the
        # TYPE to say 'Bachelor thesis' explicitly. Replace INSTITUTION by SCHOOL.
        # Convert @THESIS with TYPE = "mathesis" (and similar) to @MASTERSTHESIS, and modify the
        # TYPE to say 'Master thesis' explicitly. Replace INSTITUTION by SCHOOL.
        # Convert @THESIS without TYPE to @MASTERTHESIS, and modify the
        # TYPE to say 'Thesis' explicitly. Replace INSTITUTION by SCHOOL.
        # Convert @THESIS with TYPE = "phdthesis" (and similar) to @PHDTHESIS, and modify the
        # TYPE to say 'Ph.D. thesis' explicitly. Replace INSTITUTION by SCHOOL.
        # Convert @THESIS with TYPE = "Habilitation thesis" (and similar) to @PHDTHESIS, and modify the
        # TYPE to say 'Ph.D. thesis' explicitly. Replace INSTITUTION by SCHOOL.
        if entry.entry_type == 'thesis':
            entry.entry_type = 'mastersthesis'
            if entry.fields_dict.get('INSTITUTION') is not None:
                field = entry.pop('INSTITUTION')
                field.key = 'SCHOOL'
                entry.set_field(field)

            # Set the 'TYPE' field according to the thesis type.
            field = entry.fields_dict.get('TYPE')
            if field is None:
                field = Field(key = 'TYPE', value = 'Thesis')
                entry.set_field(field)
            elif re.search('(Bachelor|B.Sc.|BSc)\s*Thesis', field.value, flags = re.IGNORECASE) is not None:
                field.value = '{B}achelor thesis'
                entry.set_field(field)
            elif re.search('(Master|M.Sc.|MSc|M.A.|MA)\s*Thesis', field.value, flags = re.IGNORECASE) is not None:
                field.value = '{M}aster thesis'
                entry.set_field(field)
            elif re.search('(Doctoral|Ph.D.|PHD)\s*Thesis', field.value, flags = re.IGNORECASE) is not None:
                field.value = '{Ph.D.} thesis'
                entry.set_field(field)
            elif re.search('(Habilitation)\s*Thesis', field.value, flags = re.IGNORECASE) is not None:
                field.value = '{H}abilitation thesis'
                entry.set_field(field)


        # Additional conversions triggered by command line switches follow.

        # If required, transcribe @ONLINE into @TECHREPORT entries.
        if args.onlinetotechreport:
            if entry.entry_type == 'online':
                entry.entry_type = 'techreport'

        # If required, transcribe @PROCEEDINGS into @COLLECTION entries.
        if args.proceedingstocollection:
            if entry.entry_type == 'proceedings':
                entry.entry_type = 'collection'

        # If required, transcribe EPRINTTTYPE = {arXiv} fields.
        # In @TECHREPORT, generate a TYPE field from EPRINT field.
        # In all other entry types (for example, @ARTICLE), generate a NOTE field from EPRINT field.
        # Leave EPRINTTYPE in since it does no harm but remove EPRINT since some .bst files
        # interpret every EPRINT as an arxiv preprint.
        if args.arxivtotypeornote:
            field = entry.fields_dict.get('EPRINTTYPE') or Field(key = 'EPRINTTYPE', value = '')
            if re.search('arXiv', field.value, flags = re.IGNORECASE) is not None:
                field = entry.pop('EPRINT')
                if field is not None:
                    arxivString = '{{arXiv}}: \href{{https://arxiv.org/abs/{arxivIdentifier:s}}}{{\detokenize{{{arxivIdentifier:s}}}}}'.format(arxivIdentifier = field.value)
                    if entry.entry_type == 'techreport':
                        field = entry.fields_dict.get('TYPE') or Field(key = 'TYPE', value = None)
                        field.value = '. '.join(filter(None, [field.value, arxivString]))
                        entry.set_field(field)
                    else:
                        field = entry.fields_dict.get('NOTE') or Field(key = 'NOTE', value = None)
                        field.value = '. '.join(filter(None, [field.value, arxivString]))
                        entry.set_field(field)

        # If required, transcribe EPRINTTTYPE = {HAL} fields.
        # In @TECHREPORT, generate a TYPE field from the EPRINT field.
        # In all other entry types (for example, @ARTICLE), generate a NOTE field from EPRINT field.
        # Leave EPRINTTYPE in since it does no harm but remove EPRINT since some .bst files
        # interpret every EPRINT as an arxiv preprint.
        if args.haltotypeornote:
            field = entry.fields_dict.get('EPRINTTYPE') or Field(key = 'EPRINTTYPE', value = '')
            if re.search('HAL', field.value, flags = re.IGNORECASE) is not None:
                field = entry.pop('EPRINT')
                if field is not None:
                    halString = '{{HAL}}: \href{{https://hal.archives-ouvertes.fr/{halIdentifier:s}}}{{\detokenize{{{halIdentifier:s}}}}}'.format(halIdentifier = field.value)
                    if entry.entry_type == 'techreport':
                        field = entry.fields_dict.get('TYPE') or Field(key = 'TYPE', value = None)
                        field.value = '. '.join(filter(None, [field.value, halString]))
                        entry.set_field(field)
                    else:
                        field = entry.fields_dict.get('NOTE') or Field(key = 'NOTE', value = None)
                        field.value = '. '.join(filter(None, [field.value, halString]))
                        entry.set_field(field)

        # If required, transcribe EPRINTTTYPE = {urn} fields.
        # In @TECHREPORT, generate a TYPE field from the EPRINT field.
        # In all entry types (for example, @ARTICLE), generate a NOTE field from EPRINT field.
        # Leave EPRINTTYPE in since it does no harm but remove EPRINT since some .bst files
        # interpret every EPRINT as an arxiv preprint.
        if args.urntonote:
            field = entry.fields_dict.get('EPRINTTYPE') or Field(key = 'EPRINTTYPE', value = '')
            if re.search('urn', field.value, flags = re.IGNORECASE) is not None:
                field = entry.pop('EPRINT')
                if field is not None:
                    urnString = '{{URN}}: \href{{https://www.nbn-resolving.de/{urnIdentifier:s}}}{{\detokenize{{{urnIdentifier:s}}}}}'.format(urnIdentifier = field.value)
                    field = entry.fields_dict.get('NOTE') or Field(key = 'NOTE', value = None)
                    field.value = '. '.join(filter(None, [field.value, urnString]))
                    entry.set_field(field)

        # If required, transcribe DOI into URL fields.
        # Leave DOI in since it does no harm.
        if args.doitourl:
            field = entry.fields_dict.get('DOI') or Field(key = 'DOI', value = None)
            doi = field.value
            if doi is not None:
                urlString = 'https://doi.org/{doi:s}'.format(doi = doi)
                field = entry.fields_dict.get('URL') or Field(key = 'URL', value = None)
                field.value = '. '.join(filter(None, [field.value, urlString]))
                entry.set_field(field)

        # If required, transcribe DOI into NOTE fields.
        # Leave DOI in since it does no harm.
        if args.doitonote:
            if (field := entry.fields_dict.get('DOI')) is not None:
                doi = field.value
                noteString = '{{DOI}} \href{{https://doi.org/{doi:s}}}{{\detokenize{{{doi:s}}}}}'.format(doi = doi)
                field = entry.fields_dict.get('NOTE') or Field(key = 'NOTE', value = None)
                field.value = '. '.join(filter(None, [field.value, noteString]))
                entry.set_field(field)

        # If required, transcribe URL into NOTE fields.
        # Leave URL in since it does no harm.
        if args.urltonote:
            if (field := entry.fields_dict.get('URL')) is not None:
                url = entry.fields_dict.get('URL').value
                noteString = '\\url{{{url:s}}}'.format(url = url)
                field = entry.fields_dict.get('NOTE') or Field(key = 'NOTE', value = None)
                field.value = '. '.join(filter(None, [field.value, noteString]))
                entry.set_field(field)

        # If required, transcribe TITLE into BOOKTITLE fields for @PROCEEDINGS.
        if args.proceedingstitletobooktitle:
            if entry.entry_type == 'proceedings':
                if (field := entry.pop('TITLE')) is not None:
                    field.key = 'BOOKTITLE'
                    entry.set_field(field)

        # If required, abbreviate authors' and editors' given names.
        if args.giveninits:
            def abbreviateFullName(fullName):
                # Split names (which always come in comma-separated form) such as
                #   'Smith, John'
                #   'Smith, Jr, John'
                # into their components, using the comma as a separator. Then
                # process the last component (the given names) through the
                # abbreviate function, and paste the results back together.
                nameParts = fullName.split(',')
                return ', '.join(nameParts[:-1] + [abbreviateGivenNames(nameParts[-1].strip())])

            def abbreviateGivenNames(givenNames):
                # Replace (repeated) whitespaces in givenNames by a single ' '.
                # Then split the givenNames at ' ' and '-', apply abbreviateSingleGivenName to
                # each part, and paste the results back together, using the captured separators.
                givenNames = ' '.join(givenNames.split())
                givenNames = re.split('([ -])', givenNames)
                for iter in range(0,len(givenNames),2):
                    givenNames[iter] = abbreviateSingleGivenName(givenNames[iter])
                return ''.join(givenNames)

            def abbreviateSingleGivenName(givenName):
                # Abbreviate a single given name, taking into account (partly fictitious) cases such as
                #   'Donald'
                #   'Jean-Paul'
                #   '\.{I}lker'
                #   '\v{R}\'{\i{}}'
                #   '\AE{}'
                # We use the following logic. If the single given name starts with '\', then copy it
                # until we have found at least one '{' and then until the matching '}'. If the single
                # name does not start with '\', the copy only the first character.
                if givenName[0] == '\\':
                    numberOfOpeningBrackets = 0;
                    numberOfClosingBrackets = 0;
                    for iter in range(len(givenName)):
                        if givenName[iter] == '{':
                            numberOfOpeningBrackets += 1
                        if givenName[iter] == '}':
                            numberOfClosingBrackets += 1
                        if (numberOfOpeningBrackets > 0) and (numberOfOpeningBrackets == numberOfClosingBrackets):
                            break
                    return givenName[:iter+1] + '.'
                else:
                    return givenName[0] + '.'

            # Perform the abbreviations of author and editor names.
            field = entry.fields_dict.get('AUTHOR') or Field(key = 'AUTHOR', value = None)
            if field.value is not None:
                field.value = ' and '.join([abbreviateFullName(authorName) for authorName in field.value.split(' and ')])
                entry.set_field(field)
            field = entry.fields_dict.get('EDITOR') or Field(key = 'EDITOR', value = None)
            if field.value is not None:
                field.value = ' and '.join([abbreviateFullName(authorName) for authorName in field.value.split(' and ')])
                entry.set_field(field)

        # If required, protect authors' and editors' multi-part family names.
        if args.protectfamilynames:
            def protectFullName(fullName):
                # Split names (which always come in comma-separated form) such as
                #   'Smith, John'
                #   'Smith, Jr, John'
                # into their components, using the comma as a separator. Then
                # process the first component (the family names) through the
                # protect function, and paste the results back together.
                nameParts = fullName.split(',')
                return ','.join([protectFamilyNames(nameParts[:-1])] + [nameParts[-1]])

            def protectFamilyNames(familyNames):
                return '{' + ', '.join(familyNames) + '}'

            # Perform the protection of multi-part author and editor names.
            field = entry.fields_dict.get('AUTHOR') or Field(key = 'AUTHOR', value = None)
            if field.value is not None:
                field.value = ' and '.join([protectFullName(authorName) for authorName in field.value.split(' and ')])
                entry.set_field(field)
            field = entry.fields_dict.get('EDITOR') or Field(key = 'EDITOR', value = None)
            if field.value is not None:
                field.value = ' and '.join([protectFullName(authorName) for authorName in field.value.split(' and ')])
                entry.set_field(field)


        # Protect upper-case characters.
        # We protect the entire TITLE, SUBTITLE, BOOKTITLE fields by braces,
        # not only consecutive chains of uppercase letters. The reason is that some
        # .bst files would otherwise convert even an unprotected $\Omega$ to $\omega$.
        def protect(string):
            return "{" + string + "}"
        if (field := entry.fields_dict.get('TITLE')) is not None:
            field.value = protect(field.value)
            entry.set_field(field)
        if (field := entry.fields_dict.get('SUBTITLE')) is not None:
            field.value = protect(field.value)
            entry.set_field(field)
        if (field := entry.fields_dict.get('BOOKTITLE')) is not None:
            field.value = protect(field.value)
            entry.set_field(field)

    # Prepare a custom formatter.
    bibtex_format = bibtexparser.BibtexFormat()
    bibtex_format.indent = '  '
    bibtex_format.trailing_comma = True
    bibtex_format.block_separator = '\n'

    # Write the pybtex dictionary into a string initially.
    bibDataString = bibtexparser.write_string(bibData, bibtex_format = bibtex_format)

    # Create a time and invokation stamp.
    stampString = """@COMMENT{{
Generated by the {engineName:s} (version {engineVersion:s})
{engineURL:s}
on {dateTime:s} using
{callSummary:s}
}}

""".format(
      engineName = scoopTemplateEngineName,
      engineURL = scoopTemplateEngineURL,
      engineVersion = scoopTemplateEngineVersion,
      dateTime = datetime.datetime.utcnow().strftime("%Y%m%d-%H:%M:%S UTC"),
      callSummary = thisScriptCallSummary)

    # Finally, write the result to the desired outfile.
    if args.outfile is not None:
        with open(args.outfile, 'w') as outfile:
            outfile.write(stampString + bibDataString)
    else:
        print(stampString + bibDataString)


if __name__ == "__main__":
    sys.exit(main())

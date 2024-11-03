# This script initializes the LaTeX author resources provided for
# GAMM Archive for Students (GAMMAS).
# https://www.bibliothek.tu-chemnitz.de/ojs/index.php/GAMMAS/information/authors

import shutil
import sys
from ste.utilities import utilities
from subprocess import run, STDOUT

if __name__ == '__main__':
    try:
        # Remove the initialization time and version stamp.
        utilities.remove_time_version_stamp()

        # Get and unpack the LaTeX author resources from CTAN.
        utilities.get_archive('https://mirrors.ctan.org/macros/latex/contrib/gammas.zip', junk = 1)

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)

#!/usr/bin/env python3

#                               #
# Developed by James Dunbar     #
# Maintained by members of OPIG #
#                               #

import shutil, os, subprocess, importlib
# Clean this out if it exists
if os.path.isdir("build"):
    shutil.rmtree("build/")

from distutils.core import setup

setup(name='anarci',
      version='1.3',
      description='Antibody Numbering and Receptor ClassIfication',
      author='James Dunbar',
      author_email='opig@stats.ox.ac.uk',
      url='http://opig.stats.ox.ac.uk/webapps/ANARCI',
      packages=['anarci'], 
      package_dir={'anarci': 'lib/python/anarci'},
      #package_data={'anarci': ['dat/HMMs/ALL.hmm',
      #                         'dat/HMMs/ALL.hmm.h3f',
      #                         'dat/HMMs/ALL.hmm.h3i',
      #                         'dat/HMMs/ALL.hmm.h3m',
      #                         'dat/HMMs/ALL.hmm.h3p']},
      scripts=['bin/ANARCI'],
      data_files = [ ('bin', ['bin/muscle', 'bin/muscle_macOS']) ]
     )

####
import sys
if sys.argv[1] != "install":
    sys.exit(0)

try:
    ANARCI_LOC = importlib.util.find_spec("anarci").submodule_search_locations[0]
except Exception as e:
    sys.stderr.write(e.message)
    sys.exit(1)

os.chdir("build_pipeline")

# The main change in this fork is that I have run the build pipeline once,
# and will use those results for all future builds. Since I'm building
# often in docker, ANARCI may fail to build if IMGT servers are down,
# or their API is down, which has happened to me before without
# realizing.
# Built on 2022-11-29, IMGT release 202246-1 (14 November 2022) 

# try:
#     #shutil.rmtree("curated_alignments/")
#     shutil.rmtree("muscle_alignments/")
#     shutil.rmtree("HMMs/")
#     shutil.rmtree("IMGT_sequence_files/")
#     os.mkdir(os.path.join(ANARCI_LOC, "dat"))
# except OSError:
#     pass

# print('Downloading germlines from IMGT and building HMMs...')
# proc = subprocess.Popen(["bash", "RUN_pipeline.sh"], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
# o, e = proc.communicate()

# print(o.decode())
# print(e.decode())


shutil.copy( "curated_alignments/germlines.py", ANARCI_LOC )
shutil.copytree( "HMMs", os.path.join(ANARCI_LOC, "dat/HMMs/") )

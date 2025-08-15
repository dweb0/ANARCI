#!/usr/bin/env python3


#                               #
# Developed by James Dunbar     #
# Maintained by members of OPIG #
#                               #

import site
import shutil, os
# Clean this out if it exists
if os.path.isdir("build"):
    shutil.rmtree("build/")

from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.build_py import build_py as _build_py

# The main change in this fork is that I have run the build pipeline once,
# and will use those results for all future builds. Since I'm building
# often in docker, ANARCI may fail to build if IMGT servers are down,
# or their API is down, which has happened to me before without
# realizing.
# Built on 2022-11-29, IMGT release 202246-1 (14 November 2022) 

class build_py(_build_py):
    def run(self):
        anarci_dir = os.path.join("lib", "python", "anarci")

        germ_src = os.path.join("build_pipeline", "curated_alignments", "germlines.py")
        germ_dst = os.path.join(anarci_dir, "germlines.py")
        shutil.copy2(germ_src, germ_dst)

        hmm_src = os.path.join("build_pipeline", "HMMs")
        hmm_dst = os.path.join(anarci_dir, "dat", "HMMs")
        os.makedirs(os.path.dirname(hmm_dst), exist_ok=True)
        shutil.copytree(hmm_src, hmm_dst, dirs_exist_ok=True)

        _build_py.run(self)


setup(
    name='anarci',
    version='1.3',
    description='Antibody Numbering and Receptor ClassIfication',
    author='James Dunbar',
    author_email='opig@stats.ox.ac.uk',
    url='http://opig.stats.ox.ac.uk/webapps/ANARCI',
    packages=find_packages('lib/python'),
    package_dir={'': 'lib/python'},
    include_package_data=True,
    package_data={
        "anarci": [
            "germlines.py",
            "dat/HMMs/*"
        ]
    },
    scripts=['bin/ANARCI'],
    data_files=[('bin', ['bin/muscle', 'bin/muscle_macOS'])],
    cmdclass={ 'build_py': build_py }
)

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

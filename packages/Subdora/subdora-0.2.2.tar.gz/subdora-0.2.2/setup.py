import pathlib
from setuptools import setup, find_packages
import os
import codecs

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.2.2' 
DESCRIPTION = 'Subdora : A python package that takes care of obfuscation of python scripts'
LONG_DESCRIPTION = long_description


setup(
        name="Subdora", 
        version=VERSION,
        author="Lakshit Karsoliya",
        author_email="lakshitkumar220@gmail.com",
        description=DESCRIPTION,
        long_description_content_type="text/markdown",

        long_description=LONG_DESCRIPTION,
        url='https://github.com/Lakshit-Karsoliya/Subdora',
        # requires=[],

        
        keywords=['python', 'file encryption','security','obfuscation'],
        classifiers= [
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "Operating System :: Unix",
            "Operating System :: Microsoft :: Windows",
        ],
        install_requires=["pillow"],
        packages=find_packages(),
        include_package_data=True,
        entry_points={
            "console_scripts":["subdora = Subdora._subdora_cli:main"],
        }
)
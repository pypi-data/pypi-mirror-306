from pyimzml import __version__
from setuptools import setup, find_packages

setup(
    name='pyimzML',
    version=__version__,
    description="Parser for conversion of imzML 1.1.0 files",
    long_description="""
Parser for conversion of imzML 1.1.0 files. 
See specification here: https://ms-imaging.org/wp-content/uploads/2009/08/specifications_imzML1.1.0_RC1.pdf. 
Outputs data as python lists, dicts or numpy array.
""",
    # The project's main homepage.
    url='https://github.com/alexandrovteam/pyimzML',
    author='Alexandrov Team, EMBL',
    author_email='theodore.alexandrov@embl.de',

    license='Apache 2.0',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='bioinformatics imaging mass spectrometry parser imzML',

    packages=find_packages(exclude=('tests', 'docs')),

    install_requires=['numpy', 'wheezy.template'],
)

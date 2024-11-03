from setuptools import setup, Extension
from codecs import open
from Cython.Build import cythonize
import os
import sys

long_description = ""

# Load README.rst into long description. User can skip using README.rst as long description:
# GGWAVE_OMIT_README_RST=1 python setup.py install
OMIT_README_RST = os.getenv('GGWAVE_OMIT_README_RST', False)
if not OMIT_README_RST:
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()

extension = [Extension("ggwave",
                       ["src/ggwave/ggwave.pyx", "src/ggwave/ggwave/src/ggwave.cpp"],
                       include_dirs=["src/ggwave/ggwave/include", "src/ggwave/ggwave/include/ggwave"],
                       depends=["src/ggwave/ggwave/include/ggwave/ggwave.h"],
                       language="c++",
                       extra_compile_args=["-std=c++11"] if sys.platform.find("win32") < 0 else[],
                       )]

extension = cythonize(extension)

setup(
    # Information
    name="ggwave-wheels",
    description="Tiny data-over-sound library.",
    long_description=long_description,
    url="https://github.com/ggerganov/ggwave",
    author="Georgi Gerganov",
    author_email="ggerganov@gmail.com",
    license="MIT",
    keywords="data-over-sound fsk ecc serverless pairing qrcode ultrasound",
    # Build instructions
    ext_modules=extension,
)

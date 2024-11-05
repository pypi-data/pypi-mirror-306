from setuptools import setup
from setuptools import find_packages


VERSION = '0.2.1'

setup(
    name='randwave',  # package name
    version=VERSION,  # package version
    description='Random Wavelet Convolution',  # package description
    packages=find_packages(),
    zip_safe=True,
    author='Yong Feng',
    url = 'https://github.com/fyancy/RaVEL',
)
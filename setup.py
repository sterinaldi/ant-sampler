import numpy
from setuptools import setup

setup(
    name = 'antsampler',
    description = 'AntSampler',
    author = 'Stefano Rinaldi, Daniele Sanfratello',
    author_email = 'stefano.rinaldi@phd.unipi.it, d.sanfratello@studenti.unipi.it',
    url = 'https://github.com/sterinaldi/ant-sampler',
    python_requires = '>=3.7',
    packages = ['antsampler'],
    include_dirs = [numpy.get_include()],
    setup_requires=['numpy']
    )


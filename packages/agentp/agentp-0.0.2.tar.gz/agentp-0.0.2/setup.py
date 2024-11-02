from setuptools import setup, find_packages 

VERSION = '0.0.2'
DESCRIPTION = 'Associating Gene Expression to Neuroimaging Traits Pipeline (AGENT-P)'
REQ_PACKAGES = ['bgen_reader', 'h5py', 'numpy', 'pandas', 'patsy', \
                'bitarray', 'scipy', 'statsmodels', 'pyliftover']

setup(
    name='agentp', 
    version=VERSION, 
    author='Nhung Hoang', 
    author_email='nhung.hoang@vanderbilt.edu', 
    url='https://github.com/nhunghoang/neurogen',
    description=DESCRIPTION, 
    license='MIT',
    python_requires=">=3.8",
    classifiers=[
        'Programming Language :: Python :: 3', 
        ],
    packages=find_packages(),
    install_requires=[
        'bgen_reader>=4.0.8',
        'h5py>=3.7.0',
        'numpy>=1.23.5',
        'pandas>=1.5.3',
        'patsy>=0.5.6',
        'bitarray>=3.0.0',
        'scipy>=1.10.1',
        'statsmodels>=0.14.1',
        'pyliftover>=0.4.1', 
        ], 
) 

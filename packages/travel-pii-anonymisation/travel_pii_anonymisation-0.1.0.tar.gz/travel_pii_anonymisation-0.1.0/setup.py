from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(
    name='travel_pii_anonymisation',
    version='0.1.0',
    author='Ilias',
    author_email='ilias.driouich@amadeus.com',
    description='A package for pseudonymizing travel-specific PII data',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AmadeusITGroup/Travel-specific-PIIs-pseudonymization',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'pandas>=1.1.0',
        'numpy>=1.19.0',
        'faker>=8.0.0',
    ],
    tests_require=[
        'pytest>=6.0.0',
    ],
    entry_points={
        'console_scripts': [
            'travel_pii=tspii:main',
    ],
    },
    python_requires='>=3.6',
)

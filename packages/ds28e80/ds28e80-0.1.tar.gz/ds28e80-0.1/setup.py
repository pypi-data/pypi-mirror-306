from setuptools import setup, find_packages

setup(
    name='ds28e80',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'crcmod',
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='A library for interacting with the DS28E80 EEPROM using 1-Wire communication.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/ds28e80',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

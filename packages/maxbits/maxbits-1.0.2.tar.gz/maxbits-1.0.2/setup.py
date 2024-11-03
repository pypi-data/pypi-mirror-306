from setuptools import setup, find_packages

setup(
    name='maxbits',
    version='1.0.2',
    author='woskethebot',
    author_email='nushratakhter1999@gmail.com',
    description='A Python module that provides functions to calculate the maximum and minimum values for signed and unsigned integers, as well as floating-point numbers of specified bit widths.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/woskethebot/maxbits',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)

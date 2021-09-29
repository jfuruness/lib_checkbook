from setuptools import setup, find_packages
import sys

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='lib_checkbook',
    author="Justin Furuness",
    author_email="jfuruness@gmail.com",
    version="0.0.2",
    url='https://github.com/jfuruness/lib_checkbook.git',
    license="BSD",
    description="Checkbook api calls",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["Checkbook"],
    include_package_data=True,
    python_requires=">=3.6",
    packages=find_packages(),
    install_requires=[
        "email-validator==1.1.3",
        "requests==2.26.0",
    ],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3'],
    entry_points={
        'console_scripts': 'lib_checkbook = lib_checkbook.__main__:main'
    },
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)

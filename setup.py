import os

from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

# Avoids IDE errors, but actual version is read from version.py
__version__ = None
exec(open("phutils/version.py").read())

# Get the long description from the README file
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


tests_requires = [
    "pytest~=5.2",
    "pytest-pycodestyle~=1.4",
    "pytest-cov~=2.7",
    "pytest-localserver~=0.5",
    "pytest-sanic==1.0.0",
    "pytest-xdist==1.29.0",
    "pytest-sanic==1.0.0",
    "pytest-twisted<1.6",
    "treq~=17.8",
    "responses~=0.9.0",
    "httpretty~=0.9.0",
    "black==19.10b0",
    "flake8==3.7.8",
    "pytype==2019.7.11",
    "pre-commit==1.21.0",
]

install_requires = ["tqdm==4.28.1", "Pillow==6.0.0", "coloredlogs==10.0"]

upload_requires = [
    "twine==3.1.1",
]

extras_requires = {
    "dev": tests_requires + install_requires + upload_requires,
    "upload": upload_requires,
}

setup(
    name="phutils",
    packages=find_packages(exclude=["tests", "examples"]),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        # supported python versions
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries",
    ],
    version=__version__,
    install_requires=install_requires,
    tests_require=tests_requires,
    extras_require=extras_requires,
    include_package_data=True,
    description="Small photo organizer utility library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jose Marcos",
    author_email="jose@melior.ai",
    url="https://melior.ai",
    keywords="image photo python utility organizer",
    download_url="https://github.com/jmrf/phutilities/archive/{}.tar.gz"
    "".format(__version__),
    project_urls={
        "Bug Reports": "https://github.com/jmrf/phutilities/issues",
        "Source": "https://github.com/jmrf/phutilities",
    },
)

print("\nWelcome to Melior's Semantic Search!")

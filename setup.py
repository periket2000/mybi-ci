import codecs
import os
import re

from setuptools import setup, find_packages


###################################################################

NAME = "mybi-ci"
PACKAGES = find_packages(where="src")
META_PATH = os.path.join("src", "mybi-ci-meta", "__init__.py")
KEYWORDS = ["CI", "build", "devops", "sysadmin"]
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Intended Audience :: System Administrators",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 2.7"
]
INSTALL_REQUIRES = [
    'jsonschema>=2.5.1',
    'args>=0.1.0',
    'click>=6.6',
    'Flask>=0.11.1'
]
TEST_REQUIRE = [
    'pytest>=3.0.1',
    'pytest-pythonpath>=0.7.1',
    'mock>=2.0.0'
]
###################################################################

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()


META_FILE = read(META_PATH)


def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta),
        META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


if __name__ == "__main__":
    setup(
        name=NAME,
        description=find_meta("description"),
        license=find_meta("license"),
        url=find_meta("uri"),
        version=find_meta("version"),
        author=find_meta("author"),
        author_email=find_meta("email"),
        maintainer=find_meta("author"),
        maintainer_email=find_meta("email"),
        keywords=KEYWORDS,
        long_description=read("README.rst"),
        packages=PACKAGES,
        package_dir={"": "src"},
        zip_safe=False,
        classifiers=CLASSIFIERS,
        install_requires=INSTALL_REQUIRES,
        tests_require=TEST_REQUIRE,
        scripts=['bin/mybi-ci'],
    )

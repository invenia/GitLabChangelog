import codecs
from os.path import abspath, dirname, join

from setuptools import find_packages, setup


TEST_DEPS = ["coverage[toml]", "pytest", "pytest-cov"]
DOCS_DEPS = ["sphinx", "sphinx-rtd-theme", "sphinx-autoapi", "recommonmark"]
CHECK_DEPS = ["isort", "flake8", "flake8-quotes", "pep8-naming", "mypy", "black"]
EXTRAS = {
    "test": TEST_DEPS,
    "docs": DOCS_DEPS,
    "check": CHECK_DEPS,
    "dev": TEST_DEPS + DOCS_DEPS + CHECK_DEPS,
}


REQUIREMENTS = [
    "Jinja2>=2.10.3",
    "python-dateutil>=2.8.1",
    "python-gitlab>=1.8.0",
    "semver>=2.9.0",
]

# Read in the version
with open(join(dirname(abspath(__file__)), "VERSION")) as version_file:
    version = version_file.read().strip()

description = "Produces GitLab changelog release notes for projects that follow SemVer"

setup(
    name="GitLabChangelog",
    version=version,
    description=description,
    long_description=codecs.open("README.md", "r", "utf-8").read(),
    long_description_content_type="text/markdown",
    author="Invenia Technical Computing",
    url="https://github.com/invenia/gitlabchangelog",
    packages=find_packages(exclude=["tests"]),
    install_requires=REQUIREMENTS,
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    platforms=["any"],
    include_package_data=True,
    tests_require=TEST_DEPS,
    extras_require=EXTRAS,
)

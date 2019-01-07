from setuptools import setup, find_packages

VERSION = "0.0.1"
PACKAGE_NAME = "indy-agent-python"


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


if __name__ == "__main__":
    setup(
        name=PACKAGE_NAME,
        version=VERSION,
        packages=find_packages(),
        include_package_data=True,
        install_requires=parse_requirements("requirements.txt"),
        scripts=["scripts/indyagent"],
    )

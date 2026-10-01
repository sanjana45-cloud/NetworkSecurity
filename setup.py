from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:

    """
    This function will return the list of requirements
    """

    requirement_lst: List[str] = []

    try:
        with open("requirements.txt") as f:
            # Read lines from the file
            lines = f.readlines()

            # Process each line
            for line in lines:
                requirement = line.strip()

                if requirement and requirement != "-e .":
                    requirement_lst.append(requirement)

    except FileNotFoundError:
        print("requirements.txt file not found")

    return requirement_lst


print(get_requirements())

setup(
    name="NetworkSecurity",
    version="0.0.1",
    author="N S Sanjana",
    author_email="sanjanans317@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(),
)
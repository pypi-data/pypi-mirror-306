from setuptools import setup, find_packages

setup(
    name="eeg_auto_tools",
    version="0.0.1",
    author="Sear",
    author_email="vasilijkrukovskij2015@gmail.com",
    description="The set of tools for working with EEG data",
    packages=find_packages(),
    include_package_data=True,
    package_data={"": ["templates/*"]},
    python_requires=">=3.6",
)
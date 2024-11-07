from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name="open_mice_hub",
    version='0.0.2',
    packages=find_packages(),
)
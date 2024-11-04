from setuptools import setup, find_packages

setup(
    name="datehelper-now_youre_unemployed",
    version="0.1.6",
    author="now-youre-unemployed", 
    description="A simple date helper library.",
    packages=find_packages(),
    tests_require=["pytest"], 
    python_requires=">=3.6",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
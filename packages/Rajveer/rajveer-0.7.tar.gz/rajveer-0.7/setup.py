from setuptools import setup , find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
DESCRIPTION='A Python API Module That Helps Python Dev'
setup(
    name='Rajveer',
    version='0.7',
    author="Rajveer Verma",
    description=DESCRIPTION,
    long_description=(here / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['requests','user_agent','colorama','termcolor']
    )
        

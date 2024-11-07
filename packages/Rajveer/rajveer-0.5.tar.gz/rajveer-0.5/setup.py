from setuptools import setup , find_packages
DESCRIPTION='A Python API Module That Helps Python Dev'
setup(
    name='Rajveer',
    version='0.5',
    author="Rajveer Verma",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests','user_agent','colorama','termcolor']
    )
        

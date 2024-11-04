from setuptools import setup, find_packages

with open("README.md", "r") as r:
    desc = r.read()

setup(
    name="dep_client",
    version="1.0.0",
    author="npdep",
    url="https://github.com/npdep/dep-client",
    description="Data Exfiltration Protocol (DEP) Client - Transfer data with DEP",
    classifiers=[
        "Operating System :: OS Independent ",
        "Programming Language :: Python :: 3 ",
        "License :: OSI Approved :: MIT License "
    ],
    license="MIT",
    long_description=desc,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages(where='src'),
    include_package_data=True,
    install_requires=[
        "dep_common"
    ],
     entry_points={
        "console_scripts": [
            "dep_client = dep_client.__main__:main"
        ]
    }
)

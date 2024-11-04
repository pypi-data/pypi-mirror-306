from setuptools import setup, find_packages

with open("README.md", "r") as r:
    desc = r.read()

setup(
    name="dep_reader",
    version="1.0.0",
    author="npdep",
    url="https://github.com/npdep/dep-reader",
    description="Read Data Exfiltration Protocol (DEP) Bytes",
    classifiers=[
        "Operating System :: OS Independent ",
        "Programming Language :: Python :: 3 "
    ],
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
            "dep_reader = dep_reader.__main__:main"
        ]
    }
)

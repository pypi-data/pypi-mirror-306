from setuptools import setup, find_packages

with open("README.md", "r") as r:
    desc = r.read()

setup(
    name="npdep_client",
    version="0.1.0",
    author="npdep",
    url="https://github.com/npdep/npdep-client",
    description="Network Protocol Data Exfiltration Project Client - A modular approach for data exfiltration",
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
        "npdep_common"
    ],
     entry_points={
        "console_scripts": [
            "npdep_client = npdep_client.__main__:main"
        ]
    }
)

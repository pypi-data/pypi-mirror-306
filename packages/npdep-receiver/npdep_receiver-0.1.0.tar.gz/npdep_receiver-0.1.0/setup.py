from setuptools import setup, find_packages

with open("README.md", "r") as r:
    desc = r.read()

setup(
    name="npdep_receiver",
    version="0.1.0",
    author="npdep",
    url="https://github.com/npdep/npdep-receiver",
    description="Receiver Modules for Network Protocol Data Exfiltration Project Server",
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
        "dep_common",
        "dep_reader"
    ],
     entry_points={
        "console_scripts": [
            "npdep_receiver = npdep_receiver.__main__:main"
        ]
    }
)

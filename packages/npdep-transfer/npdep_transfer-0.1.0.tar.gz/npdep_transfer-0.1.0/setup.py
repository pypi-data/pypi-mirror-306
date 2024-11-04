from setuptools import setup, find_packages

with open("README.md", "r") as r:
    desc = r.read()

setup(
    name="npdep_transfer",
    version="0.1.0",
    author="npdep",
    url="https://github.com/npdep/npdep-transfer",
    description="Transfer Modules for Network Protocol Data Exfiltration Project Client",
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
        "dep_client",
        "npdep_icmp_client",
        "npdep_http_client",
        "foi"
    ],
     entry_points={
        "console_scripts": [
            "npdep_transfer = npdep_transfer.__main__:main"
        ]
    }
)

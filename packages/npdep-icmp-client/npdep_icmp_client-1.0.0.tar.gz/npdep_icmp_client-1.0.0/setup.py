from setuptools import setup, find_packages

with open("README.md", "r") as r:
    desc = r.read()

setup(
    name="npdep_icmp_client",
    version="1.0.0",
    description="A client to exfiltrate files through ICMP messages",
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
        ""
    ],
     entry_points={
        "console_scripts": [
            "npdep_icmp_client = npdep_icmp_client.__main__:main"
        ]
    }
)

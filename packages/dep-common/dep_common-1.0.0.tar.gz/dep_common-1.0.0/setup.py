from setuptools import setup, find_packages

with open("README.md", "r") as r:
    desc = r.read()

setup(
    name="dep_common",
    version="1.0.0",
    author="npdep",
    url="https://github.com/npdep/dep-common",
    description="Provides common functionality for dep_reader and dep_client",
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
            "dep_common = dep_common.__main__:main"
        ]
    }
)

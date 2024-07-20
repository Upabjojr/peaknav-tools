from setuptools import setup, find_packages

def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fin:
        return fin.read().splitlines()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="PeakNav Tools",
    version="0.1",
    author="Francesco Bonazzi",
    author_email="franz.bonazzi@gmail.com",
    description="Tools for PeakNav app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Upabjojr/peaknav-tools",
    project_urls={
        "Bug Tracker": "https://github.com/Upabjojr/peaknav-tools/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=read_requirements(),
    include_package_data=True,
)

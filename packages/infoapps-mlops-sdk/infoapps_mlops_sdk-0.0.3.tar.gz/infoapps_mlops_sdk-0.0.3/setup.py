from setuptools import setup, find_packages

setup(
    name="infoapps_mlops_sdk",                           # Package name
    version="0.0.3",                            # Version
    author="Renaldo Williams",
    author_email="renaldo_williams@apple.com",
    description="A custom MLOps SDK",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://prodgit.apple.com/feldspar/mlops-py",  # GitHub URL or any repo link
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)

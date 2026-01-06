from setuptools import setup, find_packages

setup(
    name="mkl",
    version="0.1.0",
    description="Mike Grocery List CLI App",
    author="Mike Kwiatkowsky",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    entry_points={
        "console_scripts": [
            "mkl=mkl.mk_launch:main",
        ],
    },
    install_requires=[],
    python_requires=">=3.7",
)
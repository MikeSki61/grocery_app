from setuptools import setup, find_packages

setup(
    name="mk",
    version="0.1.0",
    description="Mike Grocery List CLI App",
    author="Mike Kwiatkowsky",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    entry_points={
        "console_scripts": [
            "mk=mk.mk_launch:main",
        ],
    },
    install_requires=[],
    python_requires=">=3.7",
)
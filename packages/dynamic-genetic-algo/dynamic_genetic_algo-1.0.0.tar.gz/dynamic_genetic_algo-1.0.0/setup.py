from setuptools import find_packages, setup

setup(
    name="dynamic_genetic_algo",
    version="1.0.0",
    description="A genetic algorithm library",
    author="Gabriel Vance",
    author_email="gjvance67@gmail.com",
    packages=find_packages(),
    install_requires=["pandas", "prettytable"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)

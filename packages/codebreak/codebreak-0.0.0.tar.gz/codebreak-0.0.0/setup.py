from setuptools import setup, find_packages

setup(
    name="codebreak",
    verion="0.1.2",
    packages=find_packages(),
    description="A package to help Python developers take healthy breaks with different types of exercises.",
    author="The Fixers",
    install_requires=[
        "schedule==1.2.2"
    ],
    extras_require={
        "dev": [
            "pytest==8.3.3"
        ]
    },
    python_requires=">=3.6",
     
)


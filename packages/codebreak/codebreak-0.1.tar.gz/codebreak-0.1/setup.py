from setuptools import setup, find_packages

setup(
    name="codebreak",
    version="0.1",
    packages=find_packages(),
    description="A lighthearted package for random stretch suggestions.",
    author="Your Team",
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


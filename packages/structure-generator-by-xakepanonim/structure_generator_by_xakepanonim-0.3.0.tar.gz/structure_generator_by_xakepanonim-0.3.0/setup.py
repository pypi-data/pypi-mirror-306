from setuptools import setup, find_packages

setup(
    name="structure-generator-by-xakepanonim",
    version="0.3.0",
    author="XakepAnonim",
    description="This package automatically generates a project architecture description and saves it in the README.md file.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/XakepAnonim/structure_generator",
    packages=find_packages(),
    install_requires=['toml>=0.10.0'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'generate-structure=generator.generator:main',
        ],
    },
)

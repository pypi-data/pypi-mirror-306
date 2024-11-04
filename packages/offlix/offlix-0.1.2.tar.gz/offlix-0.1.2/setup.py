from setuptools import setup,find_packages
from os import path

def readme():
    with open("README.md") as f:
        return f.read()
setup(
    name="offlix",  # Replace with your package name
    version="0.1.2",
    long_description=readme(),  # Read the content of README.md
    long_description_content_type='text/markdown',

    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "offlix=offlix_installer.installer:main"
        ]
    },
    include_package_data=True,
    package_data={
        "offlix": ["config.json"],
    },
    install_requires=[
        # List your dependencies here
        "docker",  # For example, if you need the Docker SDK
    ],
    python_requires='>=3.6', 
    description="Offlix is a command-line tool designed to simplify the deployment and management of common services using Docker Compose. With Offlix, you can easily install, uninstall, and retrieve environment variables for services like MySQL, MongoDB, Kafka, Maildev, and PostgreSQL, etc",
    author="Suman Manna",
    author_email="manna.suman134@gmail.com",
    url="https://github.com/sumanmanna134/offlix-cli",
)
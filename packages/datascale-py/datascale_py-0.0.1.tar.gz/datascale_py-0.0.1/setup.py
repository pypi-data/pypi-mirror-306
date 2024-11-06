from setuptools import setup, find_packages

setup(
    name="datascale-py",
    version="0.0.1",
    author="Your Name",
    author_email="your.email@example.com",
    description="A brief description of your package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/your_package_name",
    packages=find_packages(),
    install_requires=[
        # Add any package dependencies here, e.g., "requests>=2.20.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

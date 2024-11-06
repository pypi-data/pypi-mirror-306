from setuptools import setup, find_packages

setup(
    name="bioir",
    version="0.1.0",  # Incremented version number
    author="Your Name",
    author_email="your.email@example.com",
    description="A short description of your package",
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/irbio",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

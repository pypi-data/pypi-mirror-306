from setuptools import setup, find_packages

setup(
    name="ix_rest_tools",
    version="0.1.2",
    description="Python library for interacting with Beijer Electronics iX Web Server API.",
    long_description="Python wrapper for Beijer Electronics iX Web Server API",
    long_description_content_type="text/plain",
    url="https://github.com/Doscon-prime/ix_rest_tools",
    author="Your Name",
    author_email="aleksander@doscon.no",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
from setuptools import setup, find_packages

setup(
    name="llmrag",
    version="0.1.0",
    packages=find_packages(exclude=["tests*", "tools*"]),
    install_requires=[
        "click>=8.0.0",
        "tabulate>=0.8.0",
        "pandas>=1.0.0",
        "matplotlib>=3.0.0",
        "pytest>=6.0.0",
    ],
    author="Samaya Mantri",
    author_email="your.email@example.com",
    description="Ethical AI Query Processing Middleware",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/samayamantri/LLMRAG",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    include_package_data=True,
    package_data={
        "llmrag": ["ethical_guidelines.json"],
    },
) 
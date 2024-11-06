import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kreatornow",
    version="1.0.0",
    author="Sans",
    author_email="sans@kreator-inc.com",
    description="Kreatornow Open Service SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://open.kreatornow.com/",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests>=2.28.2',
        'urllib3>=1.26.3'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

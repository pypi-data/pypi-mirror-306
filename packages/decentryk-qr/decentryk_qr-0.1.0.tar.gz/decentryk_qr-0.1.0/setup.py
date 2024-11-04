from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="decentryk_qr",
    version="0.1.0",
    author="Zac Weigold",
    author_email="zacweigold@gmail.com",
    description="A package for combining and verifying QR codes using cryptographic hashes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "click>=7.1.2",
        "qrcode>=7.4.2",
        "Pillow>=10.0.0",
        "opencv-python>=4.8.0.74",
        "numpy>=1.24.3",
    ],
    entry_points={
        "console_scripts": [
            "decentryk_qr=decentryk_qr.cli:main",
        ],
    },
)
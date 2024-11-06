from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="google-analytics-django",
    version="0.1.2",
    description="A Django package to integrate Google Analytics seamlessly.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Adivhaho Mavhungu",
    author_email="adivhahomavhungu@outlook.com",
    maintainer="Adivhaho Mavhungu",
    maintainer_email="adivhahomavhungu@outlook.com",
    url="https://github.com/mavhungutrezzy/google-analytics-django",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "django>=5.0,<6.0",
    ],
    extras_require={
        "dev": [
            "coverage>=7.6.3",
            "djlint>=1.35.2",
            "pre-commit>=4.0.1",
            "ruff>=0.6.9",
            "setuptools>=75.2.0",
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
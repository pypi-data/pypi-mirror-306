from setuptools import setup, find_packages

setup(
    name="ugTranslate",
    version="0.2",
    description="A simple wrapper for translating text using Google Translate API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Siraj Dal",
    author_email="siraj.d.actowiz@gmail.com",
    packages=find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

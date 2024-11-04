from setuptools import setup, find_packages

setup(
    name="ugTranslate",
    version="0.1",
    description="A simple wrapper for translating text using Google Translate API",
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

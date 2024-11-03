from setuptools import setup, find_packages

setup(
    name="pyhttpsnippet",
    version="1.0.5",
    author="negative_boy",
    author_email="negativeres@gmail.com",
    description="A short description of your package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Mohammadwh/pyhttpsnippet/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

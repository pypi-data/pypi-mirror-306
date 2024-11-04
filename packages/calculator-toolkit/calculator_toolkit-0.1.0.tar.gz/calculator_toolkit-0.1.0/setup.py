from setuptools import setup, find_packages

setup(
 name="calculator_toolkit",
 version="0.1.0",
 author="Aakash Yadav",
 author_email="akasyadav483@gmail.com",
 description="A toolkit for basic geometric calculations",
 long_description=open("README.md").read(),
 long_description_content_type="text/markdown",
 url="https://github.com/aky483/geometry_toolkit",
 packages=find_packages(),
 classifiers=[
 "Programming Language :: Python :: 3",
 "License :: OSI Approved :: MIT License",
 "Operating System :: OS Independent",
 ],
 python_requires=">=3.6",
)
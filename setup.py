# -*- coding: utf-8 -*-
"""
Author: Tchicdje Kouojip Joram Smith (DeltaGa)
Created: Wed Aug 7, 2024
"""

from setuptools import setup, find_packages

setup(
    name="ctk_toggle",
    version="1.0.1",
    description="A lightweight Python package for creating toggle buttons and groups using CustomTkinter.",
    author="Tchicdje Kouojip Joram Smith (DeltaGa)",
    author_email="dev.github.tkjoramsmith@outlook.com",
    url="https://github.com/DeltaGa/ctk_toggle",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "customtkinter>=5.1.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    keywords="customtkinter tkinter toggle button UI",
    license="MIT",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
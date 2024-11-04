from setuptools import setup, find_packages

setup(
    name="simpleraycast",
    version="0.1.0",
    description="A simple raycasting engine for 2D games in Python using Pygame",
    author="Sten Nierop",
    packages=find_packages(),
    install_requires=["pygame"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)

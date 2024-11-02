from setuptools import setup, find_packages

setup(
    name="electrox",
    version="1.24.2",
    packages=find_packages(),
    install_requires=[
        'pygame',  # Make sure to install pygame for the game
    ],
    entry_points={
        'console_scripts': [
            'electrox = electrox.main:main',  # Specify main function within main.py
        ],
    },
    author="Hussain Luai",
    author_email="hxolotl15@gmail.com",
    description="Electrox is a Python framework for 2D game development with Gen Z and Gen Alpha vibes for some reason... nvm enjoy electrox.",
)
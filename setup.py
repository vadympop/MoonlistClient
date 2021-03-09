from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='moonlistclient',
    version='0.5.2',
    description='Wrapper for the moonlist api',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['moonlistclient'],
    author_email='zyzel19@gmail.com',
    url="https://github.com/VadyChel/MoonlistClient",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pydantic",
        "discord.py",
        "aiohttp"
    ]
)
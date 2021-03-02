from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mbc',
    version='0.2',
    description='Wrapper for the moonbots api',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['mbc'],
    author_email='zyzel19@gmail.com',
    url="https://github.com/VadyChel/MoonbotsClient",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU v3 License",
        "Operating System :: OS Independent",
    ]
)
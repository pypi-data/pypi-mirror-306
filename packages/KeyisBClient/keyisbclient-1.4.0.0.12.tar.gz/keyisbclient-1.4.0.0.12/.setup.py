from setuptools import setup

name = 'KeyisBClient'

setup(
    name=name,
    version='1.4.0.0.12',
    author="KeyisB",
    author_email="keyisb.pip@gmail.com",
    description=name,
    long_description='',
    long_description_content_type="text/markdown",
    url=f"https://github.com/KeyisB/libs/tree/main/{name}",
    packages=[name],
    package_dir={'': f'{name}'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
    license="MMB License v1.0",
    install_requires= ['KeyisBLogging', 'httpx'],
)

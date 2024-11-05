from setuptools import setup, find_packages

setup(
    name="spotless-manager",
    version="0.1.2",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "flask",
        "spotipy",
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "spotless-manager=spotless.main:main",
        ]
    },
    description="A tool to manage Spotify tracks, detect and delete duplicates",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/felixBorovikov/spotless",
    author="Felix Borovikov",
    author_email="felixborovikov@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
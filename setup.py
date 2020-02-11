import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ConvertV0-n8ta",  # Replace with your own username
    version="0.1",
    author="Nathaniel Tracy-Amoroso",
    author_email="n8@u.northwestern.edu",
    description="Simple tool to convert flac files into mp3[v0]",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['ffmpeg-python'],
)

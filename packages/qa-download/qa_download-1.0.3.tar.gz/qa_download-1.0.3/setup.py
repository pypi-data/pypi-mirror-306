from setuptools import setup, find_packages

setup(
    name="qa_download",
    version="1.0.3",
    author="Ahmed Qaddoura",
    author_email="aqaddora96@gmail.com",
    description="A tool for downloading music with embedded metadata and lyrics.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AQaddora/music_downloader",
    packages=find_packages(),
    install_requires=[
        "yt-dlp",
        "requests",
        "beautifulsoup4",
        "mutagen",
    ],
    entry_points={
        "console_scripts": [
            "music-downloader=music_downloader.downloader:main",
        ],
    },
    python_requires=">=3.7",
)

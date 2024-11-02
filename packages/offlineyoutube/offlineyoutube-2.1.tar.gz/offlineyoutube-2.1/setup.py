from setuptools import setup, find_packages

setup(
    name="offlineyoutube",
    version="2.01",
    packages=find_packages(include=["lib", "lib.*"]),
    include_package_data=True,
    install_requires=[
        "yt-dlp",
        "pandas",
        "numpy",
        "requests",
        "faiss-cpu",
        "faster-whisper",
        "sentence-transformers",
        "gradio==3.36.1",
        "argparse",
        "beautifulsoup4",
        "pysrt",
        "webvtt-py"
    ],
    entry_points={
        "console_scripts": [
            "offlineYoutube=app:main"
        ]
    },
    python_requires=">=3.8",
)

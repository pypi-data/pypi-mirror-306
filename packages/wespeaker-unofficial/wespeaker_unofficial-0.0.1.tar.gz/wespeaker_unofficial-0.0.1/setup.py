from setuptools import setup, find_packages

requirements = [
    "tqdm",
    "kaldiio",
    "hdbscan==0.8.37",
    "umap-learn==0.5.6",
    "torch>=1.12.0",
    "torchaudio>=0.12.0",
    "silero-vad",
]

setup(
    name="wespeaker-unofficial",
    description="Unofficial wespeaker pypi package",
    version="0.0.1",
    install_requires=requirements,
    packages=find_packages(),
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    entry_points={
        "console_scripts": [
            "wespeaker = wespeaker.cli.speaker:main",
        ]
    },
)

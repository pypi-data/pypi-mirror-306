from pathlib import Path
from setuptools import setup, find_packages

VERSION = '0.1.0'
DESCRIPTION = 'Slack Crash Alerter Client using Incoming Webhooks'

directory = Path(__file__).parent
LONG_DESCRIPTION = (directory / "README.md").read_text()

setup(
    name="slack_alerter",
    version=VERSION,
    author="Hritik Karwasra",
    author_email="khrithik0806@gmail.com",
    url="https://github.com/hritikkarwasra/slack-alerter",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(where="slack_alerter"),
    install_requires=["requests==2.*"],
    keywords=["python", "Slack", "Alerter", "Crash Alerter"],
    python_requires='>=3.8',
    classifiers=[
        "License :: OSI Approved :: MIT License", 
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    project_urls={
        "Documentation": "https://github.com/hritikkarwasra/slack-alerter",
        "Source": "https://github.com/hritikkarwasra/slack-alerter",
    },
    license="MIT"
)

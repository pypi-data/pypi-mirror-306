from setuptools import setup
from setuptools.command.install import install
import subprocess
import sys

# Custom command to download nltk data after installing nltk
class PostInstallCommand(install):
    def run(self):
        # Install nltk if it's not already installed
        subprocess.check_call([sys.executable, "-m", "pip", "install", "nltk"])
        import nltk
        nltk.download('punkt_tab')
        nltk.download('stopwords')
        install.run(self)

setup(
    name="nltk_punkt",
    version="0.6",
    packages=["nltk_punkt"],
    install_requires=[
        "nltk",
    ],
    cmdclass={
        'install': PostInstallCommand,
    },
)

"""Setup for the chocobo package."""

import setuptools, os

from setuptools.command.install import install

VERSION = "0.0.12"

with open('README.md') as f:
    README = f.read()

class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)

setuptools.setup(
    author="Elhanan Mishraky, Shir Lador, Aviv Benarie",
    author_email="elhanan_mishraky@intuit.com, shir_lador@intuit.com, aviv_benarie@intuit.com",
    name='bias-detector',
    license="MIT",
    description='Bias Detector is a python package for detecting bias in machine learning models',
    version=VERSION,
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/intuit/bias-detector',
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=['numpy==1.19.4', 'pandas==1.1.5', 'scikit-learn==0.23.2', 'matplotlib==3.3.3', 'scipy==1.5.4', 'surgeo==1.0.2', 'nltk==3.5'],
    setup_requires=["pytest-runner"],
    extras_require={
        'test': [
            'pytest'
        ],
    },
    tests_require=["pytest"],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    cmdclass={
        'verify': VerifyVersionCommand,
    }
)

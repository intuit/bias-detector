"""Setup for the chocobo package."""

import setuptools


with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Elhanan Mishraky, Shir Lador, Aviv Benarie",
    author_email="elhanan_mishraky@intuit.com, shir_lador@intuit.com, aviv_benarie@intuit.com",
    name='bias-detector',
    license="MIT",
    description='bias-detector detects bias in ML models',
    version='0.0.1',
    long_description=README,
    url='https://github.com/bias-detector',
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
)

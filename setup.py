import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='dnashrink-bioinfo',
    version='0.1.0',
    description='A Python implementation of the Burrows-Wheeler and Huffman coding algorithms',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Ouertani95/PROJET_ALGO',
    author='Ouertani-Mohamed',
    author_email = 'ouertani2006@gmail.com',
    download_url = 'https://github.com/Ouertani95/PROJET_ALGO/archive/refs/heads/master.zip',
    packages=setuptools.find_packages(include=['PROJET_ALGO','dnashrink', 'dnashrink.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
                    "setuptools==45.2.0",
                    "ttkthemes==3.2.2"
                      ],
    extras_require={
        'dev': [
            'pytest >= 6.0.0',
            'pytest-cov >= 2.10.0',
            'coveralls >= 2.1.2',
            'flake8 >= 3.8.0',
            'mock >= 4.0.0',
        ]
    },
    entry_points={
        'console_scripts': [
            'dnashrink=dnashrink.main:main'
        ]
    },
    python_requires='>=3.8',
)

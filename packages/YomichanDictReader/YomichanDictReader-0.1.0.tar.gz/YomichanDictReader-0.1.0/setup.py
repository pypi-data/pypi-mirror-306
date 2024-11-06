from setuptools import setup,find_packages



setup(
    name="YomichanDictReader",
    version="0.1.0",
    description="Yomichan dictionary reader",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Matt7677",
    author_email="contact.mattdev@gmail.com",
    packages=find_packages(),
    install_requires=[
        "tinydb"
    ],
    python_requires = '>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        "Operating System :: OS Independent"
    ]
)
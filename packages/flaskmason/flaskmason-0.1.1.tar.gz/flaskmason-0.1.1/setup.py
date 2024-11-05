from setuptools import setup, find_packages

setup(
    name="flaskmason",  # The name of your package
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "Flask>=2.0",            
        "Flask-SQLAlchemy>=2.5",
        "Flask-WTF>=0.15",
    ],
    entry_points={
        "console_scripts": [
            "flaskmason=flaskmason.generator:main",
        ],
    },
    author="Akash Nath",
    author_email="devakash2905@gmail.com",
    description="A CLI tool to generate a Django-like structure for Flask projects",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Akash-nath29/flaskgen",  # Optional, if hosted on GitHub
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

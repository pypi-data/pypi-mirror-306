# Setup file for pip installation
# Setup file for pip installation

from setuptools import setup, find_packages

# To Load the README file to use as the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sfn_blueprint",
    version="0.4.1",  # Initial release version
    author="Rajesh Darak",
    author_email="rajesh@stepfuction.ai",
    description="sfn-blueprint is a modular framework that enables rapid building of AI Agents, offering both flexibility and ease of customization.",
    long_description=long_description,  # Using README.md as long description
    long_description_content_type="text/markdown",  # README file format
    url="https://github.com/iamrajeshdaraksfn/sfn_blueprint",  # Github URL
    packages=find_packages(),  # This will Automatically find and include packages
    include_package_data=True,  # To Ensure non-Python files are included
    package_data={
        "sfn_blueprint": [
            "config/prompts_config.json",
            "config/config.json"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # License
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',  # Required Python version
    install_requires=[
        # List of dependencies required for this package
        'pandas',
        'numpy',
        'openai',
        'python-dotenv',
        'streamlit',
        'textblob',
        'scikit-learn',
        'nltk',
        'spacy'
        ]
)
from setuptools import setup, find_packages

# Read README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cwx-aiml-app-template",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'rich',
    ],
    entry_points={
        'console_scripts': [
            'aimlapp=cwx_aiml_app_template.cli:main',
        ],
    },
    # Add these parameters
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cwx-aiml-app-template",  # Add your repository URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
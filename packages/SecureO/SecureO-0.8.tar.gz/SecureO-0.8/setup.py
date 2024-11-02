from setuptools import setup, find_packages

setup(
    name="SecureO",  # Package name
    version="0.8",
    packages=find_packages(),
    install_requires=[
        "pymongo",
        "bcrypt",
        "tabulate",
    ],
    entry_points={
        "console_scripts": [
            "pm=pm.main:main",  # Command to run the tool
        ],
    },
    author="Yash Jain",
    author_email="yash.test.project@gmail.com",
    description="A command-line password manager",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/my_project",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

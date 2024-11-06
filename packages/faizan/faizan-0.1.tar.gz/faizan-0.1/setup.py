from setuptools import setup, find_packages

setup(
    name="faizan",  # Package name
    version="0.1",
    packages=find_packages(),  # Automatically finds the package folder
    install_requires=["colorama"],  # Dependency for color output
    entry_points={
        "console_scripts": [
            "faizan-xss=faizan.faizan:main",  # Link command to main function
        ],
    },
    author="Faizan Khan",
    author_email="fk776794@gmail.com",
    description="An advanced tool for detecting and analyzing potential XSS payloads.",
    long_description=(
        "The Faizan XSS Detector is a robust tool designed to help developers "
        "and security professionals detect potential Cross-Site Scripting (XSS) vulnerabilities. "
        "With comprehensive pattern matching and payload analysis, this tool can identify various forms "
        "of XSS attacks, including JavaScript injections, malicious HTML tags, and obfuscated code. "
        "By leveraging Colorama for a color-coded terminal output, users receive clear and actionable "
        "feedback for each payload tested. This makes the Faizan XSS Detector an essential addition "
        "to any developer's or pentester's toolkit."
    ),
    long_description_content_type="text/markdown",
    url="https://github.com/faizan-khanx/XSS-DETECTOR",  # Replace with your GitHub URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
    ],
    python_requires=">=3.6",
)

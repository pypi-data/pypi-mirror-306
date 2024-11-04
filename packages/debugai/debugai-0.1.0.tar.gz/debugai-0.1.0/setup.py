from setuptools import setup, find_packages

setup(
    name="debugai",
    version="0.1.0",
    author="Sami Halawa",
    description="AI-powered Python code analysis and improvement tool",
    long_description=open("docs/README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "click>=7.0",
        "ast-decompiler>=0.4.0",
        "aider-chat>=0.8.0",
        "pyyaml>=5.1",
        "chardet>=3.0",
        "psutil>=5.8",
        "ratelimit>=2.2",
        "aiofiles>=0.6.0",
        "asyncio>=3.4.3",
        "typing-extensions>=4.0.0",
        "streamlit>=1.24.0",
        "plotly>=5.13.0",
    ],
    extras_require={
        'dev': [
            'pytest>=6.0',
            'black>=21.0',
            'flake8>=3.9',
            'mypy>=0.910',
            'bandit>=1.7'
        ],
        'gui': [
            'streamlit>=1.24.0',
            'plotly>=5.13.0',
            'streamlit-ace>=0.1.1'
        ]
    },
    entry_points={
        'console_scripts': [
            'debugai=debugai.cli.commands:cli',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
) 
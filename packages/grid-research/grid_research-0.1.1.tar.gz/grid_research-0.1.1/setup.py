from setuptools import setup, find_packages

setup(
    name="grid-research",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "openai==1.52.2",
        "html2text",
        "python-dotenv",
        "aiohttp",
        "beautifulsoup4",
        "lxml",
        "fake-useragent",
        "pandas",
        "pydantic>=2.0.0",
    ],
    author="Your Name",
    author_email="minh@everythingcompany.co",
    description="A package for automated research data collection using LLMs and Web Search API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/bobcoi03/grid",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
)
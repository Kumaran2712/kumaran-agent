from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="kumaran-agent",
    version="0.1.0",
    author="Kumaran Sundarrajan",
    author_email="kumaran271296@gmail.com",
    description="An AI agent with chain of thought processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kumaran2712/kumaran-agent",
    packages=find_packages(),
    py_modules=["agent"],
    install_requires=[
        "openai>=1.54.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.9.0",
        "requests>=2.31.0",
    ],
    entry_points={
        'console_scripts': [
            'kumaran-agent=agent:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
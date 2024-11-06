from setuptools import setup, find_packages

setup(
    name="kwoq",
    version="0.1.5",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'scipy',
        'statsmodels',
        'seaborn',
        'scikit-learn',
        'requests',
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple data processing and visualization library",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
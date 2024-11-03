from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="schwab_api_lq",
    packages=find_packages(),
    version='0.0.2',  # 在这里设置版本号
    license="MIT",
    description="Unofficial Schwab API wrapper in Python 3.",
    author="LQEPOCH",
    author_email="lqepoch@gmail.com",
    url="https://github.com/lqepoch/schwab-api-lq",
    long_description=long_description,
    long_description_content_type="text/markdown",
    download_url="https://github.com/lqepoch/schwab-api-lq/tarball/main",
    keywords=["schwab", "python3", "api", "unofficial", "schwab-api", "schwab charles api"],
    install_requires=["playwright", "playwright-stealth", "pyotp", "python-vipaccess"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires='>=3.6',
)
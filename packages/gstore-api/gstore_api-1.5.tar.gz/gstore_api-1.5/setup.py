import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gstore_api",
    version="1.5",
    author="liwenjie",
    url='https://github.com/pkumod/gStore',
    author_email="liwenjiehn@pku.edu.cn",
    description="gstore_api是一个用于python链接gStore的工具类",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
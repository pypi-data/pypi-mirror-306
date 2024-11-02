from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    # Read specific lines or truncate content as needed
    long_description = "\n".join(fh.readlines()[:10])  # Adjust to include the desired portion

setup(
    name='learn_python_package_bhupesh',
    version='0.3',
    author="Bhupesh Tongaria",
    description="package created for learning purposes",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BhupeshTongaria/Learn_python_package/",
    install_requires=[],  # List any dependencies here
)
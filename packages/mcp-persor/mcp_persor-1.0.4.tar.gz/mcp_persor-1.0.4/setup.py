from setuptools import setup, find_packages
import mcp_persor

INSTALL_REQUIRES = [
    "numpy >= 1.25.2",
    "pandas >= 2.0.3",
    "matplotlib >= 3.8.1",
    "japanize_matplotlib >= 1.1.3",
]

setup(
    name="mcp_persor",
    version=mcp_persor.__version__,
    description="It parses bvh files so you can easily handle them.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="SatooRu",
    url="https://github.com/SatooRu65536/mcp_persor",
    download_url="https://github.com/SatooRu65536/mcp_persor",
    packages=find_packages(),
    license="MIT",
    python_requires=">=3.7",
    install_requires=INSTALL_REQUIRES,
)

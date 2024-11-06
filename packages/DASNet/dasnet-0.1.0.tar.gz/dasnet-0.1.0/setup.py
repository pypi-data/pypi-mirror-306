from setuptools import setup

setup(
    name="DASNet",
    version="0.1.0",
    long_description="DASNet",
    long_description_content_type="text/markdown",
    packages=["dasnet"],
    install_requires=["numpy",  "h5py", "matplotlib", "pandas"],
)

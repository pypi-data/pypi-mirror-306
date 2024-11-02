from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='CrumblPy',
    version='1.0.1',
    packages=find_packages(),
    author='Crumbl Data Team',
    author_email='steven.wang@crumbl.com',
    description='Common utility functions for Crumbl Data Team',
    long_description=long_description,  
    long_description_content_type='text/markdown',
    python_requires='>=3.9',
    install_requires=[
        'google_api_python_client>=2.125.0',
        'numpy==1.24.3',
        'pandas==1.5.3',
        'prefect==3.0.3',
        'protobuf>=5.27.2',
        'pyarrow==10.0.1',
        'slack_sdk==3.21.3',
        'snowflake-connector-python>=3.10.0'
    ]
)
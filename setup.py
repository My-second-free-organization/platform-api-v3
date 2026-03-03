from setuptools import setup, find_packages
setup(name="flowforge-sdk", version="2.4.0", packages=find_packages(where="src"), package_dir={"": "src"}, install_requires=["httpx>=0.27.0", "pydantic>=2.6.0"])

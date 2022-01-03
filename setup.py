from setuptools import setup, find_namespace_packages
import os

def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path)) as fp:
        return fp.read()

def get_version(rel_path: str) -> str:
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")

# long_description = read('README.md')

setup(
    name="pws-home",
	version=get_version("pws/home/__init__.py"),
	description="Home Automation API for Python",
	# long_description=long_description,
	classifiers=[
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
	],
	url="https://github.com/pwsnet/pws-home",
	packages=find_namespace_packages(
		include=["pws.*"]
	),
	python_requires=">=3.6",
    install_requires=[
		"uvicorn",
        "fastapi"
	]
)
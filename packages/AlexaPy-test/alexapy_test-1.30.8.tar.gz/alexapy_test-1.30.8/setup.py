from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="AlexaPy-test",  # Nombre del paquete para PyPI
    version="1.30.8",
    description="This is a forked version of AlexaPy. Just for my testing purposes. In oder to test some commits before asking for a pull request. The original code and package is property of alandtse and keatontaylor, and you can find it under AlexaPy. Python API to control Amazon Echo Devices Programmatically.",
    author="figorr",
    author_email="jdcuartero@yahoo.es",
    license="Apache-2.0",
    url="https://gitlab.com/figorr1/alexapy",
    packages=find_packages(),  # Encuentra automáticamente los subpaquetes
    include_package_data=True,  # Incluye otros archivos listados en MANIFEST.in
    long_description=long_description,  # Agrega la descripción larga
    long_description_content_type='text/markdown',  # Especifica el tipo de contenido
    install_requires=[
        "beautifulsoup4",
        "aiofiles>=23.1.0",
        "simplejson",
        "yarl",
        "requests",
        "certifi",
        "backoff>=1.10",
        "pyotp>=2.4",
        "authcaptureproxy>=1.3.2",
        "cryptography>=35.0",
        "aiohttp>=3.8.4",
        "httpx[http2]>=0.24.0",
    ],
    extras_require={
        "dev": [
            "aresponses",
            "detox",
            "flake8",
            "mypy",
            "pydocstyle",
            "pylint",
            "pytest-aiohttp",
            "pytest-cov",
            "python-semantic-release==7.28.1",
            "tox",
            "safety>=1.8.7",
            "black>19.10b0",
            "Sphinx>=3.5.0,<7.0.0",
            "autoapi>=2.0.1",
            "sphinx-rtd-theme>=0.5.1",
            "m2r2>=0.2.7",
            "tomlkit>=0.7.0",
            "sphinx-autoapi>=1.7.0",
            "sphinx-copybutton>=0.3.1",
            "pipdeptree>=2.2.1",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11, <4',
)

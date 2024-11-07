from setuptools import setup, find_packages

setup(
    name="genai-sdk",
    version="0.0.1",
    description="SDK de conexão com o mobileX GenAI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Luiz Carvalho",
    author_email="dev@mtmtecnologia.com.br",
    url="https://github.com/mobilex-neo/genai-sdk",
    packages=find_packages(),
    install_requires=[
        "requests>=2.26.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
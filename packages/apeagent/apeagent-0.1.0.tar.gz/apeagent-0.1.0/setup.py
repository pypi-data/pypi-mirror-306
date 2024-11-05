from setuptools import setup, find_packages

setup(
    name="apeagent",
    version="0.1.0",
    author="Macaque Consulting",
    author_email="marc.riera@macaqueconsulting.com",
    description="A simple framework to manage agents and tool-based functions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tu_usuario/apeagent",  # Cambia esto a tu repositorio
    packages=find_packages(),
    install_requires=open("requirements.txt").read().splitlines(),
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)

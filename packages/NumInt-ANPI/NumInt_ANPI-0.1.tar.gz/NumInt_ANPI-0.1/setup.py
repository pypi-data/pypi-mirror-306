# setup.py

from setuptools import setup, find_packages

setup(
    name="NumInt_ANPI",
    version="0.1",
    packages=find_packages(),
    description="Paquete computacional en Python para métodos de integración",
    author="",
    author_email="tu_correo@example.com",
    install_requires=["numpy","scipy"],
    python_requires=">=3.6"
)

from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Paquete computacional'
LONG_DESCRIPTION = 'Paquete computacional para Tarea 3 de ANPI 2024'

# Configurando
setup(
    name="NumIntKMC",
    version=VERSION,
    author="Kendall Fernandez,Meibel Mora,Christopher Castro",
    author_email="kefernandez@estudiantec.cr,chriscv1608@estudiantec.cr,meimora@estudiantec.cr",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],

    keywords=['python', 'ANPI'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
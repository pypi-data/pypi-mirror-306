from setuptools import setup, find_packages

VERSION = '1.0.1'
DESCRIPTION = 'Paquete computacional que permite aproximar el valor numérico de la integra definida'
LONG_DESCRIPTION = ('Los métodos incluidos son: regla del trapecio compuesto, '
                    'regla de Simpson compuesta, cuadratura gaussiana compuesta'
                    ', regla del trapecio compuesta iterativa y método de Romberg.')


setup(
    name="NumIntGrupo1",
    version=VERSION,
    author="Abraham Venegas",
    author_email="<abravenegas@estudiantec.cr>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy'], # Requiere numpy
    keywords=['python', 'NumInt', 'integración numérica'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
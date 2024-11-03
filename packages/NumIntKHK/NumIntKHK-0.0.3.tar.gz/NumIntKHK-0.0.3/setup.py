from setuptools import setup, find_packages

VERSION = '0.0.3' 
DESCRIPTION = 'Paquete NumInt diseñado para aproximar el valor numérico de una integral definida'
LONG_DESCRIPTION = 'Paquete NumInt diseñado para aproximar el valor numérico de una integral definida, con una función f continua en A y definida en un intervalo contenido en A.'

# Configurando
setup(
       # el nombre debe coincidir con el nombre de la carpeta 	  
       #'modulomuysimple'
        name="NumIntKHK", 
        version=VERSION,
        author="Marin Kendall, Nuñez Henry, Zheng Kun",
        author_email="<kendallmarin@estudiantec.cr, henunez@estudiantec.cr, kzheng@estudiantec.cr>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # añade cualquier paquete adicional que debe ser
        #instalado junto con tu paquete. Ej: 'caer'
        
        keywords=['python', 'primer paquete'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
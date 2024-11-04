from setuptools import setup, find_packages

# Lire le fichier README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='vcodeboot',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        "pygame",
        "pymsgbox",
    ],
    author='Victorio N.',
    author_email='victorio.nascimento@gmail.com',
    description='Fonctions de Codeboot 5.\n https://codeboot-org.github.io/presentations/',
    long_description=long_description,  # Ajout du README comme description longue
    long_description_content_type='text/markdown',
    url='https://github.com/Victorio-NASCIMENTO/Fonctions_Codeboot/tree/main',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
    ],
    python_requires='>=3.6',
)

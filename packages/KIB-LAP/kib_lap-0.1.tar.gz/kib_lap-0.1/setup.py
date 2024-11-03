
from setuptools import setup, find_packages

# Lesen der README-Datei (falls sie vorhanden ist)
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "KIB package description."

setup(
    name="KIB_LAP",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,  # Sorgt dafür, dass zusätzliche Dateien wie README.md enthalten sind
    description="A package for structural engineering calculations",  # Kurze Beschreibung
    long_description=long_description,  # Lange Beschreibung aus README.md
    long_description_content_type="text/markdown",  # Falls README.md im Markdown-Format ist
    author="leoth",
    author_email="thomas.leonard@outlook.de",
    license="MIT",  # Beispiel-Lizenz, kann angepasst werden

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Mindestanforderung an die Python-Version
    install_requires=[
        # Abhängigkeiten hier angeben
        # Beispiel: 'numpy>=1.18.0', 'scipy>=1.4.0'
    ],
)

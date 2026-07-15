from pathlib import Path

# Dossiers
directories = [
    "app/core",
    "app/models",
    "app/schemas",
    "app/routers",
    "app/services",
    "app/utils",
    "tests",
]

# Fichiers
files = [
    "app/main.py",

    "app/core/config.py",
    "app/core/database.py",

    "tests/__init__.py",

    ".env.example",
    ".gitignore",
    "requirements.txt",
    "README.md",
]

for directory in directories:
    Path(directory).mkdir(parents=True, exist_ok=True)


for file in files:
    Path(file).touch(exist_ok=True)

packages = [
    "app",
    "app/core",
    "app/models",
    "app/schemas",
    "app/routers",
    "app/services",
    "app/utils",
]

for package in packages:
    Path(package, "__init__.py").touch(exist_ok=True)

print("Structure créée avec succès !")
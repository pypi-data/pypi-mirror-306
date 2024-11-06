import os
import site
import subprocess
from datetime import datetime

import yaml


# Verifica se o pacote está instalado no site-packages
def get_config_template_path():
    try:
        # Tentativa de obter o caminho do site-packages
        site_package_path = site.getsitepackages()[0]
        config_template_path = os.path.join(site_package_path, "kumo", "template")

        # Verifica se o diretório existe
        if os.path.exists(config_template_path):
            return config_template_path
    except Exception as e:
        print(f"Erro ao acessar site-packages: {e}")

    # Se não encontrar, usa o caminho local
    base_dir = os.path.dirname(os.path.abspath(__package__))
    local_config_template_path = os.path.join(base_dir, "src", "kumo", "template")

    return local_config_template_path


# Função para obter o hash do commit do git
def get_git_commit_hash() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()


# Função para obter a tag atual do git (se houver)
def get_git_tag() -> str:
    try:
        return subprocess.check_output(["git", "describe", "--tags"]).decode().strip()
    except subprocess.CalledProcessError:
        return str(None)


# Função para obter o versionamento correto
def get_versioning(config_data: dict) -> str:
    # versioning = config_data['builder'].get('versioning', 'timestamp')
    versioning = config_data["builder"]
    print(versioning)

    if versioning == "timestamp":
        print(versioning)
        return datetime.now().strftime("%Y%m%d%H%M%S")
    elif versioning == "hash":
        return get_git_commit_hash()
    elif versioning == "tag":
        tag = get_git_tag()
        if not tag:
            raise ValueError("Nenhuma tag encontrada no repositório Git.")
        return tag
    else:
        raise ValueError(f"Tipo de versionamento desconhecido: {versioning}")


# Função para ler o arquivo YAML
def read_config(config_file: str) -> dict:
    with open(config_file, "r") as file:
        return yaml.safe_load(file)

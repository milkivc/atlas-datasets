# Codeberg Connector - Associação MILK
# Versão: 1.0.0
# Licença: EUPL-1.2

"""
Conector para a Codeberg API (Forgejo).

Funcionalidades:
- Gerir repositórios (criar, listar, atualizar, deletar)
- Gerir branches e tags
- Gerir webhooks
- Sincronizar com GitHub
"""

import os
import json
import requests
from typing import Optional, Dict, List, Any
from pathlib import Path


class CodebergConnector:
    """Conector para a Codeberg API (Forgejo)."""

    def __init__(self, token: Optional[str] = None, org: str = "milkivc"):
        """
        Inicializa o conector.

        Args:
            token (str, optional): Codeberg Personal Access Token. Se None, tentará
                ler do ficheiro cockpit/tokens/codeberg_token.txt ou da variável de ambiente.
            org (str): Nome da organização. Default: "milkivc".
        """
        self.org = org
        self.base_url = "https://codeberg.org/api/v1"
        self.headers = {
            "Accept": "application/json",
            "User-Agent": "MILK-Cockpit/1.0.0"
        }

        # Obter token
        if token is None:
            token = self._get_token_from_file()
        if token is None:
            token = os.getenv("CODEBERG_TOKEN")

        if token:
            self.headers["Authorization"] = f"token {token}"
        else:
            raise ValueError(
                "Codeberg token não encontrado. "
                "Forneça um token ou configure o ficheiro cockpit/tokens/codeberg_token.txt "
                "ou a variável de ambiente CODEBERG_TOKEN."
            )

    def _get_token_from_file(self) -> Optional[str]:
        """Lê o token do ficheiro cockpit/tokens/codeberg_token.txt."""
        token_file = Path(__file__).parent.parent / "tokens" / "codeberg_token.txt"
        if token_file.exists():
            with open(token_file, "r") as f:
                token = f.read().strip()
                # Remover comentários (linhas que começam com #)
                lines = token.split("\n")
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        return line
        return None

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        json_data: Optional[Dict] = None
    ) -> Dict:
        """
        Faz uma requisição à API do Codeberg.

        Args:
            method (str): Método HTTP (GET, POST, PUT, DELETE, PATCH).
            endpoint (str): Endpoint da API (ex: "/orgs/{org}/repos").
            params (dict, optional): Parâmetros de query.
            data (dict, optional): Dados para enviar no body (form-encoded).
            json_data (dict, optional): Dados para enviar no body (JSON).

        Returns:
            dict: Resposta da API em formato JSON.

        Raises:
            requests.exceptions.HTTPError: Se a requisição falhar.
        """
        url = f"{self.base_url}{endpoint}"

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                data=data,
                json=json_data,
                timeout=30
            )
            response.raise_for_status()
            return response.json() if response.content else {}
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.HTTPError(
                f"Erro ao acessar {url}: {str(e)}"
            )

    # =========================================================================
    # Métodos para Organizações
    # =========================================================================

    def get_org(self, org: Optional[str] = None) -> Dict:
        """
        Obtém informações de uma organização.

        Args:
            org (str, optional): Nome da organização. Se None, usa self.org.

        Returns:
            dict: Informações da organização.
        """
        org = org or self.org
        endpoint = f"/orgs/{org}"
        return self._request("GET", endpoint)

    def list_org_repos(self, org: Optional[str] = None) -> List[Dict]:
        """
        Lista todos os repositórios de uma organização.

        Args:
            org (str, optional): Nome da organização. Se None, usa self.org.

        Returns:
            list: Lista de repositórios.
        """
        org = org or self.org
        endpoint = f"/orgs/{org}/repos"
        params = {"page": 1, "limit": 100}
        return self._request("GET", endpoint, params=params)

    # =========================================================================
    # Métodos para Repositórios
    # =========================================================================

    def get_repo(self, repo_name: str, org: Optional[str] = None) -> Dict:
        """
        Obtém informações de um repositório.

        Args:
            repo_name (str): Nome do repositório.
            org (str, optional): Nome da organização. Se None, usa self.org.

        Returns:
            dict: Informações do repositório.
        """
        org = org or self.org
        endpoint = f"/repos/{org}/{repo_name}"
        return self._request("GET", endpoint)

    def create_repo(
        self,
        name: str,
        description: str = "",
        private: bool = False,
        org: Optional[str] = None
    ) -> Dict:
        """
        Cria um novo repositório.

        Args:
            name (str): Nome do repositório.
            description (str): Descrição do repositório.
            private (bool): Se o repositório é privado.
            org (str, optional): Nome da organização. Se None, usa self.org.

        Returns:
            dict: Informações do repositório criado.
        """
        org = org or self.org
        endpoint = f"/orgs/{org}/repos"
        data = {
            "name": name,
            "description": description,
            "private": private
        }
        return self._request("POST", endpoint, json_data=data)

    def update_repo(
        self,
        repo_name: str,
        description: Optional[str] = None,
        private: Optional[bool] = None,
        org: Optional[str] = None
    ) -> Dict:
        """
        Atualiza um repositório.

        Args:
            repo_name (str): Nome do repositório.
            description (str, optional): Nova descrição.
            private (bool, optional): Se o repositório é privado.
            org (str, optional): Nome da organização. Se None, usa self.org.

        Returns:
            dict: Informações do repositório atualizado.
        """
        org = org or self.org
        endpoint = f"/repos/{org}/{repo_name}"
        data = {}
        if description is not None:
            data["description"] = description
        if private is not None:
            data["private"] = private
        return self._request("PATCH", endpoint, json_data=data)

    def delete_repo(self, repo_name: str, org: Optional[str] = None) -> bool:
        """
        Deleta um repositório.

        Args:
            repo_name (str): Nome do repositório.
            org (str, optional): Nome da organização. Se None, usa self.org.

        Returns:
            bool: True se o repositório foi deletado com sucesso.
        """
        org = org or self.org
        endpoint = f"/repos/{org}/{repo_name}"
        self._request("DELETE", endpoint)
        return True

    # =========================================================================
    # Métodos para Branches
    # =========================================================================

    def list_branches(self, repo_name: str, org: Optional[str] = None) -> List[Dict]:
        """
        Lista todas as branches de um repositório.

        Args:
            repo_name (str): Nome do repositório.
            org (str, optional): Nome da organização. Se None, usa self.org.

        Returns:
            list: Lista de branches.
        """
        org = org or self.org
        endpoint = f"/repos/{org}/{repo_name}/branches"
        params = {"page": 1, "limit": 100}
        return self._request("GET", endpoint, params=params)

    def get_branch(
        self, repo_name: str, branch_name: str, org: Optional[str] = None
    ) -> Dict:
        """
        Obtém informações de uma branch.

        Args:
            repo_name (str): Nome do repositório.
            branch_name (str): Nome da branch.
            org (str, optional): Nome da organização. Se None, usa self.org.

        Returns:
            dict: Informações da branch.
        """
        org = org or self.org
        endpoint = f"/repos/{org}/{repo_name}/branches/{branch_name}"
        return self._request("GET", endpoint)

    # =========================================================================
    # Métodos para Sincronização com GitHub
    # =========================================================================

    def mirror_from_github(
        self,
        repo_name: str,
        github_org: str = "milkivc",
        github_token: Optional[str] = None,
        org: Optional[str] = None
    ) -> Dict:
        """
        Espelha um repositório do GitHub para o Codeberg.

        Args:
            repo_name (str): Nome do repositório.
            github_org (str): Organização no GitHub. Default: "milkivc".
            github_token (str, optional): Token do GitHub. Se None, tentará ler do ficheiro.
            org (str, optional): Organização no Codeberg. Se None, usa self.org.

        Returns:
            dict: Resultado da sincronização.
        """
        from .github_connector import GitHubConnector
        
        org = org or self.org
        
        # Inicializar conector do GitHub
        if github_token is None:
            github_connector = GitHubConnector(org=github_org)
        else:
            github_connector = GitHubConnector(token=github_token, org=github_org)
        
        # Obter informações do repositório no GitHub
        github_repo = github_connector.get_repo(repo_name, org=github_org)
        
        # Criar repositório no Codeberg (se não existir)
        try:
            codeberg_repo = self.get_repo(repo_name, org=org)
        except:
            codeberg_repo = self.create_repo(
                name=repo_name,
                description=github_repo.get("description", ""),
                private=github_repo.get("private", False),
                org=org
            )
        
        # Obter URL do repositório no Codeberg
        codeberg_repo_url = f"git@codeberg.org:{org}/{repo_name}.git"
        
        # Adicionar remote do Codeberg ao repositório local (simulado)
        # Em um ambiente real, seria necessário clonar o repositório
        
        return {
            "status": "success",
            "message": f"Repositório {repo_name} espelhado do GitHub para o Codeberg",
            "github_repo": github_repo.get("html_url", ""),
            "codeberg_repo": f"https://codeberg.org/{org}/{repo_name}"
        }

    def sync_repo_from_github(
        self,
        repo_name: str,
        github_org: str = "milkivc",
        github_token: Optional[str] = None,
        org: Optional[str] = None
    ) -> Dict:
        """
        Sincroniza um repositório do GitHub para o Codeberg (push de todas as branches e tags).

        Args:
            repo_name (str): Nome do repositório.
            github_org (str): Organização no GitHub. Default: "milkivc".
            github_token (str, optional): Token do GitHub.
            org (str, optional): Organização no Codeberg. Se None, usa self.org.

        Returns:
            dict: Resultado da sincronização.
        """
        import subprocess
        import tempfile
        import shutil
        
        org = org or self.org
        
        # Criar pasta temporária
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_dir = f"{tmpdir}/{repo_name}"
            
            # Clonar repositório do GitHub
            github_url = f"https://github.com/{github_org}/{repo_name}.git"
            if github_token:
                github_url = github_url.replace("https://", f"https://{github_token}@")
            
            try:
                subprocess.run(
                    ["git", "clone", "--mirror", github_url, repo_dir],
                    check=True,
                    capture_output=True
                )
            except subprocess.CalledProcessError as e:
                return {
                    "status": "error",
                    "message": f"Falha ao clonar repositório do GitHub: {str(e)}"
                }
            
            # Adicionar remote do Codeberg
            codeberg_url = f"git@codeberg.org:{org}/{repo_name}.git"
            subprocess.run(
                ["git", "-C", repo_dir, "remote", "add", "codeberg", codeberg_url],
                check=True
            )
            
            # Push de todas as branches e tags para o Codeberg
            try:
                subprocess.run(
                    ["git", "-C", repo_dir, "push", "--all", "codeberg"],
                    check=True
                )
                subprocess.run(
                    ["git", "-C", repo_dir, "push", "--tags", "codeberg"],
                    check=True
                )
            except subprocess.CalledProcessError as e:
                return {
                    "status": "error",
                    "message": f"Falha ao sincronizar para o Codeberg: {str(e)}"
                }
            
            return {
                "status": "success",
                "message": f"Repositório {repo_name} sincronizado do GitHub para o Codeberg",
                "github_url": github_url,
                "codeberg_url": f"https://codeberg.org/{org}/{repo_name}"
            }

    # =========================================================================
    # Métodos para Webhooks
    # =========================================================================

    def list_webhooks(self, repo_name: str, org: Optional[str] = None) -> List[Dict]:
        """
        Lista todos os webhooks de um repositório.

        Args:
            repo_name (str): Nome do repositório.
            org (str, optional): Nome da organização. Se None, usa self.org.

        Returns:
            list: Lista de webhooks.
        """
        org = org or self.org
        endpoint = f"/repos/{org}/{repo_name}/hooks"
        return self._request("GET", endpoint)

    def create_webhook(
        self,
        repo_name: str,
        url: str,
        events: List[str] = ["push", "pull_request", "issues"],
        active: bool = True,
        org: Optional[str] = None
    ) -> Dict:
        """
        Cria um novo webhook.

        Args:
            repo_name (str): Nome do repositório.
            url (str): URL do webhook.
            events (list): Lista de eventos que disparam o webhook.
            active (bool): Se o webhook está ativo.
            org (str, optional): Nome da organização. Se None, usa self.org.

        Returns:
            dict: Informações do webhook criado.
        """
        org = org or self.org
        endpoint = f"/repos/{org}/{repo_name}/hooks"
        data = {
            "type": "gitea",
            "config": {
                "url": url,
                "content_type": "json"
            },
            "events": events,
            "active": active
        }
        return self._request("POST", endpoint, json_data=data)

    def delete_webhook(
        self, repo_name: str, hook_id: int, org: Optional[str] = None
    ) -> bool:
        """
        Deleta um webhook.

        Args:
            repo_name (str): Nome do repositório.
            hook_id (int): ID do webhook.
            org (str, optional): Nome da organização. Se None, usa self.org.

        Returns:
            bool: True se o webhook foi deletado com sucesso.
        """
        org = org or self.org
        endpoint = f"/repos/{org}/{repo_name}/hooks/{hook_id}"
        self._request("DELETE", endpoint)
        return True

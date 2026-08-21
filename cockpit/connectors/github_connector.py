# GitHub Connector - Associação MILK
# Versão: 1.0.0
# Licença: EUPL-1.2

"""
Conector para a GitHub API v3.

Funcionalidades:
- Gerir repositórios (criar, listar, atualizar, deletar)
- Gerir branches e tags
- Gerir issues e pull requests
- Gerir webhooks
- Gerir workflows (GitHub Actions)
- Obter informações de organizações
"""

import os
import json
import requests
from typing import Optional, Dict, List, Any
from pathlib import Path


class GitHubConnector:
    """Conector para a GitHub API v3."""

    def __init__(self, token: Optional[str] = None, org: str = "milkivc"):
        """
        Inicializa o conector.

        Args:
            token (str, optional): GitHub Personal Access Token. Se None, tentará
                ler do ficheiro cockpit/tokens/github_token.txt ou da variável de ambiente.
            org (str): Nome da organização. Default: "milkivc".
        """
        self.org = org
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "MILK-Cockpit/1.0.0"
        }

        # Obter token
        if token is None:
            token = self._get_token_from_file()
        if token is None:
            token = os.getenv("GITHUB_TOKEN")

        if token:
            self.headers["Authorization"] = f"token {token}"
        else:
            raise ValueError(
                "GitHub token não encontrado. "
                "Forneça um token ou configure o ficheiro cockpit/tokens/github_token.txt "
                "ou a variável de ambiente GITHUB_TOKEN."
            )

    def _get_token_from_file(self) -> Optional[str]:
        """Lê o token do ficheiro cockpit/tokens/github_token.txt."""
        token_file = Path(__file__).parent.parent / "tokens" / "github_token.txt"
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
        Faz uma requisição à API do GitHub.

        Args:
            method (str): Método HTTP (GET, POST, PUT, DELETE, PATCH).
            endpoint (str): Endpoint da API (ex: "/repos/{org}/{repo}").
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
    # Métodos para Repositórios
    # =========================================================================

    def list_repos(self, org: Optional[str] = None) -> List[Dict]:
        """
        Lista todos os repositórios de uma organização.

        Args:
            org (str, optional): Nome da organização. Se None, usa self.org.

        Returns:
            list: Lista de repositórios.
        """
        org = org or self.org
        endpoint = f"/orgs/{org}/repos"
        params = {"type": "all", "per_page": 100}
        return self._request("GET", endpoint, params=params)

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
        license: str = "eupl-1.2",
        topics: Optional[List[str]] = None,
        org: Optional[str] = None
    ) -> Dict:
        """
        Cria um novo repositório.

        Args:
            name (str): Nome do repositório.
            description (str): Descrição do repositório.
            private (bool): Se o repositório é privado.
            license (str): Licença do repositório.
            topics (list, optional): Tópicos do repositório.
            org (str, optional): Nome da organização. Se None, usa self.org.

        Returns:
            dict: Informações do repositório criado.
        """
        org = org or self.org
        endpoint = f"/orgs/{org}/repos"
        data = {
            "name": name,
            "description": description,
            "private": private,
            "license_template": license,
            "topics": topics or []
        }
        return self._request("POST", endpoint, json_data=data)

    def update_repo(
        self,
        repo_name: str,
        description: Optional[str] = None,
        private: Optional[bool] = None,
        license: Optional[str] = None,
        topics: Optional[List[str]] = None,
        org: Optional[str] = None
    ) -> Dict:
        """
        Atualiza um repositório.

        Args:
            repo_name (str): Nome do repositório.
            description (str, optional): Nova descrição.
            private (bool, optional): Se o repositório é privado.
            license (str, optional): Nova licença.
            topics (list, optional): Novos tópicos.
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
        if license is not None:
            data["license_template"] = license
        if topics is not None:
            data["topics"] = topics
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
        params = {"per_page": 100}
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

    def create_branch(
        self, repo_name: str, branch_name: str, sha: str, org: Optional[str] = None
    ) -> Dict:
        """
        Cria uma nova branch.

        Args:
            repo_name (str): Nome do repositório.
            branch_name (str): Nome da nova branch.
            sha (str): SHA do commit base.
            org (str, optional): Nome da organização. Se None, usa self.org.

        Returns:
            dict: Informações da branch criada.
        """
        org = org or self.org
        endpoint = f"/repos/{org}/{repo_name}/git/refs"
        data = {
            "ref": f"refs/heads/{branch_name}",
            "sha": sha
        }
        return self._request("POST", endpoint, json_data=data)

    def delete_branch(
        self, repo_name: str, branch_name: str, org: Optional[str] = None
    ) -> bool:
        """
        Deleta uma branch.

        Args:
            repo_name (str): Nome do repositório.
            branch_name (str): Nome da branch.
            org (str, optional): Nome da organização. Se None, usa self.org.

        Returns:
            bool: True se a branch foi deletada com sucesso.
        """
        org = org or self.org
        endpoint = f"/repos/{org}/{repo_name}/git/refs/heads/{branch_name}"
        self._request("DELETE", endpoint)
        return True

    # =========================================================================
    # Métodos para Tags
    # =========================================================================

    def list_tags(self, repo_name: str, org: Optional[str] = None) -> List[Dict]:
        """
        Lista todas as tags de um repositório.

        Args:
            repo_name (str): Nome do repositório.
            org (str, optional): Nome da organização. Se None, usa self.org.

        Returns:
            list: Lista de tags.
        """
        org = org or self.org
        endpoint = f"/repos/{org}/{repo_name}/tags"
        params = {"per_page": 100}
        return self._request("GET", endpoint, params=params)

    def create_tag(
        self, repo_name: str, tag_name: str, message: str, sha: str, org: Optional[str] = None
    ) -> Dict:
        """
        Cria uma nova tag.

        Args:
            repo_name (str): Nome do repositório.
            tag_name (str): Nome da tag.
            message (str): Mensagem da tag.
            sha (str): SHA do commit.
            org (str, optional): Nome da organização. Se None, usa self.org.

        Returns:
            dict: Informações da tag criada.
        """
        org = org or self.org
        endpoint = f"/repos/{org}/{repo_name}/git/tags"
        data = {
            "tag": tag_name,
            "message": message,
            "object": sha,
            "type": "commit"
        }
        return self._request("POST", endpoint, json_data=data)

    def create_release(
        self, repo_name: str, tag_name: str, name: str, body: str = "", org: Optional[str] = None
    ) -> Dict:
        """
        Cria um release a partir de uma tag.

        Args:
            repo_name (str): Nome do repositório.
            tag_name (str): Nome da tag.
            name (str): Nome do release.
            body (str): Descrição do release.
            org (str, optional): Nome da organização. Se None, usa self.org.

        Returns:
            dict: Informações do release criado.
        """
        org = org or self.org
        endpoint = f"/repos/{org}/{repo_name}/releases"
        data = {
            "tag_name": tag_name,
            "name": name,
            "body": body
        }
        return self._request("POST", endpoint, json_data=data)

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
            "name": "web",
            "active": active,
            "events": events,
            "config": {
                "url": url,
                "content_type": "json"
            }
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

    # =========================================================================
    # Métodos para Workflows (GitHub Actions)
    # =========================================================================

    def list_workflows(self, repo_name: str, org: Optional[str] = None) -> List[Dict]:
        """
        Lista todos os workflows de um repositório.

        Args:
            repo_name (str): Nome do repositório.
            org (str, optional): Nome da organização. Se None, usa self.org.

        Returns:
            list: Lista de workflows.
        """
        org = org or self.org
        endpoint = f"/repos/{org}/{repo_name}/actions/workflows"
        return self._request("GET", endpoint)

    def get_workflow(
        self, repo_name: str, workflow_id: str, org: Optional[str] = None
    ) -> Dict:
        """
        Obtém informações de um workflow.

        Args:
            repo_name (str): Nome do repositório.
            workflow_id (str): ID do workflow.
            org (str, optional): Nome da organização. Se None, usa self.org.

        Returns:
            dict: Informações do workflow.
        """
        org = org or self.org
        endpoint = f"/repos/{org}/{repo_name}/actions/workflows/{workflow_id}"
        return self._request("GET", endpoint)

    def create_workflow_file(
        self, repo_name: str, workflow_path: str, content: str, org: Optional[str] = None
    ) -> Dict:
        """
        Cria ou atualiza um ficheiro de workflow.

        Args:
            repo_name (str): Nome do repositório.
            workflow_path (str): Caminho do ficheiro (ex: ".github/workflows/test.yml").
            content (str): Conteúdo do ficheiro.
            org (str, optional): Nome da organização. Se None, usa self.org.

        Returns:
            dict: Informações do commit.
        """
        org = org or self.org
        endpoint = f"/repos/{org}/{repo_name}/contents/{workflow_path}"
        # Obter SHA do ficheiro existente (se houver)
        try:
            existing = self._request("GET", endpoint)
            sha = existing.get("sha", None)
        except:
            sha = None

        data = {
            "message": f"Update workflow: {workflow_path}",
            "content": content,
            "encoding": "base64"
        }
        if sha:
            data["sha"] = sha

        return self._request("PUT", endpoint, json_data=data)

    # =========================================================================
    # Métodos para Issues e Pull Requests
    # =========================================================================

    def list_issues(
        self, repo_name: str, state: str = "open", org: Optional[str] = None
    ) -> List[Dict]:
        """
        Lista todas as issues de um repositório.

        Args:
            repo_name (str): Nome do repositório.
            state (str): Estado das issues (open, closed, all).
            org (str, optional): Nome da organização. Se None, usa self.org.

        Returns:
            list: Lista de issues.
        """
        org = org or self.org
        endpoint = f"/repos/{org}/{repo_name}/issues"
        params = {"state": state, "per_page": 100}
        return self._request("GET", endpoint, params=params)

    def create_issue(
        self,
        repo_name: str,
        title: str,
        body: str = "",
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None,
        org: Optional[str] = None
    ) -> Dict:
        """
        Cria uma nova issue.

        Args:
            repo_name (str): Nome do repositório.
            title (str): Título da issue.
            body (str): Descrição da issue.
            labels (list, optional): Rótulos da issue.
            assignees (list, optional): Usuários atribuídos.
            org (str, optional): Nome da organização. Se None, usa self.org.

        Returns:
            dict: Informações da issue criada.
        """
        org = org or self.org
        endpoint = f"/repos/{org}/{repo_name}/issues"
        data = {
            "title": title,
            "body": body,
            "labels": labels or [],
            "assignees": assignees or []
        }
        return self._request("POST", endpoint, json_data=data)

    # =========================================================================
    # Métodos para Conteúdo de Repositórios
    # =========================================================================

    def get_file_content(
        self, repo_name: str, file_path: str, org: Optional[str] = None
    ) -> Dict:
        """
        Obtém o conteúdo de um ficheiro.

        Args:
            repo_name (str): Nome do repositório.
            file_path (str): Caminho do ficheiro.
            org (str, optional): Nome da organização. Se None, usa self.org.

        Returns:
            dict: Conteúdo e metadados do ficheiro.
        """
        org = org or self.org
        endpoint = f"/repos/{org}/{repo_name}/contents/{file_path}"
        return self._request("GET", endpoint)

    def create_or_update_file(
        self, repo_name: str, file_path: str, content: str, message: str, org: Optional[str] = None
    ) -> Dict:
        """
        Cria ou atualiza um ficheiro.

        Args:
            repo_name (str): Nome do repositório.
            file_path (str): Caminho do ficheiro.
            content (str): Conteúdo do ficheiro.
            message (str): Mensagem do commit.
            org (str, optional): Nome da organização. Se None, usa self.org.

        Returns:
            dict: Informações do commit.
        """
        org = org or self.org
        endpoint = f"/repos/{org}/{repo_name}/contents/{file_path}"
        
        # Obter SHA do ficheiro existente (se houver)
        try:
            existing = self._request("GET", endpoint)
            sha = existing.get("sha", None)
        except:
            sha = None

        import base64
        encoded_content = base64.b64encode(content.encode()).decode()
        
        data = {
            "message": message,
            "content": encoded_content,
            "encoding": "base64"
        }
        if sha:
            data["sha"] = sha

        return self._request("PUT", endpoint, json_data=data)

    def delete_file(
        self, repo_name: str, file_path: str, message: str, org: Optional[str] = None
    ) -> bool:
        """
        Deleta um ficheiro.

        Args:
            repo_name (str): Nome do repositório.
            file_path (str): Caminho do ficheiro.
            message (str): Mensagem do commit.
            org (str, optional): Nome da organização. Se None, usa self.org.

        Returns:
            bool: True se o ficheiro foi deletado com sucesso.
        """
        org = org or self.org
        endpoint = f"/repos/{org}/{repo_name}/contents/{file_path}"
        
        # Obter SHA do ficheiro
        existing = self._request("GET", endpoint)
        sha = existing.get("sha")
        
        data = {
            "message": message,
            "sha": sha
        }
        self._request("DELETE", endpoint, json_data=data)
        return True

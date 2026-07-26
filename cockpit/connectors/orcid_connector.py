# ORCID Connector - Associação MILK
# Versão: 1.0.0
# Licença: EUPL-1.2

"""
Conector para a ORCID API v3.

Funcionalidades:
- Obter informações de perfis ORCID
- Adicionar/atualizar publicações
- Gerir afiliações
- Pesquisar perfis
"""

import os
import json
import requests
from typing import Optional, Dict, List, Any
from pathlib import Path


class ORCIDConnector:
    """Conector para a ORCID API v3."""

    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None):
        """
        Inicializa o conector.

        Args:
            client_id (str, optional): ORCID Client ID. Se None, tentará
                ler do ficheiro cockpit/tokens/orcid_token.txt ou da variável de ambiente.
            client_secret (str, optional): ORCID Client Secret. Se None, tentará
                ler do ficheiro cockpit/tokens/orcid_token.txt ou da variável de ambiente.
        """
        self.base_url = "https://api.orcid.org/v3.0"
        self.public_api_url = "https://pub.orcid.org/v3.0"
        self.headers = {
            "Accept": "application/json",
            "User-Agent": "MILK-Cockpit/1.0.0"
        }

        # Obter credenciais
        if client_id is None or client_secret is None:
            client_id, client_secret = self._get_credentials_from_file()
        if client_id is None:
            client_id = os.getenv("ORCID_CLIENT_ID")
        if client_secret is None:
            client_secret = os.getenv("ORCID_CLIENT_SECRET")

        if not client_id or not client_secret:
            raise ValueError(
                "ORCID credentials não encontradas. "
                "Forneça client_id e client_secret ou configure o ficheiro "
                "cockpit/tokens/orcid_token.txt ou as variáveis de ambiente "
                "ORCID_CLIENT_ID e ORCID_CLIENT_SECRET."
            )

        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None

    def _get_credentials_from_file(self) -> tuple:
        """Lê as credenciais do ficheiro cockpit/tokens/orcid_token.txt."""
        token_file = Path(__file__).parent.parent / "tokens" / "orcid_token.txt"
        if token_file.exists():
            with open(token_file, "r") as f:
                content = f.read().strip()
                # Parsar LINHA1=valor1, LINHA2=valor2
                lines = content.split("\n")
                client_id = None
                client_secret = None
                for line in lines:
                    line = line.strip()
                    if line.startswith("CLIENT_ID="):
                        client_id = line.split("=", 1)[1].strip()
                    elif line.startswith("CLIENT_SECRET="):
                        client_secret = line.split("=", 1)[1].strip()
                return client_id, client_secret
        return None, None

    def _get_access_token(self) -> str:
        """
        Obtém um access token usando OAuth2 Client Credentials Flow.

        Returns:
            str: Access token.
        """
        if self.access_token:
            return self.access_token

        token_url = "https://orcid.org/oauth/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
            "scope": "/read-limited /activities/update"
        }

        try:
            response = requests.post(
                token_url,
                data=data,
                headers={"Accept": "application/json"},
                timeout=30
            )
            response.raise_for_status()
            token_data = response.json()
            self.access_token = token_data.get("access_token")
            return self.access_token
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.HTTPError(
                f"Erro ao obter access token: {str(e)}"
            )

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        use_public_api: bool = False
    ) -> Dict:
        """
        Faz uma requisição à API do ORCID.

        Args:
            method (str): Método HTTP (GET, POST, PUT, DELETE, PATCH).
            endpoint (str): Endpoint da API (ex: "/0000-0000-0000-0000").
            params (dict, optional): Parâmetros de query.
            data (dict, optional): Dados para enviar no body (form-encoded).
            json_data (dict, optional): Dados para enviar no body (JSON).
            use_public_api (bool): Se deve usar a API pública (sem autenticação).

        Returns:
            dict: Resposta da API em formato JSON.

        Raises:
            requests.exceptions.HTTPError: Se a requisição falhar.
        """
        base = self.public_api_url if use_public_api else self.base_url
        url = f"{base}{endpoint}"

        headers = self.headers.copy()
        if not use_public_api:
            access_token = self._get_access_token()
            headers["Authorization"] = f"Bearer {access_token}"

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
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
    # Métodos para Perfis
    # =========================================================================

    def get_profile(self, orcid_id: str, use_public_api: bool = True) -> Dict:
        """
        Obtém informações de um perfil ORCID.

        Args:
            orcid_id (str): ORCID iD (ex: "0000-0000-0000-0000").
            use_public_api (bool): Se deve usar a API pública. Default: True.

        Returns:
            dict: Informações do perfil.
        """
        endpoint = f"/{orcid_id}"
        return self._request("GET", endpoint, use_public_api=use_public_api)

    def search_profiles(self, query: str, rows: int = 10) -> Dict:
        """
        Pesquisa perfis ORCID.

        Args:
            query (str): Termo de pesquisa.
            rows (int): Número de resultados.

        Returns:
            dict: Resultados da pesquisa.
        """
        endpoint = "/search"
        params = {"q": query, "rows": rows}
        return self._request("GET", endpoint, params=params, use_public_api=True)

    # =========================================================================
    # Métodos para Publicações (Works)
    # =========================================================================

    def list_works(self, orcid_id: str) -> List[Dict]:
        """
        Lista todas as publicações (works) de um perfil ORCID.

        Args:
            orcid_id (str): ORCID iD.

        Returns:
            list: Lista de publicações.
        """
        endpoint = f"/{orcid_id}/works"
        response = self._request("GET", endpoint)
        return response.get("items", [])

    def get_work(self, orcid_id: str, work_id: str) -> Dict:
        """
        Obtém informações de uma publicação.

        Args:
            orcid_id (str): ORCID iD.
            work_id (str): ID da publicação.

        Returns:
            dict: Informações da publicação.
        """
        endpoint = f"/{orcid_id}/works/{work_id}"
        return self._request("GET", endpoint)

    def add_work(
        self,
        orcid_id: str,
        title: str,
        work_type: str,
        url: str,
        journal_title: Optional[str] = None,
        publication_date: Optional[Dict] = None,
        **kwargs
    ) -> Dict:
        """
        Adiciona uma publicação a um perfil ORCID.

        Args:
            orcid_id (str): ORCID iD.
            title (str): Título da publicação.
            work_type (str): Tipo de publicação (ex: "journal-article", "dataset").
            url (str): URL da publicação.
            journal_title (str, optional): Título do jornal (se aplicável).
            publication_date (dict, optional): Data de publicação.
            **kwargs: Campos adicionais.

        Returns:
            dict: Informações da publicação criada.
        """
        endpoint = f"/{orcid_id}/works"
        
        # Construir payload
        payload = {
            "title": {"title": {"value": title}},
            "type": work_type,
            "url": {"value": url}
        }
        
        if journal_title:
            payload["journal-title"] = {"value": journal_title}
        if publication_date:
            payload["publication-date"] = publication_date
        
        # Adicionar campos adicionais
        for key, value in kwargs.items():
            payload[key] = value
        
        return self._request("POST", endpoint, json_data=payload)

    def update_work(
        self,
        orcid_id: str,
        work_id: str,
        title: Optional[str] = None,
        work_type: Optional[str] = None,
        url: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """
        Atualiza uma publicação.

        Args:
            orcid_id (str): ORCID iD.
            work_id (str): ID da publicação.
            title (str, optional): Novo título.
            work_type (str, optional): Novo tipo.
            url (str, optional): Nova URL.
            **kwargs: Campos adicionais.

        Returns:
            dict: Informações da publicação atualizada.
        """
        endpoint = f"/{orcid_id}/works/{work_id}"
        
        # Obter publicação atual
        current_work = self.get_work(orcid_id, work_id)
        
        # Construir payload com atualizações
        payload = current_work.copy()
        
        if title is not None:
            payload["title"] = {"title": {"value": title}}
        if work_type is not None:
            payload["type"] = work_type
        if url is not None:
            payload["url"] = {"value": url}
        
        # Adicionar campos adicionais
        for key, value in kwargs.items():
            payload[key] = value
        
        return self._request("PUT", endpoint, json_data=payload)

    def delete_work(self, orcid_id: str, work_id: str) -> bool:
        """
        Deleta uma publicação.

        Args:
            orcid_id (str): ORCID iD.
            work_id (str): ID da publicação.

        Returns:
            bool: True se a publicação foi deletada com sucesso.
        """
        endpoint = f"/{orcid_id}/works/{work_id}"
        self._request("DELETE", endpoint)
        return True

    # =========================================================================
    # Métodos para Afiliações
    # =========================================================================

    def list_affiliations(self, orcid_id: str) -> List[Dict]:
        """
        Lista todas as afiliações de um perfil ORCID.

        Args:
            orcid_id (str): ORCID iD.

        Returns:
            list: Lista de afiliações.
        """
        endpoint = f"/{orcid_id}/employments"
        response = self._request("GET", endpoint)
        return response.get("affiliation-group", [])

    def add_affiliation(
        self,
        orcid_id: str,
        organization_name: str,
        role_title: str,
        start_date: Dict,
        end_date: Optional[Dict] = None,
        **kwargs
    ) -> Dict:
        """
        Adiciona uma afiliação a um perfil ORCID.

        Args:
            orcid_id (str): ORCID iD.
            organization_name (str): Nome da organização.
            role_title (str): Cargo.
            start_date (dict): Data de início.
            end_date (dict, optional): Data de fim.
            **kwargs: Campos adicionais.

        Returns:
            dict: Informações da afiliação criada.
        """
        endpoint = f"/{orcid_id}/employments"
        
        payload = {
            "employment-summary": {
                "organization": {"name": organization_name},
                "role-title": role_title,
                "start-date": start_date
            }
        }
        
        if end_date:
            payload["employment-summary"]["end-date"] = end_date
        
        # Adicionar campos adicionais
        for key, value in kwargs.items():
            payload["employment-summary"][key] = value
        
        return self._request("POST", endpoint, json_data=payload)

    # =========================================================================
    # Métodos para Identificadores Externos
    # =========================================================================

    def list_external_identifiers(self, orcid_id: str) -> List[Dict]:
        """
        Lista todos os identificadores externos de um perfil ORCID.

        Args:
            orcid_id (str): ORCID iD.

        Returns:
            list: Lista de identificadores externos.
        """
        endpoint = f"/{orcid_id}/external-identifiers"
        response = self._request("GET", endpoint)
        return response.get("external-identifier-group", [])

    def add_external_identifier(
        self,
        orcid_id: str,
        identifier_type: str,
        identifier_value: str,
        url: Optional[str] = None
    ) -> Dict:
        """
        Adiciona um identificador externo a um perfil ORCID.

        Args:
            orcid_id (str): ORCID iD.
            identifier_type (str): Tipo de identificador (ex: "ROR").
            identifier_value (str): Valor do identificador.
            url (str, optional): URL associada.

        Returns:
            dict: Informações do identificador criado.
        """
        endpoint = f"/{orcid_id}/external-identifiers"
        
        payload = {
            "external-identifier": {
                "external-identifier-type": identifier_type,
                "external-identifier-value": identifier_value
            }
        }
        
        if url:
            payload["external-identifier"]["external-identifier-url"] = {"value": url}
        
        return self._request("POST", endpoint, json_data=payload)

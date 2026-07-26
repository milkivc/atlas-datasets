# DataCite Connector - Associação MILK
# Versão: 1.0.0
# Licença: EUPL-1.2

"""
Conector para a DataCite API.

Funcionalidades:
- Registar DOIs
- Atualizar DOIs
- Listar DOIs
- Obter metadados de DOIs
"""

import os
import json
import requests
from typing import Optional, Dict, List, Any
from pathlib import Path


class DataCiteConnector:
    """Conector para a DataCite API."""

    def __init__(self, token: Optional[str] = None, prefix: str = "10.5281"):
        """
        Inicializa o conector.

        Args:
            token (str, optional): DataCite API Token. Se None, tentará
                ler do ficheiro cockpit/tokens/datacite_token.txt ou da variável de ambiente.
            prefix (str): Prefixo DOI. Default: "10.5281".
        """
        self.prefix = prefix
        self.base_url = "https://api.datacite.org"
        self.headers = {
            "Content-Type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json",
            "User-Agent": "MILK-Cockpit/1.0.0"
        }

        # Obter token
        if token is None:
            token = self._get_token_from_file()
        if token is None:
            token = os.getenv("DATACITE_TOKEN")

        if token:
            self.headers["Authorization"] = f"Bearer {token}"
        else:
            raise ValueError(
                "DataCite token não encontrado. "
                "Forneça um token ou configure o ficheiro cockpit/tokens/datacite_token.txt "
                "ou a variável de ambiente DATACITE_TOKEN."
            )

    def _get_token_from_file(self) -> Optional[str]:
        """Lê o token do ficheiro cockpit/tokens/datacite_token.txt."""
        token_file = Path(__file__).parent.parent / "tokens" / "datacite_token.txt"
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
        Faz uma requisição à API da DataCite.

        Args:
            method (str): Método HTTP (GET, POST, PUT, DELETE, PATCH).
            endpoint (str): Endpoint da API (ex: "/dois").
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
    # Métodos para DOIs
    # =========================================================================

    def register_doi(
        self,
        doi: str,
        title: str,
        creators: List[Dict],
        publisher: str,
        publication_year: str,
        resource_type: str = "Dataset",
        description: str = "",
        url: str = "",
        license: str = "EUPL-1.2",
        keywords: Optional[List[str]] = None,
        **kwargs
    ) -> Dict:
        """
        Regista um novo DOI.

        Args:
            doi (str): DOI a registar (ex: "10.5281/zenodo.1234567").
            title (str): Título do recurso.
            creators (list): Lista de criadores (dicts com name, orcid, etc.).
            publisher (str): Editor.
            publication_year (str): Ano de publicação.
            resource_type (str): Tipo de recurso (Dataset, Software, etc.).
            description (str): Descrição do recurso.
            url (str): URL do recurso.
            license (str): Licença do recurso.
            keywords (list, optional): Palavras-chave.
            **kwargs: Argumentos adicionais para metadados.

        Returns:
            dict: Informações do DOI registado.
        """
        endpoint = "/dois"
        
        # Construir payload
        payload = {
            "data": {
                "type": "dois",
                "attributes": {
                    "doi": doi,
                    "titles": [{"title": title}],
                    "creators": creators,
                    "publisher": publisher,
                    "publicationYear": publication_year,
                    "resourceType": resource_type,
                    "resourceTypeGeneral": resource_type,
                    "descriptions": [{"description": description, "descriptionType": "Abstract"}],
                    "url": url,
                    "rightsList": [{"rights": license, "rightsUri": "https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12"}],
                    "keywords": keywords or [],
                    **kwargs
                }
            }
        }
        
        return self._request("POST", endpoint, json_data=payload)

    def get_doi(self, doi: str) -> Dict:
        """
        Obtém informações de um DOI.

        Args:
            doi (str): DOI a consultar.

        Returns:
            dict: Informações do DOI.
        """
        endpoint = f"/dois/{doi}"
        return self._request("GET", endpoint)

    def update_doi(
        self,
        doi: str,
        title: Optional[str] = None,
        creators: Optional[List[Dict]] = None,
        publisher: Optional[str] = None,
        publication_year: Optional[str] = None,
        description: Optional[str] = None,
        url: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """
        Atualiza um DOI existente.

        Args:
            doi (str): DOI a atualizar.
            title (str, optional): Novo título.
            creators (list, optional): Nova lista de criadores.
            publisher (str, optional): Novo editor.
            publication_year (str, optional): Novo ano de publicação.
            description (str, optional): Nova descrição.
            url (str, optional): Nova URL.
            **kwargs: Argumentos adicionais para metadados.

        Returns:
            dict: Informações do DOI atualizado.
        """
        endpoint = f"/dois/{doi}"
        
        # Obter DOI atual
        current_doi = self.get_doi(doi)
        
        # Construir payload com atualizações
        payload = {
            "data": {
                "type": "dois",
                "id": doi,
                "attributes": current_doi.get("data", {}).get("attributes", {})
            }
        }
        
        # Atualizar campos
        if title is not None:
            payload["data"]["attributes"]["titles"] = [{"title": title}]
        if creators is not None:
            payload["data"]["attributes"]["creators"] = creators
        if publisher is not None:
            payload["data"]["attributes"]["publisher"] = publisher
        if publication_year is not None:
            payload["data"]["attributes"]["publicationYear"] = publication_year
        if description is not None:
            payload["data"]["attributes"]["descriptions"] = [{"description": description, "descriptionType": "Abstract"}]
        if url is not None:
            payload["data"]["attributes"]["url"] = url
        
        # Adicionar campos adicionais
        for key, value in kwargs.items():
            payload["data"]["attributes"][key] = value
        
        return self._request("PUT", endpoint, json_data=payload)

    def list_dois(self, prefix: Optional[str] = None, limit: int = 100) -> List[Dict]:
        """
        Lista todos os DOIs registados.

        Args:
            prefix (str, optional): Filtro por prefixo DOI.
            limit (int): Número máximo de resultados.

        Returns:
            list: Lista de DOIs.
        """
        endpoint = "/dois"
        params = {"page[size]": limit}
        if prefix:
            params["filter[doi]"] = f"{prefix}.*"
        
        response = self._request("GET", endpoint, params=params)
        return response.get("data", [])

    def delete_doi(self, doi: str) -> bool:
        """
        Deleta um DOI.

        Args:
            doi (str): DOI a deletar.

        Returns:
            bool: True se o DOI foi deletado com sucesso.
        """
        endpoint = f"/dois/{doi}"
        self._request("DELETE", endpoint)
        return True

    # =========================================================================
    # Métodos para Metadados
    # =========================================================================

    def validate_metadata(self, metadata: Dict) -> Dict:
        """
        Valida metadados DataCite.

        Args:
            metadata (dict): Metadados a validar.

        Returns:
            dict: Resultado da validação.
        """
        # Implementação de validação básica
        required_fields = ["doi", "titles", "creators", "publisher", "publicationYear"]
        missing_fields = []
        
        for field in required_fields:
            if field not in metadata.get("data", {}).get("attributes", {}):
                missing_fields.append(field)
        
        if missing_fields:
            return {
                "valid": False,
                "errors": [f"Campo obrigatório ausente: {field}" for field in missing_fields]
            }
        
        return {"valid": True, "errors": []}

    def generate_doi_metadata(
        self,
        title: str,
        creators: List[Dict],
        publisher: str,
        publication_year: str,
        resource_type: str = "Dataset",
        description: str = "",
        url: str = "",
        license: str = "EUPL-1.2",
        keywords: Optional[List[str]] = None
    ) -> Dict:
        """
        Gera metadados DataCite para um DOI.

        Args:
            title (str): Título do recurso.
            creators (list): Lista de criadores.
            publisher (str): Editor.
            publication_year (str): Ano de publicação.
            resource_type (str): Tipo de recurso.
            description (str): Descrição do recurso.
            url (str): URL do recurso.
            license (str): Licença do recurso.
            keywords (list, optional): Palavras-chave.

        Returns:
            dict: Metadados DataCite.
        """
        return {
            "data": {
                "type": "dois",
                "attributes": {
                    "titles": [{"title": title}],
                    "creators": creators,
                    "publisher": publisher,
                    "publicationYear": publication_year,
                    "resourceType": resource_type,
                    "resourceTypeGeneral": resource_type,
                    "descriptions": [{"description": description, "descriptionType": "Abstract"}],
                    "url": url,
                    "rightsList": [{"rights": license, "rightsUri": "https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12"}],
                    "keywords": keywords or []
                }
            }
        }

    # =========================================================================
    # Métodos para Prefixos DOI
    # =========================================================================

    def list_prefixes(self) -> List[Dict]:
        """
        Lista todos os prefixos DOI associados à conta.

        Returns:
            list: Lista de prefixos.
        """
        endpoint = "/prefixes"
        return self._request("GET", endpoint)

    def get_prefix(self, prefix: str) -> Dict:
        """
        Obtém informações de um prefixo DOI.

        Args:
            prefix (str): Prefixo DOI.

        Returns:
            dict: Informações do prefixo.
        """
        endpoint = f"/prefixes/{prefix}"
        return self._request("GET", endpoint)

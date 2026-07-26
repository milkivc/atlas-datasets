#!/usr/bin/env python3
# Register DOIs - Associação MILK
# Versão: 1.0.0
# Licença: EUPL-1.2

"""
Script para registar DOIs para todos os datasets da Associação MILK.

Funcionalidades:
- Registar DOIs para todos os repositórios
- Registar DOI para repositório específico
- Listar DOIs registados
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional

# Adicionar pasta dos conectores ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "connectors"))

from datacite_connector import DataCiteConnector
from github_connector import GitHubConnector


class DOIRegister:
    """Classe para registar DOIs."""

    def __init__(self, datacite_token: Optional[str] = None, github_token: Optional[str] = None):
        """
        Inicializa o registo de DOIs.

        Args:
            datacite_token (str, optional): DataCite API Token.
            github_token (str, optional): GitHub PAT.
        """
        self.datacite = DataCiteConnector(token=datacite_token)
        self.github = GitHubConnector(token=github_token)
        
        # Carregar configurações
        self.configs_dir = Path(__file__).parent.parent / "configs"
        self.repos_list = self._load_repos_list()
        self.settings = self._load_settings()

    def _load_repos_list(self) -> List[Dict]:
        """Carrega a lista de repositórios."""
        repos_file = self.configs_dir / "repos_list.json"
        if repos_file.exists():
            with open(repos_file, "r", encoding="utf-8") as f:
                return json.load(f).get("repositories", [])
        return []

    def _load_settings(self) -> Dict:
        """Carrega as configurações gerais."""
        settings_file = self.configs_dir / "settings.json"
        if settings_file.exists():
            with open(settings_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _generate_doi(self, repo: Dict) -> str:
        """Gera um DOI para um repositório."""
        prefix = self.settings.get("doi", {}).get("prefix", "10.5281")
        shoulder = self.settings.get("doi", {}).get("shoulder", "zenodo")
        repo_name = repo.get("name", "").replace("-", "_").replace(".", "_")
        return f"{prefix}/{shoulder}.{repo_name}"

    def _get_repo_metadata(self, repo: Dict) -> Dict:
        """Obtém metadados de um repositório para registo de DOI."""
        repo_name = repo.get("name", "")
        org = "milkivc"
        
        # Obter informações do repositório do GitHub
        try:
            github_repo = self.github.get_repo(repo_name, org=org)
        except:
            github_repo = {}
        
        # Construir metadados para DataCite
        creators = []
        for author in self.settings.get("metadata", {}).get("co_authors", []):
            creators.append({
                "name": author.get("name", ""),
                "nameIdentifiers": [{
                    "nameIdentifier": author.get("orcid", "").split("/")[-1],
                    "nameIdentifierScheme": "ORCID",
                    "schemeUri": "https://orcid.org/"
                }],
                "affiliations": [{
                    "name": self.settings.get("organization", {}).get("name", ""),
                    "affiliationIdentifier": self.settings.get("organization", {}).get("ror_id", ""),
                    "affiliationIdentifierScheme": "ROR",
                    "schemeUri": "https://ror.org/"
                }]
            })
        
        metadata = {
            "doi": self._generate_doi(repo),
            "title": repo.get("description", ""),
            "creators": creators,
            "publisher": self.settings.get("organization", {}).get("name", ""),
            "publicationYear": "2026",
            "resourceType": repo.get("resource_type", "Dataset"),
            "resourceTypeGeneral": "Dataset",
            "description": repo.get("description", ""),
            "url": repo.get("github_url", ""),
            "license": repo.get("license", "EUPL-1.2"),
            "keywords": repo.get("topics", [])
        }
        
        return metadata

    def register_repo_doi(self, repo: Dict) -> Dict:
        """
        Regista um DOI para um repositório.

        Args:
            repo (dict): Informações do repositório.

        Returns:
            dict: Resultado do registo.
        """
        repo_name = repo.get("name", "")
        
        if not repo.get("has_doi", False):
            print(f"\n⏭️  Registo de DOI desativado para: {repo_name}")
            return {
                "status": "skipped",
                "repo": repo_name,
                "reason": "has_doi=false"
            }
        
        print(f"\n🆔 Registando DOI para: {repo_name}")
        
        try:
            # Gerar metadados
            metadata = self._get_repo_metadata(repo)
            doi = metadata.get("doi", "")
            
            print(f"  DOI: {doi}")
            
            # Verificar se o DOI já existe
            try:
                existing_doi = self.datacite.get_doi(doi)
                print(f"  ⚠️  DOI já existe: {doi}")
                return {
                    "status": "exists",
                    "repo": repo_name,
                    "doi": doi,
                    "url": existing_doi.get("data", {}).get("attributes", {}).get("url", "")
                }
            except:
                pass
            
            # Registar DOI
            result = self.datacite.register_doi(
                doi=doi,
                title=metadata.get("title", ""),
                creators=metadata.get("creators", []),
                publisher=metadata.get("publisher", ""),
                publication_year=metadata.get("publicationYear", "2026"),
                resource_type=metadata.get("resourceType", "Dataset"),
                description=metadata.get("description", ""),
                url=metadata.get("url", ""),
                license=metadata.get("license", "EUPL-1.2"),
                keywords=metadata.get("keywords", [])
            )
            
            print(f"  ✅ DOI registado: {doi}")
            
            # Atualizar metadados do repositório com o DOI
            self._update_repo_with_doi(repo, doi)
            
            return {
                "status": "success",
                "repo": repo_name,
                "doi": doi,
                "url": f"https://doi.org/{doi}"
            }
            
        except Exception as e:
            print(f"  ❌ Erro ao registar DOI: {str(e)}")
            return {
                "status": "error",
                "repo": repo_name,
                "error": str(e)
            }

    def _update_repo_with_doi(self, repo: Dict, doi: str) -> None:
        """
        Atualiza os metadados do repositório com o DOI.

        Args:
            repo (dict): Informações do repositório.
            doi (str): DOI registado.
        """
        repo_name = repo.get("name", "")
        org = "milkivc"
        
        try:
            # Atualizar CITATION.cff
            cff_content = self.github.get_file_content(repo_name, "CITATION.cff", org=org)
            cff = cff_content.get("content", "")
            
            # Decodificar conteúdo (base64)
            import base64
            cff_decoded = base64.b64decode(cff).decode("utf-8") if cff else ""
            
            # Adicionar DOI
            if "identifiers:" not in cff_decoded:
                cff_decoded += "\nidentifiers:\n"
            if f"- type: \"doi\"\n    value: \"{doi}\"" not in cff_decoded:
                cff_decoded += f"  - type: \"doi\"\n    value: \"{doi}\"\n"
            
            # Atualizar ficheiro
            self.github.create_or_update_file(
                repo_name=repo_name,
                file_path="CITATION.cff",
                content=cff_decoded,
                message=f"🤖 Adiciona DOI: {doi}",
                org=org
            )
            print(f"  ✅ CITATION.cff atualizado com DOI")
            
        except Exception as e:
            print(f"  ⚠️  Erro ao atualizar CITATION.cff: {str(e)}")

    def register_all_dois(self) -> Dict:
        """
        Regista DOIs para todos os repositórios.

        Returns:
            dict: Resultado do registo de DOIs.
        """
        print("\n" + "="*60)
        print("🆔 COCKPIT - REGISTO DE DOIs")
        print("="*60)
        
        results = {}
        for repo in self.repos_list:
            results[repo.get("name", "")] = self.register_repo_doi(repo)
        
        print("\n" + "="*60)
        print("✅ REGISTO DE DOIs CONCLUÍDO")
        print("="*60)
        
        return results

    def list_registered_dois(self) -> List[Dict]:
        """
        Lista todos os DOIs registados.

        Returns:
            list: Lista de DOIs registados.
        """
        print("\n📋 Listando DOIs registados...")
        dois = self.datacite.list_dois(prefix=self.settings.get("doi", {}).get("prefix", "10.5281"))
        print(f"  ✅ Encontrados {len(dois)} DOIs")
        return dois


def main():
    """Função principal."""
    parser = argparse.ArgumentParser(
        description="Regista DOIs para repositórios"
    )
    parser.add_argument(
        "--repo",
        type=str,
        help="Nome do repositório para registar DOI (opcional)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Registar DOIs para todos os repositórios"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Listar DOIs registados"
    )
    
    args = parser.parse_args()
    
    # Inicializar registo de DOIs
    doi_register = DOIRegister()
    
    if args.list:
        # Listar DOIs registados
        dois = doi_register.list_registered_dois()
        for doi in dois:
            print(f"\n  - {doi.get('id')}")
            print(f"    Title: {doi.get('attributes', {}).get('titles', [{}])[0].get('title')}")
            print(f"    URL: {doi.get('attributes', {}).get('url')}")
    elif args.all:
        # Registar DOIs para todos os repositórios
        results = doi_register.register_all_dois()
    elif args.repo:
        # Registar DOI para repositório específico
        repo = next((r for r in doi_register.repos_list if r.get("name") == args.repo), None)
        if repo:
            results = {args.repo: doi_register.register_repo_doi(repo)}
        else:
            print(f"❌ Repositório não encontrado: {args.repo}")
            sys.exit(1)
    else:
        print("❌ Especifique --repo, --all ou --list")
        sys.exit(1)
    
    # Salvar relatório (se não for listagem)
    if not args.list:
        report = {
            "timestamp": "2026-07-26",
            "action": "register_dois",
            "results": results
        }
        
        report_file = Path(__file__).parent.parent / "reports" / "doi_report.json"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Relatório guardado em: {report_file}")
        
        # Mostrar resumo
        success_count = sum(1 for r in results.values() if r.get("status") == "success")
        exists_count = sum(1 for r in results.values() if r.get("status") == "exists")
        error_count = sum(1 for r in results.values() if r.get("status") == "error")
        skipped_count = sum(1 for r in results.values() if r.get("status") == "skipped")
        
        print(f"\n📊 Resumo:")
        print(f"   ✅ Sucesso: {success_count}")
        print(f"   ℹ️  Já existem: {exists_count}")
        print(f"   ❌ Erros: {error_count}")
        print(f"   ⏭️  Pulados: {skipped_count}")


if __name__ == "__main__":
    main()

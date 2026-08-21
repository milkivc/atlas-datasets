#!/usr/bin/env python3
# Sync GitHub to Codeberg - Associação MILK
# Versão: 1.0.0
# Licença: EUPL-1.2

"""
Script para sincronizar repositórios do GitHub para o Codeberg.

Funcionalidades:
- Sincronizar todos os repositórios
- Sincronizar repositório específico
- Sincronizar branches e tags
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional

# Adicionar pasta dos conectores ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "connectors"))

from github_connector import GitHubConnector
from codeberg_connector import CodebergConnector


class RepoSync:
    """Classe para sincronizar repositórios."""

    def __init__(self, github_token: Optional[str] = None, codeberg_token: Optional[str] = None):
        """
        Inicializa a sincronização.

        Args:
            github_token (str, optional): GitHub PAT.
            codeberg_token (str, optional): Codeberg PAT.
        """
        self.github = GitHubConnector(token=github_token)
        self.codeberg = CodebergConnector(token=codeberg_token)
        
        # Carregar configurações
        self.configs_dir = Path(__file__).parent.parent / "configs"
        self.repos_list = self._load_repos_list()

    def _load_repos_list(self) -> List[Dict]:
        """Carrega a lista de repositórios."""
        repos_file = self.configs_dir / "repos_list.json"
        if repos_file.exists():
            with open(repos_file, "r", encoding="utf-8") as f:
                return json.load(f).get("repositories", [])
        return []

    def sync_repo(
        self,
        repo_name: str,
        github_org: str = "milkivc",
        codeberg_org: str = "milkivc"
    ) -> Dict:
        """
        Sincroniza um repositório do GitHub para o Codeberg.

        Args:
            repo_name (str): Nome do repositório.
            github_org (str): Organização no GitHub.
            codeberg_org (str): Organização no Codeberg.

        Returns:
            dict: Resultado da sincronização.
        """
        print(f"\n🔄 Sincronizando: {github_org}/{repo_name} → {codeberg_org}/{repo_name}")
        
        try:
            # Verificar se o repositório existe no GitHub
            github_repo = self.github.get_repo(repo_name, org=github_org)
            print(f"  ✅ Repositório encontrado no GitHub")
            
            # Verificar se o repositório existe no Codeberg
            try:
                codeberg_repo = self.codeberg.get_repo(repo_name, org=codeberg_org)
                print(f"  ✅ Repositório encontrado no Codeberg")
            except:
                # Criar repositório no Codeberg
                codeberg_repo = self.codeberg.create_repo(
                    name=repo_name,
                    description=github_repo.get("description", ""),
                    private=github_repo.get("private", False),
                    org=codeberg_org
                )
                print(f"  ✅ Repositório criado no Codeberg")
            
            # Sincronizar usando o método do CodebergConnector
            result = self.codeberg.sync_repo_from_github(
                repo_name=repo_name,
                github_org=github_org,
                org=codeberg_org
            )
            
            if result.get("status") == "success":
                print(f"  ✅ Sincronização concluída")
                return {
                    "status": "success",
                    "repo": repo_name,
                    "github_url": github_repo.get("html_url", ""),
                    "codeberg_url": f"https://codeberg.org/{codeberg_org}/{repo_name}"
                }
            else:
                print(f"  ❌ Erro na sincronização: {result.get('message')}")
                return {
                    "status": "error",
                    "repo": repo_name,
                    "error": result.get("message", "Erro desconhecido")
                }
                
        except Exception as e:
            print(f"  ❌ Erro ao sincronizar: {str(e)}")
            return {
                "status": "error",
                "repo": repo_name,
                "error": str(e)
            }

    def sync_all_repos(
        self,
        github_org: str = "milkivc",
        codeberg_org: str = "milkivc"
    ) -> Dict:
        """
        Sincroniza todos os repositórios do GitHub para o Codeberg.

        Args:
            github_org (str): Organização no GitHub.
            codeberg_org (str): Organização no Codeberg.

        Returns:
            dict: Resultado da sincronização de todos os repositórios.
        """
        print("\n" + "="*60)
        print("🔄 COCKPIT - SINCRONIZAÇÃO DE TODOS OS REPOSITÓRIOS")
        print("="*60)
        
        results = {}
        for repo in self.repos_list:
            repo_name = repo.get("name", "")
            if repo.get("sync_to_codeberg", True):
                results[repo_name] = self.sync_repo(
                    repo_name=repo_name,
                    github_org=github_org,
                    codeberg_org=codeberg_org
                )
            else:
                print(f"\n⏭️  Sincronização desativada para: {repo_name}")
                results[repo_name] = {"status": "skipped", "reason": "sync_to_codeberg=false"}
        
        print("\n" + "="*60)
        print("✅ SINCRONIZAÇÃO CONCLUÍDA")
        print("="*60)
        
        return results


def main():
    """Função principal."""
    parser = argparse.ArgumentParser(
        description="Sincroniza repositórios do GitHub para o Codeberg"
    )
    parser.add_argument(
        "--repo",
        type=str,
        help="Nome do repositório a sincronizar (opcional)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Sincronizar todos os repositórios"
    )
    parser.add_argument(
        "--github-org",
        type=str,
        default="milkivc",
        help="Organização no GitHub (default: milkivc)"
    )
    parser.add_argument(
        "--codeberg-org",
        type=str,
        default="milkivc",
        help="Organização no Codeberg (default: milkivc)"
    )
    
    args = parser.parse_args()
    
    # Inicializar sincronização
    sync = RepoSync()
    
    if args.all:
        # Sincronizar todos os repositórios
        results = sync.sync_all_repos(
            github_org=args.github_org,
            codeberg_org=args.codeberg_org
        )
    elif args.repo:
        # Sincronizar repositório específico
        results = {
            args.repo: sync.sync_repo(
                repo_name=args.repo,
                github_org=args.github_org,
                codeberg_org=args.codeberg_org
            )
        }
    else:
        print("❌ Especifique --repo ou --all")
        sys.exit(1)
    
    # Salvar relatório
    report = {
        "timestamp": "2026-07-26",
        "action": "sync",
        "results": results
    }
    
    report_file = Path(__file__).parent.parent / "reports" / "sync_report.json"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Relatório guardado em: {report_file}")
    
    # Mostrar resumo
    success_count = sum(1 for r in results.values() if r.get("status") == "success")
    error_count = sum(1 for r in results.values() if r.get("status") == "error")
    skipped_count = sum(1 for r in results.values() if r.get("status") == "skipped")
    
    print(f"\n📊 Resumo:")
    print(f"   ✅ Sucesso: {success_count}")
    print(f"   ❌ Erros: {error_count}")
    print(f"   ⏭️  Pulados: {skipped_count}")


if __name__ == "__main__":
    main()

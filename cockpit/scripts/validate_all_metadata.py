#!/usr/bin/env python3
# Validate All Metadata - Associação MILK
# Versão: 1.0.0
# Licença: EUPL-1.2

"""
Script para validar todos os metadados dos repositórios da Associação MILK.

Funcionalidades:
- Validar CITATION.cff
- Validar codemeta.json
- Validar datacite.json
- Validar schema.org.json
- Validar conformidade com FAIR Principles
- Validar conformidade legal (RGPD, AI Act, EUPL-1.2)
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
from datacite_connector import DataCiteConnector


class MetadataValidator:
    """Classe para validar metadados."""

    def __init__(self, github_token: Optional[str] = None, datacite_token: Optional[str] = None):
        """
        Inicializa a validação.

        Args:
            github_token (str, optional): GitHub PAT.
            datacite_token (str, optional): DataCite API Token.
        """
        self.github = GitHubConnector(token=github_token)
        self.datacite = DataCiteConnector(token=datacite_token)
        
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

    def validate_cff(self, repo: Dict) -> Dict:
        """
        Valida o ficheiro CITATION.cff de um repositório.

        Args:
            repo (dict): Informações do repositório.

        Returns:
            dict: Resultado da validação.
        """
        repo_name = repo.get("name", "")
        org = "milkivc"
        
        print(f"\n📄 Validando CITATION.cff para: {org}/{repo_name}")
        
        try:
            # Obter conteúdo do ficheiro
            content = self.github.get_file_content(repo_name, "CITATION.cff", org=org)
            cff_content = content.get("content", "")
            
            # Decodificar conteúdo (base64)
            import base64
            cff_decoded = base64.b64decode(cff_content).decode("utf-8") if cff_content else ""
            
            # Validar campos obrigatórios
            required_fields = [
                "cff-version",
                "title",
                "authors",
                "version",
                "license"
            ]
            
            missing_fields = []
            for field in required_fields:
                if field not in cff_decoded:
                    missing_fields.append(field)
            
            if missing_fields:
                print(f"  ❌ Campos obrigatórios ausentes: {', '.join(missing_fields)}")
                return {
                    "status": "error",
                    "repo": repo_name,
                    "file": "CITATION.cff",
                    "errors": [f"Campo ausente: {field}" for field in missing_fields]
                }
            
            # Validar formato CFF
            lines = cff_decoded.split("\n")
            if not lines[0].startswith("cff-version:"):
                print(f"  ❌ Formato inválido: Primeira linha deve ser 'cff-version:'")
                return {
                    "status": "error",
                    "repo": repo_name,
                    "file": "CITATION.cff",
                    "errors": ["Formato inválido: Primeira linha deve ser 'cff-version:'"]
                }
            
            print(f"  ✅ CITATION.cff válido")
            return {
                "status": "success",
                "repo": repo_name,
                "file": "CITATION.cff",
                "errors": []
            }
            
        except Exception as e:
            print(f"  ❌ Erro ao validar CITATION.cff: {str(e)}")
            return {
                "status": "error",
                "repo": repo_name,
                "file": "CITATION.cff",
                "errors": [str(e)]
            }

    def validate_codemeta(self, repo: Dict) -> Dict:
        """
        Valida o ficheiro codemeta.json de um repositório.

        Args:
            repo (dict): Informações do repositório.

        Returns:
            dict: Resultado da validação.
        """
        repo_name = repo.get("name", "")
        org = "milkivc"
        
        print(f"\n📄 Validando codemeta.json para: {org}/{repo_name}")
        
        try:
            # Obter conteúdo do ficheiro
            content = self.github.get_file_content(repo_name, "codemeta.json", org=org)
            codemeta_content = content.get("content", "")
            
            # Decodificar conteúdo (base64)
            import base64
            codemeta_decoded = base64.b64decode(codemeta_content).decode("utf-8") if codemeta_content else ""
            
            # Validar JSON
            import json
            try:
                codemeta = json.loads(codemeta_decoded)
            except json.JSONDecodeError as e:
                print(f"  ❌ JSON inválido: {str(e)}")
                return {
                    "status": "error",
                    "repo": repo_name,
                    "file": "codemeta.json",
                    "errors": [f"JSON inválido: {str(e)}"]
                }
            
            # Validar campos obrigatórios
            required_fields = ["name", "description", "license", "author"]
            missing_fields = []
            for field in required_fields:
                if field not in codemeta:
                    missing_fields.append(field)
            
            if missing_fields:
                print(f"  ❌ Campos obrigatórios ausentes: {', '.join(missing_fields)}")
                return {
                    "status": "error",
                    "repo": repo_name,
                    "file": "codemeta.json",
                    "errors": [f"Campo ausente: {field}" for field in missing_fields]
                }
            
            print(f"  ✅ codemeta.json válido")
            return {
                "status": "success",
                "repo": repo_name,
                "file": "codemeta.json",
                "errors": []
            }
            
        except Exception as e:
            print(f"  ❌ Erro ao validar codemeta.json: {str(e)}")
            return {
                "status": "error",
                "repo": repo_name,
                "file": "codemeta.json",
                "errors": [str(e)]
            }

    def validate_datacite(self, repo: Dict) -> Dict:
        """
        Valida o ficheiro datacite.json de um repositório.

        Args:
            repo (dict): Informações do repositório.

        Returns:
            dict: Resultado da validação.
        """
        repo_name = repo.get("name", "")
        org = "milkivc"
        
        print(f"\n📄 Validando datacite.json para: {org}/{repo_name}")
        
        try:
            # Obter conteúdo do ficheiro
            content = self.github.get_file_content(repo_name, "datacite.json", org=org)
            datacite_content = content.get("content", "")
            
            # Decodificar conteúdo (base64)
            import base64
            datacite_decoded = base64.b64decode(datacite_content).decode("utf-8") if datacite_content else ""
            
            # Validar JSON
            import json
            try:
                datacite = json.loads(datacite_decoded)
            except json.JSONDecodeError as e:
                print(f"  ❌ JSON inválido: {str(e)}")
                return {
                    "status": "error",
                    "repo": repo_name,
                    "file": "datacite.json",
                    "errors": [f"JSON inválido: {str(e)}"]
                }
            
            # Validar campos obrigatórios
            required_fields = ["identifier", "creators", "titles", "publisher", "publicationYear"]
            missing_fields = []
            for field in required_fields:
                if field not in datacite:
                    missing_fields.append(field)
            
            if missing_fields:
                print(f"  ❌ Campos obrigatórios ausentes: {', '.join(missing_fields)}")
                return {
                    "status": "error",
                    "repo": repo_name,
                    "file": "datacite.json",
                    "errors": [f"Campo ausente: {field}" for field in missing_fields]
                }
            
            # Validar com DataCite API
            try:
                validation = self.datacite.validate_metadata(datacite)
                if not validation.get("valid", False):
                    print(f"  ❌ Validação DataCite falhou: {', '.join(validation.get('errors', []))}")
                    return {
                        "status": "error",
                        "repo": repo_name,
                        "file": "datacite.json",
                        "errors": validation.get("errors", [])
                    }
            except:
                pass
            
            print(f"  ✅ datacite.json válido")
            return {
                "status": "success",
                "repo": repo_name,
                "file": "datacite.json",
                "errors": []
            }
            
        except Exception as e:
            print(f"  ❌ Erro ao validar datacite.json: {str(e)}")
            return {
                "status": "error",
                "repo": repo_name,
                "file": "datacite.json",
                "errors": [str(e)]
            }

    def validate_schema_org(self, repo: Dict) -> Dict:
        """
        Valida o ficheiro schema.org.json de um repositório.

        Args:
            repo (dict): Informações do repositório.

        Returns:
            dict: Resultado da validação.
        """
        repo_name = repo.get("name", "")
        org = "milkivc"
        
        print(f"\n📄 Validando schema.org.json para: {org}/{repo_name}")
        
        try:
            # Obter conteúdo do ficheiro
            content = self.github.get_file_content(repo_name, "schema.org.json", org=org)
            schema_content = content.get("content", "")
            
            # Decodificar conteúdo (base64)
            import base64
            schema_decoded = base64.b64decode(schema_content).decode("utf-8") if schema_content else ""
            
            # Validar JSON
            import json
            try:
                schema = json.loads(schema_decoded)
            except json.JSONDecodeError as e:
                print(f"  ❌ JSON inválido: {str(e)}")
                return {
                    "status": "error",
                    "repo": repo_name,
                    "file": "schema.org.json",
                    "errors": [f"JSON inválido: {str(e)}"]
                }
            
            # Validar campos obrigatórios
            required_fields = ["name", "description", "license", "creator"]
            missing_fields = []
            for field in required_fields:
                if field not in schema:
                    missing_fields.append(field)
            
            if missing_fields:
                print(f"  ❌ Campos obrigatórios ausentes: {', '.join(missing_fields)}")
                return {
                    "status": "error",
                    "repo": repo_name,
                    "file": "schema.org.json",
                    "errors": [f"Campo ausente: {field}" for field in missing_fields]
                }
            
            print(f"  ✅ schema.org.json válido")
            return {
                "status": "success",
                "repo": repo_name,
                "file": "schema.org.json",
                "errors": []
            }
            
        except Exception as e:
            print(f"  ❌ Erro ao validar schema.org.json: {str(e)}")
            return {
                "status": "error",
                "repo": repo_name,
                "file": "schema.org.json",
                "errors": [str(e)]
            }

    def validate_fair_principles(self, repo: Dict) -> Dict:
        """
        Valida conformidade com FAIR Principles.

        Args:
            repo (dict): Informações do repositório.

        Returns:
            dict: Resultado da validação.
        """
        repo_name = repo.get("name", "")
        org = "milkivc"
        
        print(f"\n🎯 Validando FAIR Principles para: {org}/{repo_name}")
        
        errors = []
        
        # Findable
        try:
            cff = self.github.get_file_content(repo_name, "CITATION.cff", org=org)
            if not cff:
                errors.append("CITATION.cff não encontrado (Findable)")
            else:
                cff_decoded = base64.b64decode(cff.get("content", "")).decode("utf-8")
                if "orcid.org" not in cff_decoded:
                    errors.append("ORCID não encontrado em CITATION.cff (Findable)")
        except:
            errors.append("CITATION.cff não encontrado (Findable)")
        
        # Accessible
        try:
            repo_info = self.github.get_repo(repo_name, org=org)
            if repo_info.get("private", False):
                errors.append("Repositório é privado (Accessible)")
        except:
            errors.append("Repositório não acessível (Accessible)")
        
        # Interoperable
        metadata_files = ["codemeta.json", "datacite.json", "schema.org.json"]
        for file in metadata_files:
            try:
                content = self.github.get_file_content(repo_name, file, org=org)
                if not content:
                    errors.append(f"{file} não encontrado (Interoperable)")
            except:
                errors.append(f"{file} não encontrado (Interoperable)")
        
        # Reusable
        try:
            cff = self.github.get_file_content(repo_name, "CITATION.cff", org=org)
            if cff:
                cff_decoded = base64.b64decode(cff.get("content", "")).decode("utf-8")
                if "license:" not in cff_decoded:
                    errors.append("Licença não encontrada em CITATION.cff (Reusable)")
        except:
            errors.append("Licença não encontrada (Reusable)")
        
        if errors:
            print(f"  ❌ Erros de conformidade FAIR:")
            for error in errors:
                print(f"     - {error}")
            return {
                "status": "error",
                "repo": repo_name,
                "principle": "FAIR",
                "errors": errors
            }
        
        print(f"  ✅ Conformidade FAIR validada")
        return {
            "status": "success",
            "repo": repo_name,
            "principle": "FAIR",
            "errors": []
        }

    def validate_legal_compliance(self, repo: Dict) -> Dict:
        """
        Valida conformidade legal (RGPD, AI Act, EUPL-1.2).

        Args:
            repo (dict): Informações do repositório.

        Returns:
            dict: Resultado da validação.
        """
        repo_name = repo.get("name", "")
        org = "milkivc"
        
        print(f"\n⚖️  Validando conformidade legal para: {org}/{repo_name}")
        
        errors = []
        
        # Verificar LEGAL.md
        try:
            legal = self.github.get_file_content(repo_name, "LEGAL.md", org=org)
            if not legal:
                errors.append("LEGAL.md não encontrado")
            else:
                legal_decoded = base64.b64decode(legal.get("content", "")).decode("utf-8")
                if "RGPD" not in legal_decoded and "GDPR" not in legal_decoded:
                    errors.append("RGPD/GDPR não mencionado em LEGAL.md")
                if "AI Act" not in legal_decoded:
                    errors.append("AI Act não mencionado em LEGAL.md")
                if "EUPL-1.2" not in legal_decoded:
                    errors.append("EUPL-1.2 não mencionado em LEGAL.md")
        except:
            errors.append("LEGAL.md não encontrado")
        
        # Verificar licença nos metadados
        try:
            cff = self.github.get_file_content(repo_name, "CITATION.cff", org=org)
            if cff:
                cff_decoded = base64.b64decode(cff.get("content", "")).decode("utf-8")
                if "license: EUPL-1.2" not in cff_decoded:
                    errors.append("Licença EUPL-1.2 não encontrada em CITATION.cff")
        except:
            pass
        
        if errors:
            print(f"  ❌ Erros de conformidade legal:")
            for error in errors:
                print(f"     - {error}")
            return {
                "status": "error",
                "repo": repo_name,
                "compliance": "legal",
                "errors": errors
            }
        
        print(f"  ✅ Conformidade legal validada")
        return {
            "status": "success",
            "repo": repo_name,
            "compliance": "legal",
            "errors": []
        }

    def validate_repo(self, repo: Dict) -> Dict:
        """
        Valida todos os metadados de um repositório.

        Args:
            repo (dict): Informações do repositório.

        Returns:
            dict: Resultado da validação.
        """
        repo_name = repo.get("name", "")
        
        print(f"\n{'='*60}")
        print(f"🔍 Validando metadados para: {repo_name}")
        print(f"{'='*60}")
        
        results = {
            "cff": self.validate_cff(repo),
            "codemeta": self.validate_codemeta(repo),
            "datacite": self.validate_datacite(repo),
            "schema_org": self.validate_schema_org(repo),
            "fair": self.validate_fair_principles(repo),
            "legal": self.validate_legal_compliance(repo)
        }
        
        # Verificar se todos os ficheiros são válidos
        all_valid = all(
            result.get("status") == "success" 
            for result in results.values()
        )
        
        if all_valid:
            print(f"\n✅ Todos os metadados são válidos para: {repo_name}")
        else:
            print(f"\n❌ Metadados inválidos para: {repo_name}")
        
        return results

    def validate_all_repos(self) -> Dict:
        """
        Valida todos os metadados de todos os repositórios.

        Returns:
            dict: Resultado da validação de todos os repositórios.
        """
        print("\n" + "="*60)
        print("🔍 COCKPIT - VALIDAÇÃO DE METADADOS")
        print("="*60)
        
        results = {}
        for repo in self.repos_list:
            results[repo.get("name", "")] = self.validate_repo(repo)
        
        print("\n" + "="*60)
        print("✅ VALIDAÇÃO CONCLUÍDA")
        print("="*60)
        
        return results


def main():
    """Função principal."""
    parser = argparse.ArgumentParser(
        description="Valida metadados dos repositórios"
    )
    parser.add_argument(
        "--repo",
        type=str,
        help="Nome do repositório a validar (opcional)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Validar todos os repositórios"
    )
    
    args = parser.parse_args()
    
    # Inicializar validação
    validator = MetadataValidator()
    
    if args.all:
        # Validar todos os repositórios
        results = validator.validate_all_repos()
    elif args.repo:
        # Validar repositório específico
        repo = next((r for r in validator.repos_list if r.get("name") == args.repo), None)
        if repo:
            results = {args.repo: validator.validate_repo(repo)}
        else:
            print(f"❌ Repositório não encontrado: {args.repo}")
            sys.exit(1)
    else:
        print("❌ Especifique --repo ou --all")
        sys.exit(1)
    
    # Salvar relatório
    report = {
        "timestamp": "2026-07-26",
        "action": "validate_metadata",
        "results": results
    }
    
    report_file = Path(__file__).parent.parent / "reports" / "validation_report.json"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Relatório guardado em: {report_file}")
    
    # Mostrar resumo
    total_errors = 0
    for repo_results in results.values():
        for validation in repo_results.values():
            if validation.get("status") == "error":
                total_errors += 1
    
    total_repos = len(results)
    valid_repos = total_repos - total_errors
    
    print(f"\n📊 Resumo:")
    print(f"   ✅ Repositórios válidos: {valid_repos}/{total_repos}")
    print(f"   ❌ Erros totais: {total_errors}")


if __name__ == "__main__":
    main()

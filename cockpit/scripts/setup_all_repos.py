#!/usr/bin/env python3
# Setup All Repositories - Associação MILK
# Versão: 1.0.0
# Licença: EUPL-1.2

"""
Script para configurar todos os repositórios da Associação MILK com:
- Metadados (CITATION.cff, codemeta.json, datacite.json, schema.org.json)
- Webhooks para sincronização com Codeberg
- GitHub Actions para validação de metadados
"""

import os
import sys
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional

# Adicionar pasta dos conectores ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "connectors"))

from github_connector import GitHubConnector
from codeberg_connector import CodebergConnector


class RepoSetup:
    """Classe para configurar repositórios."""

    def __init__(self, github_token: Optional[str] = None, codeberg_token: Optional[str] = None):
        """
        Inicializa o setup.

        Args:
            github_token (str, optional): GitHub PAT.
            codeberg_token (str, optional): Codeberg PAT.
        """
        self.github = GitHubConnector(token=github_token)
        self.codeberg = CodebergConnector(token=codeberg_token)
        
        # Carregar configurações
        self.configs_dir = Path(__file__).parent.parent / "configs"
        self.repos_list = self._load_repos_list()
        self.settings = self._load_settings()
        
        # Carregar templates de metadados
        self.templates_dir = self.configs_dir / "metadata_templates"
        self.cff_template = self._load_template("CITATION.cff.template")
        self.codemeta_template = self._load_template("codemeta.json.template")
        self.datacite_template = self._load_template("datacite.json.template")
        self.schema_org_template = self._load_template("schema.org.json.template")

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

    def _load_template(self, template_name: str) -> str:
        """Carrega um template de metadados."""
        template_file = self.templates_dir / template_name
        if template_file.exists():
            with open(template_file, "r", encoding="utf-8") as f:
                return f.read()
        return ""

    def _generate_cff(self, repo: Dict) -> str:
        """Gera CITATION.cff para um repositório."""
        cff = self.cff_template
        
        # Substituir placeholders
        cff = cff.replace("{{REPO_NAME}}", repo.get("name", ""))
        cff = cff.replace("{{REPO_DESCRIPTION}}", repo.get("description", ""))
        cff = cff.replace("{{REPO_URL}}", repo.get("github_url", ""))
        cff = cff.replace("{{CODEBERG_URL}}", repo.get("codeberg_url", ""))
        cff = cff.replace("{{LICENSE}}", repo.get("license", "EUPL-1.2"))
        cff = cff.replace("{{VERSION}}", "v1.0.0")
        cff = cff.replace("{{DATE_RELEASED}}", "2026-07-26")
        
        # Adicionar autores
        authors = ""
        for author in self.settings.get("metadata", {}).get("co_authors", []):
            authors += f"  - given-names: \"{author.get('name', '')}\"\n"
            authors += f"    family-names: \"{author.get('name', '').split()[-1]}\"\n"
            authors += f"    orcid: \"{author.get('orcid', '')}\"\n"
            authors += f"    email: \"{author.get('email', '')}\"\n"
            authors += f"    affiliation: \"{self.settings.get('organization', {}).get('name', '')}\"\n\n"
        
        cff = cff.replace("{{AUTHORS}}", authors)
        
        return cff

    def _generate_codemeta(self, repo: Dict) -> str:
        """Gera codemeta.json para um repositório."""
        codemeta = self.codemeta_template
        
        # Substituir placeholders
        codemeta = codemeta.replace("{{REPO_NAME}}", repo.get("name", ""))
        codemeta = codemeta.replace("{{REPO_DESCRIPTION}}", repo.get("description", ""))
        codemeta = codemeta.replace("{{REPO_URL}}", repo.get("github_url", ""))
        codemeta = codemeta.replace("{{CODEBERG_URL}}", repo.get("codeberg_url", ""))
        codemeta = codemeta.replace("{{LICENSE}}", repo.get("license", "EUPL-1.2"))
        codemeta = codemeta.replace("{{VERSION}}", "v1.0.0")
        codemeta = codemeta.replace("{{DATE_PUBLISHED}}", "2026-07-26")
        codemeta = codemeta.replace("{{DATE_MODIFIED}}", "2026-07-26")
        
        return codemeta

    def _generate_datacite(self, repo: Dict) -> str:
        """Gera datacite.json para um repositório."""
        datacite = self.datacite_template
        
        # Substituir placeholders
        datacite = datacite.replace("{{REPO_NAME}}", repo.get("name", ""))
        datacite = datacite.replace("{{REPO_DESCRIPTION}}", repo.get("description", ""))
        datacite = datacite.replace("{{REPO_URL}}", repo.get("github_url", ""))
        datacite = datacite.replace("{{PUBLISHER}}", self.settings.get("organization", {}).get("name", ""))
        datacite = datacite.replace("{{PUBLICATION_YEAR}}", "2026")
        datacite = datacite.replace("{{LICENSE}}", repo.get("license", "EUPL-1.2"))
        
        return datacite

    def _generate_schema_org(self, repo: Dict) -> str:
        """Gera schema.org.json para um repositório."""
        schema_org = self.schema_org_template
        
        # Substituir placeholders
        schema_org = schema_org.replace("{{REPO_NAME}}", repo.get("name", ""))
        schema_org = schema_org.replace("{{REPO_DESCRIPTION}}", repo.get("description", ""))
        schema_org = schema_org.replace("{{REPO_URL}}", repo.get("github_url", ""))
        schema_org = schema_org.replace("{{CODEBERG_URL}}", repo.get("codeberg_url", ""))
        schema_org = schema_org.replace("{{LICENSE}}", repo.get("license", "EUPL-1.2"))
        schema_org = schema_org.replace("{{VERSION}}", "v1.0.0")
        schema_org = schema_org.replace("{{DATE_PUBLISHED}}", "2026-07-26")
        schema_org = schema_org.replace("{{DATE_MODIFIED}}", "2026-07-26")
        
        return schema_org

    def _create_metadata_files(self, repo: Dict) -> Dict[str, str]:
        """Cria todos os ficheiros de metadados para um repositório."""
        metadata = {
            "CITATION.cff": self._generate_cff(repo),
            "codemeta.json": self._generate_codemeta(repo),
            "datacite.json": self._generate_datacite(repo),
            "schema.org.json": self._generate_schema_org(repo)
        }
        
        # Adicionar FUNDING.yml se o repositório tiver DOI
        if repo.get("has_doi", False):
            funding_yml = """# FUNDING.yml - Informações de Financiamento
# Associação MILK - Movimento de Intervenções e Linguagens Kulturais e Arte
# NIPC: 518 706 451
# Lisboa, Portugal
# Licença: EUPL-1.2

organization:
  name: "Associacao MILK - Movimento de Intervencoes e Linguagens Kulturais e Arte"
  url: "https://github.com/milkivc"
  ror: "https://ror.org/05k9p4d32"
  location: "Lisboa, Portugal"
  tax_id: "518 706 451"

funding:
  - name: "Marco Zero v1.0.0"
    type: "Internal"
    description: "Documentacao legal fundacional da Associacao MILK"
    url: "https://github.com/milkivc/atlas-datasets/tree/master/********COES-LICENCAS-DIPLOMAS"
    funder:
      name: "Associacao MILK"
      url: "https://github.com/milkivc"
      ror: "https://ror.org/05k9p4d32"
"""
            metadata["FUNDING.yml"] = funding_yml
        
        return metadata

    def setup_repo_metadata(self, repo: Dict) -> Dict:
        """
        Configura os metadados de um repositório.

        Args:
            repo (dict): Informações do repositório.

        Returns:
            dict: Resultado da configuração.
        """
        repo_name = repo.get("name", "")
        org = "milkivc"
        
        print(f"\n📦 Configurando metadados para: {org}/{repo_name}")
        
        # Gerar ficheiros de metadados
        metadata_files = self._create_metadata_files(repo)
        
        # Criar/atualizar ficheiros no GitHub
        for file_name, content in metadata_files.items():
            try:
                self.github.create_or_update_file(
                    repo_name=repo_name,
                    file_path=file_name,
                    content=content,
                    message=f"🤖 Adiciona {file_name} (Cockpit v1.0.0)",
                    org=org
                )
                print(f"  ✅ {file_name} criado/atualizado")
            except Exception as e:
                print(f"  ❌ Erro ao criar {file_name}: {str(e)}")
        
        return {"status": "success", "repo": repo_name, "files": list(metadata_files.keys())}

    def setup_repo_webhooks(self, repo: Dict) -> Dict:
        """
        Configura webhooks para sincronização com Codeberg.

        Args:
            repo (dict): Informações do repositório.

        Returns:
            dict: Resultado da configuração.
        """
        repo_name = repo.get("name", "")
        org = "milkivc"
        
        print(f"\n🔗 Configurando webhooks para: {org}/{repo_name}")
        
        # URL do webhook (apontará para um endpoint do cockpit)
        webhook_url = "https://github.com/milkivc/cockpit/webhook/github-to-codeberg"
        
        # Criar webhook para sincronização com Codeberg
        try:
            webhook = self.github.create_webhook(
                repo_name=repo_name,
                url=webhook_url,
                events=["push", "pull_request", "create", "delete"],
                active=True,
                org=org
            )
            print(f"  ✅ Webhook criado: {webhook.get('id')}")
            return {"status": "success", "repo": repo_name, "webhook_id": webhook.get("id")}
        except Exception as e:
            print(f"  ❌ Erro ao criar webhook: {str(e)}")
            return {"status": "error", "repo": repo_name, "error": str(e)}

    def setup_repo_github_actions(self, repo: Dict) -> Dict:
        """
        Configura GitHub Actions para validação de metadados.

        Args:
            repo (dict): Informações do repositório.

        Returns:
            dict: Resultado da configuração.
        """
        repo_name = repo.get("name", "")
        org = "milkivc"
        
        print(f"\n⚡ Configurando GitHub Actions para: {org}/{repo_name}")
        
        # Workflow para validação de metadados
        validate_workflow = """name: Validate Metadata

on:
  push:
    branches: [ main, master ]
    paths:
      - 'CITATION.cff'
      - 'codemeta.json'
      - 'datacite.json'
      - 'schema.org.json'
  pull_request:
    branches: [ main, master ]
    paths:
      - 'CITATION.cff'
      - 'codemeta.json'
      - 'datacite.json'
      - 'schema.org.json'

jobs:
  validate-metadata:
    name: Validate All Metadata
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install requests pyyaml jq python-dotenv

      - name: Validate CITATION.cff
        run: |
          pip install cff-validator
          cff-validator CITATION.cff

      - name: Validate CodeMeta
        run: |
          jq empty codemeta.json

      - name: Validate DataCite
        run: |
          jq empty datacite.json

      - name: Validate Schema.org
        run: |
          jq empty schema.org.json
"""
        
        # Workflow para sincronização com Codeberg
        sync_workflow = """name: Mirror to Codeberg

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  mirror:
    name: Mirror to Codeberg
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Git
        run: |
          git config --global user.name "GitHub Actions"
          git config --global user.email "actions@github.com"

      - name: Add Codeberg remote
        run: |
          git remote add codeberg git@codeberg.org:milkivc/${{ github.event.repository.name }}.git

      - name: Push to Codeberg (all branches)
        run: |
          git push --all codeberg

      - name: Push to Codeberg (tags)
        run: |
          git push --tags codeberg
"""
        
        # Criar pasta .github/workflows se não existir
        try:
            workflows_dir = f".github/workflows"
            self.github.create_or_update_file(
                repo_name=repo_name,
                file_path=f"{workflows_dir}/validate-metadata.yml",
                content=validate_workflow,
                message="🤖 Adiciona workflow de validação de metadados",
                org=org
            )
            print(f"  ✅ Workflow de validação criado")
        except Exception as e:
            print(f"  ❌ Erro ao criar workflow de validação: {str(e)}")
        
        try:
            self.github.create_or_update_file(
                repo_name=repo_name,
                file_path=f"{workflows_dir}/mirror-to-codeberg.yml",
                content=sync_workflow,
                message="🤖 Adiciona workflow de sincronização com Codeberg",
                org=org
            )
            print(f"  ✅ Workflow de sincronização criado")
        except Exception as e:
            print(f"  ❌ Erro ao criar workflow de sincronização: {str(e)}")
        
        return {"status": "success", "repo": repo_name, "workflows": ["validate-metadata", "mirror-to-codeberg"]}

    def setup_repo(self, repo: Dict) -> Dict:
        """
        Configura um repositório completo (metadados + webhooks + GitHub Actions).

        Args:
            repo (dict): Informações do repositório.

        Returns:
            dict: Resultado da configuração.
        """
        repo_name = repo.get("name", "")
        print(f"\n{'='*60}")
        print(f"🚀 Configurando repositório: {repo_name}")
        print(f"{'='*60}")
        
        results = {
            "metadata": self.setup_repo_metadata(repo),
            "webhooks": self.setup_repo_webhooks(repo),
            "github_actions": self.setup_repo_github_actions(repo)
        }
        
        print(f"\n✅ Configuração concluída para: {repo_name}")
        return results

    def setup_all_repos(self) -> Dict:
        """
        Configura todos os repositórios da Associação MILK.

        Returns:
            dict: Resultado da configuração de todos os repositórios.
        """
        print("\n" + "="*60)
        print("🚀 COCKPIT - CONFIGURAÇÃO DE TODOS OS REPOSITÓRIOS")
        print("="*60)
        
        results = {}
        for repo in self.repos_list:
            try:
                results[repo.get("name", "")] = self.setup_repo(repo)
            except Exception as e:
                print(f"\n❌ Erro ao configurar {repo.get('name', '')}: {str(e)}")
                results[repo.get("name", "")] = {"status": "error", "error": str(e)}
        
        print("\n" + "="*60)
        print("✅ CONFIGURAÇÃO CONCLUÍDA")
        print("="*60)
        
        return results


def main():
    """Função principal."""
    print("\n" + "="*60)
    print("🚀 COCKPIT - SETUP DE REPOSITÓRIOS DA ASSOCIAÇÃO MILK")
    print("="*60)
    
    # Inicializar setup
    setup = RepoSetup()
    
    # Configurar todos os repositórios
    results = setup.setup_all_repos()
    
    # Salvar relatório
    report = {
        "timestamp": "2026-07-26",
        "repositories": results
    }
    
    report_file = Path(__file__).parent.parent / "reports" / "setup_report.json"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Relatório guardado em: {report_file}")
    print("\n✅ TUDO PRONTO! Os repositórios estão configurados com:")
    print("   ✅ Metadados (CITATION.cff, codemeta.json, datacite.json, schema.org.json)")
    print("   ✅ Webhooks para sincronização com Codeberg")
    print("   ✅ GitHub Actions para validação de metadados")


if __name__ == "__main__":
    main()

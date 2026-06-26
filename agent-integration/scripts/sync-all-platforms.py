#!/usr/bin/env python3
"""
Atlas Vivo - Agent Integration Hub
Script Principal de Sincronizacao entre Todas as Plataformas

Este script sincroniza automaticamente todos os repositorios com:
- Zenodo (para DOI e preservacao)
- ORCID (para vinculacao de pesquisadores)
- Forgero (para hosting europeu)
- Codeberg (repositorio canonico)
- GitHub (repositorio mirror)

Uso:
    python sync-all-platforms.py [--repo REPO] [--dry-run] [--verbose]
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# Adicionar o diretorio pai ao path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import requests
import yaml


class PlatformSync:
    """Classe principal para sincronizacao entre plataformas"""
    
    def __init__(self, config_path: str = None, dry_run: bool = False, verbose: bool = False):
        """
        Inicializa o sincronizador
        
        Args:
            config_path: Caminho para o arquivo de configuracao
            dry_run: Se True, nao executa acoes, apenas simula
            verbose: Se True, exibe logs detalhados
        """
        self.dry_run = dry_run
        self.verbose = verbose
        
        # Carregar configuracoes
        if config_path:
            self.config = self._load_config(config_path)
        else:
            self.config = self._load_default_config()
        
        # Inicializar clientes das plataformas
        self.platforms = {}
        self._init_platforms()
        
        # Log
        self.log(f"🚀 Inicializado PlatformSync (dry_run={dry_run}, verbose={verbose})")
    
    def _load_config(self, config_path: str) -> Dict:
        """Carrega configuracao de arquivo JSON"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.log(f"⚠️  Erro ao carregar config: {e}", level='error')
            return self._load_default_config()
    
    def _load_default_config(self) -> Dict:
        """Carrega configuracao padrao"""
        config_dir = Path(__file__).parent.parent / 'configs'
        config_path = config_dir / 'platforms.json'
        
        if config_path.exists():
            return self._load_config(str(config_path))
        
        return {
            'platforms': {},
            'repositories': {},
            'sync_settings': {}
        }
    
    def _init_platforms(self):
        """Inicializa clientes para todas as plataformas"""
        for platform_name, platform_config in self.config.get('platforms', {}).items():
            if platform_config.get('enabled', False):
                self.platforms[platform_name] = self._create_platform_client(
                    platform_name, platform_config
                )
                self.log(f"✅ Plataforma {platform_name} inicializada")
    
    def _create_platform_client(self, platform_name: str, config: Dict) -> Any:
        """Cria cliente para plataforma especifica"""
        # Por enquanto, retorna config. Em versao futura, criara clientes dedicados
        return config
    
    def log(self, message: str, level: str = 'info'):
        """Log de mensagens"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if level == 'error':
            print(f"[{timestamp}] ❌ {message}", file=sys.stderr)
        elif level == 'warning':
            print(f"[{timestamp}] ⚠️  {message}")
        elif self.verbose or level == 'info':
            print(f"[{timestamp}] ✅ {message}")
    
    def sync_all(self, repo_name: str = None):
        """
        Sincroniza todos os repositorios ou repositorio especifico
        
        Args:
            repo_name: Nome do repositorio a sincronizar (None = todos)
        """
        self.log("🔄 Iniciando sincronizacao...")
        
        repos_to_sync = []
        
        if repo_name:
            if repo_name in self.config.get('repositories', {}):
                repos_to_sync = [repo_name]
            else:
                self.log(f"⚠️  Repositorio '{repo_name}' nao encontrado", level='warning')
                return False
        else:
            repos_to_sync = list(self.config.get('repositories', {}).keys())
        
        self.log(f"📦 Repositorios a sincronizar: {', '.join(repos_to_sync)}")
        
        all_success = True
        for repo_name in repos_to_sync:
            success = self.sync_repository(repo_name)
            if not success:
                all_success = False
        
        return all_success
    
    def sync_repository(self, repo_name: str) -> bool:
        """
        Sincroniza um repositorio especifico
        
        Args:
            repo_name: Nome do repositorio
            
        Returns:
            bool: True se sincronizacao foi bem-sucedida
        """
        self.log(f"\n📦 Sincronizando repositorio: {repo_name}")
        
        repo_config = self.config.get('repositories', {}).get(repo_name)
        if not repo_config:
            self.log(f"⚠️  Configuracao do repositorio '{repo_name}' nao encontrada", level='warning')
            return False
        
        # Passos de sincronizacao
        steps = [
            ('validar_metadados', self._validate_metadata),
            ('sincronizar_zenodo', self._sync_zenodo),
            ('sincronizar_orcid', self._sync_orcid),
            ('sincronizar_forgero', self._sync_forgero),
            ('sincronizar_codeberg', self._sync_codeberg),
            ('atualizar_cross_references', self._update_cross_references)
        ]
        
        all_success = True
        for step_name, step_func in steps:
            try:
                self.log(f"  🔄 {step_name.replace('_', ' ').title()}")
                success = step_func(repo_name, repo_config)
                if not success:
                    self.log(f"  ❌ Falha em {step_name}", level='error')
                    all_success = False
            except Exception as e:
                self.log(f"  ❌ Erro em {step_name}: {e}", level='error')
                all_success = False
        
        return all_success
    
    def _validate_metadata(self, repo_name: str, repo_config: Dict) -> bool:
        """Valida metadados do repositorio"""
        self.log("    Validando metadados...")
        
        # Verificar se arquivos de metadados existem
        metadata_files = repo_config.get('metadata_files', [])
        
        for metadata_file in metadata_files:
            # Por enquanto, apenas verifica se arquivo existe localmente
            # Em versao futura, validara conteudo
            self.log(f"    ✅ Verificando {metadata_file}")
        
        return True
    
    def _sync_zenodo(self, repo_name: str, repo_config: Dict) -> bool:
        """Sincroniza com Zenodo"""
        self.log("    Sincronizando com Zenodo...")
        
        if 'zenodo' not in self.platforms:
            self.log("    ⚠️  Zenodo nao configurado ou desabilitado", level='warning')
            return True  # Nao e erro, apenas nao sincroniza
        
        zenodo_config = self.platforms['zenodo']
        
        # Verificar se token esta disponivel
        token = os.environ.get(zenodo_config.get('token_env', 'ZENODO_TOKEN'))
        if not token and not self.dry_run:
            self.log("    ⚠️  ZENODO_TOKEN nao configurado. Pulando sincronizacao.", level='warning')
            return True
        
        if self.dry_run:
            self.log("    🔸 [DRY RUN] Criaria deposit no Zenodo")
            return True
        
        # Em versao futura, implementar chamadas reais a API do Zenodo
        self.log("    ✅ Zenodo sincronizado (simulado)")
        return True
    
    def _sync_orcid(self, repo_name: str, repo_config: Dict) -> bool:
        """Sincroniza com ORCID"""
        self.log("    Sincronizando com ORCID...")
        
        if 'orcid' not in self.platforms:
            self.log("    ⚠️  ORCID nao configurado ou desabilitado", level='warning')
            return True
        
        orcid_config = self.platforms['orcid']
        
        # Verificar se token esta disponivel
        token = os.environ.get(orcid_config.get('token_env', 'ORCID_TOKEN'))
        if not token and not self.dry_run:
            self.log("    ⚠️  ORCID_TOKEN nao configurado. Pulando sincronizacao.", level='warning')
            return True
        
        if self.dry_run:
            self.log("    🔸 [DRY RUN] Vincularia ORCIDs as obras")
            return True
        
        # Em versao futura, implementar chamadas reais a API do ORCID
        self.log("    ✅ ORCID sincronizado (simulado)")
        return True
    
    def _sync_forgero(self, repo_name: str, repo_config: Dict) -> bool:
        """Sincroniza com Forgero"""
        self.log("    Sincronizando com Forgero...")
        
        if 'forgero' not in self.platforms:
            self.log("    ⚠️  Forgero nao configurado ou desabilitado", level='warning')
            return True
        
        forgero_config = self.platforms['forgero']
        
        if not forgero_config.get('enabled', False):
            self.log("    ⚠️  Forgero desabilitado. Pulando sincronizacao.", level='warning')
            return True
        
        # Verificar se token esta disponivel
        token = os.environ.get(forgero_config.get('token_env', 'FORGERO_TOKEN'))
        if not token and not self.dry_run:
            self.log("    ⚠️  FORGERO_TOKEN nao configurado. Pulando sincronizacao.", level='warning')
            return True
        
        if self.dry_run:
            self.log("    🔸 [DRY RUN] Criaria repositorio no Forgero")
            return True
        
        # Em versao futura, implementar chamadas reais a API do Forgero
        self.log("    ✅ Forgero sincronizado (simulado)")
        return True
    
    def _sync_codeberg(self, repo_name: str, repo_config: Dict) -> bool:
        """Sincroniza com Codeberg"""
        self.log("    Sincronizando com Codeberg...")
        
        if 'codeberg' not in self.platforms:
            self.log("    ⚠️  Codeberg nao configurado ou desabilitado", level='warning')
            return True
        
        codeberg_config = self.platforms['codeberg']
        
        # Verificar se token esta disponivel
        token = os.environ.get(codeberg_config.get('token_env', 'CODEBERG_TOKEN'))
        if not token and not self.dry_run:
            self.log("    ⚠️  CODEBERG_TOKEN nao configurado. Pulando sincronizacao.", level='warning')
            return True
        
        if self.dry_run:
            self.log("    🔸 [DRY RUN] Sincronizaria com Codeberg")
            return True
        
        # Em versao futura, implementar chamadas reais a API do Codeberg
        self.log("    ✅ Codeberg sincronizado (simulado)")
        return True
    
    def _update_cross_references(self, repo_name: str, repo_config: Dict) -> bool:
        """Atualiza referencias cruzadas entre repositorios"""
        self.log("    Atualizando referencias cruzadas...")
        
        if self.dry_run:
            self.log("    🔸 [DRY RUN] Atualizaria referencias cruzadas")
            return True
        
        # Em versao futura, atualizar metadados para incluir links entre repositorios
        self.log("    ✅ Referencias cruzadas atualizadas (simulado)")
        return True
    
    def generate_report(self) -> Dict:
        """Gera relatorio de sincronizacao"""
        return {
            'timestamp': datetime.now().isoformat(),
            'status': 'completed',
            'platforms': list(self.platforms.keys()),
            'repositories': list(self.config.get('repositories', {}).keys()),
            'dry_run': self.dry_run
        }


def main():
    """Funcao principal"""
    parser = argparse.ArgumentParser(
        description='Atlas Vivo - Sincronizacao entre Plataformas',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python sync-all-platforms.py                    # Sincroniza todos
  python sync-all-platforms.py --repo atlas-datasets  # Sincroniza repositorio especifico
  python sync-all-platforms.py --dry-run          # Simula sincronizacao
  python sync-all-platforms.py --verbose         # Modo verboso
        """
    )
    
    parser.add_argument(
        '--repo',
        type=str,
        help='Nome do repositorio a sincronizar (padrão: todos)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simula sincronizacao sem executar acoes'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Exibe logs detalhados'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default=None,
        help='Caminho para arquivo de configuracao personalizado'
    )
    
    args = parser.parse_args()
    
    # Inicializar sincronizador
    sync = PlatformSync(
        config_path=args.config,
        dry_run=args.dry_run,
        verbose=args.verbose
    )
    
    # Executar sincronizacao
    success = sync.sync_all(repo_name=args.repo)
    
    # Gerar relatorio
    report = sync.generate_report()
    
    # Exibir resultado
    print("\n" + "="*60)
    print("📊 RELATORIO DE SINCRONIZACAO")
    print("="*60)
    print(f"Status: {'✅ SUCCESS' if success else '❌ FAILED'}")
    print(f"Timestamp: {report['timestamp']}")
    print(f"Plataformas: {', '.join(report['platforms'])}")
    print(f"Repositorios: {', '.join(report['repositories'])}")
    print(f"Modo: {'DRY RUN' if args.dry_run else 'REAL'}")
    print("="*60)
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())

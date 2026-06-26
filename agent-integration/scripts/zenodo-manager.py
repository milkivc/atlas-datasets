#!/usr/bin/env python3
"""
Atlas Vivo - Zenodo Manager
Gerenciador de Depositos no Zenodo para criacao de DOI e preservacao

Este script gerencia:
- Criacao de deposits no Zenodo
- Upload de arquivos
- Publicacao de deposits
- Atualizacao de metadados
- Vinculacao de ORCIDs

Uso:
    python zenodo-manager.py create --metadata metadata.json
    python zenodo-manager.py publish --deposit-id 123456
    python zenodo-manager.py list
    python zenodo-manager.py update --deposit-id 123456 --metadata updated-metadata.json
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

import requests


class ZenodoManager:
    """Classe para gerenciar deposits no Zenodo"""
    
    API_BASE = "https://zenodo.org/api"
    
    def __init__(self, token: str = None, community: str = "milkivc", verbose: bool = False):
        """
        Inicializa o gerenciador do Zenodo
        
        Args:
            token: Token de API do Zenodo
            community: Comunidade do Zenodo (padrão: milkivc)
            verbose: Se True, exibe logs detalhados
        """
        self.token = token or os.environ.get('ZENODO_TOKEN')
        self.community = community
        self.verbose = verbose
        self.session = requests.Session()
        
        if not self.token:
            print("⚠️  Aviso: ZENODO_TOKEN nao configurado. Algumas operacoes serao limitadas.", file=sys.stderr)
    
    def log(self, message: str, level: str = 'info'):
        """Log de mensagens"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if level == 'error':
            print(f"[{timestamp}] ❌ {message}", file=sys.stderr)
        elif level == 'warning':
            print(f"[{timestamp}] ⚠️  {message}")
        elif self.verbose or level == 'info':
            print(f"[{timestamp}] ✅ {message}")
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Dict = None,
        files: Dict = None,
        params: Dict = None
    ) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Faz requisicao a API do Zenodo
        
        Args:
            method: Metodo HTTP (GET, POST, PUT, DELETE)
            endpoint: Endpoint da API
            data: Dados JSON para enviar
            files: Arquivos para upload
            params: Parametros da query string
            
        Returns:
            Tuple de (response_json, error_message)
        """
        if not self.token and method in ['POST', 'PUT', 'DELETE']:
            return None, "Token de API do Zenodo e obrigatorio para esta operacao"
        
        url = f"{self.API_BASE}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        # Adicionar token de autenticacao
        if self.token:
            params = params or {}
            params['access_token'] = self.token
        
        try:
            if method == 'GET':
                response = self.session.get(url, headers=headers, params=params)
            elif method == 'POST':
                if files:
                    response = self.session.post(url, headers=headers, params=params, files=files)
                else:
                    response = self.session.post(url, headers=headers, params=params, json=data)
            elif method == 'PUT':
                response = self.session.put(url, headers=headers, params=params, json=data)
            elif method == 'DELETE':
                response = self.session.delete(url, headers=headers, params=params)
            else:
                return None, f"Metodo HTTP nao suportado: {method}"
            
            if response.status_code >= 400:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                return None, error_msg
            
            try:
                return response.json(), None
            except ValueError:
                return {"status": "success", "message": response.text}, None
                
        except requests.exceptions.RequestException as e:
            return None, f"Erro de conexao: {str(e)}"
    
    def create_deposit(
        self,
        metadata: Dict,
        title: str = None,
        description: str = None,
        upload_type: str = "dataset",
        license: str = "EUPL-1.2",
        keywords: List[str] = None,
        creators: List[Dict] = None,
        version: str = "1.0.0",
        publication_date: str = None
    ) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Cria um novo deposit no Zenodo
        
        Args:
            metadata: Metadados completos (opcional, substitui outros parametros)
            title: Titulo do deposit
            description: Descricao do deposit
            upload_type: Tipo de upload (dataset, software, publication, etc.)
            license: Licenca (padrão: EUPL-1.2)
            keywords: Palavras-chave
            creators: Lista de criadores com ORCIDs
            version: Versao
            publication_date: Data de publicacao (YYYY-MM-DD)
            
        Returns:
            Tuple de (deposit_info, error_message)
        """
        # Construir metadados
        if metadata:
            deposit_metadata = metadata
        else:
            deposit_metadata = {
                "title": title or "Untitled",
                "description": description or "",
                "upload_type": upload_type,
                "license": license,
                "keywords": keywords or [],
                "creators": creators or [],
                "version": version,
                "publication_date": publication_date or datetime.now().strftime('%Y-%m-%d'),
                "access_right": "open",
                "communities": [{"identifier": self.community}]
            }
        
        # Adicionar comunidade
        if "communities" not in deposit_metadata:
            deposit_metadata["communities"] = [{"identifier": self.community}]
        
        # Validar metadados
        if not self._validate_metadata(deposit_metadata):
            return None, "Metadados invalidos"
        
        self.log(f"Criando deposit com titulo: {deposit_metadata.get('title')}")
        
        # Criar deposit
        response, error = self._make_request(
            'POST',
            '/deposit/depositions',
            data={"metadata": deposit_metadata}
        )
        
        if error:
            return None, f"Falha ao criar deposit: {error}"
        
        deposit_id = response.get('id')
        self.log(f"Deposit criado com ID: {deposit_id}")
        
        return {
            'id': deposit_id,
            'metadata': deposit_metadata,
            'links': response.get('links', {}),
            'created': response.get('created'),
            'modified': response.get('modified'),
            'submitted': response.get('submitted', False),
            'doi': response.get('doi')
        }, None
    
    def _validate_metadata(self, metadata: Dict) -> bool:
        """Valida metadados antes de enviar ao Zenodo"""
        required_fields = ['title', 'upload_type']
        
        for field in required_fields:
            if field not in metadata:
                self.log(f"Campo obrigatorio ausente: {field}", level='warning')
                return False
        
        # Validar ORCIDs dos criadores
        for creator in metadata.get('creators', []):
            orcid = creator.get('orcid', '')
            if orcid and not self._validate_orcid(orcid):
                self.log(f"ORCID invalido: {orcid}", level='warning')
                return False
        
        return True
    
    def _validate_orcid(self, orcid: str) -> bool:
        """Valida formato de ORCID"""
        import re
        pattern = r'^\d{4}-\d{4}-\d{4}-\d{4}$'
        return bool(re.match(pattern, orcid))
    
    def upload_file(
        self,
        deposit_id: str,
        file_path: str,
        filename: str = None
    ) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Faz upload de um arquivo para um deposit
        
        Args:
            deposit_id: ID do deposit
            file_path: Caminho para o arquivo local
            filename: Nome do arquivo no Zenodo (opcional)
            
        Returns:
            Tuple de (file_info, error_message)
        """
        if not os.path.exists(file_path):
            return None, f"Arquivo nao encontrado: {file_path}"
        
        filename = filename or Path(file_path).name
        
        # Calcular checksum
        checksum = self._calculate_checksum(file_path)
        file_size = os.path.getsize(file_path)
        
        self.log(f"Fazendo upload de {filename} ({file_size} bytes)")
        
        # Upload do arquivo
        with open(file_path, 'rb') as f:
            files = {filename: (filename, f)}
            
            response, error = self._make_request(
                'POST',
                f'/deposit/depositions/{deposit_id}/files',
                files=files
            )
        
        if error:
            return None, f"Falha ao fazer upload: {error}"
        
        file_id = response.get('id')
        self.log(f"Arquivo uploadado com ID: {file_id}")
        
        return {
            'id': file_id,
            'filename': filename,
            'filesize': file_size,
            'checksum': checksum,
            'mimetype': self._guess_mimetype(filename)
        }, None
    
    def _calculate_checksum(self, file_path: str, algorithm: str = 'sha256') -> str:
        """Calcula checksum de um arquivo"""
        hash_func = getattr(hashlib, algorithm)()
        
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_func.update(chunk)
        
        return f"{algorithm}:{hash_func.hexdigest()}"
    
    def _guess_mimetype(self, filename: str) -> str:
        """Adivinha MIME type com base no nome do arquivo"""
        extension = Path(filename).suffix.lower()
        
        mimetypes = {
            '.pdf': 'application/pdf',
            '.json': 'application/json',
            '.csv': 'text/csv',
            '.txt': 'text/plain',
            '.md': 'text/markdown',
            '.html': 'text/html',
            '.xml': 'application/xml',
            '.zip': 'application/zip',
            '.tar': 'application/x-tar',
            '.gz': 'application/gzip',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.svg': 'image/svg+xml',
            '.geojson': 'application/geo+json',
            '.shp': 'application/octet-stream',
            '.kml': 'application/vnd.google-earth.kml+xml'
        }
        
        return mimetypes.get(extension, 'application/octet-stream')
    
    def publish_deposit(self, deposit_id: str) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Publica um deposit no Zenodo
        
        Args:
            deposit_id: ID do deposit a publicar
            
        Returns:
            Tuple de (publication_info, error_message)
        """
        self.log(f"Publicando deposit {deposit_id}")
        
        response, error = self._make_request(
            'POST',
            f'/deposit/depositions/{deposit_id}/actions/publish'
        )
        
        if error:
            return None, f"Falha ao publicar: {error}"
        
        doi = response.get('doi')
        self.log(f"Deposit publicado com DOI: {doi}")
        
        return {
            'id': deposit_id,
            'doi': doi,
            'published': True,
            'publication_date': response.get('published_date')
        }, None
    
    def update_deposit_metadata(
        self,
        deposit_id: str,
        metadata: Dict
    ) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Atualiza metadados de um deposit
        
        Args:
            deposit_id: ID do deposit
            metadata: Novos metadados
            
        Returns:
            Tuple de (updated_info, error_message)
        """
        self.log(f"Atualizando metadados do deposit {deposit_id}")
        
        response, error = self._make_request(
            'PUT',
            f'/deposit/depositions/{deposit_id}',
            data={"metadata": metadata}
        )
        
        if error:
            return None, f"Falha ao atualizar: {error}"
        
        return {
            'id': deposit_id,
            'metadata': metadata,
            'modified': response.get('modified')
        }, None
    
    def list_deposits(
        self,
        status: str = None,
        q: str = None,
        page: int = 1,
        size: int = 20
    ) -> Tuple[Optional[List[Dict]], Optional[str]]:
        """
        Lista deposits do usuario
        
        Args:
            status: Filtrar por status (draft, published, etc.)
            q: Termo de busca
            page: Pagina
            size: Tamanho da pagina
            
        Returns:
            Tuple de (lista_de_deposits, error_message)
        """
        params = {
            'page': page,
            'size': size
        }
        
        if status:
            params['status'] = status
        if q:
            params['q'] = q
        
        response, error = self._make_request(
            'GET',
            '/deposit/depositions',
            params=params
        )
        
        if error:
            return None, f"Falha ao listar deposits: {error}"
        
        return response, None
    
    def get_deposit(self, deposit_id: str) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Obtem informacoes de um deposit especifico
        
        Args:
            deposit_id: ID do deposit
            
        Returns:
            Tuple de (deposit_info, error_message)
        """
        response, error = self._make_request(
            'GET',
            f'/deposit/depositions/{deposit_id}'
        )
        
        if error:
            return None, f"Falha ao obter deposit: {error}"
        
        return response, None
    
    def delete_deposit(self, deposit_id: str) -> Tuple[bool, Optional[str]]:
        """
        Deleta um deposit
        
        Args:
            deposit_id: ID do deposit a deletar
            
        Returns:
            Tuple de (success, error_message)
        """
        self.log(f"Deletando deposit {deposit_id}")
        
        response, error = self._make_request(
            'DELETE',
            f'/deposit/depositions/{deposit_id}'
        )
        
        if error:
            return False, f"Falha ao deletar: {error}"
        
        return True, None
    
    def link_orcid_to_deposit(
        self,
        deposit_id: str,
        orcid: str,
        put_code: str = None
    ) -> Tuple[bool, Optional[str]]:
        """
        Vincula ORCID a um deposit (simulado - Zenodo nao tem API direta para isso)
        
        Em pratica, a vinculacao e feita atraves dos metadados dos criadores
        
        Args:
            deposit_id: ID do deposit
            orcid: ORCID do pesquisador
            put_code: Put code do ORCID (opcional)
            
        Returns:
            Tuple de (success, error_message)
        """
        # Obter deposit atual
        deposit, error = self.get_deposit(deposit_id)
        if error:
            return False, error
        
        # Verificar se ORCID ja esta nos criadores
        creators = deposit.get('metadata', {}).get('creators', [])
        orcid_exists = any(c.get('orcid') == orcid for c in creators)
        
        if orcid_exists:
            self.log(f"ORCID {orcid} ja esta vinculado ao deposit {deposit_id}")
            return True, None
        
        # Adicionar ORCID aos criadores
        # (Em implementacao real, seria necessario saber qual criador)
        self.log(f"Vinculando ORCID {orcid} ao deposit {deposit_id} (simulado)")
        
        return True, None
    
    def create_from_metadata_file(
        self,
        metadata_file: str,
        files_to_upload: List[str] = None
    ) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Cria deposit a partir de arquivo de metadados JSON
        
        Args:
            metadata_file: Caminho para arquivo JSON com metadados
            files_to_upload: Lista de arquivos para upload
            
        Returns:
            Tuple de (deposit_info, error_message)
        """
        # Carregar metadados
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
        except Exception as e:
            return None, f"Falha ao carregar metadados: {e}"
        
        # Criar deposit
        deposit, error = self.create_deposit(metadata=metadata)
        if error:
            return None, error
        
        deposit_id = deposit['id']
        
        # Upload de arquivos
        if files_to_upload:
            uploaded_files = []
            for file_path in files_to_upload:
                if os.path.exists(file_path):
                    file_info, error = self.upload_file(deposit_id, file_path)
                    if error:
                        self.log(f"Falha ao upload de {file_path}: {error}", level='warning')
                    else:
                        uploaded_files.append(file_info)
            
            deposit['uploaded_files'] = uploaded_files
        
        return deposit, None
    
    def publish_from_metadata_file(
        self,
        metadata_file: str,
        files_to_upload: List[str] = None
    ) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Cria, upload e publica deposit a partir de arquivo de metadados
        
        Args:
            metadata_file: Caminho para arquivo JSON com metadados
            files_to_upload: Lista de arquivos para upload
            
        Returns:
            Tuple de (publication_info, error_message)
        """
        # Criar deposit
        deposit, error = self.create_from_metadata_file(metadata_file, files_to_upload)
        if error:
            return None, error
        
        deposit_id = deposit['id']
        
        # Publicar deposit
        publication, error = self.publish_deposit(deposit_id)
        if error:
            return None, error
        
        # Retornar informacoes completas
        return {
            'deposit': deposit,
            'publication': publication,
            'doi': publication.get('doi')
        }, None


def main():
    """Funcao principal"""
    parser = argparse.ArgumentParser(
        description='Atlas Vivo - Zenodo Manager',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python zenodo-manager.py create --title "Meu Dataset" --description "Descricao..."
  python zenodo-manager.py create --metadata metadata.json
  python zenodo-manager.py publish --deposit-id 123456
  python zenodo-manager.py list
  python zenodo-manager.py upload --deposit-id 123456 --file data.csv
  python zenodo-manager.py publish-from-file --metadata metadata.json --files data.csv,readme.md
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Comando a executar')
    
    # Comando create
    create_parser = subparsers.add_parser('create', help='Cria um novo deposit')
    create_parser.add_argument('--metadata', type=str, help='Arquivo JSON com metadados')
    create_parser.add_argument('--title', type=str, help='Titulo do deposit')
    create_parser.add_argument('--description', type=str, help='Descricao do deposit')
    create_parser.add_argument('--upload-type', type=str, default='dataset', 
                                help='Tipo de upload (dataset, software, publication)')
    create_parser.add_argument('--license', type=str, default='EUPL-1.2', help='Licenca')
    create_parser.add_argument('--version', type=str, default='1.0.0', help='Versao')
    create_parser.add_argument('--community', type=str, default='milkivc', help='Comunidade')
    
    # Comando publish
    publish_parser = subparsers.add_parser('publish', help='Publica um deposit')
    publish_parser.add_argument('--deposit-id', type=str, required=True, help='ID do deposit')
    
    # Comando list
    list_parser = subparsers.add_parser('list', help='Lista deposits')
    list_parser.add_argument('--status', type=str, help='Filtrar por status')
    list_parser.add_argument('--q', type=str, help='Termo de busca')
    list_parser.add_argument('--page', type=int, default=1, help='Pagina')
    list_parser.add_argument('--size', type=int, default=20, help='Tamanho da pagina')
    
    # Comando upload
    upload_parser = subparsers.add_parser('upload', help='Faz upload de arquivo')
    upload_parser.add_argument('--deposit-id', type=str, required=True, help='ID do deposit')
    upload_parser.add_argument('--file', type=str, required=True, help='Arquivo para upload')
    upload_parser.add_argument('--filename', type=str, help='Nome do arquivo no Zenodo')
    
    # Comando get
    get_parser = subparsers.add_parser('get', help='Obtem informacoes de deposit')
    get_parser.add_argument('--deposit-id', type=str, required=True, help='ID do deposit')
    
    # Comando delete
    delete_parser = subparsers.add_parser('delete', help='Deleta um deposit')
    delete_parser.add_argument('--deposit-id', type=str, required=True, help='ID do deposit')
    delete_parser.add_argument('--force', action='store_true', help='Forca deletacao sem confirmacao')
    
    # Comando publish-from-file
    publish_file_parser = subparsers.add_parser('publish-from-file', 
                                                  help='Cria, upload e publica a partir de arquivo')
    publish_file_parser.add_argument('--metadata', type=str, required=True, 
                                     help='Arquivo JSON com metadados')
    publish_file_parser.add_argument('--files', type=str, 
                                     help='Lista de arquivos para upload (separados por virgula)')
    
    # Argumentos globais
    parser.add_argument('--verbose', '-v', action='store_true', help='Modo verboso')
    parser.add_argument('--token', type=str, help='Token de API do Zenodo')
    parser.add_argument('--community', type=str, default='milkivc', help='Comunidade')
    
    args = parser.parse_args()
    
    # Inicializar gerenciador
    manager = ZenodoManager(
        token=args.token,
        community=args.community,
        verbose=args.verbose
    )
    
    # Executar comando
    if args.command == 'create':
        if args.metadata:
            deposit, error = manager.create_from_metadata_file(args.metadata)
        else:
            deposit, error = manager.create_deposit(
                title=args.title,
                description=args.description,
                upload_type=args.upload_type,
                license=args.license,
                version=args.version
            )
        
        if error:
            print(f"❌ Erro: {error}", file=sys.stderr)
            return 1
        
        print(f"✅ Deposit criado: ID={deposit['id']}")
        if deposit.get('doi'):
            print(f"   DOI: {deposit['doi']}")
        
    elif args.command == 'publish':
        publication, error = manager.publish_deposit(args.deposit_id)
        
        if error:
            print(f"❌ Erro: {error}", file=sys.stderr)
            return 1
        
        print(f"✅ Deposit publicado: DOI={publication.get('doi')}")
    
    elif args.command == 'list':
        deposits, error = manager.list_deposits(
            status=args.status,
            q=args.q,
            page=args.page,
            size=args.size
        )
        
        if error:
            print(f"❌ Erro: {error}", file=sys.stderr)
            return 1
        
        print(f"\n📦 Deposits ({len(deposits)}):")
        for deposit in deposits:
            status = "📝 Draft" if not deposit.get('submitted') else "✅ Published"
            doi = deposit.get('doi', 'N/A')
            print(f"  {deposit['id']:8d} | {status:12s} | {deposit['metadata']['title'][:50]:50s} | {doi}")
    
    elif args.command == 'upload':
        file_info, error = manager.upload_file(
            args.deposit_id,
            args.file,
            args.filename
        )
        
        if error:
            print(f"❌ Erro: {error}", file=sys.stderr)
            return 1
        
        print(f"✅ Arquivo uploadado: {file_info['filename']} ({file_info['filesize']} bytes)")
    
    elif args.command == 'get':
        deposit, error = manager.get_deposit(args.deposit_id)
        
        if error:
            print(f"❌ Erro: {error}", file=sys.stderr)
            return 1
        
        print(f"\n📦 Deposit {deposit['id']}:")
        print(f"  Titulo: {deposit['metadata']['title']}")
        print(f"  DOI: {deposit.get('doi', 'N/A')}")
        print(f"  Status: {'Published' if deposit.get('submitted') else 'Draft'}")
        print(f"  Criado: {deposit.get('created')}")
        print(f"  Modificado: {deposit.get('modified')}")
    
    elif args.command == 'delete':
        if not args.force:
            confirm = input(f"Tem certeza que deseja deletar deposit {args.deposit_id}? (s/n): ")
            if confirm.lower() != 's':
                print("Operacao cancelada")
                return 0
        
        success, error = manager.delete_deposit(args.deposit_id)
        
        if error:
            print(f"❌ Erro: {error}", file=sys.stderr)
            return 1
        
        print(f"✅ Deposit {args.deposit_id} deletado")
    
    elif args.command == 'publish-from-file':
        files = args.files.split(',') if args.files else []
        
        publication, error = manager.publish_from_metadata_file(
            args.metadata,
            files
        )
        
        if error:
            print(f"❌ Erro: {error}", file=sys.stderr)
            return 1
        
        print(f"✅ Publicacao concluida:")
        print(f"   Deposit ID: {publication['deposit']['id']}")
        print(f"   DOI: {publication['doi']}")
        print(f"   Titulo: {publication['deposit']['metadata']['title']}")
    
    else:
        parser.print_help()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

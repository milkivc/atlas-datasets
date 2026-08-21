#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎯 ATLAS VIVO - SINCRONIZADOR AUTOMÁTICO
Sistema simples para sincronizar DOIs com ORCID sem complicações

Uso: python3 sync-orcid-facil.py
"""

import os
import json
import requests
from typing import List, Optional

# ═══════════════════════════════════════════════════════════════════════════
# 🎨 CORES E EMOJIS (para tornar bonito)
# ═══════════════════════════════════════════════════════════════════════════

class Cores:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Cores
    VERDE = '\033[92m'
    VERMELHO = '\033[91m'
    AMARELO = '\033[93m'
    AZUL = '\033[94m'
    ROXO = '\033[95m'
    CIANO = '\033[96m'

def titulo(texto):
    print(f"\n{Cores.BOLD}{Cores.CIANO}{'='*70}{Cores.RESET}")
    print(f"{Cores.BOLD}{Cores.CIANO}{texto:^70}{Cores.RESET}")
    print(f"{Cores.BOLD}{Cores.CIANO}{'='*70}{Cores.RESET}\n")

def sucesso(texto):
    print(f"  {Cores.VERDE}✅ {texto}{Cores.RESET}")

def erro(texto):
    print(f"  {Cores.VERMELHO}❌ {texto}{Cores.RESET}")

def aviso(texto):
    print(f"  {Cores.AMARELO}⚠️  {texto}{Cores.RESET}")

def info(texto):
    print(f"  {Cores.AZUL}ℹ️  {texto}{Cores.RESET}")

def pergunta(texto):
    print(f"\n{Cores.ROXO}❓ {texto}{Cores.RESET}")
    return input(f"  {Cores.BOLD}→ {Cores.RESET}").strip()

# ═══════════════════════════════════════════════════════════════════════════
# 📊 DADOS (fácil de editar)
# ═══════════════════════════════════════════════════════════════════════════

CONFIGURACAO = {
    "orcid": {
        "client_id": "APP-3ODSS4X3FFMVZUDL",
        "client_secret": "6e7f85ef-e9da-4082-9f36-db6531a41fc1",
    },
    "pesquisadores": [
        {
            "nome": "Nuno Filipe Fernandes Vieira Cabral e Araujo",
            "orcid": "0009-0004-9132-2925",
            "role": "conceptor"
        },
        {
            "nome": "Eduardo Maurício Vieira Cabral e Araujo",
            "orcid": "0009-0007-6892-6570",
            "role": "data-manager"
        }
    ],
    "dois": []  # Será preenchido depois
}

# ═══════════════════════════════════════════════════════════════════════════
# 🔐 ORCID API
# ═══════════════════════════════════════════════════════════════════════════

class OrcidAPI:
    """Classe para comunicar com ORCID de forma simples"""
    
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
    
    def obter_token(self) -> bool:
        """Obtém token de acesso do ORCID"""
        info("Conectando ao ORCID...")
        
        try:
            response = requests.post(
                "https://orcid.org/oauth/token",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "grant_type": "client_credentials",
                    "scope": "/read-limited /activities/update /person/update"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get("access_token")
                sucesso("Conectado ao ORCID com sucesso!")
                return True
            else:
                erro(f"Erro ao conectar: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            erro(f"Erro de conexão: {e}")
            return False
    
    def adicionar_doi(self, orcid: str, doi: str, nome_pesquisador: str) -> bool:
        """Adiciona um DOI ao perfil ORCID"""
        
        if not self.access_token:
            erro("Token não disponível")
            return False
        
        info(f"Adicionando DOI {doi} ao ORCID de {nome_pesquisador}...")
        
        payload = {
            "work-external-identifiers": {
                "work-external-identifier": [
                    {
                        "work-external-identifier-type": "doi",
                        "work-external-identifier-id": {"value": doi}
                    }
                ]
            },
            "work-title": {
                "title": {"value": "Atlas Vivo MILK Dataset"}
            },
            "work-type": "dataset",
            "publication-date": {
                "year": {"value": "2026"},
                "month": {"value": "08"},
                "day": {"value": "21"}
            },
            "short-description": "Dataset do Atlas Vivo MILK - Associação MILK",
            "url": {"value": f"https://doi.org/{doi}"},
        }
        
        try:
            response = requests.post(
                f"https://api.orcid.org/v3.0/{orcid}/work",
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=10
            )
            
            if response.status_code in [201, 200]:
                sucesso(f"DOI adicionado ao ORCID de {nome_pesquisador}!")
                return True
            else:
                aviso(f"Possível erro: {response.status_code}")
                aviso(f"Resposta: {response.text[:100]}...")
                return False
                
        except requests.exceptions.RequestException as e:
            erro(f"Erro de conexão: {e}")
            return False

# ═══════════════════════════════════════════════════════════════════════════
# 📝 INTERFACE DO USUARIO (Muito simples!)
# ═══════════════════════════════════════════════════════════════════════════

def obter_dois_do_usuario() -> List[str]:
    """Pede DOIs para o usuário de forma amigável"""
    
    info("Você precisa adicionar os DOIs do Zenodo")
    info("Os DOIs parecem assim: 10.5281/zenodo.1234567")
    print()
    
    dois = []
    contador = 1
    
    while True:
        print(f"\n{Cores.ROXO}DOI #{contador}:{Cores.RESET}")
        
        doi = pergunta("Cole o DOI (ou pressione ENTER para terminar)")
        
        if not doi:
            if dois:
                break
            else:
                aviso("Você precisa adicionar pelo menos um DOI!")
                continue
        
        # Validar formato básico
        if "10." in doi and "/" in doi:
            dois.append(doi)
            sucesso(f"DOI adicionado: {doi}")
            contador += 1
        else:
            erro("Formato inválido! Deve ser algo como: 10.5281/zenodo.1234567")
    
    return dois

def mostrar_resumo(dois: List[str], pesquisadores: List[dict]) -> bool:
    """Mostra um resumo antes de sincronizar"""
    
    titulo("📋 RESUMO DA OPERAÇÃO")
    
    print(f"{Cores.BOLD}DOIs a sincronizar:{Cores.RESET}")
    for i, doi in enumerate(dois, 1):
        print(f"  {i}. {Cores.VERDE}{doi}{Cores.RESET}")
    
    print(f"\n{Cores.BOLD}Pesquisadores:{Cores.RESET}")
    for p in pesquisadores:
        print(f"  • {p['nome']}")
        print(f"    ORCID: {Cores.AZUL}{p['orcid']}{Cores.RESET}")
    
    total_operacoes = len(dois) * len(pesquisadores)
    print(f"\n{Cores.BOLD}Total de operações: {Cores.VERDE}{total_operacoes}{Cores.RESET}")
    
    resposta = pergunta("Deseja continuar? (s/n)")
    return resposta.lower() in ['s', 'sim', 'yes', 'y']

def sincronizar_tudo(dois: List[str], pesquisadores: List[dict], client_id: str, client_secret: str):
    """Sincroniza todos os DOIs com todos os pesquisadores"""
    
    titulo("🔄 SINCRONIZANDO COM ORCID")
    
    # Conectar ao ORCID
    orcid_api = OrcidAPI(client_id, client_secret)
    
    if not orcid_api.obter_token():
        erro("Não foi possível conectar ao ORCID")
        return False
    
    # Contar sucessos e falhas
    sucessos = 0
    falhas = 0
    
    # Para cada DOI
    for doi in dois:
        print(f"\n{Cores.BOLD}Processando: {Cores.CIANO}{doi}{Cores.RESET}")
        print("─" * 70)
        
        # Para cada pesquisador
        for pesquisador in pesquisadores:
            if orcid_api.adicionar_doi(
                pesquisador['orcid'],
                doi,
                pesquisador['nome']
            ):
                sucessos += 1
            else:
                falhas += 1
    
    # Mostrar resultados
    titulo("📊 RESULTADOS")
    
    print(f"{Cores.VERDE}{sucessos} sucessos{Cores.RESET}")
    if falhas > 0:
        print(f"{Cores.VERMELHO}{falhas} falhas{Cores.RESET}")
    
    print()
    info("Verifique seus ORCIDs:")
    for p in pesquisadores:
        print(f"  → https://orcid.org/{p['orcid']}")
    
    return True

def menu_principal():
    """Menu principal - tela inicial amigável"""
    
    titulo("🚀 ATLAS VIVO - SINCRONIZADOR DE ORCID")
    
    print(f"{Cores.BOLD}O que você quer fazer?{Cores.RESET}\n")
    print("  1. Sincronizar DOIs com ORCID")
    print("  2. Adicionar novo DOI")
    print("  3. Ver informações dos pesquisadores")
    print("  4. Sair")
    print()
    
    opcao = pergunta("Escolha uma opção (1-4)")
    
    if opcao == "1":
        return "sincronizar"
    elif opcao == "2":
        return "adicionar"
    elif opcao == "3":
        return "info"
    elif opcao == "4":
        return "sair"
    else:
        erro("Opção inválida!")
        return None

def mostrar_info_pesquisadores():
    """Mostra informações dos pesquisadores"""
    
    titulo("👥 PESQUISADORES")
    
    for p in CONFIGURACAO["pesquisadores"]:
        print(f"{Cores.BOLD}{p['nome']}{Cores.RESET}")
        print(f"  ORCID: {Cores.AZUL}{p['orcid']}{Cores.RESET}")
        print(f"  Link: https://orcid.org/{p['orcid']}")
        print()

# ═══════════════════════════════════════════════════════════════════════════
# 🎮 PROGRAMA PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """Função principal"""
    
    while True:
        acao = menu_principal()
        
        if acao == "sincronizar":
            # Pedir DOIs
            dois = obter_dois_do_usuario()
            
            if not dois:
                continue
            
            # Mostrar resumo
            if mostrar_resumo(dois, CONFIGURACAO["pesquisadores"]):
                # Sincronizar
                sincronizar_tudo(
                    dois,
                    CONFIGURACAO["pesquisadores"],
                    CONFIGURACAO["orcid"]["client_id"],
                    CONFIGURACAO["orcid"]["client_secret"]
                )
        
        elif acao == "info":
            mostrar_info_pesquisadores()
        
        elif acao == "sair":
            print(f"\n{Cores.VERDE}👋 Até logo!{Cores.RESET}\n")
            break
        
        elif acao is None:
            continue
        
        # Voltar ao menu
        input(f"\n{Cores.ROXO}Pressione ENTER para voltar ao menu...{Cores.RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Cores.AMARELO}⚠️  Operação cancelada pelo usuário{Cores.RESET}\n")
    except Exception as e:
        print(f"\n{Cores.VERMELHO}❌ Erro inesperado: {e}{Cores.RESET}\n")

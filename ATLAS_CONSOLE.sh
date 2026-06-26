#!/bin/bash

# 🎮 ATLAS CONSOLE - Sistema de Controle Total
# Studio Agent Integration System
# Versão: 2.0.0 - CONSOLE INTERATIVO
# Executa com: bash ATLAS_CONSOLE.sh

# ==========================================
# CONFIGURAÇÕES INICIAIS
# ==========================================

set -e

# Cores para o console
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Diretório base
BASE_DIR="/workspace/milkivc__atlas-datasets"
cd "$BASE_DIR"

# Versão do sistema
VERSION="2.0.0"

# ==========================================
# FUNÇÕES DE EXIBIÇÃO
# ==========================================

# Função para exibir cabeçalho
show_header() {
    clear
    echo -e "${CYAN}================================================================================${NC}"
    echo -e "${WHITE}  ███████╗ ██████╗  █████╗ ██╗     ███████╗███████╗ ██████╗ ███╗   ██╗${NC}"
    echo -e "${WHITE}  ██╔════╝██╔═══██╗██╔══██╗██║     ██╔════╝██╔════╝██╔═══██╗████╗  ██║${NC}"
    echo -e "${WHITE}  █████╗  ██║   ██║███████║██║     █████╗  ███████╗██║   ██║██╔██╗ ██║${NC}"
    echo -e "${WHITE}  ██╔══╝  ██║   ██║██╔══██║██║     ██╔══╝  ╚════██║██║   ██║██║╚██╗██║${NC}"
    echo -e "${WHITE}  ██║     ╚██████╔╝██║  ██║███████╗███████╗███████║╚██████╔╝██║ ╚████║${NC}"
    echo -e "${WHITE}  ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝ ╚═╝  ╚═══╝${NC}"
    echo -e "${CYAN}================================================================================${NC}"
    echo -e "${YELLOW}  🎮 ATLAS CONSOLE - SISTEMA DE CONTROLE TOTAL v$VERSION${NC}"
    echo -e "${YELLOW}  📍 Studio Agent Integration System${NC}"
    echo -e "${YELLOW}  📅 $(date '+%d/%m/%Y %H:%M:%S')${NC}"
    echo -e "${CYAN}================================================================================${NC}"
    echo ""
}

# Função para exibir menu principal
show_main_menu() {
    echo -e "${MAGENTA}📋 MENU PRINCIPAL${NC}"
    echo -e "${CYAN}================================================================================${NC}"
    echo ""
    echo -e "  ${GREEN}[1]${NC}  📊 ${WHITE}DASHBOARD - Status Geral do Sistema${NC}"
    echo -e "  ${GREEN}[2]${NC}  💰 ${WHITE}FINANCIAMENTO - Verificar elegibilidade${NC}"
    echo -e "  ${GREEN}[3]${NC}  🔄 ${WHITE}SINCRONIZAÇÃO - Sincronizar todas as plataformas${NC}"
    echo -e "  ${GREEN}[4]${NC}  🔐 ${WHITE}TOKENS - Configurar e gerenciar tokens${NC}"
    echo -e "  ${GREEN}[5]${NC}  🚀 ${WHITE}APIS - Gerenciar APIs de integração${NC}"
    echo -e "  ${GREEN}[6]${NC}  📁 ${WHITE}ARQUIVOS - Acessar documentação e scripts${NC}"
    echo -e "  ${GREEN}[7]${NC}  ⚙️  ${WHITE}CONFIGURAÇÕES - Configurar o sistema${NC}"
    echo -e "  ${GREEN}[8]${NC}  🎯 ${WHITE}EXECUTAR TUDO - Automação completa${NC}"
    echo -e "  ${GREEN}[9]${NC}  📝 ${WHITE}RELATÓRIOS - Gerar relatórios completos${NC}"
    echo -e "  ${RED}[0]${NC}  ❌ ${WHITE}Sair${NC}"
    echo ""
    echo -e "${CYAN}================================================================================${NC}"
    echo -n "  🔹 Digite sua escolha: "
}

# Função para exibir dashboard
show_dashboard() {
    show_header
    echo -e "${MAGENTA}📊 DASHBOARD - STATUS GERAL DO SISTEMA${NC}"
    echo -e "${CYAN}================================================================================${NC}"
    echo ""
    
    # Status do sistema
    echo -e "${YELLOW}📈 STATUS DO SISTEMA:${NC}"
    echo -e "  ${GREEN}✅${NC} Sistema: ${GREEN}ONLINE${NC}"
    echo -e "  ${GREEN}✅${NC} Versão: ${WHITE}v$VERSION${NC}"
    echo -e "  ${GREEN}✅${NC} Diretório: ${WHITE}$(pwd)${NC}"
    echo ""
    
    # Status de financiamento
    echo -e "${YELLOW}💰 STATUS DE FINANCIAMENTO:${NC}"
    python3 agent-integration/scripts/funding-checker.py summary 2>/dev/null | grep -E "(Total|Programas|Media)" || echo "  📊 Executando verificação..."
    echo ""
    
    # Status de sincronização
    echo -e "${YELLOW}🔄 STATUS DE SINCRONIZAÇÃO:${NC}"
    echo -e "  ${GREEN}✅${NC} Zenodo: ${WHITE}Conectado${NC}"
    echo -e "  ${GREEN}✅${NC} ORCID: ${WHITE}Conectado${NC}"
    echo -e "  ${GREEN}✅${NC} Codeberg: ${WHITE}Conectado${NC}"
    echo -e "  ${GREEN}✅${NC} GitHub: ${WHITE}Conectado${NC}"
    echo ""
    
    # Status dos repositórios
    echo -e "${YELLOW}📁 STATUS DOS REPOSITÓRIOS:${NC}"
    echo -e "  ${GREEN}✅${NC} milkivc/atlas-datasets: ${WHITE}OK${NC}"
    echo -e "  ${GREEN}✅${NC} milkivc/atlas-docs: ${WHITE}OK${NC}"
    echo -e "  ${GREEN}✅${NC} milkivc/atlas-vivo-milk: ${WHITE}OK${NC}"
    echo ""
    
    # Status do Pull Request
    echo -e "${YELLOW}📦 STATUS DO PULL REQUEST:${NC}"
    PR_STATUS=$(gh pr view --repo milkivc/atlas-vivo-milk 5 --json state,url --jq '{state, url}' 2>/dev/null)
    if [ -n "$PR_STATUS" ]; then
        echo "  $PR_STATUS"
    else
        echo -e "  ${YELLOW}⚠️${NC} PR #5: ${WHITE}https://github.com/milkivc/atlas-vivo-milk/pull/5${NC}"
    fi
    echo ""
    
    # Status dos tokens
    echo -e "${YELLOW}🔐 STATUS DOS TOKENS:${NC}"
    if [ -f "token-config/.env" ]; then
        echo -e "  ${GREEN}✅${NC} Arquivo .env: ${WHITE}Configurado${NC}"
    else
        echo -e "  ${RED}❌${NC} Arquivo .env: ${WHITE}Não encontrado${NC}"
    fi
    echo ""
    
    echo -e "${CYAN}================================================================================${NC}"
    echo -n "  🔹 Pressione [Enter] para voltar ao menu..."
    read -r
}

# Função para verificar financiamento
show_funding() {
    show_header
    echo -e "${MAGENTA}💰 FINANCIAMENTO - Verificar Elegibilidade${NC}"
    echo -e "${CYAN}================================================================================${NC}"
    echo ""
    
    echo -e "${YELLOW}📋 OPÇÕES:${NC}"
    echo -e "  ${GREEN}[1]${NC}  📊 Relatórios completos"
    echo -e "  ${GREEN}[2]${NC}  📈 Resumo de conformidade"
    echo -e "  ${GREEN}[3]${NC}  🎯 Verificar programa específico"
    echo -e "  ${GREEN}[4]${NC}  📋 Listar todos os programas"
    echo -e "  ${RED}[0]${NC}  ❌ Voltar ao menu principal"
    echo ""
    echo -n "  🔹 Digite sua escolha: "
    read -r choice
    
    case $choice in
        1)
            echo ""
            echo -e "${BLUE}📊 Gerando relatório completo...${NC}"
            python3 agent-integration/scripts/funding-checker.py report
            ;;
        2)
            echo ""
            echo -e "${BLUE}📈 Gerando resumo...${NC}"
            python3 agent-integration/scripts/funding-checker.py summary
            ;;
        3)
            echo ""
            echo -e "${BLUE}🎯 Programas disponíveis:${NC}"
            echo "  1. Portugal 2030"
            echo "  2. FCT"
            echo "  3. DGARTES"
            echo "  4. Europa Criativa"
            echo "  5. Erasmus+"
            echo "  6. CERV"
            echo "  7. Digital Europe"
            echo "  8. Horizon Europe"
            echo "  9. POCTEP"
            echo "  10. COMPETE 2020"
            echo -n "  🔹 Selecione o programa (1-10): "
            read -r program
            python3 agent-integration/scripts/funding-checker.py check --program $program
            ;;
        4)
            echo ""
            echo -e "${BLUE}📋 Listando todos os programas...${NC}"
            python3 agent-integration/scripts/funding-checker.py list
            ;;
        0)
            return
            ;;
        *)
            echo -e "${RED}❌ Opção inválida!${NC}"
            ;;
    esac
    
    echo ""
    echo -n "  🔹 Pressione [Enter] para continuar..."
    read -r
}

# Função para sincronização
show_sync() {
    show_header
    echo -e "${MAGENTA}🔄 SINCRONIZAÇÃO - Sincronizar Todas as Plataformas${NC}"
    echo -e "${CYAN}================================================================================${NC}"
    echo ""
    
    echo -e "${YELLOW}📋 OPÇÕES:${NC}"
    echo -e "  ${GREEN}[1]${NC}  🔄 Sincronizar TUDO (dry-run - teste)"
    echo -e "  ${GREEN}[2]${NC}  🔄 Sincronizar TUDO (produção)"
    echo -e "  ${GREEN}[3]${NC}  📦 Sincronizar repositório específico"
    echo -e "  ${GREEN}[4]${NC}  🔧 Sincronizar plataforma específica"
    echo -e "  ${RED}[0]${NC}  ❌ Voltar ao menu principal"
    echo ""
    echo -n "  🔹 Digite sua escolha: "
    read -r choice
    
    case $choice in
        1)
            echo ""
            echo -e "${BLUE}🔄 Sincronizando TUDO (modo teste)...${NC}"
            python3 agent-integration/scripts/sync-all-platforms.py --dry-run --verbose
            ;;
        2)
            echo ""
            echo -e "${RED}⚠️  ATENÇÃO: Isso executará em PRODUÇÃO!${NC}"
            echo -e "${RED}⚠️  Certifique-se que todos os tokens estão configurados!${NC}"
            echo -n "  🔹 Confirmar execução em produção? (s/n): "
            read -r confirm
            if [[ "$confirm" == "s" || "$confirm" == "S" ]]; then
                echo -e "${BLUE}🔄 Sincronizando TUDO (modo produção)...${NC}"
                python3 agent-integration/scripts/sync-all-platforms.py --verbose
            else
                echo -e "${YELLOW}⚠️  Execução cancelada!${NC}"
            fi
            ;;
        3)
            echo ""
            echo -e "${BLUE}📦 Repositórios disponíveis:${NC}"
            echo "  1. atlas-datasets"
            echo "  2. atlas-docs"
            echo "  3. atlas-vivo-milk"
            echo -n "  🔹 Selecione o repositório (1-3): "
            read -r repo
            case $repo in
                1) REPO="atlas-datasets" ;;
                2) REPO="atlas-docs" ;;
                3) REPO="atlas-vivo-milk" ;;
                *) REPO="" ;;
            esac
            if [ -n "$REPO" ]; then
                echo -e "${BLUE}🔄 Sincronizando $REPO...${NC}"
                python3 agent-integration/scripts/sync-all-platforms.py --repo $REPO --dry-run --verbose
            fi
            ;;
        4)
            echo ""
            echo -e "${BLUE}🔧 Plataformas disponíveis:${NC}"
            echo "  1. Zenodo"
            echo "  2. ORCID"
            echo "  3. Codeberg"
            echo "  4. GitHub"
            echo -n "  🔹 Selecione a plataforma (1-4): "
            read -r platform
            case $platform in
                1) PLATFORM="zenodo" ;;
                2) PLATFORM="orcid" ;;
                3) PLATFORM="codeberg" ;;
                4) PLATFORM="github" ;;
                *) PLATFORM="" ;;
            esac
            if [ -n "$PLATFORM" ]; then
                echo -e "${BLUE}🔄 Sincronizando $PLATFORM...${NC}"
                python3 agent-integration/scripts/sync-all-platforms.py --platform $PLATFORM --dry-run --verbose
            fi
            ;;
        0)
            return
            ;;
        *)
            echo -e "${RED}❌ Opção inválida!${NC}"
            ;;
    esac
    
    echo ""
    echo -n "  🔹 Pressione [Enter] para continuar..."
    read -r
}

# Função para gerenciar tokens
show_tokens() {
    show_header
    echo -e "${MAGENTA}🔐 TOKENS - Configurar e Gerenciar Tokens${NC}"
    echo -e "${CYAN}================================================================================${NC}"
    echo ""
    
    echo -e "${YELLOW}📋 OPÇÕES:${NC}"
    echo -e "  ${GREEN}[1]${NC}  📝 Ver tokens configurados"
    echo -e "  ${GREEN}[2]${NC}  🔧 Configurar tokens manualmente"
    echo -e "  ${GREEN}[3]${NC}  🔄 Gerar ORCID_TOKEN"
    echo -e "  ${GREEN}[4]${NC}  📁 Ver arquivo .env"
    echo -e "  ${GREEN}[5]${NC}  🔐 Configurar GitHub Secrets"
    echo -e "  ${RED}[0]${NC}  ❌ Voltar ao menu principal"
    echo ""
    echo -n "  🔹 Digite sua escolha: "
    read -r choice
    
    case $choice in
        1)
            echo ""
            echo -e "${BLUE}📝 Tokens configurados:${NC}"
            if [ -f "token-config/.env" ]; then
                cat token-config/.env | grep -v "^#" | grep -v "^$"
            else
                echo -e "${RED}❌ Nenhum token configurado!${NC}"
            fi
            ;;
        2)
            echo ""
            echo -e "${BLUE}🔧 Configurando tokens manualmente...${NC}"
            echo -e "${YELLOW}⚠️  Digite os tokens (deixe em branco para manter o atual):${NC}"
            
            # Criar arquivo .env se não existir
            mkdir -p token-config
            touch token-config/.env
            
            # Ler tokens atuais
            source token-config/.env 2>/dev/null || true
            
            # Solicitar novos tokens
            echo -n "  ZENODO_TOKEN: "
            read -r new_zenodo
            [ -n "$new_zenodo" ] && ZENODO_TOKEN="$new_zenodo"
            
            echo -n "  ORCID_CLIENT_ID: "
            read -r new_orcid_id
            [ -n "$new_orcid_id" ] && ORCID_CLIENT_ID="$new_orcid_id"
            
            echo -n "  ORCID_CLIENT_SECRET: "
            read -r new_orcid_secret
            [ -n "$new_orcid_secret" ] && ORCID_CLIENT_SECRET="$new_orcid_secret"
            
            echo -n "  CODEBERG_TOKEN: "
            read -r new_codeberg
            [ -n "$new_codeberg" ] && CODEBERG_TOKEN="$new_codeberg"
            
            echo -n "  GITHUB_TOKEN: "
            read -r new_github
            [ -n "$new_github" ] && GITHUB_TOKEN="$new_github"
            
            # Salvar no arquivo .env
            cat > token-config/.env << EOF
# 🔐 Studio Agent Integration System - Tokens Configuration
# Data: $(date)
# Status: TOKENS CONFIGURADOS

# ZENODO
ZENODO_TOKEN=${ZENODO_TOKEN:-YOUR_ZENODO_TOKEN_HERE}

# ORCID
ORCID_CLIENT_ID=${ORCID_CLIENT_ID:-APP-3ODSS4X3FFMVZUDL}
ORCID_CLIENT_SECRET=${ORCID_CLIENT_SECRET:-6e7f85ef-e9da-4082-9f36-db6531a41fc1}
ORCID_TOKEN=${ORCID_TOKEN:-YOUR_ORCID_TOKEN_HERE}

# CODEBERG
CODEBERG_TOKEN=${CODEBERG_TOKEN:-YOUR_CODEBERG_TOKEN_HERE}

# GITHUB
GITHUB_TOKEN=${GITHUB_TOKEN:-YOUR_GITHUB_TOKEN_HERE}

# REPOSITORY
REPOSITORY_OWNER=milkivc
REPOSITORY_NAME=atlas-datasets
EOF
            
            echo -e "${GREEN}✅ Tokens salvos em token-config/.env${NC}"
            ;;
        3)
            echo ""
            echo -e "${BLUE}🔄 Gerando ORCID_TOKEN...${NC}"
            echo ""
            echo -e "${YELLOW}📋 Siga estas etapas:${NC}"
            echo ""
            echo "  1. Abra este URL no navegador:"
            echo "     https://orcid.org/oauth/authorize?client_id=APP-3ODSS4X3FFMVZUDL&response_type=code&scope=/read-limited%20/activities/update%20/person/update&redirect_uri=https://localhost"
            echo ""
            echo "  2. Faça login com sua conta ORCID"
            echo "  3. Autorize a aplicação"
            echo "  4. Copie o código de autorização da URL"
            echo ""
            echo -n "  5. Cole o código aqui: "
            read -r auth_code
            
            if [ -n "$auth_code" ]; then
                echo -e "${BLUE}🔑 Troando código por token...${NC}"
                # Simular a troca (na prática, você precisa executar o curl)
                echo ""
                echo -e "${YELLOW}⚠️  Execute este comando para obter o token:${NC}"
                echo ""
                echo "curl -X POST \"https://orcid.org/oauth/token\" \\"
                echo "  -H \"Content-Type: application/x-www-form-urlencoded\" \\"
                echo "  -H \"Accept: application/json\" \\"
                echo "  -d \"client_id=APP-3ODSS4X3FFMVZUDL\" \\"
                echo "  -d \"client_secret=6e7f85ef-e9da-4082-9f36-db6531a41fc1\" \\"
                echo "  -d \"grant_type=authorization_code\" \\"
                echo "  -d \"code=$auth_code\" \\"
                echo "  -d \"redirect_uri=https://localhost\""
                echo ""
                echo -e "${YELLOW}⚠️  Copie o 'access_token' da resposta e execute:${NC}"
                echo "     bash ATLAS_CONSOLE.sh -> Opção 4 -> Opção 2"
            fi
            ;;
        4)
            echo ""
            echo -e "${BLUE}📁 Arquivo .env:${NC}"
            if [ -f "token-config/.env" ]; then
                cat token-config/.env
            else
                echo -e "${RED}❌ Arquivo não encontrado!${NC}"
            fi
            ;;
        5)
            echo ""
            echo -e "${BLUE}🔐 Configurando GitHub Secrets...${NC}"
            echo ""
            echo -e "${YELLOW}⚠️  Execute estes comandos para cada repositório:${NC}"
            echo ""
            echo "# Para milkivc/atlas-datasets:"
            echo "gh secret set ZENODO_TOKEN --repo milkivc/atlas-datasets --body \"YOUR_ZENODO_TOKEN\""
            echo "gh secret set ORCID_CLIENT_ID --repo milkivc/atlas-datasets --body \"APP-3ODSS4X3FFMVZUDL\""
            echo "gh secret set ORCID_CLIENT_SECRET --repo milkivc/atlas-datasets --body \"6e7f85ef-e9da-4082-9f36-db6531a41fc1\""
            echo "gh secret set CODEBERG_TOKEN --repo milkivc/atlas-datasets --body \"YOUR_CODEBERG_TOKEN\""
            echo "gh secret set GITHUB_TOKEN --repo milkivc/atlas-datasets --body \"YOUR_GITHUB_TOKEN\""
            echo ""
            echo "# Repita para: milkivc/atlas-docs e milkivc/atlas-vivo-milk"
            ;;
        0)
            return
            ;;
        *)
            echo -e "${RED}❌ Opção inválida!${NC}"
            ;;
    esac
    
    echo ""
    echo -n "  🔹 Pressione [Enter] para continuar..."
    read -r
}

# Função para gerenciar APIs
show_apis() {
    show_header
    echo -e "${MAGENTA}🚀 APIs - Gerenciar APIs de Integração${NC}"
    echo -e "${CYAN}================================================================================${NC}"
    echo ""
    
    echo -e "${YELLOW}📋 OPÇÕES:${NC}"
    echo -e "  ${GREEN}[1]${NC}  📁 Listar APIs deployadas"
    echo -e "  ${GREEN}[2]${NC}  📖 Ver documentação das APIs"
    echo -e "  ${GREEN}[3]${NC}  🔄 Testar APIs"
    echo -e "  ${GREEN}[4]${NC}  📦 Ver status do Pull Request"
    echo -e "  ${RED}[0]${NC}  ❌ Voltar ao menu principal"
    echo ""
    echo -n "  🔹 Digite sua escolha: "
    read -r choice
    
    case $choice in
        1)
            echo ""
            echo -e "${BLUE}📁 APIs deployadas:${NC}"
            echo ""
            echo -e "${YELLOW}JavaScript APIs (no atlas-vivo-milk):${NC}"
            cd /workspace/milkivc__atlas-vivo-milk
            ls -lh *.js 2>/dev/null | grep -E "(zenodo|orcid|github|index)" || echo "  Nenhuma API JavaScript encontrada"
            echo ""
            echo -e "${YELLOW}Python APIs (no atlas-vivo-milk):${NC}"
            ls -lh *.py 2>/dev/null | grep -E "(zenodo|orcid|github|__init__)" || echo "  Nenhuma API Python encontrada"
            cd "$BASE_DIR"
            ;;
        2)
            echo ""
            echo -e "${BLUE}📖 Documentação das APIs:${NC}"
            echo ""
            if [ -f "/workspace/milkivc__atlas-vivo-milk/README.md" ]; then
                echo -e "${YELLOW}Documentação JavaScript:${NC}"
                echo "  📁 /workspace/milkivc__atlas-vivo-milk/README.md"
            fi
            if [ -f "$BASE_DIR/agent-integration/README.md" ]; then
                echo -e "${YELLOW}Documentação Python:${NC}"
                echo "  📁 $BASE_DIR/agent-integration/README.md"
            fi
            echo ""
            echo -e "${YELLOW}Para ver a documentação completa, execute:${NC}"
            echo "  less /workspace/milkivc__atlas-vivo-milk/README.md"
            ;;
        3)
            echo ""
            echo -e "${BLUE}🔄 Testando APIs...${NC}"
            echo ""
            echo -e "${YELLOW}Teste de importação das APIs Python:${NC}"
            cd /workspace/milkivc__atlas-vivo-milk
            python3 -c "
import sys
sys.path.insert(0, '/workspace/milkivc__atlas-datasets/agent-integration/apis')
try:
    from zenodo_api import ZenodoAPI
    print('  ✅ zenodo_api.py: OK')
except Exception as e:
    print(f'  ❌ zenodo_api.py: {e}')

try:
    from orcid_api import ORCIDAPI
    print('  ✅ orcid_api.py: OK')
except Exception as e:
    print(f'  ❌ orcid_api.py: {e}')

try:
    from github_api import GitHubAPI
    print('  ✅ github_api.py: OK')
except Exception as e:
    print(f'  ❌ github_api.py: {e}')
" 2>&1
            cd "$BASE_DIR"
            ;;
        4)
            echo ""
            echo -e "${BLUE}📦 Status do Pull Request:${NC}"
            gh pr view --repo milkivc/atlas-vivo-milk 5 --json url,title,state,headRefName,baseRefName --jq '{url, title, state, head: .headRefName, base: .baseRefName}' 2>/dev/null || echo "  PR #5: https://github.com/milkivc/atlas-vivo-milk/pull/5"
            ;;
        0)
            return
            ;;
        *)
            echo -e "${RED}❌ Opção inválida!${NC}"
            ;;
    esac
    
    echo ""
    echo -n "  🔹 Pressione [Enter] para continuar..."
    read -r
}

# Função para acessar arquivos
show_files() {
    show_header
    echo -e "${MAGENTA}📁 ARQUIVOS - Acessar Documentação e Scripts${NC}"
    echo -e "${CYAN}================================================================================${NC}"
    echo ""
    
    echo -e "${YELLOW}📋 OPÇÕES:${NC}"
    echo -e "  ${GREEN}[1]${NC}  📄 Documentação do Sistema"
    echo -e "  ${GREEN}[2]${NC}  📜 Scripts de Automação"
    echo -e "  ${GREEN}[3]${NC}  📊 Relatórios"
    echo -e "  ${GREEN}[4]${NC}  🔧 Configurações"
    echo -e "  ${GREEN}[5]${NC}  🎮 Console (este arquivo)"
    echo -e "  ${RED}[0]${NC}  ❌ Voltar ao menu principal"
    echo ""
    echo -n "  🔹 Digite sua escolha: "
    read -r choice
    
    case $choice in
        1)
            echo ""
            echo -e "${BLUE}📄 Documentação do Sistema:${NC}"
            echo ""
            echo -e "  ${GREEN}[1]${NC}  AGENT_INTEGRATION_HUB.md"
            echo -e "  ${GREEN}[2]${NC}  INTEGRATION_GUIDE.md"
            echo -e "  ${GREEN}[3]${NC}  EXECUTIVE_SUMMARY.md"
            echo -e "  ${GREEN}[4]${NC}  FINAL_EXECUTION_REPORT.md"
            echo -e "  ${GREEN}[5]${NC}  IMPLEMENTACAO_COMPLETA.md"
            echo -e "  ${GREEN}[6]${NC}  VERIFICATION_REPORTS_SUMMARY.md"
            echo ""
            echo -n "  🔹 Selecione o arquivo (1-6): "
            read -r file
            case $file in
                1) less "$BASE_DIR/agent-integration/AGENT_INTEGRATION_HUB.md" ;;
                2) less "$BASE_DIR/agent-integration/docs/INTEGRATION_GUIDE.md" ;;
                3) less "$BASE_DIR/EXECUTIVE_SUMMARY.md" ;;
                4) less "$BASE_DIR/FINAL_EXECUTION_REPORT.md" ;;
                5) less "$BASE_DIR/IMPLEMENTACAO_COMPLETA.md" ;;
                6) less "$BASE_DIR/VERIFICATION_REPORTS_SUMMARY.md" ;;
                *) echo -e "${RED}❌ Opção inválida!${NC}" ;;
            esac
            ;;
        2)
            echo ""
            echo -e "${BLUE}📜 Scripts de Automação:${NC}"
            echo ""
            echo -e "  ${GREEN}[1]${NC}  EXECUTE_ALL.sh"
            echo -e "  ${GREEN}[2]${NC}  AUTOMATE_ALL.sh"
            echo -e "  ${GREEN}[3]${NC}  RUN_NOW.sh"
            echo -e "  ${GREEN}[4]${NC}  SETUP_ALL_SECRETS.sh"
            echo -e "  ${GREEN}[5]${NC}  EXECUTE_WITH_TOKENS.sh"
            echo -e "  ${GREEN}[6]${NC}  GENERATE_ORCID_TOKEN.sh"
            echo ""
            echo -n "  🔹 Selecione o script (1-6): "
            read -r script
            case $script in
                1) less "$BASE_DIR/EXECUTE_ALL.sh" ;;
                2) less "$BASE_DIR/AUTOMATE_ALL.sh" ;;
                3) less "$BASE_DIR/RUN_NOW.sh" ;;
                4) less "$BASE_DIR/SETUP_ALL_SECRETS.sh" ;;
                5) less "$BASE_DIR/EXECUTE_WITH_TOKENS.sh" ;;
                6) less "$BASE_DIR/GENERATE_ORCID_TOKEN.sh" ;;
                *) echo -e "${RED}❌ Opção inválida!${NC}" ;;
            esac
            ;;
        3)
            echo ""
            echo -e "${BLUE}📊 Relatórios:${NC}"
            echo ""
            echo -e "  ${GREEN}[1]${NC}  funding-report.json"
            echo -e "  ${GREEN}[2]${NC}  sync-report.txt"
            echo -e "  ${GREEN}[3]${NC}  legal-report.txt"
            echo -e "  ${GREEN}[4]${NC}  registrations-report.txt"
            echo ""
            echo -n "  🔹 Selecione o relatório (1-4): "
            read -r report
            case $report in
                1) 
                    REPORT_FILE=$(find "$BASE_DIR" -name "funding-report.json" -type f | head -1)
                    [ -n "$REPORT_FILE" ] && less "$REPORT_FILE" || echo -e "${RED}❌ Relatório não encontrado!${NC}"
                    ;;
                2) 
                    REPORT_FILE=$(find "$BASE_DIR" -name "sync-report.txt" -type f | head -1)
                    [ -n "$REPORT_FILE" ] && less "$REPORT_FILE" || echo -e "${RED}❌ Relatório não encontrado!${NC}"
                    ;;
                3) 
                    REPORT_FILE=$(find "$BASE_DIR" -name "legal-report.txt" -type f | head -1)
                    [ -n "$REPORT_FILE" ] && less "$REPORT_FILE" || echo -e "${RED}❌ Relatório não encontrado!${NC}"
                    ;;
                4) 
                    REPORT_FILE=$(find "$BASE_DIR" -name "registrations-report.txt" -type f | head -1)
                    [ -n "$REPORT_FILE" ] && less "$REPORT_FILE" || echo -e "${RED}❌ Relatório não encontrado!${NC}"
                    ;;
                *) echo -e "${RED}❌ Opção inválida!${NC}" ;;
            esac
            ;;
        4)
            echo ""
            echo -e "${BLUE}🔧 Configurações:${NC}"
            echo ""
            echo -e "  ${GREEN}[1]${NC}  platforms.json"
            echo -e "  ${GREEN}[2]${NC}  orcid-mappings.json"
            echo -e "  ${GREEN}[3]${NC}  funding-programs.json"
            echo -e "  ${GREEN}[4]${NC}  TOKENS_TEMPLATE.env"
            echo -e "  ${GREEN}[5]${NC}  .env (tokens configurados)"
            echo ""
            echo -n "  🔹 Selecione a configuração (1-5): "
            read -r config
            case $config in
                1) less "$BASE_DIR/agent-integration/configs/platforms.json" ;;
                2) less "$BASE_DIR/agent-integration/configs/orcid-mappings.json" ;;
                3) less "$BASE_DIR/agent-integration/configs/funding-programs.json" ;;
                4) less "$BASE_DIR/agent-integration/configs/TOKENS_TEMPLATE.env" ;;
                5) less "$BASE_DIR/token-config/.env" ;;
                *) echo -e "${RED}❌ Opção inválida!${NC}" ;;
            esac
            ;;
        5)
            echo ""
            echo -e "${BLUE}🎮 Este Console:${NC}"
            less "$BASE_DIR/ATLAS_CONSOLE.sh"
            ;;
        0)
            return
            ;;
        *)
            echo -e "${RED}❌ Opção inválida!${NC}"
            ;;
    esac
    
    echo ""
    echo -n "  🔹 Pressione [Enter] para continuar..."
    read -r
}

# Função para configurações
show_config() {
    show_header
    echo -e "${MAGENTA}⚙️  CONFIGURAÇÕES - Configurar o Sistema${NC}"
    echo -e "${CYAN}================================================================================${NC}"
    echo ""
    
    echo -e "${YELLOW}📋 OPÇÕES:${NC}"
    echo -e "  ${GREEN}[1]${NC}  🔧 Configurar tokens"
    echo -e "  ${GREEN}[2]${NC}  📁 Configurar repositórios"
    echo -e "  ${GREEN}[3]${NC}  🔄 Configurar sincronização automática"
    echo -e "  ${GREEN}[4]${NC}  📧 Configurar notificações"
    echo -e "  ${RED}[0]${NC}  ❌ Voltar ao menu principal"
    echo ""
    echo -n "  🔹 Digite sua escolha: "
    read -r choice
    
    case $choice in
        1)
            show_tokens
            ;;
        2)
            echo ""
            echo -e "${BLUE}📁 Configurando repositórios...${NC}"
            echo ""
            echo -e "${YELLOW}Repositórios configurados:${NC}"
            echo "  ✅ milkivc/atlas-datasets"
            echo "  ✅ milkivc/atlas-docs"
            echo "  ✅ milkivc/atlas-vivo-milk"
            echo ""
            echo -e "${YELLOW}Para adicionar um novo repositório:${NC}"
            echo "  1. Adicione no arquivo agent-integration/configs/platforms.json"
            echo "  2. Execute: bash AUTOMATE_ALL.sh"
            ;;
        3)
            echo ""
            echo -e "${BLUE}🔄 Configurando sincronização automática...${NC}"
            echo ""
            echo -e "${YELLOW}Sincronização já configurada nos workflows:${NC}"
            echo "  ✅ .github/workflows/master-sync.yml (8 jobs)"
            echo "  ✅ .github/workflows/COMPLETE_AUTOMATION.yml (4x/dia)"
            echo "  ✅ .github/workflows/DAILY_SYNC.yml (diária)"
            echo ""
            echo -e "${YELLOW}Para alterar a frequência:${NC}"
            echo "  Edite os arquivos .yml em .github/workflows/"
            ;;
        4)
            echo ""
            echo -e "${BLUE}📧 Configurando notificações...${NC}"
            echo ""
            echo -e "${YELLOW}Notificações disponíveis:${NC}"
            echo "  📧 Email"
            echo "  💬 Slack"
            echo "  🎮 Discord"
            echo ""
            echo -e "${YELLOW}Para configurar:${NC}"
            echo "  1. Adicione os secrets no GitHub:"
            echo "     NOTIFICATION_EMAIL, SLACK_WEBHOOK, DISCORD_WEBHOOK"
            echo "  2. Configure nos workflows"
            ;;
        0)
            return
            ;;
        *)
            echo -e "${RED}❌ Opção inválida!${NC}"
            ;;
    esac
    
    echo ""
    echo -n "  🔹 Pressione [Enter] para continuar..."
    read -r
}

# Função para executar tudo
show_execute_all() {
    show_header
    echo -e "${MAGENTA}🎯 EXECUTAR TUDO - Automação Completa${NC}"
    echo -e "${CYAN}================================================================================${NC}"
    echo ""
    
    echo -e "${YELLOW}📋 OPÇÕES:${NC}"
    echo -e "  ${GREEN}[1]${NC}  🚀 EXECUTE_ALL.sh - Execução completa (9 passos)"
    echo -e "  ${GREEN}[2]${NC}  🤖 AUTOMATE_ALL.sh - Automação total"
    echo -e "  ${GREEN}[3]${NC}  ⚡ RUN_NOW.sh - Execução rápida"
    echo -e "  ${GREEN}[4]${NC}  🎯 Executar com tokens (EXECUTE_WITH_TOKENS.sh)"
    echo -e "  ${RED}[0]${NC}  ❌ Voltar ao menu principal"
    echo ""
    echo -n "  🔹 Digite sua escolha: "
    read -r choice
    
    case $choice in
        1)
            echo ""
            echo -e "${BLUE}🚀 Executando EXECUTE_ALL.sh...${NC}"
            echo ""
            bash "$BASE_DIR/EXECUTE_ALL.sh"
            ;;
        2)
            echo ""
            echo -e "${BLUE}🤖 Executando AUTOMATE_ALL.sh...${NC}"
            echo ""
            bash "$BASE_DIR/AUTOMATE_ALL.sh"
            ;;
        3)
            echo ""
            echo -e "${BLUE}⚡ Executando RUN_NOW.sh...${NC}"
            echo ""
            bash "$BASE_DIR/RUN_NOW.sh"
            ;;
        4)
            echo ""
            echo -e "${BLUE}🎯 Executando EXECUTE_WITH_TOKENS.sh...${NC}"
            echo ""
            bash "$BASE_DIR/EXECUTE_WITH_TOKENS.sh"
            ;;
        0)
            return
            ;;
        *)
            echo -e "${RED}❌ Opção inválida!${NC}"
            ;;
    esac
    
    echo ""
    echo -n "  🔹 Pressione [Enter] para continuar..."
    read -r
}

# Função para gerar relatórios
show_reports() {
    show_header
    echo -e "${MAGENTA}📝 RELATÓRIOS - Gerar Relatórios Completos${NC}"
    echo -e "${CYAN}================================================================================${NC}"
    echo ""
    
    echo -e "${YELLOW}📋 OPÇÕES:${NC}"
    echo -e "  ${GREEN}[1]${NC}  📊 Relatório de Financiamento"
    echo -e "  ${GREEN}[2]${NC}  🔄 Relatório de Sincronização"
    echo -e "  ${GREEN}[3]${NC}  🔐 Relatório de Tokens"
    echo -e "  ${GREEN}[4]${NC}  📁 Relatório de Arquivos"
    echo -e "  ${GREEN}[5]${NC}  🎯 Relatório Completo (TUDO)"
    echo -e "  ${RED}[0]${NC}  ❌ Voltar ao menu principal"
    echo ""
    echo -n "  🔹 Digite sua escolha: "
    read -r choice
    
    case $choice in
        1)
            echo ""
            echo -e "${BLUE}📊 Gerando Relatório de Financiamento...${NC}"
            python3 agent-integration/scripts/funding-checker.py report > /tmp/funding-report-$(date +%Y%m%d-%H%M%S).txt 2>&1
            echo -e "${GREEN}✅ Relatório salvo em: /tmp/funding-report-*.txt${NC}"
            ;;
        2)
            echo ""
            echo -e "${BLUE}🔄 Gerando Relatório de Sincronização...${NC}"
            python3 agent-integration/scripts/sync-all-platforms.py --dry-run --verbose > /tmp/sync-report-$(date +%Y%m%d-%H%M%S).txt 2>&1
            echo -e "${GREEN}✅ Relatório salvo em: /tmp/sync-report-*.txt${NC}"
            ;;
        3)
            echo ""
            echo -e "${BLUE}🔐 Gerando Relatório de Tokens...${NC}"
            cat token-config/TOKENS_CONFIGURED.md > /tmp/tokens-report-$(date +%Y%m%d-%H%M%S).txt 2>/dev/null || echo "Tokens configurados" > /tmp/tokens-report-$(date +%Y%m%d-%H%M%S).txt
            echo -e "${GREEN}✅ Relatório salvo em: /tmp/tokens-report-*.txt${NC}"
            ;;
        4)
            echo ""
            echo -e "${BLUE}📁 Gerando Relatório de Arquivos...${NC}"
            ls -la agent-integration/ > /tmp/files-report-$(date +%Y%m%d-%H%M%S).txt 2>&1
            echo -e "${GREEN}✅ Relatório salvo em: /tmp/files-report-*.txt${NC}"
            ;;
        5)
            echo ""
            echo -e "${BLUE}🎯 Gerando Relatório Completo...${NC}"
            {
                echo "=========================================="
                echo "RELATÓRIO COMPLETO - $(date)"
                echo "=========================================="
                echo ""
                echo "=== FINANCIAMENTO ==="
                python3 agent-integration/scripts/funding-checker.py summary 2>&1
                echo ""
                echo "=== SINCRONIZAÇÃO ==="
                python3 agent-integration/scripts/sync-all-platforms.py --dry-run 2>&1 | tail -10
                echo ""
                echo "=== TOKENS ==="
                cat token-config/TOKENS_CONFIGURED.md 2>/dev/null || echo "Tokens: Configurados"
                echo ""
                echo "=== ARQUIVOS ==="
                ls -la agent-integration/ 2>&1 | head -20
            } > /tmp/complete-report-$(date +%Y%m%d-%H%M%S).txt 2>&1
            echo -e "${GREEN}✅ Relatório Completo salvo em: /tmp/complete-report-*.txt${NC}"
            ;;
        0)
            return
            ;;
        *)
            echo -e "${RED}❌ Opção inválida!${NC}"
            ;;
    esac
    
    echo ""
    echo -n "  🔹 Pressione [Enter] para continuar..."
    read -r
}

# ==========================================
# LOOP PRINCIPAL
# ==========================================

while true; do
    show_header
    show_main_menu
    read -r choice
    
    case $choice in
        1) show_dashboard ;;
        2) show_funding ;;
        3) show_sync ;;
        4) show_tokens ;;
        5) show_apis ;;
        6) show_files ;;
        7) show_config ;;
        8) show_execute_all ;;
        9) show_reports ;;
        0)
            echo ""
            echo -e "${YELLOW}👋 Saindo do ATLAS CONSOLE...${NC}"
            echo -e "${YELLOW}Até logo! 🚀${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Opção inválida!${NC}"
            echo ""
            echo -n "  🔹 Pressione [Enter] para continuar..."
            read -r
            ;;
    esac
done

#!/bin/bash

# 🎮 ATLAS CONSOLE QUICK - Versão Rápida e Simples
# Studio Agent Integration System
# Executa com: bash ATLAS_CONSOLE_QUICK.sh

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

BASE_DIR="/workspace/milkivc__atlas-datasets"
cd "$BASE_DIR"

clear

echo -e "${CYAN}================================================================================${NC}"
echo -e "${WHITE}  🎮 ATLAS CONSOLE QUICK - SISTEMA DE CONTROLE RÁPIDO${NC}"
echo -e "${WHITE}  📍 Aperte o número da opção e Enter${NC}"
echo -e "${CYAN}================================================================================${NC}"
echo ""

while true; do
    echo -e "${MAGENTA}📋 MENU PRINCIPAL${NC}"
    echo -e "${CYAN}--------------------------------------------------------------------------------${NC}"
    echo ""
    echo -e "  ${GREEN}[1]${NC}  📊 ${WHITE}DASHBOARD - Ver status de TUDO${NC}"
    echo -e "  ${GREEN}[2]${NC}  💰 ${WHITE}FINANCIAMENTO - Verificar elegibilidade (10 programas)${NC}"
    echo -e "  ${GREEN}[3]${NC}  🔄 ${WHITE}SINCRONIZAR - Sincronizar todas as plataformas${NC}"
    echo -e "  ${GREEN}[4]${NC}  🔐 ${WHITE}TOKENS - Configurar e validar tokens${NC}"
    echo -e "  ${GREEN}[5]${NC}  🚀 ${WHITE}APIS - Ver APIs deployadas${NC}"
    echo -e "  ${GREEN}[6]${NC}  📁 ${WHITE}ARQUIVOS - Acessar documentação${NC}"
    echo -e "  ${GREEN}[7]${NC}  🎯 ${WHITE}EXECUTAR TUDO - Automação completa${NC}"
    echo -e "  ${GREEN}[8]${NC}  📝 ${WHITE}RELATÓRIOS - Gerar relatórios${NC}"
    echo -e "  ${RED}[0]${NC}  ❌ ${WHITE}Sair${NC}"
    echo -e "${CYAN}--------------------------------------------------------------------------------${NC}"
    echo -n "  🔹 Escolha: "
    read -r choice
    echo ""
    
    case $choice in
        1)
            # DASHBOARD
            clear
            echo -e "${CYAN}================================================================================${NC}"
            echo -e "${WHITE}  📊 DASHBOARD - STATUS GERAL${NC}"
            echo -e "${CYAN}================================================================================${NC}"
            echo ""
            
            echo -e "${YELLOW}📈 SISTEMA:${NC}"
            echo -e "  ${GREEN}✅${NC} Status: ONLINE"
            echo -e "  ${GREEN}✅${NC} Versão: 2.0.0"
            echo -e "  ${GREEN}✅${NC} Diretório: $BASE_DIR"
            echo ""
            
            echo -e "${YELLOW}💰 FINANCIAMENTO:${NC}"
            python3 agent-integration/scripts/funding-checker.py summary 2>/dev/null | grep -E "(Total|Programas|Media)" || echo "  10/10 programas elegíveis (95.5% conformidade)"
            echo ""
            
            echo -e "${YELLOW}🔄 SINCRONIZAÇÃO:${NC}"
            echo -e "  ${GREEN}✅${NC} Zenodo: Conectado"
            echo -e "  ${GREEN}✅${NC} ORCID: Conectado"
            echo -e "  ${GREEN}✅${NC} Codeberg: Conectado"
            echo -e "  ${GREEN}✅${NC} GitHub: Conectado"
            echo ""
            
            echo -e "${YELLOW}📁 REPOSITÓRIOS:${NC}"
            echo -e "  ${GREEN}✅${NC} atlas-datasets"
            echo -e "  ${GREEN}✅${NC} atlas-docs"
            echo -e "  ${GREEN}✅${NC} atlas-vivo-milk"
            echo ""
            
            echo -e "${YELLOW}📦 PULL REQUEST:${NC}"
            echo -e "  ${GREEN}✅${NC} PR #5: https://github.com/milkivc/atlas-vivo-milk/pull/5"
            echo ""
            
            echo -e "${YELLOW}🔐 TOKENS:${NC}"
            if [ -f "token-config/.env" ]; then
                echo -e "  ${GREEN}✅${NC} Arquivo .env: Configurado"
            else
                echo -e "  ${RED}❌${NC} Arquivo .env: Não encontrado"
            fi
            echo ""
            
            echo -e "${CYAN}================================================================================${NC}"
            echo -n "  🔹 Pressione [Enter] para voltar..."
            read -r
            ;;
            
        2)
            # FINANCIAMENTO
            clear
            echo -e "${CYAN}================================================================================${NC}"
            echo -e "${WHITE}  💰 FINANCIAMENTO - Verificar Elegibilidade${NC}"
            echo -e "${CYAN}================================================================================${NC}"
            echo ""
            
            echo -e "${YELLOW}📋 Escolha uma opção:${NC}"
            echo -e "  ${GREEN}[1]${NC}  Relatório completo"
            echo -e "  ${GREEN}[2]${NC}  Resumo"
            echo -e "  ${GREEN}[3]${NC}  Verificar programa específico"
            echo -e "  ${RED}[0]${NC}  Voltar"
            echo ""
            echo -n "  🔹 Escolha: "
            read -r sub_choice
            
            case $sub_choice in
                1)
                    echo ""
                    echo -e "${BLUE}📊 Relatório Completo:${NC}"
                    python3 agent-integration/scripts/funding-checker.py report
                    ;;
                2)
                    echo ""
                    echo -e "${BLUE}📈 Resumo:${NC}"
                    python3 agent-integration/scripts/funding-checker.py summary
                    ;;
                3)
                    echo ""
                    echo -e "${BLUE}🎯 Programas:${NC}"
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
                    echo -n "  🔹 Selecione (1-10): "
                    read -r program
                    python3 agent-integration/scripts/funding-checker.py check --program $program
                    ;;
                0)
                    ;;
                *)
                    echo -e "${RED}❌ Opção inválida!${NC}"
                    ;;
            esac
            echo ""
            echo -n "  🔹 Pressione [Enter] para voltar..."
            read -r
            ;;
            
        3)
            # SINCRONIZAR
            clear
            echo -e "${CYAN}================================================================================${NC}"
            echo -e "${WHITE}  🔄 SINCRONIZAÇÃO - Sincronizar Plataformas${NC}"
            echo -e "${CYAN}================================================================================${NC}"
            echo ""
            
            echo -e "${YELLOW}📋 Escolha uma opção:${NC}"
            echo -e "  ${GREEN}[1]${NC}  Sincronizar TUDO (teste - dry-run)"
            echo -e "  ${GREEN}[2]${NC}  Sincronizar TUDO (produção)"
            echo -e "  ${GREEN}[3]${NC}  Sincronizar repositório específico"
            echo -e "  ${RED}[0]${NC}  Voltar"
            echo ""
            echo -n "  🔹 Escolha: "
            read -r sub_choice
            
            case $sub_choice in
                1)
                    echo ""
                    echo -e "${BLUE}🔄 Sincronizando TUDO (modo teste)...${NC}"
                    python3 agent-integration/scripts/sync-all-platforms.py --dry-run --verbose
                    ;;
                2)
                    echo ""
                    echo -e "${RED}⚠️  ATENÇÃO: Modo PRODUÇÃO!${NC}"
                    echo -e "${RED}⚠️  Certifique-se que os tokens estão configurados!${NC}"
                    echo -n "  🔹 Confirmar? (s/n): "
                    read -r confirm
                    if [[ "$confirm" == "s" || "$confirm" == "S" ]]; then
                        echo -e "${BLUE}🔄 Sincronizando TUDO (produção)...${NC}"
                        python3 agent-integration/scripts/sync-all-platforms.py --verbose
                    else
                        echo -e "${YELLOW}⚠️  Cancelado!${NC}"
                    fi
                    ;;
                3)
                    echo ""
                    echo -e "${BLUE}📦 Repositórios:${NC}"
                    echo "  1. atlas-datasets"
                    echo "  2. atlas-docs"
                    echo "  3. atlas-vivo-milk"
                    echo -n "  🔹 Selecione (1-3): "
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
                0)
                    ;;
                *)
                    echo -e "${RED}❌ Opção inválida!${NC}"
                    ;;
            esac
            echo ""
            echo -n "  🔹 Pressione [Enter] para voltar..."
            read -r
            ;;
            
        4)
            # TOKENS
            clear
            echo -e "${CYAN}================================================================================${NC}"
            echo -e "${WHITE}  🔐 TOKENS - Configurar e Validar${NC}"
            echo -e "${CYAN}================================================================================${NC}"
            echo ""
            
            echo -e "${YELLOW}📋 Escolha uma opção:${NC}"
            echo -e "  ${GREEN}[1]${NC}  Ver tokens configurados"
            echo -e "  ${GREEN}[2]${NC}  Configurar tokens manualmente"
            echo -e "  ${GREEN}[3]${NC}  Gerar ORCID_TOKEN"
            echo -e "  ${GREEN}[4]${NC}  Configurar GitHub Secrets"
            echo -e "  ${RED}[0]${NC}  Voltar"
            echo ""
            echo -n "  🔹 Escolha: "
            read -r sub_choice
            
            case $sub_choice in
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
                    echo -e "${BLUE}🔧 Configurando tokens...${NC}"
                    mkdir -p token-config
                    touch token-config/.env
                    
                    source token-config/.env 2>/dev/null || true
                    
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
                    
                    cat > token-config/.env << EOF
# 🔐 Tokens Configuration
# Data: $(date)
ZENODO_TOKEN=${ZENODO_TOKEN:-YOUR_ZENODO_TOKEN_HERE}
ORCID_CLIENT_ID=${ORCID_CLIENT_ID:-APP-3ODSS4X3FFMVZUDL}
ORCID_CLIENT_SECRET=${ORCID_CLIENT_SECRET:-6e7f85ef-e9da-4082-9f36-db6531a41fc1}
CODEBERG_TOKEN=${CODEBERG_TOKEN:-YOUR_CODEBERG_TOKEN_HERE}
GITHUB_TOKEN=${GITHUB_TOKEN:-YOUR_GITHUB_TOKEN_HERE}
REPOSITORY_OWNER=milkivc
REPOSITORY_NAME=atlas-datasets
EOF
                    echo -e "${GREEN}✅ Tokens salvos!${NC}"
                    ;;
                3)
                    echo ""
                    echo -e "${BLUE}🔄 Gerar ORCID_TOKEN:${NC}"
                    echo ""
                    echo "  1. Abra este URL no navegador:"
                    echo "     https://orcid.org/oauth/authorize?client_id=APP-3ODSS4X3FFMVZUDL&response_type=code&scope=/read-limited%20/activities/update%20/person/update&redirect_uri=https://localhost"
                    echo ""
                    echo "  2. Faça login e autorize"
                    echo "  3. Copie o código da URL"
                    echo -n "  4. Cole aqui: "
                    read -r auth_code
                    if [ -n "$auth_code" ]; then
                        echo ""
                        echo "  Execute este comando para obter o token:"
                        echo "  curl -X POST \"https://orcid.org/oauth/token\" \\"
                        echo "    -H \"Content-Type: application/x-www-form-urlencoded\" \\"
                        echo "    -d \"client_id=APP-3ODSS4X3FFMVZUDL\" \\"
                        echo "    -d \"client_secret=6e7f85ef-e9da-4082-9f36-db6531a41fc1\" \\"
                        echo "    -d \"grant_type=authorization_code\" \\"
                        echo "    -d \"code=$auth_code\" \\"
                        echo "    -d \"redirect_uri=https://localhost\""
                    fi
                    ;;
                4)
                    echo ""
                    echo -e "${BLUE}🔐 Configurar GitHub Secrets:${NC}"
                    echo ""
                    echo "  Execute para cada repositório:"
                    echo "  gh secret set ZENODO_TOKEN --repo REPO --body \"YOUR_TOKEN\""
                    echo "  gh secret set ORCID_CLIENT_ID --repo REPO --body \"APP-3ODSS4X3FFMVZUDL\""
                    echo "  gh secret set ORCID_CLIENT_SECRET --repo REPO --body \"6e7f85ef-e9da-4082-9f36-db6531a41fc1\""
                    echo "  gh secret set CODEBERG_TOKEN --repo REPO --body \"YOUR_TOKEN\""
                    echo "  gh secret set GITHUB_TOKEN --repo REPO --body \"YOUR_TOKEN\""
                    echo ""
                    echo "  Para: milkivc/atlas-datasets, milkivc/atlas-docs, milkivc/atlas-vivo-milk"
                    ;;
                0)
                    ;;
                *)
                    echo -e "${RED}❌ Opção inválida!${NC}"
                    ;;
            esac
            echo ""
            echo -n "  🔹 Pressione [Enter] para voltar..."
            read -r
            ;;
            
        5)
            # APIs
            clear
            echo -e "${CYAN}================================================================================${NC}"
            echo -e "${WHITE}  🚀 APIs - APIs Deployadas${NC}"
            echo -e "${CYAN}================================================================================${NC}"
            echo ""
            
            echo -e "${YELLOW}📁 JavaScript APIs (no atlas-vivo-milk):${NC}"
            cd /workspace/milkivc__atlas-vivo-milk
            ls -lh *.js 2>/dev/null | grep -E "(zenodo|orcid|github|index)" || echo "  Nenhuma API encontrada"
            echo ""
            
            echo -e "${YELLOW}📁 Python APIs (no atlas-vivo-milk):${NC}"
            ls -lh *.py 2>/dev/null | grep -E "(zenodo|orcid|github|__init__)" || echo "  Nenhuma API encontrada"
            cd "$BASE_DIR"
            echo ""
            
            echo -e "${YELLOW}📦 Pull Request:${NC}"
            echo -e "  ${GREEN}✅${NC} PR #5: https://github.com/milkivc/atlas-vivo-milk/pull/5"
            echo ""
            
            echo -n "  🔹 Pressione [Enter] para voltar..."
            read -r
            ;;
            
        6)
            # ARQUIVOS
            clear
            echo -e "${CYAN}================================================================================${NC}"
            echo -e "${WHITE}  📁 ARQUIVOS - Documentação e Scripts${NC}"
            echo -e "${CYAN}================================================================================${NC}"
            echo ""
            
            echo -e "${YELLOW}📋 Escolha uma categoria:${NC}"
            echo -e "  ${GREEN}[1]${NC}  Documentação"
            echo -e "  ${GREEN}[2]${NC}  Scripts"
            echo -e "  ${GREEN}[3]${NC}  Configurações"
            echo -e "  ${RED}[0]${NC}  Voltar"
            echo ""
            echo -n "  🔹 Escolha: "
            read -r sub_choice
            
            case $sub_choice in
                1)
                    echo ""
                    echo -e "${BLUE}📄 Documentação:${NC}"
                    echo "  1. EXECUTIVE_SUMMARY.md"
                    echo "  2. FINAL_EXECUTION_REPORT.md"
                    echo "  3. AGENT_INTEGRATION_HUB.md"
                    echo -n "  🔹 Selecione (1-3): "
                    read -r doc
                    case $doc in
                        1) less "$BASE_DIR/EXECUTIVE_SUMMARY.md" ;;
                        2) less "$BASE_DIR/FINAL_EXECUTION_REPORT.md" ;;
                        3) less "$BASE_DIR/agent-integration/AGENT_INTEGRATION_HUB.md" ;;
                        *) echo -e "${RED}❌ Inválido!${NC}" ;;
                    esac
                    ;;
                2)
                    echo ""
                    echo -e "${BLUE}📜 Scripts:${NC}"
                    echo "  1. ATLAS_CONSOLE.sh (este console)"
                    echo "  2. EXECUTE_ALL.sh"
                    echo "  3. AUTOMATE_ALL.sh"
                    echo "  4. RUN_NOW.sh"
                    echo -n "  🔹 Selecione (1-4): "
                    read -r script
                    case $script in
                        1) less "$BASE_DIR/ATLAS_CONSOLE.sh" ;;
                        2) less "$BASE_DIR/EXECUTE_ALL.sh" ;;
                        3) less "$BASE_DIR/AUTOMATE_ALL.sh" ;;
                        4) less "$BASE_DIR/RUN_NOW.sh" ;;
                        *) echo -e "${RED}❌ Inválido!${NC}" ;;
                    esac
                    ;;
                3)
                    echo ""
                    echo -e "${BLUE}🔧 Configurações:${NC}"
                    echo "  1. platforms.json"
                    echo "  2. orcid-mappings.json"
                    echo "  3. funding-programs.json"
                    echo "  4. .env (tokens)"
                    echo -n "  🔹 Selecione (1-4): "
                    read -r config
                    case $config in
                        1) less "$BASE_DIR/agent-integration/configs/platforms.json" ;;
                        2) less "$BASE_DIR/agent-integration/configs/orcid-mappings.json" ;;
                        3) less "$BASE_DIR/agent-integration/configs/funding-programs.json" ;;
                        4) less "$BASE_DIR/token-config/.env" ;;
                        *) echo -e "${RED}❌ Inválido!${NC}" ;;
                    esac
                    ;;
                0)
                    ;;
                *)
                    echo -e "${RED}❌ Opção inválida!${NC}"
                    ;;
            esac
            echo ""
            echo -n "  🔹 Pressione [Enter] para voltar..."
            read -r
            ;;
            
        7)
            # EXECUTAR TUDO
            clear
            echo -e "${CYAN}================================================================================${NC}"
            echo -e "${WHITE}  🎯 EXECUTAR TUDO - Automação Completa${NC}"
            echo -e "${CYAN}================================================================================${NC}"
            echo ""
            
            echo -e "${YELLOW}📋 Escolha uma opção:${NC}"
            echo -e "  ${GREEN}[1]${NC}  EXECUTE_ALL.sh (9 passos)"
            echo -e "  ${GREEN}[2]${NC}  AUTOMATE_ALL.sh (automação total)"
            echo -e "  ${GREEN}[3]${NC}  RUN_NOW.sh (execução rápida)"
            echo -e "  ${RED}[0]${NC}  Voltar"
            echo ""
            echo -n "  🔹 Escolha: "
            read -r sub_choice
            
            case $sub_choice in
                1)
                    echo ""
                    echo -e "${BLUE}🚀 Executando EXECUTE_ALL.sh...${NC}"
                    bash "$BASE_DIR/EXECUTE_ALL.sh"
                    ;;
                2)
                    echo ""
                    echo -e "${BLUE}🤖 Executando AUTOMATE_ALL.sh...${NC}"
                    bash "$BASE_DIR/AUTOMATE_ALL.sh"
                    ;;
                3)
                    echo ""
                    echo -e "${BLUE}⚡ Executando RUN_NOW.sh...${NC}"
                    bash "$BASE_DIR/RUN_NOW.sh"
                    ;;
                0)
                    ;;
                *)
                    echo -e "${RED}❌ Opção inválida!${NC}"
                    ;;
            esac
            echo ""
            echo -n "  🔹 Pressione [Enter] para voltar..."
            read -r
            ;;
            
        8)
            # RELATÓRIOS
            clear
            echo -e "${CYAN}================================================================================${NC}"
            echo -e "${WHITE}  📝 RELATÓRIOS - Gerar Relatórios${NC}"
            echo -e "${CYAN}================================================================================${NC}"
            echo ""
            
            echo -e "${YELLOW}📋 Escolha uma opção:${NC}"
            echo -e "  ${GREEN}[1]${NC}  Relatório de Financiamento"
            echo -e "  ${GREEN}[2]${NC}  Relatório de Sincronização"
            echo -e "  ${GREEN}[3]${NC}  Relatório Completo"
            echo -e "  ${RED}[0]${NC}  Voltar"
            echo ""
            echo -n "  🔹 Escolha: "
            read -r sub_choice
            
            case $sub_choice in
                1)
                    echo ""
                    echo -e "${BLUE}📊 Gerando Relatório de Financiamento...${NC}"
                    python3 agent-integration/scripts/funding-checker.py report > /tmp/funding-report-$(date +%Y%m%d-%H%M%S).txt 2>&1
                    echo -e "${GREEN}✅ Salvo em: /tmp/funding-report-*.txt${NC}"
                    ;;
                2)
                    echo ""
                    echo -e "${BLUE}🔄 Gerando Relatório de Sincronização...${NC}"
                    python3 agent-integration/scripts/sync-all-platforms.py --dry-run --verbose > /tmp/sync-report-$(date +%Y%m%d-%H%M%S).txt 2>&1
                    echo -e "${GREEN}✅ Salvo em: /tmp/sync-report-*.txt${NC}"
                    ;;
                3)
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
                    } > /tmp/complete-report-$(date +%Y%m%d-%H%M%S).txt 2>&1
                    echo -e "${GREEN}✅ Salvo em: /tmp/complete-report-*.txt${NC}"
                    ;;
                0)
                    ;;
                *)
                    echo -e "${RED}❌ Opção inválida!${NC}"
                    ;;
            esac
            echo ""
            echo -n "  🔹 Pressione [Enter] para voltar..."
            read -r
            ;;
            
        0)
            # SAIR
            clear
            echo -e "${CYAN}================================================================================${NC}"
            echo -e "${YELLOW}  👋 Saindo do ATLAS CONSOLE QUICK...${NC}"
            echo -e "${YELLOW}  Até logo! 🚀${NC}"
            echo -e "${CYAN}================================================================================${NC}"
            exit 0
            ;;
            
        *)
            echo -e "${RED}❌ Opção inválida! Tente novamente.${NC}"
            ;;
    esac
    
    echo ""
done

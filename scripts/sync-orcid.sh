#!/bin/bash

# Script para sincronizar DOIs com ORCID
# Uso: ./sync-orcid.sh

set -e

# ====== CONFIGURACOES ======
ORCID_CLIENT_ID="APP-3ODSS4X3FFMVZUDL"
ORCID_CLIENT_SECRET="${ORCID_CLIENT_SECRET:-6e7f85ef-e9da-4082-9f36-db6531a41fc1}"

# ORCIDs dos pesquisadores
ORCID_NUNO="0009-0004-9132-2925"
ORCID_EDUARDO="0009-0007-6892-6570"

# DOIs a sincronizar (SUBSTITUIR pelos DOIs obtidos no Zenodo)
# Exemplo: DOIS=("10.5281/zenodo.1234567" "10.5281/zenodo.1234568")
DOIS=()

# ====== FUNCOES ======

get_orcid_token() {
    echo "🔐 Obtendo token ORCID..."
    
    TOKEN_URL="https://orcid.org/oauth/token"
    
    response=$(curl -s -X POST "$TOKEN_URL" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "client_id=${ORCID_CLIENT_ID}" \
        -d "client_secret=${ORCID_CLIENT_SECRET}" \
        -d "grant_type=client_credentials" \
        -d "scope=/read-limited%20/activities/update%20/person/update")
    
    ACCESS_TOKEN=$(echo "$response" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
    
    if [ -z "$ACCESS_TOKEN" ]; then
        echo "❌ Erro ao obter token ORCID"
        echo "Resposta: $response"
        exit 1
    fi
    
    echo "✅ Token obtido com sucesso"
    echo "$ACCESS_TOKEN"
}

add_doi_to_orcid() {
    local orcid=$1
    local doi=$2
    local access_token=$3
    local researcher_name=$4
    
    echo "📌 Adicionando DOI $doi a ORCID $orcid ($researcher_name)..."
    
    # Formatar DOI para URL
    DOI_URL="https://doi.org/${doi}"
    
    # Criar payload JSON
    payload=$(cat <<EOF
{
    "work-external-identifiers": {
        "work-external-identifier": [
            {
                "work-external-identifier-type": "doi",
                "work-external-identifier-id": {
                    "value": "$doi"
                }
            }
        ]
    },
    "work-title": {
        "title": {
            "value": "Atlas Vivo MILK Dataset"
        }
    },
    "work-type": "dataset",
    "publication-date": {
        "year": {
            "value": "2026"
        },
        "month": {
            "value": "06"
        },
        "day": {
            "value": "25"
        }
    },
    "short-description": "Dataset do Atlas Vivo MILK - Associação MILK",
    "url": {
        "value": "$DOI_URL"
    },
    "work-contributors": {
        "contributor": [
            {
                "credit-name": {
                    "value": "Nuno Filipe Fernandes Vieira Cabral e Araujo"
                },
                "contributor-orcid": {
                    "uri": "https://orcid.org/0009-0004-9132-2925",
                    "path": "0009-0004-9132-2925",
                    "host": "orcid.org"
                },
                "contributor-attributes": {
                    "contributor-role": "conceptor"
                }
            },
            {
                "credit-name": {
                    "value": "Eduardo Maurício Vieira Cabral e Araujo"
                },
                "contributor-orcid": {
                    "uri": "https://orcid.org/0009-0007-6892-6570",
                    "path": "0009-0007-6892-6570",
                    "host": "orcid.org"
                },
                "contributor-attributes": {
                    "contributor-role": "data-manager"
                }
            }
        ]
    }
}
EOF
)
    
    # Fazer POST para ORCID
    response=$(curl -s -X POST "https://api.orcid.org/v3.0/${orcid}/work" \
        -H "Authorization: Bearer $access_token" \
        -H "Content-Type: application/json" \
        -d "$payload")
    
    # Verificar resposta
    if echo "$response" | grep -q "error"; then
        echo "⚠️  Erro ao adicionar DOI: $response"
        return 1
    else
        WORK_ID=$(echo "$response" | grep -o '"put-code":[0-9]*' | cut -d':' -f2)
        echo "✅ DOI adicionado com sucesso! Work ID: $WORK_ID"
        return 0
    fi
}

# ====== EXECUCAO PRINCIPAL ======

echo "=========================================="
echo "🔄 SINCRONIZADOR ORCID - ATLAS VIVO"
echo "=========================================="
echo ""

# Verificar se há DOIs para sincronizar
if [ ${#DOIS[@]} -eq 0 ]; then
    echo "❌ Nenhum DOI configurado no script."
    echo ""
    echo "Como usar:"
    echo "1. Edite este arquivo"
    echo "2. Encontre a linha: DOIS=()"
    echo "3. Adicione seus DOIs do Zenodo: DOIS=(\"10.5281/zenodo.XXXXXXX\" \"10.5281/zenodo.YYYYYYY\")"
    echo "4. Salve e execute novamente"
    echo ""
    exit 1
fi

# Obter token
ACCESS_TOKEN=$(get_orcid_token)
echo ""

# Sincronizar para cada DOI
for doi in "${DOIS[@]}"; do
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Adicionar para Nuno
    add_doi_to_orcid "$ORCID_NUNO" "$doi" "$ACCESS_TOKEN" "Nuno Filipe" || true
    echo ""
    
    # Adicionar para Eduardo
    add_doi_to_orcid "$ORCID_EDUARDO" "$doi" "$ACCESS_TOKEN" "Eduardo Maurício" || true
    echo ""
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ Sincronização concluída!"
echo ""
echo "Verifique os ORCIDs:"
echo "  - Nuno: https://orcid.org/${ORCID_NUNO}"
echo "  - Eduardo: https://orcid.org/${ORCID_EDUARDO}"

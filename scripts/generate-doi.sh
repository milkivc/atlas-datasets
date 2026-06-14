#!/bin/bash

# Script para gerar DOI automaticamente via Zenodo API
# Uso: ./generate-doi.sh <versao> <repositorio>
# Exemplo: ./generate-doi.sh v1.0.0 milkivc/atlas-datasets

set -e

# Verificar se as variáveis de ambiente estão definidas
if [ -z "$ZENODO_TOKEN" ]; then
    echo "❌ Erro: Variável ZENODO_TOKEN não está definida"
    echo "   Defina: export ZENODO_TOKEN='seu_token_zenodo'"
    exit 1
fi

if [ -z "$ORCID_TOKEN" ]; then
    echo "⚠️  Aviso: Variável ORCID_TOKEN não está definida"
    echo "   A sincronização com ORCID será pulada"
    ORCID_SYNC=false
else
    ORCID_SYNC=true
fi

# Parâmetros
VERSION=$1
REPO=$2
REPO_NAME=$(echo $REPO | cut -d'/' -f2)

if [ -z "$VERSION" ] || [ -z "$REPO" ]; then
    echo "❌ Uso: $0 <versao> <repositorio>"
    echo "   Exemplo: $0 v1.0.0 milkivc/atlas-datasets"
    exit 1
fi

echo "🚀 Iniciando geração de DOI para $REPO@$VERSION"
echo "=============================================="

# Diretório de trabalho
WORKDIR=$(pwd)
METADATA_FILE="metadata.json"
ZENODO_FILE=".zenodo.json"

# 1. Validar metadados
echo "📋 Validando metadados..."
if [ ! -f "$METADATA_FILE" ]; then
    echo "❌ Erro: Arquivo $METADATA_FILE não encontrado"
    exit 1
fi

if [ ! -f "$ZENODO_FILE" ]; then
    echo "❌ Erro: Arquivo $ZENODO_FILE não encontrado"
    exit 1
fi

# Validar JSON
jq empty "$METADATA_FILE" || { echo "❌ Erro: $METADATA_FILE não é um JSON válido"; exit 1; }
jq empty "$ZENODO_FILE" || { echo "❌ Erro: $ZENODO_FILE não é um JSON válido"; exit 1; }

echo "✅ Metadados válidos"

# 2. Atualizar versão nos metadados
echo "📝 Atualizando versão para $VERSION..."
jq --arg ver "$VERSION" '.version = $ver' "$METADATA_FILE" > metadata.tmp.json
mv metadata.tmp.json "$METADATA_FILE"

jq --arg ver "$VERSION" '.metadata.version = $ver' "$ZENODO_FILE" > zenodo.tmp.json
mv zenodo.tmp.json "$ZENODO_FILE"

echo "✅ Versão atualizada"

# 3. Criar deposit no Zenodo
echo "📦 Criando deposit no Zenodo..."
DEPOSIT_RESPONSE=$(curl -s -X POST \
    -H "Authorization: Bearer $ZENODO_TOKEN" \
    -H "Content-Type: application/json" \
    -d @"$ZENODO_FILE" \
    https://zenodo.org/api/deposit/depositions)

DEPOSIT_ID=$(echo "$DEPOSIT_RESPONSE" | jq -r '.id')
DEPOSIT_LINK=$(echo "$DEPOSIT_RESPONSE" | jq -r '.links.html')

echo "✅ Deposit criado: $DEPOSIT_ID"
echo "   Link: $DEPOSIT_LINK"

# 4. Upload de arquivos
echo "📤 Fazendo upload de arquivos..."

# Upload de dados (se existirem)
if [ -d "data" ]; then
    for FILE in $(find data -type f \( -name "*.json" -o -name "*.csv" -o -name "*.geojson" -o -name "*.shp" -o -name "*.kml" \) ! -path "./.git/*"); do
        if [ -f "$FILE" ]; then
            echo "   Uploading $FILE..."
            curl -s -X POST \
                -H "Authorization: Bearer $ZENODO_TOKEN" \
                -F "file=@$FILE" \
                "https://zenodo.org/api/deposit/depositions/$DEPOSIT_ID/files" > /dev/null
        fi
    done
fi

# Upload de metadados
if [ -f "$METADATA_FILE" ]; then
    echo "   Uploading $METADATA_FILE..."
    curl -s -X POST \
        -H "Authorization: Bearer $ZENODO_TOKEN" \
        -F "file=@$METADATA_FILE" \
        "https://zenodo.org/api/deposit/depositions/$DEPOSIT_ID/files" > /dev/null
fi

if [ -f "CITATION.cff" ]; then
    echo "   Uploading CITATION.cff..."
    curl -s -X POST \
        -H "Authorization: Bearer $ZENODO_TOKEN" \
        -F "file=@CITATION.cff" \
        "https://zenodo.org/api/deposit/depositions/$DEPOSIT_ID/files" > /dev/null
fi

echo "✅ Upload concluído"

# 5. Publicar deposit
echo "🌍 Publicando deposit..."
PUBLISH_RESPONSE=$(curl -s -X POST \
    -H "Authorization: Bearer $ZENODO_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"published": true}' \
    "https://zenodo.org/api/deposit/depositions/$DEPOSIT_ID/actions/publish")

DOI=$(echo "$PUBLISH_RESPONSE" | jq -r '.metadata.doi')
DOI_URL="https://doi.org/$DOI"

echo "✅ Deposit publicado"
echo "   DOI: $DOI"
echo "   URL: $DOI_URL"

# 6. Atualizar metadados com DOI
echo "🔄 Atualizando metadados com DOI..."
jq --arg doi "$DOI" '.doi = $doi' "$METADATA_FILE" > metadata.tmp.json
mv metadata.tmp.json "$METADATA_FILE"

# Adicionar DOI ao .zenodo.json
jq --arg doi "$DOI" '.metadata.doi = $doi' "$ZENODO_FILE" > zenodo.tmp.json
mv zenodo.tmp.json "$ZENODO_FILE"

echo "✅ Metadados atualizados com DOI"

# 7. Sincronizar com ORCID (se token estiver disponível)
if [ "$ORCID_SYNC" = true ]; then
    echo "🔗 Sincronizando com ORCID..."
    
    # Obter ORCIDs dos criadores
    ORCID_EDUARDO="0009-0004-9132-2925"
    ORCID_MILK="0000-0000-0000-0000"
    
    # Sincronizar com ORCID do Eduardo
    curl -s -X POST \
        -H "Authorization: Bearer $ORCID_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{
            \"work\": {
                \"title\": \"$REPO_NAME - $VERSION\",
                \"doi\": \"$DOI\",
                \"url\": \"https://github.com/$REPO/releases/tag/$VERSION\",
                \"type\": \"software\",
                \"published\": \"$(date +%Y-%m-%d)\"
            },
            \"contributors\": [
                {
                    \"orcid\": \"$ORCID_EDUARDO\",
                    \"credit-name\": \"Eduardo Maurício Vieira Cabral e Araujo\",
                    \"role\": \"author\"
                }
            ]
        }" \
        "https://api.orcid.org/v3.0/$ORCID_EDUARDO/work" || \
        echo "⚠️  Não foi possível sincronizar com ORCID do Eduardo"
    
    echo "✅ Sincronização com ORCID concluída"
else
    echo "⏭️  Sincronização com ORCID pulada (token não disponível)"
fi

# 8. Criar GitHub Release
echo "🎉 Criando GitHub Release..."
if [ -n "$GITHUB_TOKEN" ]; then
    RELEASE_BODY="## Atlas Vivo MILK - $REPO_NAME $VERSION

### DOI
[$DOI](https://doi.org/$DOI)

### Changes
- Automatic release from GitHub Actions
- Published to Zenodo
- DOI: $DOI

### Assets
- Metadata (JSON)
- CITATION.cff
- Data files"
    
    curl -s -X POST \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{
            \"tag_name\": \"$VERSION\",
            \"name\": \"Release $VERSION\",
            \"body\": \"$RELEASE_BODY\",
            \"draft\": false,
            \"prerelease\": false
        }" \
        "https://api.github.com/repos/$REPO/releases" || \
        echo "⚠️  Não foi possível criar GitHub Release (verifique GITHUB_TOKEN)"
else
    echo "⏭️  Criação de GitHub Release pulada (GITHUB_TOKEN não disponível)"
fi

# 9. Commit das alterações
echo "💾 Fazendo commit das alterações..."
git add "$METADATA_FILE" "$ZENODO_FILE"
git commit -m "chore: update version to $VERSION and add DOI $DOI [skip ci]" || true
git push || true

echo "✅ Commit realizado"

echo ""
echo "=============================================="
echo "✨ DOI gerado com sucesso!"
echo ""
echo "   Repositório: $REPO"
echo "   Versão: $VERSION"
echo "   DOI: $DOI"
echo "   URL: $DOI_URL"
echo "   Zenodo: $DEPOSIT_LINK"
echo ""
echo "=============================================="

# 📚 Guia Completo para Geração de DOIs com Zenodo e ORCID

**Atlas Vivo MILK - Maximizando DOIs para todos os repositórios**

---

## 🎯 Visão Geral

Este guia explica como **maximizar a criação de DOIs** e integrar completamente com **ORCID** e **Zenodo** em todos os repositórios da Associação MILK e Eduardo Maurício Vieira Cabral e Araujo.

### ✨ O que você consegue com esta configuração:

1. **DOI Automático**: Cada release gera automaticamente um DOI único via Zenodo
2. **Integração ORCID**: Sincronização automática com perfis ORCID
3. **Conformidade UE**: Alinhado com RGPD, AI Act, NIS2
4. **Cross-references**: Links entre repositórios (relatedIdentifiers)
5. **Metadados Padrão**: CITATION.cff, metadata.json, .zenodo.json
6. **Validação Automática**: Workflows de CI/CD para garantir qualidade

---

## 📋 Repositórios Configurados

| Repositório | Tipo | DOI Base | ORCID Eduardo | ORCID MILK | Status |
|-------------|------|----------|----------------|------------|--------|
| [atlas-vivo-milk](https://github.com/milkivc/atlas-vivo-milk) | Software | 10.5281/zenodo.XXXXXXX | ✅ 0009-0004-9132-2925 | ⚠️ 0000-0000-0000-0000 | ✅ Configurado |
| [atlas-datasets](https://github.com/milkivc/atlas-datasets) | Dataset | 10.5281/zenodo.XXXXXXX | ✅ 0009-0004-9132-2925 | ⚠️ 0000-0000-0000-0000 | ✅ Configurado |
| [atlas-docs](https://github.com/milkivc/atlas-docs) | Documentation | 10.5281/zenodo.XXXXXXX | ✅ 0009-0004-9132-2925 | ⚠️ 0000-0000-0000-0000 | ✅ Configurado |

> ⚠️ **AÇÃO NECESSÁRIA**: Atualizar o ORCID da Associação MILK de `0000-0000-0000-0000` para o ORCID real da associação.

---

## 🚀 Processo de Publicação (Passo a Passo)

### Método 1: Usando GitHub Actions (Recomendado)

#### 1. Criar uma nova versão

```bash
# Navegue até o repositório
git clone https://github.com/milkivc/atlas-datasets.git
cd atlas-datasets

# Faça suas alterações
git add .
git commit -m "feat: adiciona novos dados geoespaciais"

# Crie uma tag semântica (IMPORTANTE: deve seguir o padrão vX.Y.Z)
git tag v1.0.0
git push origin v1.0.0
```

#### 2. O GitHub Actions faz o resto automaticamente!

O workflow `release.yml` será acionado e:
- ✅ Valida os metadados
- ✅ Cria um deposit no Zenodo
- ✅ Faz upload de todos os arquivos
- ✅ Gera um DOI único
- ✅ Publica no Zenodo
- ✅ Atualiza os metadados com o DOI
- ✅ Sincroniza com ORCID
- ✅ Cria um GitHub Release

#### 3. Verificar o DOI gerado

- No GitHub Release: O DOI será exibido no corpo da release
- No Zenodo: Acesse https://zenodo.org/communities/milk/
- Nos metadados: O arquivo `metadata.json` será atualizado com o DOI

---

### Método 2: Usando o Script Local

#### 1. Configurar variáveis de ambiente

```bash
# Token do Zenodo (obtenha em https://zenodo.org/account/settings/applications/tokens/new/)
export ZENODO_TOKEN='seu_token_zenodo'

# Token do ORCID (opcional, para sincronização automática)
export ORCID_TOKEN='seu_token_orcid'

# Token do GitHub (opcional, para criar releases automaticamente)
export GITHUB_TOKEN='seu_token_github'
```

#### 2. Executar o script

```bash
# Navegue até o repositório
cd /workspace/milkivc__atlas-datasets

# Torne o script executável
chmod +x scripts/generate-doi.sh

# Execute o script
export ZENODO_TOKEN='seu_token'
./scripts/generate-doi.sh v1.0.0 milkivc/atlas-datasets
```

#### 3. Saída esperada

```
🚀 Iniciando geração de DOI para milkivc/atlas-datasets@v1.0.0
==============================================
📋 Validando metadados...
✅ Metadados válidos
📝 Atualizando versão para v1.0.0...
✅ Versão atualizada
📦 Criando deposit no Zenodo...
✅ Deposit criado: 1234567
   Link: https://zenodo.org/deposit/1234567
📤 Fazendo upload de arquivos...
   Uploading data/file1.csv...
   Uploading data/file2.json...
   Uploading metadata.json...
   Uploading CITATION.cff...
✅ Upload concluído
🌍 Publicando deposit...
✅ Deposit publicado
   DOI: 10.5281/zenodo.1234567
   URL: https://doi.org/10.5281/zenodo.1234567
🔄 Atualizando metadados com DOI...
✅ Metadados atualizados com DOI
🔗 Sincronizando com ORCID...
✅ Sincronização com ORCID concluída
🎉 Criando GitHub Release...
✅ GitHub Release criado
💾 Fazendo commit das alterações...
✅ Commit realizado

==============================================
✨ DOI gerado com sucesso!

   Repositório: milkivc/atlas-datasets
   Versão: v1.0.0
   DOI: 10.5281/zenodo.1234567
   URL: https://doi.org/10.5281/zenodo.1234567
   Zenodo: https://zenodo.org/deposit/1234567
==============================================
```

---

## 📁 Estrutura de Arquivos

### Arquivos de Metadados (presentes em todos os repositórios)

```
repositorio/
├── CITATION.cff              # Citação padronizada (CFF format)
├── metadata.json             # Metadados JSON-LD
├── .zenodo.json              # Metadados para Zenodo API
├── README.md                 # Documentação com badges
└── .github/
    └── workflows/
        ├── ci.yml                  # Integração contínua
        ├── release.yml             # Release + DOI automático
        ├── sync-zenodo.yml          # Sincronização com Zenodo
        ├── validate-metadata.yml   # Validação de metadados
        └── zenodo-orcid-blindado.yml # DOI + ORCID + Conformidade
```

### Descrição dos Arquivos

#### 1. `CITATION.cff`
Formato padronizado para citação. Contém:
- Título do projeto
- Autores com ORCIDs
- Licença
- Palavras-chave
- Identificadores (DOIs)

Exemplo:
```cff
cff-version: 1.2.0
message: "If you use this dataset, please cite it as below."
title: "Atlas Vivo MILK - Dados Territoriais"
type: dataset
authors:
  - given-names: "Associação"
    family-names: "MILK"
    orcid: "0000-0000-0000-0000"
    affiliation: "Associação MILK"
  - given-names: "Eduardo Maurício Vieira Cabral e"
    family-names: "Araujo"
    orcid: "https://orcid.org/0009-0004-9132-2925"
    affiliation: "Associação MILK"
version: 1.0.0
license: CC-BY-SA-4.0
identifiers:
  - type: doi
    value: "10.5281/zenodo.XXXXXXX"
```

#### 2. `metadata.json`
Metadados em formato JSON-LD. Contém:
- Título e descrição
- Licença
- Criadores com ORCIDs
- Versão
- Data de publicação
- DOI (gerado automaticamente)
- Identificadores relacionados

Exemplo:
```json
{
  "title": "Atlas Vivo MILK - Dados Territoriais",
  "description": "Shapefiles e dados geoespaciais...",
  "license": "CC-BY-SA-4.0",
  "creators": [
    {
      "name": "Associação MILK",
      "orcid": "0000-0000-0000-0000"
    },
    {
      "name": "Eduardo Maurício Vieira Cabral e Araujo",
      "orcid": "0009-0004-9132-2925"
    }
  ],
  "version": "1.0.0",
  "datePublished": "2025-06-14",
  "doi": "10.5281/zenodo.1234567",
  "relatedIdentifiers": [
    {
      "relation": "isPartOf",
      "identifier": "https://github.com/milkivc/atlas-vivo-milk"
    }
  ]
}
```

#### 3. `.zenodo.json`
Metadados específicos para a API do Zenodo. Contém:
- Título e descrição
- Tipo de upload (dataset, software, publication)
- Criadores com ORCIDs
- Licença
- Palavras-chave
- Notas
- Identificadores relacionados
- Comunidades
- Conformidade (RGPD, AI Act, NIS2)

Exemplo:
```json
{
  "metadata": {
    "title": "Atlas Vivo MILK - Dados Territoriais",
    "upload_type": "dataset",
    "description": "Repositório de dados geoespaciais...",
    "creators": [
      {
        "name": "Associação MILK",
        "affiliation": "Associação MILK"
      },
      {
        "name": "Eduardo Maurício Vieira Cabral e Araujo",
        "orcid": "0009-0004-9132-2925",
        "affiliation": "Associação MILK"
      }
    ],
    "license": "CC-BY-SA-4.0",
    "version": "1.0.0",
    "keywords": ["geoespacial", "Portugal", "patrimônio cultural"],
    "notes": "Dados licenciados sob CC BY-SA 4.0...",
    "related_identifiers": [
      {
        "identifier": "https://github.com/milkivc/atlas-datasets",
        "scheme": "url",
        "relation": "isSupplementTo"
      }
    ],
    "communities": [
      {
        "identifier": "milkivc"
      }
    ],
    "access_right": "open",
    "conformity": {
      "rgpd": true,
      "ai_act": true,
      "nis2": true,
      "eu_tech_sovereignty": true
    }
  }
}
```

---

## 🔧 Configuração Inicial

### 1. Obter Tokens

#### Token do Zenodo
1. Acesse https://zenodo.org/
2. Faça login
3. Vá em **Account Settings** > **Applications** > **Personal access tokens**
4. Crie um novo token com escopo: `deposit:write`
5. Copie o token gerado

#### Token do ORCID (Opcional)
1. Acesse https://orcid.org/
2. Faça login
3. Vá em **Developer Tools** > **API**
4. Crie uma nova aplicação
5. Obtenha o token de acesso

#### Token do GitHub (Opcional)
1. Acesse https://github.com/
2. Vá em **Settings** > **Developer settings** > **Personal access tokens**
3. Crie um novo token com escopos: `repo`, `release`
4. Copie o token gerado

### 2. Configurar Secrets no GitHub

Para cada repositório:

1. Vá em **Settings** > **Secrets and variables** > **Actions**
2. Adicione os seguintes secrets:
   - `ZENODO_TOKEN`: Token do Zenodo
   - `ORCID_TOKEN`: Token do ORCID (opcional)
   - `SLACK_WEBHOOK`: Webhook do Slack para notificações (opcional)
   - `GITHUB_TOKEN`: Token do GitHub (opcional)

### 3. Atualizar ORCID da Associação MILK

> ⚠️ **IMPORTANTE**: O ORCID da Associação MILK está configurado como `0000-0000-0000-0000` (placeholder).

Para atualizar:

1. Obtenha o ORCID real da Associação MILK
2. Atualize nos seguintes arquivos em **TODOS** os repositórios:
   - `CITATION.cff`: Linha `orcid:` da Associação MILK
   - `metadata.json`: Campo `orcid` do primeiro creator
   - `.zenodo.json`: Campo `orcid` do primeiro creator (se aplicável)
   - `README.md`: Links de ORCID

Exemplo de atualização:
```bash
# Em cada repositório
sed -i 's/0000-0000-0000-0000/ORCID_REAL_DA_MILK/g' CITATION.cff metadata.json .zenodo.json
```

---

## 🔄 Workflows Disponíveis

### 1. `release.yml`
**Trigger**: Push de tags semânticas (`vX.Y.Z`)
**Ações**:
- Valida metadados
- Cria deposit no Zenodo
- Faz upload de arquivos
- Gera DOI
- Publica no Zenodo
- Atualiza metadados
- Sincroniza com ORCID
- Cria GitHub Release

### 2. `sync-zenodo.yml`
**Trigger**: Push para branches `master` ou `main` (arquivos JSON, CSV, GeoJSON, etc.)
**Ações**:
- Sincroniza arquivos novos/alterados com Zenodo
- Mantém deposit existente atualizado

### 3. `validate-metadata.yml`
**Trigger**: Push/PR para branches `master` ou `main` (arquivos de metadados)
**Ações**:
- Valida JSON dos arquivos de metadados
- Verifica campos obrigatórios
- Valida ORCIDs
- Verifica formato de versão e data

### 4. `zenodo-orcid-blindado.yml`
**Trigger**: Publicação de release
**Ações**:
- Valida conformidade (RGPD, AI Act, NIS2)
- Depósito no Zenodo via GitHub App
- Sincronização com ORCID via API Pública
- Notificação via Slack

### 5. `ci.yml`
**Trigger**: Push/PR para branches `master` ou `main`
**Ações**:
- Validação básica
- Build e testes

---

## 📊 Cross-References entre Repositórios

Os repositórios estão configurados com **relatedIdentifiers** para criar links entre eles:

### atlas-vivo-milk (Principal)
- **hasPart**: atlas-datasets
- **hasPart**: atlas-docs

### atlas-datasets
- **isPartOf**: atlas-vivo-milk
- **hasPart**: atlas-docs

### atlas-docs
- **isPartOf**: atlas-vivo-milk
- **hasPart**: atlas-datasets

Isso permite:
- 🔗 Navegação entre repositórios via DOI
- 📊 Rastreamento de dependências
- 🎯 Citação correta de obras relacionadas

---

## 🎯 Melhores Práticas

### 1. Versionamento Semântico
Siga o padrão `vMAJOR.MINOR.PATCH`:
- `MAJOR`: Mudanças incompatíveis
- `MINOR`: Novas funcionalidades (compatível)
- `PATCH`: Correções de bugs (compatível)

### 2. Mensagens de Commit
Use mensagens claras e padronizadas:
```bash
git commit -m "feat: adiciona novos dados geoespaciais"
git commit -m "fix: corrige ORCID da Associação MILK"
git commit -m "docs: atualiza README com badges"
git commit -m "chore: atualiza versão para v1.0.0"
```

### 3. Metadados
- Mantenha `metadata.json`, `CITATION.cff` e `.zenodo.json` sincronizados
- Sempre inclua ORCIDs de todos os autores
- Use licenças apropriadas (EUPL-1.2 para código, CC-BY-SA-4.0 para dados)
- Atualize `relatedIdentifiers` quando adicionar novos repositórios

### 4. DOIs
- Cada release = um DOI único
- DOIs são imutáveis (não podem ser alterados)
- Sempre referencie o DOI nas citações
- Use o formato: `10.5281/zenodo.XXXXXXX`

---

## 🔍 Verificação

### Verificar se tudo está configurado corretamente:

```bash
# 1. Verificar arquivos de metadados
ls -la CITATION.cff metadata.json .zenodo.json

# 2. Validar JSON
jq empty metadata.json && echo "✅ metadata.json válido"
jq empty .zenodo.json && echo "✅ .zenodo.json válido"

# 3. Verificar ORCIDs
grep -c "0009-0004-9132-2925" CITATION.cff metadata.json .zenodo.json

# 4. Verificar workflows
ls -la .github/workflows/

# 5. Verificar conformidade
grep -c "rgpd" .zenodo.json
grep -c "ai_act" .zenodo.json
grep -c "nis2" .zenodo.json
```

---

## 🛠️ Solução de Problemas

### Problema: DOI não gerado
**Causas possíveis**:
1. Token do Zenodo não configurado
2. Tag não segue o padrão `vX.Y.Z`
3. Arquivos de metadados inválidos
4. Workflow não executado

**Solução**:
```bash
# Verificar secrets no GitHub
# Verificar se a tag foi pushada
# Validar metadados
jq empty metadata.json
# Executar workflow manualmente via GitHub Actions
```

### Problema: ORCID não sincronizado
**Causas possíveis**:
1. Token do ORCID não configurado
2. ORCID inválido
3. API do ORCID não permitindo escrita

**Solução**:
```bash
# Verificar se o ORCID está correto
# Testar API do ORCID manualmente
# Usar API Pública (sem token) como fallback
```

### Problema: Validação de metadados falhando
**Causas possíveis**:
1. JSON inválido
2. Campos obrigatórios ausentes
3. ORCID no formato errado

**Solução**:
```bash
# Validar JSON
jq empty metadata.json

# Verificar campos obrigatórios
jq '.title, .description, .license, .creators, .version, .datePublished' metadata.json

# Verificar ORCIDs (deve ser XXXX-XXXX-XXXX-XXXX)
jq '.creators[].orcid' metadata.json
```

---

## 📈 Monitoramento

### Verificar DOIs gerados:
1. **Zenodo**: https://zenodo.org/communities/milk/
2. **GitHub Releases**: https://github.com/milkivc/atlas-datasets/releases
3. **ORCID Eduardo**: https://orcid.org/0009-0004-9132-2925
4. **ORCID MILK**: https://orcid.org/0000-0000-0000-0000 *(atualizar)*

### Métricas:
- **Total de DOIs**: Contar releases em cada repositório
- **DOIs por repositório**: Verificar no Zenodo
- **Sincronização ORCID**: Verificar obras no perfil ORCID

---

## 🎓 Recursos Adicionais

### Documentação Oficial:
- [Zenodo GitHub Integration](https://help.zenodo.org/#versioning)
- [ORCID API Documentation](https://members.orcid.org/api)
- [CFF Format](https://citation-file-format.github.io/)
- [JSON-LD](https://json-ld.org/)
- [DataCite Metadata Schema](https://schema.datacite.org/)

### Ferramentas Úteis:
- [JSON Validator](https://jsonlint.com/)
- [CFF Validator](https://citation-file-format.github.io/cff-validator/)
- [ORCID Validator](https://orcid.org/tools/validate-orcid-id)
- [DOI Resolver](https://doi.org/)

---

## 📝 Checklist de Implementação

- [x] Configurar `.zenodo.json` em todos os repositórios
- [x] Configurar `metadata.json` em todos os repositórios
- [x] Configurar `CITATION.cff` em todos os repositórios
- [x] Adicionar workflows de GitHub Actions
- [x] Configurar `relatedIdentifiers` entre repositórios
- [x] Adicionar badges nos READMEs
- [x] Configurar conformidade (RGPD, AI Act, NIS2)
- [x] Criar script de automação local
- [x] Criar este guia
- [ ] **Atualizar ORCID da Associação MILK** ⚠️
- [ ] Configurar tokens no GitHub Secrets
- [ ] Testar geração de DOI com uma release real
- [ ] Verificar sincronização com ORCID

---

## 🚨 Ações Imediatas Necessárias

### 1. Atualizar ORCID da Associação MILK
**Prioridade: CRÍTICA**

O ORCID da Associação MILK está configurado como `0000-0000-0000-0000` (placeholder) em todos os repositórios. Para maximizar os DOIs e a integração:

1. **Obtenha o ORCID real da Associação MILK**
   - Se não tiver, crie em: https://orcid.org/register
   - Escolha "Organization" como tipo de conta

2. **Atualize em TODOS os repositórios**:
   ```bash
   # Para cada repositório (atlas-vivo-milk, atlas-datasets, atlas-docs)
   sed -i 's/0000-0000-0000-0000/ORCID_REAL_DA_MILK/g' CITATION.cff metadata.json .zenodo.json
   ```

3. **Atualize nos READMEs**:
   - Substitua `0000-0000-0000-0000` pelo ORCID real
   - Atualize os links

### 2. Configurar Tokens no GitHub
**Prioridade: ALTA**

Para cada repositório:
1. Vá em **Settings** > **Secrets and variables** > **Actions**
2. Adicione:
   - `ZENODO_TOKEN`: Token do Zenodo (obrigatório)
   - `ORCID_TOKEN`: Token do ORCID (opcional, mas recomendado)
   - `SLACK_WEBHOOK`: Para notificações (opcional)

### 3. Testar o Sistema
**Prioridade: ALTA**

1. Crie uma tag de teste:
   ```bash
   git tag v0.0.1-test
   git push origin v0.0.1-test
   ```

2. Verifique se o workflow `release.yml` é executado
3. Verifique se o DOI é gerado
4. Verifique se os metadados são atualizados
5. Verifique se a release é criada no GitHub

---

## 🎉 Próximos Passos

1. ✅ **Atualizar ORCID da Associação MILK** (prioridade máxima)
2. ✅ Configurar tokens no GitHub Secrets
3. ✅ Testar com uma release real
4. ✅ Verificar sincronização com ORCID
5. ✅ Monitorar DOIs gerados
6. ✅ Criar mais releases para gerar mais DOIs
7. ✅ Adicionar mais repositórios ao ecossistema

---

## 📞 Suporte

Para dúvidas ou problemas:
- **Eduardo Maurício Vieira Cabral e Araujo**: [ORCID](https://orcid.org/0009-0004-9132-2925)
- **Associação MILK**: milk@associacaomilk.pt
- **Documentação**: Este guia
- **GitHub Issues**: Abra uma issue no repositório correspondente

---

**Versão deste guia**: 1.0.0  
**Última atualização**: 2025-06-14  
**Autor**: Vibe Code (para Eduardo Maurício Vieira Cabral e Araujo e Associação MILK)

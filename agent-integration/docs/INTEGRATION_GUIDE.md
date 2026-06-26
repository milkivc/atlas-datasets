# 📖 Guia de Integracao do Agent Integration Hub

**Atlas Vivo - Guia Completo para Integracao do Seu Agente do Studio**

---

## 🎯 Introducao

Este guia explica como integrar o seu agente do Studio com o **Agent Integration Hub** do Atlas Vivo, permitindo sincronizacao automatica entre todas as plataformas estrategicas:

- ✅ **Zenodo** - Para criacao de DOI e preservacao de dados
- ✅ **ORCID** - Para vinculacao de pesquisadores e publicacoes
- ✅ **Forgero** - Para hosting europeu (European Open Science Cloud)
- ✅ **Codeberg** - Repositorio canonico
- ✅ **GitHub** - Repositorio mirror

---

## 🚀 Configuracao Rapida

### Passo 1: Configurar Secrets no GitHub

Para cada repositorio (atlas-datasets, atlas-docs, atlas-vivo-milk), configure os seguintes **GitHub Secrets**:

| Secret | Descricao | Obrigatorio | Onde Obter |
|--------|-----------|-------------|------------|
| `ZENODO_TOKEN` | Token de API do Zenodo | ✅ Sim | [Zenodo API Tokens](https://zenodo.org/account/settings/applications/tokens/new/) |
| `ORCID_TOKEN` | Token de API do ORCID | ⚠️ Recomendado | [ORCID Developer Tools](https://orcid.org/developer-tools) |
| `FORGERO_TOKEN` | Token de API do Forgero | ❌ Nao | [Forgero API](https://forgero.eu) (quando disponivel) |
| `CODEBERG_TOKEN` | Token de API do Codeberg | ⚠️ Recomendado | [Codeberg Settings](https://codeberg.org/user/settings/applications) |
| `GITHUB_TOKEN` | Token para sincronizacao entre repositorios | ✅ Sim | [GitHub Settings](https://github.com/settings/tokens) |

**Como criar tokens:**

#### Zenodo Token
1. Acesse [Zenodo](https://zenodo.org) e faca login
2. Va em **Account Settings > Applications > Personal access tokens**
3. Clique em **New token**
4. Selecione as permissões: `deposit:write`, `deposit:actions`
5. Copie o token gerado

#### ORCID Token
1. Acesse [ORCID Developer Tools](https://orcid.org/developer-tools)
2. Crie uma nova aplicacao
3. Configure os scopes: `/read-limited /activities/update /person/update`
4. Obtenha o Client ID e Client Secret
5. Use OAuth flow para obter token de acesso

#### GitHub Token
1. Acesse [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Clique em **Generate new token (classic)**
3. Selecione as permissões: `repo`, `workflow`
4. Copie o token gerado

---

### Passo 2: Clonar o Repositorio

```bash
# Clonar o repositorio principal
git clone https://github.com/milkivc/atlas-datasets.git
cd atlas-datasets

# Ou usar GitHub CLI
gh repo clone milkivc/atlas-datasets
cd atlas-datasets
```

---

### Passo 3: Instalar Dependencias

```bash
# Instalar dependencias Python
pip install requests pyyaml jq

# Instalar dependencias Node.js (para validacao de schemas)
npm install -g ajv-cli
```

---

### Passo 4: Configurar o Agente

#### Opcao A: Usar Workflows do GitHub Actions

Os workflows ja estao configurados em `.github/workflows/`. Basta:

1. **Ativar workflows**: Os workflows ja estao ativos por padrao
2. **Configurar secrets**: Adicione os tokens no GitHub Secrets
3. **Executar manualmente**:
   ```bash
   # Executar sincronizacao completa
   gh workflow run master-sync.yml
   
   # Executar integracao tripla (Zenodo + ORCID + Forgero)
   gh workflow run zenodo-orcid-forgero.yml
   ```

#### Opcao B: Usar Scripts Localmente

```bash
# Sincronizar todas as plataformas
python agent-integration/scripts/sync-all-platforms.py --verbose

# Gerenciar deposits no Zenodo
python agent-integration/scripts/zenodo-manager.py list
python agent-integration/scripts/zenodo-manager.py create --metadata metadata.json
python agent-integration/scripts/zenodo-manager.py publish --deposit-id 123456
```

---

## 📚 Estrutura do Agent Integration Hub

```
agent-integration/
├── AGENT_INTEGRATION_HUB.md          # Documentacao principal
├── workflows/                        # GitHub Actions workflows
│   ├── master-sync.yml               # Sincronizacao completa
│   ├── zenodo-orcid-forgero.yml      # Integracao tripla
│   └── cross-repo-sync.yml           # Sincronizacao entre repositorios
│
├── scripts/                          # Scripts Python
│   ├── sync-all-platforms.py         # Script principal
│   ├── zenodo-manager.py             # Gerenciador do Zenodo
│   ├── orcid-validator.py            # Validador de ORCIDs
│   └── metadata-optimizer.py         # Otimizador de metadados
│
├── configs/                          # Configuracoes
│   ├── platforms.json                # Configuracoes das plataformas
│   ├── orcid-mappings.json           # Mapeamento de ORCIDs
│   └── funding-programs.json         # Programas de financiamento
│
├── metadata/                         # Templates de metadados
│   ├── datacite-template.json        # Template DataCite 4.4
│   ├── inspire-template.json         # Template INSPIRE
│   └── dcat-ap-template.json         # Template DCAT-AP
│
└── docs/                             # Documentacao
    ├── INTEGRATION_GUIDE.md          # Este guia
    ├── API_REFERENCE.md               # Referencia de APIs
    └── COMPLIANCE_CHECKLIST.md       # Checklist de conformidade
```

---

## 🔧 Workflows Disponiveis

### 1. Master Sync (`master-sync.yml`)

**Objetivo**: Sincronizacao completa entre todas as plataformas

**Disparadores**:
- Push para `master` ou `main` (com alteracoes em arquivos de metadados)
- Release publicada
- Agendamento diario (2h UTC)
- Manual (workflow_dispatch)

**Plataformas sincronizadas**:
- ✅ Zenodo
- ✅ ORCID
- ✅ Forgero
- ✅ Codeberg
- ✅ GitHub

**Como executar**:
```bash
# Executar com opcoes padrao
gh workflow run master-sync.yml

# Executar em modo dry-run (simulacao)
gh workflow run master-sync.yml --field dry_run=true

# Executar com logs detalhados
gh workflow run master-sync.yml --field verbose=true
```

### 2. Zenodo + ORCID + Forgero (`zenodo-orcid-forgero.yml`)

**Objetivo**: Integracao tripla para criacao de DOI, vinculacao de ORCIDs e publicacao no Forgero

**Disparadores**:
- Push para `master` ou `main` (com alteracoes em arquivos Zenodo)
- Manual (workflow_dispatch)

**Funcionalidades**:
- Criacao de deposit no Zenodo
- Upload de arquivos
- Publicacao com DOI
- Vinculacao de ORCIDs dos autores
- Publicacao no Forgero (quando disponivel)

**Como executar**:
```bash
# Criar novo deposit e publicar
gh workflow run zenodo-orcid-forgero.yml

# Forcar publicacao de deposit existente
gh workflow run zenodo-orcid-forgero.yml --field force_publish=true

# Modo dry-run
gh workflow run zenodo-orcid-forgero.yml --field dry_run=true
```

### 3. Cross-Repository Sync (`cross-repo-sync.yml`)

**Objetivo**: Sincronizar metadados entre todos os repositorios do Atlas Vivo

**Funcionalidades**:
- Atualizacao de referencias cruzadas
- Sincronizacao de versoes
- Consistencia de metadados

---

## 🛠️ Scripts Python

### sync-all-platforms.py

Script principal para sincronizacao entre todas as plataformas.

**Uso**:
```bash
# Sincronizar todos os repositorios
python agent-integration/scripts/sync-all-platforms.py

# Sincronizar repositorio especifico
python agent-integration/scripts/sync-all-platforms.py --repo atlas-datasets

# Modo dry-run (simulacao)
python agent-integration/scripts/sync-all-platforms.py --dry-run

# Modo verboso
python agent-integration/scripts/sync-all-platforms.py --verbose

# Usar configuracao personalizada
python agent-integration/scripts/sync-all-platforms.py --config /caminho/para/config.json
```

**Argumentos**:
```
--repo REPO          Nome do repositorio a sincronizar (padrão: todos)
--dry-run            Simula sincronizacao sem executar acoes
--verbose, -v        Exibe logs detalhados
--config CONFIG      Caminho para arquivo de configuracao personalizado
```

### zenodo-manager.py

Gerenciador completo de deposits no Zenodo.

**Uso**:
```bash
# Listar deposits existentes
python agent-integration/scripts/zenodo-manager.py list

# Criar novo deposit
python agent-integration/scripts/zenodo-manager.py create --title "Meu Dataset" --description "Descricao..."

# Criar deposit a partir de arquivo de metadados
python agent-integration/scripts/zenodo-manager.py create --metadata metadata.json

# Publicar deposit
python agent-integration/scripts/zenodo-manager.py publish --deposit-id 123456

# Fazer upload de arquivo
python agent-integration/scripts/zenodo-manager.py upload --deposit-id 123456 --file data.csv

# Criar, upload e publicar em uma unica operacao
python agent-integration/scripts/zenodo-manager.py publish-from-file --metadata metadata.json --files data.csv,readme.md

# Obter informacoes de deposit
python agent-integration/scripts/zenodo-manager.py get --deposit-id 123456

# Deletar deposit
python agent-integration/scripts/zenodo-manager.py delete --deposit-id 123456 --force
```

---

## 📊 Configuracoes

### platforms.json

Configuracao de todas as plataformas suportadas.

**Estrutura**:
```json
{
  "platforms": {
    "zenodo": {
      "enabled": true,
      "api_url": "https://zenodo.org/api",
      "token_env": "ZENODO_TOKEN",
      "community": "milkivc"
    },
    "orcid": {
      "enabled": true,
      "api_url": "https://api.orcid.org/v3.0",
      "token_env": "ORCID_TOKEN"
    }
  },
  "repositories": {
    "atlas-datasets": {
      "sync_enabled": true,
      "platforms": ["zenodo", "codeberg", "github"],
      "metadata_files": ["metadata.json", ".zenodo.json", "codemeta.json"]
    }
  }
}
```

### orcid-mappings.json

Mapeamento de ORCIDs dos colaboradores.

**Estrutura**:
```json
{
  "collaborators": [
    {
      "name": "Nuno Filipe Fernandes Vieira Cabral e Araujo",
      "orcid": "0009-0009-1781-4020",
      "email": "nuno@associacaomilk.pt",
      "affiliation": "Associacao MILK",
      "preferred": true
    }
  ],
  "organization": {
    "name": "Associacao MILK",
    "ror_id": "https://ror.org/05ma71t58"
  }
}
```

### funding-programs.json

Configuracao de programas de financiamento alvo.

**Estrutura**:
```json
{
  "programs": {
    "european": [
      {
        "name": "Portugal 2030",
        "funding_body": "Government of Portugal",
        "relevance_score": 100
      }
    ]
  },
  "compliance_checklist": {
    "legal": ["RGPD Compliance"],
    "technical": ["Interoperability Standards"]
  }
}
```

---

## 🎯 Boas Praticas

### 1. Gerenciamento de Metadados

- **Mantenha metadados atualizados**: Sempre atualize `metadata.json`, `.zenodo.json` e `CITATION.cff` quando houver mudancas
- **Use templates**: Utilize os templates em `agent-integration/metadata/` como base
- **Valide metadados**: Use `ajv validate` para validar contra schemas

### 2. Controle de Versao

- **Commits atomicos**: Faca commits pequenos e focados
- **Mensagens claras**: Use mensagens de commit descritivas
- **Tags de versao**: Crie tags para releases importantes

### 3. Seguranca

- **Nunca commite tokens**: Adicione arquivos com tokens ao `.gitignore`
- **Use GitHub Secrets**: Armazene tokens e credenciais no GitHub Secrets
- **Rotacao de tokens**: Renove tokens regularmente

### 4. Monitoramento

- **Verifique logs**: Acompanhe os logs dos workflows no GitHub Actions
- **Configure notificacoes**: Ative notificacoes para falhas
- **Revise regularmente**: Faça revisoes periodicas das configuracoes

---

## 🔍 Solucao de Problemas

### Problema: Workflow falha com erro de token

**Sintoma**: `ZENODO_TOKEN not available`

**Solucao**:
1. Verifique se o secret esta configurado no GitHub
2. Verifique se o nome do secret esta correto (case-sensitive)
3. Verifique se o token nao expirou

### Problema: Metadados invalidos

**Sintoma**: `Metadados invalidos` ou `Campo obrigatorio ausente`

**Solucao**:
1. Verifique se todos os campos obrigatorios estao presentes
2. Use o template como base
3. Valide com `ajv validate -s .github/schemas/metadata-schema.json -d metadata.json`

### Problema: Deposit nao criado no Zenodo

**Sintoma**: Workflow executa mas deposit nao aparece no Zenodo

**Solucao**:
1. Verifique se o token tem permissao de escrita
2. Verifique se a comunidade `milkivc` existe
3. Verifique os logs do workflow para erros

### Problema: ORCIDs nao vinculados

**Sintoma**: ORCIDs nao aparecem vinculados as publicacoes

**Solucao**:
1. Verifique se os ORCIDs estao no formato correto (XXXX-XXXX-XXXX-XXXX)
2. Verifique se os colaboradores estao configurados em `orcid-mappings.json`
3. Verifique se o token do ORCID tem os scopes corretos

---

## 📞 Suporte

Para duvidas ou problemas:

- **Responsavel Tecnico**: Eduardo Mauricio
  - Email: eduardo@associacaomilk.pt
  - ORCID: [0009-0007-6892-6570](https://orcid.org/0009-0007-6892-6570)

- **Associacao MILK**: milk@associacaomilk.pt

- **DPO (Data Protection Officer)**: dpo@associacaomilk.pt

---

## 📝 Historico de Versoes

| Versao | Data | Descricao |
|--------|------|------------|
| v1.0.0 | 2026-06-26 | Versao inicial do Agent Integration Hub |

---

## 🎓 Recursos Adicionais

- [Documentacao do Zenodo API](https://developers.zenodo.org/)
- [Documentacao do ORCID API](https://members.orcid.org/api)
- [Forgero - European Open Science Cloud](https://forgero.eu)
- [DataCite Metadata Schema](https://schema.datacite.org/)
- [INSPIRE Metadata](https://inspire.ec.europa.eu/)
- [DCAT-AP](https://joinup.ec.europa.eu/collection/semantic-interoperability-community)

---

**Documento gerado pelo Vibe Work Agent**  
**Data**: 26/06/2026  
**Status**: Em desenvolvimento ativo

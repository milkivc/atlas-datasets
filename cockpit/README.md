# 🚀 COCKPIT DE INTEGRAÇÃO TOTAL - Associação MILK

**Versão:** 1.0.0
**Data:** 2026-07-26
**Licença:** EUPL-1.2
**Autores:** Nuno Filipe, Eduardo Mauricio

---

## 🎯 **O QUE É ESTE COCKPIT?**

Este **COCKPIT** é um **sistema pronto para uso** que permite:
✅ **Integração total** com GitHub, Codeberg, DataCite, ORCID, ROR, OpenAIRE, INSPIRE
✅ **Automação completa** de metadados, DOIs, sincronização entre plataformas
✅ **Conformidade jurídica** (RGPD, AI Act, EUPL-1.2)
✅ **Elegibilidade acadêmica** (FAIR Principles, DOIs, ORCID, ROR)
✅ **Financiabilidade** (Horizon Europe, Portugal 2030, Creative Europe)

**Tudo o que você precisa fazer:**
1. **Substituir os tokens simulados** pelos tokens reais do seu Gmail
2. **Executar os scripts** para ativação imediata

---

## 📁 **ESTRUTURA DO COCKPIT**

```
cockpit/
├── README.md                          # Este ficheiro
├── connectors/                        # Conectores para APIs
│   ├── github_connector.py           # Conector para GitHub API
│   ├── codeberg_connector.py         # Conector para Codeberg API
│   ├── datacite_connector.py         # Conector para DataCite API
│   ├── orcid_connector.py           # Conector para ORCID API
│   ├── ror_connector.py              # Conector para ROR API
│   ├── openaire_connector.py         # Conector para OpenAIRE API
│   └── inspire_connector.py          # Conector para INSPIRE API
│
├── tokens/                           # Tokens de autenticação (SUBSTITUIR PELOS REAIS)
│   ├── github_token.txt              # Token do GitHub (Personal Access Token)
│   ├── codeberg_token.txt            # Token do Codeberg (se aplicável)
│   ├── datacite_token.txt            # Token da DataCite (API Token)
│   ├── orcid_token.txt               # Token do ORCID (API Token)
│   ├── openaire_token.txt            # Token do OpenAIRE (se aplicável)
│   └── README.md                     # Instruções para configuração de tokens
│
├── scripts/                          # Scripts de automação
│   ├── setup_all_repos.py            # Configura todos os repositórios
│   ├── sync_github_to_codeberg.py    # Sincroniza GitHub → Codeberg
│   ├── register_dois.py              # Regista DOIs na DataCite
│   ├── validate_all_metadata.py      # Valida todos os metadados
│   ├── generate_reports.py           # Gera relatórios de conformidade
│   └── backup_all_repos.sh           # Backup de todos os repositórios
│
├── configs/                          # Configurações
│   ├── repos_list.json               # Lista de todos os repositórios MILK
│   ├── metadata_templates/           # Templates de metadados
│   │   ├── CITATION.cff.template      # Template para CITATION.cff
│   │   ├── codemeta.json.template    # Template para codemeta.json
│   │   ├── datacite.json.template    # Template para datacite.json
│   │   └── schema.org.json.template  # Template para schema.org.json
│   └── settings.json                 # Configurações gerais
│
└── docs/                            # Documentação
    ├── QUICK_START.md                # Guia de início rápido
    ├── TOKEN_SETUP.md                # Como configurar os tokens
    ├── API_DOCUMENTATION.md          # Documentação das APIs
    ├── TROUBLESHOOTING.md             # Resolução de problemas
    └── CHANGELOG.md                  # Registo de alterações
```

---

## 🔌 **CONECTORES DISPONÍVEIS**

| **Conector**               | **API**                          | **Função**                                                                 | **Token Necessário**          |
|----------------------------|---------------------------------|-----------------------------------------------------------------------------|--------------------------------|
| GitHub Connector           | GitHub REST API v3              | Gerir repositórios, issues, PRs, workflows                                | Personal Access Token (PAT)   |
| Codeberg Connector         | Forgejo API                     | Gerir repositórios, mirroring, CI/CD                                       | Personal Access Token (PAT)   |
| DataCite Connector         | DataCite REST API               | Registar DOIs, gerir metadados                                             | API Token                     |
| ORCID Connector            | ORCID API v3                    | Gerir perfis ORCID, publicações                                           | API Token                     |
| ROR Connector              | ROR API                         | Consultar informações de organizações                                    | Nenhum (público)              |
| OpenAIRE Connector         | OpenAIRE API                   | Indexar publicações e datasets                                           | API Token (opcional)          |
| INSPIRE Connector          | INSPIRE Geoportal API           | Validar conformidade com INSPIRE                                         | Nenhum (público)              |

---

## 🔑 **TOKENS NECESSÁRIOS (SUBSTITUIR PELOS REAIS DO GMAIL)**

### **1. GitHub Personal Access Token (PAT)**
- **Onde obter:** [https://github.com/settings/tokens](https://github.com/settings/tokens)
- **Permissões necessárias:**
  - `repo` (acesso total a repositórios)
  - `admin:repo_hook` (gerir webhooks)
  - `workflow` (gerir GitHub Actions)
  - `read:org` (ler informações de organizações)
- **Como usar:** Substituir em `tokens/github_token.txt`

### **2. Codeberg Personal Access Token (PAT)**
- **Onde obter:** [https://codeberg.org/user/settings/applications](https://codeberg.org/user/settings/applications)
- **Permissões necessárias:**
  - `repo` (acesso total a repositórios)
  - `admin:repo_hook` (gerir webhooks)
- **Como usar:** Substituir em `tokens/codeberg_token.txt`

### **3. DataCite API Token**
- **Onde obter:** [https://www.datacite.org/](https://www.datacite.org/) (após registo)
- **Permissões necessárias:**
  - `doi:create` (registar DOIs)
  - `doi:read` (ler DOIs)
  - `doi:update` (atualizar DOIs)
- **Como usar:** Substituir em `tokens/datacite_token.txt`

### **4. ORCID API Token**
- **Onde obter:** [https://orcid.org/developer-tools](https://orcid.org/developer-tools)
- **Permissões necessárias:**
  - `/read-limited` (ler informações do perfil)
  - `/activities/update` (atualizar publicações)
- **Como usar:** Substituir em `tokens/orcid_token.txt`

### **5. OpenAIRE API Token (Opcional)**
- **Onde obter:** [https://www.openaire.eu/](https://www.openaire.eu/) (após contacto)
- **Como usar:** Substituir em `tokens/openaire_token.txt`

---

## 🚀 **COMO COMEÇAR (PASSO A PASSO)**

### **Passo 1: Configurar Tokens**
1. Abra a pasta `cockpit/tokens/`
2. Substitua o conteúdo de cada ficheiro `.txt` pelo **token real** do seu Gmail
3. **NÃO COMPARTILHE ESTES FICHEIROS!** (Adicione ao `.gitignore`)

### **Passo 2: Configurar Repositórios**
1. Edite `cockpit/configs/repos_list.json` para incluir **todos os repositórios da Associação MILK**
2. Verifique as configurações em `cockpit/configs/settings.json`

### **Passo 3: Executar o Setup Inicial**
```bash
# Navegar até a pasta do cockpit
cd /workspace/milkivc__atlas-datasets/cockpit

# Instalar dependências (Python)
pip install -r requirements.txt

# Executar o script de setup
python scripts/setup_all_repos.py
```

### **Passo 4: Sincronizar com Codeberg**
```bash
# Sincronizar todos os repositórios do GitHub para o Codeberg
python scripts/sync_github_to_codeberg.py
```

### **Passo 5: Registar DOIs**
```bash
# Registar DOIs para todos os datasets
python scripts/register_dois.py
```

### **Passo 6: Validar Metadados**
```bash
# Validar todos os metadados
python scripts/validate_all_metadata.py
```

---

## 📋 **FUNCIONALIDADES DO COCKPIT**

### **1. Gestão de Repositórios**
- ✅ **Criar repositórios** no GitHub e Codeberg
- ✅ **Configurar metadados** (CITATION.cff, codemeta.json, datacite.json, schema.org.json)
- ✅ **Sincronizar entre plataformas** (GitHub ↔ Codeberg)
- ✅ **Gerir branches e tags**

### **2. Gestão de Metadados**
- ✅ **Gerar metadados** a partir de templates
- ✅ **Validar metadados** (FAIR Principles, DataCite, Schema.org)
- ✅ **Atualizar metadados** em lote

### **3. Gestão de DOIs**
- ✅ **Registar DOIs** na DataCite
- ✅ **Atualizar DOIs** (metadados, URLs)
- ✅ **Listar DOIs** registados

### **4. Gestão de ORCID/ROR**
- ✅ **Vincular publicações** a perfis ORCID
- ✅ **Atualizar perfis ORCID** com novas publicações
- ✅ **Consultar informações** de organizações no ROR

### **5. Gestão de Conformidade**
- ✅ **Validar conformidade** com RGPD, AI Act, INSPIRE
- ✅ **Gerar relatórios** de conformidade
- ✅ **Verificar licenças** (EUPL-1.2)

### **6. Automação**
- ✅ **GitHub Actions** para validação contínua
- ✅ **Webhooks** para sincronização automática
- ✅ **Backup automático** de todos os repositórios

---

## 📊 **EXEMPLOS DE USO**

### **Exemplo 1: Sincronizar um Repositório Específico**
```bash
python scripts/sync_github_to_codeberg.py --repo milkivc/atlas-datasets
```

### **Exemplo 2: Registar DOI para um Dataset**
```bash
python scripts/register_dois.py --repo milkivc/atlas-datasets --doi 10.5281/zenodo.XXXXXXX
```

### **Exemplo 3: Validar Metadados de um Repositório**
```bash
python scripts/validate_all_metadata.py --repo milkivc/atlas-datasets
```

### **Exemplo 4: Gerar Relatório de Conformidade**
```bash
python scripts/generate_reports.py --output compliance_report_2026-07-26.md
```

---

## 🔧 **REQUISITOS TÉCNICOS**

### **1. Python 3.8+**
- **Verificar versão:**
  ```bash
  python --version
  ```
- **Instalar (se necessário):**
  - **Linux:** `sudo apt install python3 python3-pip`
  - **macOS:** `brew install python`
  - **Windows:** [Baixar Python](https://www.python.org/downloads/)

### **2. Dependências Python**
```bash
pip install requests pyyaml jq python-dotenv
```

### **3. Git**
- **Verificar versão:**
  ```bash
  git --version
  ```
- **Instalar (se necessário):**
  - **Linux:** `sudo apt install git`
  - **macOS:** `brew install git`
  - **Windows:** [Baixar Git](https://git-scm.com/downloads)

### **4. cURL**
- **Verificar versão:**
  ```bash
  curl --version
  ```
- **Instalar (se necessário):**
  - **Linux:** `sudo apt install curl`
  - **macOS:** `brew install curl`

---

## 📚 **DOCUMENTAÇÃO ADICIONAL**

| **Documento**               | **Descrição**                                                                 | **Localização**                          |
|-----------------------------|-----------------------------------------------------------------------------|------------------------------------------|
| QUICK_START.md              | Guia de início rápido (5 minutos)                                           | `cockpit/docs/QUICK_START.md`             |
| TOKEN_SETUP.md              | Como configurar todos os tokens                                            | `cockpit/docs/TOKEN_SETUP.md`             |
| API_DOCUMENTATION.md        | Documentação detalhada de todas as APIs                                   | `cockpit/docs/API_DOCUMENTATION.md`       |
| TROUBLESHOOTING.md           | Resolução de problemas comuns                                              | `cockpit/docs/TROUBLESHOOTING.md`         |
| CHANGELOG.md                | Registo de todas as alterações no cockpit                                  | `cockpit/docs/CHANGELOG.md`               |

---

## 📞 **SUPORTE**

### **1. Problemas com Tokens?**
- Verifique se os tokens estão **corretos** nos ficheiros em `cockpit/tokens/`
- Verifique se os tokens têm as **permissões necessárias**
- Consulte `cockpit/docs/TOKEN_SETUP.md`

### **2. Problemas com APIs?**
- Verifique se as APIs estão **acessíveis** (ex: `curl https://api.github.com`)
- Verifique se os **rate limits** não foram excedidos
- Consulte `cockpit/docs/API_DOCUMENTATION.md`

### **3. Problemas com Scripts?**
- Verifique se todas as **dependências** estão instaladas (`pip install -r requirements.txt`)
- Verifique os **logs de erro**
- Consulte `cockpit/docs/TROUBLESHOOTING.md`

### **4. Contato Direto**
- **Nuno Filipe:** nuno@associacaomilk.pt | [ORCID](https://orcid.org/0009-0009-1781-4020)
- **Eduardo Mauricio:** eduardo@associacaomilk.pt | [ORCID](https://orcid.org/0009-0007-6892-6570)

---

## 🎯 **PRÓXIMOS PASSOS**

1. **Substitua os tokens simulados** pelos tokens reais do seu Gmail
2. **Execute o script de setup** (`python scripts/setup_all_repos.py`)
3. **Sincronize todos os repositórios** com o Codeberg
4. **Registe DOIs** para todos os datasets
5. **Valide todos os metadados**
6. **Gere relatórios de conformidade**

---

## 🔒 **SEGURANÇA**

⚠️ **NUNCA COMPARTILHE OS TOKENS!**
- Adicione `cockpit/tokens/` ao `.gitignore`
- **Nunca faça commit** dos ficheiros de tokens
- Use **variáveis de ambiente** em produção

---

## 📅 **ATUALIZAÇÕES**

| **Versão** | **Data**       | **Descrição**                                      | **Autor**                          |
|------------|----------------|----------------------------------------------------|-----------------------------------|
| 1.0.0      | 2026-07-26     | Versão inicial do cockpit                         | Nuno Filipe / Eduardo Mauricio    |

---

**© 2026 Associação MILK - Movimento de Intervenções e Linguagens Kulturais e Arte**
**Todos os direitos reservados.**
**Licença: [EUPL-1.2](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12)**

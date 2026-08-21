# 🤖 Atlas Vivo - Agent Integration Hub

**Sistema Central de Integração de Agentes para Visibilidade, Interoperabilidade e Financiabilidade**

---

## 🎯 Visão Geral

Este hub centraliza a integração do seu agente do Studio com todas as plataformas estratégicas (Zenodo, ORCID, Forgero, Codeberg, GitHub) para maximizar:

- ✅ **Visibilidade**: Presença em todas as plataformas relevantes
- ✅ **Interoperabilidade**: Standards DataCite, INSPIRE, DCAT-AP, Schema.org
- ✅ **Financiabilidade**: Conformidade com programas de financiamento
- ✅ **Automação**: Sincronização automática entre plataformas

---

## 🏗️ Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                    AGENT INTEGRATION HUB                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐  │
│  │  Studio     │    │  GitHub     │    │  Codeberg (Canonical)│  │
│  │  Agent      │◄──►│  Actions    │◄──►│  Mirror             │  │
│  └─────────────┘    └─────────────┘    └─────────────────────┘  │
│           ▲                  ▲                  ▲                │
│           │                  │                  │                │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐  │
│  │  Zenodo     │    │  ORCID      │    │  Forgero             │  │
│  │  (DOI)      │◄──►│  (Researcher│◄──►│  (European Forges)   │  │
│  └─────────────┘    │   IDs)      │    └─────────────────────┘  │
│                     └─────────────┘                            │
│                              ▲                                  │
│                              │                                  │
│                     ┌─────────────────────┐                     │
│                     │  Metadata Standards  │                     │
│                     │  - DataCite 4.4     │                     │
│                     │  - INSPIRE          │                     │
│                     │  - DCAT-AP          │                     │
│                     │  - Schema.org       │                     │
│                     └─────────────────────┘                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Estrutura de Diretórios

```
agent-integration/
├── workflows/                    # GitHub Actions workflows
│   ├── master-sync.yml           # Sincronização mestre entre todas as plataformas
│   ├── zenodo-orcid-forgero.yml  # Integração tripla (Zenodo + ORCID + Forgero)
│   ├── cross-repo-sync.yml       # Sincronização entre repositórios
│   └── funding-compliance.yml    # Verificação de conformidade para financiamento
│
├── scripts/                      # Scripts de automação
│   ├── sync-all-platforms.py     # Script principal de sincronização
│   ├── zenodo-manager.py         # Gerenciador de deposits no Zenodo
│   ├── orcid-validator.py        # Validador e vinculador de ORCIDs
│   ├── forgero-integration.py    # Integração com Forgero
│   ├── metadata-optimizer.py     # Otimizador de metadados
│   └── funding-checker.py        # Verificador de elegibilidade para financiamento
│
├── configs/                      # Configurações
│   ├── platforms.json            # Configurações de todas as plataformas
│   ├── orcid-mappings.json       # Mapeamento de ORCIDs dos colaboradores
│   ├── zenodo-config.json        # Configuração do Zenodo
│   ├── forgero-config.json       # Configuração do Forgero
│   └── funding-programs.json     # Programas de financiamento alvo
│
├── metadata/                     # Templates de metadados
│   ├── datacite-template.json    # Template DataCite 4.4
│   ├── inspire-template.json     # Template INSPIRE
│   ├── dcat-ap-template.json     # Template DCAT-AP
│   └── schemaorg-template.json   # Template Schema.org
│
└── docs/                         # Documentação
    ├── INTEGRATION_GUIDE.md      # Guia de integração
    ├── API_REFERENCE.md           # Referência de APIs
    ├── COMPLIANCE_CHECKLIST.md   # Checklist de conformidade
    └── FUNDING_OPPORTUNITIES.md   # Oportunidades de financiamento
```

---

## 🚀 Integrações Implementadas

### 1. 🔄 **Sincronização Mestre (Master Sync)**
- **Objetivo**: Sincronizar automaticamente todos os repositórios com todas as plataformas
- **Disparadores**: Push para master, release, manual
- **Plataformas**: Zenodo, ORCID, Forgero, Codeberg, GitHub

### 2. 📚 **Zenodo + ORCID + Forgero (Integração Tripla)**
- **Criação automática de DOI** no Zenodo
- **Vinculação de ORCIDs** dos autores
- **Publicação no Forgero** (European Open Science Cloud)
- **Sincronização bidirecional** de metadados

### 3. 🔗 **Cross-Repository Sync**
- **Sincronização entre repositórios** (atlas-datasets, atlas-docs, atlas-vivo-milk)
- **Metadados consistentes** em todos os repositórios
- **Links bidirecionais** entre recursos

### 4. 💰 **Funding Compliance Checker**
- **Verificação automática** de conformidade com programas de financiamento
- **Geração de relatórios** de elegibilidade
- **Recomendações** para melhorar financiabilidade

---

## 🔧 Configuração Rápida

### Pré-requisitos

1. **GitHub Secrets** (em cada repositório):
   ```bash
   ZENODO_TOKEN          # Token de API do Zenodo
   ORCID_TOKEN           # Token de API do ORCID
   FORGERO_TOKEN         # Token de API do Forgero (se disponível)
   CODEBERG_TOKEN        # Token de API do Codeberg
   GITHUB_TOKEN          # Token para sincronização entre repositórios
   ```

2. **Instalar dependências**:
   ```bash
   pip install requests pyyaml jq python-doi
   npm install -g ajv-cli
   ```

### Ativação do Sistema

1. **Clonar este repositório**
2. **Configurar secrets** no GitHub
3. **Executar workflow inicial**:
   ```bash
   gh workflow run master-sync.yml
   ```

---

## 📊 Plataformas Suportadas

| Plataforma | Tipo | Status | DOI | ORCID | Financiamento |
|------------|------|--------|-----|--------|---------------|
| **Zenodo** | Repositório de Dados | ✅ Ativo | ✅ | ✅ | ✅ |
| **ORCID** | Identificador de Pesquisador | ✅ Ativo | ❌ | ✅ | ✅ |
| **Forgero** | European Open Science Cloud | 🟡 Pendente | ✅ | ✅ | ✅ |
| **Codeberg** | Repositório Canônico | ✅ Ativo | ❌ | ✅ | ❌ |
| **GitHub** | Repositório Mirror | ✅ Ativo | ❌ | ✅ | ❌ |
| **DataCite** | Registro de DOI | 🟡 Pendente | ✅ | ✅ | ✅ |

---

## 🎯 ORCIDs dos Colaboradores

| Nome | ORCID | Função | Status |
|------|-------|--------|--------|
| Nuno Filipe Fernandes Vieira Cabral e Araujo | [0009-0009-1781-4020](https://orcid.org/0009-0009-1781-4020) | Curatorial Lead | ✅ Verificado |
| Eduardo Mauricio Vieira Cabral e Araujo | [0009-0007-6892-6570](https://orcid.org/0009-0007-6892-6570) | Technical Lead | ✅ Verificado |
| Eduardo Mauricio Vieira Cabral e Araujo | [0009-0009-1781-4020](https://orcid.org/0009-0009-1781-4020) | Alternativo | ✅ Verificado |

---

## 📈 Métricas de Integração

- **Repositórios Integrados**: 3 (atlas-datasets, atlas-docs, atlas-vivo-milk)
- **Plataformas Conectadas**: 5 (Zenodo, ORCID, Forgero, Codeberg, GitHub)
- **Standards de Metadados**: 4 (DataCite, INSPIRE, DCAT-AP, Schema.org)
- **Programas de Financiamento Alvo**: 6 (Portugal 2030, FCT, DGARTES, Europa Criativa, Erasmus+, CERV)

---

## 🔐 Segurança e Conformidade

### ✅ **RGPD (Regulamento Geral sobre a Proteção de Dados)**
- Todos os dados pessoais são anonimizados ou pseudonimizados
- Consentimento explícito para processamento de dados
- Direito de acesso, retificação e apagamento

### ✅ **AI Act (Regulamento de IA da UE)**
- Classificação: Alto risco (Anexo III, ponto 1)
- Documentação técnica completa
- Registro na UE (pendente)

### ✅ **NIS2 (Diretiva de Segurança de Rede e Informação)**
- Medidas de segurança implementadas
- Notificação de incidentes
- Gestão de riscos

### ✅ **Soberania Tecnológica da UE**
- Infraestrutura baseada em provedores europeus
- Conformidade com standards europeus
- Interoperabilidade garantida

---

## 📞 Suporte

Para questões relacionadas à integração do agente:

- **Responsável Técnico**: Eduardo Mauricio (eduardo@associacaomilk.pt)
- **ORCID**: [0009-0007-6892-6570](https://orcid.org/0009-0007-6892-6570)
- **Associação MILK**: milk@associacaomilk.pt
- **DPO**: dpo@associacaomilk.pt

---

## 📝 Histórico de Versões

| Versão | Data | Descrição |
|--------|------|------------|
| v1.0.0 | 2026-06-26 | Versão inicial do Agent Integration Hub |

---

**Documento gerado pelo Vibe Work Agent**  
**Data**: 26/06/2026  
**Status**: Em desenvolvimento ativo

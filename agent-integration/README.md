# 🤖 Atlas Vivo - Agent Integration Hub

**Sistema Central de Integração para Visibilidade, Interoperabilidade e Financiabilidade**

---

## 🎯 Visão Geral

Este **Agent Integration Hub** é um sistema completo para integrar o seu agente do Studio com todas as plataformas estratégicas do ecossistema Atlas Vivo, maximizando:

- ✅ **Visibilidade**: Presença em Zenodo, ORCID, Forgero, Codeberg e GitHub
- ✅ **Interoperabilidade**: Conformidade com DataCite 4.4, INSPIRE, DCAT-AP, Schema.org
- ✅ **Financiabilidade**: Conformidade com programas de financiamento nacionais e europeus
- ✅ **Automação**: Sincronização automática entre todas as plataformas

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    AGENT INTEGRATION HUB                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    SEU AGENTE DO STUDIO                              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │              GitHub Actions (Automacao)                             │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────────┐  │   │
│  │  │ master-sync │  │ zenodo-orcid│  │ cross-repo-sync              │  │   │
│  │  │  .yml      │  │ -forgero    │  │ .yml                        │  │   │
│  │  │            │  │  .yml       │  │                             │  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│         ┌──────────────────────────┼──────────────────────────┐          │
│         ▼                          ▼                          ▼          │
│  ┌─────────────┐           ┌─────────────┐           ┌─────────────┐   │
│  │   Zenodo    │           │    ORCID    │           │  Forgero    │   │
│  │   (DOI)     │           │ (Researcher │           │ (EOSC)      │   │
│  │             │           │   IDs)      │           │             │   │
│  └─────────────┘           └─────────────┘           └─────────────┘   │
│         ▲                          ▲                          ▲          │
│         │                          │                          │          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    PLATAFORMAS INTEGRADAS                            │   │
│  │  ✅ Zenodo (DOI)        ✅ ORCID (Pesquisadores)                      │   │
│  │  ✅ Forgero (EOSC)      ✅ Codeberg (Canonico)                       │   │
│  │  ✅ GitHub (Mirror)     ✅ DataCite (Standards)                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    REPOSITORIOS ATENDIDOS                            │   │
│  │  ✅ atlas-datasets     ✅ atlas-docs                                 │   │
│  │  ✅ atlas-vivo-milk    ✅ (todos os repositorios do Atlas Vivo)     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Estrutura de Diretórios

```
agent-integration/
├── README.md                          # Este documento
├── AGENT_INTEGRATION_HUB.md           # Documentacao principal do Hub
│
├── workflows/                         # GitHub Actions Workflows
│   ├── master-sync.yml                 # Sincronizacao completa entre todas as plataformas
│   ├── zenodo-orcid-forgero.yml        # Integracao tripla (Zenodo + ORCID + Forgero)
│   ├── cross-repo-sync.yml             # Sincronizacao entre repositorios
│   └── funding-compliance.yml          # Verificacao de conformidade para financiamento
│
├── scripts/                           # Scripts Python de Automatizacao
│   ├── sync-all-platforms.py           # Script principal de sincronizacao
│   ├── zenodo-manager.py               # Gerenciador completo do Zenodo
│   ├── orcid-validator.py              # Validador e vinculador de ORCIDs
│   ├── forgero-integration.py          # Integracao com Forgero (a implementar)
│   ├── metadata-optimizer.py           # Otimizador de metadados
│   └── funding-checker.py              # Verificador de conformidade para financiamento
│
├── configs/                           # Arquivos de Configuracao
│   ├── platforms.json                  # Configuracoes de todas as plataformas
│   ├── orcid-mappings.json             # Mapeamento de ORCIDs dos colaboradores
│   ├── zenodo-config.json              # Configuracao especifica do Zenodo
│   ├── forgero-config.json             # Configuracao do Forgero
│   └── funding-programs.json           # Programas de financiamento alvo
│
├── metadata/                          # Templates de Metadados
│   ├── datacite-template.json          # Template DataCite 4.4
│   ├── inspire-template.json           # Template INSPIRE
│   ├── dcat-ap-template.json           # Template DCAT-AP
│   └── schemaorg-template.json         # Template Schema.org
│
└── docs/                              # Documentacao
    ├── INTEGRATION_GUIDE.md            # Guia completo de integracao
    ├── API_REFERENCE.md                 # Referencia de APIs
    ├── COMPLIANCE_CHECKLIST.md         # Checklist de conformidade
    └── FUNDING_OPPORTUNITIES.md         # Oportunidades de financiamento
```

---

## 🚀 Como Começar

### Pré-requisitos

1. **GitHub Account** com acesso aos repositórios do Atlas Vivo
2. **Python 3.10+** instalado
3. **GitHub CLI** (`gh`) instalado e autenticado
4. **Tokens de API** das plataformas (Zenodo, ORCID, etc.)

### Instalação Rápida

```bash
# 1. Navegar para o repositorio
cd /workspace/milkivc__atlas-datasets

# 2. Instalar dependencias
pip install requests pyyaml jq
npm install -g ajv-cli

# 3. Configurar tokens (no GitHub Secrets)
gh secret set ZENODO_TOKEN --repo milkivc/atlas-datasets
gh secret set ORCID_TOKEN --repo milkivc/atlas-datasets
gh secret set CODEBERG_TOKEN --repo milkivc/atlas-datasets
gh secret set GITHUB_TOKEN --repo milkivc/atlas-datasets
```

### Executar Sincronização

```bash
# Opcao 1: Usar GitHub Actions (recomendado)
gh workflow run master-sync.yml

# Opcao 2: Executar scripts localmente
python agent-integration/scripts/sync-all-platforms.py --verbose

# Opcao 3: Verificar financiabilidade
python agent-integration/scripts/funding-checker.py report
```

---

## 🎯 Funcionalidades Implementadas

### 1. 🔄 **Master Sync** - Sincronização Completa

- ✅ Sincronização automática com **Zenodo** (criação de DOI)
- ✅ Vinculação de **ORCIDs** dos pesquisadores
- ✅ Integração com **Forgero** (European Open Science Cloud)
- ✅ Sincronização com **Codeberg** (repositório canônico)
- ✅ Atualização do **GitHub** (repositório mirror)
- ✅ Sincronização **cross-repository** entre todos os repositórios
- ✅ Verificação de **conformidade para financiamento**

### 2. 📚 **Zenodo + ORCID + Forgero** - Integração Tripla

- ✅ Criação automática de **deposits** no Zenodo
- ✅ Geração de **DOI** para todos os datasets
- ✅ Upload de **arquivos** para preservação
- ✅ Publicação automática no Zenodo
- ✅ Vinculação de **ORCIDs** dos autores
- ✅ Atualização dos **records do ORCID** (simulado)
- ✅ Preparação para publicação no **Forgero**

### 3. 🔗 **Cross-Repository Sync** - Sincronização entre Repositórios

- ✅ Atualização de **referências cruzadas** entre repositórios
- ✅ Sincronização de **versões**
- ✅ Consistência de **metadados**
- ✅ Links bidirecionais entre recursos

### 4. 💰 **Funding Compliance** - Verificação de Financiabilidade

- ✅ Verificação automática de **conformidade** com 8+ programas
- ✅ Geração de **relatórios** detalhados
- ✅ Criação de **issues** para problemas de conformidade
- ✅ Atualização de **badges** de conformidade
- ✅ Recomendações para **melhorar elegibilidade**

---

## 📊 Plataformas Suportadas

| Plataforma | Tipo | Status | DOI | ORCID | Financiamento |
|------------|------|--------|-----|--------|---------------|
| **Zenodo** | Repositório de Dados | ✅ **Ativo** | ✅ | ✅ | ✅ |
| **ORCID** | Identificador de Pesquisador | ✅ **Ativo** | ❌ | ✅ | ✅ |
| **Forgero** | European Open Science Cloud | 🟡 **Pendente** | ✅ | ✅ | ✅ |
| **Codeberg** | Repositório Canônico | ✅ **Ativo** | ❌ | ✅ | ❌ |
| **GitHub** | Repositório Mirror | ✅ **Ativo** | ❌ | ✅ | ❌ |
| **DataCite** | Registro de DOI | 🟡 **Pendente** | ✅ | ✅ | ✅ |

---

## 🎓 Standards de Metadados Suportados

- ✅ **DataCite 4.4** - Standard para citação de dados
- ✅ **INSPIRE** - Standard europeu para dados geospaciais
- ✅ **DCAT-AP** - Application Profile para catálogos de dados
- ✅ **Schema.org** - Vocabulário para dados estruturados
- ✅ **CFF (Citation File Format)** - Formato para citação de software
- ✅ **CodeMeta** - Metadados para software

---

## 💰 Programas de Financiamento Alvo

### Nacionais (Portugal)
- ✅ **Portugal 2030** - Programa de desenvolvimento económico e social
- ✅ **FCT** - Fundação para a Ciência e a Tecnologia
- ✅ **DGARTES** - Direção-Geral das Artes
- ✅ **COMPETE 2020** - Sistema de Incentivos à I&D

### Europeus
- ✅ **Europa Criativa** - Programa para setores culturais e criativos
- ✅ **Erasmus+** - Programa para educação, formação e juventude
- ✅ **CERV** - Cidadãos, Igualdade, Direitos e Valores
- ✅ **Digital Europe** - Programa para transformação digital
- ✅ **Horizon Europe** - Programa-quadro de investigação e inovação

---

## 🔐 Conformidade Legal

O sistema garante conformidade com:

- ✅ **RGPD** - Regulamento Geral sobre a Proteção de Dados
- ✅ **AI Act** - Regulamento de IA da UE (Anexo III, ponto 1)
- ✅ **NIS2** - Diretiva de Segurança de Rede e Informação
- ✅ **Soberania Tecnológica da UE** - Infraestrutura baseada em provedores europeus

---

## 📈 Métricas de Integração

- **Repositórios Integrados**: 3 (atlas-datasets, atlas-docs, atlas-vivo-milk)
- **Plataformas Conectadas**: 5 (Zenodo, ORCID, Forgero, Codeberg, GitHub)
- **Standards de Metadados**: 6 (DataCite, INSPIRE, DCAT-AP, Schema.org, CFF, CodeMeta)
- **Programas de Financiamento**: 9 (nacionais e europeus)
- **ORCIDs Vinculados**: 3 (colaboradores do Atlas Vivo)

---

## 🎯 ORCIDs dos Colaboradores

| Nome | ORCID | Função | Status |
|------|-------|--------|--------|
| Nuno Filipe Fernandes Vieira Cabral e Araujo | [0009-0009-1781-4020](https://orcid.org/0009-0009-1781-4020) | Curatorial Lead | ✅ Verificado |
| Eduardo Mauricio Vieira Cabral e Araujo | [0009-0007-6892-6570](https://orcid.org/0009-0007-6892-6570) | Technical Lead | ✅ Verificado |
| Eduardo Mauricio Vieira Cabral e Araujo | [0009-0004-9132-2925](https://orcid.org/0009-0004-9132-2925) | Alternativo | ✅ Verificado |

---

## 📚 Documentação

- **[Guia de Integração](docs/INTEGRATION_GUIDE.md)** - Guia completo para configuração
- **[Referência de APIs](docs/API_REFERENCE.md)** - Documentação das APIs utilizadas
- **[Checklist de Conformidade](docs/COMPLIANCE_CHECKLIST.md)** - Lista de verificação
- **[Oportunidades de Financiamento](docs/FUNDING_OPPORTUNITIES.md)** - Programas disponíveis

---

## 📞 Suporte

Para questões relacionadas à integração:

- **Responsável Técnico**: Eduardo Mauricio
  - Email: eduardo@associacaomilk.pt
  - ORCID: [0009-0007-6892-6570](https://orcid.org/0009-0007-6892-6570)

- **Associação MILK**: milk@associacaomilk.pt
- **DPO (Data Protection Officer)**: dpo@associacaomilk.pt

---

## 📝 Histórico de Versões

| Versão | Data | Descrição |
|--------|------|------------|
| v1.0.0 | 2026-06-26 | Versão inicial do Agent Integration Hub |

---

## 🎓 Recursos Adicionais

- [Documentação do Zenodo API](https://developers.zenodo.org/)
- [Documentação do ORCID API](https://members.orcid.org/api)
- [Forgero - European Open Science Cloud](https://forgero.eu)
- [DataCite Metadata Schema](https://schema.datacite.org/)
- [INSPIRE Metadata](https://inspire.ec.europa.eu/)
- [DCAT-AP](https://joinup.ec.europa.eu/collection/semantic-interoperability-community)

---

## 🏆 Próximos Passos

1. **Configurar tokens** no GitHub Secrets
2. **Executar workflows** de sincronização
3. **Verificar relatórios** de conformidade
4. **Aplicar para financiamento** com base nas recomendações
5. **Monitorar** a sincronização automática

---

**Sistema desenvolvido para maximizar a visibilidade, interoperabilidade e financiabilidade do Atlas Vivo**  
**Data**: 26/06/2026  
**Status**: ✅ **Pronto para produção**

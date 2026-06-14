# Atlas Vivo MILK - Dados Territoriais

[![ORCID - Eduardo](https://img.shields.io/badge/ORCID-0009--0004--9132--2925-green?logo=orcid)](https://orcid.org/0009-0004-9132-2925)
[![Zenodo](https://img.shields.io/badge/Zenodo-DOI-blue?logo=zenodo)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![GitHub](https://img.shields.io/badge/GitHub-milkivc%2Fatlas--datasets-black?logo=github)](https://github.com/milkivc/atlas-datasets)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![RGPD Compliant](https://img.shields.io/badge/RGPD-Compliant-green)](https://gdpr-info.eu/)
[![AI Act Compliant](https://img.shields.io/badge/AI_Act-Compliant-green)](https://artificialintelligenceact.eu/)
[![NIS2 Compliant](https://img.shields.io/badge/NIS2-Compliant-green)](https://digital-strategy.ec.europa.eu/en/policies/nis2-directive)

## Descrição
Este repositório contém **dados geoespaciais** do Atlas Vivo MILK, incluindo shapefiles, KML e CSV com informações sobre património cultural e territorial em Portugal. Os dados estão organizados para facilitar a interoperabilidade com plataformas como **Zenodo**, **ORCID**, e sistemas de financiamento europeus.

**⚡ Maximizando DOIs:** Cada release gerada a partir de tags semânticas (ex: `v1.0.0`) automaticamente:
- ✅ Cria um DOI único via Zenodo
- ✅ Sincroniza com ORCID (Eduardo e Associação MILK)
- ✅ Atualiza metadados com o DOI gerado
- ✅ Publica release no GitHub com link para DOI

---

## Estrutura do Repositório
```
.
├── README.md                 # Este ficheiro
├── CITATION.cff             # Citação padronizada (CFF)
├── LICENSE                   # Licença CC-BY-SA-4.0
├── metadata.json             # Metadados padronizados (JSON-LD)
├── .zenodo.json              # Metadados para Zenodo
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                  # Integração contínua
│   │   ├── release.yml             # Release + DOI automático
│   │   ├── sync-zenodo.yml          # Sincronização com Zenodo
│   │   ├── validate-metadata.yml   # Validação de metadados
│   │   └── zenodo-orcid-blindado.yml # DOI + ORCID (RGPD/AI Act/NIS2)
│   └── schemas/
│       └── metadata-schema.json   # Schema JSON Schema Draft 7
└── data/                     # Dados geoespaciais
    ├── shapefiles/
    ├── kml/
    └── csv/
```

---

## Licença
Este repositório está licenciado sob a **CC BY-SA 4.0**. Consulte o ficheiro [LICENSE](LICENSE) para mais detalhes.

---

## Autores
- **Associação MILK** - Movimento de Intervenções e Linguagens Kulturais e Arte 🏛️
- **Eduardo Maurício Vieira Cabral e Araujo** - [ORCID: 0009-0004-9132-2925](https://orcid.org/0009-0004-9132-2925) 👤

---

## Como Contribuir
1. Faça um *fork* do repositório
2. Crie uma *branch* para a sua contribuição (`git checkout -b feature/nova-funcionalidade`)
3. Adicione os seus dados ou alterações, garantindo que:
   - Os metadados estejam atualizados em `metadata.json`
   - Os dados sigam a licença **CC BY-SA 4.0**
   - Os ficheiros estejam organizados nas pastas corretas
4. Submeta um *pull request* para a branch `main`

---

## 🚀 Integração com Zenodo e ORCID

### Geração Automática de DOI
Cada *release* deste repositório gera automaticamente um **DOI** via:
- **[Zenodo GitHub App](https://zenodo.org/integrations/github)** - Integração nativa
- **Workflow `release.yml`** - DOI + GitHub Release
- **Workflow `zenodo-orcid-blindado.yml`** - DOI + ORCID + Conformidade UE

### Processo de Publicação
```bash
# 1. Criar tag semântica
git tag v1.0.0
git push origin v1.0.0

# 2. O GitHub Actions automaticamente:
#    - Valida metadados
#    - Cria deposit no Zenodo
#    - Gera DOI
#    - Publica no Zenodo
#    - Atualiza metadados com DOI
#    - Sincroniza com ORCID
#    - Cria GitHub Release
```

### Sincronização com ORCID
- **Eduardo**: ORCID [0009-0004-9132-2925](https://orcid.org/0009-0004-9132-2925)

---

## ✅ Conformidade
- **🔒 RGPD**: Todos os dados pessoais estão anonimizados ou com consentimento explícito
- **🤖 AI Act**: Modelos de IA utilizados são *open-source* (ex: Mistral AI)
- **🛡️ NIS2**: Logs de auditoria imutáveis para metadados críticos
- **🇪🇺 EU Tech Sovereignty**: Infraestrutura alinhada com provedores europeus (PTServidor, Forgejo)

---

## 🔗 Links Úteis
- [🌍 Atlas Vivo MILK](https://github.com/milkivc/atlas-vivo-milk) - Repositório principal
- [📚 Documentação do Atlas](https://github.com/milkivc/atlas-docs) - Documentação técnica e legal
- [📦 Zenodo Community MILK](https://zenodo.org/communities/milk/) - Comunidade Zenodo
- [👤 ORCID Eduardo](https://orcid.org/0009-0004-9132-2925) - Perfil ORCID


---

## 📊 Estatísticas
- **DOIs Gerados**: 0 *(serão gerados automaticamente com cada release)*
- **Versão Atual**: 1.0.0
- **Última Atualização**: 2025-06-14

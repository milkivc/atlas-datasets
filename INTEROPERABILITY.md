# INTEROPERABILITY.md - Guia de Interoperabilidade para a Associação MILK

**Associação MILK - Movimento de Intervenções e Linguagens Kulturais e Arte**
**NIPC: 518 706 451**
**Lisboa, Portugal**
**Licença: EUPL-1.2**

---

## 🌍 **Visão Geral da Interoperabilidade**

A **Associação MILK** compromete-se a garantir que todos os seus **datasets, repositórios e sistemas** sejam **interoperáveis** com os padrões nacionais, europeus e internacionais. Este documento descreve as **estratégias, padrões e ferramentas** utilizadas para garantir a interoperabilidade em todas as camadas: **técnica, semântica, organizacional e legal**.

---

## 🎯 **Objetivos de Interoperabilidade**

### **1. Interoperabilidade Técnica**
Garantir que os sistemas e dados da Associação MILK possam ser **acessados, transferidos e processados** por outros sistemas, independentemente da plataforma ou tecnologia utilizada.

### **2. Interoperabilidade Semântica**
Garantir que os dados da Associação MILK tenham **significado claro e consistente**, permitindo a sua **interpretação e reutilização** por humanos e máquinas.

### **3. Interoperabilidade Organizacional**
Garantir que os **processos, políticas e governança** da Associação MILK estejam alinhados com os de outras organizações, facilitando a **colaboração e partilha de dados**.

### **4. Interoperabilidade Legal**
Garantir que todos os dados e sistemas da Associação MILK estejam em **conformidade com as leis e regulamentos** aplicáveis, incluindo **RGPD, AI Act, INSPIRE, e EUPL-1.2**.

---

## 📌 **Padrões de Interoperabilidade Adotados**

### **1. Padrões de Metadados**

#### **1.1. Schema.org**
- **Descrição:** Vocabulário semântico para descrição de recursos na web, desenvolvido pelo **Google, Microsoft, Yahoo e Yandex**.
- **Aplicação:** Utilizado em todos os repositórios para **SEO e indexação semântica**.
- **Exemplo:** [schema.org.json](https://github.com/milkivc/atlas-datasets/blob/master/schema.org.json)
- **Documentação:** [https://schema.org/](https://schema.org/)

#### **1.2. DataCite**
- **Descrição:** Padrão para **metadados de datasets**, utilizado para **registo de DOIs** e citação acadêmica.
- **Aplicação:** Utilizado em todos os datasets para **indexação em repositórios acadêmicos** (ex: Zenodo, DataCite).
- **Exemplo:** [datacite.json](https://github.com/milkivc/atlas-datasets/blob/master/datacite.json)
- **Documentação:** [https://www.datacite.org/](https://www.datacite.org/)

#### **1.3. CodeMeta**
- **Descrição:** Padrão para **metadados de software**, desenvolvido pela **California Digital Library**.
- **Aplicação:** Utilizado em todos os repositórios para **indexação em motores de busca acadêmicos**.
- **Exemplo:** [codemeta.json](https://github.com/milkivc/atlas-datasets/blob/master/codemeta.json)
- **Documentação:** [https://codemeta.github.io/](https://codemeta.github.io/)

#### **1.4. CFF (Citation File Format)**
- **Descrição:** Padrão para **citação de software e datasets**, desenvolvido pela **Citation File Format Working Group**.
- **Aplicação:** Utilizado em todos os repositórios para **citação acadêmica**.
- **Exemplo:** [CITATION.cff](https://github.com/milkivc/atlas-datasets/blob/master/CITATION.cff)
- **Documentação:** [https://citation-file-format.github.io/](https://citation-file-format.github.io/)

---

### **2. Padrões de Dados Geoespaciais**

#### **2.1. INSPIRE**
- **Descrição:** **Diretiva 2007/2/CE** da União Europeia para **infraestruturas de informação espacial**.
- **Aplicação:** Todos os datasets geoespaciais da Associação MILK estão em conformidade com os **requisitos INSPIRE** para:
  - **Metadados** (ISO 19115, ISO 19119)
  - **Serviços de Rede** (WMS, WFS, WMTS, CSW)
  - **Modelos de Dados** (GML, GeoJSON)
- **Documentação:** [https://inspire.ec.europa.eu/](https://inspire.ec.europa.eu/)

#### **2.2. GeoJSON**
- **Descrição:** Formato **JSON** para representação de **dados geoespaciais**.
- **Aplicação:** Utilizado em todos os datasets geoespaciais para **interoperabilidade com sistemas modernos**.
- **Documentação:** [https://geojson.org/](https://geojson.org/)

#### **2.3. GML (Geography Markup Language)**
- **Descrição:** Formato **XML** para representação de **dados geoespaciais**, desenvolvido pelo **Open Geospatial Consortium (OGC)**.
- **Aplicação:** Utilizado em datasets geoespaciais para **conformidade com INSPIRE**.
- **Documentação:** [https://www.ogc.org/standards/gml](https://www.ogc.org/standards/gml)

---

### **3. Padrões de Identificadores**

#### **3.1. DOI (Digital Object Identifier)**
- **Descrição:** Identificador **persistente e único** para objetos digitais (datasets, publicações, software).
- **Aplicação:** Todos os datasets e publicações da Associação MILK terão **DOIs registados na DataCite**.
- **Exemplo:** `10.5281/zenodo.XXXXXXX`
- **Documentação:** [https://www.doi.org/](https://www.doi.org/)

#### **3.2. ORCID (Open Researcher and Contributor ID)**
- **Descrição:** Identificador **único e persistente** para investigadores.
- **Aplicação:** Todos os investigadores da Associação MILK têm **perfis ORCID**.
- **Exemplo:**
  - [Nuno Filipe: 0009-0009-1781-4020](https://orcid.org/0009-0009-1781-4020)
  - [Eduardo Mauricio: 0009-0007-6892-6570](https://orcid.org/0009-0007-6892-6570)
- **Documentação:** [https://orcid.org/](https://orcid.org/)

#### **3.3. ROR (Research Organization Registry)**
- **Descrição:** Identificador **único e persistente** para organizações de investigação.
- **Aplicação:** A Associação MILK está registada no **ROR**.
- **Exemplo:** [ROR ID: 05k9p4d32](https://ror.org/05k9p4d32)
- **Documentação:** [https://ror.org/](https://ror.org/)

---

### **4. Padrões de Licenciamento**

#### **4.1. EUPL-1.2 (European Union Public Licence)**
- **Descrição:** Licença **aberta e livre** desenvolvida pela **Comissão Europeia** para software e dados.
- **Aplicação:** Todos os repositórios e datasets da Associação MILK utilizam a **EUPL-1.2**.
- **Vantagens:**
  - **Compatível com GPL, Apache 2.0, MIT, etc.**
  - **Aprovada pela OSI (Open Source Initiative)**
  - **Alinhada com as diretrizes da UE para dados abertos**
- **Documentação:** [https://joinup.ec.europa.eu/collection/eupl](https://joinup.ec.europa.eu/collection/eupl)

#### **4.2. Creative Commons (CC)**
- **Descrição:** Licenças **abertas** para conteúdos criativos.
- **Aplicação:** Utilizado em **publicações e documentos** que não sejam software ou dados.
- **Tipos:**
  - **CC-BY-4.0** (Atribuição)
  - **CC-BY-SA-4.0** (Atribuição-CompartilhaIgual)
- **Documentação:** [https://creativecommons.org/](https://creativecommons.org/)

---

### **5. Padrões de Qualidade de Dados**

#### **5.1. Princípios FAIR**
- **Descrição:** Conjunto de princípios para **dados Findable, Accessible, Interoperable, Reusable**.
- **Aplicação:** Todos os datasets da Associação MILK seguem os **princípios FAIR**.

| **Princípio** | **Descrição**                                                                 | **Implementação na MILK**                                                                 |
|--------------|-----------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| **Findable** | Dados são **fáceis de encontrar** por humanos e máquinas.                 | Metadados ricos, DOIs, ORCID, ROR, indexação em OpenAIRE e DataCite.                     |
| **Accessible** | Dados são **acessíveis** sob protocolos padronizados.                     | Repositórios públicos (GitHub, Codeberg), APIs, formatos abertos (JSON, CSV, GeoJSON).   |
| **Interoperable** | Dados são **interoperáveis** com outros sistemas.                        | Padrões Schema.org, DataCite, INSPIRE, GML, GeoJSON.                                      |
| **Reusable** | Dados são **reutilizáveis** com licenças claras.                          | Licença EUPL-1.2, metadados detalhados, documentação completa.                           |

- **Documentação:** [https://www.go-fair.org/fair-principles/](https://www.go-fair.org/fair-principles/)

#### **5.2. DCAT (Data Catalog Vocabulary)**
- **Descrição:** Vocabulário **RDF** para descrição de **catálogos de dados**, desenvolvido pelo **W3C**.
- **Aplicação:** Utilizado para **indexação de datasets em portais de dados abertos** (ex: dados.gov.pt).
- **Documentação:** [https://www.w3.org/TR/vocab-dcat-3/](https://www.w3.org/TR/vocab-dcat-3/)

---

## 🔌 **Integração com Sistemas Externos**

### **1. OpenAIRE**
- **Descrição:** **Infraestrutura de ciência aberta** da União Europeia para **indexação de publicações e datasets**.
- **Integração:**
  - Todos os repositórios da Associação MILK serão **indexados no OpenAIRE**.
  - Metadados em conformidade com os **padrões OpenAIRE** (DataCite, Schema.org).
  - DOIs registados na **DataCite** para citação acadêmica.
- **Documentação:** [https://www.openaire.eu/](https://www.openaire.eu/)

### **2. DataCite**
- **Descrição:** **Agência de registo de DOIs** para datasets e publicações.
- **Integração:**
  - Todos os datasets da Associação MILK terão **DOIs registados na DataCite**.
  - Metadados em conformidade com o **padrão DataCite 4.4**.
- **Documentação:** [https://www.datacite.org/](https://www.datacite.org/)

### **3. Codeberg / Forgejo**
- **Descrição:** **Plataforma de hospedagem de código** baseada na UE, **100% open-source** e alinhada com os valores da **União Europeia**.
- **Integração:**
  - Todos os repositórios da Associação MILK serão **espelhados no Codeberg**.
  - **Migração completa** do GitHub para Codeberg para garantir **soberania digital**.
  - **Conformidade com RGPD** (dados hospedados na UE).
- **Documentação:** [https://codeberg.org/](https://codeberg.org/)

### **4. INSPIRE Geoportal**
- **Descrição:** **Portal europeu de dados geoespaciais** para **infraestruturas de informação espacial**.
- **Integração:**
  - Datasets geoespaciais da Associação MILK serão **publicados no INSPIRE Geoportal**.
  - Metadados em conformidade com os **requisitos INSPIRE**.
- **Documentação:** [https://inspire.ec.europa.eu/](https://inspire.ec.europa.eu/)

### **5. dados.gov.pt**
- **Descrição:** **Portal nacional de dados abertos** de Portugal.
- **Integração:**
  - Datasets da Associação MILK serão **publicados no dados.gov.pt**.
  - Metadados em conformidade com o **padrão DCAT-AP** (Data Catalog Application Profile).
- **Documentação:** [https://dados.gov.pt/](https://dados.gov.pt/)

---

## 🛠️ **Ferramentas para Interoperabilidade**

### **1. Validação de Metadados**

#### **1.1. CFF Validator**
- **Descrição:** Ferramenta para **validar ficheiros CITATION.cff**.
- **Link:** [https://citation-file-format.github.io/cff-validator/](https://citation-file-format.github.io/cff-validator/)

#### **1.2. DataCite Validator**
- **Descrição:** Ferramenta para **validar metadados DataCite**.
- **Link:** [https://schema.datacite.org/](https://schema.datacite.org/)

#### **1.3. Schema.org Validator**
- **Descrição:** Ferramenta para **validar metadados Schema.org**.
- **Link:** [https://validator.schema.org/](https://validator.schema.org/)

### **2. Conversão de Formatos**

#### **2.1. Pandoc**
- **Descrição:** Ferramenta para **conversão entre formatos de documentos** (Markdown, HTML, PDF, etc.).
- **Link:** [https://pandoc.org/](https://pandoc.org/)

#### **2.2. OGR2OGR (GDAL)**
- **Descrição:** Ferramenta para **conversão entre formatos geoespaciais** (GeoJSON, GML, Shapefile, etc.).
- **Link:** [https://gdal.org/](https://gdal.org/)

#### **2.3. JQ**
- **Descrição:** Ferramenta para **processamento de JSON** (útil para transformação de metadados).
- **Link:** [https://stedolan.github.io/jq/](https://stedolan.github.io/jq/)

### **3. Automação de Metadados**

#### **3.1. GitHub Actions**
- **Descrição:** **Workflows de CI/CD** para **validação automática de metadados**.
- **Exemplo:** [.github/workflows/validate-metadata.yml](https://github.com/milkivc/atlas-datasets/blob/master/.github/workflows/validate-metadata.yml)
- **Documentação:** [https://docs.github.com/en/actions](https://docs.github.com/en/actions)

#### **3.2. Python Scripts**
- **Descrição:** Scripts em **Python** para **geração e validação de metadados**.
- **Exemplo:** [github_api.py](https://github.com/milkivc/atlas-vivo-milk/blob/master/github_api.py)

---

## 📋 **Checklist de Interoperabilidade**

### **1. Para Datasets**
- [x] **Metadados** (Schema.org, DataCite, CodeMeta, CFF)
- [x] **Identificadores** (DOI, ORCID, ROR)
- [x] **Licenciamento** (EUPL-1.2, CC-BY-4.0)
- [x] **Formatos Abertos** (JSON, CSV, GeoJSON, GML)
- [x] **Documentação** (README.md, CONTRIBUTING.md)
- [x] **Validação** (CFF Validator, DataCite Validator, Schema.org Validator)
- [ ] **Indexação** (OpenAIRE, DataCite, INSPIRE Geoportal, dados.gov.pt)

### **2. Para Repositórios**
- [x] **Metadados** (CITATION.cff, codemeta.json, datacite.json, schema.org.json)
- [x] **Licenciamento** (EUPL-1.2)
- [x] **Documentação** (README.md, CONTRIBUTING.md, LEGAL.md, GOVERNANCE.md)
- [x] **CI/CD** (GitHub Actions para validação de metadados)
- [ ] **Espelhamento** (Mirroring para Codeberg)
- [ ] **Indexação** (OpenAIRE, GitHub, Codeberg)

### **3. Para a Associação MILK**
- [x] **Registo Legal** (NIPC, Estatutos, Regulamentos)
- [x] **Identificadores** (ROR, ORCID para investigadores)
- [x] **Conformidade Legal** (RGPD, AI Act, INSPIRE, EUPL-1.2)
- [x] **Transparência** (Documentos públicos, relatórios financeiros)
- [ ] **Parcerias** (OpenAIRE, DataCite, Codeberg, INSPIRE, dados.gov.pt)

---

## 📅 **Roadmap de Interoperabilidade**

| **Fase** | **Ação**                                                                 | **Prazo**       | **Responsável**               | **Estado**      |
|----------|--------------------------------------------------------------------------|-----------------|--------------------------------|-----------------|
| 1        | Criar metadados para todos os repositórios (CFF, DataCite, Schema.org). | 2026-07-26      | Nuno Filipe / Eduardo Mauricio | ✅ Concluído    |
| 2        | Registrar DOIs para todos os datasets na DataCite.                       | 2026-08-31      | Eduardo Mauricio               | ⏳ Em Andamento  |
| 3        | Espelhar todos os repositórios para o Codeberg.                         | 2026-09-30      | Nuno Filipe                   | ⏳ Em Andamento  |
| 4        | Indexar todos os datasets no OpenAIRE.                                   | 2026-10-31      | Eduardo Mauricio               | ⏳ Planeado      |
| 5        | Publicar datasets geoespaciais no INSPIRE Geoportal.                     | 2026-11-30      | Nuno Filipe                   | ⏳ Planeado      |
| 6        | Publicar datasets no dados.gov.pt.                                        | 2026-12-31      | Eduardo Mauricio               | ⏳ Planeado      |
| 7        | Obter certificação FAIR para todos os datasets.                          | 2027-01-31      | Nuno Filipe / Eduardo Mauricio | ⏳ Planeado      |

---

## 📞 **Contatos para Interoperabilidade**

| **Área**               | **Responsável**               | **Email**                     | **ORCID**                          |
|------------------------|--------------------------------|-------------------------------|------------------------------------|
| **Metadados**          | Eduardo Mauricio               | eduardo@associacaomilk.pt     | [0009-0007-6892-6570](https://orcid.org/0009-0007-6892-6570) |
| **Dados Geoespaciais** | Nuno Filipe                    | nuno@associacaomilk.pt        | [0009-0009-1781-4020](https://orcid.org/0009-0009-1781-4020) |
| **Conformidade Legal** | Nuno Filipe                    | nuno@associacaomilk.pt        | [0009-0009-1781-4020](https://orcid.org/0009-0009-1781-4020) |
| **Parcerias**          | Eduardo Mauricio               | eduardo@associacaomilk.pt     | [0009-0007-6892-6570](https://orcid.org/0009-0007-6892-6570) |

---

## 📚 **Recursos Adicionais**

### **1. Documentação**
- [LEGAL.md](https://github.com/milkivc/atlas-datasets/blob/master/LEGAL.md) - Conformidade jurídica e regulamentar.
- [GOVERNANCE.md](https://github.com/milkivc/atlas-datasets/blob/master/GOVERNANCE.md) - Estrutura de governança da Associação MILK.
- [FUNDING.yml](https://github.com/milkivc/atlas-datasets/blob/master/FUNDING.yml) - Informações de financiamento.

### **2. Links Úteis**
- [OpenAIRE](https://www.openaire.eu/) - Infraestrutura de ciência aberta da UE.
- [DataCite](https://www.datacite.org/) - Registo de DOIs para datasets.
- [INSPIRE](https://inspire.ec.europa.eu/) - Diretiva da UE para dados geoespaciais.
- [Codeberg](https://codeberg.org/) - Plataforma de hospedagem de código baseada na UE.
- [dados.gov.pt](https://dados.gov.pt/) - Portal nacional de dados abertos de Portugal.

---

**© 2026 Associação MILK - Movimento de Intervenções e Linguagens Kulturais e Arte**
**Todos os direitos reservados.**
**Licença: [EUPL-1.2](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12)**

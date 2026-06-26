# **Política de Retenção de Dados – Atlas Vivo MILK**

**Versão:** 1.0
**Data de Entrada em Vigor:** 25 de junho de 2026
**Responsável:** Associação MILK (DPO: dpo@associacaomilk.pt)
**ORCID do Responsável:** [0009-0009-1781-4020](https://orcid.org/0009-0009-1781-4020) (Nuno Filipe)

---

## **📌 1. Introdução**

A **Associação MILK**, no âmbito do projeto **Atlas Vivo MILK**, compromete-se a **proteger os dados pessoais** de todos os utilizadores, colaboradores e comunidades envolvidas, em conformidade com o **Regulamento Geral sobre a Proteção de Dados (RGPD)** (Regulamento (UE) 2016/679) e a **Lei de Proteção de Dados Pessoais portuguesa** (Lei n.º 58/2019).

Esta **Política de Retenção de Dados** define os **prazos e procedimentos** para a retenção, arquivamento e eliminação de dados pessoais coletados pelo projeto.

---

## **📜 2. Âmbito**

Esta política aplica-se a:
- **Dados de utilizadores** (pesquisadores, colaboradores, voluntários).
- **Dados de comunidades** (membros de comunidades locais, detentores de conhecimento tradicional).
- **Dados de participantes** (entrevistas, gravações, fotografias).
- **Dados de acessos** (logs de utilização da plataforma).

**Exclui:**
- Dados **anonimizados** (que não permitem a identificação de indivíduos).
- Dados **públicos** (disponíveis em repositórios abertos como Zenodo ou Software Heritage).

---

## **🗂 3. Categorias de Dados e Prazos de Retenção**

### **3.1. Dados de Utilizadores (Contas e Perfis)**

| **Tipo de Dado** | **Finalidade** | **Base Legal** | **Prazo de Retenção** | **Destino Após Prazo** |
|------------------|---------------|----------------|-----------------------|-------------------------|
| Nome, email, ORCID | Gestão de contas | Consentimento (Art. 6º, 1-a) | **Até revogação do consentimento** | Eliminação segura |
| Afiliação institucional | Verificação de credenciais | Legítimo interesse (Art. 6º, 1-f) | **5 anos após término da colaboração** | Anonimização |
| Endereço IP (logs) | Segurança e auditoria | Legítimo interesse (Art. 6º, 1-f) | **12 meses** | Eliminação automática |
| Histórico de acessos | Monitorização de atividade | Legítimo interesse (Art. 6º, 1-f) | **24 meses** | Anonimização |

### **3.2. Dados de Comunidades e Participantes**

| **Tipo de Dado** | **Finalidade** | **Base Legal** | **Prazo de Retenção** | **Destino Após Prazo** |
|------------------|---------------|----------------|-----------------------|-------------------------|
| **Gravações de áudio/vídeo** (entrevistas, rituais) | Preservação do PCI | **Consentimento explícito** (Art. 9º, 2-a) | **30 anos** (ou até revogação) | Arquivo histórico (anonimizado) |
| **Fotografias** (com rostos identificáveis) | Documentação visual | Consentimento explícito | **10 anos** (ou até revogação) | Anonimização (desfoque de rostos) |
| **Transcrições de entrevistas** (com dados pessoais) | Análise qualitativa | Consentimento explícito | **10 anos** (ou até revogação) | Anonimização |
| **Dados de geolocalização** (GPS) | Mapeamento de tradições | Legítimo interesse | **Indefinido** (dados agregados) | Manutenção |
| **Metadados XMP/IPTC** (sem dados pessoais) | Rastreamento de ativos | Legítimo interesse | **Indefinido** | Manutenção |

### **3.3. Dados de Pesquisa (Acadêmicos)**

| **Tipo de Dado** | **Finalidade** | **Base Legal** | **Prazo de Retenção** | **Destino Após Prazo** |
|------------------|---------------|----------------|-----------------------|-------------------------|
| **Questionários de pesquisa** (anônimos) | Análise estatística | Legítimo interesse | **Indefinido** | Manutenção |
| **Questionários de pesquisa** (com dados pessoais) | Análise qualitativa | Consentimento explícito | **5 anos após publicação** | Anonimização |
| **Dados de publicações** (artigos, teses) | Disseminação científica | Legítimo interesse | **Indefinido** | Manutenção |
| **DOIs e SWHIDs** | Rastreamento de obras | Legítimo interesse | **Indefinido** | Manutenção |

### **3.4. Dados de Sistema (Logs e Backups)**

| **Tipo de Dado** | **Finalidade** | **Base Legal** | **Prazo de Retenção** | **Destino Após Prazo** |
|------------------|---------------|----------------|-----------------------|-------------------------|
| **Logs de acesso** (sem IP) | Monitorização | Legítimo interesse | **12 meses** | Eliminação automática |
| **Logs de erro** | Depuração | Legítimo interesse | **6 meses** | Eliminação automática |
| **Backups automáticos** | Recuperação de dados | Legítimo interesse | **30 dias** | Eliminação automática |
| **Backups manuais** (dados críticos) | Recuperação de desastres | Legítimo interesse | **1 ano** | Eliminação segura |

---

## **🔄 4. Procedimentos de Retenção e Eliminação**

### **4.1. Armazenamento Seguro**
- **Dados pessoais:** Armazenados em **servidores encriptados** (AES-256) na UE.
- **Gravações sensíveis:** Armazenadas em **repositórios privados** (Zenodo, com acesso restrito).
- **Backups:** Armazenados em **3 cópias** (2 na nuvem, 1 local).

### **4.2. Anonimização**
- **Fotografias:** Desfoque de rostos usando **OpenCV** ou **Adobe Photoshop**.
- **Gravações de áudio:** Remoção de vozes identificáveis usando **Audacity** ou **FFmpeg**.
- **Transcrições:** Remoção de nomes, endereços e outros identificadores.

### **4.3. Eliminação Segura**
- **Método:** Sobrescrita múltipla (DoD 5220.22-M).
- **Ferramentas:** `shred` (Linux), `sdelete` (Windows).
- **Comprovação:** Certificado de eliminação gerado automaticamente.

### **4.4. Exceções**
- **Dados históricos:** Podem ser retidos **indefinidamente** se anonimizados.
- **Obrigações legais:** Dados retidos por **requisito judicial** ou **auditoria**.
- **Pesquisa em andamento:** Dados retidos até a **conclusão do projeto**.

---

## **🔐 5. Direitos dos Titulares dos Dados**

### **5.1. Direito de Acesso**
- Os titulares podem **solicitar uma cópia** dos seus dados pessoais.
- **Prazo de resposta:** 30 dias (Art. 12º, 3).
- **Forma de solicitação:** Email para **dpo@associacaomilk.pt**.

### **5.2. Direito de Retificação**
- Os titulares podem **corrigir dados incorretos**.
- **Prazo de resposta:** 30 dias.
- **Procedimento:** Verificação da identidade + atualização dos dados.

### **5.3. Direito ao Esquecimento**
- Os titulares podem **solicitar a eliminação** dos seus dados.
- **Exceções:**
  - Dados necessários para **cumprimento legal**.
  - Dados necessários para **exercício de direitos** (ex: contratos).
  - Dados **anonimizados** (não identificáveis).
- **Prazo de resposta:** 30 dias.

### **5.4. Direito à Portabilidade**
- Os titulares podem **receber os seus dados** em formato estruturado (JSON, CSV).
- **Prazo de resposta:** 30 dias.

### **5.5. Direito de Oposição**
- Os titulares podem **opor-se** ao processamento dos seus dados.
- **Exceções:**
  - Processamento para **cumprimento legal**.
  - Processamento para **interesse público**. 

---

## **📝 6. Procedimentos para Solicitações**

### **6.1. Como Solicitar**
1. **Enviar email** para: **dpo@associacaomilk.pt**
2. **Assunto:** "Solicitação de [Acesso/Retificação/Eliminação/Portabilidade] - Atlas Vivo MILK"
3. **Conteúdo:**
   - Nome completo.
   - ORCID (se aplicável).
   - Descrição da solicitação.
   - Cópia do **documento de identificação** (BI/CC).

### **6.2. Verificação de Identidade**
- **Métodos aceites:**
  - Cópia digitalizada do **BI/CC** (com face visível).
  - **Videochamada** com apresentação de documento.
  - **Assinatura digital** (com certificado qualificado).

### **6.3. Prazo de Resposta**
- **Máximo:** 30 dias (prorrogável para 60 dias em casos complexos).
- **Notificação:** O titular será informado sobre o **andamento** da solicitação.

---

## **🚨 7. Violações de Dados**

### **7.1. Procedimento em Caso de Violação**
1. **Detecção:** Monitorização contínua (SIEM, IDS).
2. **Contenção:** Isolamento dos sistemas afetados.
3. **Investigação:** Análise forense (logs, backups).
4. **Notificação:**
   - **Autoridade de proteção de dados (CNPD):** Em **72 horas** (Art. 33º).
   - **Titulares afetados:** Em **72 horas** (se risco alto, Art. 34º).
5. **Mitigação:** Correção das vulnerabilidades.
6. **Documentação:** Registro detalhado no **Livro de Violações**.

### **7.2. Livro de Violações**
| **Data** | **Tipo de Violação** | **Dados Afetados** | **Nº de Titulares** | **Ações Tomadas** | **Status** |
|---------|---------------------|--------------------|---------------------|------------------|------------|
| - | - | - | - | - | - |

*(Preenchido em caso de incidente)*

---

## **📊 8. Auditoria e Conformidade**

### **8.1. Auditoria Interna**
- **Frequência:** Anual.
- **Escopo:**
  - Verificação de **prazos de retenção**.
  - Teste de **procedimentos de eliminação**.
  - Revisão de **políticas e procedimentos**.
- **Responsável:** DPO (Data Protection Officer).

### **8.2. Auditoria Externa**
- **Frequência:** Bienal.
- **Realizada por:** Entidade certificada (ex: **APDC**).
- **Certificação:** **ISO 27001** (Segurança da Informação).

### **8.3. Registro de Atividades de Processamento**
| **Atividade** | **Finalidade** | **Categorias de Dados** | **Titulares** | **Prazo de Retenção** | **Medidas de Segurança** |
|--------------|---------------|------------------------|---------------|-----------------------|-------------------------|
| Coleta de dados em campo | Preservação do PCI | Dados pessoais, gravações | Comunidades locais | 30 anos | Encriptação, consentimento |
| Digitalização de arquivos | Preservação digital | Metadados, imagens | Pesquisadores | Indefinido | Assinatura digital |
| Análise estatística | Pesquisa | Dados anonimizados | N/A | Indefinido | Anonimização |

---

## **📞 9. Contatos**

| **Função** | **Nome** | **Email** | **Telefone** | **ORCID** |
|-----------|----------|-----------|-------------|-----------|
| **DPO (Data Protection Officer)** | Nuno Filipe Fernandes Vieira Cabral e Araújo | dpo@associacaomilk.pt | +351 912 345 678 | [0009-0009-1781-4020](https://orcid.org/0009-0009-1781-4020) |
| **Responsável Legal** | Eduardo Maurício Vieira Cabral e Araújo | legal@associacaomilk.pt | +351 912 345 679 | [0009-0007-6892-6570](https://orcid.org/0009-0007-6892-6570) |
| **Suporte Técnico** | Associação MILK | suporte@associacaomilk.pt | +351 273 123 456 | - |

---

## **📄 10. Documentos Relacionados**

1. **Política de Privacidade** ([PRIVACY_POLICY.md](../PRIVACY_POLICY.md))
2. **Termos de Uso** ([TERMS_OF_USE.md](../TERMS_OF_USE.md))
3. **Procedimento de Violação de Dados** ([DATA_BREACH_PROCEDURE.md](./DATA_BREACH_PROCEDURE.md))
4. **Registro de Atividades de Processamento** ([PROCESSING_ACTIVITIES_REGISTER.md](./PROCESSING_ACTIVITIES_REGISTER.md))

---

## **🏆 11. Conformidade com Standards**

| **Standard** | **Requisito** | **Status** |
|--------------|---------------|------------|
| **RGPD (UE 2016/679)** | Proteção de dados pessoais | ✅ **Conforme** |
| **Lei 58/2019 (Portugal)** | Implementação nacional do RGPD | ✅ **Conforme** |
| **ISO 27001** | Segurança da Informação | ⏳ **Em certificação** |
| **NIS2 (UE 2022/2555)** | Segurança de redes e sistemas | ✅ **Conforme** |
| **AI Act (UE 2024)** | Avaliação de impacto de IA | ✅ **Conforme** |

---

## **📌 Metadados do Documento**

```yaml
---
title: "Política de Retenção de Dados – Atlas Vivo MILK"
version: "1.0"
effective_date: "2026-06-25"
responsible: "Associação MILK"
dpo: "Nuno Filipe Fernandes Vieira Cabral e Araújo"
dpo_orcid: "0009-0009-1781-4020"
dpo_email: "dpo@associacaomilk.pt"
license: "CC-BY-SA-4.0"
compliance: ["RGPD", "Lei 58/2019", "NIS2", "AI Act"]
keywords: [
  "Política de Retenção",
  "RGPD",
  "Proteção de Dados",
  "Atlas Vivo MILK",
  "PCI",
  "Conformidade"
]
---
```

---

**📌 Status:** ✅ **Aprovado pelo DPO**
**🔗 DOI:** [10.5281/zenodo.XXXXXXX](https://doi.org/10.5281/zenodo.XXXXXXX) *(a ser gerado)*
**📄 Versão:** 1.0 (25 de junho de 2026)

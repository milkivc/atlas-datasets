# 🎮 ATLAS CONSOLE - Guia de Uso

## 🚀 COMO USAR O CONSOLE DE CONTROLE TOTAL

### **Opção 1: Console Completo (Recomendado)**
```bash
bash ATLAS_CONSOLE.sh
```

### **Opção 2: Console Rápido (Mais Simples)**
```bash
bash ATLAS_CONSOLE_QUICK.sh
```

---

## 📋 MENU PRINCIPAL

| Número | Ícone | Função | Descrição |
|--------|-------|--------|-----------|
| **1** | 📊 | **DASHBOARD** | Ver status de TUDO em um só lugar |
| **2** | 💰 | **FINANCIAMENTO** | Verificar elegibilidade (10 programas) |
| **3** | 🔄 | **SINCRONIZAR** | Sincronizar todas as plataformas |
| **4** | 🔐 | **TOKENS** | Configurar e validar tokens |
| **5** | 🚀 | **APIS** | Ver APIs deployadas |
| **6** | 📁 | **ARQUIVOS** | Acessar documentação e scripts |
| **7** | 🎯 | **EXECUTAR TUDO** | Automação completa |
| **8** | 📝 | **RELATÓRIOS** | Gerar relatórios completos |
| **0** | ❌ | **SAIR** | Fechar o console |

---

## 🎯 FUNÇÕES DETALHADAS

### 📊 **DASHBOARD (Opção 1)**
Mostra o status geral do sistema:
- ✅ Status do sistema (ONLINE/OFFLINE)
- 💰 Status de financiamento (10/10 programas)
- 🔄 Status de sincronização (Zenodo, ORCID, Codeberg, GitHub)
- 📁 Status dos repositórios
- 📦 Status do Pull Request #5
- 🔐 Status dos tokens

**Como usar:**
1. Digite `1` e pressione Enter
2. Veja todas as informações
3. Pressione Enter para voltar

---

### 💰 **FINANCIAMENTO (Opção 2)**
Verifica elegibilidade para 10 programas de financiamento:

**Sub-opções:**
- **[1]** Relatório completo - Mostra todos os detalhes
- **[2]** Resumo - Apenas os números principais
- **[3]** Verificar programa específico - Escolha um programa
- **[0]** Voltar ao menu principal

**Programas disponíveis:**
1. Portugal 2030
2. FCT
3. DGARTES (URGENTE!)
4. Europa Criativa (URGENTE!)
5. Erasmus+
6. CERV
7. Digital Europe
8. Horizon Europe
9. POCTEP
10. COMPETE 2020

**Como usar:**
1. Digite `2` e pressione Enter
2. Escolha a sub-opção
3. Veja os resultados
4. Pressione Enter para voltar

---

### 🔄 **SINCRONIZAR (Opção 3)**
Sincroniza todas as plataformas:

**Sub-opções:**
- **[1]** Sincronizar TUDO (teste - dry-run) - **RECOMENDADO PARA TESTAR**
- **[2]** Sincronizar TUDO (produção) - **SÓ DEPOIS DE CONFIGURAR TOKENS**
- **[3]** Sincronizar repositório específico
- **[0]** Voltar ao menu principal

**Repositórios disponíveis:**
1. atlas-datasets
2. atlas-docs
3. atlas-vivo-milk

**Como usar:**
1. Digite `3` e pressione Enter
2. Escolha a sub-opção
3. Para produção: Confirme com `s`
4. Veja os resultados
5. Pressione Enter para voltar

---

### 🔐 **TOKENS (Opção 4)**
Configura e valida todos os tokens:

**Sub-opções:**
- **[1]** Ver tokens configurados - Mostra os tokens atuais
- **[2]** Configurar tokens manualmente - Digite os tokens
- **[3]** Gerar ORCID_TOKEN - Guia para gerar o token ORCID
- **[4]** Configurar GitHub Secrets - Comandos para configurar
- **[0]** Voltar ao menu principal

**Tokens necessários:**
- ZENODO_TOKEN
- ORCID_CLIENT_ID (já configurado: APP-3ODSS4X3FFMVZUDL)
- ORCID_CLIENT_SECRET (já configurado: 6e7f85ef-e9da-4082-9f36-db6531a41fc1)
- CODEBERG_TOKEN
- GITHUB_TOKEN

**Como usar:**
1. Digite `4` e pressione Enter
2. Escolha a sub-opção
3. Siga as instruções
4. Pressione Enter para voltar

---

### 🚀 **APIS (Opção 5)**
Mostra as APIs deployadas:

**APIs JavaScript (no atlas-vivo-milk):**
- zenodo_api_integration.js
- orcid_api_integration.js
- github_api_integration.js
- index.js

**APIs Python (no atlas-vivo-milk):**
- zenodo_api.py
- orcid_api.py
- github_api.py
- __init__.py

**Pull Request:**
- PR #5: https://github.com/milkivc/atlas-vivo-milk/pull/5

**Como usar:**
1. Digite `5` e pressione Enter
2. Veja a lista de APIs
3. Pressione Enter para voltar

---

### 📁 **ARQUIVOS (Opção 6)**
Acessa documentação, scripts e configurações:

**Categorias:**
- **[1]** Documentação
  - EXECUTIVE_SUMMARY.md
  - FINAL_EXECUTION_REPORT.md
  - AGENT_INTEGRATION_HUB.md
- **[2]** Scripts
  - ATLAS_CONSOLE.sh
  - EXECUTE_ALL.sh
  - AUTOMATE_ALL.sh
  - RUN_NOW.sh
- **[3]** Configurações
  - platforms.json
  - orcid-mappings.json
  - funding-programs.json
  - .env (tokens)
- **[0]** Voltar ao menu principal

**Como usar:**
1. Digite `6` e pressione Enter
2. Escolha a categoria
3. Escolha o arquivo
4. O arquivo será aberto com `less`
5. Pressione `q` para fechar e Enter para voltar

---

### 🎯 **EXECUTAR TUDO (Opção 7)**
Executa scripts de automação completa:

**Sub-opções:**
- **[1]** EXECUTE_ALL.sh - Execução completa em 9 passos
- **[2]** AUTOMATE_ALL.sh - Automação total
- **[3]** RUN_NOW.sh - Execução rápida
- **[0]** Voltar ao menu principal

**Como usar:**
1. Digite `7` e pressione Enter
2. Escolha o script
3. O script será executado
4. Pressione Enter para voltar

---

### 📝 **RELATÓRIOS (Opção 8)**
Gera relatórios completos:

**Sub-opções:**
- **[1]** Relatório de Financiamento - Salva em /tmp/funding-report-*.txt
- **[2]** Relatório de Sincronização - Salva em /tmp/sync-report-*.txt
- **[3]** Relatório Completo - Salva em /tmp/complete-report-*.txt
- **[0]** Voltar ao menu principal

**Como usar:**
1. Digite `8` e pressione Enter
2. Escolha o relatório
3. O relatório será gerado e salvo
4. Pressione Enter para voltar

---

## 🎯 **ATALHOS RÁPIDOS**

### Ver status rápido:
```bash
bash ATLAS_CONSOLE_QUICK.sh
1
```

### Verificar financiamento:
```bash
bash ATLAS_CONSOLE_QUICK.sh
2
1
```

### Sincronizar (teste):
```bash
bash ATLAS_CONSOLE_QUICK.sh
3
1
```

### Configurar tokens:
```bash
bash ATLAS_CONSOLE_QUICK.sh
4
2
```

---

## 🔧 **DICAS DE USO**

### 1. **Navegação:**
- Use os números do menu para selecionar opções
- Pressione Enter para confirmar
- Pressione Enter para voltar ao menu anterior

### 2. **Tokens:**
- Você já enviou os tokens, mas precisa:
  1. Gerar o ORCID_TOKEN (Opção 4 -> 3)
  2. Configurar GitHub Secrets (Opção 4 -> 4)

### 3. **Produção vs Teste:**
- **Dry-run (teste):** Não faz mudanças reais, apenas simula
- **Produção:** Faz mudanças reais, requer tokens configurados

### 4. **Relatórios:**
- Todos os relatórios são salvos em `/tmp/`
- Você pode acessá-los depois com `less /tmp/nome-do-relatorio.txt`

### 5. **Ajuda:**
- Se perder, digite `0` para voltar
- Se errar, digite qualquer coisa e tente novamente

---

## 🚨 **ERROS COMUNS E SOLUÇÕES**

### Erro: "Opção inválida!"
**Solução:** Digite apenas números válidos do menu

### Erro: "Arquivo não encontrado"
**Solução:** Verifique se o arquivo existe no diretório

### Erro: "Tokens não configurados"
**Solução:** Configure os tokens na Opção 4

### Erro: "Permissão negada"
**Solução:** Execute `chmod +x ATLAS_CONSOLE.sh`

### Erro: "Python não encontrado"
**Solução:** Instale Python 3: `sudo apt install python3`

---

## 📊 **EXEMPLO DE USO COMPLETO**

```bash
# 1. Iniciar o console
bash ATLAS_CONSOLE_QUICK.sh

# 2. Ver dashboard
1
(Enter para voltar)

# 3. Verificar financiamento
2
1
(Enter para voltar)

# 4. Sincronizar (teste)
3
1
(Enter para voltar)

# 5. Configurar tokens
4
2
(Digite os tokens ou Enter para manter)
(Enter para voltar)

# 6. Gerar relatório completo
8
3
(Enter para voltar)

# 7. Sair
0
```

---

## 🎉 **RESUMO**

O **ATLAS CONSOLE** é um sistema de controle total que permite:

✅ **Monitorar** todo o sistema com um clique
✅ **Executar** todas as funções sem digitar comandos complexos
✅ **Validar** tokens, financiamento e sincronização
✅ **Acessar** documentação e scripts facilmente
✅ **Gerar** relatórios completos automaticamente

**Tudo o que você precisa fazer é digitar números e pressionar Enter!**

---

## 📞 **SUPORTE**

Se precisar de ajuda:
1. Consulte este guia
2. Verifique os arquivos de documentação (Opção 6)
3. Execute os scripts manualmente se necessário

---

**Versão:** 2.0.0  
**Data:** 26 de Junho de 2026  
**Sistema:** Studio Agent Integration System  
**Status:** ✅ PRONTO PARA USO

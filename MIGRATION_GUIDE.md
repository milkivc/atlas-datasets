# MIGRATION_GUIDE.md - Guia de Migração para Codeberg/Forgejo

**Associação MILK - Movimento de Intervenções e Linguagens Kulturais e Arte**
**NIPC: 518 706 451**
**Lisboa, Portugal**
**Licença: EUPL-1.2**

---

## 🚀 **Introdução**

Este guia fornece **instruções detalhadas** para migrar os repositórios da **Associação MILK** do **GitHub** para o **Codeberg/Forgejo**, garantindo:
✅ **Soberania digital** (dados hospedados na UE)
✅ **Conformidade com RGPD** (proteção de dados pessoais)
✅ **Interoperabilidade** (integração com sistemas europeus)
✅ **Elegibilidade acadêmica** (DOIs, ORCID, ROR)
✅ **Financiabilidade** (conformidade com chamadas de financiamento da UE)

---

## 🎯 **Porquê Migrar para Codeberg/Forgejo?**

### **1. Vantagens do Codeberg**
| **Característica**               | **GitHub**                          | **Codeberg**                          | **Vantagem**                                                                 |
|----------------------------------|-------------------------------------|---------------------------------------|-----------------------------------------------------------------------------|
| **Localização**                  | Servidores nos EUA (Microsoft)      | Servidores na UE (Alemanha)          | **Conformidade com RGPD** (dados na UE).                                  |
| **Licença**                      | Software proprietário               | **100% Open-Source (GPLv3)**           | **Transparência e soberania digital**.                                    |
| **Modelo de Negócio**             | Freemium (pago para repositórios privados) | **Gratuito para todos** (doações) | **Sem custos ocultos**.                                                   |
| **Privacidade**                   | Coleta de dados para publicidade    | **Sem rastreamento, sem anúncios**     | **Proteção de dados pessoais**.                                           |
| **Conformidade Legal**           | Sujeito a leis dos EUA (CLOUD Act)   | **Sujeito a leis da UE (RGPD, AI Act)** | **Alinhamento com regulamentações europeias**.                          |
| **Integração com ORCID/ROR**      | Sim                                  | **Sim (em desenvolvimento)**           | **Elegibilidade acadêmica**.                                               |
| **Suporte a DOIs**                | Sim (via Zenodo)                     | **Sim (via DataCite)**                | **Citação acadêmica**.                                                    |
| **Interoperabilidade**            | API proprietária                     | **API aberta (Forgejo)**               | **Integração com sistemas abertos**.                                     |
| **Comunidade**                    | Global (foco em empresas)            | **Foco em projetos éticos e open-source** | **Alinhamento com valores da Associação MILK**.                          |

### **2. Vantagens do Forgejo**
- **Auto-hospedado**: Pode ser instalado em **servidores próprios** (ex: na infraestrutura da Associação MILK).
- **100% Open-Source**: Sem dependências de software proprietário.
- **Conformidade com RGPD**: Dados sob controle total da Associação MILK.
- **Integração com Codeberg**: O Codeberg utiliza o Forgejo como base.

---

## 📋 **Pré-Requisitos para Migração**

### **1. Conta no Codeberg**
1. **Criar uma conta pessoal** em [https://codeberg.org](https://codeberg.org):
   - Clique em **"Sign Up"** no canto superior direito.
   - Preencha o formulário com os seus dados (nome, email, username).
   - **Recomendação:** Use o mesmo **username** do GitHub para consistência.

2. **Criar uma organização para a Associação MILK**:
   - Após fazer login, clique em **"New Organization"** no menu superior.
   - **Nome:** `milkivc` (ou outro nome disponível).
   - **Descrição:** "Associação MILK - Movimento de Intervenções e Linguagens Kulturais e Arte"
   - **Website:** [https://github.com/milkivc](https://github.com/milkivc)
   - **Email:** `nuno@associacaomilk.pt` (ou outro email oficial).

3. **Configurar a organização**:
   - Adicione **membros** (Nuno Filipe, Eduardo Mauricio, etc.).
   - Defina **permissões** (Admin, Maintainer, Member).
   - Ative **repositórios públicos por padrão**.

### **2. Ferramentas Necessárias**
| **Ferramenta**               | **Descrição**                                                                 | **Link**                                                                 | **Instalação**                                                                 |
|------------------------------|-----------------------------------------------------------------------------|--------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| **Git**                      | Sistema de controle de versões.                              | [https://git-scm.com/](https://git-scm.com/)                          | `sudo apt install git` (Linux) / `brew install git` (macOS)               |
| **GitHub CLI (`gh`)**         | Interface de linha de comandos para o GitHub.              | [https://cli.github.com/](https://cli.github.com/)                  | `sudo apt install gh` (Linux) / `brew install gh` (macOS)                 |
| **Codeberg CLI (`cb`)**       | Interface de linha de comandos para o Codeberg.             | [https://codeberg.org/Codeberg/Codeberg-CLI](https://codeberg.org/Codeberg/Codeberg-CLI) | `pip install codeberg-cli`                                                   |
| **Forgejo CLI (`forgejo`)**   | Interface de linha de comandos para o Forgejo.              | [https://forgejo.org/](https://forgejo.org/)                          | `pip install forgejo-cli`                                                   |
| **`git-remote-codeberg`**      | Plugin para interagir com o Codeberg via Git.              | [https://codeberg.org/Codeberg/git-remote-codeberg](https://codeberg.org/Codeberg/git-remote-codeberg) | `pip install git-remote-codeberg`                                           |

### **3. Chaves SSH**
1. **Gerar uma chave SSH** (se ainda não tiver):
   ```bash
   ssh-keygen -t ed25519 -C "seu_email@associacaomilk.pt"
   ```
   - **Localização:** `~/.ssh/id_ed25519` (chave privada) e `~/.ssh/id_ed25519.pub` (chave pública).

2. **Adicionar a chave SSH ao Codeberg**:
   - Acesse [https://codeberg.org/user/settings/keys](https://codeberg.org/user/settings/keys).
   - Clique em **"Add Key"**.
   - **Título:** `Laptop - Nuno Filipe` (ou outro identificador).
   - **Chave:** Cole o conteúdo de `~/.ssh/id_ed25519.pub`.
   - Clique em **"Add Key"**.

3. **Testar a conexão SSH**:
   ```bash
   ssh -T git@codeberg.org
   ```
   - **Resultado esperado:** `Hello, [username]! You've successfully authenticated...`

---

## 🔄 **Estratégias de Migração**

### **1. Espelhamento (Mirroring)**
**Recomendado para:** Repositórios que **permanecerão no GitHub** mas também serão **espelhados no Codeberg**.

#### **Vantagens:**
- **Sem downtime** (repositórios continuam disponíveis no GitHub).
- **Sincronização automática** (alterações no GitHub são refletidas no Codeberg).
- **Backup** (cópia de segurança na UE).

#### **Desvantagens:**
- **Duplicação de esforço** (manutenção em duas plataformas).
- **Possível divergência** (se não for sincronizado corretamente).

#### **Passos para Espelhamento:**
1. **Criar um repositório vazio no Codeberg**:
   - Acesse [https://codeberg.org/milkivc](https://codeberg.org/milkivc).
   - Clique em **"New Repository"**.
   - **Nome:** Mesmo nome do repositório no GitHub (ex: `atlas-datasets`).
   - **Descrição:** Mesma descrição do GitHub.
   - **Visibilidade:** **Público** (ou Privado, se aplicável).
   - **Inicializar com README:** **Não** (vamos espelhar o repositório existente).

2. **Adicionar o Codeberg como remote no GitHub**:
   ```bash
   cd /caminho/para/o/repositorio
   git remote add codeberg git@codeberg.org:milkivc/atlas-datasets.git
   ```

3. **Enviar todas as branches para o Codeberg**:
   ```bash
   git push --all codeberg
   git push --tags codeberg
   ```

4. **Automatizar a sincronização (opcional)**:
   - **GitHub Actions:** Criar um workflow para **empurrar automaticamente** alterações para o Codeberg.
   - **Exemplo de workflow:** [`.github/workflows/mirror-to-codeberg.yml`](https://github.com/milkivc/atlas-datasets/blob/master/.github/workflows/mirror-to-codeberg.yml)
     ```yaml
     name: Mirror to Codeberg
     on:
       push:
         branches: [ main, master ]
       pull_request:
         branches: [ main, master ]
     jobs:
       mirror:
         runs-on: ubuntu-latest
         steps:
           - uses: actions/checkout@v4
             with:
               fetch-depth: 0
           - name: Push to Codeberg
             run: |
               git remote add codeberg git@codeberg.org:milkivc/${{ github.repository.name }}.git
               git push --all codeberg
               git push --tags codeberg
     ```

---

### **2. Migração Completa**
**Recomendado para:** Repositórios que **serão movidos permanentemente** para o Codeberg.

#### **Vantagens:**
- **Centralização** (apenas uma plataforma para gerir).
- **Soberania digital** (dados 100% na UE).
- **Conformidade total com RGPD**.

#### **Desvantagens:**
- **Downtime temporário** (repositórios não estarão disponíveis durante a migração).
- **Redirecionamento de links** (necessário atualizar todos os links para o Codeberg).

#### **Passos para Migração Completa:**
1. **Criar um repositório vazio no Codeberg** (mesmo processo do espelhamento).

2. **Clonar o repositório do GitHub localmente**:
   ```bash
   git clone --mirror https://github.com/milkivc/atlas-datasets.git
   cd atlas-datasets.git
   ```

3. **Enviar para o Codeberg**:
   ```bash
   git remote set-url origin git@codeberg.org:milkivc/atlas-datasets.git
   git push --mirror
   ```

4. **Atualizar o repositório local**:
   ```bash
   cd ..
   rm -rf atlas-datasets.git
   git clone git@codeberg.org:milkivc/atlas-datasets.git
   cd atlas-datasets
   ```

5. **Redirecionar o GitHub para o Codeberg**:
   - **Opção 1:** Deletar o repositório no GitHub e **criar um redirect** no README.
     ```markdown
     # 🚨 Repositório Movido para Codeberg 🚨
     
     Este repositório foi migrado para o **Codeberg** para garantir conformidade com o RGPD e soberania digital.
     
     **Novo endereço:** [https://codeberg.org/milkivc/atlas-datasets](https://codeberg.org/milkivc/atlas-datasets)
     
     **Porquê?**
     - Dados hospedados na **União Europeia** (conformidade com RGPD).
     - **100% Open-Source** (sem dependências de software proprietário).
     - **Sem rastreamento ou anúncios** (proteção de dados pessoais).
     ```
   - **Opção 2:** Usar o **GitHub Pages** para redirecionar automaticamente.
     - Crie um ficheiro `index.html` com:
       ```html
       <!DOCTYPE html>
       <html>
         <head>
           <meta http-equiv="refresh" content="0; url=https://codeberg.org/milkivc/atlas-datasets" />
           <title>Redirecionando para Codeberg...</title>
         </head>
         <body>
           <p>Redirecionando para <a href="https://codeberg.org/milkivc/atlas-datasets">Codeberg</a>...</p>
         </body>
       </html>
       ```
     - Ative o **GitHub Pages** nas configurações do repositório.

6. **Atualizar todos os links**:
   - **Documentação:** Atualize todos os links nos ficheiros `README.md`, `CITATION.cff`, etc.
   - **Metadados:** Atualize os campos `url`, `codeRepository`, etc. nos ficheiros de metadados.
   - **Sites externos:** Atualize links em websites, publicações, etc.

---

### **3. Migração com Forgejo Auto-Hospedado**
**Recomendado para:** Associação MILK que queira **controle total** sobre a infraestrutura.

#### **Vantagens:**
- **Soberania digital absoluta** (dados em servidores próprios).
- **Conformidade total com RGPD** (dados sob controle da Associação).
- **Sem dependências externas** (nenhum serviço de terceiros).

#### **Desvantagens:**
- **Custo de infraestrutura** (servidores, manutenção).
- **Complexidade técnica** (requer conhecimento de administração de sistemas).

#### **Passos para Auto-Hospedagem:**
1. **Instalar o Forgejo**:
   - **Requisitos:**
     - Servidor com **Linux (Ubuntu/Debian recomendado)**.
     - **4 GB de RAM** (mínimo).
     - **50 GB de disco** (para repositórios).
     - **Domínio** (ex: `git.associacaomilk.pt`).
   - **Instalação:**
     ```bash
     # Instalar dependências
     sudo apt update && sudo apt install -y git curl wget
     
     # Baixar e instalar o Forgejo
     wget https://forgejo.org/releases/latest/download
     tar -xzf download
     cd forgejo-*/
     
     # Configurar e iniciar
     ./forgejo install --data /var/lib/forgejo --domain git.associacaomilk.pt
     sudo systemctl start forgejo
     sudo systemctl enable forgejo
     ```

2. **Configurar o Forgejo**:
   - Acesse `http://git.associacaomilk.pt` no navegador.
   - **Primeiro login:**
     - **Username:** `root`
     - **Password:** (definida durante a instalação).
   - **Criar organização:**
     - Clique em **"New Organization"**.
     - **Nome:** `milkivc`
     - **Descrição:** "Associação MILK - Movimento de Intervenções e Linguagens Kulturais e Arte"

3. **Migrar repositórios**:
   - Siga os mesmos passos da **Migração Completa**, mas usando o endereço do seu Forgejo:
     ```bash
     git remote set-url origin git@git.associacaomilk.pt:milkivc/atlas-datasets.git
     git push --mirror
     ```

4. **Configurar backup automático**:
   - **Script de backup:**
     ```bash
     #!/bin/bash
     # Backup diário dos repositórios Forgejo
     BACKUP_DIR="/backup/forgejo"
     DATE=$(date +%Y-%m-%d)
     
     mkdir -p "$BACKUP_DIR/$DATE"
     cd /var/lib/forgejo
     
     # Backup dos repositórios
     tar -czf "$BACKUP_DIR/$DATE/forgejo-repos.tar.gz" gitea/repositories
     
     # Backup do banco de dados (PostgreSQL)
     sudo -u postgres pg_dump -Fc forgejo > "$BACKUP_DIR/$DATE/forgejo-db.dump"
     
     # Backup das configurações
     tar -czf "$BACKUP_DIR/$DATE/forgejo-config.tar.gz" gitea/conf
     
     # Remover backups antigos (mais de 30 dias)
     find "$BACKUP_DIR" -type d -mtime +30 -exec rm -rf {} \;
     ```
   - **Agendar backup:**
     ```bash
     sudo crontab -e
     ```
     Adicione:
     ```cron
     0 2 * * * /caminho/para/o/script/backup-forgejo.sh
     ```

---

## 🔧 **Configuração Pós-Migração**

### **1. Configurar Webhooks**
**Objetivo:** Automatizar a **sincronização entre plataformas** (ex: GitHub → Codeberg).

#### **Passos:**
1. **No GitHub**:
   - Acesse **Settings → Webhooks** do repositório.
   - Clique em **"Add webhook"**.
   - **Payload URL:** `https://codeberg.org/milkivc/atlas-datasets/api/v1/repos/milkivc/atlas-datasets/mirror-sync` (verificar API do Codeberg).
   - **Content Type:** `application/json`
   - **Secret:** (gerar uma chave secreta).
   - **Events:** `Push`, `Pull Request`, `Issue Comment`.
   - Clique em **"Add webhook"**.

2. **No Codeberg**:
   - Acesse **Settings → Webhooks** do repositório.
   - Configure um webhook para **notificar o GitHub** (opcional).

### **2. Configurar CI/CD no Codeberg**
**Objetivo:** Automatizar **validação de metadados, testes e deployments**.

#### **Passos:**
1. **Criar um ficheiro de workflow**:
   - No Codeberg, crie o ficheiro `.woodpecker.yml` (o Codeberg usa **Woodpecker CI** em vez de GitHub Actions).
   - **Exemplo:**
     ```yaml
     pipeline:
       validate-metadata:
         image: alpine
         commands:
           - apk add --no-cache git curl jq
           - curl -s https://raw.githubusercontent.com/citation-file-format/cff-validator/main/cff-validator.py -o cff-validator.py
           - python cff-validator.py CITATION.cff
           - jq empty codemeta.json
           - jq empty datacite.json
     ```

2. **Ativar o Woodpecker**:
   - Acesse **Settings → CI/CD** do repositório.
   - Ative o **Woodpecker CI**.

### **3. Configurar DOIs com DataCite**
**Objetivo:** Garantir que todos os datasets tenham **DOIs para citação acadêmica**.

#### **Passos:**
1. **Registrar-se na DataCite**:
   - Acesse [https://www.datacite.org/](https://www.datacite.org/) e crie uma conta.
   - **Organização:** Associação MILK.
   - **Prefixo DOI:** Solicite um prefixo (ex: `10.5281`).

2. **Registrar DOIs para datasets**:
   - **Manual:**
     - Acesse o **painel da DataCite**.
     - Clique em **"Register DOI"**.
     - Preencha os metadados (título, autores, descrição, etc.).
     - **URL:** `https://codeberg.org/milkivc/atlas-datasets`
     - **Schema:** `DataCite 4.4`
     - Clique em **"Register"**.
   - **Automático (API):**
     ```bash
     curl -X POST https://api.datacite.org/dois \
       -H "Content-Type: application/vnd.api+json" \
       -H "Authorization: Bearer YOUR_DATACITE_TOKEN" \
       -d '{
         "data": {
           "type": "dois",
           "attributes": {
             "doi": "10.5281/zenodo.XXXXXXX",
             "titles": [{"title": "Atlas Vivo MILK - Datasets"}],
             "creators": [
               {"name": "Nuno Filipe Fernandes Vieira Cabral e Araujo", "nameIdentifiers": [{"nameIdentifier": "0009-0009-1781-4020", "nameIdentifierScheme": "ORCID"}]},
               {"name": "Eduardo Mauricio Vieira Cabral e Araujo", "nameIdentifiers": [{"nameIdentifier": "0009-0007-6892-6570", "nameIdentifierScheme": "ORCID"}]}
             ],
             "publisher": "Associacao MILK",
             "publicationYear": "2026",
             "resourceType": {"resourceType": "Dataset"},
             "url": "https://codeberg.org/milkivc/atlas-datasets"
           }
         }
       }'
     ```

3. **Atualizar metadados**:
   - Adicione o DOI aos ficheiros `CITATION.cff`, `datacite.json`, `codemeta.json`, etc.
   - Exemplo:
     ```yaml
     # CITATION.cff
     identifiers:
       - type: "doi"
         value: "10.5281/zenodo.XXXXXXX"
     ```

### **4. Configurar ORCID e ROR**
**Objetivo:** Garantir **identificação única** para investigadores e organização.

#### **Passos:**
1. **ORCID para Investigadores**:
   - **Nuno Filipe:** [https://orcid.org/0009-0009-1781-4020](https://orcid.org/0009-0009-1781-4020)
   - **Eduardo Mauricio:** [https://orcid.org/0009-0007-6892-6570](https://orcid.org/0009-0007-6892-6570)
   - **Adicionar ao perfil:**
     - **Emprego:** Associação MILK.
     - **Publicações:** Adicione os repositórios e datasets.

2. **ROR para Organização**:
   - **ROR ID:** [https://ror.org/05k9p4d32](https://ror.org/05k9p4d32)
   - **Atualizar perfil:**
     - **Nome:** Associação MILK - Movimento de Intervenções e Linguagens Kulturais e Arte
     - **Website:** [https://codeberg.org/milkivc](https://codeberg.org/milkivc)
     - **Localização:** Lisboa, Portugal

---

## 📊 **Verificação Pós-Migração**

### **1. Checklist de Verificação**

| **Item**                          | **Verificado?** | **Notas** |
|-----------------------------------|-----------------|-----------|
| Repositório clonado com sucesso   | ☐               |           |
| Todas as branches sincronizadas   | ☐               |           |
| Todas as tags sincronizadas       | ☐               |           |
| Metadados atualizados (URLs)      | ☐               |           |
| CI/CD configurado                  | ☐               |           |
| Webhooks configurados             | ☐               |           |
| DOIs registados                   | ☐               |           |
| ORCID/ROR vinculados              | ☐               |           |
| Links atualizados (README, etc.)   | ☐               |           |
| Backup configurado                | ☐               |           |

### **2. Testes de Integração**

#### **2.1. Teste de Acesso**
```bash
# Testar clone do repositório no Codeberg
git clone git@codeberg.org:milkivc/atlas-datasets.git
cd atlas-datasets

# Verificar branches
git branch -a

# Verificar tags
git tag -l
```

#### **2.2. Teste de Sincronização**
```bash
# Fazer uma alteração local
 echo "Teste de sincronização" >> TESTE.md
 git add TESTE.md
 git commit -m "Teste de sincronização"
 git push origin main

# Verificar se a alteração aparece no Codeberg
```

#### **2.3. Teste de CI/CD**
- **No Codeberg:**
  - Faça um **push** para o repositório.
  - Verifique se o **Woodpecker CI** executa o workflow.
  - Verifique os **logs** para garantir que não há erros.

#### **2.4. Teste de DOI**
- Acesse o **DOI registado** (ex: [https://doi.org/10.5281/zenodo.XXXXXXX](https://doi.org/10.5281/zenodo.XXXXXXX)).
- Verifique se **redireciona para o repositório no Codeberg**.

#### **2.5. Teste de ORCID/ROR**
- Acesse o **perfil ORCID** de um investigador (ex: [https://orcid.org/0009-0009-1781-4020](https://orcid.org/0009-0009-1781-4020)).
- Verifique se o repositório está listado nas **publicações**.
- Acesse o **perfil ROR** da Associação MILK ([https://ror.org/05k9p4d32](https://ror.org/05k9p4d32)).
- Verifique se os repositórios estão vinculados.

---

## 📅 **Cronograma de Migração**

| **Fase** | **Ação**                                                                 | **Prazo**       | **Responsável**               | **Estado**      |
|----------|--------------------------------------------------------------------------|-----------------|--------------------------------|-----------------|
| 1        | Criar organização no Codeberg                                           | 2026-07-26      | Nuno Filipe                   | ✅ Concluído    |
| 2        | Configurar chaves SSH e ferramentas                                     | 2026-07-27      | Eduardo Mauricio               | ⏳ Em Andamento  |
| 3        | Espelhar repositórios principais (atlas-datasets, atlas-docs, etc.)     | 2026-07-30      | Nuno Filipe / Eduardo Mauricio | ⏳ Planeado      |
| 4        | Configurar CI/CD (Woodpecker) nos repositórios espelhados              | 2026-08-05      | Eduardo Mauricio               | ⏳ Planeado      |
| 5        | Registrar DOIs para todos os datasets na DataCite                       | 2026-08-31      | Eduardo Mauricio               | ⏳ Planeado      |
| 6        | Atualizar metadados (URLs, DOIs, ORCID, ROR)                            | 2026-09-15      | Nuno Filipe                   | ⏳ Planeado      |
| 7        | Migrar repositórios restantes                                          | 2026-09-30      | Nuno Filipe / Eduardo Mauricio | ⏳ Planeado      |
| 8        | Configurar backup automático (Forgejo auto-hospedado)                  | 2026-10-31      | Eduardo Mauricio               | ⏳ Planeado      |
| 9        | Verificar conformidade com RGPD, AI Act, INSPIRE                       | 2026-11-30      | Nuno Filipe                   | ⏳ Planeado      |
| 10       | Publicar anúncio oficial da migração                                   | 2026-12-01      | Nuno Filipe / Eduardo Mauricio | ⏳ Planeado      |

---

## 📞 **Suporte e Contatos**

### **1. Suporte Técnico**
| **Área**               | **Responsável**               | **Email**                     | **ORCID**                          |
|------------------------|--------------------------------|-------------------------------|------------------------------------|
| **Migração**           | Nuno Filipe                    | nuno@associacaomilk.pt        | [0009-0009-1781-4020](https://orcid.org/0009-0009-1781-4020) |
| **Metadados**          | Eduardo Mauricio               | eduardo@associacaomilk.pt     | [0009-0007-6892-6570](https://orcid.org/0009-0007-6892-6570) |
| **CI/CD**              | Eduardo Mauricio               | eduardo@associacaomilk.pt     | [0009-0007-6892-6570](https://orcid.org/0009-0007-6892-6570) |
| **DOIs**               | Eduardo Mauricio               | eduardo@associacaomilk.pt     | [0009-0007-6892-6570](https://orcid.org/0009-0007-6892-6570) |
| **Conformidade Legal** | Nuno Filipe                    | nuno@associacaomilk.pt        | [0009-0009-1781-4020](https://orcid.org/0009-0009-1781-4020) |

### **2. Recursos de Suporte**
- **Documentação do Codeberg:** [https://docs.codeberg.org/](https://docs.codeberg.org/)
- **Fórum do Codeberg:** [https://forum.codeberg.org/](https://forum.codeberg.org/)
- **Documentação do Forgejo:** [https://forgejo.org/docs/](https://forgejo.org/docs/)
- **Suporte da DataCite:** [https://support.datacite.org/](https://support.datacite.org/)
- **Suporte do ORCID:** [https://support.orcid.org/](https://support.orcid.org/)

---

## 📚 **Recursos Adicionais**

### **1. Documentação Relacionada**
- [INTEROPERABILITY.md](https://github.com/milkivc/atlas-datasets/blob/master/INTEROPERABILITY.md) - Guia de interoperabilidade.
- [LEGAL.md](https://github.com/milkivc/atlas-datasets/blob/master/LEGAL.md) - Conformidade jurídica.
- [GOVERNANCE.md](https://github.com/milkivc/atlas-datasets/blob/master/GOVERNANCE.md) - Estrutura de governança.
- [FUNDING.yml](https://github.com/milkivc/atlas-datasets/blob/master/FUNDING.yml) - Informações de financiamento.

### **2. Links Úteis**
- [Codeberg](https://codeberg.org/) - Plataforma de hospedagem de código baseada na UE.
- [Forgejo](https://forgejo.org/) - Software de hospedagem de código 100% open-source.
- [DataCite](https://www.datacite.org/) - Registo de DOIs para datasets.
- [ORCID](https://orcid.org/) - Identificadores únicos para investigadores.
- [ROR](https://ror.org/) - Identificadores únicos para organizações de investigação.
- [OpenAIRE](https://www.openaire.eu/) - Infraestrutura de ciência aberta da UE.
- [INSPIRE](https://inspire.ec.europa.eu/) - Diretiva da UE para dados geoespaciais.

---

## 🔒 **Segurança e Conformidade**

### **1. Segurança Durante a Migração**
- **Chaves SSH:** Garanta que as chaves SSH são **seguras e não compartilhadas**.
- **Tokens de API:** Não compartilhe **tokens de API** (GitHub, DataCite, etc.).
- **Backups:** Faça **backups completos** antes de qualquer migração.
- **Verificação:** Verifique **todos os dados** após a migração.

### **2. Conformidade com RGPD**
- **Dados Pessoais:** Garanta que **nenhum dado pessoal** é migrado sem consentimento.
- **Anonimização:** Anonimize dados sensíveis antes da migração.
- **Notificação:** Notifique os utilizadores sobre a **mudança de plataforma**.

### **3. Conformidade com AI Act**
- **Sistemas de IA:** Se a Associação MILK utilizar **sistemas de IA**, garanta que estão em conformidade com o **AI Act**.
- **Transparência:** Documente todos os **modelos de IA** utilizados.
- **Supervisão Humana:** Garanta que os sistemas de IA têm **supervisão humana**.

---

**© 2026 Associação MILK - Movimento de Intervenções e Linguagens Kulturais e Arte**
**Todos os direitos reservados.**
**Licença: [EUPL-1.2](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12)**

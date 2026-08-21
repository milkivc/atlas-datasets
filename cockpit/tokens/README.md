# 🔑 TOKENS - Configuração de Autenticação

**Associação MILK - Movimento de Intervenções e Linguagens Kulturais e Arte**
**Versão:** 1.0.0
**Data:** 2026-07-26
**Licença:** EUPL-1.2

---

## ⚠️ **AVISO IMPORTANTE**

**NUNCA COMPARTILHE ESTES TOKENS!**
- Estes ficheiros **NÃO DEVEM** ser versionados no Git
- Adicione esta pasta ao `.gitignore`:
  ```gitignore
  cockpit/tokens/
  *.token.txt
  *.secret
  ```
- **Nunca faça commit** destes ficheiros
- Use **variáveis de ambiente** em produção

---

## 📁 **ESTRUTURA DE TOKENS**

```
cockpit/tokens/
├── README.md                     # Este ficheiro
├── github_token.txt              # Token do GitHub (Personal Access Token)
├── codeberg_token.txt            # Token do Codeberg (Personal Access Token)
├── datacite_token.txt            # Token da DataCite (API Token)
├── orcid_token.txt               # Token do ORCID (API Token)
└── openaire_token.txt            # Token do OpenAIRE (API Token)
```

---

## 🔑 **TOKENS NECESSÁRIOS**

### **1. GitHub Personal Access Token (PAT)**

#### **Onde Obter:**
1. Acesse [https://github.com/settings/tokens](https://github.com/settings/tokens)
2. Clique em **"Generate new token"**
3. **Token name:** `MILK Cockpit Integration`
4. **Expiration:** `No expiration` (ou 90 dias, se preferir)
5. **Scopes (Permissões):**
   - [x] **repo** (Full control of private repositories)
   - [x] **admin:repo_hook** (Manage repository webhooks)
   - [x] **workflow** (Update GitHub Action workflows)
   - [x] **read:org** (Read organization and team membership)
   - [x] **read:user** (Read user profile)
6. Clique em **"Generate token"**
7. **COPIE O TOKEN GERADO** (ele só será mostrado uma vez!)

#### **Como Configurar:**
1. Abra `cockpit/tokens/github_token.txt`
2. **Substitua o conteúdo** pelo token copiado
3. **Salve o ficheiro**

#### **Exemplo de Token (SIMULADO - SUBSTITUIR PELO REAL):**
```
github_pat_11B234567890abcdef1234567890abcdef1234567890
```

#### **Como Testar:**
```bash
# Testar autenticação com a API do GitHub
curl -H "Authorization: token $(cat cockpit/tokens/github_token.txt)" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user
```
**Resultado esperado:** Informações do seu perfil GitHub

---

### **2. Codeberg Personal Access Token (PAT)**

#### **Onde Obter:**
1. Acesse [https://codeberg.org/user/settings/applications](https://codeberg.org/user/settings/applications)
2. Clique em **"Generate new token"**
3. **Token name:** `MILK Cockpit Integration`
4. **Scopes (Permissões):**
   - [x] **repo** (Full control of repositories)
   - [x] **admin:repo_hook** (Manage repository webhooks)
5. Clique em **"Generate token"**
6. **COPIE O TOKEN GERADO**

#### **Como Configurar:**
1. Abra `cockpit/tokens/codeberg_token.txt`
2. **Substitua o conteúdo** pelo token copiado
3. **Salve o ficheiro**

#### **Exemplo de Token (SIMULADO - SUBSTITUIR PELO REAL):**
```
cb_pat_11B234567890abcdef1234567890abcdef1234567890
```

#### **Como Testar:**
```bash
# Testar autenticação com a API do Codeberg
curl -H "Authorization: token $(cat cockpit/tokens/codeberg_token.txt)" \
  https://codeberg.org/api/v1/user
```
**Resultado esperado:** Informações do seu perfil Codeberg

---

### **3. DataCite API Token**

#### **Onde Obter:**
1. **Registe-se** em [https://www.datacite.org/](https://www.datacite.org/)
   - Clique em **"Register"** no canto superior direito
   - Preencha o formulário com os dados da **Associação MILK**
2. **Solicite um prefixo DOI** (ex: `10.5281`)
   - Acesse [https://www.datacite.org/services/dois.html](https://www.datacite.org/services/dois.html)
   - Clique em **"Request a DOI Prefix"**
   - **Organization:** Associação MILK
   - **Prefix:** (Deixe em branco para atribuir automaticamente)
   - **Contact:** nuno@associacaomilk.pt
3. **Obtenha o API Token**
   - Após aprovação, acesse [https://www.datacite.org/user](https://www.datacite.org/user)
   - Clique em **"API Tokens"**
   - Clique em **"Generate new token"**
   - **Token name:** `MILK Cockpit Integration`
   - **Scopes:**
     - [x] **doi:create**
     - [x] **doi:read**
     - [x] **doi:update**
   - Clique em **"Generate token"**
   - **COPIE O TOKEN GERADO**

#### **Como Configurar:**
1. Abra `cockpit/tokens/datacite_token.txt`
2. **Substitua o conteúdo** pelo token copiado
3. **Salve o ficheiro**

#### **Exemplo de Token (SIMULADO - SUBSTITUIR PELO REAL):**
```
DataCite.MILK.1234567890abcdef1234567890abcdef
```

#### **Como Testar:**
```bash
# Testar autenticação com a API da DataCite
curl -H "Authorization: Bearer $(cat cockpit/tokens/datacite_token.txt)" \
  https://api.datacite.org/dois
```
**Resultado esperado:** Lista de DOIs registados (ou erro 404 se não houver DOIs)

---

### **4. ORCID API Token**

#### **Onde Obter:**
1. **Registe-se** em [https://orcid.org/](https://orcid.org/)
   - Se já tiver uma conta ORCID, faça login
2. **Acesse as Developer Tools**
   - Acesse [https://orcid.org/developer-tools](https://orcid.org/developer-tools)
3. **Registe uma Aplicação**
   - Clique em **"Register a new application"**
   - **Application name:** `MILK Cockpit Integration`
   - **Website:** [https://github.com/milkivc](https://github.com/milkivc)
   - **Redirect URI:** `https://github.com/milkivc/cockpit/auth/callback` (ou qualquer URL válida)
   - **Description:** "Integração com o Cockpit da Associação MILK para gestão de publicações"
4. **Obtenha o API Token**
   - Após registo, será redirecionado para uma página com:
     - **Client ID:** (ex: `APP-1234567890ABCDEF`)
     - **Client Secret:** (ex: `12345678-1234-1234-1234-1234567890AB`)
   - **COPIE AMBOS** (Client ID e Client Secret)

#### **Como Configurar:**
1. Abra `cockpit/tokens/orcid_token.txt`
2. **Formato do ficheiro:**
   ```
   CLIENT_ID=APP-1234567890ABCDEF
   CLIENT_SECRET=12345678-1234-1234-1234-1234567890AB
   ```
3. **Substitua** `CLIENT_ID` e `CLIENT_SECRET` pelos valores reais
4. **Salve o ficheiro**

#### **Exemplo de Token (SIMULADO - SUBSTITUIR PELO REAL):**
```
CLIENT_ID=APP-1234567890ABCDEF
CLIENT_SECRET=12345678-1234-1234-1234-1234567890AB
```

#### **Como Testar:**
```bash
# Obter um token de acesso (OAuth2)
CLIENT_ID=$(grep "CLIENT_ID" cockpit/tokens/orcid_token.txt | cut -d'=' -f2)
CLIENT_SECRET=$(grep "CLIENT_SECRET" cockpit/tokens/orcid_token.txt | cut -d'=' -f2)

# Solicitar token de acesso
RESPONSE=$(curl -s -X POST \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=$CLIENT_ID&client_secret=$CLIENT_SECRET&grant_type=client_credentials&scope=/read-limited" \
  https://orcid.org/oauth/token)

ACCESS_TOKEN=$(echo $RESPONSE | jq -r '.access_token')
echo "Access Token: $ACCESS_TOKEN"

# Testar autenticação
curl -H "Authorization: Bearer $ACCESS_TOKEN" \
  https://api.orcid.org/v3.0/0009-0009-1781-4020/person
```
**Resultado esperado:** Informações do perfil ORCID

---

### **5. OpenAIRE API Token (Opcional)**

#### **Onde Obter:**
1. **Contate o OpenAIRE** em [https://www.openaire.eu/support](https://www.openaire.eu/support)
2. **Solicite acesso à API**
   - **Organization:** Associação MILK
   - **Use Case:** Indexação de publicações e datasets
   - **Contact:** nuno@associacaomilk.pt
3. **Obtenha o API Token**
   - Após aprovação, receberá um token por email

#### **Como Configurar:**
1. Abra `cockpit/tokens/openaire_token.txt`
2. **Substitua o conteúdo** pelo token recebido
3. **Salve o ficheiro**

#### **Exemplo de Token (SIMULADO - SUBSTITUIR PELO REAL):**
```
openaire_api_1234567890abcdef1234567890abcdef
```

---

## 🔒 **MELHORES PRÁTICAS DE SEGURANÇA**

### **1. Armazenamento Seguro de Tokens**
- **Nunca armazene tokens em ficheiros versionados** (Git)
- **Use variáveis de ambiente** em produção:
  ```bash
  export GITHUB_TOKEN=$(cat cockpit/tokens/github_token.txt)
  export DATACITE_TOKEN=$(cat cockpit/tokens/datacite_token.txt)
  ```
- **Use um gestor de segredos** (ex: HashiCorp Vault, AWS Secrets Manager)

### **2. Rotação de Tokens**
- **GitHub PAT:** Renove a cada **90 dias** (ou defina sem expiração)
- **DataCite Token:** Renove a cada **1 ano**
- **ORCID Token:** Renove a cada **6 meses**

### **3. Permissões Mínimas**
- **Dê apenas as permissões necessárias** a cada token
- **Evite tokens com permissões de admin** a menos que seja estritamente necessário

### **4. Auditoria**
- **Monitore o uso dos tokens** (logs de acesso)
- **Revogue tokens não utilizados**
- **Verifique regularmente** as permissões dos tokens

---

## 🚨 **O QUE FAZER SE UM TOKEN FOR COMPROMETIDO?**

1. **Revogue o token imediatamente**
   - GitHub: [https://github.com/settings/tokens](https://github.com/settings/tokens)
   - Codeberg: [https://codeberg.org/user/settings/applications](https://codeberg.org/user/settings/applications)
   - DataCite: [https://www.datacite.org/user](https://www.datacite.org/user)
   - ORCID: [https://orcid.org/developer-tools](https://orcid.org/developer-tools)

2. **Gere um novo token** com as mesmas permissões

3. **Atualize o ficheiro de token** no cockpit

4. **Verifique os logs** para identificar acesso não autorizado

---

## 📚 **DOCUMENTAÇÃO RELACIONADA**

- [QUICK_START.md](../docs/QUICK_START.md) - Guia de início rápido
- [API_DOCUMENTATION.md](../docs/API_DOCUMENTATION.md) - Documentação das APIs
- [TROUBLESHOOTING.md](../docs/TROUBLESHOOTING.md) - Resolução de problemas

---

## 📞 **SUPORTE**

Se tiver problemas com a configuração dos tokens:
- **Nuno Filipe:** nuno@associacaomilk.pt | [ORCID](https://orcid.org/0009-0009-1781-4020)
- **Eduardo Mauricio:** eduardo@associacaomilk.pt | [ORCID](https://orcid.org/0009-0007-6892-6570)

---

**© 2026 Associação MILK - Movimento de Intervenções e Linguagens Kulturais e Arte**
**Todos os direitos reservados.**
**Licença: [EUPL-1.2](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12)**

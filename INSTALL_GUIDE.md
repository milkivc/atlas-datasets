# 📥 GUIA DE INSTALAÇÃO - ATLAS CONSOLE

## 🎯 COMO INSTALAR E USAR EM QUALQUER DISPOSITIVO

**Versão:** 2.0.0  
**Data:** 26 de Junho de 2026  
**Sistema:** Studio Agent Integration System

---

## 💻 **COMPUTADOR (Windows)**

### **Método 1: Usando o Atalho .bat (Recomendado)**

1. **Baixe os arquivos:**
   - `ATLAS_CONSOLE.bat`
   - `ATLAS_CONSOLE.ps1`
   - `ATLAS_CONSOLE_QUICK.sh`
   - Todos os arquivos da pasta `agent-integration/`

2. **Crie uma pasta:**
   ```
   C:\ATLAS_CONSOLE
   ```

3. **Copie todos os arquivos** para a pasta `C:\ATLAS_CONSOLE`

4. **Execute o atalho:**
   - Dê duplo clique em `ATLAS_CONSOLE.bat`
   - Se pedir permissão, clique em "Sim"

5. **Se o PowerShell não estiver instalado:**
   - Baixe e instale: https://aka.ms/PSWindows
   - Ou execute manualmente:
     ```cmd
     powershell -ExecutionPolicy Bypass -File "C:\ATLAS_CONSOLE\ATLAS_CONSOLE.ps1"
     ```

### **Método 2: Criar Atalho na Área de Trabalho**

1. **Clique com o botão direito** na área de trabalho
2. **Novo → Atalho**
3. **Local do item:**
   ```
   C:\ATLAS_CONSOLE\ATLAS_CONSOLE.bat
   ```
4. **Nome:** ATLAS CONSOLE
5. **Clique em Concluir**

### **Método 3: Executar Diretamente**

```cmd
cd C:\ATLAS_CONSOLE
ATLAS_CONSOLE.bat
```

---

## 🐧 **COMPUTADOR (Linux/Mac)**

### **Método 1: Usando o Console Rápido**

1. **Baixe os arquivos:**
   ```bash
   git clone https://github.com/milkivc/atlas-datasets.git
   cd atlas-datasets
   ```

2. **Torne os arquivos executáveis:**
   ```bash
   chmod +x ATLAS_CONSOLE.sh ATLAS_CONSOLE_QUICK.sh
   ```

3. **Execute o console:**
   ```bash
   ./ATLAS_CONSOLE_QUICK.sh
   ```

### **Método 2: Criar Atalho na Área de Trabalho**

1. **Crie um arquivo de atalho:**
   ```bash
   nano ~/Desktop/ATLAS_CONSOLE.desktop
   ```

2. **Cole este conteúdo:**
   ```ini
   [Desktop Entry]
   Version=1.0
   Type=Application
   Name=ATLAS CONSOLE
   Comment=Sistema de Controle Total - Associação MILK
   Exec=bash -c "cd /caminho/para/atlas-datasets && ./ATLAS_CONSOLE_QUICK.sh"
   Icon=/caminho/para/atlas-datasets/ATLAS_ICON.png
   Terminal=true
   Categories=Utility;Application;
   ```

3. **Torne o atalho executável:**
   ```bash
   chmod +x ~/Desktop/ATLAS_CONSOLE.desktop
   ```

4. **Execute:**
   - Dê duplo clique no ícone ATLAS CONSOLE na área de trabalho

### **Método 3: Adicionar ao PATH**

1. **Adicione ao seu .bashrc ou .zshrc:**
   ```bash
   echo 'export PATH="$PATH:/caminho/para/atlas-datasets"' >> ~/.bashrc
   source ~/.bashrc
   ```

2. **Execute de qualquer lugar:**
   ```bash
   ATLAS_CONSOLE_QUICK.sh
   ```

---

## 📱 **IPAD / CELULAR (iOS/Android)**

### **Método 1: Usando o Arquivo HTML (Recomendado)**

1. **Baixe o arquivo:**
   - `ATLAS_CONSOLE_WEB.html`

2. **Abra no navegador:**
   - Safari (iPad/iPhone)
   - Chrome (Android)

3. **Salve como App:**
   
   **No iPad/iPhone:**
   1. Abra o arquivo no Safari
   2. Toque no ícone de compartilhar (quadrado com seta para cima)
   3. Role para baixo e toque em "Adicionar à Tela Inicial"
   4. Dê um nome: "ATLAS CONSOLE"
   5. Toque em "Adicionar"
   6. Pronto! Você terá um app na tela inicial
   
   **No Android:**
   1. Abra o arquivo no Chrome
   2. Toque nos 3 pontos (menu)
   3. Toque em "Adicionar à tela inicial"
   4. Dê um nome: "ATLAS CONSOLE"
   5. Toque em "Adicionar"
   6. Pronto! Você terá um app na tela inicial

4. **Use o app:**
   - Toque no ícone do ATLAS CONSOLE
   - Navegue pelo menu tocando nos botões
   - Todas as funções estarão disponíveis

### **Método 2: Usando Termux (Android)**

1. **Instale o Termux:**
   - Baixe do Google Play ou F-Droid

2. **Instale dependências:**
   ```bash
   pkg update && pkg upgrade
   pkg install git python curl wget
   ```

3. **Baixe os arquivos:**
   ```bash
   git clone https://github.com/milkivc/atlas-datasets.git
   cd atlas-datasets
   ```

4. **Torne executáveis:**
   ```bash
   chmod +x ATLAS_CONSOLE_QUICK.sh
   ```

5. **Execute:**
   ```bash
   ./ATLAS_CONSOLE_QUICK.sh
   ```

### **Método 3: Usando iSH (iPad/iPhone)**

1. **Instale o iSH:**
   - Baixe do App Store

2. **Instale dependências:**
   ```bash
   apk add git python3 curl
   ```

3. **Baixe os arquivos:**
   ```bash
   git clone https://github.com/milkivc/atlas-datasets.git
   cd atlas-datasets
   ```

4. **Execute:**
   ```bash
   bash ATLAS_CONSOLE_QUICK.sh
   ```

---

## 🌐 **ACESSO REMOTO (Qualquer Dispositivo)**

### **Método 1: Usando GitHub Codespaces**

1. **Acesse:** https://github.com/codespaces
2. **Crie um novo Codespace** com o repositório `milkivc/atlas-datasets`
3. **Execute no terminal:**
   ```bash
   chmod +x ATLAS_CONSOLE_QUICK.sh
   ./ATLAS_CONSOLE_QUICK.sh
   ```

### **Método 2: Usando Replit**

1. **Acesse:** https://replit.com
2. **Crie um novo Repl** (Bash)
3. **Copie os arquivos** para o Repl
4. **Execute:**
   ```bash
   chmod +x ATLAS_CONSOLE_QUICK.sh
   ./ATLAS_CONSOLE_QUICK.sh
   ```

### **Método 3: Usando Google Colab**

1. **Acesse:** https://colab.research.google.com
2. **Crie um novo notebook**
3. **Execute:**
   ```python
   !git clone https://github.com/milkivc/atlas-datasets.git
   %cd atlas-datasets
   !chmod +x ATLAS_CONSOLE_QUICK.sh
   !./ATLAS_CONSOLE_QUICK.sh
   ```

---

## 📋 **RESUMO DOS ARQUIVOS NECESSÁRIOS**

| Arquivo | Descrição | Dispositivo |
|---------|-----------|-------------|
| `ATLAS_CONSOLE.bat` | Atalho Windows | Windows |
| `ATLAS_CONSOLE.ps1` | Console PowerShell | Windows |
| `ATLAS_CONSOLE.sh` | Console Bash Completo | Linux/Mac |
| `ATLAS_CONSOLE_QUICK.sh` | Console Bash Rápido | Linux/Mac/Termux/iSH |
| `ATLAS_CONSOLE_WEB.html` | Console Web | iPad/Celular |
| `agent-integration/` | APIs e scripts | Todos |
| `token-config/.env` | Configuração de tokens | Todos |

---

## 🎯 **COMO USAR DEPOIS DE INSTALAR**

### **No Computador (Windows/Linux/Mac):**
1. Execute o console
2. Digite o número da opção
3. Pressione Enter
4. Siga as instruções

### **No iPad/Celular:**
1. Abra o app ATLAS CONSOLE
2. Toque no botão da função desejada
3. Leia as informações
4. Toque em "Voltar" para retornar

### **Funções Disponíveis:**
- **📊 Dashboard** - Ver status de TUDO
- **💰 Financiamento** - Verificar elegibilidade (10 programas)
- **🔄 Sincronizar** - Sincronizar todas as plataformas
- **🔐 Tokens** - Configurar e validar tokens
- **🚀 APIs** - Ver APIs deployadas
- **📁 Arquivos** - Acessar documentação
- **🎯 Executar Tudo** - Automação completa
- **📝 Relatórios** - Gerar relatórios

---

## 🔧 **SOLUÇÃO DE PROBLEMAS**

### **Problema: PowerShell não encontrado (Windows)**
**Solução:**
1. Baixe e instale: https://aka.ms/PSWindows
2. Ou use o console Linux (WSL)

### **Problema: Permissão negada (Linux/Mac)**
**Solução:**
```bash
chmod +x ATLAS_CONSOLE_QUICK.sh
```

### **Problema: Python não encontrado**
**Solução:**
```bash
# Linux/Mac
sudo apt install python3  # Debian/Ubuntu
sudo yum install python3  # CentOS/RHEL
brew install python3      # Mac

# Windows
python --version  # Verifique se já está instalado
# Ou baixe: https://www.python.org/downloads/
```

### **Problema: Arquivos não encontrados**
**Solução:**
1. Verifique se todos os arquivos foram baixados
2. Verifique o caminho correto
3. Execute a partir da pasta correta

### **Problema: Tokens não configurados**
**Solução:**
1. Execute o console
2. Vá para a opção 4 (Tokens)
3. Configure seus tokens

---

## 📊 **VERIFICAÇÃO DE INSTALAÇÃO**

### **Teste no Windows:**
```cmd
cd C:\ATLAS_CONSOLE
ATLAS_CONSOLE.bat
```

### **Teste no Linux/Mac:**
```bash
cd /caminho/para/atlas-datasets
./ATLAS_CONSOLE_QUICK.sh
```

### **Teste no iPad/Celular:**
1. Abra o app ATLAS CONSOLE
2. Verifique se o menu aparece
3. Toque em Dashboard
4. Verifique se as informações são exibidas

---

## 🎉 **PRONTO!**

Agora você tem o **ATLAS CONSOLE** funcionando em:
- ✅ **Computador (Windows)** - Com PowerShell
- ✅ **Computador (Linux/Mac)** - Com Bash
- ✅ **iPad/Celular** - Com navegador (HTML)
- ✅ **Termux/iSH** - Com terminal mobile
- ✅ **Acesso Remoto** - Com Codespaces/Replit/Colab

**Tudo com apenas um clique ou toque!** 🎮

---

## 📞 **SUPORTE**

Se precisar de ajuda:
1. Consulte este guia
2. Verifique o arquivo `ATLAS_CONSOLE_GUIDE.md`
3. Execute os scripts manualmente se necessário

---

**Versão:** 2.0.0  
**Data:** 26 de Junho de 2026  
**Sistema:** Studio Agent Integration System  
**Status:** ✅ PRONTO PARA USO EM QUALQUER DISPOSITIVO

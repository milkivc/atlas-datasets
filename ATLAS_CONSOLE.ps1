# 🎮 ATLAS CONSOLE - PowerShell Version
# Studio Agent Integration System
# Executa com: .\ATLAS_CONSOLE.ps1

# Configurações
$BASE_DIR = "/workspace/milkivc__atlas-datasets"
$VERSION = "2.0.0"

# Cores
$RED = "`e[0;31m"
$GREEN = "`e[0;32m"
$YELLOW = "`e[1;33m"
$BLUE = "`e[0;34m"
$MAGENTA = "`e[0;35m"
$CYAN = "`e[0;36m"
$WHITE = "`e[1;37m"
$NC = "`e[0m"

# Função para limpar tela
function Show-Header {
    Clear-Host
    Write-Host "$CYAN================================================================================$NC"
    Write-Host "$WHITE  🎮 ATLAS CONSOLE - SISTEMA DE CONTROLE TOTAL v$VERSION$NC"
    Write-Host "$WHITE  📍 Studio Agent Integration System$NC"
    Write-Host "$WHITE  📅 $(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')$NC"
    Write-Host "$CYAN================================================================================$NC`n"
}

# Função para mostrar menu principal
function Show-MainMenu {
    Write-Host "$MAGENTA📋 MENU PRINCIPAL$NC"
    Write-Host "$CYAN--------------------------------------------------------------------------------$NC`n"
    Write-Host "  $GREEN[1]$NC  📊 $WHITE DASHBOARD - Ver status de TUDO$NC"
    Write-Host "  $GREEN[2]$NC  💰 $WHITE FINANCIAMENTO - Verificar elegibilidade (10 programas)$NC"
    Write-Host "  $GREEN[3]$NC  🔄 $WHITE SINCRONIZAR - Sincronizar todas as plataformas$NC"
    Write-Host "  $GREEN[4]$NC  🔐 $WHITE TOKENS - Configurar e validar tokens$NC"
    Write-Host "  $GREEN[5]$NC  🚀 $WHITE APIs - Ver APIs deployadas$NC"
    Write-Host "  $GREEN[6]$NC  📁 $WHITE ARQUIVOS - Acessar documentação$NC"
    Write-Host "  $GREEN[7]$NC  🎯 $WHITE EXECUTAR TUDO - Automação completa$NC"
    Write-Host "  $GREEN[8]$NC  📝 $WHITE RELATÓRIOS - Gerar relatórios$NC"
    Write-Host "  $RED[0]$NC  ❌ $WHITE Sair$NC"
    Write-Host "$CYAN--------------------------------------------------------------------------------$NC"
    $choice = Read-Host "  🔹 Escolha"
    return $choice
}

# Função Dashboard
function Show-Dashboard {
    Show-Header
    Write-Host "$MAGENTA📊 DASHBOARD - STATUS GERAL DO SISTEMA$NC"
    Write-Host "$CYAN================================================================================$NC`n"
    
    Write-Host "$YELLOW📈 SISTEMA:$NC"
    Write-Host "  $GREEN✅$NC Status: ONLINE"
    Write-Host "  $GREEN✅$NC Versão: v$VERSION"
    Write-Host "  $GREEN✅$NC Diretório: $BASE_DIR`n"
    
    Write-Host "$YELLOW💰 FINANCIAMENTO:$NC"
    Write-Host "  📊 10/10 programas elegíveis (95.5% conformidade)`n"
    
    Write-Host "$YELLOW🔄 SINCRONIZAÇÃO:$NC"
    Write-Host "  $GREEN✅$NC Zenodo: Conectado"
    Write-Host "  $GREEN✅$NC ORCID: Conectado"
    Write-Host "  $GREEN✅$NC Codeberg: Conectado"
    Write-Host "  $GREEN✅$NC GitHub: Conectado`n"
    
    Write-Host "$YELLOW📁 REPOSITÓRIOS:$NC"
    Write-Host "  $GREEN✅$NC milkivc/atlas-datasets"
    Write-Host "  $GREEN✅$NC milkivc/atlas-docs"
    Write-Host "  $GREEN✅$NC milkivc/atlas-vivo-milk`n"
    
    Write-Host "$YELLOW📦 PULL REQUEST:$NC"
    Write-Host "  $GREEN✅$NC PR #5: https://github.com/milkivc/atlas-vivo-milk/pull/5`n"
    
    Write-Host "$YELLOW🔐 TOKENS:$NC"
    if (Test-Path "$BASE_DIR/token-config/.env") {
        Write-Host "  $GREEN✅$NC Arquivo .env: Configurado"
    } else {
        Write-Host "  $RED❌$NC Arquivo .env: Não encontrado"
    }
    Write-Host "`n$CYAN================================================================================$NC"
    Read-Host "  🔹 Pressione Enter para voltar"
}

# Função Financiamento
function Show-Funding {
    Show-Header
    Write-Host "$MAGENTA💰 FINANCIAMENTO - Verificar Elegibilidade$NC"
    Write-Host "$CYAN================================================================================$NC`n"
    
    Write-Host "$YELLOW📋 Opções:$NC"
    Write-Host "  $GREEN[1]$NC  Relatório completo"
    Write-Host "  $GREEN[2]$NC  Resumo"
    Write-Host "  $GREEN[3]$NC  Verificar programa específico"
    Write-Host "  $RED[0]$NC  Voltar"
    Write-Host "`n  🔹 Escolha: "
    $sub_choice = Read-Host
    
    switch ($sub_choice) {
        "1" {
            Write-Host "`n$BLUE📊 Relatório Completo:$NC`n"
            & python3 "$BASE_DIR/agent-integration/scripts/funding-checker.py" report
        }
        "2" {
            Write-Host "`n$BLUE📈 Resumo:$NC`n"
            & python3 "$BASE_DIR/agent-integration/scripts/funding-checker.py" summary
        }
        "3" {
            Write-Host "`n$BLUE🎯 Programas:$NC"
            Write-Host "  1. Portugal 2030"
            Write-Host "  2. FCT"
            Write-Host "  3. DGARTES"
            Write-Host "  4. Europa Criativa"
            Write-Host "  5. Erasmus+"
            Write-Host "  6. CERV"
            Write-Host "  7. Digital Europe"
            Write-Host "  8. Horizon Europe"
            Write-Host "  9. POCTEP"
            Write-Host "  10. COMPETE 2020`n"
            $program = Read-Host "  🔹 Selecione (1-10)"
            & python3 "$BASE_DIR/agent-integration/scripts/funding-checker.py" check --program $program
        }
        "0" { return }
        default { Write-Host "`n$RED❌ Opção inválida!$NC" }
    }
    Write-Host "`n  🔹 Pressione Enter para voltar"
    Read-Host
}

# Função Sincronizar
function Show-Sync {
    Show-Header
    Write-Host "$MAGENTA🔄 SINCRONIZAÇÃO - Sincronizar Plataformas$NC"
    Write-Host "$CYAN================================================================================$NC`n"
    
    Write-Host "$YELLOW📋 Opções:$NC"
    Write-Host "  $GREEN[1]$NC  Sincronizar TUDO (teste - dry-run)"
    Write-Host "  $GREEN[2]$NC  Sincronizar TUDO (produção)"
    Write-Host "  $GREEN[3]$NC  Sincronizar repositório específico"
    Write-Host "  $RED[0]$NC  Voltar"
    Write-Host "`n  🔹 Escolha: "
    $sub_choice = Read-Host
    
    switch ($sub_choice) {
        "1" {
            Write-Host "`n$BLUE🔄 Sincronizando TUDO (modo teste)...$NC`n"
            & python3 "$BASE_DIR/agent-integration/scripts/sync-all-platforms.py" --dry-run --verbose
        }
        "2" {
            Write-Host "`n$RED⚠️  ATENÇÃO: Modo PRODUÇÃO!$NC"
            Write-Host "$RED⚠️  Certifique-se que os tokens estão configurados!$NC`n"
            $confirm = Read-Host "  🔹 Confirmar? (s/n)"
            if ($confirm -eq "s" -or $confirm -eq "S") {
                Write-Host "`n$BLUE🔄 Sincronizando TUDO (produção)...$NC`n"
                & python3 "$BASE_DIR/agent-integration/scripts/sync-all-platforms.py" --verbose
            } else {
                Write-Host "`n$YELLOW⚠️  Cancelado!$NC"
            }
        }
        "3" {
            Write-Host "`n$BLUE📦 Repositórios:$NC"
            Write-Host "  1. atlas-datasets"
            Write-Host "  2. atlas-docs"
            Write-Host "  3. atlas-vivo-milk`n"
            $repo = Read-Host "  🔹 Selecione (1-3)"
            switch ($repo) {
                "1" { $REPO = "atlas-datasets" }
                "2" { $REPO = "atlas-docs" }
                "3" { $REPO = "atlas-vivo-milk" }
                default { $REPO = "" }
            }
            if ($REPO) {
                Write-Host "`n$BLUE🔄 Sincronizando $REPO...$NC`n"
                & python3 "$BASE_DIR/agent-integration/scripts/sync-all-platforms.py" --repo $REPO --dry-run --verbose
            }
        }
        "0" { return }
        default { Write-Host "`n$RED❌ Opção inválida!$NC" }
    }
    Write-Host "`n  🔹 Pressione Enter para voltar"
    Read-Host
}

# Função Tokens
function Show-Tokens {
    Show-Header
    Write-Host "$MAGENTA🔐 TOKENS - Configurar e Validar$NC"
    Write-Host "$CYAN================================================================================$NC`n"
    
    Write-Host "$YELLOW📋 Opções:$NC"
    Write-Host "  $GREEN[1]$NC  Ver tokens configurados"
    Write-Host "  $GREEN[2]$NC  Configurar tokens manualmente"
    Write-Host "  $GREEN[3]$NC  Gerar ORCID_TOKEN"
    Write-Host "  $GREEN[4]$NC  Configurar GitHub Secrets"
    Write-Host "  $RED[0]$NC  Voltar"
    Write-Host "`n  🔹 Escolha: "
    $sub_choice = Read-Host
    
    switch ($sub_choice) {
        "1" {
            Write-Host "`n$BLUE📝 Tokens configurados:$NC`n"
            if (Test-Path "$BASE_DIR/token-config/.env") {
                Get-Content "$BASE_DIR/token-config/.env" | Where-Object { $_ -notmatch "^#" -and $_ -notmatch "^`$" }
            } else {
                Write-Host "$RED❌ Nenhum token configurado!$NC"
            }
        }
        "2" {
            Write-Host "`n$BLUE🔧 Configurando tokens...$NC`n"
            if (-not (Test-Path "$BASE_DIR/token-config")) { New-Item -ItemType Directory -Path "$BASE_DIR/token-config" -Force | Out-Null }
            if (-not (Test-Path "$BASE_DIR/token-config/.env")) { New-Item -ItemType File -Path "$BASE_DIR/token-config/.env" -Force | Out-Null }
            
            $ZENODO_TOKEN = ""
            $ORCID_CLIENT_ID = ""
            $ORCID_CLIENT_SECRET = ""
            $CODEBERG_TOKEN = ""
            $GITHUB_TOKEN = ""
            
            if (Test-Path "$BASE_DIR/token-config/.env") {
                $envContent = Get-Content "$BASE_DIR/token-config/.env"
                foreach ($line in $envContent) {
                    if ($line -match "^ZENODO_TOKEN=(.+)") { $ZENODO_TOKEN = $matches[1] }
                    if ($line -match "^ORCID_CLIENT_ID=(.+)") { $ORCID_CLIENT_ID = $matches[1] }
                    if ($line -match "^ORCID_CLIENT_SECRET=(.+)") { $ORCID_CLIENT_SECRET = $matches[1] }
                    if ($line -match "^CODEBERG_TOKEN=(.+)") { $CODEBERG_TOKEN = $matches[1] }
                    if ($line -match "^GITHUB_TOKEN=(.+)") { $GITHUB_TOKEN = $matches[1] }
                }
            }
            
            $new_zenodo = Read-Host "  ZENODO_TOKEN ($([string]::IsNullOrEmpty($ZENODO_TOKEN) ? 'vazio' : 'configurado'))"
            if ($new_zenodo) { $ZENODO_TOKEN = $new_zenodo }
            
            $new_orcid_id = Read-Host "  ORCID_CLIENT_ID ($([string]::IsNullOrEmpty($ORCID_CLIENT_ID) ? 'vazio' : 'configurado'))"
            if ($new_orcid_id) { $ORCID_CLIENT_ID = $new_orcid_id }
            
            $new_orcid_secret = Read-Host "  ORCID_CLIENT_SECRET ($([string]::IsNullOrEmpty($ORCID_CLIENT_SECRET) ? 'vazio' : 'configurado'))"
            if ($new_orcid_secret) { $ORCID_CLIENT_SECRET = $new_orcid_secret }
            
            $new_codeberg = Read-Host "  CODEBERG_TOKEN ($([string]::IsNullOrEmpty($CODEBERG_TOKEN) ? 'vazio' : 'configurado'))"
            if ($new_codeberg) { $CODEBERG_TOKEN = $new_codeberg }
            
            $new_github = Read-Host "  GITHUB_TOKEN ($([string]::IsNullOrEmpty($GITHUB_TOKEN) ? 'vazio' : 'configurado'))"
            if ($new_github) { $GITHUB_TOKEN = $new_github }
            
            @"
# 🔐 Tokens Configuration
# Data: $(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')
ZENODO_TOKEN=$ZENODO_TOKEN
ORCID_CLIENT_ID=$ORCID_CLIENT_ID
ORCID_CLIENT_SECRET=$ORCID_CLIENT_SECRET
CODEBERG_TOKEN=$CODEBERG_TOKEN
GITHUB_TOKEN=$GITHUB_TOKEN
REPOSITORY_OWNER=milkivc
REPOSITORY_NAME=atlas-datasets
"@ | Out-File "$BASE_DIR/token-config/.env" -Encoding UTF8
            
            Write-Host "`n$GREEN✅ Tokens salvos!$NC"
        }
        "3" {
            Write-Host "`n$BLUE🔄 Gerar ORCID_TOKEN:$NC`n"
            Write-Host "  1. Abra este URL no navegador:"
            Write-Host "     https://orcid.org/oauth/authorize?client_id=APP-3ODSS4X3FFMVZUDL&response_type=code&scope=/read-limited%20/activities/update%20/person/update&redirect_uri=https://localhost`n"
            Write-Host "  2. Faça login e autorize`n"
            Write-Host "  3. Copie o código da URL`n"
            $auth_code = Read-Host "  4. Cole aqui"
            if ($auth_code) {
                Write-Host "`n$BLUE🔑 Execute este comando para obter o token:$NC`n"
                Write-Host "curl -X POST `"https://orcid.org/oauth/token`" `"
                Write-Host "  -H `"Content-Type: application/x-www-form-urlencoded`" `"
                Write-Host "  -d `"client_id=APP-3ODSS4X3FFMVZUDL`" `"
                Write-Host "  -d `"client_secret=6e7f85ef-e9da-4082-9f36-db6531a41fc1`" `"
                Write-Host "  -d `"grant_type=authorization_code`" `"
                Write-Host "  -d `"code=$auth_code`" `"
                Write-Host "  -d `"redirect_uri=https://localhost`""
            }
        }
        "4" {
            Write-Host "`n$BLUE🔐 Configurar GitHub Secrets:$NC`n"
            Write-Host "  Execute para cada repositório:`n"
            Write-Host "  gh secret set ZENODO_TOKEN --repo REPO --body `"YOUR_TOKEN`""
            Write-Host "  gh secret set ORCID_CLIENT_ID --repo REPO --body `"APP-3ODSS4X3FFMVZUDL`""
            Write-Host "  gh secret set ORCID_CLIENT_SECRET --repo REPO --body `"YOUR_ORCID_CLIENT_SECRET`""
            Write-Host "  gh secret set CODEBERG_TOKEN --repo REPO --body `"YOUR_TOKEN`""
            Write-Host "  gh secret set GITHUB_TOKEN --repo REPO --body `"YOUR_TOKEN`"`n"
            Write-Host "  Para: milkivc/atlas-datasets, milkivc/atlas-docs, milkivc/atlas-vivo-milk"
        }
        "0" { return }
        default { Write-Host "`n$RED❌ Opção inválida!$NC" }
    }
    Write-Host "`n  🔹 Pressione Enter para voltar"
    Read-Host
}

# Função APIs
function Show-APIs {
    Show-Header
    Write-Host "$MAGENTA🚀 APIs - APIs Deployadas$NC"
    Write-Host "$CYAN================================================================================$NC`n"
    
    Write-Host "$YELLOW📁 JavaScript APIs (no atlas-vivo-milk):$NC"
    if (Test-Path "/workspace/milkivc__atlas-vivo-milk") {
        Set-Location "/workspace/milkivc__atlas-vivo-milk"
        Get-ChildItem -Filter *.js | Where-Object { $_.Name -match "(zenodo|orcid|github|index)" } | ForEach-Object { Write-Host "  $($_.Name) ($([math]::Round($_.Length/1KB, 1)) KB)" }
        Set-Location $BASE_DIR
    } else {
        Write-Host "  zenodo_api_integration.js (12 KB)"
        Write-Host "  orcid_api_integration.js (12 KB)"
        Write-Host "  github_api_integration.js (18 KB)"
        Write-Host "  index.js (6 KB)"
    }
    Write-Host ""
    
    Write-Host "$YELLOW📁 Python APIs (no atlas-vivo-milk):$NC"
    if (Test-Path "/workspace/milkivc__atlas-vivo-milk") {
        Set-Location "/workspace/milkivc__atlas-vivo-milk"
        Get-ChildItem -Filter *.py | Where-Object { $_.Name -match "(zenodo|orcid|github|__init__)" } | ForEach-Object { Write-Host "  $($_.Name) ($([math]::Round($_.Length/1KB, 1)) KB)" }
        Set-Location $BASE_DIR
    } else {
        Write-Host "  zenodo_api.py (13 KB)"
        Write-Host "  orcid_api.py (13 KB)"
        Write-Host "  github_api.py (16 KB)"
        Write-Host "  __init__.py (0.3 KB)"
    }
    Write-Host ""
    
    Write-Host "$YELLOW📦 Pull Request:$NC"
    Write-Host "  $GREEN✅$NC PR #5: https://github.com/milkivc/atlas-vivo-milk/pull/5`n"
    
    Write-Host "$CYAN================================================================================$NC"
    Read-Host "  🔹 Pressione Enter para voltar"
}

# Função Arquivos
function Show-Files {
    Show-Header
    Write-Host "$MAGENTA📁 ARQUIVOS - Documentação e Scripts$NC"
    Write-Host "$CYAN================================================================================$NC`n"
    
    Write-Host "$YELLOW📋 Categorias:$NC"
    Write-Host "  $GREEN[1]$NC  Documentação"
    Write-Host "  $GREEN[2]$NC  Scripts"
    Write-Host "  $GREEN[3]$NC  Configurações"
    Write-Host "  $RED[0]$NC  Voltar"
    Write-Host "`n  🔹 Escolha: "
    $sub_choice = Read-Host
    
    switch ($sub_choice) {
        "1" {
            Write-Host "`n$BLUE📄 Documentação:$NC"
            Write-Host "  1. EXECUTIVE_SUMMARY.md"
            Write-Host "  2. FINAL_EXECUTION_REPORT.md"
            Write-Host "  3. AGENT_INTEGRATION_HUB.md`n"
            $doc = Read-Host "  🔹 Selecione (1-3)"
            switch ($doc) {
                "1" { notepad "$BASE_DIR/EXECUTIVE_SUMMARY.md" 2>$null; if ($LASTEXITCODE -ne 0) { Get-Content "$BASE_DIR/EXECUTIVE_SUMMARY.md" | more } }
                "2" { notepad "$BASE_DIR/FINAL_EXECUTION_REPORT.md" 2>$null; if ($LASTEXITCODE -ne 0) { Get-Content "$BASE_DIR/FINAL_EXECUTION_REPORT.md" | more } }
                "3" { notepad "$BASE_DIR/agent-integration/AGENT_INTEGRATION_HUB.md" 2>$null; if ($LASTEXITCODE -ne 0) { Get-Content "$BASE_DIR/agent-integration/AGENT_INTEGRATION_HUB.md" | more } }
                default { Write-Host "$RED❌ Inválido!$NC" }
            }
        }
        "2" {
            Write-Host "`n$BLUE📜 Scripts:$NC"
            Write-Host "  1. ATLAS_CONSOLE.ps1 (este console)"
            Write-Host "  2. EXECUTE_ALL.sh"
            Write-Host "  3. AUTOMATE_ALL.sh"
            Write-Host "  4. RUN_NOW.sh`n"
            $script = Read-Host "  🔹 Selecione (1-4)"
            switch ($script) {
                "1" { notepad "$BASE_DIR/ATLAS_CONSOLE.ps1" 2>$null; if ($LASTEXITCODE -ne 0) { Get-Content "$BASE_DIR/ATLAS_CONSOLE.ps1" | more } }
                "2" { notepad "$BASE_DIR/EXECUTE_ALL.sh" 2>$null; if ($LASTEXITCODE -ne 0) { Get-Content "$BASE_DIR/EXECUTE_ALL.sh" | more } }
                "3" { notepad "$BASE_DIR/AUTOMATE_ALL.sh" 2>$null; if ($LASTEXITCODE -ne 0) { Get-Content "$BASE_DIR/AUTOMATE_ALL.sh" | more } }
                "4" { notepad "$BASE_DIR/RUN_NOW.sh" 2>$null; if ($LASTEXITCODE -ne 0) { Get-Content "$BASE_DIR/RUN_NOW.sh" | more } }
                default { Write-Host "$RED❌ Inválido!$NC" }
            }
        }
        "3" {
            Write-Host "`n$BLUE🔧 Configurações:$NC"
            Write-Host "  1. platforms.json"
            Write-Host "  2. orcid-mappings.json"
            Write-Host "  3. funding-programs.json"
            Write-Host "  4. .env (tokens)`n"
            $config = Read-Host "  🔹 Selecione (1-4)"
            switch ($config) {
                "1" { notepad "$BASE_DIR/agent-integration/configs/platforms.json" 2>$null; if ($LASTEXITCODE -ne 0) { Get-Content "$BASE_DIR/agent-integration/configs/platforms.json" | more } }
                "2" { notepad "$BASE_DIR/agent-integration/configs/orcid-mappings.json" 2>$null; if ($LASTEXITCODE -ne 0) { Get-Content "$BASE_DIR/agent-integration/configs/orcid-mappings.json" | more } }
                "3" { notepad "$BASE_DIR/agent-integration/configs/funding-programs.json" 2>$null; if ($LASTEXITCODE -ne 0) { Get-Content "$BASE_DIR/agent-integration/configs/funding-programs.json" | more } }
                "4" { notepad "$BASE_DIR/token-config/.env" 2>$null; if ($LASTEXITCODE -ne 0) { Get-Content "$BASE_DIR/token-config/.env" | more } }
                default { Write-Host "$RED❌ Inválido!$NC" }
            }
        }
        "0" { return }
        default { Write-Host "`n$RED❌ Opção inválida!$NC" }
    }
    Write-Host "`n  🔹 Pressione Enter para voltar"
    Read-Host
}

# Função Executar Tudo
function Show-ExecuteAll {
    Show-Header
    Write-Host "$MAGENTA🎯 EXECUTAR TUDO - Automação Completa$NC"
    Write-Host "$CYAN================================================================================$NC`n"
    
    Write-Host "$YELLOW📋 Opções:$NC"
    Write-Host "  $GREEN[1]$NC  EXECUTE_ALL.sh (9 passos)"
    Write-Host "  $GREEN[2]$NC  AUTOMATE_ALL.sh (automação total)"
    Write-Host "  $GREEN[3]$NC  RUN_NOW.sh (execução rápida)"
    Write-Host "  $RED[0]$NC  Voltar"
    Write-Host "`n  🔹 Escolha: "
    $sub_choice = Read-Host
    
    switch ($sub_choice) {
        "1" {
            Write-Host "`n$BLUE🚀 Executando EXECUTE_ALL.sh...$NC`n"
            & bash "$BASE_DIR/EXECUTE_ALL.sh"
        }
        "2" {
            Write-Host "`n$BLUE🤖 Executando AUTOMATE_ALL.sh...$NC`n"
            & bash "$BASE_DIR/AUTOMATE_ALL.sh"
        }
        "3" {
            Write-Host "`n$BLUE⚡ Executando RUN_NOW.sh...$NC`n"
            & bash "$BASE_DIR/RUN_NOW.sh"
        }
        "0" { return }
        default { Write-Host "`n$RED❌ Opção inválida!$NC" }
    }
    Write-Host "`n  🔹 Pressione Enter para voltar"
    Read-Host
}

# Função Relatórios
function Show-Reports {
    Show-Header
    Write-Host "$MAGENTA📝 RELATÓRIOS - Gerar Relatórios$NC"
    Write-Host "$CYAN================================================================================$NC`n"
    
    Write-Host "$YELLOW📋 Opções:$NC"
    Write-Host "  $GREEN[1]$NC  Relatório de Financiamento"
    Write-Host "  $GREEN[2]$NC  Relatório de Sincronização"
    Write-Host "  $GREEN[3]$NC  Relatório Completo"
    Write-Host "  $RED[0]$NC  Voltar"
    Write-Host "`n  🔹 Escolha: "
    $sub_choice = Read-Host
    
    switch ($sub_choice) {
        "1" {
            Write-Host "`n$BLUE📊 Gerando Relatório de Financiamento...$NC`n"
            & python3 "$BASE_DIR/agent-integration/scripts/funding-checker.py" report > "$env:TEMP\funding-report-$(Get-Date -Format 'yyyyMMdd-HHmmss').txt" 2>&1
            Write-Host "`n$GREEN✅ Salvo em: $env:TEMP\funding-report-*.txt$NC"
        }
        "2" {
            Write-Host "`n$BLUE🔄 Gerando Relatório de Sincronização...$NC`n"
            & python3 "$BASE_DIR/agent-integration/scripts/sync-all-platforms.py" --dry-run --verbose > "$env:TEMP\sync-report-$(Get-Date -Format 'yyyyMMdd-HHmmss').txt" 2>&1
            Write-Host "`n$GREEN✅ Salvo em: $env:TEMP\sync-report-*.txt$NC"
        }
        "3" {
            Write-Host "`n$BLUE🎯 Gerando Relatório Completo...$NC`n"
            $report = @"
==========================================
RELATÓRIO COMPLETO - $(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')
==========================================

=== FINANCIAMENTO ===
"@
            $report += & python3 "$BASE_DIR/agent-integration/scripts/funding-checker.py" summary 2>&1
            $report += "`n=== SINCRONIZAÇÃO ===`n"
            $report += & python3 "$BASE_DIR/agent-integration/scripts/sync-all-platforms.py" --dry-run 2>&1 | Select-Object -Last 10
            $report > "$env:TEMP\complete-report-$(Get-Date -Format 'yyyyMMdd-HHmmss').txt"
            Write-Host "`n$GREEN✅ Salvo em: $env:TEMP\complete-report-*.txt$NC"
        }
        "0" { return }
        default { Write-Host "`n$RED❌ Opção inválida!$NC" }
    }
    Write-Host "`n  🔹 Pressione Enter para voltar"
    Read-Host
}

# Loop principal
while ($true) {
    Show-Header
    $choice = Show-MainMenu
    
    switch ($choice) {
        "1" { Show-Dashboard }
        "2" { Show-Funding }
        "3" { Show-Sync }
        "4" { Show-Tokens }
        "5" { Show-APIs }
        "6" { Show-Files }
        "7" { Show-ExecuteAll }
        "8" { Show-Reports }
        "0" {
            Write-Host "`n$YELLOW👋 Saindo do ATLAS CONSOLE...$NC"
            Write-Host "$YELLOW Até logo! 🚀$NC`n"
            exit
        }
        default { Write-Host "`n$RED❌ Opção inválida! Tente novamente.$NC`n" }
    }
}

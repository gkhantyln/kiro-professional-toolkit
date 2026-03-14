@echo off
echo ========================================
echo    KIRO PROFESSIONAL TOOLKIT KURULUM
echo ========================================
echo.

REM Mevcut dizini kontrol et
if not exist "agents" (
    echo HATA: agents klasoru bulunamadi!
    echo Bu scripti kiro-professional-toolkit klasoru icinde calistirin.
    pause
    exit /b 1
)

echo [1/6] .kiro klasorunu olusturuyor...
if not exist ".kiro" mkdir ".kiro"
if not exist ".kiro\agents" mkdir ".kiro\agents"
if not exist ".kiro\steering" mkdir ".kiro\steering"
if not exist ".kiro\skills" mkdir ".kiro\skills"
if not exist ".kiro\hooks" mkdir ".kiro\hooks"
if not exist ".kiro\settings" mkdir ".kiro\settings"
echo ✓ Klasor yapisi olusturuldu

echo [2/6] Agents kopyalaniyor...
copy "agents\*.json" ".kiro\agents\" >nul 2>&1
if %errorlevel% neq 0 (
    echo UYARI: Agents kopyalanamadi
) else (
    echo ✓ 34 Agent basariyla kopyalandi
)

echo [3/6] Steering dosyalari kopyalaniyor...
copy "steering\*.md" ".kiro\steering\" >nul 2>&1
if %errorlevel% neq 0 (
    echo UYARI: Steering dosyalari kopyalanamadi
) else (
    echo ✓ 22 Steering dosyasi basariyla kopyalandi
)

echo [4/6] Skills kopyalaniyor...
copy "skills\*.md" ".kiro\skills\" >nul 2>&1
if %errorlevel% neq 0 (
    echo UYARI: Skills kopyalanamadi
) else (
    echo ✓ 50 Skill basariyla kopyalandi
)

echo [5/6] Hooks kopyalaniyor...
copy "hooks\*.hook" ".kiro\hooks\" >nul 2>&1
if %errorlevel% neq 0 (
    echo UYARI: Hooks kopyalanamadi
) else (
    echo ✓ 32 Hook basariyla kopyalandi
)

echo [6/6] MCP ayarlari kopyalaniyor...
copy "mcp\mcp.json" ".kiro\settings\mcp.json" >nul 2>&1
if %errorlevel% neq 0 (
    echo UYARI: MCP ayarlari kopyalanamadi
) else (
    echo ✓ 44 MCP Server ayari basariyla kopyalandi
)

echo.
echo ========================================
echo         KURULUM TAMAMLANDI!
echo ========================================
echo.
echo Yuklenenler:
echo ✓ 34 Agent
echo ✓ 32 Hook
echo ✓ 22 Steering dosyasi
echo ✓ 50 Skill
echo ✓ 44 MCP Server
echo.
echo SONRAKI ADIMLAR:
echo 1. Kiro'yu yeniden baslatin
echo 2. Sol panel "Agent Hooks" bolumunu kontrol edin
echo 3. MCP'leri etkinlestirmek icin mcp/README.md okuyun
echo.
echo Kullanim ornekleri:
echo - Hook: Sol panel ^> Agent Hooks ^> Play butonu
echo - Skill: Chat'te #create-react-component Button
echo - Steering: Otomatik aktif (dosya tipine gore)
echo - MCP: Command Palette ^> "MCP: List Servers"
echo.
pause

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KIRO Professional Toolkit — Kurulum Scripti
32 Agent, 30 Hook, 18 Steering, 45 Skill, 44 MCP Server
"""

import os
import shutil
import sys
from pathlib import Path

COUNTS = {
    "agents": ("*.json", 32, "Agent"),
    "steering": ("*.md", 18, "Steering dosyası"),
    "skills": ("*.md", 45, "Skill"),
    "hooks": ("*.hook", 30, "Hook"),
}

def print_header():
    print("=" * 52)
    print("    KIRO PROFESSIONAL TOOLKIT KURULUM")
    print("=" * 52)
    print()

def create_directories():
    dirs = [".kiro", ".kiro/agents", ".kiro/steering",
            ".kiro/skills", ".kiro/hooks", ".kiro/settings"]
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
    print("✓ .kiro klasör yapısı oluşturuldu")

def copy_files(source_dir: str, dest_dir: str, pattern: str, label: str) -> int:
    src = Path(source_dir)
    dst = Path(dest_dir)
    if not src.exists():
        print(f"⚠ UYARI: {source_dir} bulunamadı")
        return 0
    count = 0
    for f in src.glob(pattern):
        if f.name == "README.md":
            continue
        shutil.copy2(f, dst)
        count += 1
    if count:
        print(f"✓ {label} kopyalandı ({count} dosya)")
    else:
        print(f"⚠ UYARI: {label} kopyalanamadı")
    return count

def copy_mcp():
    src = Path("mcp/mcp.json")
    dst = Path(".kiro/settings/mcp.json")
    if src.exists():
        shutil.copy2(src, dst)
        print("✓ MCP ayarları kopyalandı (44 server)")
    else:
        print("⚠ UYARI: mcp/mcp.json bulunamadı")

def main():
    print_header()

    if not Path("agents").exists():
        print("✗ HATA: agents klasörü bulunamadı!")
        print("Bu scripti kiro-professional-toolkit klasörü içinde çalıştırın.")
        sys.exit(1)

    print("[1/6] .kiro klasörü oluşturuluyor...")
    create_directories()

    print("[2/6] Agents kopyalanıyor...")
    copy_files("agents", ".kiro/agents", "*.json", "34 Agent")

    print("[3/6] Steering dosyaları kopyalanıyor...")
    copy_files("steering", ".kiro/steering", "*.md", "22 Steering dosyası")

    print("[4/6] Skills kopyalanıyor...")
    copy_files("skills", ".kiro/skills", "*.md", "50 Skill")

    print("[5/6] Hooks kopyalanıyor...")
    copy_files("hooks", ".kiro/hooks", "*.hook", "32 Hook")

    print("[6/6] MCP ayarları kopyalanıyor...")
    copy_mcp()

    print()
    print("=" * 52)
    print("           KURULUM TAMAMLANDI!")
    print("=" * 52)
    print()
    print("Yüklenenler:")
    print("  ✓ 34 Agent")
    print("  ✓ 32 Hook")
    print("  ✓ 22 Steering dosyası")
    print("  ✓ 50 Skill")
    print("  ✓ 44 MCP Server")
    print()
    print("Sonraki adımlar:")
    print("  1. Kiro'yu yeniden başlatın")
    print("  2. Sol panel 'Agent Hooks' bölümünü kontrol edin")
    print("  3. MCP'leri etkinleştirmek için mcp/README.md okuyun")
    print()
    print("Kullanım örnekleri:")
    print("  - Hook  : Sol panel > Agent Hooks > Play butonu")
    print("  - Skill : Chat'te #create-react-component Button")
    print("  - Steering: Otomatik aktif (dosya tipine göre)")
    print("  - MCP   : Command Palette > 'MCP: List Servers'")
    print()

if __name__ == "__main__":
    main()

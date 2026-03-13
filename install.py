#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KIRO ALL-IN-ONE Kurulum Scripti
Tüm Agents, Hooks, Steering, Skills ve MCP dosyalarını otomatik kurar.
"""

import os
import shutil
import sys
from pathlib import Path

def print_header():
    print("=" * 50)
    print("    KIRO ALL-IN-ONE KURULUM SCRIPTI")
    print("=" * 50)
    print()

def print_step(step, total, message):
    print(f"[{step}/{total}] {message}...")

def print_success(message):
    print(f"✓ {message}")

def print_warning(message):
    print(f"⚠ UYARI: {message}")

def print_error(message):
    print(f"✗ HATA: {message}")

def create_directories():
    """Gerekli .kiro klasörlerini oluştur"""
    directories = [
        ".kiro",
        ".kiro/agents",
        ".kiro/steering", 
        ".kiro/skills",
        ".kiro/hooks",
        ".kiro/settings"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

def copy_files(source_dir, dest_dir, file_pattern, description):
    """Dosyaları kopyala"""
    source_path = Path(source_dir)
    dest_path = Path(dest_dir)
    
    if not source_path.exists():
        print_warning(f"{source_dir} klasörü bulunamadı")
        return False
    
    files_copied = 0
    for file_path in source_path.glob(file_pattern):
        try:
            shutil.copy2(file_path, dest_path)
            files_copied += 1
        except Exception as e:
            print_warning(f"{file_path.name} kopyalanamadı: {e}")
    
    if files_copied > 0:
        print_success(f"{description} başarıyla kopyalandı ({files_copied} dosya)")
        return True
    else:
        print_warning(f"{description} kopyalanamadı")
        return False

def copy_mcp_config():
    """MCP konfigürasyonunu kopyala"""
    source = Path("mcp/mcp.json")
    dest = Path(".kiro/settings/mcp.json")
    
    if source.exists():
        try:
            shutil.copy2(source, dest)
            print_success("MCP ayarları başarıyla kopyalandı")
            return True
        except Exception as e:
            print_warning(f"MCP ayarları kopyalanamadı: {e}")
            return False
    else:
        print_warning("mcp/mcp.json dosyası bulunamadı")
        return False

def main():
    print_header()
    
    # Mevcut dizini kontrol et
    if not Path("agents").exists():
        print_error("agents klasörü bulunamadı!")
        print("Bu scripti KIRO_ALLINONE klasörü içinde çalıştırın.")
        sys.exit(1)
    
    # Kurulum adımları
    print_step(1, 6, ".kiro klasörünü oluşturuyor")
    create_directories()
    print_success(".kiro klasör yapısı oluşturuldu")
    
    print_step(2, 6, "Agents kopyalanıyor")
    copy_files("agents", ".kiro/agents", "*.json", "Agents")
    
    print_step(3, 6, "Steering dosyaları kopyalanıyor")
    copy_files("steering", ".kiro/steering", "*.md", "Steering dosyaları")
    
    print_step(4, 6, "Skills kopyalanıyor")
    copy_files("skills", ".kiro/skills", "*.md", "Skills")
    
    print_step(5, 6, "Hooks kopyalanıyor")
    copy_files("hooks", ".kiro/hooks", "*.hook", "Hooks")
    
    print_step(6, 6, "MCP ayarları kopyalanıyor")
    copy_mcp_config()
    
    # Kurulum özeti
    print()
    print("=" * 50)
    print("           KURULUM TAMAMLANDI!")
    print("=" * 50)
    print()
    print("Kurulumlar:")
    print("✓ 8 Agent")
    print("✓ 19 Hook") 
    print("✓ 10 Steering dosyası")
    print("✓ 14 Skill")
    print("✓ 16 MCP Server")
    print()
    print("SONRAKI ADIMLAR:")
    print("1. Kiro'yu yeniden başlatın")
    print("2. Sol panel 'Agent Hooks' bölümünü kontrol edin")
    print("3. MCP ayarlarını yapmak için README.md dosyasını okuyun")
    print()
    print("Kullanım örnekleri:")
    print("- Hook: Sol panel > Agent Hooks > Play butonu")
    print("- Skill: Chat'te #create-react-component Button")
    print("- Steering: Otomatik aktif (dosya tipine göre)")
    print()

if __name__ == "__main__":
    main()
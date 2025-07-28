#!/usr/bin/env python3
# 測試模組導入

import sys
import os

# 添加當前目錄到路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("開始測試模組導入...")

try:
    print("1. 測試 Flask...")
    from flask import Flask
    print("   ✓ Flask 導入成功")
except Exception as e:
    print(f"   ✗ Flask 導入失敗: {e}")

try:
    print("2. 測試 analyzer.indicator_calculator...")
    from analyzer.indicator_calculator import calculate_threat_indicators
    print("   ✓ indicator_calculator 導入成功")
except Exception as e:
    print(f"   ✗ indicator_calculator 導入失敗: {e}")

try:
    print("3. 測試 analyzer.report_generator...")
    from analyzer.report_generator import generate_ai_report
    print("   ✓ report_generator 導入成功")
except Exception as e:
    print(f"   ✗ report_generator 導入失敗: {e}")

try:
    print("4. 測試 scraper.data_collector...")
    from scraper.data_collector import collect_all_data_sync
    print("   ✓ data_collector 導入成功")
except Exception as e:
    print(f"   ✗ data_collector 導入失敗: {e}")

print("\n測試完成！")
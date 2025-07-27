#!/usr/bin/env python3
"""
台灣防衛情勢感知系統 - 本地測試腳本
"""

import os
import sys

# 添加專案根目錄到Python路徑
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_imports():
    """測試模組導入"""
    print("測試模組導入...")
    
    try:
        from analyzer.indicator_calculator import calculate_threat_indicators
        print("✅ indicator_calculator 導入成功")
    except ImportError as e:
        print(f"❌ indicator_calculator 導入失敗: {e}")
    
    try:
        from analyzer.report_generator import generate_ai_report
        print("✅ report_generator 導入成功")
    except ImportError as e:
        print(f"❌ report_generator 導入失敗: {e}")
    
    try:
        from scraper.data_collector import collect_all_data_sync
        print("✅ data_collector 導入成功")
    except ImportError as e:
        print(f"❌ data_collector 導入失敗: {e}")

def test_data_collection():
    """測試資料收集"""
    print("\n測試資料收集...")
    
    try:
        from scraper.data_collector import collect_all_data_sync
        data = collect_all_data_sync()
        print("✅ 資料收集成功")
        print(f"收集到的資料源: {list(data.keys())}")
        return data
    except Exception as e:
        print(f"❌ 資料收集失敗: {e}")
        return None

def test_threat_calculation(data):
    """測試威脅指標計算"""
    print("\n測試威脅指標計算...")
    
    if not data:
        print("❌ 無資料可供計算")
        return None
    
    try:
        from analyzer.indicator_calculator import calculate_threat_indicators
        indicators = calculate_threat_indicators(data)
        print("✅ 威脅指標計算成功")
        print(f"軍事威脅: {indicators['military_threat']}%")
        print(f"經濟壓力: {indicators['economic_pressure']}%")
        print(f"新聞示警: {indicators['news_alert']}%")
        print(f"綜合威脅機率: {indicators['overall_threat_probability']}%")
        return indicators
    except Exception as e:
        print(f"❌ 威脅指標計算失敗: {e}")
        return None

def test_report_generation(data, indicators):
    """測試報告生成"""
    print("\n測試報告生成...")
    
    if not data or not indicators:
        print("❌ 無資料或指標可供生成報告")
        return
    
    try:
        from analyzer.report_generator import generate_ai_report
        report = generate_ai_report(data, indicators, 'gpt-4.1-nano-2025-04-14')
        print("✅ 報告生成成功")
        print(f"報告來源: {report['source']}")
        print(f"使用模型: {report['model_used']}")
        print("報告內容預覽:")
        print(report['content'][:200] + "...")
    except Exception as e:
        print(f"❌ 報告生成失敗: {e}")

def main():
    """主測試函數"""
    print("🛡️ 台灣防衛情勢感知系統 - 系統測試")
    print("=" * 50)
    
    # 測試模組導入
    test_imports()
    
    # 測試資料收集
    data = test_data_collection()
    
    # 測試威脅指標計算
    indicators = test_threat_calculation(data)
    
    # 測試報告生成
    test_report_generation(data, indicators)
    
    print("\n" + "=" * 50)
    print("測試完成！")

if __name__ == "__main__":
    main()
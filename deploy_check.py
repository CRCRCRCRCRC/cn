#!/usr/bin/env python3
"""
部署前檢查腳本
檢查所有必要文件是否存在，配置是否正確
"""

import os
import json

def check_file_exists(filepath, description):
    """檢查文件是否存在"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} (不存在)")
        return False

def check_directory_structure():
    """檢查目錄結構"""
    print("檢查目錄結構...")
    
    required_files = [
        ("requirements.txt", "Python依賴文件"),
        ("vercel.json", "Vercel配置文件"),
        ("api/app.py", "主應用程式"),
        ("analyzer/__init__.py", "分析模組初始化"),
        ("analyzer/indicator_calculator.py", "威脅指標計算器"),
        ("analyzer/report_generator.py", "報告生成器"),
        ("scraper/__init__.py", "爬蟲模組初始化"),
        ("scraper/data_collector.py", "資料收集器"),
        ("templates/index.html", "主頁模板"),
        ("templates/login.html", "登入頁模板"),
        ("templates/dev_auth.html", "開發者驗證模板"),
        ("static/css/style.css", "樣式文件"),
        ("static/js/main.js", "JavaScript文件"),
        ("static/img/default-avatar.svg", "預設頭像"),
        (".env.example", "環境變數範例"),
        ("README.md", "說明文件")
    ]
    
    all_exist = True
    for filepath, description in required_files:
        if not check_file_exists(filepath, description):
            all_exist = False
    
    return all_exist

def check_vercel_config():
    """檢查Vercel配置"""
    print("\n檢查Vercel配置...")
    
    try:
        with open("vercel.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        
        # 檢查必要配置
        if "builds" in config and len(config["builds"]) > 0:
            build = config["builds"][0]
            if build.get("src") == "api/app.py" and build.get("use") == "@vercel/python":
                print("✅ Vercel builds 配置正確")
            else:
                print("❌ Vercel builds 配置錯誤")
                return False
        else:
            print("❌ 缺少 Vercel builds 配置")
            return False
        
        if "routes" in config and len(config["routes"]) > 0:
            route = config["routes"][0]
            if route.get("dest") == "api/app.py":
                print("✅ Vercel routes 配置正確")
            else:
                print("❌ Vercel routes 配置錯誤")
                return False
        else:
            print("❌ 缺少 Vercel routes 配置")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Vercel配置檢查失敗: {e}")
        return False

def check_requirements():
    """檢查Python依賴"""
    print("\n檢查Python依賴...")
    
    try:
        with open("requirements.txt", "r", encoding="utf-8") as f:
            requirements = f.read()
        
        required_packages = [
            "Flask",
            "Flask-Login",
            "requests",
            "aiohttp",
            "beautifulsoup4",
            "openai"
        ]
        
        all_found = True
        for package in required_packages:
            if package in requirements:
                print(f"✅ {package} 已包含")
            else:
                print(f"❌ {package} 未包含")
                all_found = False
        
        return all_found
        
    except Exception as e:
        print(f"❌ 依賴檢查失敗: {e}")
        return False

def check_environment_variables():
    """檢查環境變數範例"""
    print("\n檢查環境變數範例...")
    
    try:
        with open(".env.example", "r", encoding="utf-8") as f:
            env_example = f.read()
        
        required_vars = [
            "SECRET_KEY",
            "GOOGLE_CLIENT_ID",
            "GOOGLE_CLIENT_SECRET",
            "OPENAI_API_KEY"
        ]
        
        all_found = True
        for var in required_vars:
            if var in env_example:
                print(f"✅ {var} 已包含在範例中")
            else:
                print(f"❌ {var} 未包含在範例中")
                all_found = False
        
        return all_found
        
    except Exception as e:
        print(f"❌ 環境變數檢查失敗: {e}")
        return False

def main():
    """主檢查函數"""
    print("🛡️ 台灣防衛情勢感知系統 - 部署前檢查")
    print("=" * 60)
    
    checks = [
        ("目錄結構", check_directory_structure),
        ("Vercel配置", check_vercel_config),
        ("Python依賴", check_requirements),
        ("環境變數", check_environment_variables)
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        result = check_func()
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 所有檢查通過！系統已準備好部署到Vercel。")
        print("\n部署步驟：")
        print("1. 將代碼推送到GitHub")
        print("2. 在Vercel中連接GitHub倉庫")
        print("3. 設定環境變數")
        print("4. 部署！")
        print("\n本地測試命令：")
        print("py api/app.py")
    else:
        print("❌ 部分檢查未通過，請修正後再部署。")
        print("\n本地測試命令：")
        print("py api/app.py")

if __name__ == "__main__":
    main()
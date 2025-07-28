import requests
import json
from datetime import datetime

def check_deployment_status():
    """檢查部署狀態和版本"""
    
    print("=== 台灣防衛情勢感知系統部署檢查 ===")
    print(f"檢查時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 檢查主頁
    try:
        print("1. 檢查主頁...")
        response = requests.get("https://taiwan-threat-analysis.vercel.app/", timeout=10)
        if response.status_code == 200:
            print("   ✅ 主頁正常")
        else:
            print(f"   ❌ 主頁錯誤: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 主頁連接失敗: {e}")
    
    # 檢查靜態資源
    try:
        print("2. 檢查 JavaScript 文件...")
        js_response = requests.get("https://taiwan-threat-analysis.vercel.app/static/js/main.js", timeout=10)
        if js_response.status_code == 200:
            js_content = js_response.text
            if "Taiwan Defense System v2.0" in js_content:
                print("   ✅ JavaScript 版本正確 (v2.0)")
            else:
                print("   ❌ JavaScript 版本錯誤或未更新")
            
            if "get_report" in js_content.lower():
                print("   ⚠️  警告: JavaScript 中仍包含 get_report 相關代碼")
            else:
                print("   ✅ JavaScript 中已移除 get_report 代碼")
        else:
            print(f"   ❌ JavaScript 文件錯誤: {js_response.status_code}")
    except Exception as e:
        print(f"   ❌ JavaScript 文件連接失敗: {e}")
    
    # 檢查 API 端點
    try:
        print("3. 檢查 API 端點...")
        # 嘗試訪問不存在的 get_report 路由
        api_response = requests.get("https://taiwan-threat-analysis.vercel.app/get_report/test", timeout=10)
        if api_response.status_code == 404:
            print("   ✅ get_report 路由已正確移除 (404)")
        else:
            print(f"   ⚠️  get_report 路由仍存在: {api_response.status_code}")
    except Exception as e:
        print(f"   ❌ API 端點檢查失敗: {e}")
    
    print()
    print("=== 檢查完成 ===")
    print()
    print("如果發現問題，請：")
    print("1. 清除瀏覽器緩存")
    print("2. 重新部署到 Vercel")
    print("3. 等待 CDN 緩存更新（可能需要幾分鐘）")

if __name__ == "__main__":
    check_deployment_status()
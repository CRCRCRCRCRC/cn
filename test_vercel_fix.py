#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試 Vercel 部署修復
檢查 Flask 應用是否能正常運行，沒有 request context 錯誤
"""

import sys
import os

# 添加當前目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_app_import():
    """測試應用導入"""
    try:
        from vercel_app import app, User, AI_MODELS
        print("✅ 應用導入成功")
        return True
    except Exception as e:
        print(f"❌ 應用導入失敗: {e}")
        return False

def test_user_class():
    """測試 User 類別"""
    try:
        from vercel_app import User
        
        # 測試普通用戶
        user = User('test_id', 'test@example.com', 'Test User', '')
        print(f"✅ 普通用戶創建成功，積分: {user.credits}")
        
        # 測試開發者用戶
        dev_user = User('dev_id', 'dev@example.com', 'Dev User', '', is_dev=True)
        print(f"✅ 開發者用戶創建成功，積分: {dev_user.credits}")
        
        # 測試積分扣除
        result = user.deduct_credits(10)
        print(f"✅ 積分扣除測試: {result}, 剩餘積分: {user.credits}")
        
        # 測試 update_session_credits（在沒有 request context 的情況下）
        user.update_session_credits()
        print("✅ update_session_credits 在無 context 環境下正常運行")
        
        return True
    except Exception as e:
        print(f"❌ User 類別測試失敗: {e}")
        return False

def test_ai_models():
    """測試 AI 模型配置"""
    try:
        from vercel_app import AI_MODELS
        
        expected_models = [
            'gpt-4.1-nano-2025-04-14',
            'o4-mini-2025-04-16',
            'o3-2025-04-16',
            'o3-pro-2025-06-10',
            'o3-deep-research-2025-06-26',
            'o4-mini-deep-research-2025-06-26'
        ]
        
        for model in expected_models:
            if model not in AI_MODELS:
                print(f"❌ 缺少 AI 模型: {model}")
                return False
            print(f"✅ AI 模型 {model}: {AI_MODELS[model]} 積分")
        
        print(f"✅ 所有 {len(AI_MODELS)} 個 AI 模型配置正確")
        return True
    except Exception as e:
        print(f"❌ AI 模型測試失敗: {e}")
        return False

def test_flask_app():
    """測試 Flask 應用基本功能"""
    try:
        from vercel_app import app
        
        with app.test_client() as client:
            # 測試首頁
            response = client.get('/')
            if response.status_code == 200:
                print("✅ 首頁路由正常")
            else:
                print(f"❌ 首頁路由錯誤: {response.status_code}")
                return False
            
            # 測試登入頁面
            response = client.get('/login')
            if response.status_code == 200:
                print("✅ 登入頁面路由正常")
            else:
                print(f"❌ 登入頁面路由錯誤: {response.status_code}")
                return False
            
            # 測試開發者認證頁面
            response = client.get('/dev-auth')
            if response.status_code == 200:
                print("✅ 開發者認證頁面路由正常")
            else:
                print(f"❌ 開發者認證頁面路由錯誤: {response.status_code}")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Flask 應用測試失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("🚀 開始測試 Vercel 部署修復...")
    print("=" * 50)
    
    tests = [
        ("應用導入", test_app_import),
        ("User 類別", test_user_class),
        ("AI 模型配置", test_ai_models),
        ("Flask 應用", test_flask_app)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 測試: {test_name}")
        print("-" * 30)
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} 測試失敗")
    
    print("\n" + "=" * 50)
    print(f"🎯 測試結果: {passed}/{total} 通過 ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 所有測試通過！應用已準備好部署到 Vercel")
        return True
    else:
        print("⚠️  部分測試失敗，請檢查錯誤並修復")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
import os
import sys
import asyncio
import json
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import requests
from urllib.parse import urlencode
import threading
import time

# 添加父目錄到路徑以便導入模組
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analyzer.indicator_calculator import calculate_threat_indicators
from analyzer.report_generator import generate_ai_report
from scraper.data_collector import collect_all_data_sync

# 設定模板和靜態文件路徑
template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates')
static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = os.environ.get('SECRET_KEY', 'taiwan-defense-system-2025')

# 配置
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Flask-Login 設定
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 自定義未授權處理器，返回 JSON 而不是重定向
@login_manager.unauthorized_handler
def unauthorized():
    if request.is_json or request.path.startswith('/start_analysis'):
        return jsonify({'error': '請先登入系統'}), 401
    return redirect(url_for('login'))

# 用戶類別
class User(UserMixin):
    def __init__(self, id, email, name, picture, is_dev=False):
        self.id = id
        self.email = email
        self.name = name
        self.picture = picture
        self.is_dev = is_dev
        self.credits = 999999 if is_dev else self.get_monthly_credits()
    
    def get_monthly_credits(self):
        # 簡化版：每月1000積分，實際應該從資料庫讀取
        return 1000
    
    def deduct_credits(self, amount):
        if self.is_dev:
            return True
        if self.credits >= amount:
            self.credits -= amount
            return True
        return False
    
    def update_session_credits(self):
        """更新 session 中的積分（只在有 request context 時調用）"""
        try:
            from flask import has_request_context, session
            if has_request_context() and 'user_data' in session:
                session['user_data']['credits'] = self.credits
                session.modified = True
        except (RuntimeError, ImportError):
            # 沒有 request context 時忽略
            pass

# 全域變量存儲用戶
users = {}

@login_manager.user_loader
def load_user(user_id):
    # 在 Serverless 環境中，先嘗試從 session 恢復用戶
    if user_id not in users and 'user_data' in session:
        user_data = session['user_data']
        if user_data['id'] == user_id:
            user = User(
                user_data['id'],
                user_data['email'],
                user_data['name'],
                user_data['picture'],
                user_data.get('is_dev', False)
            )
            user.credits = user_data.get('credits', user.credits)
            users[user_id] = user
    
    return users.get(user_id)

# AI 模型配置
AI_MODELS = {
    'gpt-4.1-nano-2025-04-14': 2.5,
    'o4-mini-2025-04-16': 27.5,
    'o3-2025-04-16': 50,
    'o3-pro-2025-06-10': 500,
    'o3-deep-research-2025-06-26': 250,
    'o4-mini-deep-research-2025-06-26': 50
}

@app.route('/')
def index():
    return render_template('index.html', 
                         user=current_user if current_user.is_authenticated else None,
                         ai_models=AI_MODELS)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dev-auth', methods=['GET', 'POST'])
def dev_auth():
    if request.method == 'POST':
        test_code = request.form.get('test_code')
        if test_code == 'howard is a pig':
            # 創建開發者用戶
            dev_user = User('dev_user', 'dev@taiwan-defense.com', '開發團隊', '', is_dev=True)
            users['dev_user'] = dev_user
            
            # 保存到 session
            session['user_data'] = {
                'id': dev_user.id,
                'email': dev_user.email,
                'name': dev_user.name,
                'picture': dev_user.picture,
                'is_dev': dev_user.is_dev,
                'credits': dev_user.credits
            }
            
            login_user(dev_user)
            return redirect(url_for('index'))
        else:
            flash('此測試碼無法使用')
    return render_template('dev_auth.html')

@app.route('/auth/google')
def google_auth():
    # Google OAuth 重定向
    params = {
        'client_id': GOOGLE_CLIENT_ID,
        'redirect_uri': request.url_root + 'auth/google/callback',
        'scope': 'openid email profile',
        'response_type': 'code',
        'state': 'taiwan_defense_system'
    }
    auth_url = 'https://accounts.google.com/o/oauth2/auth?' + urlencode(params)
    return redirect(auth_url)

@app.route('/auth/google/callback')
def google_callback():
    code = request.args.get('code')
    if not code:
        flash('登入失敗')
        return redirect(url_for('login'))
    
    # 交換 access token
    token_data = {
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': request.url_root + 'auth/google/callback'
    }
    
    try:
        token_response = requests.post('https://oauth2.googleapis.com/token', data=token_data)
        token_json = token_response.json()
        access_token = token_json['access_token']
        
        # 獲取用戶信息
        user_response = requests.get(
            'https://www.googleapis.com/oauth2/v2/userinfo',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        user_info = user_response.json()
        
        # 創建用戶
        user = User(
            user_info['id'],
            user_info['email'],
            user_info['name'],
            user_info.get('picture', '')
        )
        users[user_info['id']] = user
        
        # 保存到 session
        session['user_data'] = {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'picture': user.picture,
            'is_dev': user.is_dev,
            'credits': user.credits
        }
        
        login_user(user)
        
        return redirect(url_for('index'))
    except Exception as e:
        flash('登入過程發生錯誤')
        return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    # 清除 session 中的用戶數據
    session.pop('user_data', None)
    return redirect(url_for('index'))

@app.route('/start_analysis', methods=['POST'])
@login_required
def start_analysis():
    try:
        # 確保請求包含 JSON 數據
        if not request.is_json:
            return jsonify({'error': '請求必須包含 JSON 數據'}), 400
        
        model = request.json.get('model', 'gpt-4.1-nano-2025-04-14')
        
        if model not in AI_MODELS:
            return jsonify({'error': '無效的AI模型'}), 400
        
        cost = AI_MODELS[model]
        
        # 檢查積分
        if not current_user.is_dev and current_user.credits < cost:
            return jsonify({'error': '積分不足'}), 400
        
        # 在 Serverless 環境中直接同步執行分析
        try:
            print("開始收集資料...")
            # 收集資料
            data = collect_all_data_sync()
            print("資料收集完成，開始計算威脅指標...")
            
            # 計算威脅指標
            indicators = calculate_threat_indicators(data)
            print("威脅指標計算完成，開始生成AI報告...")
            
            # 生成AI報告
            report = generate_ai_report(data, indicators, model)
            print("AI報告生成完成")
            
            # 扣除積分
            if not current_user.is_dev:
                current_user.deduct_credits(cost)
                print(f"積分已扣除: {cost}, 剩餘: {current_user.credits}")
            
            # 更新 session 中的積分
            current_user.update_session_credits()
            
            # 直接返回結果
            result = {
                'status': 'completed',
                'progress': 100,
                'result': {
                    'indicators': indicators,
                    'report': report,
                    'timestamp': datetime.now().isoformat()
                },
                'remaining_credits': current_user.credits
            }
            
            return jsonify(result)
            
        except Exception as e:
            import traceback
            error_details = f"分析執行錯誤: {str(e)}"
            print(f"錯誤詳情: {error_details}")
            print(f"追蹤: {traceback.format_exc()}")
            return jsonify({
                'status': 'error',
                'error': error_details,
                'remaining_credits': current_user.credits
            }), 500
    
    except Exception as e:
        return jsonify({'error': f'分析啟動失敗: {str(e)}'}), 500

# get_report 路由已移除，因為改為同步處理，直接在 start_analysis 中返回結果

# Vercel 需要的應用實例
application = app

if __name__ == '__main__':
    app.run(debug=True)
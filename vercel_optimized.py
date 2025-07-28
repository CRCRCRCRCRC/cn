# Vercel 優化版本
import os
import sys
import json
from datetime import datetime, timedelta

# 基礎導入
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash, has_request_context
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import requests
from urllib.parse import urlencode

# 添加當前目錄到路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 備用函數定義
def calculate_threat_indicators_fallback(data):
    """備用威脅指標計算"""
    return {
        'military_threat': 30.0,
        'economic_pressure': 25.0,
        'news_alert': 20.0,
        'overall_threat_probability': 25.0,
        'three_month_probabilities': {
            'month1': 20.0,
            'month2': 25.0,
            'month3': 28.0
        },
        'calculation_time': datetime.now().isoformat(),
        'source': 'fallback'
    }

def generate_ai_report_fallback(data, indicators, model):
    """備用AI報告生成"""
    return {
        'content': f"""# 台灣防衛情勢分析報告

## 綜合威脅評估
當前綜合威脅機率：{indicators['overall_threat_probability']}%

## 各項指標分析
- 軍事威脅指標：{indicators['military_threat']}%
- 經濟壓力指標：{indicators['economic_pressure']}%
- 新聞示警指標：{indicators['news_alert']}%

## 未來三個月預測
- 第一個月：{indicators['three_month_probabilities']['month1']}%
- 第二個月：{indicators['three_month_probabilities']['month2']}%
- 第三個月：{indicators['three_month_probabilities']['month3']}%

*注意：此為備用報告，建議檢查系統模組狀態*
""",
        'model_used': model,
        'generation_time': datetime.now().isoformat(),
        'source': 'fallback'
    }

def collect_all_data_sync_fallback():
    """備用數據收集"""
    return {
        "military": {
            "status": "fallback",
            "data": {"threat_level": "中等", "activity_count": 15}
        },
        "news": {
            "status": "fallback", 
            "economic_news": [
                {"title": "中美貿易關係持續關注", "source": "備用資料", "url": "#"}
            ],
            "diplomatic_news": [
                {"title": "兩岸關係發展動態", "source": "備用資料", "url": "#"}
            ],
            "public_opinion_news": [
                {"title": "台海情勢民意調查", "source": "備用資料", "url": "#"}
            ]
        },
        "economic": {
            "status": "fallback",
            "gold_price": {"price": 2050.0, "currency": "USD"},
            "wheat_price": {"price": 650.0, "currency": "USD"}
        },
        "timestamp": datetime.now().isoformat()
    }

# 嘗試導入自定義模組，失敗時使用備用函數
try:
    from analyzer.indicator_calculator import calculate_threat_indicators
except:
    calculate_threat_indicators = calculate_threat_indicators_fallback

try:
    from analyzer.report_generator import generate_ai_report
except:
    generate_ai_report = generate_ai_report_fallback

try:
    from scraper.data_collector import collect_all_data_sync
except:
    collect_all_data_sync = collect_all_data_sync_fallback

# Flask 應用設置
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = os.environ.get('SECRET_KEY', 'taiwan-defense-system-2025')

# Flask-Login 設定
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

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
        self.credits = 999999 if is_dev else 1000
    
    def deduct_credits(self, amount):
        if self.is_dev:
            return True
        if self.credits >= amount:
            self.credits -= amount
            return True
        return False

# 全域變量存儲用戶
users = {}

@login_manager.user_loader
def load_user(user_id):
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

@app.route('/google-auth')
def google_auth():
    # 暫時重定向到開發者認證，因為Google OAuth需要額外配置
    flash('Google 登入功能正在開發中，請使用開發者認證')
    return redirect(url_for('dev_auth'))

@app.route('/dev-auth', methods=['GET', 'POST'])
def dev_auth():
    if request.method == 'POST':
        test_code = request.form.get('test_code')
        if test_code == 'howard is a pig':
            dev_user = User('dev_user', 'dev@taiwan-defense.com', '開發團隊', '', is_dev=True)
            users['dev_user'] = dev_user
            
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

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user_data', None)
    return redirect(url_for('index'))

@app.route('/start_analysis', methods=['POST'])
@login_required
def start_analysis():
    try:
        if not request.is_json:
            return jsonify({'error': '請求必須包含 JSON 數據'}), 400
        
        model = request.json.get('model', 'gpt-4.1-nano-2025-04-14')
        
        if model not in AI_MODELS:
            return jsonify({'error': '無效的AI模型'}), 400
        
        cost = AI_MODELS[model]
        
        if not current_user.is_dev and current_user.credits < cost:
            return jsonify({'error': '積分不足'}), 400
        
        # 執行分析
        try:
            # 收集資料
            data = collect_all_data_sync()
            
            # 計算威脅指標
            indicators = calculate_threat_indicators(data)
            
            # 生成AI報告
            report = generate_ai_report(data, indicators, model)
            
            # 扣除積分
            if not current_user.is_dev:
                current_user.deduct_credits(cost)
            
            # 返回結果
            result = {
                'status': 'completed',
                'progress': 100,
                'result': {
                    'indicators': indicators,
                    'report': report,
                    'data': data,
                    'timestamp': datetime.now().isoformat()
                },
                'remaining_credits': current_user.credits
            }
            
            return jsonify(result)
            
        except Exception as e:
            return jsonify({
                'status': 'error',
                'error': f'分析執行錯誤: {str(e)}',
                'remaining_credits': current_user.credits
            }), 500
    
    except Exception as e:
        return jsonify({'error': f'分析啟動失敗: {str(e)}'}), 500

# Vercel 需要的應用實例
application = app

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, jsonify, request, render_template
import os

# 設定模板和靜態文件路徑
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = os.environ.get('SECRET_KEY', 'taiwan-defense-system-2025')

@app.route('/')
def index():
    try:
        return render_template('index.html', user=None, ai_models={
            'gpt-4.1-nano-2025-04-14': 2.5,
            'o4-mini-2025-04-16': 27.5,
            'o3-2025-04-16': 50
        })
    except Exception as e:
        return jsonify({'error': f'模板錯誤: {str(e)}'}), 500

@app.route('/login')
def login():
    try:
        return render_template('login.html')
    except Exception as e:
        return jsonify({'error': f'登入頁面錯誤: {str(e)}'}), 500

@app.route('/test_analysis', methods=['POST'])
def test_analysis():
    try:
        # 簡單的測試分析，不使用任何 session 或 login 功能
        return jsonify({
            'status': 'completed',
            'progress': 100,
            'result': {
                'indicators': {
                    'military_threat': 30.0,
                    'economic_pressure': 25.0,
                    'news_alert': 20.0,
                    'overall_threat_probability': 25.0,
                    'three_month_probabilities': {
                        'month1': 20.0,
                        'month2': 25.0,
                        'month3': 28.0
                    }
                },
                'report': {
                    'content': '# 測試報告\n\n這是一個簡化的測試報告，用於驗證系統基本功能。'
                }
            }
        })
    except Exception as e:
        import traceback
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

# Vercel 需要的應用實例
application = app

if __name__ == "__main__":
    app.run(debug=True)
import openai
import os
import json
from datetime import datetime

def generate_ai_report(collected_data, indicators, model_name):
    """生成AI綜合分析報告"""
    try:
        # 設定OpenAI API
        openai.api_key = os.environ.get('OPENAI_API_KEY')
        
        if not openai.api_key:
            return generate_template_report(indicators)
        
        # 準備提示詞
        prompt = create_analysis_prompt(collected_data, indicators)
        
        # 根據模型名稱選擇實際的OpenAI模型
        actual_model = map_to_openai_model(model_name)
        
        # 調用OpenAI API
        response = openai.ChatCompletion.create(
            model=actual_model,
            messages=[
                {"role": "system", "content": "你是一位專業的國防安全分析師，專門分析台海情勢。請提供客觀、專業的分析報告。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        
        ai_report = response.choices[0].message.content
        
        return {
            'content': ai_report,
            'model_used': model_name,
            'generation_time': datetime.now().isoformat(),
            'source': 'ai_generated'
        }
        
    except Exception as e:
        # 如果AI生成失敗，使用模板報告
        return generate_template_report(indicators, error=str(e))

def map_to_openai_model(model_name):
    """將自定義模型名稱映射到實際的OpenAI模型"""
    model_mapping = {
        'gpt-4.1-nano-2025-04-14': 'gpt-4',
        'o4-mini-2025-04-16': 'gpt-4',
        'o3-2025-04-16': 'gpt-4',
        'o3-pro-2025-06-10': 'gpt-4',
        'o3-deep-research-2025-06-26': 'gpt-4',
        'o4-mini-deep-research-2025-06-26': 'gpt-4'
    }
    return model_mapping.get(model_name, 'gpt-3.5-turbo')

def create_analysis_prompt(collected_data, indicators):
    """創建分析提示詞"""
    prompt = f"""
請基於以下數據進行台海情勢分析：

威脅指標：
- 軍事威脅指數：{indicators['military_threat']}%
- 經濟壓力指數：{indicators['economic_pressure']}%
- 新聞示警指數：{indicators['news_alert']}%
- 股市影響指數：{indicators['stock_impact']}%
- 綜合威脅機率：{indicators['overall_threat_probability']}%

近三個月攻台機率預測：
- 第一個月：{indicators['three_month_probabilities']['month1']}%
- 第二個月：{indicators['three_month_probabilities']['month2']}%
- 第三個月：{indicators['three_month_probabilities']['month3']}%

資料來源狀態：
- 軍事資料：{indicators['data_sources']['military_status']}
- 經濟資料：{indicators['data_sources']['economic_status']}
- 新聞資料：{indicators['data_sources']['news_status']}
- 股市資料：{indicators['data_sources']['stock_status']}

請提供一份專業的分析報告，包含：
1. 當前情勢評估
2. 主要風險因素
3. 趨勢分析
4. 建議關注重點

報告應該客觀、專業，避免過度渲染或恐慌。
"""
    return prompt

def generate_template_report(indicators, error=None):
    """生成模板報告（當AI不可用時）"""
    
    threat_level = get_threat_level(indicators['overall_threat_probability'])
    
    report_content = f"""
# 台灣防衛情勢分析報告

## 📊 當前威脅評估

根據最新收集的多源情報數據，當前台海情勢評估如下：

**綜合威脅機率：{indicators['overall_threat_probability']}% ({threat_level})**

### 各項指標分析

🔴 **軍事威脅指數：{indicators['military_threat']}%**
- 基於國防部軍事動態和相關軍事活動分析
- {get_military_analysis(indicators['military_threat'])}

🟡 **經濟壓力指數：{indicators['economic_pressure']}%**
- 基於黃金、農產品等避險資產價格變化
- {get_economic_analysis(indicators['economic_pressure'])}

🔵 **新聞示警指數：{indicators['news_alert']}%**
- 基於主流媒體報導的敏感詞彙分析
- {get_news_analysis(indicators['news_alert'])}

## 📈 近三個月攻台機率預測

- **第一個月：{indicators['three_month_probabilities']['month1']}%**
- **第二個月：{indicators['three_month_probabilities']['month2']}%**
- **第三個月：{indicators['three_month_probabilities']['month3']}%**

## 🎯 主要關注重點

{get_focus_points(indicators)}

## ⚠️ 風險提醒

本分析基於公開資訊和量化指標，僅供參考。實際情勢可能受到多種複雜因素影響，建議持續關注官方發布的權威資訊。

---
*報告生成時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*資料來源：多源情報整合分析*
"""

    if error:
        report_content += f"\n\n*注意：AI分析服務暫時不可用，使用模板報告。錯誤：{error}*"

    return {
        'content': report_content,
        'model_used': 'template',
        'generation_time': datetime.now().isoformat(),
        'source': 'template_generated'
    }

def get_threat_level(probability):
    """根據機率獲取威脅等級"""
    if probability >= 70:
        return "高度威脅"
    elif probability >= 50:
        return "中高威脅"
    elif probability >= 30:
        return "中等威脅"
    elif probability >= 15:
        return "低度威脅"
    else:
        return "極低威脅"

def get_military_analysis(score):
    """軍事威脅分析"""
    if score >= 60:
        return "軍事活動頻繁，需密切關注相關動態"
    elif score >= 40:
        return "軍事活動處於正常範圍，但有增加趨勢"
    elif score >= 20:
        return "軍事活動相對平穩"
    else:
        return "軍事威脅較低"

def get_economic_analysis(score):
    """經濟壓力分析"""
    if score >= 50:
        return "市場避險情緒濃厚，經濟不確定性增加"
    elif score >= 30:
        return "經濟指標顯示輕微壓力"
    else:
        return "經濟環境相對穩定"

def get_news_analysis(score):
    """新聞示警分析"""
    if score >= 50:
        return "媒體報導中敏感事件增多，輿論關注度高"
    elif score >= 30:
        return "新聞報導中出現一些關注議題"
    else:
        return "媒體報導相對平穩"

def get_focus_points(indicators):
    """獲取關注重點"""
    points = []
    
    if indicators['military_threat'] >= 50:
        points.append("• 密切關注軍事演習和部署動態")
    
    if indicators['economic_pressure'] >= 40:
        points.append("• 監控國際經濟制裁和貿易變化")
    
    if indicators['news_alert'] >= 40:
        points.append("• 關注國際媒體和官方聲明")
    
    if not points:
        points.append("• 維持正常警戒，持續監控各項指標")
    
    return "\n".join(points)
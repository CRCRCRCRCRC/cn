import json
import math
from datetime import datetime, timedelta
import re

def calculate_military_threat(military_data):
    """計算軍事威脅指標 (0-100)"""
    try:
        if military_data.get('status') != 'success':
            return 30  # 預設值，當無法獲取資料時
        
        threat_score = 0
        data = military_data.get('data', [])
        
        # 分析軍事動態關鍵字
        threat_keywords = ['演習', '軍演', '戰機', '軍艦', '導彈', '飛彈', '巡航', '警戒', '緊急']
        high_threat_keywords = ['入侵', '突破', '攻擊', '威脅', '挑釁', '對峙']
        
        keyword_count = 0
        high_threat_count = 0
        
        for item in data:
            content = str(item).lower()
            for keyword in threat_keywords:
                if keyword in content:
                    keyword_count += 1
            for keyword in high_threat_keywords:
                if keyword in content:
                    high_threat_count += 2
        
        # 計算基礎威脅分數
        base_score = min(keyword_count * 5 + high_threat_count * 10, 70)
        
        # 根據資料新鮮度調整
        if len(data) > 0:
            threat_score = base_score + 10
        else:
            threat_score = 25
        
        return min(max(threat_score, 0), 100)
        
    except Exception as e:
        return 35  # 錯誤時返回中等威脅值

def calculate_economic_pressure(economic_data):
    """計算經濟壓力指標 (0-100)"""
    try:
        if economic_data.get('status') != 'success':
            return 25
        
        pressure_score = 0
        data = economic_data.get('data', {})
        
        # 分析黃金價格變化（避險情緒指標）
        if 'gold' in data or 'GC=F' in data:
            pressure_score += 15  # 有黃金數據表示市場關注避險
        
        # 分析農產品價格（糧食安全指標）
        commodity_count = 0
        for commodity in ['ZS=F', 'ZW=F', 'ZC=F']:  # 黃豆、小麥、玉米
            if commodity in data:
                commodity_count += 1
        
        pressure_score += commodity_count * 8
        
        # 基礎經濟壓力
        base_pressure = 20
        total_score = base_pressure + pressure_score
        
        return min(max(total_score, 0), 100)
        
    except Exception as e:
        return 30

def calculate_news_alert(news_data):
    """計算新聞示警指標 (0-100)"""
    try:
        if news_data.get('status') != 'success':
            return 20
        
        alert_score = 0
        articles = news_data.get('data', [])
        
        # 分析新聞標題和內容的敏感詞彙
        alert_keywords = ['緊張', '衝突', '對立', '制裁', '軍事', '戰爭', '危機', '威脅']
        high_alert_keywords = ['開火', '攻擊', '入侵', '戰爭', '軍事行動', '緊急狀態']
        
        keyword_score = 0
        high_alert_score = 0
        
        for article in articles:
            title = article.get('title', '').lower()
            description = article.get('description', '').lower()
            content = title + ' ' + description
            
            for keyword in alert_keywords:
                if keyword in content:
                    keyword_score += 3
            
            for keyword in high_alert_keywords:
                if keyword in content:
                    high_alert_score += 8
        
        # 計算總分
        total_score = min(keyword_score + high_alert_score, 80)
        
        # 根據新聞數量調整
        if len(articles) > 10:
            total_score += 10
        elif len(articles) > 5:
            total_score += 5
        
        return min(max(total_score, 0), 100)
        
    except Exception as e:
        return 25

def calculate_stock_impact(stock_data):
    """計算股市影響指標"""
    try:
        if stock_data.get('status') != 'success':
            return 0
        
        # 簡化的股市分析
        return 15  # 基礎影響分數
        
    except Exception as e:
        return 0

def calculate_threat_indicators(collected_data):
    """計算所有威脅指標"""
    try:
        # 計算各項指標
        military_threat = calculate_military_threat(collected_data.get('military', {}))
        economic_pressure = calculate_economic_pressure(collected_data.get('economic', {}))
        news_alert = calculate_news_alert(collected_data.get('news', {}))
        stock_impact = calculate_stock_impact(collected_data.get('stock', {}))
        
        # 計算綜合威脅機率（加權平均）
        weights = {
            'military': 0.4,    # 軍事威脅權重40%
            'economic': 0.25,   # 經濟壓力權重25%
            'news': 0.25,       # 新聞示警權重25%
            'stock': 0.1        # 股市影響權重10%
        }
        
        overall_threat = (
            military_threat * weights['military'] +
            economic_pressure * weights['economic'] +
            news_alert * weights['news'] +
            stock_impact * weights['stock']
        )
        
        # 計算近三個月攻台機率（基於歷史趨勢模擬）
        base_probability = overall_threat * 0.6  # 基礎機率
        
        # 模擬三個月的機率變化
        month1_prob = max(base_probability - 5, 0)
        month2_prob = base_probability
        month3_prob = min(base_probability + 3, 100)
        
        return {
            'military_threat': round(military_threat, 1),
            'economic_pressure': round(economic_pressure, 1),
            'news_alert': round(news_alert, 1),
            'stock_impact': round(stock_impact, 1),
            'overall_threat_probability': round(overall_threat, 1),
            'three_month_probabilities': {
                'month1': round(month1_prob, 1),
                'month2': round(month2_prob, 1),
                'month3': round(month3_prob, 1)
            },
            'calculation_time': datetime.now().isoformat(),
            'data_sources': {
                'military_status': collected_data.get('military', {}).get('status', 'unknown'),
                'economic_status': collected_data.get('economic', {}).get('status', 'unknown'),
                'news_status': collected_data.get('news', {}).get('status', 'unknown'),
                'stock_status': collected_data.get('stock', {}).get('status', 'unknown')
            }
        }
        
    except Exception as e:
        # 錯誤時返回預設值
        return {
            'military_threat': 30.0,
            'economic_pressure': 25.0,
            'news_alert': 20.0,
            'stock_impact': 10.0,
            'overall_threat_probability': 25.0,
            'three_month_probabilities': {
                'month1': 20.0,
                'month2': 25.0,
                'month3': 28.0
            },
            'calculation_time': datetime.now().isoformat(),
            'error': str(e)
        }
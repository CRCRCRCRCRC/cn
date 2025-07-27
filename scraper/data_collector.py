import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

def collect_all_data_sync():
    """同步收集所有數據"""
    try:
        print("開始收集數據...")
        
        # 收集軍事新聞
        military_data = collect_military_data_sync()
        
        # 收集一般新聞
        news_data = collect_news_data_sync()
        
        # 收集經濟數據
        economic_data = collect_economic_data_sync()
        
        all_data = {
            "military": military_data,
            "news": news_data,
            "economic": economic_data,
            "timestamp": datetime.now().isoformat()
        }
        
        print("數據收集完成")
        return all_data
        
    except Exception as e:
        print(f"數據收集錯誤: {e}")
        return {"error": str(e), "timestamp": datetime.now().isoformat()}

def collect_military_data_sync():
    """收集軍事新聞數據 (同步版本)"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # 模擬軍事新聞數據
        military_news = [
            {
                "title": "國防部例行記者會",
                "source": "國防部",
                "timestamp": datetime.now().isoformat()
            },
            {
                "title": "軍事演習進行中",
                "source": "國防部",
                "timestamp": datetime.now().isoformat()
            }
        ]
        
        return {
            "news": military_news,
            "source": "國防部",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"軍事數據收集錯誤: {e}")
        return {"error": str(e), "timestamp": datetime.now().isoformat()}

def collect_news_data_sync():
    """收集新聞數據 (同步版本) - 使用 Google News"""
    try:
        print("正在從 Google 新聞抓取相關新聞...")
        
        # 使用 Google News 抓取新聞
        news_data = scrape_google_news()
        
        # 整理新聞格式
        all_news = []
        
        # 合併所有類型的新聞
        for category in ['economic_news', 'diplomatic_news', 'public_opinion_news']:
            if category in news_data:
                for article in news_data[category]:
                    all_news.append({
                        "title": article.get('title', ''),
                        "source": article.get('source', '未知來源'),
                        "url": article.get('url', ''),
                        "published_date": article.get('published_date', ''),
                        "category": category.replace('_news', ''),
                        "timestamp": datetime.now().isoformat()
                    })
        
        return {
            "news": all_news,
            "economic_news": news_data.get('economic_news', []),
            "diplomatic_news": news_data.get('diplomatic_news', []),
            "public_opinion_news": news_data.get('public_opinion_news', []),
            "sources": news_data.get('sources', []),
            "total_count": news_data.get('total_articles', len(all_news)),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"新聞數據收集錯誤: {e}")
        return get_fallback_news_data()

def scrape_google_news():
    """從 Google 新聞抓取與中國相關的新聞資料"""
    from urllib.parse import quote_plus, urljoin
    import logging
    
    # Google News 基礎 URL
    GOOGLE_NEWS_URL = "https://news.google.com"
    
    try:
        # 定義搜尋關鍵字
        economic_keywords = ["中國經濟", "中美貿易", "台海經濟", "兩岸貿易"]
        diplomatic_keywords = ["中國外交", "兩岸關係", "台海情勢", "中美關係"]
        opinion_keywords = ["中國輿情", "兩岸民意", "台海局勢", "中國社會"]
        
        economic_news = []
        diplomatic_news = []
        public_opinion_news = []
        sources = []
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # 搜尋經濟相關新聞
        for keyword in economic_keywords[:2]:  # 限制搜尋數量避免超時
            articles = search_google_news(keyword, headers, GOOGLE_NEWS_URL)
            economic_news.extend(articles)
            
        # 搜尋外交相關新聞
        for keyword in diplomatic_keywords[:2]:
            articles = search_google_news(keyword, headers, GOOGLE_NEWS_URL)
            diplomatic_news.extend(articles)
            
        # 搜尋輿情相關新聞
        for keyword in opinion_keywords[:2]:
            articles = search_google_news(keyword, headers, GOOGLE_NEWS_URL)
            public_opinion_news.extend(articles)
        
        # 收集所有來源
        all_articles = economic_news + diplomatic_news + public_opinion_news
        sources = list(set([article['source'] for article in all_articles if article['source']]))
        
        # 如果沒有抓到新聞，提供備用資料
        if not all_articles:
            print("無法從 Google 新聞抓取到任何文章，使用備用資料")
            return get_fallback_news_data()
        
        return {
            "economic_news": economic_news[:5],  # 限制數量
            "diplomatic_news": diplomatic_news[:5],
            "public_opinion_news": public_opinion_news[:5],
            "sources": sources[:10],  # 限制來源數量
            "total_articles": len(all_articles)
        }
        
    except Exception as e:
        print(f"抓取新聞資料時發生錯誤: {e}")
        return get_fallback_news_data()

def search_google_news(query, headers, base_url):
    """輔助函式，用於搜尋特定關鍵字的 Google 新聞"""
    from urllib.parse import quote_plus, urljoin
    
    try:
        formatted_query = quote_plus(query)
        search_url = f"{base_url}/search?q={formatted_query}&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
        
        response = requests.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = []
        # Google News 的 HTML 結構可能會變，此選擇器相對穩定
        for article_div in soup.find_all('div', {'class': 'SoaBEf'}, limit=8):
            try:
                link_tag = article_div.find('a', href=True)
                title_tag = article_div.find('div', attrs={'role': 'heading'})
                time_tag = article_div.find('time')
                
                # 抓取來源資訊
                source_tag = article_div.find('div', attrs={'data-n-tid': lambda x: x and 'source' in x})
                
                if link_tag and title_tag:
                    # Google News 的連結需要處理
                    href = link_tag.get('href', '')
                    if href.startswith('./'):
                        href = href[2:]  # 移除 './'
                    full_url = urljoin(base_url, href)
                    
                    article = {
                        'title': title_tag.get_text(strip=True),
                        'url': full_url,
                        'published_date': time_tag.get('datetime', '') if time_tag else '',
                        'source': source_tag.get_text(strip=True) if source_tag else '未知來源'
                    }
                    articles.append(article)
            except:
                continue

        return articles

    except Exception as e:
        print(f"搜尋 Google 新聞時發生錯誤 (查詢: {query}): {e}")
        return []

def get_fallback_news_data():
    """提供備用新聞資料"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    fallback_articles = [
        {
            'title': '中美貿易關係持續關注中',
            'url': '#',
            'published_date': current_time,
            'source': '財經新聞'
        },
        {
            'title': '兩岸關係發展備受矚目',
            'url': '#',
            'published_date': current_time,
            'source': '政治新聞'
        },
        {
            'title': '台海局勢持續穩定發展',
            'url': '#',
            'published_date': current_time,
            'source': '國際新聞'
        }
    ]
    
    return {
        "economic_news": [fallback_articles[0]],
        "diplomatic_news": [fallback_articles[1]],
        "public_opinion_news": [fallback_articles[2]],
        "sources": ['財經新聞', '政治新聞', '國際新聞'],
        "total_articles": 3,
        "error": "Using fallback data"
    }

def collect_economic_data_sync():
    """收集經濟指標數據 (同步版本)"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # 黃金價格
        gold_data = fetch_investing_price_sync("https://www.investing.com/commodities/gold", "黃金", headers)
        
        # 小麥價格
        wheat_data = fetch_investing_price_sync("https://www.investing.com/commodities/us-wheat", "小麥", headers)
        
        economic_data = {
            "gold_price": gold_data,
            "wheat_price": wheat_data,
            "timestamp": datetime.now().isoformat()
        }
        
        return economic_data
        
    except Exception as e:
        print(f"經濟數據收集錯誤: {e}")
        return {"error": str(e), "timestamp": datetime.now().isoformat()}

def fetch_investing_price_sync(url, commodity_name, headers):
    """從 investing.com 獲取商品價格 (同步版本)"""
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 尋找價格元素
            price_element = soup.find('span', {'data-test': 'instrument-price-last'}) or \
                           soup.find('span', class_='text-2xl') or \
                           soup.find('div', class_='text-5xl')
            
            if price_element:
                price_text = price_element.get_text().strip()
                import re
                price_match = re.search(r'[\d,]+\.?\d*', price_text)
                if price_match:
                    price = float(price_match.group().replace(',', ''))
                    return {
                        "name": commodity_name,
                        "price": price,
                        "currency": "USD",
                        "source": "investing.com"
                    }
            
            # 如果無法獲取實際價格，返回模擬數據
            if commodity_name == "黃金":
                return {
                    "name": commodity_name,
                    "price": 2050.0,
                    "currency": "USD",
                    "source": "investing.com (模擬)"
                }
            elif commodity_name == "小麥":
                return {
                    "name": commodity_name,
                    "price": 650.0,
                    "currency": "USD",
                    "source": "investing.com (模擬)"
                }
            
            return {"name": commodity_name, "error": "價格元素未找到", "source": "investing.com"}
        else:
            # 返回模擬數據
            if commodity_name == "黃金":
                return {
                    "name": commodity_name,
                    "price": 2050.0,
                    "currency": "USD",
                    "source": "investing.com (模擬)"
                }
            elif commodity_name == "小麥":
                return {
                    "name": commodity_name,
                    "price": 650.0,
                    "currency": "USD",
                    "source": "investing.com (模擬)"
                }
            return {"name": commodity_name, "error": f"HTTP {response.status_code}", "source": "investing.com"}
            
    except Exception as e:
        # 返回模擬數據
        if commodity_name == "黃金":
            return {
                "name": commodity_name,
                "price": 2050.0,
                "currency": "USD",
                "source": "investing.com (模擬)"
            }
        elif commodity_name == "小麥":
            return {
                "name": commodity_name,
                "price": 650.0,
                "currency": "USD",
                "source": "investing.com (模擬)"
            }
        return {"name": commodity_name, "error": str(e), "source": "investing.com"}
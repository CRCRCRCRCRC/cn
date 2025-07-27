# 台灣防衛情勢感知系統

一個即時蒐集多源情報、量化威脅並產生AI綜合分析報告的賽博龐克風格系統。

## 功能特色

- 🛡️ **多源情報收集**：整合軍事動態、新聞輿情、經濟指標
- 🤖 **AI智能分析**：支援多種AI模型進行深度威脅評估
- 📊 **即時視覺化**：賽博龐克風格儀表板，直觀呈現威脅態勢
- 🔐 **Google登入**：安全的OAuth 2.0身份驗證
- 💰 **積分制度**：月度積分管理，不同AI模型不同消耗
- 📱 **響應式設計**：支援桌面和行動裝置

## 技術架構

### 後端
- **Flask**：Web框架
- **Python**：爬蟲和資料分析
- **OpenAI API**：AI報告生成
- **Google OAuth**：用戶身份驗證

### 前端
- **HTML5/CSS3**：賽博龐克風格UI
- **JavaScript**：動態交互和AJAX
- **響應式設計**：適配各種螢幕尺寸

### 部署
- **Vercel**：Serverless部署平台
- **環境變數**：安全的配置管理

## 快速開始

### 1. 環境設定

```bash
# 複製環境變數範例
cp .env.example .env

# 編輯 .env 文件，填入實際的API密鑰
```

### 2. 本地開發

```bash
# 安裝依賴
pip install -r requirements.txt

# 啟動開發伺服器
python api/app.py
```

### 3. Vercel部署

1. 將專案推送到GitHub
2. 在Vercel中連接GitHub倉庫
3. 設定環境變數
4. 一鍵部署

## 環境變數配置

| 變數名稱 | 說明 | 必需 |
|---------|------|------|
| `SECRET_KEY` | Flask應用密鑰 | ✅ |
| `GOOGLE_CLIENT_ID` | Google OAuth客戶端ID | ✅ |
| `GOOGLE_CLIENT_SECRET` | Google OAuth客戶端密鑰 | ✅ |
| `OPENAI_API_KEY` | OpenAI API密鑰 | ✅ |
| `NEWS_API_KEY` | News API密鑰 | ❌ |

## AI模型與積分

| 模型名稱 | 積分消耗 | 說明 |
|---------|---------|------|
| gpt-4.1-nano-2025-04-14 | 2.5 | 基礎模型 |
| o4-mini-2025-04-16 | 27.5 | 進階模型 |
| o3-2025-04-16 | 50 | 高級模型 |
| o3-pro-2025-06-10 | 500 | 專業模型 |
| o3-deep-research-2025-06-26 | 250 | 深度研究模型 |
| o4-mini-deep-research-2025-06-26 | 50 | 迷你深度研究模型 |

## 開發者測試

系統提供開發者測試入口：
- 測試碼：`howard is a pig`
- 功能：無限積分，無需Google登入

## 專案結構

```
/
├── api/                    # Vercel Serverless Functions
│   └── app.py             # 主應用程式
├── analyzer/              # 威脅分析模組
│   ├── indicator_calculator.py
│   └── report_generator.py
├── scraper/               # 資料收集模組
│   └── data_collector.py
├── static/                # 靜態資源
│   ├── css/style.css
│   └── js/main.js
├── templates/             # HTML模板
│   ├── index.html
│   ├── login.html
│   └── dev_auth.html
├── requirements.txt       # Python依賴
├── vercel.json           # Vercel配置
└── .env.example          # 環境變數範例
```

## 安全注意事項

- 所有API密鑰都通過環境變數管理
- 使用Google OAuth進行安全身份驗證
- 積分制度防止API濫用
- 開發者測試碼僅供開發使用

## 貢獻指南

1. Fork 專案
2. 建立功能分支
3. 提交變更
4. 發起 Pull Request

## 授權

本專案僅供學術研究和教育用途。

## 聯絡資訊

如有問題或建議，請通過GitHub Issues聯絡。
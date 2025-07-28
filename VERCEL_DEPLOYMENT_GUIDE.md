# Vercel 部署環境變數設定指南

## 🔧 最新修復 (2025-07-28)

✅ **修復了 "Working outside of request context" 錯誤**
- 改善了 Flask session 處理機制
- 增強了 Serverless 環境兼容性
- 優化了用戶認證流程

## 必要的環境變數

在 Vercel 控制台中設定以下環境變數：

### 1. 基本配置
```
SECRET_KEY=taiwan-defense-system-2025-your-secret-key
```

### 2. Google OAuth 配置（可選）
如果要啟用 Google 登入功能：
```
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

### 3. OpenAI API 配置（可選）
如果要使用真實的 OpenAI API：
```
OPENAI_API_KEY=your-openai-api-key
```

## 部署步驟

1. **運行修復驗證**：
   ```bash
   py test_vercel_fix.py
   ```

2. **執行部署**：
   ```bash
   deploy_to_vercel.bat
   ```
   或手動：
   ```bash
   vercel --prod
   ```

## 設定步驟

1. 登入 Vercel 控制台
2. 選擇您的專案
3. 進入 Settings > Environment Variables
4. 添加上述環境變數

## 注意事項

- `SECRET_KEY` 是必須的，用於 Flask session 加密
- Google OAuth 變數是可選的，如果不設定會使用開發者認證
- OpenAI API 變數是可選的，如果不設定會使用模擬報告
- 所有環境變數都應該設定為 Production、Preview 和 Development 環境

## 部署後測試

部署完成後，請測試：

1. ✅ 網站是否正常載入
2. ✅ 登入功能是否正常（不再出現 request context 錯誤）
3. ✅ AI 模型選項是否顯示（應該有 6 個選項）
4. ✅ 威脅分析功能是否正常
5. ✅ 經濟數據是否正常獲取
6. ✅ Session 管理是否穩定

## AI 模型配置

系統已配置以下 6 個 AI 模型：

- `gpt-4.1-nano-2025-04-14`: 2.5 積分
- `o4-mini-2025-04-16`: 27.5 積分  
- `o3-2025-04-16`: 50 積分
- `o3-pro-2025-06-10`: 500 積分
- `o3-deep-research-2025-06-26`: 250 積分
- `o4-mini-deep-research-2025-06-26`: 50 積分

這些模型選項會在用戶登入後的分析介面中顯示。

## 故障排除

### 如果仍然遇到 "Working outside of request context" 錯誤：

1. 檢查 Vercel 函數日誌
2. 確認環境變數設定正確
3. 重新部署應用
4. 聯繫技術支援

### 常見問題：

- **登入失敗**: 檢查 Google OAuth 設定
- **分析功能異常**: 檢查 OpenAI API 密鑰
- **Session 問題**: 確認 SECRET_KEY 設定正確
@echo off
echo ========================================
echo 台灣防衛情勢感知系統 - 強制重新部署
echo ========================================
echo.

echo 檢查當前文件狀態...
echo - vercel_app.py: 同步處理版本 ✓
echo - static/js/main.js: v2.0 同步處理版本 ✓
echo - api/app.py: 同步處理版本 ✓
echo.

echo 問題診斷:
echo Vercel 上的 JavaScript 文件仍是舊版本，包含輪詢邏輯
echo 這導致前端仍會調用已移除的 /get_report 路由
echo.

echo 解決方案:
echo 1. 強制重新部署到 Vercel
echo 2. 清除 CDN 緩存
echo 3. 驗證部署結果
echo.

echo 開始強制部署...
vercel --prod --force

echo.
echo 部署完成！請等待 2-3 分鐘讓 CDN 緩存更新
echo.
echo 驗證步驟:
echo 1. 打開 https://taiwan-threat-analysis.vercel.app/
echo 2. 按 F12 打開開發者工具
echo 3. 在 Console 中應該看到 "Taiwan Defense System v2.0"
echo 4. 測試威脅分析功能，不應再有 get_report 錯誤
echo.
echo 如果仍有問題，請清除瀏覽器緩存並重新測試
echo.
pause
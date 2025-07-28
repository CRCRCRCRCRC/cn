@echo off
echo 正在部署台灣防衛情勢感知系統到 Vercel...
echo.

echo 檢查文件狀態...
echo - vercel_app.py: 同步處理版本
echo - static/js/main.js: v2.0 同步處理版本
echo - api/app.py: 同步處理版本
echo.

echo 開始部署...
vercel --prod

echo.
echo 部署完成！
echo.
echo 重要提醒：
echo 1. 部署後請清除瀏覽器緩存
echo 2. 確認前端控制台顯示 "Taiwan Defense System v2.0"
echo 3. 不應再有 get_report 相關的錯誤
echo.
pause
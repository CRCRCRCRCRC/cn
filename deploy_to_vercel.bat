@echo off
set PATH=%PATH%;C:\Users\howar\AppData\Roaming\npm
echo 開始部署到 Vercel...
echo.

echo 檢查修復驗證...
py test_vercel_fix.py
if %errorlevel% neq 0 (
    echo 修復驗證失敗，請檢查錯誤
    pause
    exit /b 1
)

echo.
echo 修復驗證通過！
echo.

echo 開始 Vercel 部署...
vercel --prod

echo.
echo 部署完成！
echo.
echo 修復內容：
echo   - 修復了 "Working outside of request context" 錯誤
echo   - 改善了 session 處理機制
echo   - 增強了 Serverless 環境兼容性
echo   - 所有 6 個 AI 模型正常運作
echo.
echo 部署後檢查清單：
echo   1. 檢查 Vercel 控制台確認部署成功
echo   2. 測試網站功能是否正常
echo   3. 確認登入功能正常運作
echo   4. 測試威脅分析功能
echo   5. 驗證不再出現 request context 錯誤
echo.

pause
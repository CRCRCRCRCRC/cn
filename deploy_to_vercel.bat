@echo off
echo 🚀 開始部署到 Vercel...
echo.

echo 📋 檢查部署前測試...
py test_vercel_deploy.py
if %errorlevel% neq 0 (
    echo ❌ 部署前測試失敗，請修復問題後再試
    pause
    exit /b 1
)

echo.
echo ✅ 部署前測試通過！
echo.

echo 📦 開始 Vercel 部署...
vercel --prod

echo.
echo 🎉 部署完成！
echo.
echo 📝 部署後檢查清單：
echo   1. 檢查 Vercel 控制台確認部署成功
echo   2. 測試網站功能是否正常
echo   3. 確認所有 6 個 AI 模型選項都顯示
echo   4. 測試登入功能
echo   5. 測試威脅分析功能
echo.

pause
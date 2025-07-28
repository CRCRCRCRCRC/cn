# Vercel 部署腳本
Write-Host "開始部署到 Vercel..." -ForegroundColor Green
Write-Host ""

# 添加 npm 路徑到環境變數
$env:PATH += ";C:\Users\howar\AppData\Roaming\npm"

Write-Host "檢查修復驗證..." -ForegroundColor Yellow
python test_vercel_fix.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "修復驗證失敗，請檢查錯誤" -ForegroundColor Red
    Read-Host "按 Enter 鍵繼續"
    exit 1
}

Write-Host ""
Write-Host "修復驗證通過！" -ForegroundColor Green
Write-Host ""

Write-Host "開始 Vercel 部署..." -ForegroundColor Yellow
vercel --prod

Write-Host ""
Write-Host "部署完成！" -ForegroundColor Green
Write-Host ""
Write-Host "修復內容：" -ForegroundColor Cyan
Write-Host "  - 修復了 'Working outside of request context' 錯誤"
Write-Host "  - 改善了 session 處理機制"
Write-Host "  - 增強了 Serverless 環境兼容性"
Write-Host "  - 所有 6 個 AI 模型正常運作"
Write-Host ""
Write-Host "部署後檢查清單：" -ForegroundColor Cyan
Write-Host "  1. 檢查 Vercel 控制台確認部署成功"
Write-Host "  2. 測試網站功能是否正常"
Write-Host "  3. 確認登入功能正常運作"
Write-Host "  4. 測試威脅分析功能"
Write-Host "  5. 驗證不再出現 request context 錯誤"
Write-Host ""

Read-Host "按 Enter 鍵繼續"
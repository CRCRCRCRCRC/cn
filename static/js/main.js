// 台灣防衛情勢感知系統 - 主要JavaScript文件
// 版本: 2.1 - 同步處理版本 (2025-07-28 15:30)
// 注意：此版本已移除所有異步任務輪詢，改為同步處理
// 部署時間戳: 20250728153000

console.log('Taiwan Defense System v2.1 - Synchronous Processing Version Loaded - Deploy: 20250728153000');
console.log('✅ 已移除所有 get_report 和輪詢邏輯');
console.log('✅ 改為同步處理威脅分析');

class ThreatAnalysisSystem {
    constructor() {
        this.init();
    }

    init() {
        this.bindEvents();
        this.initializeAnimations();
    }

    bindEvents() {
        // 開始分析按鈕
        const startBtn = document.getElementById('start-analysis');
        if (startBtn) {
            startBtn.addEventListener('click', () => this.startAnalysis());
        }

        // 演示按鈕（未登入用戶）
        const demoBtn = document.getElementById('start-demo');
        if (demoBtn) {
            demoBtn.addEventListener('click', () => this.showLoginModal());
        }

        // AI模型選擇
        const modelSelect = document.getElementById('ai-model');
        if (modelSelect) {
            modelSelect.addEventListener('change', () => this.updateModelCost());
        }
    }

    initializeAnimations() {
        // 初始化掃描線動畫
        this.animateScanLines();
        
        // 初始化進度圓環
        this.initializeProgressCircles();
    }

    animateScanLines() {
        const scanLines = document.querySelector('.scan-lines');
        if (scanLines) {
            // 掃描線已通過CSS動畫實現
        }
    }

    initializeProgressCircles() {
        const circles = document.querySelectorAll('.circular-progress');
        circles.forEach(circle => {
            this.updateProgressCircle(circle, 0);
        });
    }

    updateProgressCircle(circle, percentage) {
        const progressFill = circle.querySelector('.progress-fill');
        const progressText = circle.querySelector('.progress-text');
        
        if (progressFill && progressText) {
            const degrees = (percentage / 100) * 360;
            progressFill.style.background = `conic-gradient(
                var(--primary-color) ${degrees}deg,
                rgba(0, 255, 255, 0.1) ${degrees}deg
            )`;
            progressText.textContent = `${percentage}%`;
            
            // 根據威脅等級改變顏色
            let color = 'var(--success-color)';
            if (percentage >= 70) color = 'var(--danger-color)';
            else if (percentage >= 50) color = 'var(--warning-color)';
            else if (percentage >= 30) color = 'var(--primary-color)';
            
            progressText.style.color = color;
        }
    }

    updateModelCost() {
        const modelSelect = document.getElementById('ai-model');
        const selectedOption = modelSelect.options[modelSelect.selectedIndex];
        const cost = selectedOption.dataset.cost;
        
        // 可以在這裡顯示成本信息
        console.log(`選擇的模型成本: ${cost} 積分`);
    }

    async startAnalysis() {
        const modelSelect = document.getElementById('ai-model');
        const selectedModel = modelSelect.value;
        
        try {
            // 顯示載入動畫
            this.showLoading();
            
            // 發送分析請求（同步執行）
            const response = await fetch('/start_analysis', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    model: selectedModel
                })
            });

            // 檢查響應是否為 JSON
            const contentType = response.headers.get('content-type');
            if (!contentType || !contentType.includes('application/json')) {
                throw new Error('伺服器返回非 JSON 響應，可能需要重新登入');
            }

            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || '分析請求失敗');
            }

            // 更新積分顯示
            this.updateCredits(data.remaining_credits);
            
            // 檢查分析結果
            if (data.status === 'completed' && data.result) {
                // 處理完成的結果
                this.handleAnalysisComplete(data.result);
            } else if (data.status === 'error') {
                throw new Error(data.error || '分析過程發生錯誤');
            } else {
                throw new Error('分析結果格式異常');
            }
            
        } catch (error) {
            this.hideLoading();
            this.showError(error.message);
        }
    }

    handleAnalysisComplete(result) {
        console.log('分析完成，結果:', result);
        
        // 隱藏載入動畫
        this.hideLoading();
        
        // 顯示儀表板
        this.showDashboard();
        
        // 更新威脅指標
        this.updateThreatIndicators(result.indicators);
        
        // 更新經濟數據
        this.updateEconomicData(result.data);
        
        // 顯示AI報告
        this.showReport(result.report);
        
        // 播放完成動畫
        this.playCompletionAnimation();
    }

    showDashboard() {
        const dashboard = document.getElementById('dashboard');
        if (dashboard) {
            dashboard.style.display = 'block';
            dashboard.scrollIntoView({ behavior: 'smooth' });
        }
    }

    updateThreatIndicators(indicators) {
        // 更新各項威脅指標
        const indicatorMap = {
            'military': indicators.military_threat,
            'economic': indicators.economic_pressure,
            'news': indicators.news_alert
        };

        Object.entries(indicatorMap).forEach(([type, value]) => {
            const circle = document.querySelector(`[data-indicator="${type}"]`);
            if (circle) {
                this.animateProgressCircle(circle, value);
            }
        });

        // 更新綜合威脅機率
        this.updateOverallThreat(indicators.overall_threat_probability);
        
        // 更新月度機率
        this.updateMonthlyProbabilities(indicators.three_month_probabilities);
    }

    animateProgressCircle(circle, targetValue) {
        let currentValue = 0;
        const increment = targetValue / 50; // 50步動畫
        
        const animation = setInterval(() => {
            currentValue += increment;
            if (currentValue >= targetValue) {
                currentValue = targetValue;
                clearInterval(animation);
            }
            this.updateProgressCircle(circle, Math.round(currentValue));
        }, 50);
    }

    updateOverallThreat(probability) {
        const meterFill = document.getElementById('overall-meter');
        const percentageText = document.getElementById('overall-percentage');
        
        if (meterFill && percentageText) {
            // 動畫更新
            let currentWidth = 0;
            const targetWidth = probability;
            const increment = targetWidth / 50;
            
            const animation = setInterval(() => {
                currentWidth += increment;
                if (currentWidth >= targetWidth) {
                    currentWidth = targetWidth;
                    clearInterval(animation);
                }
                
                meterFill.style.width = `${currentWidth}%`;
                percentageText.textContent = `${Math.round(currentWidth)}%`;
            }, 50);
        }
    }

    updateMonthlyProbabilities(probabilities) {
        const months = ['month1', 'month2', 'month3'];
        
        months.forEach((month, index) => {
            const element = document.getElementById(`${month}-prob`);
            if (element) {
                setTimeout(() => {
                    this.animateNumber(element, probabilities[month]);
                }, index * 200); // 錯開動畫時間
            }
        });
    }

    updateEconomicData(data) {
        console.log('更新經濟數據:', data);
        
        if (data && data.economic) {
            const economic = data.economic;
            
            // 更新黃金價格
            if (economic.gold_price) {
                const goldElement = document.getElementById('gold-price');
                if (goldElement) {
                    const price = economic.gold_price.price || economic.gold_price;
                    this.animateEconomicValue(goldElement, price, '$');
                }
            }
            
            // 更新小麥價格
            if (economic.wheat_price) {
                const wheatElement = document.getElementById('wheat-price');
                if (wheatElement) {
                    const price = economic.wheat_price.price || economic.wheat_price;
                    this.animateEconomicValue(wheatElement, price, '$');
                }
            }
            
            // 更新經濟壓力指數
            const pressureElement = document.getElementById('economic-pressure');
            if (pressureElement) {
                // 基於經濟數據計算壓力指數
                let pressureScore = 75; // 基礎分數
                
                if (economic.gold_price && economic.gold_price.price) {
                    // 黃金價格越高，經濟壓力越大
                    if (economic.gold_price.price > 2000) pressureScore += 10;
                    if (economic.gold_price.price > 2100) pressureScore += 5;
                }
                
                if (economic.wheat_price && economic.wheat_price.price) {
                    // 小麥價格越高，經濟壓力越大
                    if (economic.wheat_price.price > 600) pressureScore += 8;
                    if (economic.wheat_price.price > 700) pressureScore += 7;
                }
                
                // 限制在合理範圍內
                pressureScore = Math.min(100, Math.max(50, pressureScore));
                
                this.animateEconomicValue(pressureElement, pressureScore, '', '/100');
            }
        }
    }

    animateEconomicValue(element, targetValue, prefix = '', suffix = '') {
        // 添加更新動畫效果
        const card = element.closest('.economic-card');
        if (card) {
            card.classList.add('updating');
            setTimeout(() => {
                card.classList.remove('updating');
            }, 2000);
        }
        
        let currentValue = 0;
        const increment = targetValue / 50;
        
        const animation = setInterval(() => {
            currentValue += increment;
            if (currentValue >= targetValue) {
                currentValue = targetValue;
                clearInterval(animation);
            }
            
            const displayValue = typeof currentValue === 'number' ? 
                currentValue.toFixed(currentValue < 10 ? 1 : 0) : currentValue;
            element.textContent = `${prefix}${displayValue}${suffix}`;
        }, 40);
    }

    animateNumber(element, targetValue) {
        let currentValue = 0;
        const increment = targetValue / 30;
        
        const animation = setInterval(() => {
            currentValue += increment;
            if (currentValue >= targetValue) {
                currentValue = targetValue;
                clearInterval(animation);
            }
            element.textContent = `${Math.round(currentValue)}%`;
        }, 50);
    }

    showReport(report) {
        const reportSection = document.getElementById('report-section');
        const reportContent = document.getElementById('report-content');
        
        if (reportSection && reportContent) {
            reportSection.style.display = 'block';
            
            // 將Markdown轉換為HTML（簡化版）
            const htmlContent = this.markdownToHtml(report.content);
            reportContent.innerHTML = htmlContent;
            
            // 滾動到報告區域
            setTimeout(() => {
                reportSection.scrollIntoView({ behavior: 'smooth' });
            }, 500);
        }
    }

    markdownToHtml(markdown) {
        // 簡化的Markdown轉HTML
        return markdown
            .replace(/^# (.*$)/gim, '<h1>$1</h1>')
            .replace(/^## (.*$)/gim, '<h2>$1</h2>')
            .replace(/^### (.*$)/gim, '<h3>$1</h3>')
            .replace(/^\* (.*$)/gim, '<li>$1</li>')
            .replace(/^- (.*$)/gim, '<li>$1</li>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>');
    }

    showLoading() {
        const loadingOverlay = document.getElementById('loading-overlay');
        if (loadingOverlay) {
            loadingOverlay.style.display = 'flex';
        }
    }

    hideLoading() {
        const loadingOverlay = document.getElementById('loading-overlay');
        if (loadingOverlay) {
            loadingOverlay.style.display = 'none';
        }
    }

    updateProgress(progress) {
        const progressFill = document.getElementById('loading-progress-fill');
        const progressText = document.getElementById('loading-progress-text');
        
        if (progressFill && progressText) {
            progressFill.style.width = `${progress}%`;
            progressText.textContent = `${progress}%`;
        }
    }

    updateCredits(credits) {
        const creditsCount = document.getElementById('credits-count');
        if (creditsCount) {
            creditsCount.textContent = credits;
        }
    }

    showLoginModal() {
        const modal = document.getElementById('login-modal');
        if (modal) {
            modal.style.display = 'flex';
        }
    }

    showError(message) {
        // 簡單的錯誤提示
        alert(`錯誤: ${message}`);
    }

    playCompletionAnimation() {
        // 播放完成動畫效果
        const dashboard = document.getElementById('dashboard');
        if (dashboard) {
            dashboard.style.animation = 'fadeInUp 0.8s ease-out';
        }
    }
}

// 全域函數
function closeModal() {
    const modal = document.getElementById('login-modal');
    if (modal) {
        modal.style.display = 'none';
    }
}

// 初始化系統
document.addEventListener('DOMContentLoaded', () => {
    window.threatSystem = new ThreatAnalysisSystem();
});

// 添加一些CSS動畫
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }
    
    .pulse-animation {
        animation: pulse 2s infinite;
    }
`;
document.head.appendChild(style);
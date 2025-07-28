// 台灣防衛情勢感知系統 - 主要JavaScript文件

class ThreatAnalysisSystem {
    constructor() {
        this.currentTask = null;
        this.pollInterval = null;
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
            
            // 發送分析請求
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
            
            // 檢查是否已經完成（同步執行）
            if (data.status === 'completed' && data.result) {
                // 直接處理完成的結果
                this.handleAnalysisComplete(data.result);
                
                // 更新最終積分
                if (data.remaining_credits !== undefined) {
                    this.updateCredits(data.remaining_credits);
                }
            } else {
                // 如果還需要檢查狀態（備用方案）
                this.currentTask = data.task_id;
                this.checkTaskStatus();
            }
            
        } catch (error) {
            this.hideLoading();
            this.showError(error.message);
        }
    }

    async checkTaskStatus() {
        try {
            const response = await fetch(`/get_report/${this.currentTask}`);
            
            // 檢查響應是否為 JSON
            const contentType = response.headers.get('content-type');
            if (!contentType || !contentType.includes('application/json')) {
                throw new Error('伺服器返回非 JSON 響應，可能需要重新登入');
            }
            
            const data = await response.json();

            if (!response.ok) {
                // 如果是 404 錯誤，說明報告已經在主請求中返回了
                if (response.status === 404) {
                    this.hideLoading();
                    this.showError('分析系統已改為同步執行，報告應該已經顯示。如果沒有看到結果，請重新開始分析。');
                    return;
                }
                throw new Error(data.error || '獲取報告失敗');
            }

            // 更新進度
            this.updateProgress(data.progress);

            if (data.status === 'completed') {
                this.handleAnalysisComplete(data.result);
                // 更新積分顯示
                if (data.final_credits !== undefined) {
                    this.updateCredits(data.final_credits);
                }
            } else if (data.status === 'error') {
                throw new Error(data.error || '分析過程發生錯誤');
            } else {
                // 如果還在進行中，繼續檢查
                setTimeout(() => this.checkTaskStatus(), 1000);
            }

        } catch (error) {
            this.hideLoading();
            this.showError(error.message);
        }
    }


    handleAnalysisComplete(result) {
        this.hideLoading();
        
        // 顯示儀表板
        this.showDashboard();
        
        // 更新威脅指標
        this.updateThreatIndicators(result.indicators);
        
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
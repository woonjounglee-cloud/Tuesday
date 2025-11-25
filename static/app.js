// Tuesday Portfolio Manager - Client Side JavaScript

let data = {
    roi: [],
    balance: [],
    portfolio: []
};

let currentDB = 'Home_IRP';
let uploadedFileData = null;
let selectedDBFile = null;  // 선택된 DB 파일

// 페이지 로드 시 실행
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    loadDBFiles();
    loadData();
    drawBalanceChart();
});

// 탭 초기화
function initTabs() {
    document.querySelectorAll('.tab-button').forEach(button => {
        button.addEventListener('click', () => {
            const tabName = button.dataset.tab;
            const dbName = button.dataset.db;
            switchTab(tabName, dbName);
        });
    });
}

// 탭 전환
function switchTab(tabName, dbName) {
    // 모든 탭 버튼과 컨텐츠 비활성화
    document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));

    // 선택된 탭 활성화
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    document.getElementById(`${tabName}-tab`).classList.add('active');

    // DB 변경
    if (dbName) {
        currentDB = dbName;
        loadData(false); // 조용히 로드
    }
}

// DB 파일 목록 로드
async function loadDBFiles() {
    try {
        const response = await fetch('/api/db-files');
        const result = await response.json();

        const selector = document.getElementById('db-selector');
        if (!selector) return;

        // 기존 옵션 유지하고 새 옵션 추가
        selector.innerHTML = '<option value="">DB 선택</option>';

        if (result.files && result.files.length > 0) {
            result.files.forEach(file => {
                const option = document.createElement('option');
                option.value = file.filename;
                option.textContent = file.date;  // YYYYMMDD만 표시
                selector.appendChild(option);
            });
        }
    } catch (error) {
        console.error('DB 파일 로드 실패:', error);
    }
}

// DB 선택 변경 처리
async function handleDBChange(filename) {
    if (!filename) {
        selectedDBFile = null;
        return;
    }

    selectedDBFile = filename;

    // 종목코드 수집
    const stockCodes = data.roi
        .map(row => row['종목코드'])
        .filter(code => code && code.trim() !== '');

    if (stockCodes.length === 0) {
        showNotification('⚠️ 종목코드가 없습니다.', 'warning');
        return;
    }

    try {
        // VLOOKUP - 종가 조회
        const response = await fetch(`/api/lookup-price?file=${filename}&codes=${stockCodes.join(',')}`);
        const result = await response.json();

        if (result.prices) {
            // ROI 데이터 업데이트
            data.roi.forEach(row => {
                const code = row['종목코드'];
                if (code && result.prices[code]) {
                    row['종가'] = result.prices[code].price;
                    // 종목명도 업데이트 (있는 경우)
                    if (result.prices[code].name) {
                        row['종목명'] = result.prices[code].name;
                    }
                }
            });

            renderROITable();
            updatePortfolioFromROI();  // 포트폴리오도 자동 업데이트
            renderPortfolioTable();

            showNotification('✅ 종가가 업데이트되었습니다!', 'success');
        }
    } catch (error) {
        showNotification('❌ 종가 조회 실패: ' + error.message, 'error');
    }
}

// 파일 업로드 처리
async function handleFileUpload(type, file) {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('type', type);
    formData.append('db', currentDB);

    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            // 파일 데이터 저장
            uploadedFileData = result.fileData;

            // ROI 데이터 자동 채우기
            updateROIFromFile(uploadedFileData);

            // Balance에 새 행 추가
            if (result.date) {
                addBalanceRowFromUpload(result.date);
            }

            renderROITable();
            renderBalanceTable();

            showNotification('✅ 파일이 업로드되었습니다!', 'success');
        } else {
            showNotification('❌ 업로드 실패: ' + result.error, 'error');
        }
    } catch (error) {
        showNotification('❌ 업로드 실패: ' + error.message, 'error');
    }
}

// 파일 데이터로 ROI 업데이트
function updateROIFromFile(fileData) {
    if (!fileData || !fileData.rows) return;

    data.roi.forEach(row => {
        const code = row['종목코드'];
        if (!code) return;

        // 파일에서 종목코드 찾기
        const fileRow = fileData.rows.find(fr => fr[0] === code);
        if (fileRow) {
            row['종목명'] = fileRow[1] || row['종목명'];
            row['종가'] = parseFloat(fileRow[2]) || row['종가'];
        }
    });
}

// Balance에 새 행 추가 (ETF 업로드 시)
function addBalanceRowFromUpload(dateInfo) {
    if (!dateInfo || !dateInfo.year || !dateInfo.month) return;

    // ROI 테이블에서 총합 계산
    let totalEval = 0;
    let totalInitial = 0;

    data.roi.forEach(row => {
        const quantity = parseFloat(row['수량'] || 0);
        const price = parseFloat(row['종가'] || 0);
        const evaluation = quantity * price;
        const initial = parseFloat(row['초기투자금'] || 0);

        totalEval += evaluation;
        totalInitial += initial;
    });

    // 수익률 계산
    const roi = totalInitial > 0 ? ((totalEval - totalInitial) / totalInitial * 100) : 0;

    // 새 행 추가
    const newRow = {
        '연도': dateInfo.year + '년',
        '월': dateInfo.month + '월',
        '투자원금': totalInitial,
        '추가납입': 0,
        '잔고': totalEval,
        '수익률': roi.toFixed(1) + '%',
        '기타': ''
    };

    data.balance.push(newRow);
}

// 포트폴리오 테이블 업데이트 (ROI 기반)
function updatePortfolioFromROI() {
    if (!data.roi || !data.portfolio) return;

    // 총 평가금 계산
    let totalEval = 0;
    data.roi.forEach(row => {
        const quantity = parseFloat(row['수량'] || 0);
        const price = parseFloat(row['종가'] || 0);
        totalEval += quantity * price;
    });

    // 각 포트폴리오 항목의 현재비중과 녹색매수 계산
    data.portfolio.forEach(row => {
        const code = row['종목코드'];
        if (!code) return;

        // ROI에서 해당 종목의 평가금 찾기
        let evalAmt = 0;
        const roiRow = data.roi.find(r => r['종목코드'] === code);
        if (roiRow) {
            const quantity = parseFloat(roiRow['수량'] || 0);
            const price = parseFloat(roiRow['종가'] || 0);
            evalAmt = quantity * price;
        }

        // 현재비중 계산
        const currentRatio = totalEval > 0 ? (evalAmt / totalEval * 100) : 0;
        row['현재비중'] = currentRatio;

        // 녹색매수 계산
        const settingRatio = parseFloat(row['세팅비중'] || 0);
        const rebalancing = (settingRatio - currentRatio) / 100 * totalEval;
        row['녹색매수'] = rebalancing;
    });
}

// 데이터 로드
async function loadData(showMessage = false) {
    try {
        const response = await fetch(`/api/data?db=${currentDB}`);
        const result = await response.json();

        data = {
            roi: result.roi || [],
            balance: result.balance || [],
            portfolio: result.portfolio || []
        };

        renderROITable();
        renderBalanceTable();
        renderPortfolioTable();
        drawBalanceChart();

        if (showMessage) {
            showNotification('✅ 데이터를 불러왔습니다.', 'success');
        }
    } catch (error) {
        console.error('데이터 로드 실패:', error);
        showNotification('❌ 데이터 로드 실패: ' + error.message, 'error');
    }
}

// ROI 테이블 렌더링
function renderROITable() {
    const tbody = document.querySelector('#roi-table tbody');
    if (!tbody) return;

    tbody.innerHTML = '';

    if (!data.roi || data.roi.length === 0) {
        data.roi = [createEmptyROIRow()];
    }

    // 총합 계산
    let totalInitial = 0;
    let totalEval = 0;

    data.roi.forEach((row, index) => {
        // 평가금 계산
        const quantity = parseFloat(row['수량'] || 0);
        const price = parseFloat(row['종가'] || 0);
        const evaluation = quantity * price;
        row['평가금'] = evaluation;

        // 수익률 계산
        const initial = parseFloat(row['초기투자금'] || 0);
        const roi = initial > 0 ? ((evaluation - initial) / initial * 100) : 0;
        row['수익률'] = roi;

        totalInitial += initial;
        totalEval += evaluation;

        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><input type="text" value="${row['종목코드'] || ''}" onchange="updateROI(${index}, '종목코드', this.value)"></td>
            <td><input type="text" value="${row['종목명'] || ''}" onchange="updateROI(${index}, '종목명', this.value)"></td>
            <td><input type="text" value="${formatNumber(row['초기투자금'] || 0)}" onchange="updateROI(${index}, '초기투자금', this.value.replace(/,/g, ''))"></td>
            <td><input type="number" value="${row['수량'] || 0}" onchange="updateROI(${index}, '수량', this.value)"></td>
            <td><input type="text" value="${formatNumber(row['종가'] || 0)}" onchange="updateROI(${index}, '종가', this.value.replace(/,/g, ''))"></td>
            <td>${formatCurrency(evaluation)}</td>
            <td class="${roi < 0 ? 'negative' : 'positive'}">${roi.toFixed(1)}%</td>
            <td><button class="delete-btn" onclick="deleteRow('roi', ${index})">❌</button></td>
        `;
        tbody.appendChild(tr);
    });

    // 총합 업데이트
    const totalROI = totalInitial > 0 ? ((totalEval - totalInitial) / totalInitial * 100) : 0;

    const totalInitialEl = document.getElementById('total-initial');
    const totalEvalEl = document.getElementById('total-eval');
    const totalRoiEl = document.getElementById('total-roi');

    if (totalInitialEl) totalInitialEl.textContent = formatCurrency(totalInitial);
    if (totalEvalEl) totalEvalEl.textContent = formatCurrency(totalEval);
    if (totalRoiEl) {
        totalRoiEl.textContent = totalROI.toFixed(1) + '%';
        totalRoiEl.className = totalROI < 0 ? 'negative' : 'positive';
    }

    // Balance 자동 업데이트
    updateBalanceFromROI(totalInitial, totalEval);
}

// ROI 데이터로 Balance 업데이트
function updateBalanceFromROI(totalInitial, totalEval) {
    if (data.balance.length > 0) {
        const lastRow = data.balance[data.balance.length - 1];
        lastRow['투자원금'] = totalInitial;
        lastRow['잔고'] = totalEval;

        // 수익률 계산
        const roi = totalInitial > 0 ? ((totalEval - totalInitial) / totalInitial * 100) : 0;
        lastRow['수익률'] = roi.toFixed(1) + '%';
    }
}

// Balance 테이블 렌더링
function renderBalanceTable() {
    const tbody = document.querySelector('#balance-table tbody');
    if (!tbody) return;

    tbody.innerHTML = '';

    if (!data.balance || data.balance.length === 0) {
        data.balance = [createEmptyBalanceRow()];
    }

    data.balance.forEach((row, index) => {
        // 수익률 계산
        const principal = parseFloat(row['투자원금'] || 0);
        const balance = parseFloat(row['잔고'] || 0);
        const returnRate = principal > 0 ? ((balance - principal) / principal * 100) : 0;
        const returnRateClass = returnRate < 0 ? 'negative' : 'positive';

        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><input type="text" value="${row['연도'] || ''}" onchange="updateBalance(${index}, '연도', this.value)"></td>
            <td><input type="text" value="${row['월'] || ''}" onchange="updateBalance(${index}, '월', this.value)"></td>
            <td>${principal.toLocaleString()}</td>
            <td><input type="number" value="${row['추가납입'] || 0}" onchange="updateBalance(${index}, '추가납입', this.value)"></td>
            <td>${balance.toLocaleString()}</td>
            <td class="${returnRateClass}">${returnRate.toFixed(1)}%</td>
            <td><input type="text" class="note-input" value="${row['기타'] || ''}" onchange="updateBalance(${index}, '기타', this.value)"></td>
            <td><button class="delete-btn" onclick="deleteRow('balance', ${index})">❌</button></td>
        `;
        tbody.appendChild(tr);
    });

    drawBalanceChart();
}

// Portfolio 테이블 렌더링
function renderPortfolioTable() {
    const tbody = document.querySelector('#portfolio-table tbody');
    if (!tbody) return;

    tbody.innerHTML = '';

    if (!data.portfolio || data.portfolio.length === 0) {
        data.portfolio = [createEmptyPortfolioRow()];
    }

    let totalSetting = 0;
    let totalCurrent = 0;

    data.portfolio.forEach((row, index) => {
        const settingRatio = parseFloat(row['세팅비중'] || 0);
        const currentRatio = parseFloat(row['현재비중'] || 0);
        const rebalancing = parseFloat(row['녹색매수'] || 0);

        totalSetting += settingRatio;
        totalCurrent += currentRatio;

        const rebalancingClass = rebalancing > 0 ? 'positive' : '';
        const rebalancingText = rebalancing >= 0
            ? formatCurrency(rebalancing)
            : `(${formatCurrency(Math.abs(rebalancing))})`;

        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><input type="text" value="${row['종목코드'] || ''}" onchange="updatePortfolio(${index}, '종목코드', this.value)"></td>
            <td><input type="text" value="${row['종목명'] || ''}" onchange="updatePortfolio(${index}, '종목명', this.value)"></td>
            <td><input type="text" value="${row['자산군'] || ''}" onchange="updatePortfolio(${index}, '자산군', this.value)"></td>
            <td><input type="text" value="${row['구분'] || ''}" onchange="updatePortfolio(${index}, '구분', this.value)"></td>
            <td><input type="number" step="0.1" value="${settingRatio.toFixed(1)}" onchange="updatePortfolio(${index}, '세팅비중', this.value)"></td>
            <td>${currentRatio.toFixed(1)}%</td>
            <td class="${rebalancingClass}">${rebalancingText}</td>
            <td><button class="delete-btn" onclick="deleteRow('portfolio', ${index})">❌</button></td>
        `;
        tbody.appendChild(tr);
    });

    // 총합 업데이트
    const totalSettingEl = document.getElementById('total-setting');
    const totalCurrentEl = document.getElementById('total-current');

    if (totalSettingEl) {
        totalSettingEl.textContent = totalSetting.toFixed(1) + '%';
        totalSettingEl.className = Math.abs(totalSetting - 100) > 0.1 ? 'negative' : '';
    }
    if (totalCurrentEl) {
        totalCurrentEl.textContent = totalCurrent.toFixed(1) + '%';
    }
}

// ROI 데이터 업데이트
function updateROI(index, field, value) {
    data.roi[index][field] = field === '종목코드' || field === '종목명' ? value : parseFloat(value) || 0;
    renderROITable();
}

// Balance 데이터 업데이트
function updateBalance(index, field, value) {
    data.balance[index][field] = value;
    renderBalanceTable();
}

// Portfolio 데이터 업데이트
function updatePortfolio(index, field, value) {
    data.portfolio[index][field] = field === '종목코드' || field === '종목명' || field === '자산군' || field === '구분'
        ? value
        : parseFloat(value) || 0;
    renderPortfolioTable();
}

// 행 추가
function addRow(table) {
    let newRow;
    if (table === 'roi') {
        newRow = createEmptyROIRow();
        data.roi.push(newRow);
        renderROITable();
    } else if (table === 'balance') {
        newRow = createEmptyBalanceRow();
        data.balance.push(newRow);
        renderBalanceTable();
    } else if (table === 'portfolio') {
        newRow = createEmptyPortfolioRow();
        data.portfolio.push(newRow);
        renderPortfolioTable();
    }
}

// 행 삭제
function deleteRow(table, index) {
    if (confirm('정말 삭제하시겠습니까?')) {
        data[table].splice(index, 1);

        if (table === 'roi') renderROITable();
        else if (table === 'balance') renderBalanceTable();
        else if (table === 'portfolio') renderPortfolioTable();
    }
}

// 데이터 저장
async function saveData() {
    try {
        const response = await fetch('/api/save', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                db: currentDB,
                data: data
            })
        });

        const result = await response.json();

        if (result.success) {
            showNotification('✅ 저장되었습니다!', 'success');
        } else {
            showNotification('❌ 저장 실패: ' + result.error, 'error');
        }
    } catch (error) {
        showNotification('❌ 저장 실패: ' + error.message, 'error');
    }
}

// 리밸런싱 수행
async function performRebalancing() {
    try {
        const response = await fetch('/api/rebalance', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                roi: data.roi,
                portfolio: data.portfolio
            })
        });

        const result = await response.json();

        if (result.portfolio) {
            data.portfolio = result.portfolio;
            renderPortfolioTable();
            showNotification('✅ 리밸런싱 완료!', 'success');
        } else {
            showNotification('❌ 리밸런싱 실패: ' + result.error, 'error');
        }
    } catch (error) {
        showNotification('❌ 리밸런싱 실패: ' + error.message, 'error');
    }
}

// Balance 차트 그리기
function drawBalanceChart() {
    const canvas = document.getElementById('balance-chart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const width = 380;
    const height = 350;
    canvas.width = width;
    canvas.height = height;

    // 캔버스 클리어
    ctx.clearRect(0, 0, width, height);

    if (!data.balance || data.balance.length === 0) {
        ctx.font = '16px Arial';
        ctx.fillStyle = '#999';
        ctx.textAlign = 'center';
        ctx.fillText('데이터가 없습니다', width / 2, height / 2);
        return;
    }

    // 데이터 준비
    const balances = data.balance.map(row => parseFloat(row['잔고'] || 0));
    const labels = data.balance.map(row => `${row['연도'] || ''} ${row['월'] || ''}`);

    // Y축 범위 설정: 16,000,000 ~ 최대값 (500,000 단위)
    const minBalance = 16000000;
    const maxData = Math.max(...balances, minBalance);
    const maxBalance = Math.ceil((maxData - minBalance) / 500000) * 500000 + minBalance;
    const range = maxBalance - minBalance;

    // 차트 영역 (bottom 패딩 증가)
    const paddingTop = 40;
    const paddingRight = 40;
    const paddingBottom = 60;
    const paddingLeft = 40;
    const chartWidth = width - paddingLeft - paddingRight;
    const chartHeight = height - paddingTop - paddingBottom;

    // 배경
    ctx.fillStyle = '#f8f9fa';
    ctx.fillRect(0, 0, width, height);

    // 그리드 라인 (500,000 단위)
    ctx.strokeStyle = '#dee2e6';
    ctx.lineWidth = 1;
    const gridStep = 500000;
    const gridCount = Math.ceil(range / gridStep);
    for (let i = 0; i <= gridCount; i++) {
        const value = minBalance + (gridStep * i);
        const y = paddingTop + chartHeight - ((value - minBalance) / range * chartHeight);
        ctx.beginPath();
        ctx.moveTo(paddingLeft, y);
        ctx.lineTo(width - paddingRight, y);
        ctx.stroke();
    }

    // 라인 그리기
    if (balances.length > 0) {
        ctx.strokeStyle = '#667eea';
        ctx.lineWidth = 3;
        ctx.beginPath();

        balances.forEach((balance, index) => {
            const x = paddingLeft + (chartWidth / Math.max(balances.length - 1, 1)) * index;
            const y = paddingTop + chartHeight - ((balance - minBalance) / range * chartHeight);

            if (index === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        });

        ctx.stroke();

        // 포인트 그리기
        ctx.fillStyle = '#667eea';
        balances.forEach((balance, index) => {
            const x = paddingLeft + (chartWidth / Math.max(balances.length - 1, 1)) * index;
            const y = paddingTop + chartHeight - ((balance - minBalance) / range * chartHeight);

            ctx.beginPath();
            ctx.arc(x, y, 5, 0, Math.PI * 2);
            ctx.fill();
        });
    }

    // 축 레이블
    ctx.fillStyle = '#333';
    ctx.textAlign = 'center';

    // X축 레이블 (모든 데이터 표시)
    ctx.font = '11px Arial';
    labels.forEach((label, index) => {
        const x = paddingLeft + (chartWidth / Math.max(labels.length - 1, 1)) * index;
        const y = height - paddingBottom + 25;
        ctx.fillText(label, x, y);
    });

    // Y축 레이블 (500,000 단위)
    ctx.textAlign = 'right';
    ctx.font = '11px Arial';
    for (let i = 0; i <= gridCount; i++) {
        const value = minBalance + (gridStep * i);
        const y = paddingTop + chartHeight - ((value - minBalance) / range * chartHeight) + 4;
        ctx.fillText(formatCurrency(value), paddingLeft - 10, y);
    }
}

// 빈 행 생성
function createEmptyROIRow() {
    return {
        '종목코드': '',
        '종목명': '',
        '초기투자금': 0,
        '수량': 0,
        '종가': 0,
        '평가금': 0,
        '수익률': 0
    };
}

function createEmptyBalanceRow() {
    return {
        '연도': '',
        '월': '',
        '투자원금': 0,
        '추가납입': 0,
        '잔고': 0,
        '수익률': '0%',
        '기타': ''
    };
}

function createEmptyPortfolioRow() {
    return {
        '종목코드': '',
        '종목명': '',
        '자산군': '',
        '구분': '',
        '세팅비중': 0,
        '현재비중': 0,
        '녹색매수': 0
    };
}

// 숫자 포맷팅 (천 단위 구분)
function formatCurrency(num) {
    return new Intl.NumberFormat('ko-KR', {
        style: 'currency',
        currency: 'KRW',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(num).replace('₩', '₩');
}

// 숫자 포맷팅 (천 단위 콤마만)
function formatNumber(num) {
    return new Intl.NumberFormat('ko-KR', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 2
    }).format(num);
}

// 알림 표시
function showNotification(message, type) {
    alert(message);
}

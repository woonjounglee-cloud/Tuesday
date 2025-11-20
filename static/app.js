// Tuesday Portfolio Manager - Client Side JavaScript

let data = {
    roi: [],
    balance: [],
    portfolio: []
};

let currentDB = 'Home_IRP';
let uploadedFileData = null;

// 페이지 로드 시 실행
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
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
        loadData();
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

            // Balance 날짜 자동 채우기
            if (result.date) {
                updateBalanceFromDate(result.date);
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

// 날짜로 Balance 업데이트
function updateBalanceFromDate(dateInfo) {
    // 새로운 행 추가 또는 마지막 행 업데이트
    if (data.balance.length === 0) {
        data.balance.push(createEmptyBalanceRow());
    }

    const lastRow = data.balance[data.balance.length - 1];
    lastRow['연도'] = dateInfo.year + '년';
    lastRow['월'] = dateInfo.month + '월';
}

// 데이터 로드
async function loadData() {
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

        showNotification('✅ 데이터를 불러왔습니다.', 'success');
    } catch (error) {
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
            <td><input type="number" value="${row['초기투자금'] || 0}" onchange="updateROI(${index}, '초기투자금', this.value)"></td>
            <td><input type="number" value="${row['수량'] || 0}" onchange="updateROI(${index}, '수량', this.value)"></td>
            <td><input type="number" value="${row['종가'] || 0}" onchange="updateROI(${index}, '종가', this.value)"></td>
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
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><input type="text" value="${row['연도'] || ''}" onchange="updateBalance(${index}, '연도', this.value)"></td>
            <td><input type="text" value="${row['월'] || ''}" onchange="updateBalance(${index}, '월', this.value)"></td>
            <td><input type="number" value="${row['투자원금'] || 0}" onchange="updateBalance(${index}, '투자원금', this.value)" readonly></td>
            <td><input type="number" value="${row['추가납입'] || 0}" onchange="updateBalance(${index}, '추가납입', this.value)"></td>
            <td><input type="number" value="${row['잔고'] || 0}" onchange="updateBalance(${index}, '잔고', this.value)" readonly></td>
            <td><input type="text" value="${row['수익률'] || '0%'}" readonly></td>
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
        const rebalancing = parseFloat(row['빨강매수'] || 0);

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
    const height = 300;
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

    const maxBalance = Math.max(...balances, 0);
    const minBalance = 0;
    const range = maxBalance - minBalance;

    // 차트 영역
    const padding = 40;
    const chartWidth = width - padding * 2;
    const chartHeight = height - padding * 2;

    // 배경
    ctx.fillStyle = '#f8f9fa';
    ctx.fillRect(0, 0, width, height);

    // 그리드 라인
    ctx.strokeStyle = '#dee2e6';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 5; i++) {
        const y = padding + (chartHeight / 5) * i;
        ctx.beginPath();
        ctx.moveTo(padding, y);
        ctx.lineTo(width - padding, y);
        ctx.stroke();
    }

    // 라인 그리기
    if (balances.length > 0) {
        ctx.strokeStyle = '#667eea';
        ctx.lineWidth = 3;
        ctx.beginPath();

        balances.forEach((balance, index) => {
            const x = padding + (chartWidth / Math.max(balances.length - 1, 1)) * index;
            const y = padding + chartHeight - ((balance - minBalance) / range * chartHeight);

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
            const x = padding + (chartWidth / Math.max(balances.length - 1, 1)) * index;
            const y = padding + chartHeight - ((balance - minBalance) / range * chartHeight);

            ctx.beginPath();
            ctx.arc(x, y, 5, 0, Math.PI * 2);
            ctx.fill();
        });
    }

    // 축 레이블
    ctx.fillStyle = '#333';
    ctx.font = '12px Arial';
    ctx.textAlign = 'center';

    // X축 레이블 (최대 5개만 표시)
    const labelStep = Math.max(1, Math.floor(labels.length / 5));
    labels.forEach((label, index) => {
        if (index % labelStep === 0 || index === labels.length - 1) {
            const x = padding + (chartWidth / Math.max(labels.length - 1, 1)) * index;
            ctx.fillText(label, x, height - 10);
        }
    });

    // Y축 레이블
    ctx.textAlign = 'right';
    for (let i = 0; i <= 5; i++) {
        const value = minBalance + (range / 5) * (5 - i);
        const y = padding + (chartHeight / 5) * i + 5;
        ctx.fillText(formatCurrency(value), padding - 10, y);
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
        '빨강매수': 0
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

// 알림 표시
function showNotification(message, type) {
    alert(message);
}

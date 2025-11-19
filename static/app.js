// Tuesday Portfolio Manager - Client Side JavaScript

let data = {
    roi: [],
    balance: [],
    portfolio: []
};

// 페이지 로드 시 실행
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    loadData();
});

// 탭 초기화
function initTabs() {
    document.querySelectorAll('.tab-button').forEach(button => {
        button.addEventListener('click', () => {
            const tabName = button.dataset.tab;
            switchTab(tabName);
        });
    });
}

// 탭 전환
function switchTab(tabName) {
    // 모든 탭 버튼과 컨텐츠 비활성화
    document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));

    // 선택된 탭 활성화
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    document.getElementById(`${tabName}-tab`).classList.add('active');
}

// 데이터 로드
async function loadData() {
    try {
        const response = await fetch('/api/data');
        data = await response.json();

        renderROITable();
        renderBalanceTable();
        renderPortfolioTable();

        showNotification('✅ 데이터를 불러왔습니다.', 'success');
    } catch (error) {
        showNotification('❌ 데이터 로드 실패: ' + error.message, 'error');
    }
}

// ROI 테이블 렌더링
function renderROITable() {
    const tbody = document.querySelector('#roi-table tbody');
    tbody.innerHTML = '';

    if (!data.roi || data.roi.length === 0) {
        data.roi = [createEmptyROIRow()];
    }

    data.roi.forEach((row, index) => {
        const tr = document.createElement('tr');

        // 평가금 계산
        const quantity = parseFloat(row['수량'] || 0);
        const price = parseFloat(row['종가'] || 0);
        const evaluation = quantity * price;
        row['평가금'] = evaluation;

        // 수익률 계산
        const initial = parseFloat(row['초기투자금'] || 0);
        const roi = initial > 0 ? ((evaluation - initial) / initial * 100) : 0;
        row['수익률'] = roi;

        tr.innerHTML = `
            <td><input type="text" value="${row['종목코드'] || ''}" onchange="updateROI(${index}, '종목코드', this.value)"></td>
            <td><input type="text" value="${row['종목명'] || ''}" onchange="updateROI(${index}, '종목명', this.value)"></td>
            <td><input type="number" value="${row['초기투자금'] || 0}" onchange="updateROI(${index}, '초기투자금', this.value)"></td>
            <td><input type="number" value="${row['수량'] || 0}" onchange="updateROI(${index}, '수량', this.value)"></td>
            <td><input type="number" value="${row['종가'] || 0}" onchange="updateROI(${index}, '종가', this.value)"></td>
            <td>${formatNumber(evaluation)}</td>
            <td class="${roi < 0 ? 'negative' : 'positive'}">${roi.toFixed(2)}%</td>
            <td><button class="delete-btn" onclick="deleteRow('roi', ${index})">❌</button></td>
        `;
        tbody.appendChild(tr);
    });

    updateROISummary();
}

// Balance 테이블 렌더링
function renderBalanceTable() {
    const tbody = document.querySelector('#balance-table tbody');
    tbody.innerHTML = '';

    if (!data.balance || data.balance.length === 0) {
        data.balance = [createEmptyBalanceRow()];
    }

    data.balance.forEach((row, index) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><input type="text" value="${row['연도'] || ''}" onchange="updateBalance(${index}, '연도', this.value)"></td>
            <td><input type="text" value="${row['월'] || ''}" onchange="updateBalance(${index}, '월', this.value)"></td>
            <td><input type="number" value="${row['투자원금'] || 0}" onchange="updateBalance(${index}, '투자원금', this.value)"></td>
            <td><input type="number" value="${row['추가납입'] || 0}" onchange="updateBalance(${index}, '추가납입', this.value)"></td>
            <td><input type="number" value="${row['잔고'] || 0}" onchange="updateBalance(${index}, '잔고', this.value)"></td>
            <td><input type="text" value="${row['수익률'] || '0%'}" onchange="updateBalance(${index}, '수익률', this.value)"></td>
            <td><input type="text" value="${row['기타'] || ''}" onchange="updateBalance(${index}, '기타', this.value)"></td>
            <td><button class="delete-btn" onclick="deleteRow('balance', ${index})">❌</button></td>
        `;
        tbody.appendChild(tr);
    });
}

// Portfolio 테이블 렌더링
function renderPortfolioTable() {
    const tbody = document.querySelector('#portfolio-table tbody');
    tbody.innerHTML = '';

    if (!data.portfolio || data.portfolio.length === 0) {
        data.portfolio = [createEmptyPortfolioRow()];
    }

    data.portfolio.forEach((row, index) => {
        const rebalancing = parseFloat(row['빨강매수'] || 0);
        const rebalancingClass = rebalancing > 0 ? 'positive' : 'negative';
        const rebalancingText = rebalancing > 0 ? formatNumber(rebalancing) : `(${formatNumber(Math.abs(rebalancing))})`;

        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><input type="text" value="${row['종목코드'] || ''}" onchange="updatePortfolio(${index}, '종목코드', this.value)"></td>
            <td><input type="text" value="${row['종목명'] || ''}" onchange="updatePortfolio(${index}, '종목명', this.value)"></td>
            <td><input type="text" value="${row['자산군'] || ''}" onchange="updatePortfolio(${index}, '자산군', this.value)"></td>
            <td><input type="text" value="${row['구분'] || ''}" onchange="updatePortfolio(${index}, '구분', this.value)"></td>
            <td><input type="number" step="0.1" value="${row['세팅비중'] || 0}" onchange="updatePortfolio(${index}, '세팅비중', this.value)"></td>
            <td>${(row['현재비중'] || 0).toFixed(1)}%</td>
            <td class="${rebalancingClass}">${rebalancingText}</td>
            <td><button class="delete-btn" onclick="deleteRow('portfolio', ${index})">❌</button></td>
        `;
        tbody.appendChild(tr);
    });

    updatePortfolioSummary();
}

// ROI 데이터 업데이트
function updateROI(index, field, value) {
    data.roi[index][field] = value;
    renderROITable();
}

// Balance 데이터 업데이트
function updateBalance(index, field, value) {
    data.balance[index][field] = value;
    renderBalanceTable();
}

// Portfolio 데이터 업데이트
function updatePortfolio(index, field, value) {
    data.portfolio[index][field] = value;
    renderPortfolioTable();
}

// ROI 요약 업데이트
function updateROISummary() {
    let totalInitial = 0;
    let totalEval = 0;

    data.roi.forEach(row => {
        totalInitial += parseFloat(row['초기투자금'] || 0);
        totalEval += parseFloat(row['평가금'] || 0);
    });

    const totalROI = totalInitial > 0 ? ((totalEval - totalInitial) / totalInitial * 100) : 0;

    document.getElementById('total-initial').textContent = formatNumber(totalInitial);
    document.getElementById('total-eval').textContent = formatNumber(totalEval);
    document.getElementById('total-roi').textContent = totalROI.toFixed(2) + '%';
    document.getElementById('total-roi').className = totalROI < 0 ? 'negative' : 'positive';
}

// Portfolio 요약 업데이트
function updatePortfolioSummary() {
    let totalSetting = 0;
    let totalCurrent = 0;

    data.portfolio.forEach(row => {
        totalSetting += parseFloat(row['세팅비중'] || 0);
        totalCurrent += parseFloat(row['현재비중'] || 0);
    });

    document.getElementById('total-setting').textContent = totalSetting.toFixed(1) + '%';
    document.getElementById('total-current').textContent = totalCurrent.toFixed(1) + '%';

    if (Math.abs(totalSetting - 100) > 0.1) {
        document.getElementById('total-setting').classList.add('negative');
    } else {
        document.getElementById('total-setting').classList.remove('negative');
    }
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
            body: JSON.stringify(data)
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
            body: JSON.stringify({roi: data.roi, portfolio: data.portfolio})
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

// 숫자 포맷팅
function formatNumber(num) {
    return new Intl.NumberFormat('ko-KR').format(Math.round(num));
}

// 알림 표시
function showNotification(message, type) {
    alert(message);
}

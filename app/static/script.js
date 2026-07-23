let token = "";
let messages = [];

// =======================
// D-Day 계산 유틸리티
// =======================
function calculateDDay(examDate) {
    if (!examDate) return "";
    const today = new Date();
    const target = new Date(examDate);

    today.setHours(0, 0, 0, 0);
    target.setHours(0, 0, 0, 0);

    const diffTime = target - today;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return "D-Day";
    if (diffDays > 0) return `D-${diffDays}`;
    return `D+${Math.abs(diffDays)}`;
}

// =======================
// 로그인
// =======================
async function login() {
    const form = new FormData();
    form.append("username", document.getElementById("username").value);
    form.append("password", document.getElementById("password").value);

    const response = await fetch("/login", {
        method: "POST",
        body: form
    });

    const data = await response.json();

    if (data.access_token) {
        token = data.access_token;
        localStorage.setItem("token", token);
        location.href = "/planner";
    } else {
        document.getElementById("login-result").innerText = data.detail;
    }
}

// =======================
// 회원가입
// =======================
async function signup() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const password2 = document.getElementById("password2").value;

    if (password !== password2) {
        document.getElementById("login-result").innerText = "비밀번호가 일치하지 않습니다.";
        return;
    }

    const response = await fetch("/signup", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    });

    const data = await response.json();

    document.getElementById("login-result").innerText = data.message || data.detail;

    if (response.ok) {
        setTimeout(function () {
            location.href = "/login-page";
        }, 1000);
    }
}

// =======================
// AI 공부 계획 생성
// =======================
async function createPlan() {
    token = localStorage.getItem("token");

    if (!token) {
        document.getElementById("result").innerText = "먼저 로그인해주세요.";
        return;
    }

    const subject = document.getElementById("subject").value;
    const exam_date = document.getElementById("exam_date").value;
    const study_time = document.getElementById("study_time").value;
    const goal = document.getElementById("goal").value;

    if (!subject || !exam_date || !study_time || !goal) {
        alert("모든 항목을 입력해주세요.");
        return;
    }

    const response = await fetch("/generate-plan", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({
            subject: subject,
            exam_date: exam_date,
            study_time: study_time,
            goal: goal
        })
    });

    const data = await response.json();

    if (data.plan) {
        document.getElementById("user-info").innerText = "👤 " + data.username + "님";

        // D-Day 및 요약 박스 바인딩 (새 UI 호환)
        const summaryDiv = document.getElementById("plan-summary");
        if (summaryDiv) {
            const dDay = calculateDDay(exam_date);
            summaryDiv.innerHTML = `
                <span class="d-day-badge">${dDay}</span>
                <span class="summary-info"><strong>과목:</strong> ${subject} | <strong>하루:</strong> ${study_time} | <strong>목표:</strong> ${goal}</span>
            `;
            summaryDiv.style.display = "flex";
        }

        document.getElementById("result").innerHTML = data.plan.replace(/\n/g, "<br>");
    } else {
        document.getElementById("result").innerText = data.detail || "계획 생성에 실패했습니다.";
    }
}

// =======================
// AI 대화 메시지 전송
// =======================
async function sendMessage() {
    const input = document.getElementById("chat-input");
    const text = input.value.trim();

    console.log("보내는 메시지:", text);

    if (text === "") return;

    const chatBox = document.getElementById("chat-box");

    // 사용자 메시지 말풍선 UI 추가
    chatBox.innerHTML += `
        <div class="chat-item user">
            <div class="chat-bubble">${text}</div>
        </div>
    `;
    input.value = "";

    // 사용자 메시지 저장
    messages.push({
        role: "user",
        content: text
    });

    // 로딩 표시 UI (새 아바타 말풍선 호환)
    chatBox.innerHTML += `
        <div id="loading" class="chat-item assistant">
            <div class="chat-avatar">🤖</div>
            <div class="chat-bubble loading-bubble">AI가 생각 중입니다...</div>
        </div>
    `;

    // 자동 스크롤
    chatBox.scrollTop = chatBox.scrollHeight;

    const response = await fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + localStorage.getItem("token")
        },
        body: JSON.stringify({
            messages: messages
        })
    });

    const data = await response.json();

    console.log("AI 응답:", data);

    // 로딩 제거
    const loading = document.getElementById("loading");
    if (loading) {
        loading.remove();
    }

    if (data.answer) {
        messages.push({
            role: "assistant",
            content: data.answer
        });

        // AI 메시지 말풍선 UI 추가
        chatBox.innerHTML += `
            <div class="chat-item assistant">
                <div class="chat-avatar">🤖</div>
                <div class="chat-bubble">${data.answer.replace(/\n/g, "<br>")}</div>
            </div>
        `;
    } else {
        chatBox.innerHTML += `
            <div class="chat-item assistant">
                <div class="chat-avatar">🤖</div>
                <div class="chat-bubble">오류 발생: ${JSON.stringify(data)}</div>
            </div>
        `;
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}

// =======================
// 유틸리티
// =======================

function logout() {
    localStorage.removeItem("token");
    location.href = "/login-page";
}

function copyPlan() {
    navigator.clipboard.writeText(
        document.getElementById("result").innerText
    );
    alert("복사되었습니다.");
}

// =======================
// 페이지 로드 및 이벤트 바인딩
// =======================

window.onload = function () {
    token = localStorage.getItem("token") || "";

    const userInfo = document.getElementById("user-info");

    if (userInfo) {
        if (token) {
            userInfo.innerText = "로그인됨";
        } else {
            userInfo.innerText = "로그아웃 상태";
        }
    }
};

document.addEventListener("DOMContentLoaded", function () {
    // 1. AI 채팅창 엔터키 감지
    const chatInput = document.getElementById("chat-input");
    if (chatInput) {
        chatInput.addEventListener("keydown", function (e) {
            if (e.key === "Enter") {
                sendMessage();
            }
        });
    }

    // 2. 로그인 / 회원가입 Input 엔터키 감지 추가
    const usernameInput = document.getElementById("username");
    const passwordInput = document.getElementById("password");
    const password2Input = document.getElementById("password2");

    function handleAuthEnter(e) {
        if (e.key === "Enter") {
            e.preventDefault();
            // password2 필드가 존재하는 페이지면 회원가입, 없으면 로그인 실행
            if (password2Input) {
                signup();
            } else {
                login();
            }
        }
    }

    if (usernameInput) usernameInput.addEventListener("keydown", handleAuthEnter);
    if (passwordInput) passwordInput.addEventListener("keydown", handleAuthEnter);
    if (password2Input) password2Input.addEventListener("keydown", handleAuthEnter);
});

// =======================
// 마이페이지 데이터 로드
// =======================

async function loadMyPage() {
    const token = localStorage.getItem("token");

    const planResponse = await fetch("/my-plans", {
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    const plans = await planResponse.json();

    let planHTML = "";

    plans.forEach(p => {
        planHTML += `
            <div class="card">
                <h3>${p.subject}</h3>
                <p>시험일 : ${p.exam_date}</p>
                <p>목표 : ${p.goal}</p>
                <p>${p.plan.replace(/\n/g, "<br>")}</p>
            </div>
        `;
    });

    const plansElement = document.getElementById("plans");
    if (plansElement) plansElement.innerHTML = planHTML;

    const chatResponse = await fetch("/my-chats", {
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    const chats = await chatResponse.json();

    let chatHTML = "";

    chats.forEach(c => {
        chatHTML += `
            <p>
                <b>${c.role}</b> : ${c.content}
            </p>
        `;
    });

    const chatsElement = document.getElementById("chats");
    if (chatsElement) chatsElement.innerHTML = chatHTML;
}

if (location.pathname == "/mypage") {
    loadMyPage();
}
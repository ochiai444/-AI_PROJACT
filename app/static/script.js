let token = "";

let messages = [];


// =======================
// 로그인
// =======================
async function login() {

    const form = new FormData();

    form.append(
        "username",
        document.getElementById("username").value
    );

    form.append(
        "password",
        document.getElementById("password").value
    );


    const response = await fetch(
        "/login",
        {
            method: "POST",
            body: form
        }
    );


    const data = await response.json();


    if (data.access_token) {

        token = data.access_token;

        localStorage.setItem(
            "token",
            token
        );

        location.href = "/planner";


    } else {

        document.getElementById(
            "login-result"
        ).innerText = data.detail;

    }

}



// =======================
// 회원가입
// =======================
async function signup() {

    const username =
        document.getElementById("username").value;


    const password =
        document.getElementById("password").value;


    const password2 =
        document.getElementById("password2").value;



    if (password !== password2) {

        document.getElementById(
            "login-result"
        ).innerText =
        "비밀번호가 일치하지 않습니다.";

        return;

    }



    const response = await fetch(
        "/signup",
        {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },


            body: JSON.stringify({

                username: username,

                password: password

            })

        }
    );



    const data =
        await response.json();



    document.getElementById(
        "login-result"
    ).innerText =
    data.message || data.detail;



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


    token =
    localStorage.getItem("token");


    if (!token) {

        document.getElementById(
            "result"
        ).innerText =
        "먼저 로그인해주세요.";

        return;

    }



    const subject =
    document.getElementById("subject").value;


    const exam_date =
    document.getElementById("exam_date").value;


    const study_time =
    document.getElementById("study_time").value;


    const goal =
    document.getElementById("goal").value;



    if (!subject || !exam_date || !study_time || !goal) {

        alert("모든 항목을 입력해주세요.");

        return;

    }



    const response = await fetch(
        "/generate-plan",
        {

            method: "POST",

            headers: {

                "Content-Type":
                "application/json",

                "Authorization":
                "Bearer " + token

            },


            body: JSON.stringify({

                subject: subject,

                exam_date: exam_date,

                study_time: study_time,

                goal: goal

            })

        }
    );



    const data =
    await response.json();



    if (data.plan) {


        document.getElementById(
            "user-info"
        ).innerHTML =
        "👤 " + data.username + "님";


        document.getElementById(
            "result"
        ).innerHTML =
        data.plan.replace(/\n/g,"<br>");


    } else {


        document.getElementById(
            "result"
        ).innerText =
        data.detail ||
        "계획 생성에 실패했습니다.";

    }

}



// =======================
// AI 대화 메시지 전송
// =======================
async function sendMessage() {


    const input =
    document.getElementById("chat-input");


    const text =
    input.value.trim();



    console.log(
        "보내는 메시지:",
        text
    );



    if (text === "") return;



    const chatBox =
    document.getElementById("chat-box");



    chatBox.innerHTML +=
    `<div class="user">${text}</div>`;


    input.value = "";



    // 사용자 메시지 저장
messages.push({

    role: "user",

    content: text

});



const response =
await fetch(
    "/chat",
    {

        method: "POST",

        headers: {

            "Content-Type":
            "application/json"

        },


        body: JSON.stringify({

            messages: messages

        })

    }
);


    const data =
    await response.json();



    console.log(
        "AI 응답:",
        data
    );



    if(data.answer){


        messages.push({

            role:"assistant",

            content:data.answer

        });



        chatBox.innerHTML +=
        `
        <div class="assistant">
        ${data.answer.replace(/\n/g,"<br>")}
        </div>
        `;



    } else {


        chatBox.innerHTML +=
        `
        <div class="assistant">
        오류 발생:
        ${JSON.stringify(data)}
        </div>
        `;


    }



    chatBox.scrollTop =
    chatBox.scrollHeight;

}




// =======================
// 유틸리티
// =======================

function logout() {

    localStorage.removeItem(
        "token"
    );

    location.href =
    "/login-page";

}



function copyPlan() {

    navigator.clipboard.writeText(
        document.getElementById("result").innerText
    );


    alert(
        "복사되었습니다."
    );

}




// =======================
// 페이지 로드
// =======================

window.onload = function () {


    token =
    localStorage.getItem("token") || "";



    const userInfo =
    document.getElementById("user-info");



    if(userInfo){


        if(token){

            userInfo.innerText =
            "✅ 로그인 상태";


        } else {


            userInfo.innerText =
            "로그아웃 상태";

        }

    }

};





document.addEventListener(
"DOMContentLoaded",
function(){


    const input =
    document.getElementById("chat-input");



    if(input){


        input.addEventListener(
        "keydown",
        function(e){


            if(e.key==="Enter"){

                sendMessage();

            }


        });


    }


});
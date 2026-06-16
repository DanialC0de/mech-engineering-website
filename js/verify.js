
// دیتابیس کاربران آزمایشی
const USERS_DB = [
    { phone: "09139971950", email: "danial_sh@eng.uk.ac.ir", name: "دانیال شیخ شعاعی", role: "student", studentId: "403405045" },
    { phone: "09198765432", email: "karimi@eng.uk.ac.ir", name: "دکتر کریمی", role: "professor", studentId: "40198765" },
    { phone: "09111111111", email: "admin@eng.uk.ac.ir", name: "ادمین سیستم", role: "admin", studentId: "admin001" }
];

if (!localStorage.getItem("registeredUsers")) {
    localStorage.setItem("registeredUsers", JSON.stringify(USERS_DB));
}

// دریافت اطلاعات از صفحه قبل
const tempIdentifier = localStorage.getItem("tempIdentifier");
const tempIdentifierType = localStorage.getItem("tempIdentifierType");

console.log("tempIdentifier:", tempIdentifier);
console.log("tempIdentifierType:", tempIdentifierType);

if (!tempIdentifier) {
    alert("خطا: اطلاعات ورودی یافت نشد. به صفحه ورود برمی‌گردید.");
    window.location.href = "login.html";
}

// بررسی وجود کاربر

let foundUser = null;
let isExisting = false;

const dbUsers = JSON.parse(localStorage.getItem("registeredUsers")) || USERS_DB;

if (tempIdentifierType === "phone") {
    foundUser = dbUsers.find(user => user.phone === tempIdentifier);
} else if (tempIdentifierType === "email") {
    foundUser = dbUsers.find(user => user.email === tempIdentifier);
}

isExisting = (foundUser !== null);

console.log("User exists:", isExisting);
if (foundUser) console.log("Found user:", foundUser);


// نمایش اطلاعات در صفحه

function displayUserStatus() {
    const banner = document.getElementById("statusBanner");
    const icon = document.getElementById("statusIcon");
    const title = document.getElementById("statusTitle");
    const message = document.getElementById("statusMessage");
    const identifierDisplay = document.getElementById("identifierDisplay");

    // نمایش شناسه کاربر با فرمت صحیح
    if (tempIdentifierType === "phone" && tempIdentifier) {
        let phone = tempIdentifier;
        if (phone.length === 11) {
            let part1 = phone.slice(0, 4);
            let part2 = phone.slice(7, 11);
            let masked = `${part1}***${part2}`;
            identifierDisplay.innerHTML = `📱 شماره موبایل: <strong dir="ltr">${masked}</strong>`;
        } else {
            identifierDisplay.innerHTML = `📱 شماره موبایل: <strong>${phone}</strong>`;
        }
    } else if (tempIdentifierType === "email" && tempIdentifier) {
        let masked = tempIdentifier;
        if (tempIdentifier.includes("@")) {
            let parts = tempIdentifier.split("@");
            let local = parts[0];
            let domain = parts[1];
            let maskedLocal = local.length > 2 ? local[0] + "***" + local[local.length - 1] : "***";
            masked = maskedLocal + "@" + domain;
        }
        identifierDisplay.innerHTML = `✉️ آدرس ایمیل: <strong>${masked}</strong>`;
    }

    if (isExisting && foundUser) {
        banner.className = "status-banner existing-user";
        icon.innerHTML = "✅";
        title.innerHTML = "خوش آمدید!";
        message.innerHTML = `${foundUser.name} عزیز، برای ورود به حساب کاربری، کد تایید را وارد کنید.`;
    } else {
        banner.className = "status-banner new-user";
        icon.innerHTML = "📝";
        title.innerHTML = "ثبت‌نام جدید";
        message.innerHTML = "به انجمن علمی مکانیک خوش آمدید! برای تکمیل ثبت‌نام، کد تایید را وارد کنید.";
    }
}

displayUserStatus();


// مدیریت فیلدهای کد (از چپ به راست - حالت عادی)

const inputs = document.querySelectorAll('.otp-input');

inputs.forEach((input, index) => {
    input.addEventListener('input', (e) => {
        const value = e.target.value;
        if (value && !/^\d+$/.test(value)) {
            e.target.value = '';
            return;
        }
        if (value && index < 5) {
            inputs[index + 1].focus();
        }
        checkComplete();
    });

    input.addEventListener('keydown', (e) => {
        if (e.key === 'Backspace') {
            if (input.value === '' && index > 0) {
                inputs[index - 1].focus();
                inputs[index - 1].value = '';
            }
            checkComplete();
        }
    });
});

function getCode() {
    let code = '';
    inputs.forEach(input => {
        code += input.value;
    });
    return code;
}

function checkComplete() {
    const btn = document.getElementById("verifyBtn");
    if (getCode().length === 6) {
        btn.disabled = false;
    } else {
        btn.disabled = true;
    }
}


// تایمر

let timerSeconds = 120;
let timerInterval = null;

function startTimer() {
    const timerSpan = document.getElementById("timerSeconds");
    const resendBtn = document.getElementById("resendBtn");

    if (timerInterval) clearInterval(timerInterval);

    timerSeconds = 120;
    resendBtn.disabled = true;
    resendBtn.style.opacity = "0.5";

    timerInterval = setInterval(() => {
        timerSeconds--;
        timerSpan.textContent = timerSeconds;

        if (timerSeconds <= 0) {
            clearInterval(timerInterval);
            resendBtn.disabled = false;
            resendBtn.style.opacity = "1";
            timerSpan.textContent = "۰";
        }
    }, 1000);
}

startTimer();

document.getElementById("resendBtn").addEventListener("click", () => {
    if (timerSeconds > 0) return;
    showError("کد جدید برای شما ارسال شد (کد تست: 123456)");
    startTimer();
    inputs.forEach(i => i.value = '');
    inputs[0].focus();
    document.getElementById("verifyBtn").disabled = true;
});


// تایید کد

const CORRECT_CODE = "123456";

function showError(msg) {
    const errDiv = document.getElementById("errorMsg");
    errDiv.textContent = msg;
    errDiv.style.display = "block";
    setTimeout(() => errDiv.style.display = "none", 3000);
}

function showLoading(show) {
    const loadingDiv = document.getElementById("loading");
    const btn = document.getElementById("verifyBtn");
    if (show) {
        loadingDiv.style.display = "block";
        btn.disabled = true;
    } else {
        loadingDiv.style.display = "none";
        btn.disabled = false;
    }
}

document.getElementById("verifyBtn").addEventListener("click", () => {
    const code = getCode();

    if (code.length !== 6) {
        showError("لطفاً کد ۶ رقمی را کامل وارد کنید");
        return;
    }

    if (code !== CORRECT_CODE) {
        showError("کد وارد شده اشتباه است. کد صحیح: 123456");
        return;
    }

    showLoading(true);

    setTimeout(() => {
        if (isExisting && foundUser) {
            const session = {
                name: foundUser.name,
                phone: foundUser.phone,
                email: foundUser.email,
                role: foundUser.role,
                studentId: foundUser.studentId,
                loginTime: new Date().toISOString()
            };
            localStorage.setItem("currentUser", JSON.stringify(session));

            let redirectUrl = "";
            switch (foundUser.role) {
                case "admin": redirectUrl = "admin.html"; break;
                case "professor": redirectUrl = "professor.html"; break;
                default: redirectUrl = "student.html";
            }

            const btn = document.getElementById("verifyBtn");
            btn.textContent = "✓ تایید شد! در حال انتقال...";

            setTimeout(() => {
                window.location.href = redirectUrl;
            }, 1500);
        } else {
            localStorage.setItem("tempIdentifier", tempIdentifier);
            localStorage.setItem("tempIdentifierType", tempIdentifierType);
            window.location.href = "register.html";
        }
    }, 1000);
});

// فوکوس خودکار روی فیلد اول (سمت چپ)
setTimeout(() => inputs[0].focus(), 200);
// ===============================
// مدیریت فیلدهای OTP
// ===============================
const otpInputs = document.querySelectorAll('.otp-input');
const otpVerifyBtn = document.getElementById("verifyBtn");
const otpErrorDiv = document.getElementById("errorMsg");
const otpLoadingDiv = document.getElementById("loading");

// تابع تبدیل اعداد فارسی به انگلیسی
function toEnglishDigits(str) {
    if (!str) return '';
    return str
        .replace(/[۰-۹]/g, d => '۰۱۲۳۴۵۶۷۸۹'.indexOf(d))
        .replace(/[٠-٩]/g, d => '٠١٢٣٤٥٦٧٨٩'.indexOf(d));
}

// گرفتن کوکی CSRF برای امنیت جنگو
function getOtpCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// بررسی وضعیت دکمه
function checkOtpComplete() {
    const code = getOtpCode();
    otpVerifyBtn.disabled = code.length !== 6;
}

function getOtpCode() {
    let code = '';
    otpInputs.forEach(input => {
        code += toEnglishDigits(input.value);
    });
    return code;
}

function showOtpError(msg) {
    if (otpErrorDiv) {
        otpErrorDiv.textContent = msg;
        otpErrorDiv.style.display = "block";
    }
}

function setLoading(isLoading) {
    otpVerifyBtn.disabled = isLoading;
    if (otpLoadingDiv) otpLoadingDiv.style.display = isLoading ? "block" : "none";
    if (otpErrorDiv && isLoading) otpErrorDiv.style.display = "none";
}

// منطق اصلی ورودی‌ها
otpInputs.forEach((input, index) => {
    input.addEventListener('input', (e) => {
        let value = toEnglishDigits(e.target.value);
        e.target.value = value;
        if (value && !/^\d$/.test(value)) { e.target.value = ''; return; }
        if (value && index < otpInputs.length - 1) otpInputs[index + 1].focus();
        checkOtpComplete();
    });

    input.addEventListener('keydown', (e) => {
        if (e.key === 'Backspace' && input.value === '' && index > 0) otpInputs[index - 1].focus();
    });
});

// ===============================
// ارسال به جنگو (بخش اصلی)
// ===============================
otpVerifyBtn.addEventListener("click", async () => {
    const code = getOtpCode();
    
    setLoading(true);

    try {
        const response = await fetch("/accounts/verify-otp/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getOtpCookie("csrftoken")
            },
            body: JSON.stringify({ code: code })
        });

        const data = await response.json();

        if (response.ok) {
            // ریدایرکت موفق به پنل کاربری
            window.location.href = data.redirect;
        } else {
            // نمایش خطای سرور (مثلاً کد اشتباه است)
            showOtpError(data.message || "خطا در تایید کد");
            setLoading(false);
        }
    } catch (error) {
        showOtpError("خطا در ارتباط با سرور");
        setLoading(false);
    }
});
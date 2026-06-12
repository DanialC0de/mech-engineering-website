// ===============================
// مدیریت فیلدهای OTP
// ===============================
const otpInputs = document.querySelectorAll('.otp-input');
const otpVerifyBtn = document.getElementById("verifyBtn");
const otpErrorDiv = document.getElementById("errorMsg");
const otpLoadingDiv = document.getElementById("loading");

otpInputs.forEach((input, index) => {
    input.addEventListener('input', (e) => {
        let value = e.target.value;

        // تبدیل اعداد فارسی/عربی به انگلیسی
        value = toEnglishDigits(value);
        e.target.value = value;

        // فقط یک عدد مجاز است
        if (value && !/^\d$/.test(value)) {
            e.target.value = '';
            return;
        }

        // رفتن به خانه بعدی
        if (value && index < otpInputs.length - 1) {
            otpInputs[index + 1].focus();
        }

        checkOtpComplete();
    });

    input.addEventListener('keydown', (e) => {
        if (e.key === 'Backspace' && input.value === '' && index > 0) {
            otpInputs[index - 1].focus();
        }
    });

    // پشتیبانی از paste کردن کل کد
    input.addEventListener('paste', (e) => {
        e.preventDefault();

        const pasted = toEnglishDigits(
            (e.clipboardData || window.clipboardData).getData('text')
        ).replace(/\D/g, '');

        if (!pasted) return;

        for (let i = 0; i < otpInputs.length; i++) {
            otpInputs[i].value = pasted[i] || '';
        }

        checkOtpComplete();

        const nextEmpty = Array.from(otpInputs).find(input => !input.value);
        if (nextEmpty) {
            nextEmpty.focus();
        } else {
            otpVerifyBtn.focus();
        }
    });
});

function getOtpCode() {
    let code = '';

    otpInputs.forEach(input => {
        code += toEnglishDigits(input.value);
    });

    return code;
}

function checkOtpComplete() {
    otpVerifyBtn.disabled = getOtpCode().length !== 6;
}

// ===============================
// ارسال کد به Django
// ===============================
otpVerifyBtn.addEventListener("click", async () => {
    const code = getOtpCode();

    if (code.length !== 6) {
        showOtpError("لطفاً کد ۶ رقمی را کامل وارد کنید");
        return;
    }

    setLoading(true);

    try {
        const response = await fetch("/accounts/verify/", {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getOtpCookie("csrftoken")
            },
            body: new URLSearchParams({
                code: code
            })
        });

        /*
          حالت موفق:
          ویوی Django شما بعد از موفقیت redirect("/") می‌کند.
          fetch معمولاً redirect را دنبال می‌کند و response.url می‌شود آدرس نهایی.
        */
        if (response.redirected || response.url !== window.location.href) {
            window.location.href = response.url || "/";
            return;
        }

        /*
          اگر redirect نشد یعنی Django دوباره verify.html را با error برگردانده.
          پس HTML برگشتی را جایگزین می‌کنیم تا پیام خطای Django دیده شود.
        */
        const html = await response.text();

        document.open();
        document.write(html);
        document.close();

    } catch (error) {
        console.error(error);
        showOtpError("خطا در ارتباط با سرور");
        setLoading(false);
    }
});

// ===============================
// loading state
// ===============================
function setLoading(isLoading) {
    otpVerifyBtn.disabled = isLoading;

    if (otpLoadingDiv) {
        otpLoadingDiv.style.display = isLoading ? "block" : "none";
    }

    if (otpErrorDiv && isLoading) {
        otpErrorDiv.style.display = "none";
    }
}

// ===============================
// گرفتن CSRF
// ===============================
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

// ===============================
// تبدیل اعداد فارسی/عربی به انگلیسی
// ===============================
function toEnglishDigits(str) {
    if (!str) return '';

    return str
        .replace(/[۰-۹]/g, d => '۰۱۲۳۴۵۶۷۸۹'.indexOf(d))
        .replace(/[٠-٩]/g, d => '٠١٢٣٤٥٦٧٨٩'.indexOf(d));
}

// ===============================
// نمایش خطا
// ===============================
function showOtpError(msg) {
    if (!otpErrorDiv) {
        alert(msg);
        return;
    }

    otpErrorDiv.textContent = msg;
    otpErrorDiv.style.display = "block";
}

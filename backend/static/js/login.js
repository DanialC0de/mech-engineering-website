// ============================================
// دیتابیس محلی (فقط برای تست)
// ============================================
function initDatabase() {
    let registeredUsers = localStorage.getItem("registeredUsers");
    if (!registeredUsers) {
        const defaultUsers = [
            { phone: "09123456789", email: "rezaei@eng.uk.ac.ir", name: "علی رضایی", role: "student", studentId: "40245636" },
            { phone: "09198765432", email: "karimi@eng.uk.ac.ir", name: "دکتر کریمی", role: "professor", studentId: "40198765" },
            { phone: "09111111111", email: "admin@eng.uk.ac.ir", name: "ادمین سیستم", role: "admin", studentId: "admin001" }
        ];
        localStorage.setItem("registeredUsers", JSON.stringify(defaultUsers));
        console.log("✅ Database initialized with default users");
    }
}
initDatabase();

// ============================================
// متغیرها
// ============================================
let activeTab = "phone";

// ============================================
// مدیریت تب‌ها
// ============================================
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        activeTab = this.getAttribute('data-tab');

        if (activeTab === 'phone') {
            document.getElementById('phoneTab').style.display = 'block';
            document.getElementById('emailTab').style.display = 'none';
        } else {
            document.getElementById('phoneTab').style.display = 'none';
            document.getElementById('emailTab').style.display = 'block';
        }
        document.getElementById("errorMsg").style.display = "none";
    });
});

// ============================================
// توابع اعتبارسنجی
// ============================================
function validatePhoneNumber(phone) {
    phone = phone.trim();
    const phonePattern = /^09[0-9]{9}$/;
    if (!phone) return { valid: false, message: "لطفاً شماره موبایل را وارد کنید" };
    if (!phonePattern.test(phone)) return { valid: false, message: "شماره موبایل معتبر نیست (باید با 09 شروع شود)" };
    return { valid: true, message: "" };
}

function validateEmail(email) {
    email = email.trim();
    const emailPattern = /^[^\s@]+@([^\s@.,]+\.)+[^\s@.,]{2,}$/;
    if (!email) return { valid: false, message: "لطفاً آدرس ایمیل را وارد کنید" };
    if (!emailPattern.test(email)) return { valid: false, message: "آدرس ایمیل معتبر نیست" };
    return { valid: true, message: "" };
}

function showError(message) {
    const errorDiv = document.getElementById("errorMsg");
    errorDiv.textContent = message;
    errorDiv.style.display = "block";
    setTimeout(() => errorDiv.style.display = "none", 3500);
}

function showLoading(show) {
    const loadingDiv = document.getElementById("loading");
    const loginBtn = document.getElementById("loginBtn");
    if (show) {
        loadingDiv.style.display = "block";
        loginBtn.disabled = true;
        loginBtn.style.opacity = "0.6";
    } else {
        loadingDiv.style.display = "none";
        loginBtn.disabled = false;
        loginBtn.style.opacity = "1";
    }
}

// ============================================
// اعتبارسنجی ورودی شماره موبایل
// ============================================
document.getElementById("phoneNumber").addEventListener("input", function(e) {
    let value = this.value.replace(/\D/g, "");
    if (value.length > 11) value = value.slice(0, 11);
    this.value = value;
});

// ============================================
// ✅ دریافت CSRF Token
// ============================================
function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            return value;
        }
    }
    return '';
}

// ============================================
// ✅ ارسال فرم (فقط یک رویداد)
// ============================================
document.getElementById("loginForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    let identifier;

    if (activeTab === 'phone') {
        let phone = document.getElementById("phoneNumber").value.trim();
        if (phone.length === 10 && phone.startsWith("9")) phone = "0" + phone;
        const validation = validatePhoneNumber(phone);
        if (!validation.valid) {
            showError(validation.message);
            return;
        }
        identifier = phone;
    } else {
        const email = document.getElementById("emailAddress").value.trim();
        const validation = validateEmail(email);
        if (!validation.valid) {
            showError(validation.message);
            return;
        }
        identifier = email;
        // ورود با ایمیل - فعلاً غیرفعال
        showError("⏳ ورود با ایمیل در حال توسعه است");
        return;
    }

    showLoading(true);

    try {
        const response = await fetch("/accounts/send-otp/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()
            },
            body: JSON.stringify({
                phone: identifier
            })
        });

        const data = await response.json();
        console.log("📡 پاسخ سرور:", data);

        if (data.status === "sent") {
            localStorage.setItem("tempPhone", identifier);
            window.location.href = "/accounts/verify/";
        } else {
            showError(data.message || "خطا در ارسال کد");
            showLoading(false);
        }

    } catch (error) {
        console.error("❌ خطا:", error);
        showError("ارتباط با سرور برقرار نشد");
        showLoading(false);
    }
});

// ============================================
// فوکوس اولیه
// ============================================
setTimeout(() => {
    document.getElementById("phoneNumber").focus();
}, 100);
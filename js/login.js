// ==================== راه‌اندازی دیتابیس کاربران (یکسان در همه صفحات) ====================
function initDatabase() {
    let registeredUsers = localStorage.getItem("registeredUsers");

    if (!registeredUsers) {
        // دیتابیس اولیه
        const defaultUsers = [
            { phone: "09123456789", email: "ali@mech.ac.ir", name: "علی رضایی", role: "student", studentId: "40112345" },
            { phone: "09198765432", email: "karimi@mech.ac.ir", name: "دکتر کریمی", role: "professor", studentId: "40198765" },
            { phone: "09111111111", email: "admin@mech.ac.ir", name: "ادمین سیستم", role: "admin", studentId: "admin001" }
        ];
        localStorage.setItem("registeredUsers", JSON.stringify(defaultUsers));
        console.log("Database initialized with default users");
    }
}

// اجرای راه‌اندازی دیتابیس
initDatabase();

let activeTab = "phone";

// مدیریت تب‌ها
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', function () {
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

document.getElementById("loginForm").addEventListener("submit", function (e) {
    e.preventDefault();

    let identifier, type;

    if (activeTab === 'phone') {
        let phone = document.getElementById("phoneNumber").value.trim();
        if (phone.length === 10 && phone.startsWith("9")) phone = "0" + phone;
        const validation = validatePhoneNumber(phone);
        if (!validation.valid) { showError(validation.message); return; }
        identifier = phone;
        type = 'phone';
    } else {
        const email = document.getElementById("emailAddress").value.trim();
        const validation = validateEmail(email);
        if (!validation.valid) { showError(validation.message); return; }
        identifier = email;
        type = 'email';
    }

    showLoading(true);

    setTimeout(() => {
        localStorage.setItem("tempIdentifier", identifier);
        localStorage.setItem("tempIdentifierType", type);
        window.location.href = "verify.html";
    }, 800);
});

document.getElementById("phoneNumber").addEventListener("input", function (e) {
    let value = this.value.replace(/\D/g, "");
    if (value.length > 11) value = value.slice(0, 11);
    this.value = value;
});

setTimeout(() => {
    document.getElementById("phoneNumber").focus();
}, 100);
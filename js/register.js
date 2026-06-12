// ============================================================
// دریافت اطلاعات از صفحه قبل (کد تایید)
// ============================================================
const tempIdentifier = localStorage.getItem("tempIdentifier");
const tempIdentifierType = localStorage.getItem("tempIdentifierType");

console.log("Register page - tempIdentifier:", tempIdentifier);
console.log("Register page - tempIdentifierType:", tempIdentifierType);

// اگر اطلاعات وجود نداشت برگرد به لاگین
if (!tempIdentifier) {
    alert("خطا: اطلاعات ورودی یافت نشد. لطفاً از صفحه ورود اقدام کنید.");
    window.location.href = "login.html";
}

// ============================================================
// نمایش اطلاعات ورودی
// ============================================================
function displayIdentifierInfo() {
    const infoValue = document.getElementById("infoValue");
    const infoLabel = document.getElementById("infoLabel");

    if (tempIdentifierType === "phone") {
        infoLabel.innerHTML = "📱 شماره موبایل:";
        let phone = tempIdentifier;
        if (phone.length === 11) {
            let part1 = phone.slice(0, 4);
            let part2 = phone.slice(7, 11);
            let masked = `${part1}***${part2}`;
            infoValue.innerHTML = masked;
        } else {
            infoValue.innerHTML = phone;
        }
    } else if (tempIdentifierType === "email") {
        infoLabel.innerHTML = "✉️ آدرس ایمیل:";
        let email = tempIdentifier;
        if (email.includes("@")) {
            let parts = email.split("@");
            let local = parts[0];
            let domain = parts[1];
            let maskedLocal = local.length > 2 ? local[0] + "***" + local[local.length - 1] : "***";
            infoValue.innerHTML = maskedLocal + "@" + domain;
        } else {
            infoValue.innerHTML = email;
        }
    }
}

displayIdentifierInfo();

// ============================================================
// اعتبارسنجی
// ============================================================
function validateForm() {
    const firstName = document.getElementById("firstName").value.trim();
    const lastName = document.getElementById("lastName").value.trim();
    const studentId = document.getElementById("studentId").value.trim();
    const degree = document.getElementById("degree").value;
    const major = document.getElementById("major").value.trim();

    if (!firstName) {
        showError("لطفاً نام خود را وارد کنید");
        return false;
    }
    if (!lastName) {
        showError("لطفاً نام خانوادگی خود را وارد کنید");
        return false;
    }
    if (!studentId) {
        showError("لطفاً شماره دانشجویی خود را وارد کنید");
        return false;
    }
    if (studentId.length < 6) {
        showError("شماره دانشجویی معتبر نیست");
        return false;
    }
    if (!degree) {
        showError("لطفاً مقطع تحصیلی خود را انتخاب کنید");
        return false;
    }
    if (!major) {
        showError("لطفاً رشته تحصیلی خود را وارد کنید");
        return false;
    }

    // بررسی تکراری نبودن شماره دانشجویی
    const dbUsers = JSON.parse(localStorage.getItem("registeredUsers")) || [];
    const existingUser = dbUsers.find(u => u.studentId === studentId);
    if (existingUser) {
        showError("این شماره دانشجویی قبلاً ثبت شده است");
        return false;
    }

    return true;
}

// ============================================================
// ذخیره کاربر جدید
// ============================================================
function saveNewUser() {
    const firstName = document.getElementById("firstName").value.trim();
    const lastName = document.getElementById("lastName").value.trim();
    const studentId = document.getElementById("studentId").value.trim();
    const degree = document.getElementById("degree").value;
    const major = document.getElementById("major").value.trim();
    const term = document.getElementById("term").value;
    const committee = document.getElementById("committee").value;
    const interest = document.getElementById("interest").value.trim();
    const bio = document.getElementById("bio").value.trim();

    // خواندن دیتابیس موجود
    let dbUsers = JSON.parse(localStorage.getItem("registeredUsers")) || [];

    // ایجاد کاربر جدید
    const newUser = {
        phone: tempIdentifierType === "phone" ? tempIdentifier : null,
        email: tempIdentifierType === "email" ? tempIdentifier : null,
        name: `${firstName} ${lastName}`,
        firstName: firstName,
        lastName: lastName,
        studentId: studentId,
        degree: degree,
        major: major,
        term: term,
        committee: committee,
        interest: interest,
        bio: bio,
        role: "student",
        status: "pending",
        registerDate: new Date().toISOString()
    };

    dbUsers.push(newUser);
    localStorage.setItem("registeredUsers", JSON.stringify(dbUsers));

    // پاک کردن اطلاعات موقت
    localStorage.removeItem("tempIdentifier");
    localStorage.removeItem("tempIdentifierType");

    return newUser;
}

// ============================================================
// توابع کمکی
// ============================================================
function showError(message) {
    const errorDiv = document.getElementById("errorMsg");
    const successDiv = document.getElementById("successMsg");
    errorDiv.textContent = message;
    errorDiv.style.display = "block";
    successDiv.style.display = "none";

    setTimeout(() => {
        errorDiv.style.display = "none";
    }, 4000);
}

function showSuccess(message) {
    const successDiv = document.getElementById("successMsg");
    const errorDiv = document.getElementById("errorMsg");
    successDiv.textContent = message;
    successDiv.style.display = "block";
    errorDiv.style.display = "none";
}

function showLoading(show) {
    const loadingDiv = document.getElementById("loading");
    const registerBtn = document.getElementById("registerBtn");

    if (show) {
        loadingDiv.style.display = "block";
        registerBtn.disabled = true;
        registerBtn.style.opacity = "0.6";
    } else {
        loadingDiv.style.display = "none";
        registerBtn.disabled = false;
        registerBtn.style.opacity = "1";
    }
}

// ============================================================
// هندل فرم
// ============================================================
document.getElementById("registerForm").addEventListener("submit", function (e) {
    e.preventDefault();

    if (!validateForm()) {
        return;
    }

    showLoading(true);

    setTimeout(() => {
        try {
            const newUser = saveNewUser();
            console.log("New user saved:", newUser);

            showSuccess("✅ ثبت‌نام شما با موفقیت انجام شد! در حال انتقال به صفحه ورود...");

            setTimeout(() => {
                window.location.href = "login.html";
            }, 2000);
        } catch (error) {
            showError("خطایی در ثبت‌نام رخ داد. لطفاً مجدداً تلاش کنید.");
            showLoading(false);
        }
    }, 1000);
});

// ============================================================
// اعتبارسنجی لحظه‌ای شماره دانشجویی
// ============================================================
document.getElementById("studentId").addEventListener("input", function (e) {
    let value = this.value.replace(/[^0-9]/g, "");
    this.value = value;
});
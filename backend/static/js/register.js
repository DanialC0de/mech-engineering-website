// ============================================================
// Register JS - Django Backend Version
// ============================================================

const registerForm = document.getElementById("registerForm");
const registerBtn = document.getElementById("registerBtn");

const errorDiv = document.getElementById("errorMsg");
const successDiv = document.getElementById("successMsg");
const loadingDiv = document.getElementById("loading");

// ============================================================
// نمایش شماره موبایل تایید شده
// ============================================================
function displayVerifiedPhone() {
    const infoValue = document.getElementById("infoValue");
    const infoLabel = document.getElementById("infoLabel");

    const phone = localStorage.getItem("tempPhone");

    if (!phone) {
        // اگر شماره در localStorage نبود، کاربر را برگردان
        window.location.href = "/accounts/login/";
        return;
    }

    infoLabel.innerHTML = "📱 شماره موبایل:";
    infoValue.innerHTML = maskPhone(phone);
}

function maskPhone(phone) {
    if (!phone || phone.length !== 11) return phone || "";

    const part1 = phone.slice(0, 4);
    const part2 = phone.slice(7, 11);
    return `${part1}***${part2}`;
}

displayVerifiedPhone();

// ============================================================
// اعتبارسنجی فرم
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

    return true;
}

// ============================================================
// ارسال ثبت‌نام به Django
// ============================================================
registerForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    if (!validateForm()) return;

    const phone = localStorage.getItem("tempPhone");

    if (!phone) {
        showError("شماره موبایل یافت نشد. لطفاً دوباره وارد شوید.");
        setTimeout(() => {
            window.location.href = "/accounts/login/";
        }, 1500);
        return;
    }

    showLoading(true);

    const firstName = document.getElementById("firstName").value.trim();
    const lastName = document.getElementById("lastName").value.trim();
    const studentId = document.getElementById("studentId").value.trim();
    const degree = document.getElementById("degree").value;
    const major = document.getElementById("major").value.trim();
    const term = document.getElementById("term").value;
    const committee = document.getElementById("committee").value;
    const interest = document.getElementById("interest").value.trim();
    const bio = document.getElementById("bio").value.trim();

    try {
        const response = await fetch("/accounts/register-user/", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: new URLSearchParams({
                phone: phone,
                username: studentId,
                first_name: firstName,
                last_name: lastName,
                student_id: studentId,
                degree: degree,
                major: major,
                term: term,
                committee: committee,
                interest: interest,
                bio: bio
            })
        });

        if (response.redirected) {
            localStorage.removeItem("tempPhone");
            window.location.href = response.url;
            return;
        }

        const data = await response.json();

        if (data.status === "ok") {
            localStorage.removeItem("tempPhone");

            showSuccess("✅ ثبت‌نام شما با موفقیت انجام شد.");

            setTimeout(() => {
                window.location.href = data.redirect || "/student-panel/";
            }, 1000);
        } else {
            showError(data.message || "خطا در ثبت‌نام");
        }

    } catch (error) {
        console.error(error);
        showError("خطا در ارتباط با سرور");
    } finally {
        showLoading(false);
    }
});

// ============================================================
// اعتبارسنجی لحظه‌ای شماره دانشجویی
// ============================================================
const studentIdInput = document.getElementById("studentId");

if (studentIdInput) {
    studentIdInput.addEventListener("input", function () {
        this.value = this.value.replace(/[^0-9]/g, "");
    });
}

// ============================================================
// توابع کمکی
// ============================================================
function showError(message) {
    if (!errorDiv) return;

    errorDiv.textContent = message;
    errorDiv.style.display = "block";

    if (successDiv) {
        successDiv.style.display = "none";
    }

    setTimeout(() => {
        errorDiv.style.display = "none";
    }, 4000);
}

function showSuccess(message) {
    if (!successDiv) return;

    successDiv.textContent = message;
    successDiv.style.display = "block";

    if (errorDiv) {
        errorDiv.style.display = "none";
    }
}

function showLoading(show) {
    if (loadingDiv) {
        loadingDiv.style.display = show ? "block" : "none";
    }

    if (registerBtn) {
        registerBtn.disabled = show;
        registerBtn.style.opacity = show ? "0.6" : "1";
    }
}

function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {
            cookie = cookie.trim();

            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }

    return cookieValue;
}

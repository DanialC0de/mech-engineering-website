// ============================================================
// Register JS - Django Backend Version (Complete)
// ============================================================

document.addEventListener("DOMContentLoaded", function () {

    const registerForm = document.getElementById("registerForm");
    const registerBtn = document.querySelector(".register-btn");

    const errorDiv = document.getElementById("errorMsg");
    const successDiv = document.getElementById("successMsg");

    if (!registerForm) {
        console.error("registerForm پیدا نشد");
        return;
    }

    // ============================================================
    // نمایش شماره موبایل تایید شده
    // ============================================================
    function displayVerifiedPhone() {
        const infoValue = document.getElementById("infoValue");
        const phone = localStorage.getItem("tempPhone");

        if (!phone) {
            // اگر شماره موبایل نبود، به صفحه ورود برگرد
            window.location.href = "/accounts/login/";
            return;
        }

        if (infoValue) {
            infoValue.textContent = maskPhone(phone);
        }
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

        // پاک کردن پیام‌های قبلی
        hideError();
        hideSuccess();

        if (!firstName) {
            showError("لطفاً نام خود را وارد کنید");
            document.getElementById("firstName").focus();
            return false;
        }

        if (!lastName) {
            showError("لطفاً نام خانوادگی خود را وارد کنید");
            document.getElementById("lastName").focus();
            return false;
        }

        if (!studentId) {
            showError("لطفاً شماره دانشجویی خود را وارد کنید");
            document.getElementById("studentId").focus();
            return false;
        }

        if (studentId.length < 6) {
            showError("شماره دانشجویی باید حداقل ۶ رقم باشد");
            document.getElementById("studentId").focus();
            return false;
        }

        if (!degree) {
            showError("لطفاً مقطع تحصیلی خود را انتخاب کنید");
            document.getElementById("degree").focus();
            return false;
        }

        if (!major) {
            showError("لطفاً رشته تحصیلی خود را وارد کنید");
            document.getElementById("major").focus();
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

        // دریافت اطلاعات از فرم
        const firstName = document.getElementById("firstName").value.trim();
        const lastName = document.getElementById("lastName").value.trim();
        const studentId = document.getElementById("studentId").value.trim();
        const degree = document.getElementById("degree").value;
        const major = document.getElementById("major").value.trim();
        const term = document.getElementById("term").value;
        const committee = document.getElementById("committee").value;
        const interest = document.getElementById("interest").value.trim();
        const bio = document.getElementById("bio").value.trim();

        // غیرفعال کردن دکمه ثبت‌نام
        if (registerBtn) {
            registerBtn.disabled = true;
            registerBtn.textContent = "⏳ در حال ثبت‌نام...";
            registerBtn.style.opacity = "0.6";
            registerBtn.style.cursor = "not-allowed";
        }

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

            const data = await response.json();

            if (data.status === "ok") {
                // پاک کردن اطلاعات موقت
                localStorage.removeItem("tempPhone");
                localStorage.removeItem("otpCode");

                showSuccess("✅ ثبت‌نام شما با موفقیت انجام شد. در حال انتقال به پنل...");

                setTimeout(() => {
                    window.location.href = data.redirect || "/panel/student/";
                }, 1500);

            } else {
                showError(data.message || "خطا در ثبت‌نام. لطفاً دوباره تلاش کنید.");
                // فعال کردن مجدد دکمه
                if (registerBtn) {
                    registerBtn.disabled = false;
                    registerBtn.textContent = "✓ ثبت‌نام و عضویت در انجمن";
                    registerBtn.style.opacity = "1";
                    registerBtn.style.cursor = "pointer";
                }
            }

        } catch (error) {
            console.error("خطا در ثبت‌نام:", error);
            showError("خطا در ارتباط با سرور. لطفاً دوباره تلاش کنید.");
            
            // فعال کردن مجدد دکمه
            if (registerBtn) {
                registerBtn.disabled = false;
                registerBtn.textContent = "✓ ثبت‌نام و عضویت در انجمن";
                registerBtn.style.opacity = "1";
                registerBtn.style.cursor = "pointer";
            }
        }
    });

    // ============================================================
    // اعتبارسنجی لحظه‌ای شماره دانشجویی (فقط عدد)
    // ============================================================
    const studentIdInput = document.getElementById("studentId");

    if (studentIdInput) {
        studentIdInput.addEventListener("input", function () {
            this.value = this.value.replace(/[^0-9]/g, "");
            
            // حذف خطا هنگام تایپ
            if (errorDiv && errorDiv.style.display !== "none") {
                hideError();
            }
        });
    }

    // ============================================================
    // پاک کردن خطا هنگام کلیک روی فیلدها
    // ============================================================
    const inputs = document.querySelectorAll("input, select, textarea");
    inputs.forEach(input => {
        input.addEventListener("focus", function () {
            if (errorDiv && errorDiv.style.display !== "none") {
                hideError();
            }
        });
    });

    // ============================================================
    // جلوگیری از ارسال مجدد با Enter
    // ============================================================
    registerForm.addEventListener("keydown", function (e) {
        if (e.key === "Enter") {
            const target = e.target;
            if (target.tagName !== "TEXTAREA") {
                e.preventDefault();
                registerForm.dispatchEvent(new Event("submit"));
            }
        }
    });

    // ============================================================
    // توابع کمکی
    // ============================================================
    function showError(message) {
        if (!errorDiv) return;

        errorDiv.textContent = message;
        errorDiv.style.display = "block";
        errorDiv.style.backgroundColor = "#f8d7da";
        errorDiv.style.color = "#721c24";
        errorDiv.style.border = "1px solid #f5c6cb";
        errorDiv.style.padding = "10px";
        errorDiv.style.borderRadius = "4px";
        errorDiv.style.marginBottom = "15px";

        if (successDiv) {
            successDiv.style.display = "none";
        }
    }

    function hideError() {
        if (errorDiv) {
            errorDiv.style.display = "none";
            errorDiv.textContent = "";
        }
    }

    function showSuccess(message) {
        if (!successDiv) return;

        successDiv.textContent = message;
        successDiv.style.display = "block";
        successDiv.style.backgroundColor = "#d4edda";
        successDiv.style.color = "#155724";
        successDiv.style.border = "1px solid #c3e6cb";
        successDiv.style.padding = "10px";
        successDiv.style.borderRadius = "4px";
        successDiv.style.marginBottom = "15px";

        if (errorDiv) {
            errorDiv.style.display = "none";
        }
    }

    function hideSuccess() {
        if (successDiv) {
            successDiv.style.display = "none";
            successDiv.textContent = "";
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

    // ============================================================
    // نمایش پیام‌های سرور (اگر قبلاً خطایی بوده)
    // ============================================================
    const urlParams = new URLSearchParams(window.location.search);
    const error = urlParams.get("error");
    const success = urlParams.get("success");

    if (error) {
        showError(decodeURIComponent(error));
    }

    if (success) {
        showSuccess(decodeURIComponent(success));
    }

    console.log("✅ Register.js بارگذاری شد");
});
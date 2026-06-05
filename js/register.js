document.getElementById("registerForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const firstName = document.getElementById("firstName").value;
    const lastName = document.getElementById("lastName").value;
    const studentId = document.getElementById("studentId").value;
    const email = document.getElementById("email").value;
    const phone = document.getElementById("phone").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    // اعتبارسنجی
    if (!firstName || !lastName || !studentId || !email || !phone || !password) {
        showError("لطفاً تمام فیلدها را پر کنید");
        return;
    }

    if (password !== confirmPassword) {
        showError("رمز عبور و تکرار آن مطابقت ندارند");
        return;
    }

    if (password.length < 6) {
        showError("رمز عبور باید حداقل ۶ کاراکتر باشد");
        return;
    }

    // شبیه‌سازی ثبت در دیتابیس
    const newUser = {
        firstName: firstName,
        lastName: lastName,
        studentId: studentId,
        email: email,
        phone: phone,
        password: password,
        role: "student",  // پیش‌فرض دانشجو
        status: "pending" // در انتظار تأیید ادمین
    };

    // ذخیره در localStorage (شبیه‌سازی دیتابیس)
    let users = JSON.parse(localStorage.getItem("registeredUsers") || "[]");
    users.push(newUser);
    localStorage.setItem("registeredUsers", JSON.stringify(users));

    // نمایش موفقیت و هدایت به صفحه لاگین
    document.getElementById("successMsg").style.display = "block";
    document.getElementById("errorMsg").style.display = "none";

    setTimeout(() => {
        window.location.href = "login.html";
    }, 2000);
});

function showError(msg) {
    document.getElementById("errorMsg").textContent = msg;
    document.getElementById("errorMsg").style.display = "block";
    document.getElementById("successMsg").style.display = "none";
}
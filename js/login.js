// شبیه‌سازی دیتابیس کاربران
const users = [
    { username: "student@mech.ac.ir", password: "123456", role: "student", name: "علی رضایی" },
    { username: "professor@mech.ac.ir", password: "123456", role: "professor", name: "دکتر کریمی" },
    { username: "admin@mech.ac.ir", password: "123456", role: "admin", name: "ادمین سیستم" }
];

document.getElementById("loginForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const user = users.find(u => u.username === username && u.password === password);

    if (user) {
        // ذخیره اطلاعات کاربر در localStorage
        localStorage.setItem("currentUser", JSON.stringify({
            name: user.name,
            username: user.username,
            role: user.role
        }));

        // هدایت به پنل مناسب بر اساس نقش
        switch (user.role) {
            case "admin":
                window.location.href = "admin/index.html";
                break;
            case "professor":
                window.location.href = "professor/index.html";
                break;
            default:
                window.location.href = "student/index.html";
        }
    } else {
        document.getElementById("errorMsg").style.display = "block";
    }
});
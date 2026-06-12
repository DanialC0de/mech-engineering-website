document.getElementById("loginForm").addEventListener("submit", async function(e) {

    e.preventDefault();

    const phone = document.getElementById("phoneNumber").value.trim();

    if (!phone) {
        alert("شماره موبایل را وارد کنید");
        return;
    }

    try {

        const response = await fetch("/accounts/send-otp/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                phone: phone
            })
        });

        const data = await response.json();

        console.log(data);

        if (data.status === "sent") {

            localStorage.setItem("tempPhone", phone);

            window.location.href = "/accounts/verify/";

        } else {

            alert(data.message || "خطا در ارسال کد");

        }

    } catch (error) {

        console.error(error);

        alert("ارتباط با سرور برقرار نشد");

    }

});
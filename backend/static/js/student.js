// ========== داده‌های شبیه‌سازی شده ==========
let availableEvents = [
    { id: 1, title: "وبینار سیستم‌های تعلیق", date: "۱۴۰۴/۰۱/۲۰", capacity: 50, registered: 45, type: "کارگاه" },
    { id: 2, title: "بازدید از ایران خودرو", date: "۱۴۰۴/۰۲/۰۵", capacity: 30, registered: 28, type: "بازدید" },
    { id: 3, title: "مسابقه سالیدورک", date: "۱۴۰۴/۰۲/۱۵", capacity: 20, registered: 10, type: "مسابقه" }
];

let myRegistrationsList = [
    { id: 1, title: "همایش مکانیک سیالات", date: "۱۴۰۴/۰۱/۱۰", status: "تأیید شده" }
];

let resourcesData = [
    { id: 1, title: "جزوه ترمودینامیک پیشرفته", category: "آموزشی", desc: "جزوه کامل ترمودینامیک - دکتر کریمی" },
    { id: 2, title: "مقالات همایش ملی مکانیک", category: "پژوهشی", desc: "مجموعه مقالات پذیرفته شده ۱۴۰۳" },
    { id: 3, title: "گزارش بازدید صنعتی", category: "صنعتی", desc: "گزارش تصویری بازدید از ایران خودرو" },
];

let ticketsList = [
    { id: "T-001", subject: "مشکل در ثبت‌نام", status: "پاسخ داده شده", date: "۱۴۰۴/۰۱/۰۵" }
];

let downloadHistory = 5;

// ========== توابع رندر ==========
function updateStats() {
    document.getElementById("myRegistrations").innerText = myRegistrationsList.length;
    document.getElementById("newResources").innerText = "۳";
    document.getElementById("myTickets").innerText = ticketsList.length;
    document.getElementById("eventCount").innerText = myRegistrationsList.length;
    document.getElementById("downloadCount").innerText = downloadHistory;
}

function renderAvailableEvents() {
    let html = "";
    availableEvents.forEach(ev => {
        let remaining = ev.capacity - ev.registered;
        let isRegistered = myRegistrationsList.some(r => r.title === ev.title);
        html += `<tr>
                    <td>${ev.title}</td><td>${ev.date}</td><td>${remaining}</td>
                    <td>${!isRegistered ? `<button class="register-btn" onclick="registerEvent(${ev.id}, '${ev.title}')">✓ ثبت‌نام</button>` : '<span style="color:green;">✓ ثبت‌نام شده</span>'}</td>
                </tr>`;
    });
    document.getElementById("availableEventsBody").innerHTML = html;
}

function renderAllEvents() {
    let html = "";
    availableEvents.forEach(ev => {
        let isRegistered = myRegistrationsList.some(r => r.title === ev.title);
        html += `<tr>
                    <td>${ev.title}</td><td>${ev.date}</td><td>${ev.type}</td>
                    <td><span class="status-accepted">فعال</span></td>
                    <td>${!isRegistered ? `<button class="register-btn" onclick="registerEvent(${ev.id}, '${ev.title}')">ثبت‌نام</button>` : 'ثبت‌نام شده'}</td>
                </tr>`;
    });
    document.getElementById("allEventsBody").innerHTML = html;
}

function renderMyRegistrations() {
    let html = "";
    myRegistrationsList.forEach(reg => {
        html += `<tr>
                    <td>${reg.title}</td><td>${reg.date}</td>
                    <td><span class="status-accepted">${reg.status}</span></td>
                    <td><button class="ticket-btn" onclick="cancelRegistration('${reg.title}')">لغو ثبت‌نام</button></td>
                </tr>`;
    });
    document.getElementById("myRegistrationsBody").innerHTML = html;
}

function renderResources() {
    let html = "";
    resourcesData.forEach(res => {
        html += `<tr>
                    <td>${res.title}</td><td>${res.category}</td><td>${res.desc}</td>
                    <td><button class="download-btn" onclick="downloadResource(${res.id}, '${res.title}')">📥 دانلود</button></td>
                </tr>`;
    });
    document.getElementById("resourcesBody").innerHTML = html;
}

function renderTickets() {
    let html = "";
    ticketsList.forEach(t => {
        html += `<tr>
                    <td>${t.id}</td><td>${t.subject}</td>
                    <td><span class="${t.status === 'پاسخ داده شده' ? 'status-accepted' : 'status-pending'}">${t.status}</span></td>
                    <td>${t.date}</td>
                    <td><button class="register-btn" onclick="viewTicket('${t.id}')">مشاهده</button></td>
                </tr>`;
    });
    document.getElementById("ticketsBody").innerHTML = html;
}

// ========== توابع عملیاتی ==========
function registerEvent(id, title) {
    let event = availableEvents.find(e => e.id === id);
    if (event && event.registered < event.capacity) {
        event.registered++;
        myRegistrationsList.push({
            id: myRegistrationsList.length + 1,
            title: title,
            date: event.date,
            status: "تأیید شده"
        });
        updateStats();
        renderAvailableEvents();
        renderAllEvents();
        renderMyRegistrations();
        alert(`شما در رویداد "${title}" با موفقیت ثبت‌نام شدید`);
    } else {
        alert("ظرفیت رویداد پر است! آیا مایل به قرار گرفتن در صف انتظار هستید؟");
    }
}

function cancelRegistration(title) {
    if (confirm(`آیا از لغو ثبت‌نام در "${title}" اطمینان دارید؟`)) {
        myRegistrationsList = myRegistrationsList.filter(r => r.title !== title);
        let event = availableEvents.find(e => e.title === title);
        if (event) event.registered--;
        updateStats();
        renderAvailableEvents();
        renderAllEvents();
        renderMyRegistrations();
        alert("ثبت‌نام با موفقیت لغو شد");
    }
}

function downloadResource(id, title) {
    downloadHistory++;
    updateStats();
    alert(`فایل "${title}" در حال دانلود...`);
}

function submitTicket() {
    let subject = document.getElementById("ticketSubject").value;
    let message = document.getElementById("ticketMessage").value;
    if (!subject || !message) { alert("لطفاً موضوع و متن تیکت را وارد کنید"); return; }

    ticketsList.push({
        id: `T-${String(ticketsList.length + 2).padStart(3, '0')}`,
        subject: subject,
        status: "جدید",
        date: new Date().toLocaleDateString('fa-IR')
    });
    updateStats();
    renderTickets();
    closeTicketModal();
    alert("تیکت شما با موفقیت ارسال شد");
}

function filterResources() {
    let filter = document.getElementById("resourceFilter").value;
    let filtered = filter === "all" ? resourcesData : resourcesData.filter(r => r.category === filter);
    let html = "";
    filtered.forEach(res => {
        html += `<tr>
                    <td>${res.title}</td><td>${res.category}</td><td>${res.desc}</td>
                    <td><button class="download-btn" onclick="downloadResource(${res.id}, '${res.title}')">📥 دانلود</button></td>
                </tr>`;
    });
    document.getElementById("resourcesBody").innerHTML = html;
}

function changePassword() {
    let newPass = document.getElementById("newPassword").value;
    let confirmPass = document.getElementById("confirmNewPassword").value;
    if (!newPass) { alert("لطفاً رمز عبور جدید را وارد کنید"); return; }
    if (newPass !== confirmPass) { alert("رمز عبور و تکرار آن مطابقت ندارند"); return; }
    alert("رمز عبور با موفقیت تغییر کرد");
}

function changeProfilePic() { alert("تغییر عکس پروفایل"); }
function viewTicket(id) { alert(`مشاهده تیکت ${id}`); }

// ========== مودال‌ها ==========
function openNewTicketModal() { document.getElementById("newTicketModal").style.display = "flex"; }
function closeTicketModal() { document.getElementById("newTicketModal").style.display = "none"; }

function logout() { localStorage.removeItem("currentUser"); window.location.href = "../login.html"; }

// ========== تب‌ها ==========
document.querySelectorAll('.menu li').forEach(item => {
    item.addEventListener('click', function () {
        document.querySelectorAll('.menu li').forEach(li => li.classList.remove('active'));
        this.classList.add('active');
        let tabId = this.getAttribute('data-tab');
        document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
        document.getElementById(tabId).classList.add('active');
        document.getElementById("pageTitle").innerText = this.innerText.trim();
    });
});

updateStats();
renderAvailableEvents();
renderAllEvents();
renderMyRegistrations();
renderResources();
renderTickets();

//hide side bar
document.getElementById('toggleSidebar').addEventListener('click', function () {

    if (document.querySelector('.sidebar').style.marginRight == '-240px') {
        document.querySelector('.sidebar').style.marginRight = '0';
        document.querySelector('.main-content').style.marginRight = '280px';
    }
    else {
        document.querySelector('.sidebar').style.marginRight = '-240px';
        document.querySelector('.main-content').style.marginRight = '50px';
    }
});
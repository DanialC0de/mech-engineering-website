// ==================== داده‌های شبیه‌سازی شده ====================
let students = [
    { id: 1, name: "علی رضایی", studentId: "40112345", email: "ali@mech.ac.ir", status: "فعال" },
    { id: 2, name: "سارا احمدی", studentId: "40123456", email: "sara@mech.ac.ir", status: "فعال" },
    { id: 3, name: "محمد حسینی", studentId: "40134567", email: "mohammad@mech.ac.ir", status: "غیرفعال" }
];

let professors = [
    { id: 1, name: "دکتر کریمی", position: "دانشیار", email: "karimi@mech.ac.ir", events: 5 },
    { id: 2, name: "دکتر رضایی", position: "استادتمام", email: "rezaei@mech.ac.ir", events: 8 }
];

let members = [
    { id: 1, name: "رضا کریمی", role: "عضو عادی", committee: "آموزش", activity: "فعال" },
    { id: 2, name: "زهرا محمدی", role: "مسئول کمیته", committee: "پژوهشی", activity: "فعال" }
];

let pendingRequestsList = [
    { id: 1, name: "مهدی عباسی", studentId: "40145678", committee: "صنعتی", status: "pending" },
    { id: 2, name: "نرگس کریمی", studentId: "40156789", committee: "آموزش", status: "pending" }
];

let eventsList = [
    { id: 1, title: "وبینار سیستم‌های تعلیق", date: "۱۴۰۴/۰۱/۲۰", type: "کارگاه", status: "فعال", capacity: 50, registered: 45, committee: "آموزش" },
    { id: 2, title: "بازدید از ایران خودرو", date: "۱۴۰۴/۰۲/۰۵", type: "بازدید", status: "فعال", capacity: 30, registered: 30, committee: "صنعتی" }
];

let resourcesList = [
    { id: 1, title: "جزوه ترمودینامیک پیشرفته", category: "آموزشی", access: "عمومی", downloads: 120 },
    { id: 2, title: "گزارش جلسه کمیته پژوهش", category: "گزارش جلسات", access: "فقط اعضا", downloads: 45 }
];

let ticketsList = [
    { id: "T-001", sender: "علی رضایی", subject: "مشکل در ثبت‌نام", status: "جدید", date: "۱۴۰۴/۰۱/۱۰" },
    { id: "T-002", sender: "سارا احمدی", subject: "درخواست منبع آموزشی", status: "در انتظار", date: "۱۴۰۴/۰۱/۱۲" }
];

// ==================== توابع کمکی ====================
function updateStats() {
    document.getElementById("studentCount").innerText = students.length;
    document.getElementById("professorCount").innerText = professors.length;
    document.getElementById("memberCount").innerText = members.length;
    document.getElementById("eventCount").innerText = eventsList.filter(e => e.status === "فعال").length;
    document.getElementById("pendingRequests").innerText = pendingRequestsList.length;
    document.getElementById("pendingCountBadge").innerText = pendingRequestsList.length + " درخواست";
    document.getElementById("reportParticipation").innerText = "۷۵%";
    document.getElementById("reportDownloads").innerText = "۱,۲۵۰";
    document.getElementById("reportEvents").innerText = eventsList.length;

    renderRequestsTable();
    renderEventsTable();
    renderAllEvents();
    renderStudentsList();
    renderProfessorsList();
    renderMembersList();
    renderResources();
    renderTickets();
}

function renderRequestsTable() {
    let html = "";
    pendingRequestsList.forEach(req => {
        html += `<tr>
                    <td>${req.name}</td>
                    <td>${req.studentId}</td>
                    <td>${req.committee}</td>
                    <td><span class="status-pending">در انتظار</span></td>
                    <td><button class="approve" onclick="approveRequest(${req.id})">✓ تأیید</button><button class="reject" onclick="rejectRequest(${req.id})">✗ رد</button></td>
                </tr>`;
    });
    if (pendingRequestsList.length === 0) html = "<tr><td colspan='5' style='text-align:center'>هیچ درخواستی وجود ندارد</td></tr>";
    document.getElementById("requestsTableBody").innerHTML = html;
}

function renderEventsTable() {
    let html = "";
    eventsList.filter(e => e.status === "فعال").forEach(event => {
        html += `<tr>
                    <td>${event.title}</td>
                    <td>${event.date}</td>
                    <td>${event.registered}/${event.capacity}</td>
                    <td>${event.committee}</td>
                    <td><button class="edit" onclick="editEvent(${event.id})">ویرایش</button><button class="view" onclick="viewEvent(${event.id})">مشاهده شرکت‌کنندگان</button></td>
                </tr>`;
    });
    document.getElementById("eventsTableBody").innerHTML = html;
}

function renderAllEvents() {
    let html = "";
    eventsList.forEach(event => {
        html += `<tr>
                    <td>${event.title}</td>
                    <td>${event.date}</td>
                    <td>${event.type}</td>
                    <td><span class="${event.status === 'فعال' ? 'status-approved' : 'status-pending'}">${event.status}</span></td>
                    <td>${event.registered}/${event.capacity}</td>
                    <td><button class="edit" onclick="editEvent(${event.id})">✏️</button><button class="reject" onclick="deleteEvent(${event.id})">🗑️</button></td>
                </tr>`;
    });
    document.getElementById("allEventsBody").innerHTML = html;
}

function renderStudentsList() {
    let html = "";
    students.forEach(s => {
        html += `<tr><td>${s.name}</td><td>${s.studentId}</td><td>${s.email}</td><td>${s.status}</td>
                <td><button class="edit" onclick="editUser('student',${s.id})">ویرایش</button><button class="${s.status === 'فعال' ? 'reject' : 'approve'}" onclick="toggleUserStatus('student',${s.id})">${s.status === 'فعال' ? 'غیرفعال' : 'فعال'}</button></td></tr>`;
    });
    document.getElementById("studentsList").innerHTML = html;
}

function renderProfessorsList() {
    let html = "";
    professors.forEach(p => {
        html += `<tr><td>${p.name}</td><td>${p.position}</td><td>${p.email}</td><td>${p.events}</td>
                <td><button class="edit" onclick="editUser('professor',${p.id})">ویرایش</button></td></tr>`;
    });
    document.getElementById("professorsList").innerHTML = html;
}

function renderMembersList() {
    let html = "";
    members.forEach(m => {
        html += `<tr><td>${m.name}</td><td>${m.role}</td><td>${m.committee}</td><td>${m.activity}</td>
                <td><button class="edit" onclick="promoteMember(${m.id})">ارتقای نقش</button></td></tr>`;
    });
    document.getElementById("membersList").innerHTML = html;
}

function renderResources() {
    let html = "";
    resourcesList.forEach(r => {
        html += `<tr><td>${r.title}</td><td>${r.category}</td><td>${r.access}</td><td>${r.downloads}</td>
                <td><button class="edit" onclick="editResource(${r.id})">✏️</button><button class="reject" onclick="deleteResource(${r.id})">🗑️</button></td></tr>`;
    });
    document.getElementById("resourcesList").innerHTML = html;
}

function renderTickets() {
    let html = "";
    ticketsList.forEach(t => {
        html += `<tr><td>${t.id}</td><td>${t.sender}</td><td>${t.subject}</td>
                <td><span class="${t.status === 'جدید' ? 'status-pending' : 'status-approved'}">${t.status}</span></td>
                <td>${t.date}</td>
                <td><button class="view" onclick="viewTicket('${t.id}')">مشاهده</button></td></tr>`;
    });
    document.getElementById("ticketsList").innerHTML = html;
}

// ==================== توابع عملیاتی ====================
function approveRequest(id) {
    pendingRequestsList = pendingRequestsList.filter(r => r.id !== id);
    updateStats();
    alert("درخواست عضویت تأیید شد");
}

function rejectRequest(id) {
    pendingRequestsList = pendingRequestsList.filter(r => r.id !== id);
    updateStats();
    alert("درخواست عضویت رد شد");
}

function createEvent() {
    const title = document.getElementById("eventTitle").value;
    const desc = document.getElementById("eventDesc").value;
    const date = document.getElementById("eventDate").value;
    const capacity = document.getElementById("eventCapacity").value;
    const type = document.getElementById("eventType").value;

    if (!title || !date) { alert("لطفاً عنوان و تاریخ را وارد کنید"); return; }

    eventsList.push({
        id: eventsList.length + 1,
        title: title,
        date: date,
        type: type,
        status: "فعال",
        capacity: parseInt(capacity) || 30,
        registered: 0,
        committee: "آموزش"
    });
    closeEventModal();
    updateStats();
    alert(`رویداد "${title}" با موفقیت ایجاد شد`);
}

function editEvent(id) {
    let event = eventsList.find(e => e.id === id);
    if (event) {
        let newTitle = prompt("عنوان جدید:", event.title);
        if (newTitle) event.title = newTitle;
        updateStats();
    }
}

function deleteEvent(id) {
    if (confirm("آیا از حذف این رویداد اطمینان دارید؟")) {
        eventsList = eventsList.filter(e => e.id !== id);
        updateStats();
    }
}

function sendNotification() {
    const target = document.getElementById("notifyTarget").value;
    const title = document.getElementById("notifyTitle").value;
    const message = document.getElementById("notifyMessage").value;
    if (!title || !message) { alert("لطفاً عنوان و متن اعلان را وارد کنید"); return; }
    alert(`اعلان "${title}" برای ${target === 'all' ? 'همه کاربران' : target} ارسال شد`);
    closeNotificationModal();
}

function exportReport(type) {
    alert(`گزارش با فرمت ${type.toUpperCase()} در حال دانلود...`);
}

function saveSettings() {
    const siteName = document.getElementById("siteName").value;
    const primaryColor = document.getElementById("primaryColor").value;
    document.querySelector(".sidebar").style.backgroundColor = primaryColor;
    alert("تنظیمات ذخیره شد");
}

function promoteMember(id) {
    alert("نقش عضو با موفقیت ارتقا یافت");
}

// ==================== توابع تب و نویگیشن ====================
function showUserTab(tab) {
    document.querySelectorAll('.user-tab').forEach(t => t.style.display = 'none');
    document.getElementById(`${tab}Tab`).style.display = 'block';
    document.querySelectorAll('.tabs .tab-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
}

function filterResources() {
    // فیلتر منابع
}

// ==================== مودال‌ها ====================
function openEventModal() { document.getElementById("eventModal").style.display = "flex"; }
function closeEventModal() { document.getElementById("eventModal").style.display = "none"; }
function openNotificationModal() { document.getElementById("notificationModal").style.display = "flex"; }
function closeNotificationModal() { document.getElementById("notificationModal").style.display = "none"; }

function showUserManagement() { document.querySelector('[data-tab="users"]').click(); }
function showPendingRequests() { document.querySelector('[data-tab="dashboard"]').click(); }
function showAllRequests() { document.querySelector('[data-tab="users"]').click(); }
function showAddUserModal() { alert("فرم افزودن کاربر جدید باز می‌شود"); }
function openResourceModal() { alert("فرم آپلود منبع جدید باز می‌شود"); }
function editResource(id) { alert("ویرایش منبع"); }
function deleteResource(id) { if (confirm("حذف شود؟")) { resourcesList = resourcesList.filter(r => r.id !== id); renderResources(); } }
function viewTicket(id) { alert(`مشاهده تیکت ${id}`); }
function editUser(type, id) { alert(`ویرایش ${type} با شناسه ${id}`); }
function toggleUserStatus(type, id) { alert(`وضعیت کاربر تغییر کرد`); updateStats(); }
function viewEvent(id) { alert(`مشاهده شرکت‌کنندگان رویداد`); }
function logout() { localStorage.removeItem("currentUser"); window.location.href = "../login.html"; }

// ==================== راه‌اندازی اولیه ====================
document.querySelectorAll('.menu li').forEach(item => {
    item.addEventListener('click', function () {
        document.querySelectorAll('.menu li').forEach(li => li.classList.remove('active'));
        this.classList.add('active');
        const tabId = this.getAttribute('data-tab');
        document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
        document.getElementById(tabId).classList.add('active');
        document.getElementById("pageTitle").innerText = this.innerText.trim();
    });
});

updateStats();

// جستجوی دانشجو
document.getElementById("searchStudent")?.addEventListener("input", function (e) {
    let search = e.target.value;
    let filtered = students.filter(s => s.name.includes(search) || s.studentId.includes(search));
    let html = "";
    filtered.forEach(s => {
        html += `<tr><td>${s.name}</td><td>${s.studentId}</td><td>${s.email}</td><td>${s.status}</td>
                <td><button class="edit" onclick="editUser('student',${s.id})">ویرایش</button><button class="${s.status === 'فعال' ? 'reject' : 'approve'}" onclick="toggleUserStatus('student',${s.id})">${s.status === 'فعال' ? 'غیرفعال' : 'فعال'}</button></td></tr>`;
    });
    document.getElementById("studentsList").innerHTML = html;
});
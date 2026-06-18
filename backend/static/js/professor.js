// ========== داده‌های شبیه‌سازی شده ==========
let invitations = [
    { id: 1, title: "همایش مکانیک سیالات", date: "۱۴۰۴/۰۲/۱۰", role: "سخنران کلیدی", status: "pending" },
    { id: 2, title: "کارگاه تخصصی سالیدورک", date: "۱۴۰۴/۰۲/۱۵", role: "مدرس", status: "pending" }
];

let myEvents = [
    { id: 1, title: "همایش مکانیک سیالات", date: "۱۴۰۴/۰۲/۱۰", time: "۱۰:۰۰", role: "سخنران" },
    { id: 2, title: "وبینار سیستم‌های تعلیق", date: "۱۴۰۴/۰۱/۲۰", time: "۱۵:۰۰", role: "مدرس" }
];

let articles = [
    { id: 1, title: "بهینه‌سازی سیستم تعلیق فعال", author: "دکتر کریمی", date: "۱۴۰۳/۱۲/۱۰", status: "پذیرفته شده" }
];

let messages = [
    { id: 1, from: "دبیر انجمن", subject: "دعوت به همایش", date: "۱۴۰۴/۰۱/۰۵", status: "خوانده نشده" },
    { id: 2, from: "دانشجو علی رضایی", subject: "سوال علمی", date: "۱۴۰۴/۰۱/۰۳", status: "خوانده شده" }
];

// ========== توابع رندر ==========
function updateStats() {
    document.getElementById("upcomingEvents").innerText = myEvents.length;
    document.getElementById("invitations").innerText = invitations.filter(i => i.status === "pending").length;
    document.getElementById("newMessages").innerText = messages.filter(m => m.status === "خوانده نشده").length;
    document.getElementById("myArticles").innerText = articles.length;
}

function renderInvitations() {
    let html = "";
    invitations.forEach(inv => {
        html += `<tr>
                    <td>${inv.title}</td>
                    <td>${inv.date}</td>
                    <td>${inv.role}</td>
                    <td><span class="${inv.status === 'pending' ? 'status-pending' : 'status-accepted'}">${inv.status === 'pending' ? 'در انتظار پاسخ' : 'پذیرفته شده'}</span></td>
                    <td>${inv.status === 'pending' ? `<button class="accept" onclick="acceptInvite(${inv.id})">✓ پذیرش</button><button class="decline" onclick="declineInvite(${inv.id})">✗ رد</button>` : '-'}</td>
                </tr>`;
    });
    if (invitations.length === 0) html = "<tr><td colspan='5' style='text-align:center'>هیچ دعوتنامه‌ای وجود ندارد</td></tr>";
    document.getElementById("invitationsBody").innerHTML = html;
}

function renderMyEvents() {
    let html = "";
    myEvents.forEach(ev => {
        html += `<tr><td>${ev.title}</td><td>${ev.date}</td><td>${ev.time}</td><td>${ev.role}</td></tr>`;
    });
    document.getElementById("myEventsBody").innerHTML = html;
}

function renderArticles() {
    let html = "";
    articles.forEach(art => {
        html += `<tr><td>${art.title}</td><td>${art.author}</td><td>${art.date}</td><td><span class="status-accepted">${art.status}</span></td>
                <td><button class="edit" onclick="editArticle(${art.id})">✏️</button></td></tr>`;
    });
    document.getElementById("articlesBody").innerHTML = html;
}

function renderMessages() {
    let html = "";
    messages.forEach(msg => {
        html += `<tr>
                    <td>${msg.from}</td>
                    <td>${msg.subject}</td>
                    <td>${msg.date}</td>
                    <td><span class="${msg.status === 'خوانده نشده' ? 'status-pending' : 'status-accepted'}">${msg.status}</span></td>
                    <td><button class="accept" onclick="viewMessage(${msg.id})">مشاهده</button></td>
                </tr>`;
    });
    document.getElementById("messagesBody").innerHTML = html;
}

// ========== توابع عملیاتی ==========
function acceptInvite(id) {
    let invite = invitations.find(i => i.id === id);
    if (invite) {
        invite.status = "accepted";
        myEvents.push({
            id: myEvents.length + 1,
            title: invite.title,
            date: invite.date,
            time: "TBD",
            role: invite.role
        });
        updateStats();
        renderInvitations();
        renderMyEvents();
        alert("دعوتنامه پذیرفته شد");
    }
}

function declineInvite(id) {
    invitations = invitations.filter(i => i.id !== id);
    updateStats();
    renderInvitations();
    alert("دعوتنامه رد شد");
}

function submitProposal() {
    let title = document.getElementById("proposeTitle").value;
    if (!title) { alert("لطفاً عنوان رویداد را وارد کنید"); return; }
    alert(`پیشنهاد رویداد "${title}" با موفقیت به دبیر انجمن ارسال شد`);
    closeProposeModal();
}

function submitArticle() {
    let title = document.getElementById("articleTitle").value;
    if (!title) { alert("لطفاً عنوان مقاله را وارد کنید"); return; }
    articles.push({
        id: articles.length + 1,
        title: title,
        author: "دکتر کریمی",
        date: new Date().toLocaleDateString('fa-IR'),
        status: "در انتظار بررسی"
    });
    updateStats();
    renderArticles();
    closeArticleModal();
    alert(`مقاله "${title}" با موفقیت ارسال شد`);
}

function sendMessage() {
    let target = document.getElementById("messageTarget").value;
    let subject = document.getElementById("messageSubject").value;
    let text = document.getElementById("messageText").value;
    if (!subject || !text) { alert("لطفاً موضوع و متن پیام را وارد کنید"); return; }
    alert(`پیام "${subject}" به ${target === 'admin' ? 'دبیر انجمن' : 'دانشجویان'} ارسال شد`);
    document.getElementById("messageSubject").value = "";
    document.getElementById("messageText").value = "";
}

function changePassword() {
    let newPass = document.getElementById("newPassword").value;
    let confirmPass = document.getElementById("confirmNewPassword").value;
    if (!newPass) { alert("لطفاً رمز عبور جدید را وارد کنید"); return; }
    if (newPass !== confirmPass) { alert("رمز عبور و تکرار آن مطابقت ندارند"); return; }
    alert("رمز عبور با موفقیت تغییر کرد");
}

function saveExpertise() {
    alert("اطلاعات تخصصی ذخیره شد");
}

function changeProfilePic() { alert("تغییر عکس پروفایل"); }
function editArticle(id) { alert("ویرایش مقاله"); }
function viewMessage(id) { alert("مشاهده پیام"); }

// ========== مودال‌ها ==========
function openProposeEventModal() { document.getElementById("proposeEventModal").style.display = "flex"; }
function closeProposeModal() { document.getElementById("proposeEventModal").style.display = "none"; }
function openAddArticleModal() { document.getElementById("addArticleModal").style.display = "flex"; }
function closeArticleModal() { document.getElementById("addArticleModal").style.display = "none"; }

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
renderInvitations();
renderMyEvents();
renderArticles();
renderMessages();


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
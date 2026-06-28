// let managedEvents = [{ id: 1, title: "وبینار تخصصی", date: "۱۴۰۴/۰۱/۲۰", status: "فعال", registered: 25 }];
// let memberRequests = [{ id: 1, name: "علی محمدی", studentId: "۴۰۱۱۲۳۴۵", committee: "آموزش" }];
// let membersList = [{ id: 1, name: "زهرا احمدی", role: "عضو عادی", committee: "پژوهشی" }];
// let internalResources = [{ id: 1, title: "گزارش جلسه کمیته آموزش", category: "گزارشات" }];
// let galleryImages = [];

// function updateStats() { document.getElementById("myEvents").innerText = managedEvents.length; document.getElementById("pendingRequests").innerText = memberRequests.length; }
// function renderManagedEvents() { let html = ""; managedEvents.forEach(e => { html += `<tr><td>${e.title}</td><td>${e.date}</td><td>${e.registered}</td><td><button onclick="viewEvent(${e.id})">مشاهده</button><button onclick="editEvent(${e.id})">ویرایش</button></td></tr>`; }); document.getElementById("myManagedEventsBody").innerHTML = html; }
// function renderAllManagedEvents() { let html = ""; managedEvents.forEach(e => { html += `<tr><td>${e.title}</td><td>${e.date}</td><td>${e.status}</td><td><button onclick="editEvent(${e.id})">✏️</button><button onclick="deleteEvent(${e.id})">🗑️</button></td></tr>`; }); document.getElementById("allManagedEventsBody").innerHTML = html; }
// function renderMemberRequests() { let html = ""; memberRequests.forEach(r => { html += `<tr><td>${r.name}</td><td>${r.studentId}</td><td>${r.committee}</td><td><button class="approve" onclick="approveRequest(${r.id})">✓</button><button class="reject" onclick="rejectRequest(${r.id})">✗</button></td></tr>`; }); document.getElementById("memberRequestsBody").innerHTML = html; }
// function renderMembersList() { let html = ""; membersList.forEach(m => { html += `<tr><td>${m.name}</td><td>${m.role}</td><td>${m.committee}</td><td><button onclick="promoteMember(${m.id})">ارتقا</button></td></tr>`; }); document.getElementById("membersListBody").innerHTML = html; }
// function renderInternalResources() { let html = ""; internalResources.forEach(r => { html += `<tr><td>${r.title}</td><td>${r.category}</td><td><button>دانلود</button></td></tr>`; }); document.getElementById("internalResourcesBody").innerHTML = html; }
// function renderGallery() { let html = ""; galleryImages.forEach(img => { html += `<div><img src="${img}" width="100%"><button onclick="deleteImage()">حذف</button></div>`; }); document.getElementById("galleryGrid").innerHTML = html || "هیچ تصویری وجود ندارد"; }

// function createEvent() { let title = document.getElementById("newEventTitle").value; if (!title) return; managedEvents.push({ id: managedEvents.length + 1, title: title, date: document.getElementById("newEventDate").value, status: "فعال", registered: 0 }); updateStats(); renderManagedEvents(); renderAllManagedEvents(); closeCreateEventModal(); alert("رویداد ایجاد شد"); }
// function editEvent(id) { alert("ویرایش رویداد"); }
// function deleteEvent(id) { if (confirm("حذف شود؟")) { managedEvents = managedEvents.filter(e => e.id !== id); updateStats(); renderManagedEvents(); renderAllManagedEvents(); } }
// function viewEvent(id) { alert("مشاهده شرکت‌کنندگان"); }
// function approveRequest(id) { memberRequests = memberRequests.filter(r => r.id !== id); renderMemberRequests(); updateStats(); }
// function rejectRequest(id) { memberRequests = memberRequests.filter(r => r.id !== id); renderMemberRequests(); updateStats(); }
// function promoteMember(id) { alert("نقش عضو ارتقا یافت"); }
// function uploadImage() { alert("تصویر بارگذاری شد"); galleryImages.push("https://via.placeholder.com/150"); renderGallery(); closeUploadImageModal(); }
// function changePassword() { alert("رمز عبور تغییر کرد"); }
// function logout() { localStorage.removeItem("currentUser"); window.location.href = "../login.html"; }

// function openCreateEventModal() { document.getElementById("createEventModal").style.display = "flex"; }
// function closeCreateEventModal() { document.getElementById("createEventModal").style.display = "none"; }
// function openUploadImageModal() { document.getElementById("uploadImageModal").style.display = "flex"; }
// function closeUploadImageModal() { document.getElementById("uploadImageModal").style.display = "none"; }

// document.querySelectorAll('.menu li').forEach(item => { item.addEventListener('click', function () { document.querySelectorAll('.menu li').forEach(li => li.classList.remove('active')); this.classList.add('active'); let tabId = this.getAttribute('data-tab'); document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active')); document.getElementById(tabId).classList.add('active'); document.getElementById("pageTitle").innerText = this.innerText.trim(); }); });
// updateStats(); renderManagedEvents(); renderAllManagedEvents(); renderMemberRequests(); renderMembersList(); renderInternalResources(); renderGallery();


// document.addEventListener('DOMContentLoaded', function () {
//     document.getElementById('toggleSidebar')?.addEventListener('click', () => {
//         if (window.innerWidth <= 900) {
//             document.body.classList.toggle('sidebar-open');
//         } else {
//             document.body.classList.toggle('sidebar-collapsed');
//         }
//     });

//     document.querySelectorAll('.modal').forEach(modal => {
//         modal.addEventListener('click', event => {
//             if (event.target === modal) {
//                 modal.style.display = 'none';
//             }
//         });
//     });

//     // بارگذاری اولیه همه تب‌ها
//     // loadDashboard();
//     // loadInvitations();
//     // loadAllEvents();
//     // loadArticles();
//     // loadProfile();
// });

// ==================== توابع کمکی ====================
function toPersianDigits(value) {
    return String(value ?? '').replace(/\d/g, digit => '۰۱۲۳۴۵۶۷۸۹'[digit]);
}

function escapeHtml(value) {
    return String(value ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

function setLoadingContainer(containerId, message) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `<div class="empty-state">${message || 'در حال بارگذاری...'}</div>`;
    }
}

function setEmptyContainer(containerId, message) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `<div class="empty-state">${message}</div>`;
    }
}

function setLoading(elementId, colspan) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `<tr><td colspan="${colspan}" class="empty-state">در حال بارگذاری...</td></tr>`;
    }
}

function setEmpty(elementId, colspan, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `<tr><td colspan="${colspan}" class="empty-state">${message}</td></tr>`;
    }
}

function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (const cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') return value;
    }
    return '';
}

let currentProfileData = {};

// ==================== مدیریت تب‌ها ====================
// در member.html لینک‌ها با href="#tabId" هستند (بدون onclick)
// پس باید با گوش دادن به کلیک روی <a> تب‌ها را تغییر دهیم

function switchTab(tabId) {
    // غیرفعال کردن همه تب‌ها و آیتم‌های منو
    document.querySelectorAll('.menu li').forEach(item => item.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));

    // فعال کردن تب و آیتم منوی انتخاب شده
    const menuItem = document.querySelector(`.menu li[data-tab="${tabId}"]`);
    if (menuItem) menuItem.classList.add('active');

    const tabContent = document.getElementById(tabId);
    if (tabContent) tabContent.classList.add('active');

    // به‌روزرسانی عنوان صفحه
    const titles = {
        dashboard:           'داشبورد عضو انجمن',
        community:           'مدیریت انجمن',
        events:              'مدیریت رویدادها',
        gallery:             'گالری و رسانه',
        resources:           'منابع و دانلودها',
        'suggested-events':  'رویدادهای پیشنهادی',
        'suggested-articles':'مقالات پیشنهادی',
        'invite-professors': 'دعوت از اساتید',
        profile:             'پروفایل من'
    };
    const pageTitle = document.getElementById('pageTitle');
    if (pageTitle) pageTitle.innerText = titles[tabId] || 'پنل عضو انجمن';

    // بارگذاری داده مربوط به هر تب
    const loaders = {
        dashboard:           loadDashboard,
        community:           function () { loadMemberRequests(); loadMembersList(); },
        events:              loadManagedEvents,
        gallery:             loadGallery,
        resources:           loadResources,
        'suggested-events':  loadSuggestedEvents,
        'suggested-articles':loadSuggestedArticles,
        'invite-professors': loadInvitations,
        profile:             loadProfile
    };
    if (loaders[tabId]) loaders[tabId]();

    // بستن سایدبار در موبایل
    if (window.innerWidth <= 900) {
        document.body.classList.remove('sidebar-open');
    }
}

// ==================== داشبورد ====================
async function loadDashboard() {
    try {
        const res  = await fetch('/panel/member/api/dashboard/');
        const data = await res.json();
        if (data.error) throw new Error(data.error);

        // آمار - چون در HTML مقادیر با Django template مستقیم رندر شده‌اند،
        // این بخش فقط در صورتی لازم است که API جداگانه داشته باشید
        renderAnnouncements(data.announcements || []);

    } catch (error) {
        console.error('Error loading dashboard:', error);
        renderAnnouncements([]);
    }
}

function renderAnnouncements(announcements) {
    const list = document.getElementById('announcementsList');
    if (!list) return;

    if (!announcements.length) {
        list.innerHTML = '<li>هیچ اطلاعیه‌ای وجود ندارد</li>';
        return;
    }

    list.innerHTML = announcements.map(item => `
        <li>
            <span>🔔 ${escapeHtml(item.title)}</span>
            <small>${escapeHtml(item.created_at || '')}</small>
        </li>
    `).join('');
}

// ==================== مدیریت انجمن ====================
function loadMemberRequests() {
    setLoading('memberRequestsBody', 4);

    fetch('/panel/member/api/member-requests/')
        .then(res => res.json())
        .then(data => {
            if (data.error) throw new Error(data.error);
            const tbody = document.getElementById('memberRequestsBody');
            if (!tbody) return;

            if (!data.requests || !data.requests.length) {
                setEmpty('memberRequestsBody', 4, 'هیچ درخواستی وجود ندارد');
                return;
            }

            tbody.innerHTML = data.requests.map(req => `
                <tr>
                    <td>${escapeHtml(req.full_name || req.username)}</td>
                    <td>${escapeHtml(req.student_id || '-')}</td>
                    <td>${escapeHtml(req.committee || 'نامشخص')}</td>
                    <td>
                        <button class="btn-approve" onclick="approveRequest(${req.id}, '${escapeHtml(req.full_name || req.username)}')">✅ تایید</button>
                        <button class="btn-reject"  onclick="rejectRequest(${req.id},  '${escapeHtml(req.full_name || req.username)}')">❌ رد</button>
                    </td>
                </tr>
            `).join('');
        })
        .catch(error => {
            console.error('Error loading member requests:', error);
            setEmpty('memberRequestsBody', 4, 'خطا در دریافت درخواست‌ها');
        });
}

function loadMembersList() {
    setLoading('membersListBody', 4);

    fetch('/panel/member/api/members/')
        .then(res => res.json())
        .then(data => {
            if (data.error) throw new Error(data.error);
            const tbody = document.getElementById('membersListBody');
            if (!tbody) return;

            if (!data.members || !data.members.length) {
                setEmpty('membersListBody', 4, 'هیچ عضوی یافت نشد');
                return;
            }

            tbody.innerHTML = data.members.map(member => `
                <tr>
                    <td>${escapeHtml(member.full_name || member.username)}</td>
                    <td>${escapeHtml(member.role_display || member.role)}</td>
                    <td>${escapeHtml(member.committee || 'نامشخص')}</td>
                    <td><a href="#" class="btn-edit" onclick="promoteMember(${member.id}, '${escapeHtml(member.full_name || member.username)}'); return false;">✏️ ویرایش</a></td>
                </tr>
            `).join('');
        })
        .catch(error => {
            console.error('Error loading members list:', error);
            setEmpty('membersListBody', 4, 'خطا در دریافت لیست اعضا');
        });
}

function approveRequest(requestId, name) {
    if (!confirm(`آیا از تایید درخواست عضویت «${name}» مطمئن هستید؟`)) return;

    fetch(`/panel/member/api/member-requests/${requestId}/approve/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCSRFToken(), 'Content-Type': 'application/json' }
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) { alert(data.message); loadMemberRequests(); loadMembersList(); }
            else alert(`خطا: ${data.error}`);
        })
        .catch(() => alert('خطا در ارتباط با سرور'));
}

function rejectRequest(requestId, name) {
    if (!confirm(`آیا از رد درخواست عضویت «${name}» مطمئن هستید؟`)) return;

    fetch(`/panel/member/api/member-requests/${requestId}/reject/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCSRFToken(), 'Content-Type': 'application/json' }
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) { alert(data.message); loadMemberRequests(); }
            else alert(`خطا: ${data.error}`);
        })
        .catch(() => alert('خطا در ارتباط با سرور'));
}

function promoteMember(memberId, name) {
    if (!confirm(`آیا از ارتقای نقش «${name}» مطمئن هستید؟`)) return;

    fetch(`/panel/member/api/members/${memberId}/promote/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCSRFToken(), 'Content-Type': 'application/json' }
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) { alert(data.message); loadMembersList(); }
            else alert(`خطا: ${data.error}`);
        })
        .catch(() => alert('خطا در ارتباط با سرور'));
}

// ==================== مدیریت رویدادها ====================
// در member.html فرم ایجاد رویداد با method POST مستقیم است (Django form)
// پس تابع loadManagedEvents فقط جدول رویدادها را از API می‌خواند (در صورت وجود)
// اگر API ندارید این تابع را حذف یا خالی بگذارید

function loadManagedEvents() {
    // جدول رویدادها در member.html با Django template رندر می‌شود
    // اگر API جداگانه دارید، کد زیر را فعال کنید:
    /*
    setLoading('allManagedEventsBody', 4);
    fetch('/panel/member/api/events/')
        .then(res => res.json())
        .then(data => {
            if (data.error) throw new Error(data.error);
            const tbody = document.getElementById('allManagedEventsBody');
            if (!tbody) return;
            if (!data.events || !data.events.length) {
                setEmpty('allManagedEventsBody', 4, 'هیچ رویدادی وجود ندارد');
                return;
            }
            tbody.innerHTML = data.events.map(event => `
                <tr>
                    <td>${escapeHtml(event.title)}</td>
                    <td>${escapeHtml(event.date || '')}</td>
                    <td>${escapeHtml(event.get_status_display || event.status || '')}</td>
                    <td>
                        <a href="/events/${event.id}/" class="btn-view">👁️ مشاهده</a>
                        <button class="btn-delete" onclick="deleteEvent(${event.id}, '${escapeHtml(event.title)}')">🗑️ حذف</button>
                    </td>
                </tr>
            `).join('');
        })
        .catch(error => {
            console.error('Error loading events:', error);
            setEmpty('allManagedEventsBody', 4, 'خطا در دریافت رویدادها');
        });
    */
}

function deleteEvent(eventId, title) {
    if (!confirm(`آیا از حذف رویداد «${title}» مطمئن هستید؟`)) return;

    fetch(`/panel/member/api/events/${eventId}/delete/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCSRFToken(), 'Content-Type': 'application/json' }
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) { alert(data.message); location.reload(); }
            else alert(`خطا: ${data.error}`);
        })
        .catch(() => alert('خطا در ارتباط با سرور'));
}

// ==================== گالری ====================
// گالری در member.html با Django template رندر می‌شود
// این تابع اگر API جداگانه دارید می‌توانید فعال کنید

function loadGallery() {
    // گالری با Django template رندر شده، نیازی به fetch نیست
    // اگر API جداگانه دارید کد زیر را فعال کنید:
    /*
    fetch('/panel/member/api/gallery/')
        .then(res => res.json())
        .then(data => {
            if (data.error) throw new Error(data.error);
            renderGallery(data.images || []);
        })
        .catch(error => {
            console.error('Error loading gallery:', error);
            setEmptyContainer('galleryGrid', 'خطا در دریافت تصاویر');
        });
    */
}

function deleteGalleryImage(imageId, caption) {
    if (!confirm(`آیا از حذف «${caption}» مطمئن هستید؟`)) return;

    fetch(`/panel/member/api/gallery/${imageId}/delete/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCSRFToken(), 'Content-Type': 'application/json' }
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) { alert(data.message); location.reload(); }
            else alert(`خطا: ${data.error}`);
        })
        .catch(() => alert('خطا در ارتباط با سرور'));
}

// ==================== منابع ====================
// منابع در member.html با Django template رندر می‌شوند
function loadResources() {
    // منابع با Django template رندر شده، نیازی به fetch نیست
    // اگر API جداگانه دارید فعال کنید
}

function filterResources() {
    loadResources();
}

// ==================== رویدادهای پیشنهادی اساتید ====================
// این بخش در member.html با داده فیک رندر شده
// وقتی به backend متصل شد کد زیر را فعال کنید

function loadSuggestedEvents() {
    // داده‌های فیک در HTML هستند – وقتی backend آماده شد:
    /*
    setLoading('suggestedEventsBody', 5);
    fetch('/panel/member/api/suggested-events/')
        .then(res => res.json())
        .then(data => {
            if (data.error) throw new Error(data.error);
            const tbody = document.getElementById('suggestedEventsBody');
            if (!tbody) return;
            if (!data.events || !data.events.length) {
                setEmpty('suggestedEventsBody', 5, 'هیچ رویداد پیشنهادی وجود ندارد');
                return;
            }
            tbody.innerHTML = data.events.map(event => `
                <tr>
                    <td>${escapeHtml(event.professor_name)}</td>
                    <td><strong>${escapeHtml(event.title)}</strong></td>
                    <td>${escapeHtml(event.description || '-')}</td>
                    <td>${escapeHtml(event.date || '-')}</td>
                    <td>
                        <button class="btn-approve" onclick="approveSuggestedEvent(${event.id}, '${escapeHtml(event.title)}')">✅ تایید</button>
                        <button class="btn-reject"  onclick="rejectSuggestedEvent(${event.id},  '${escapeHtml(event.title)}')">❌ رد</button>
                    </td>
                </tr>
            `).join('');
        })
        .catch(() => setEmpty('suggestedEventsBody', 5, 'خطا در دریافت رویدادهای پیشنهادی'));
    */
}

function approveSuggestedEvent(eventId, title) {
    if (!confirm(`آیا از تایید رویداد «${title}» مطمئن هستید؟`)) return;
    fetch(`/panel/member/api/suggested-events/${eventId}/approve/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCSRFToken(), 'Content-Type': 'application/json' }
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) { alert(data.message); loadSuggestedEvents(); }
            else alert(`خطا: ${data.error}`);
        })
        .catch(() => alert('خطا در ارتباط با سرور'));
}

function rejectSuggestedEvent(eventId, title) {
    if (!confirm(`آیا از رد رویداد «${title}» مطمئن هستید؟`)) return;
    fetch(`/panel/member/api/suggested-events/${eventId}/reject/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCSRFToken(), 'Content-Type': 'application/json' }
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) { alert(data.message); loadSuggestedEvents(); }
            else alert(`خطا: ${data.error}`);
        })
        .catch(() => alert('خطا در ارتباط با سرور'));
}

// ==================== مقالات پیشنهادی اساتید ====================
function loadSuggestedArticles() {
    // داده‌های فیک در HTML هستند – وقتی backend آماده شد فعال کنید
}

function approveSuggestedArticle(articleId, title) {
    if (!confirm(`آیا از تایید مقاله «${title}» مطمئن هستید؟`)) return;
    fetch(`/panel/member/api/suggested-articles/${articleId}/approve/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCSRFToken(), 'Content-Type': 'application/json' }
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) { alert(data.message); loadSuggestedArticles(); }
            else alert(`خطا: ${data.error}`);
        })
        .catch(() => alert('خطا در ارتباط با سرور'));
}

function rejectSuggestedArticle(articleId, title) {
    if (!confirm(`آیا از رد مقاله «${title}» مطمئن هستید؟`)) return;
    fetch(`/panel/member/api/suggested-articles/${articleId}/reject/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCSRFToken(), 'Content-Type': 'application/json' }
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) { alert(data.message); loadSuggestedArticles(); }
            else alert(`خطا: ${data.error}`);
        })
        .catch(() => alert('خطا در ارتباط با سرور'));
}

// ==================== دعوت از اساتید ====================
// در member.html فرم دعوت با method POST مستقیم است و جدول با داده فیک
function loadInvitations() {
    // داده‌های فیک در HTML هستند – وقتی backend آماده شد فعال کنید
}

// ==================== پروفایل ====================
// پروفایل در member.html با Django template رندر شده
function loadProfile() {
    // اطلاعات پروفایل با Django template مستقیم رندر شده
    // اگر ویرایش پروفایل اضافه کردید، API را اینجا فراخوانی کنید
}

// ==================== تغییر رمز عبور ====================
function changePassword() {
    const newPassword     = document.getElementById('newPassword')?.value;
    const confirmPassword = document.getElementById('confirmNewPassword')?.value;

    if (!newPassword) {
        alert('لطفاً رمز عبور جدید را وارد کنید');
        return;
    }
    if (newPassword !== confirmPassword) {
        alert('رمز عبور و تکرار آن مطابقت ندارند');
        return;
    }
    if (newPassword.length < 8) {
        alert('رمز عبور باید حداقل ۸ کاراکتر باشد');
        return;
    }

    fetch('/panel/member/api/change-password/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCSRFToken(), 'Content-Type': 'application/json' },
        body: JSON.stringify({ new_password: newPassword, confirm_password: confirmPassword })
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                if (document.getElementById('newPassword'))        document.getElementById('newPassword').value        = '';
                if (document.getElementById('confirmNewPassword')) document.getElementById('confirmNewPassword').value = '';
            } else {
                alert(`خطا: ${data.error}`);
            }
        })
        .catch(() => alert('خطا در ارتباط با سرور'));
}

// ==================== خروج ====================
function logout() {
    if (confirm('آیا مطمئن هستید که می‌خواهید خارج شوید؟')) {
        window.location.href = '/accounts/logout/';
    }
}

// ==================== رویدادهای DOM ====================
document.addEventListener('DOMContentLoaded', function () {

    // ---- مدیریت سایدبار ----
    document.getElementById('toggleSidebar')?.addEventListener('click', () => {
        if (window.innerWidth <= 900) {
            document.body.classList.toggle('sidebar-open');
        } else {
            document.body.classList.toggle('sidebar-collapsed');
        }
    });

    // ---- اتصال کلیک منو به switchTab ----
    // در member.html لینک‌ها href="#tabId" دارند (بدون onclick)
    // پس باید اینجا event listener اضافه کنیم
    document.querySelectorAll('.menu li[data-tab]').forEach(item => {
        item.addEventListener('click', function (e) {
            e.preventDefault();
            const tabId = this.getAttribute('data-tab');
            if (tabId) switchTab(tabId);
        });
    });

    // ---- بستن مودال‌ها با کلیک روی پس‌زمینه ----
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', event => {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        });
    });

    // ---- بارگذاری اولیه تب فعال (dashboard) ----
    loadDashboard();
});
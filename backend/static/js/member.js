let managedEvents = [{ id: 1, title: "وبینار تخصصی", date: "۱۴۰۴/۰۱/۲۰", status: "فعال", registered: 25 }];
let memberRequests = [{ id: 1, name: "علی محمدی", studentId: "۴۰۱۱۲۳۴۵", committee: "آموزش" }];
let membersList = [{ id: 1, name: "زهرا احمدی", role: "عضو عادی", committee: "پژوهشی" }];
let internalResources = [{ id: 1, title: "گزارش جلسه کمیته آموزش", category: "گزارشات" }];
let galleryImages = [];

function updateStats() { document.getElementById("myEvents").innerText = managedEvents.length; document.getElementById("pendingRequests").innerText = memberRequests.length; }
function renderManagedEvents() { let html = ""; managedEvents.forEach(e => { html += `<tr><td>${e.title}</td><td>${e.date}</td><td>${e.registered}</td><td><button onclick="viewEvent(${e.id})">مشاهده</button><button onclick="editEvent(${e.id})">ویرایش</button></td></tr>`; }); document.getElementById("myManagedEventsBody").innerHTML = html; }
function renderAllManagedEvents() { let html = ""; managedEvents.forEach(e => { html += `<tr><td>${e.title}</td><td>${e.date}</td><td>${e.status}</td><td><button onclick="editEvent(${e.id})">✏️</button><button onclick="deleteEvent(${e.id})">🗑️</button></td></tr>`; }); document.getElementById("allManagedEventsBody").innerHTML = html; }
function renderMemberRequests() { let html = ""; memberRequests.forEach(r => { html += `<tr><td>${r.name}</td><td>${r.studentId}</td><td>${r.committee}</td><td><button class="approve" onclick="approveRequest(${r.id})">✓</button><button class="reject" onclick="rejectRequest(${r.id})">✗</button></td></tr>`; }); document.getElementById("memberRequestsBody").innerHTML = html; }
function renderMembersList() { let html = ""; membersList.forEach(m => { html += `<tr><td>${m.name}</td><td>${m.role}</td><td>${m.committee}</td><td><button onclick="promoteMember(${m.id})">ارتقا</button></td></tr>`; }); document.getElementById("membersListBody").innerHTML = html; }
function renderInternalResources() { let html = ""; internalResources.forEach(r => { html += `<tr><td>${r.title}</td><td>${r.category}</td><td><button>دانلود</button></td></tr>`; }); document.getElementById("internalResourcesBody").innerHTML = html; }
function renderGallery() { let html = ""; galleryImages.forEach(img => { html += `<div><img src="${img}" width="100%"><button onclick="deleteImage()">حذف</button></div>`; }); document.getElementById("galleryGrid").innerHTML = html || "هیچ تصویری وجود ندارد"; }

function createEvent() { let title = document.getElementById("newEventTitle").value; if (!title) return; managedEvents.push({ id: managedEvents.length + 1, title: title, date: document.getElementById("newEventDate").value, status: "فعال", registered: 0 }); updateStats(); renderManagedEvents(); renderAllManagedEvents(); closeCreateEventModal(); alert("رویداد ایجاد شد"); }
function editEvent(id) { alert("ویرایش رویداد"); }
function deleteEvent(id) { if (confirm("حذف شود؟")) { managedEvents = managedEvents.filter(e => e.id !== id); updateStats(); renderManagedEvents(); renderAllManagedEvents(); } }
function viewEvent(id) { alert("مشاهده شرکت‌کنندگان"); }
function approveRequest(id) { memberRequests = memberRequests.filter(r => r.id !== id); renderMemberRequests(); updateStats(); }
function rejectRequest(id) { memberRequests = memberRequests.filter(r => r.id !== id); renderMemberRequests(); updateStats(); }
function promoteMember(id) { alert("نقش عضو ارتقا یافت"); }
function uploadImage() { alert("تصویر بارگذاری شد"); galleryImages.push("https://via.placeholder.com/150"); renderGallery(); closeUploadImageModal(); }
function changePassword() { alert("رمز عبور تغییر کرد"); }
function logout() { localStorage.removeItem("currentUser"); window.location.href = "../login.html"; }

function openCreateEventModal() { document.getElementById("createEventModal").style.display = "flex"; }
function closeCreateEventModal() { document.getElementById("createEventModal").style.display = "none"; }
function openUploadImageModal() { document.getElementById("uploadImageModal").style.display = "flex"; }
function closeUploadImageModal() { document.getElementById("uploadImageModal").style.display = "none"; }

document.querySelectorAll('.menu li').forEach(item => { item.addEventListener('click', function () { document.querySelectorAll('.menu li').forEach(li => li.classList.remove('active')); this.classList.add('active'); let tabId = this.getAttribute('data-tab'); document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active')); document.getElementById(tabId).classList.add('active'); document.getElementById("pageTitle").innerText = this.innerText.trim(); }); });
updateStats(); renderManagedEvents(); renderAllManagedEvents(); renderMemberRequests(); renderMembersList(); renderInternalResources(); renderGallery();


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
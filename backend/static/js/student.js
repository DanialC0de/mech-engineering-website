// ========== تابع تغییر تب ==========
function switchTab(tabId) {
    // حذف کلاس active از همه منوها
    document.querySelectorAll('.menu li').forEach(li => li.classList.remove('active'));
    
    // اضافه کردن کلاس active به منوی انتخاب شده
    const menuItem = document.querySelector(`.menu li[data-tab="${tabId}"]`);
    if (menuItem) {
        menuItem.classList.add('active');
    }
    
    // مخفی کردن همه تب‌ها
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    
    // نمایش تب انتخاب شده
    const targetTab = document.getElementById(tabId);
    if (targetTab) {
        targetTab.classList.add('active');
    }
    
    // تغییر عنوان صفحه
    const titles = {
        'dashboard': 'داشبورد دانشجو',
        'events': 'اخبار و رویدادها',
        'registrations': 'ثبت‌نام‌های من',
        'resources': 'منابع و دانلودها',
        'tickets': 'تیکت‌ها',
        'profile': 'پروفایل من'
    };
    document.getElementById("pageTitle").innerText = titles[tabId] || 'پنل دانشجو';
    
    // بارگذاری داده‌های مربوط به هر تب
    switch(tabId) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'events':
            loadAllEvents();
            break;
        case 'registrations':
            loadDashboard();
            break;
        case 'resources':
            loadResources();
            break;
        case 'tickets':
            loadTickets();
            break;
        case 'profile':
            loadProfile();
            break;
    }
}

// ========== توابع اصلی برای ارتباط با API ==========

function loadDashboard() {
    fetch('/panel/student/api/dashboard/')
        .then(response => response.json())
        .then(data => {
            document.getElementById("myRegistrations").innerText = data.stats.myRegistrations;
            document.getElementById("newResources").innerText = data.stats.newResources;
            document.getElementById("myTickets").innerText = data.stats.myTickets;
            document.getElementById("eventCount").innerText = data.stats.myRegistrations;
            
            const announcementsList = document.querySelector('#dashboard .section-card ul');
            if (announcementsList && data.announcements) {
                if (data.announcements.length === 0) {
                    announcementsList.innerHTML = '<li>هیچ اطلاعیه‌ای وجود ندارد</li>';
                } else {
                    announcementsList.innerHTML = data.announcements.map(item => 
                        `<li>🔔 ${item.title} <small style="color:#999;">(${item.created_at})</small></li>`
                    ).join('');
                }
            }
            
            const tableBody = document.getElementById("availableEventsBody");
            if (tableBody) {
                if (data.availableEvents.length === 0) {
                    tableBody.innerHTML = '<tr><td colspan="4" style="text-align:center;">هیچ رویداد قابل ثبت‌نامی وجود ندارد</td></tr>';
                } else {
                    tableBody.innerHTML = data.availableEvents.map(event => `
                        <tr>
                            <td>${event.title}</td>
                            <td>${event.date}</td>
                            <td>${event.remaining}</td>
                            <td>
                                <button class="register-btn" onclick="registerEvent(${event.id}, '${event.title}')" style="background:#0a2a44; color:white; padding:5px 15px; border:none; border-radius:5px; cursor:pointer;">
                                    ✓ ثبت‌نام
                                </button>
                            </td>
                        </tr>
                    `).join('');
                }
            }
            
            renderMyRegistrations(data.myEvents);
        })
        .catch(error => {
            console.error('Error loading dashboard:', error);
        });
}

function loadAllEvents() {
    const status = document.getElementById('eventStatusFilter')?.value || 'all';
    
    fetch(`/panel/student/api/events/?status=${status}`)
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("allEventsBody");
            if (tableBody) {
                if (data.events.length === 0) {
                    tableBody.innerHTML = '<tr><td colspan="5" style="text-align:center;">هیچ رویدادی وجود ندارد</td></tr>';
                } else {
                    tableBody.innerHTML = data.events.map(event => `
                        <tr>
                            <td>${event.title}</td>
                            <td>${event.date} - ${event.time}</td>
                            <td>${event.status}</td>
                            <td>
                                <span class="${event.is_registered ? 'status-accepted' : event.is_full ? 'status-rejected' : 'status-pending'}">
                                    ${event.is_registered ? '✅ ثبت‌نام شده' : 
                                      event.is_full ? '❌ تکمیل شده' : 
                                      '✅ قابل ثبت‌نام'}
                                </span>
                            </td>
                            <td>
                                ${!event.is_registered && !event.is_full && event.status === 'upcoming' ? 
                                  `<button class="register-btn" onclick="registerEvent(${event.id}, '${event.title}')" style="background:#0a2a44; color:white; padding:5px 15px; border:none; border-radius:5px; cursor:pointer;">ثبت‌نام</button>` : 
                                  event.is_registered ? 
                                  `<button class="cancel-btn" onclick="cancelRegistration(${event.registration_id}, '${event.title}')" style="background:#dc3545; color:white; padding:5px 15px; border:none; border-radius:5px; cursor:pointer;">لغو</button>` :
                                  'غیرقابل ثبت‌نام'}
                            </td>
                        </tr>
                    `).join('');
                }
            }
        })
        .catch(error => {
            console.error('Error loading events:', error);
        });
}

function renderMyRegistrations(events) {
    const tableBody = document.getElementById("myRegistrationsBody");
    if (tableBody) {
        if (!events || events.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="4" style="text-align:center;">هیچ ثبت‌نامی ندارید</td></tr>';
        } else {
            tableBody.innerHTML = events.map(reg => `
                <tr>
                    <td>${reg.title}</td>
                    <td>${reg.date}</td>
                    <td><span class="status-accepted">${reg.status}</span></td>
                    <td>
                        ${reg.status !== 'cancelled' ? 
                          `<button class="cancel-btn" onclick="cancelRegistration(${reg.id}, '${reg.title}')" style="background:#dc3545; color:white; padding:5px 15px; border:none; border-radius:5px; cursor:pointer;">لغو ثبت‌نام</button>` :
                          'لغو شده'}
                    </td>
                </tr>
            `).join('');
        }
    }
}

function loadResources() {
    const category = document.getElementById('resourceFilter')?.value || 'all';
    
    fetch(`/panel/student/api/resources/?category=${category}`)
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("resourcesBody");
            if (tableBody) {
                if (data.resources.length === 0) {
                    tableBody.innerHTML = '<tr><td colspan="4" style="text-align:center;">هیچ منبعی وجود ندارد</td></tr>';
                } else {
                    tableBody.innerHTML = data.resources.map(resource => `
                        <tr>
                            <td><strong>${resource.title}</strong></td>
                            <td><span class="badge">${resource.category}</span></td>
                            <td>${resource.description}</td>
                            <td>
                                ${resource.has_file ? 
                                  `<button class="download-btn" onclick="downloadResource(${resource.id}, '${resource.title}')" style="background:#28a745; color:white; padding:5px 15px; border:none; border-radius:5px; cursor:pointer;">📥 دانلود</button>` : 
                                  'فایلی موجود نیست'}
                                <span style="font-size:12px; color:#999;">(${resource.download_count} دانلود)</span>
                            </td>
                        </tr>
                    `).join('');
                }
            }
        })
        .catch(error => {
            console.error('Error loading resources:', error);
        });
}

function loadTickets() {
    const tableBody = document.getElementById("ticketsBody");
    if (tableBody) {
        tableBody.innerHTML = '<tr><td colspan="5" style="text-align:center;">در حال توسعه...</td></tr>';
    }
}

function loadProfile() {
    fetch('/panel/student/api/profile/')
        .then(response => response.json())
        .then(data => {
            document.getElementById("profileName").innerText = `${data.first_name} ${data.last_name}`;
            document.getElementById("profileStudentId").innerText = data.student_id || 'ثبت نشده';
            document.getElementById("profileMajor").innerText = data.major || 'ثبت نشده';
            document.getElementById("profileLevel").innerText = data.level || 'ثبت نشده';
            document.getElementById("profileEmail").innerText = data.email || 'ثبت نشده';
            document.getElementById("eventCount").innerText = data.event_count || 0;
            document.getElementById("downloadCount").innerText = data.download_count || 0;
        })
        .catch(error => {
            console.error('Error loading profile:', error);
        });
}

// ========== توابع عملیاتی ==========

function registerEvent(eventId, title) {
    if (!confirm(`آیا مطمئن هستید که می‌خواهید در "${title}" ثبت‌نام کنید؟`)) {
        return;
    }
    
    fetch(`/panel/student/api/events/${eventId}/register/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            loadDashboard();
            loadAllEvents();
        } else {
            alert('خطا: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error registering:', error);
        alert('خطا در ارتباط با سرور');
    });
}

function cancelRegistration(registrationId, title) {
    if (!confirm(`آیا از لغو ثبت‌نام در "${title}" اطمینان دارید؟`)) {
        return;
    }
    
    fetch(`/panel/student/api/registrations/${registrationId}/cancel/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            loadDashboard();
            loadAllEvents();
        } else {
            alert('خطا: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error canceling:', error);
        alert('خطا در ارتباط با سرور');
    });
}

function downloadResource(resourceId, title) {
    window.open(`/panel/student/api/resources/${resourceId}/download/`, '_blank');
    setTimeout(() => {
        loadResources();
        loadProfile();
    }, 1000);
}

function changePassword() {
    let newPass = document.getElementById("newPassword").value;
    let confirmPass = document.getElementById("confirmNewPassword").value;
    
    if (!newPass) {
        alert("لطفاً رمز عبور جدید را وارد کنید");
        return;
    }
    
    if (newPass !== confirmPass) {
        alert("رمز عبور و تکرار آن مطابقت ندارند");
        return;
    }
    
    if (newPass.length < 8) {
        alert("رمز عبور باید حداقل ۸ کاراکتر باشد");
        return;
    }
    
    fetch('/panel/student/api/change-password/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            new_password: newPass,
            confirm_password: confirmPass
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            document.getElementById("newPassword").value = '';
            document.getElementById("confirmNewPassword").value = '';
        } else {
            alert('خطا: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error changing password:', error);
        alert('خطا در ارتباط با سرور');
    });
}

function submitTicket() {
    let subject = document.getElementById("ticketSubject").value;
    let message = document.getElementById("ticketMessage").value;
    
    if (!subject || !message) {
        alert("لطفاً موضوع و متن تیکت را وارد کنید");
        return;
    }
    
    alert('تیکت شما با موفقیت ارسال شد');
    closeTicketModal();
}

function filterResources() {
    loadResources();
}

function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            return value;
        }
    }
    return '';
}

function openNewTicketModal() {
    document.getElementById("newTicketModal").style.display = "flex";
}

function closeTicketModal() {
    document.getElementById("newTicketModal").style.display = "none";
    document.getElementById("ticketSubject").value = '';
    document.getElementById("ticketPriority").value = 'متوسط';
    document.getElementById("ticketMessage").value = '';
}

function logout() {
    if (confirm('آیا مطمئن هستید که می‌خواهید خارج شوید؟')) {
        window.location.href = '/accounts/logout/';
    }
}

function changeProfilePic() {
    alert('تغییر عکس پروفایل - این قابلیت به زودی اضافه می‌شود');
}

function viewTicket(id) {
    alert(`مشاهده تیکت ${id} - این قابلیت به زودی اضافه می‌شود`);
}

// ========== بارگذاری اولیه ==========
document.addEventListener('DOMContentLoaded', function() {
    loadDashboard();
    loadAllEvents();
    loadResources();
    loadTickets();
    loadProfile();
});
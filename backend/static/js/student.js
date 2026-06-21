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

function getEventTitle(eventId) {
    return document.querySelector(`[data-event-id="${eventId}"]`)?.dataset.eventTitle || 'این رویداد';
}

function getTicketTitle(ticketId) {
    return document.querySelector(`[data-ticket-id="${ticketId}"]`)?.dataset.ticketSubject || 'این تیکت';
}

let currentProfileData = {};

function switchTab(tabId) {
    document.querySelectorAll('.menu li').forEach(item => item.classList.remove('active'));
    document.querySelector(`.menu li[data-tab="${tabId}"]`)?.classList.add('active');

    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    document.getElementById(tabId)?.classList.add('active');

    const titles = {
        dashboard: 'داشبورد دانشجو',
        events: 'اخبار و رویدادها',
        registrations: 'ثبت‌نام‌های من',
        resources: 'منابع و دانلودها',
        tickets: 'تیکت‌ها',
        profile: 'پروفایل من'
    };
    document.getElementById('pageTitle').innerText = titles[tabId] || 'پنل دانشجو';

    const loaders = {
        dashboard: loadDashboard,
        events: loadAllEvents,
        registrations: loadDashboard,
        resources: loadResources,
        tickets: loadTickets,
        profile: loadProfile
    };

    loaders[tabId]?.();
    if (window.innerWidth <= 900) {
        document.body.classList.remove('sidebar-open');
    }
}

function loadDashboard() {
    fetch('/panel/student/api/dashboard/')
        .then(response => response.json())
        .then(data => {
            if (data.error) throw new Error(data.error);

            document.getElementById('myRegistrations').innerText = toPersianDigits(data.stats.myRegistrations);
            document.getElementById('newResources').innerText = toPersianDigits(data.stats.newResources);
            document.getElementById('myTickets').innerText = toPersianDigits(getTickets().length);
            document.getElementById('eventCount').innerText = toPersianDigits(data.stats.myRegistrations);

            renderAnnouncements(data.announcements || []);
            renderAvailableEvents(data.availableEvents || []);
            renderMyRegistrations(data.myEvents || []);
        })
        .catch(error => {
            console.error('Error loading dashboard:', error);
            renderAnnouncements([]);
            setEmpty('availableEventsBody', 4, 'خطا در دریافت اطلاعات داشبورد');
        });
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
            <small>${escapeHtml(item.created_at)}</small>
        </li>
    `).join('');
}

function renderAvailableEvents(events) {
    const tableBody = document.getElementById('availableEventsBody');
    if (!tableBody) return;

    if (!events.length) {
        setEmpty('availableEventsBody', 4, 'هیچ رویداد قابل ثبت‌نامی وجود ندارد');
        return;
    }

    tableBody.innerHTML = events.map(event => `
        <tr data-event-id="${event.id}" data-event-title="${escapeHtml(event.title)}">
            <td><strong>${escapeHtml(event.title)}</strong></td>
            <td>${escapeHtml(event.date)} ${event.time ? `- ${escapeHtml(event.time)}` : ''}</td>
            <td>${toPersianDigits(event.remaining)}</td>
            <td>
                <button class="register-btn" onclick="registerEvent(${event.id}, getEventTitle(${event.id}))">
                    <i class="fa-solid fa-check"></i> ثبت‌نام
                </button>
            </td>
        </tr>
    `).join('');
}

function loadAllEvents() {
    const status = document.getElementById('eventStatusFilter')?.value || 'all';
    setLoading('allEventsBody', 5);

    fetch(`/panel/student/api/events/?status=${encodeURIComponent(status)}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) throw new Error(data.error);

            const tableBody = document.getElementById('allEventsBody');
            if (!tableBody) return;

            if (!data.events.length) {
                setEmpty('allEventsBody', 5, 'هیچ رویدادی وجود ندارد');
                return;
            }

            tableBody.innerHTML = data.events.map(event => {
                const action = !event.is_registered && !event.is_full && event.status_code === 'upcoming'
                    ? `<button class="register-btn" onclick="registerEvent(${event.id}, getEventTitle(${event.id}))">ثبت‌نام</button>`
                    : event.is_registered
                        ? `<button class="cancel-btn" onclick="cancelRegistration(${event.registration_id}, getEventTitle(${event.id}))">لغو</button>`
                        : '<span class="status-rejected">غیرقابل ثبت‌نام</span>';

                const statusLabel = event.is_registered ? 'ثبت‌نام شده' : event.is_full ? 'تکمیل شده' : 'قابل ثبت‌نام';
                const statusClass = event.is_registered ? 'status-accepted' : event.is_full ? 'status-rejected' : 'status-pending';

                return `
                    <tr data-event-id="${event.id}" data-event-title="${escapeHtml(event.title)}">
                        <td><strong>${escapeHtml(event.title)}</strong></td>
                        <td>${escapeHtml(event.date)} - ${escapeHtml(event.time)}</td>
                        <td><span class="status-${escapeHtml(event.status_class)}">${escapeHtml(event.status)}</span></td>
                        <td><span class="${statusClass}">${statusLabel}</span></td>
                        <td>${action}</td>
                    </tr>
                `;
            }).join('');
        })
        .catch(error => {
            console.error('Error loading events:', error);
            setEmpty('allEventsBody', 5, 'خطا در دریافت رویدادها');
        });
}

function renderMyRegistrations(events) {
    const tableBody = document.getElementById('myRegistrationsBody');
    if (!tableBody) return;

    if (!events.length) {
        setEmpty('myRegistrationsBody', 4, 'هیچ ثبت‌نامی ندارید');
        return;
    }

    tableBody.innerHTML = events.map(registration => `
        <tr data-event-id="${registration.event_id}" data-event-title="${escapeHtml(registration.title)}">
            <td><strong>${escapeHtml(registration.title)}</strong></td>
            <td>${escapeHtml(registration.date)}</td>
            <td><span class="status-accepted">${escapeHtml(registration.status)}</span></td>
            <td>
                <button class="cancel-btn" onclick="cancelRegistration(${registration.id}, getEventTitle(${registration.event_id}))">
                    لغو ثبت‌نام
                </button>
            </td>
        </tr>
    `).join('');
}

function loadResources() {
    const category = document.getElementById('resourceFilter')?.value || 'all';
    setLoading('resourcesBody', 4);

    fetch(`/panel/student/api/resources/?category=${encodeURIComponent(category)}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) throw new Error(data.error);

            const tableBody = document.getElementById('resourcesBody');
            if (!tableBody) return;

            if (!data.resources.length) {
                setEmpty('resourcesBody', 4, 'هیچ منبعی وجود ندارد');
                return;
            }

            tableBody.innerHTML = data.resources.map(resource => `
                <tr>
                    <td><strong>${escapeHtml(resource.title)}</strong></td>
                    <td><span class="badge">${escapeHtml(resource.category || 'سایر')}</span></td>
                    <td>${escapeHtml(resource.description)}</td>
                    <td>
                        ${resource.has_file
                            ? `<button class="download-btn" onclick="downloadResource(${resource.id})"><i class="fa-solid fa-download"></i> دانلود</button>`
                            : '<span class="status-rejected">فایلی موجود نیست</span>'}
                        <span class="badge">${toPersianDigits(resource.download_count)} دانلود</span>
                    </td>
                </tr>
            `).join('');
        })
        .catch(error => {
            console.error('Error loading resources:', error);
            setEmpty('resourcesBody', 4, 'خطا در دریافت منابع');
        });
}

function getTickets() {
    try {
        return JSON.parse(localStorage.getItem('studentTickets') || '[]');
    } catch {
        return [];
    }
}

function saveTickets(tickets) {
    localStorage.setItem('studentTickets', JSON.stringify(tickets));
    document.getElementById('myTickets').innerText = toPersianDigits(tickets.length);
}

function loadTickets() {
    const tableBody = document.getElementById('ticketsBody');
    if (!tableBody) return;

    const tickets = getTickets();
    if (!tickets.length) {
        setEmpty('ticketsBody', 6, 'هنوز تیکتی ثبت نکرده‌اید');
        return;
    }

    tableBody.innerHTML = tickets.map(ticket => `
        <tr data-ticket-id="${ticket.id}" data-ticket-subject="${escapeHtml(ticket.subject)}">
            <td>#${toPersianDigits(ticket.id)}</td>
            <td><strong>${escapeHtml(ticket.subject)}</strong></td>
            <td><span class="badge">${escapeHtml(ticket.priority)}</span></td>
            <td><span class="status-pending">${escapeHtml(ticket.status)}</span></td>
            <td>${escapeHtml(ticket.date)}</td>
            <td>
                <button class="ticket-btn" onclick="viewTicket(${ticket.id})">مشاهده</button>
                <button class="cancel-btn" onclick="deleteTicket(${ticket.id})">حذف</button>
            </td>
        </tr>
    `).join('');
}

function loadProfile() {
    fetch('/panel/student/api/profile/')
        .then(response => response.json())
        .then(data => {
            if (data.error) throw new Error(data.error);

            currentProfileData = data;
            const fullName = `${data.first_name || ''} ${data.last_name || ''}`.trim() || data.username || 'دانشجو';
            document.getElementById('profileName').innerText = fullName;
            document.getElementById('profileStudentId').innerText = data.student_id || 'ثبت نشده';
            document.getElementById('profilePhone').innerText = data.phone_number || 'ثبت نشده';
            document.getElementById('profileMajor').innerText = data.major || 'ثبت نشده';
            document.getElementById('profileLevel').innerText = data.level || 'ثبت نشده';
            document.getElementById('profileEmail').innerText = data.email || 'ثبت نشده';
            document.getElementById('profileEntryYear').innerText = data.entry_year ? toPersianDigits(data.entry_year) : 'ثبت نشده';
            document.getElementById('profileTerm').innerText = data.term || 'ثبت نشده';
            document.getElementById('profileCommittee').innerText = data.committee || 'ثبت نشده';
            document.getElementById('profileInterest').innerText = data.interest || 'ثبت نشده';
            document.getElementById('profileBio').innerText = data.bio || 'ثبت نشده';
            document.getElementById('eventCount').innerText = toPersianDigits(data.event_count || 0);
            document.getElementById('downloadCount').innerText = toPersianDigits(data.download_count || 0);

            if (data.avatar_url) {
                document.getElementById('profileAvatar').innerHTML = `<img src="${escapeHtml(data.avatar_url)}" alt="${escapeHtml(fullName)}">`;
            }
        })
        .catch(error => {
            console.error('Error loading profile:', error);
        });
}

function fillProfileForm(data) {
    document.getElementById('editFirstName').value = data.first_name || '';
    document.getElementById('editLastName').value = data.last_name || '';
    document.getElementById('editPhoneNumber').value = data.phone_number || '';
    document.getElementById('editEmail').value = data.email || '';
    document.getElementById('editStudentId').value = data.student_id || '';
    document.getElementById('editMajor').value = data.major || '';
    document.getElementById('editLevel').value = data.level || '';
    document.getElementById('editEntryYear').value = data.entry_year || '';
    document.getElementById('editTerm').value = data.term || '';
    document.getElementById('editCommittee').value = data.committee || '';
    document.getElementById('editInterest').value = data.interest || '';
    document.getElementById('editBio').value = data.bio || '';
}

function toggleProfileEdit(isEditing) {
    const form = document.getElementById('profileEditForm');
    const editButton = document.getElementById('editProfileBtn');
    if (!form || !editButton) return;

    if (isEditing) {
        fillProfileForm(currentProfileData);
        form.classList.add('active');
        editButton.style.display = 'none';
        document.getElementById('editFirstName')?.focus();
    } else {
        form.classList.remove('active');
        editButton.style.display = 'inline-flex';
    }
}

function saveProfile(event) {
    event.preventDefault();

    const saveButton = document.getElementById('saveProfileBtn');
    const payload = {
        first_name: document.getElementById('editFirstName').value.trim(),
        last_name: document.getElementById('editLastName').value.trim(),
        phone_number: document.getElementById('editPhoneNumber').value.trim(),
        email: document.getElementById('editEmail').value.trim(),
        student_id: document.getElementById('editStudentId').value.trim(),
        major: document.getElementById('editMajor').value.trim(),
        level: document.getElementById('editLevel').value,
        entry_year: document.getElementById('editEntryYear').value,
        term: document.getElementById('editTerm').value.trim(),
        committee: document.getElementById('editCommittee').value.trim(),
        interest: document.getElementById('editInterest').value.trim(),
        bio: document.getElementById('editBio').value.trim()
    };

    saveButton.disabled = true;
    saveButton.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> در حال ذخیره...';

    fetch('/panel/student/api/profile/update/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                toggleProfileEdit(false);
                loadProfile();
            } else {
                alert(`خطا: ${data.error}`);
            }
        })
        .catch(error => {
            console.error('Error saving profile:', error);
            alert('خطا در ذخیره اطلاعات پروفایل');
        })
        .finally(() => {
            saveButton.disabled = false;
            saveButton.innerHTML = '<i class="fa-solid fa-floppy-disk"></i> ذخیره اطلاعات';
        });
}

function refreshConnectedSections() {
    loadDashboard();
    loadAllEvents();
    loadTickets();
}

function registerEvent(eventId, title) {
    if (!confirm(`آیا مطمئن هستید که می‌خواهید در "${title}" ثبت‌نام کنید؟`)) return;

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
                refreshConnectedSections();
            } else {
                alert(`خطا: ${data.error}`);
            }
        })
        .catch(error => {
            console.error('Error registering:', error);
            alert('خطا در ارتباط با سرور');
        });
}

function cancelRegistration(registrationId, title) {
    if (!confirm(`آیا از لغو ثبت‌نام در "${title}" اطمینان دارید؟`)) return;

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
                refreshConnectedSections();
            } else {
                alert(`خطا: ${data.error}`);
            }
        })
        .catch(error => {
            console.error('Error canceling:', error);
            alert('خطا در ارتباط با سرور');
        });
}

function downloadResource(resourceId) {
    window.open(`/panel/student/api/resources/${resourceId}/download/`, '_blank');
    setTimeout(() => {
        loadResources();
        loadProfile();
    }, 1000);
}

function changePassword() {
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmNewPassword').value;

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

    fetch('/panel/student/api/change-password/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            new_password: newPassword,
            confirm_password: confirmPassword
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                document.getElementById('newPassword').value = '';
                document.getElementById('confirmNewPassword').value = '';
            } else {
                alert(`خطا: ${data.error}`);
            }
        })
        .catch(error => {
            console.error('Error changing password:', error);
            alert('خطا در ارتباط با سرور');
        });
}

function submitTicket() {
    const subject = document.getElementById('ticketSubject').value.trim();
    const message = document.getElementById('ticketMessage').value.trim();
    const priority = document.getElementById('ticketPriority').value;

    if (!subject || !message) {
        alert('لطفاً موضوع و متن تیکت را وارد کنید');
        return;
    }

    const tickets = getTickets();
    const newTicket = {
        id: Date.now(),
        subject,
        message,
        priority,
        status: 'در انتظار بررسی',
        date: new Date().toLocaleDateString('fa-IR')
    };

    tickets.unshift(newTicket);
    saveTickets(tickets);
    closeTicketModal();
    loadTickets();
    alert('تیکت شما با موفقیت ثبت شد');
}

function deleteTicket(ticketId) {
    if (!confirm(`آیا از حذف "${getTicketTitle(ticketId)}" اطمینان دارید؟`)) return;
    saveTickets(getTickets().filter(ticket => ticket.id !== ticketId));
    loadTickets();
}

function filterResources() {
    loadResources();
}

function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (const cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') return value;
    }
    return '';
}

function openNewTicketModal() {
    document.getElementById('newTicketModal').style.display = 'flex';
}

function closeTicketModal() {
    document.getElementById('newTicketModal').style.display = 'none';
    document.getElementById('ticketSubject').value = '';
    document.getElementById('ticketPriority').value = 'متوسط';
    document.getElementById('ticketMessage').value = '';
}

function logout() {
    if (confirm('آیا مطمئن هستید که می‌خواهید خارج شوید؟')) {
        window.location.href = '/accounts/logout/';
    }
}

function changeProfilePic() {
    alert('برای تغییر عکس پروفایل، لطفاً از بخش مدیریت حساب کاربری استفاده کنید.');
}

function viewTicket(id) {
    const ticket = getTickets().find(item => item.id === id);
    if (!ticket) return;
    alert(`موضوع: ${ticket.subject}\nاولویت: ${ticket.priority}\nوضعیت: ${ticket.status}\n\n${ticket.message}`);
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('toggleSidebar')?.addEventListener('click', () => {
        if (window.innerWidth <= 900) {
            document.body.classList.toggle('sidebar-open');
        } else {
            document.body.classList.toggle('sidebar-collapsed');
        }
    });

    document.getElementById('newTicketModal')?.addEventListener('click', event => {
        if (event.target.id === 'newTicketModal') {
            closeTicketModal();
        }
    });

    loadDashboard();
    loadAllEvents();
    loadResources();
    loadTickets();
    loadProfile();
});

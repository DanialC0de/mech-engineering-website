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

let currentProfileData = {};

function switchTab(tabId) {
    document.querySelectorAll('.menu li').forEach(item => item.classList.remove('active'));
    document.querySelector(`.menu li[data-tab="${tabId}"]`)?.classList.add('active');

    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    document.getElementById(tabId)?.classList.add('active');

    const titles = {
        dashboard: 'داشبورد استاد',
        events: 'مدیریت رویدادها',
        resources: 'منابع علمی',
        profile: 'پروفایل من'
    };
    document.getElementById('pageTitle').innerText = titles[tabId] || 'پنل استاد';

    const loaders = {
        dashboard: loadDashboard,
        events: loadAllEvents,
        resources: loadArticles,
        profile: loadProfile
    };

    loaders[tabId]?.();
    if (window.innerWidth <= 900) {
        document.body.classList.remove('sidebar-open');
    }
}

// ==================== داشبورد ====================
function loadDashboard() {
    fetch('/panel/professor/api/dashboard/')
        .then(response => response.json())
        .then(data => {
            if (data.error) throw new Error(data.error);

            document.getElementById('upcomingEvents').innerText = toPersianDigits(data.stats.upcomingEvents || 0);
            document.getElementById('invitations').innerText = toPersianDigits(data.stats.invitations || 0);
            document.getElementById('newMessages').innerText = toPersianDigits(data.stats.newMessages || 0);
            document.getElementById('myArticles').innerText = toPersianDigits(data.stats.myArticles || 0);

            renderInvitations(data.invitations || []);
            renderMyEvents(data.myEvents || []);
        })
        .catch(error => {
            console.error('Error loading dashboard:', error);
            setEmpty('invitationsBody', 5, 'خطا در دریافت اطلاعات');
            setEmpty('myEventsBody', 4, 'خطا در دریافت اطلاعات');
        });
}

function renderInvitations(invitations) {
    const tbody = document.getElementById('invitationsBody');
    if (!tbody) return;

    if (!invitations.length) {
        setEmpty('invitationsBody', 5, 'هیچ دعوتنامه‌ای وجود ندارد');
        return;
    }

    tbody.innerHTML = invitations.map(item => `
        <tr>
            <td><strong>${escapeHtml(item.title)}</strong></td>
            <td>${escapeHtml(item.date)}</td>
            <td>${escapeHtml(item.role)}</td>
            <td><span class="status-pending">${escapeHtml(item.status)}</span></td>
            <td><button class="primary-btn" onclick="respondInvitation(${item.id}, 'accept')">پذیرش</button>
                <button class="secondary-btn" onclick="respondInvitation(${item.id}, 'reject')">رد</button></td>
        </tr>
    `).join('');
}

function renderMyEvents(events) {
    const tbody = document.getElementById('myEventsBody');
    if (!tbody) return;

    if (!events.length) {
        setEmpty('myEventsBody', 4, 'هیچ رویدادی برای شما ثبت نشده');
        return;
    }

    tbody.innerHTML = events.map(event => `
        <tr>
            <td><strong>${escapeHtml(event.title)}</strong></td>
            <td>${escapeHtml(event.date)}</td>
            <td>${escapeHtml(event.time)}</td>
            <td>${escapeHtml(event.role)}</td>
        </tr>
    `).join('');
}

function respondInvitation(id, action) {
    fetch(`/panel/professor/api/invitations/${id}/respond/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ action })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                loadDashboard();
            } else {
                alert(`خطا: ${data.error}`);
            }
        })
        .catch(error => {
            console.error('Error responding to invitation:', error);
            alert('خطا در ارتباط با سرور');
        });
}

// ==================== رویدادها ====================
function loadAllEvents() {
    setLoading('allEventsBody', 6);

    fetch('/panel/professor/api/events/')
        .then(response => response.json())
        .then(data => {
            if (data.error) throw new Error(data.error);

            const tbody = document.getElementById('allEventsBody');
            if (!tbody) return;

            if (!data.events.length) {
                setEmpty('allEventsBody', 6, 'هیچ رویدادی وجود ندارد');
                return;
            }

            tbody.innerHTML = data.events.map(event => `
                <tr>
                    <td><strong>${escapeHtml(event.title)}</strong></td>
                    <td>${escapeHtml(event.date)}</td>
                    <td>${escapeHtml(event.time)}</td>
                    <td>${escapeHtml(event.type)}</td>
                    <td><span class="status-${event.status_class}">${escapeHtml(event.status)}</span></td>
                    <td><button class="primary-btn" onclick="viewEvent(${event.id})"><i class="fa-solid fa-eye"></i></button></td>
                </tr>
            `).join('');
        })
        .catch(error => {
            console.error('Error loading events:', error);
            setEmpty('allEventsBody', 6, 'خطا در دریافت رویدادها');
        });
}

function viewEvent(id) {
    alert(`مشاهده جزئیات رویداد با شناسه ${id} - در حال توسعه`);
}

// ==================== منابع علمی ====================
function loadArticles() {
    setLoading('articlesBody', 5);

    fetch('/panel/professor/api/articles/')
        .then(response => response.json())
        .then(data => {
            if (data.error) throw new Error(data.error);

            const tbody = document.getElementById('articlesBody');
            if (!tbody) return;

            if (!data.articles.length) {
                setEmpty('articlesBody', 5, 'هیچ مقاله‌ای وجود ندارد');
                return;
            }

            tbody.innerHTML = data.articles.map(article => `
                <tr>
                    <td><strong>${escapeHtml(article.title)}</strong></td>
                    <td>${escapeHtml(article.author)}</td>
                    <td>${escapeHtml(article.date)}</td>
                    <td><span class="status-${article.status_class}">${escapeHtml(article.status)}</span></td>
                    <td><button class="download-btn" onclick="downloadArticle(${article.id})"><i class="fa-solid fa-download"></i></button>
                        <button class="cancel-btn" onclick="deleteArticle(${article.id})"><i class="fa-solid fa-trash"></i></button></td>
                </tr>
            `).join('');
        })
        .catch(error => {
            console.error('Error loading articles:', error);
            setEmpty('articlesBody', 5, 'خطا در دریافت مقالات');
        });
}

function downloadArticle(id) {
    window.open(`/panel/professor/api/articles/${id}/download/`, '_blank');
}

function deleteArticle(id) {
    if (!confirm('آیا از حذف این مقاله اطمینان دارید؟')) return;

    fetch(`/panel/professor/api/articles/${id}/delete/`, {
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
                loadArticles();
            } else {
                alert(`خطا: ${data.error}`);
            }
        })
        .catch(error => {
            console.error('Error deleting article:', error);
            alert('خطا در حذف مقاله');
        });
}

// ==================== پروفایل (یکپارچه با دانشجو) ====================
function loadProfile() {
    fetch('/panel/professor/api/profile/')
        .then(response => response.json())
        .then(data => {
            if (data.error) throw new Error(data.error);

            currentProfileData = data;
            const fullName = `${data.first_name || ''} ${data.last_name || ''}`.trim() || data.username || 'استاد';
            document.getElementById('profName').innerText = fullName;
            document.getElementById('profPosition').innerText = data.position || 'ثبت نشده';
            document.getElementById('profFaculty').innerText = data.faculty || 'ثبت نشده';
            document.getElementById('profEmail').innerText = data.email || 'ثبت نشده';
            document.getElementById('profPhone').innerText = data.phone_number || 'ثبت نشده';
            document.getElementById('profExpertise').innerText = data.expertise || 'ثبت نشده';
            document.getElementById('profBio').innerText = data.bio || 'ثبت نشده';
            document.getElementById('profArticles').innerText = toPersianDigits(data.article_count || 0);

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
    document.getElementById('editPosition').value = data.position || '';
    document.getElementById('editFaculty').value = data.faculty || '';
    document.getElementById('editPhone').value = data.phone_number || '';
    document.getElementById('editEmail').value = data.email || '';
    document.getElementById('editExpertise').value = data.expertise || '';
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
        position: document.getElementById('editPosition').value,
        faculty: document.getElementById('editFaculty').value.trim(),
        phone_number: document.getElementById('editPhone').value.trim(),
        email: document.getElementById('editEmail').value.trim(),
        expertise: document.getElementById('editExpertise').value.trim(),
        bio: document.getElementById('editBio').value.trim()
    };

    saveButton.disabled = true;
    saveButton.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> در حال ذخیره...';

    fetch('/panel/professor/api/profile/update/', {
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

// ==================== تغییر رمز عبور ====================
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

    fetch('/panel/professor/api/change-password/', {
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

// ==================== مودال‌ها ====================
function openProposeEventModal() {
    document.getElementById('proposeEventModal').style.display = 'flex';
}

function closeProposeModal() {
    document.getElementById('proposeEventModal').style.display = 'none';
    document.getElementById('proposeTitle').value = '';
    document.getElementById('proposeDesc').value = '';
    document.getElementById('proposeDate').value = '';
}

function submitProposal() {
    const title = document.getElementById('proposeTitle').value.trim();
    const desc = document.getElementById('proposeDesc').value.trim();
    const date = document.getElementById('proposeDate').value;
    const type = document.getElementById('proposeType').value;

    if (!title || !desc || !date) {
        alert('لطفاً تمام فیلدها را پر کنید');
        return;
    }

    fetch('/panel/professor/api/events/propose/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ title, description: desc, date, type })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                closeProposeModal();
                loadAllEvents();
            } else {
                alert(`خطا: ${data.error}`);
            }
        })
        .catch(error => {
            console.error('Error proposing event:', error);
            alert('خطا در ارسال پیشنهاد');
        });
}

function openAddArticleModal() {
    document.getElementById('addArticleModal').style.display = 'flex';
}

function closeArticleModal() {
    document.getElementById('addArticleModal').style.display = 'none';
    document.getElementById('articleTitle').value = '';
    document.getElementById('articleAbstract').value = '';
    document.getElementById('articleFile').value = '';
}

function submitArticle() {
    const title = document.getElementById('articleTitle').value.trim();
    const abstract = document.getElementById('articleAbstract').value.trim();
    const file = document.getElementById('articleFile').files[0];

    if (!title || !file) {
        alert('لطفاً عنوان و فایل مقاله را وارد کنید');
        return;
    }

    const formData = new FormData();
    formData.append('title', title);
    formData.append('abstract', abstract);
    formData.append('file', file);

    fetch('/panel/professor/api/articles/upload/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken()
        },
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                closeArticleModal();
                loadArticles();
                loadDashboard();
            } else {
                alert(`خطا: ${data.error}`);
            }
        })
        .catch(error => {
            console.error('Error uploading article:', error);
            alert('خطا در آپلود مقاله');
        });
}

// ==================== ابزارها ====================
function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (const cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') return value;
    }
    return '';
}

function logout() {
    if (confirm('آیا مطمئن هستید که می‌خواهید خارج شوید؟')) {
        window.location.href = '/accounts/logout/';
    }
}

function changeProfilePic() {
    alert('برای تغییر عکس پروفایل، لطفاً از بخش مدیریت حساب کاربری استفاده کنید.');
}

// ==================== رویدادهای DOM ====================
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('toggleSidebar')?.addEventListener('click', () => {
        if (window.innerWidth <= 900) {
            document.body.classList.toggle('sidebar-open');
        } else {
            document.body.classList.toggle('sidebar-collapsed');
        }
    });

    // بستن مودال با کلیک بیرون
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', event => {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        });
    });

    // بارگذاری اولیه
    loadDashboard();
    loadAllEvents();
    loadArticles();
    loadProfile();
});
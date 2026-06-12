let aboutLink = document.querySelector('.nav-links a:nth-child(2)');
let aboutUl = document.getElementById('ul-about');

aboutLink.addEventListener('mouseover', function () {
    aboutUl.classList.add('show');
});
aboutLink.addEventListener('mouseout', function () {
    aboutUl.classList.remove("show");
});

aboutUl.addEventListener('mouseover', function () {
    aboutUl.classList.add('show');
});
aboutUl.addEventListener('mouseout', function () {
    aboutUl.classList.remove("show");
});



let relationLink = document.querySelector('.nav-links a:nth-child(3)');
let relationUl = document.getElementById('ul-relation');

relationLink.addEventListener('mouseover', function () {
    relationUl.classList.add('show');
});
relationLink.addEventListener('mouseout', function () {
    relationUl.classList.remove("show");
});

relationUl.addEventListener('mouseover', function () {
    relationUl.classList.add('show');
});
relationUl.addEventListener('mouseout', function () {
    relationUl.classList.remove("show");
});


// _________________________________________________________________________


// کد های مربوط به اسلایدر

let currentSlide = 1;
const totalSlides = 5;

// تابع پیدا کردن شماره اسلاید فعلی بر اساس رادیوباکس تیک‌خورده
function updateCurrentSlide() {
    for (let i = 1; i <= totalSlides; i++) {
        if (document.getElementById('slide' + i).checked) {
            currentSlide = i;
            break;
        }
    }
}

// تابع اصلی رفتن به اسلاید مشخص و کنترل ویدیوها
function goToSlide(n) {
    if (n < 1) n = totalSlides;
    if (n > totalSlides) n = 1;

    // تغییر وضعیت رادیو باکس اسلاید
    const targetRadio = document.getElementById('slide' + n);
    if (targetRadio) {
        targetRadio.checked = true;
        currentSlide = n;
    }

    // ۱. ابتدا تمام ویدیوها را متوقف و صفر می‌کنیم
    document.querySelectorAll('video').forEach(video => {
        video.pause();
        video.currentTime = 0;
    });

    // ۲. حالا ویدیو اسلاید فعال را پیدا کرده و پخش می‌کنیم (کوتیشن‌ها اصلاح شد)
    const activeSlide = document.querySelector('input[name="slider"]#slide' + n + ' + .slide');

    if (activeSlide) {
        const video = activeSlide.querySelector('video');
        if (video) {
            video.muted = true;

            let playPromise = video.play();
            if (playPromise !== undefined) {
                playPromise.catch(error => {
                    console.log("پخش خودکار توسط مرورگر مسدود شد:", error);
                });
            }
        }
    }
}

// گوش دادن به تغییر وضعیت رادیوباکس‌ها (کلیک روی نقاط ناوبری پایین)
for (let i = 1; i <= totalSlides; i++) {
    const radioBtn = document.getElementById('slide' + i);
    if (radioBtn) {
        radioBtn.addEventListener('change', function () {
            updateCurrentSlide();
            goToSlide(currentSlide);
        });
    }
}

// فعال‌سازی دقیق دکمه‌های قبلی و بعدی بر اساس کلاس‌های اختصاصی شما
const prevBtn = document.querySelector('.slider-controls .prev');
const nextBtn = document.querySelector('.slider-controls .next');

if (prevBtn) {
    prevBtn.addEventListener('click', function (e) {
        e.preventDefault();
        goToSlide(currentSlide - 1);
    });
}

if (nextBtn) {
    nextBtn.addEventListener('click', function (e) {
        e.preventDefault();
        goToSlide(currentSlide + 1);
    });
}

// اجرای اولیه برای هماهنگی مقادیر
updateCurrentSlide();
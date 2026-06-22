// ============================================
// بخش ۱: منوهای کشویی (دراپ‌داون) هدر
// ============================================
document.addEventListener('DOMContentLoaded', function() {

    // ---------- شناسایی المنت‌ها ----------
    const aboutTrigger = document.querySelector('.nav-links a[href*="about"]');
    const industryTrigger = document.querySelector('.nav-links a[href*="industry"]');
    const aboutMenu = document.getElementById('ul-about');
    const industryMenu = document.getElementById('ul-relation');
    
    let timeoutId = null;

    // ---------- توابع کمکی ----------
    function showMenu(menu) {
        if (!menu) return;
        clearTimeout(timeoutId);
        menu.classList.add('show');
    }

    function hideMenuWithDelay(menu) {
        if (!menu) return;
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
            menu.classList.remove('show');
        }, 200); // ۲۰۰ میلی‌ثانیه تاخیر برای جلوگیری از پرش ناگهانی
    }

    // ---------- تنظیم منوی "درباره دانشکده" ----------
    if (aboutTrigger && aboutMenu) {
        aboutTrigger.addEventListener('mouseenter', function(e) {
            showMenu(aboutMenu);
        });
        aboutTrigger.addEventListener('mouseleave', function(e) {
            hideMenuWithDelay(aboutMenu);
        });
        aboutMenu.addEventListener('mouseenter', function(e) {
            showMenu(aboutMenu);
        });
        aboutMenu.addEventListener('mouseleave', function(e) {
            hideMenuWithDelay(aboutMenu);
        });
    }

    // ---------- تنظیم منوی "ارتباط با صنعت" ----------
    if (industryTrigger && industryMenu) {
        industryTrigger.addEventListener('mouseenter', function(e) {
            showMenu(industryMenu);
        });
        industryTrigger.addEventListener('mouseleave', function(e) {
            hideMenuWithDelay(industryMenu);
        });
        industryMenu.addEventListener('mouseenter', function(e) {
            showMenu(industryMenu);
        });
        industryMenu.addEventListener('mouseleave', function(e) {
            hideMenuWithDelay(industryMenu);
        });
    }

    // ============================================
    // بخش ۲: اسکریپت گالری اسلایدر (نسخه مقاوم)
    // ============================================
    
    // چک 1: آیا المنت مخفی وجود داره؟
    const configEl = document.getElementById('gallery-config');
    if (!configEl) {
        console.warn('⚠️ المنت گالری (gallery-config) پیدا نشد!');
        return;
    }
    
    // چک 2: آیا تعداد اسلایدها معتبره؟
    const totalSlides = parseInt(configEl.dataset.total) || 0;
    if (totalSlides === 0) {
        console.warn('⚠️ تعداد اسلایدها صفر است!');
        return;
    }
    
    // چک 3: آیا حداقل یک اسلاید در DOM وجود داره؟
    const firstSlide = document.getElementById('slide1');
    if (!firstSlide) {
        console.warn('⚠️ هیچ اسلایدی در DOM پیدا نشد!');
        return;
    }
    
    // چک 4: آیا دکمه‌های ناوبری وجود دارن؟
    const prevBtn = document.querySelector('.slider-controls .prev');
    const nextBtn = document.querySelector('.slider-controls .next');
    
    if (!prevBtn || !nextBtn) {
        console.warn('⚠️ دکمه‌های قبلی/بعدی پیدا نشدند!');
    }
    
    console.log(`✅ گالری پیدا شد. تعداد اسلایدها: ${totalSlides}`);
    
    let currentSlide = 1;
    
    // تابع به‌روزرسانی اسلاید فعلی
    function updateCurrentSlide() {
        for(let i = 1; i <= totalSlides; i++) {
            const radio = document.getElementById('slide' + i);
            if(radio && radio.checked) {
                currentSlide = i;
                break;
            }
        }
    }
    
    // تابع رفتن به اسلاید مشخص
    function goToSlide(n) {
        // محدود کردن عدد بین 1 تا totalSlides
        if(n < 1) n = totalSlides;
        if(n > totalSlides) n = 1;
        
        const targetRadio = document.getElementById('slide' + n);
        if (targetRadio) {
            targetRadio.checked = true;
            currentSlide = n;
        } else {
            console.warn(`⚠️ اسلاید شماره ${n} پیدا نشد!`);
            return;
        }
        
        // توقف تمام ویدیوها
        document.querySelectorAll('video').forEach(video => {
            video.pause();
            video.currentTime = 0;
        });

        // پخش خودکار ویدیوی اسلاید فعال
        const activeSlide = document.querySelector('#slide' + n + ' ~ .slide');
        if (activeSlide) {
            const video = activeSlide.querySelector('video');
            if (video) {
                video.muted = true;
                video.play().catch(error => {
                    console.log('ℹ️ پخش خودکار توسط مرورگر مسدود شد');
                });
            }
        }
    }
    
    // اضافه کردن رویداد به رادیو دکمه‌ها
    for(let i = 1; i <= totalSlides; i++) {
        const radioBtn = document.getElementById('slide' + i);
        if(radioBtn) {
            radioBtn.addEventListener('change', function() {
                updateCurrentSlide();
                goToSlide(currentSlide);
            });
        }
    }
    
    // دکمه‌های قبلی و بعدی
    if(prevBtn) {
        prevBtn.addEventListener('click', function(e) {
            e.preventDefault();
            goToSlide(currentSlide - 1);
        });
    }
    
    if(nextBtn) {
        nextBtn.addEventListener('click', function(e) {
            e.preventDefault();
            goToSlide(currentSlide + 1);
        });
    }
    
    // تنظیم اسلاید اولیه
    updateCurrentSlide();
    
    console.log(`✅ گالری با موفقیت بارگذاری شد. اسلاید فعلی: ${currentSlide}`);

});
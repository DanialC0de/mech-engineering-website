// ============================================
// اسکریپت گالری اسلایدر - نسخه مقاوم
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    
    // ========================================
    // چک 1: آیا المنت مخفی وجود داره؟
    // ========================================
    const configEl = document.getElementById('gallery-config');
    if (!configEl) {
        console.warn('⚠️ المنت گالری (gallery-config) پیدا نشد!');
        return;
    }
    
    // ========================================
    // چک 2: آیا تعداد اسلایدها معتبره؟
    // ========================================
    const totalSlides = parseInt(configEl.dataset.total) || 0;
    if (totalSlides === 0) {
        console.warn('⚠️ تعداد اسلایدها صفر است!');
        return;
    }
    
    // ========================================
    // چک 3: آیا حداقل یک اسلاید در DOM وجود داره؟
    // ========================================
    const firstSlide = document.getElementById('slide1');
    if (!firstSlide) {
        console.warn('⚠️ هیچ اسلایدی در DOM پیدا نشد!');
        return;
    }
    
    // ========================================
    // چک 4: آیا دکمه‌های ناوبری وجود دارن؟
    // ========================================
    const prevBtn = document.querySelector('.slider-controls .prev');
    const nextBtn = document.querySelector('.slider-controls .next');
    
    if (!prevBtn || !nextBtn) {
        console.warn('⚠️ دکمه‌های قبلی/بعدی پیدا نشدند!');
        // ولی ادامه بده، شاید فقط دکمه‌ها نباشن
    }
    
    // ========================================
    // شروع کد اصلی
    // ========================================
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
        // استفاده از سِلکتور امن‌تر
        const activeSlide = document.querySelector('#slide' + n + ' ~ .slide');
        if (activeSlide) {
            const video = activeSlide.querySelector('video');
            if (video) {
                video.muted = true;
                video.play().catch(error => {
                    // این خطا رو نادیده بگیر، فقط لاگ کن
                    console.log('ℹ️ پخش خودکار توسط مرورگر مسدود شد');
                });
            }
        }
    }
    
    // ========================================
    // اضافه کردن رویداد به رادیو دکمه‌ها
    // ========================================
    for(let i = 1; i <= totalSlides; i++) {
        const radioBtn = document.getElementById('slide' + i);
        if(radioBtn) {
            radioBtn.addEventListener('change', function() {
                updateCurrentSlide();
                goToSlide(currentSlide);
            });
        }
    }
    
    // ========================================
    // دکمه‌های قبلی و بعدی
    // ========================================
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
    
    // ========================================
    // تنظیم اسلاید اولیه
    // ========================================
    updateCurrentSlide();
    
    console.log(`✅ گالری با موفقیت بارگذاری شد. اسلاید فعلی: ${currentSlide}`);
});
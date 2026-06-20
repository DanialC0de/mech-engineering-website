# students/forms.py
from django import forms
from django.contrib.auth import get_user_model
from .models import StudentProfile

User = get_user_model()


class StudentProfileForm(forms.ModelForm):
    """فرم ویرایش پروفایل دانشجو"""
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="نام",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام خود را وارد کنید'
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label="نام خانوادگی",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام خانوادگی خود را وارد کنید'
        })
    )
    
    email = forms.EmailField(
        required=True,
        label="ایمیل",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ایمیل خود را وارد کنید'
        })
    )
    
    class Meta:
        model = StudentProfile
        fields = ['student_id', 'major', 'level', 'entry_year', 'avatar']
        labels = {
            'student_id': 'شماره دانشجویی',
            'major': 'رشته تحصیلی',
            'level': 'مقطع تحصیلی',
            'entry_year': 'سال ورود',
            'avatar': 'عکس پروفایل',
        }
        widgets = {
            'student_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثال: ۴۰۱۱۲۳۴۵'
            }),
            'major': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثال: مهندسی مکانیک'
            }),
            'level': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', 'انتخاب مقطع'),
                ('کارشناسی', 'کارشناسی'),
                ('کارشناسی ارشد', 'کارشناسی ارشد'),
                ('دکتری', 'دکتری'),
            ]),
            'entry_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثال: ۱۴۰۰',
                'min': 1390,
                'max': 1410
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # اگر کاربر وجود دارد، اطلاعات را از User هم پر کنیم
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email
        
        # اضافه کردن کلاس به فیلدها برای استایل بهتر
        for field in self.fields:
            if field not in ['avatar']:
                self.fields[field].widget.attrs.update({'class': 'form-control'})
    
    def clean_student_id(self):
        """اعتبارسنجی شماره دانشجویی"""
        student_id = self.cleaned_data.get('student_id')
        if student_id:
            # بررسی اینکه شماره دانشجویی فقط عدد باشد
            if not student_id.isdigit():
                raise forms.ValidationError('شماره دانشجویی باید فقط شامل اعداد باشد')
            
            # بررسی اینکه شماره دانشجویی ۸ رقمی باشد
            if len(student_id) != 8:
                raise forms.ValidationError('شماره دانشجویی باید ۸ رقمی باشد')
            
            # بررسی یکتا بودن شماره دانشجویی (به جز خود کاربر)
            if StudentProfile.objects.filter(
                student_id=student_id
            ).exclude(user=self.user).exists():
                raise forms.ValidationError('این شماره دانشجویی قبلاً ثبت شده است')
        
        return student_id
    
    def clean_entry_year(self):
        """اعتبارسنجی سال ورود"""
        entry_year = self.cleaned_data.get('entry_year')
        if entry_year:
            import jdatetime
            current_year = jdatetime.datetime.now().year
            if entry_year < 1390 or entry_year > current_year:
                raise forms.ValidationError(f'سال ورود باید بین ۱۳۹۰ تا {current_year} باشد')
        return entry_year
    
    def save(self, commit=True):
        # ذخیره اطلاعات User
        if self.user:
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            self.user.email = self.cleaned_data['email']
            if commit:
                self.user.save()
        
        # ذخیره اطلاعات StudentProfile
        profile = super().save(commit=False)
        profile.user = self.user
        if commit:
            profile.save()
        return profile


class ChangePasswordForm(forms.Form):
    """فرم تغییر رمز عبور"""
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور فعلی را وارد کنید'
        }),
        label="رمز عبور فعلی"
    )
    
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور جدید را وارد کنید (حداقل ۸ کاراکتر)'
        }),
        label="رمز عبور جدید",
        min_length=8
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور جدید را تکرار کنید'
        }),
        label="تکرار رمز عبور جدید"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("رمز عبور جدید با تکرار آن مطابقت ندارد")
        
        return cleaned_data
    
    def clean_new_password(self):
        """اعتبارسنجی رمز عبور جدید"""
        password = self.cleaned_data.get('new_password')
        
        if len(password) < 8:
            raise forms.ValidationError('رمز عبور باید حداقل ۸ کاراکتر باشد')
        
        # بررسی وجود حروف بزرگ و کوچک
        if not any(c.isupper() for c in password):
            raise forms.ValidationError('رمز عبور باید حداقل یک حرف بزرگ داشته باشد')
        
        if not any(c.islower() for c in password):
            raise forms.ValidationError('رمز عبور باید حداقل یک حرف کوچک داشته باشد')
        
        if not any(c.isdigit() for c in password):
            raise forms.ValidationError('رمز عبور باید حداقل یک عدد داشته باشد')
        
        return password


class TicketForm(forms.Form):
    """فرم ایجاد تیکت جدید"""
    subject = forms.CharField(
        max_length=200,
        required=True,
        label="موضوع",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'موضوع تیکت را وارد کنید'
        })
    )
    
    priority = forms.ChoiceField(
        choices=[
            ('کم', 'کم'),
            ('متوسط', 'متوسط'),
            ('فوری', 'فوری')
        ],
        required=True,
        label="اولویت",
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    message = forms.CharField(
        required=True,
        label="متن پیام",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'متن تیکت را وارد کنید...'
        })
    )
    
    def clean_subject(self):
        subject = self.cleaned_data.get('subject')
        if len(subject) < 5:
            raise forms.ValidationError('موضوع باید حداقل ۵ کاراکتر باشد')
        return subject
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError('متن پیام باید حداقل ۱۰ کاراکتر باشد')
        return message
# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from students.models import StudentProfile

User = get_user_model()

class StudentRegistrationForm(UserCreationForm):
    """فرم ثبت‌نام دانشجو"""
    
    # فیلدهای User
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
    
    # فیلدهای StudentProfile
    student_id = forms.CharField(
        max_length=20,
        required=True,
        label="شماره دانشجویی",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'مثال: ۴۰۱۱۲۳۴۵'
        })
    )
    
    major = forms.CharField(
        max_length=100,
        required=True,
        label="رشته تحصیلی",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'مثال: مهندسی مکانیک'
        })
    )
    
    level = forms.ChoiceField(
        choices=[
            ('', 'انتخاب مقطع'),
            ('کارشناسی', 'کارشناسی'),
            ('کارشناسی ارشد', 'کارشناسی ارشد'),
            ('دکتری', 'دکتری'),
        ],
        required=True,
        label="مقطع تحصیلی",
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    entry_year = forms.IntegerField(
        required=True,
        label="سال ورود",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'مثال: ۱۴۰۰',
            'min': 1390,
            'max': 1410
        })
    )
    
    term = forms.CharField(
        max_length=50,
        required=True,
        label="ترم تحصیلی",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'مثال: ترم ۴'
        })
    )
    
    committee = forms.CharField(
        max_length=100,
        required=False,
        label="کمیته مورد نظر",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'کمیته مورد نظر خود را وارد کنید'
        })
    )
    
    interest = forms.CharField(
        max_length=200,
        required=False,
        label="تخصص/علاقه‌مندی",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'تخصص یا علاقه‌مندی خود را وارد کنید'
        })
    )
    
    bio = forms.CharField(
        required=False,
        label="درباره خود",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'درباره خودتان بنویسید...'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def clean_student_id(self):
        """اعتبارسنجی شماره دانشجویی"""
        student_id = self.cleaned_data.get('student_id')
        if student_id:
            if not student_id.isdigit():
                raise forms.ValidationError('شماره دانشجویی باید فقط شامل اعداد باشد')
            if len(student_id) != 8:
                raise forms.ValidationError('شماره دانشجویی باید ۸ رقمی باشد')
            if StudentProfile.objects.filter(student_id=student_id).exists():
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
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            # ایجاد پروفایل دانشجو
            StudentProfile.objects.create(
                user=user,
                student_id=self.cleaned_data['student_id'],
                major=self.cleaned_data['major'],
                level=self.cleaned_data['level'],
                entry_year=self.cleaned_data['entry_year'],
                term=self.cleaned_data['term'],
                committee=self.cleaned_data.get('committee', ''),
                interest=self.cleaned_data.get('interest', ''),
                bio=self.cleaned_data.get('bio', '')
            )
        return user
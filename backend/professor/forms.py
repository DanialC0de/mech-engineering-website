# professor/forms.py
from django import forms
from django.contrib.auth import get_user_model
from .models import ProfessorProfile

User = get_user_model()


class ProfessorProfileForm(forms.ModelForm):
    """فرم ویرایش پروفایل استاد"""
    
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
        model = ProfessorProfile
        fields = ['employee_id', 'department', 'academic_rank', 'field_of_study', 
                  'office_number', 'research_interests', 'publications', 'bio', 'avatar']
        labels = {
            'employee_id': 'شماره پرسنلی',
            'department': 'دانشکده',
            'academic_rank': 'مرتبه علمی',
            'field_of_study': 'رشته تخصصی',
            'office_number': 'شماره دفتر',
            'research_interests': 'زمینه‌های پژوهشی',
            'publications': 'مقالات و تالیفات',
            'bio': 'درباره خود',
            'avatar': 'عکس پروفایل',
        }
        widgets = {
            'employee_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثال: ۱۲۳۴۵'
            }),
            'department': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثال: دانشکده مهندسی مکانیک'
            }),
            'academic_rank': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', 'انتخاب مرتبه'),
                ('مربی', 'مربی'),
                ('استادیار', 'استادیار'),
                ('دانشیار', 'دانشیار'),
                ('استاد', 'استاد'),
            ]),
            'field_of_study': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثال: ترمودینامیک'
            }),
            'office_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثال: اتاق ۲۰۵'
            }),
            'research_interests': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'زمینه‌های پژوهشی خود را بنویسید...'
            }),
            'publications': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'لیست مقالات و تالیفات خود را بنویسید...'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'درباره خود بنویسید...'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
    
    def clean_employee_id(self):
        """اعتبارسنجی شماره پرسنلی"""
        employee_id = self.cleaned_data.get('employee_id')
        if employee_id:
            if ProfessorProfile.objects.filter(
                employee_id=employee_id
            ).exclude(user=self.user).exists():
                raise forms.ValidationError('این شماره پرسنلی قبلاً ثبت شده است')
        
        return employee_id
    
    def save(self, commit=True):
        # ذخیره اطلاعات User
        if self.user:
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            self.user.email = self.cleaned_data['email']
            if commit:
                self.user.save()
        
        # ذخیره اطلاعات Profile
        return super().save(commit=commit)


class ChangePasswordForm(forms.Form):
    """فرم تغییر رمز عبور"""
    new_password = forms.CharField(
        max_length=100,
        required=True,
        label="رمز عبور جدید",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور جدید را وارد کنید'
        })
    )
    
    confirm_password = forms.CharField(
        max_length=100,
        required=True,
        label="تکرار رمز عبور",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور را دوباره وارد کنید'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password and confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError('رمز عبور با تکرار آن مطابقت ندارد')
        
        return cleaned_data
    
    def clean_new_password(self):
        password = self.cleaned_data.get('new_password')
        
        if len(password) < 8:
            raise forms.ValidationError('رمز عبور باید حداقل ۸ کاراکتر باشد')
        
        return password

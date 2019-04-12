from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Member, Profile


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = Member
        fields = ['email']

    def clean_email(self): #check that email is not already registered
        email = self.cleaned_data.get('email')
        emailCheck = Member.objects.filter(email=email)
        if emailCheck.exists():
            raise forms.ValidationError("Email already has a registered account")
        return email
    
    def clean_password2(self): #check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

class MemberCreationForm(forms.ModelForm):
    #Form for admin to create new accounts
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Member
        fields = ['email']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit=True):
        #Save the provided password in hashed format
        member = super(MemberCreationForm, self).save(commit=False)
        member.set_password(self.cleaned_data["password1"])
        if commit:
            member.save()
        return member
    
class MemberChangeForm(forms.ModelForm):
    #Form for updating users.  Replaces pasword field with admin's password hash display field.

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Member
        fields = ['email', 'password', 'active', 'staff', 'admin']

    def clean_password(self):
        return self.initial["password"]
        
class ProfileForm(MemberCreationForm):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    address = forms.CharField(required=False)
    cell_phone = forms.CharField(label='Cell Phone', required=False)
    work_phone = forms.CharField(label='Work Phone', required=False)
    home_phone = forms.CharField(label='Home Phone', required=False)
    

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'address', 'cell_phone', 'work_phone', 'home_phone']

class ProfileChangeForm(forms.ModelForm):
    #Form for updating users.  Replaces pasword field with admin's password hash display field.

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'address', 'cell_phone', 'work_phone', 'home_phone']



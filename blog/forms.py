from django import forms
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
class RegForm(forms.Form):

    username=forms.CharField(min_length=5,
                             max_length=12,
                             widget=forms.TextInput(attrs={"class":"form-control","placeholder":"username"}))


    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"password"}))

    repeat_password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"password"}))

    email=forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control","placeholder":"email"}))

    valid_code=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"valid_code"}))


    def __init__(self,request,*args,**kwargs):

        super(RegForm,self).__init__(*args,**kwargs)
        self.request=request


    # def clean_password(self):  #  关于密码字段的钩子
    #
    #     if len(self.cleaned_data["password"])>8:
    #         return self.cleaned_data["password"] # sadfsad234532
    #     else:
    #         raise ValidationError("密码小于8位！")
    #
    # def clean_username(self):
    #
    #     if self.cleaned_data["username"].isdigit() or self.cleaned_data["username"].isalpha():
    #         raise ValidationError("用户名必须包含数字与字母！")
    #     else:
    #         return self.cleaned_data["username"]
    #
    #
    #
    # def clean_valid_code(self):
    #     if self.cleaned_data["valid_code"].upper() ==self.request.session["valid_code"].upper():
    #         return self.cleaned_data["valid_code"]
    #
    #
    #     else:
    #         raise ValidationError("验证码错误！")





    # def clean(self):
    #     if self.cleaned_data["password"]==self.cleaned_data["repeat_password"]:
    #         return self.cleaned_data
    #
    #     else:
    #         raise ValidationError("密码不一致")


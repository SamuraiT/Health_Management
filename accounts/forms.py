from django import forms
from allauth.account.forms import SignupForm

class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='FIRST NAME')
    last_name = forms.CharField(max_length=30, label='LAST NAME')
    age = forms.IntegerField(label='age')
    height = forms.FloatField(label='Height')
    weight = forms.FloatField(label='Taget Weight')


class SignupUserForm(SignupForm):
    #メールアドレスとパスワードは、allauthですでに設定してあるため必要なし
    first_name = forms.CharField(max_length=30, label='FIRST NAME')
    last_name = forms.CharField(max_length=30, label='LAST NAME')
    email = forms.EmailField(max_length=30, label='EMAIL')
#    age = forms.IntegerField(label='age')
#    height = forms.FloatField(label='height')
#    weight = forms.FloatField(label='weight')

    def save(self, request):
        user = super(SignupUserForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
#        user.age = self.cleaned_data['age']
#        user.height = self.cleaned_data['height']
#        user.weight = self.cleaned_data['weight']
        user.save()

        return user
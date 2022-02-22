from django.contrib.auth.forms import AuthenticationForm

class formLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(formLogin,self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class UserCreationForm(UserCreationForm):

    count2field = ['username', 'email', 'password', 'password(confirm)']

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        count = 0
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = self.count2field[count]
            count += 1
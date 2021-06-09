from django.forms import *
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import *

class ProviderForm(ModelForm):
    class Meta:
        model = Provider
        fields = "__all__"
        exclude = ['user','status']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save person'))

class DealerForm(ModelForm):
    class Meta:
        model = Dealer
        fields = "__all__"
        exclude = ['user','provider']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save person'))

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        exclude = ['provider']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save person'))

class CodeForm(ModelForm):
    class Meta:
        model = Code
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save person'))

class NumberForm(ModelForm):
    class Meta:
        model = Number
        fields = "__all__"
        exclude = ['status']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save person'))

class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = "__all__"
        exclude = ['number']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save person'))

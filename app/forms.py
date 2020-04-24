from django import forms
from app.models import *
from django_select2.forms import Select2MultipleWidget

class productForm(forms.ModelForm):
    class Meta:  
        model = product
        fields = "__all__"
  
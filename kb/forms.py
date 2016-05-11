import tinymce.widgets
from django import forms
from djangoformsetjs.utils import formset_media_js
import kb.models

from django_select2.forms import ModelSelect2MultipleWidget, ModelSelect2Widget, ModelSelect2Mixin, Select2Widget, HeavySelect2Widget


class DepartamentWidget(ModelSelect2MultipleWidget):
    search_fields = [
        'name__icontains',
    ]

class InstructionsWidget(ModelSelect2MultipleWidget):
    search_fields = [
        'name__icontains',
    ]


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    json_file = forms.FileField()


class UserManual(forms.ModelForm):
    class Meta:
        model = kb.models.UserManual
        fields = ('name', 'description', 'instructions',)
        widgets = {
            'name': HeavySelect2Widget(attrs={'style': 'width:100%'}, data_url='/kb_name/', choices=()),
            'description': tinymce.widgets.TinyMCE(attrs={'style': 'width:100%'}),
            'instructions': InstructionsWidget(attrs={'style': 'width:100%'})
        }

    class Media:
        js = ('kb/js/select2_options.js',)

    def __init__(self, *args, **kwargs):
        super(UserManual, self).__init__(*args, **kwargs)
        if self.instance.id:
            self.fields['name'].widget = forms.TextInput()
        self.fields['name'].choices = ((val, val) for val in kb.models.KbUserManualName.objects.values_list('kb_name', flat=True))

    def save(self, commit=True):
        instance = super(UserManual, self).save(commit)
        instance.view_path = kb.models.KbUserManualName.objects.get(kb_name=instance.name).view_path
        instance.save()
        return instance


class Instruction(forms.ModelForm):
    usermanuals = forms.ModelMultipleChoiceField(queryset=kb.models.UserManual.objects.all())

    class Meta:
        model = kb.models.Instruction
        fields = ('name',  'departaments', 'usermanuals', 'file')
        widgets = {
            'departaments': DepartamentWidget(attrs={'style': 'width:300px'}),
            'usermanuals': ModelSelect2MultipleWidget(search_fields=['name__icontains'],attrs={'style': 'width:300px'}),
        }

    def save(self, commit=True):
        instance = super(Instruction, self).save(commit)
        print(self.cleaned_data['usermanuals'])
        setattr(instance, 'usermanuals', self.cleaned_data['usermanuals'])
        return instance

class Departament(forms.Form):
    app = forms.ModelChoiceField(
        label='Приложение',
        queryset=kb.models.App.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    departament = forms.ModelChoiceField(label='Отдел', queryset=kb.models.Departament.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    usermanual = forms.CharField(label='Название', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название справки'}))


class InstructionSearch(forms.Form):
    departament = forms.ModelChoiceField(label='Отдел', queryset=kb.models.Departament.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    instruction = forms.CharField(label='Название', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название инструкции'}))


from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
class CustomAuthenticationForm(AuthenticationForm):
    """
    Переопределяю класс чтобы добавить в input класс form-control
    """
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

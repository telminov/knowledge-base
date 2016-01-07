import tinymce.widgets
from django import forms
from djangoformsetjs.utils import formset_media_js
import kb.models

from django_select2.forms import ModelSelect2MultipleWidget


class DepartamentWidget(ModelSelect2MultipleWidget):
    search_fields = [
        'name__icontains',
    ]


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    json_file = forms.FileField()


# class KbCollection(forms.ModelForm):
#     class Meta:
#         model = kb.models.KbCollection
#         fields = ('name',)


class UserManual(forms.ModelForm):
    class Meta:
        model = kb.models.UserManual
        fields = ('name', 'view_path', 'departaments', 'description')
        widgets = {
            'departaments': DepartamentWidget(attrs={'style': 'width:100%'}),
            'description': tinymce.widgets.TinyMCE(attrs={'style': 'width:100%'})
        }


class Instruction(forms.ModelForm):

    class Meta:
        model = kb.models.Instruction
        fields = ('name',  'departaments', 'file')
        exclude = ('usermanuals',)
        widgets = {
            'departaments': DepartamentWidget(attrs={'style': 'width:300px'}),
        }

    class Media:
        js = formset_media_js


class Departament(forms.Form):
    departament = forms.ModelChoiceField(label='Департамент', queryset=kb.models.Departament.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    usermanual = forms.CharField(label='Название', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название мануала'}))


class InstructionSearch(forms.Form):
    departament = forms.ModelChoiceField(label='Департамент', queryset=kb.models.Departament.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    instruction = forms.CharField(label='Название', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название инструкции'}))

ManualInstructionsFormSet = forms.inlineformset_factory(kb.models.UserManual, kb.models.Instruction, form=Instruction, extra=0)
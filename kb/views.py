from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.utils.encoding import smart_text
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin

import kb.models
import kb.forms


def create_kb_collection(form, json_file):
    """
    Структура kb_json:
        {
            crm_view_name: {
                'view_path': view_path,
                'kb_name': kb_name
            }
        }
    :param json_file:
    :return:
    """

    chunks = list(json_file.chunks())
    json_str = ''.join([chunk.decode('utf-8') for chunk in chunks])
    kb_collection = kb.models.KbCollection.objects.create(
        kb_json=json_str,
        file=json_file,
        name=form.cleaned_data.get('title')
    )
    kb_collection.save()
    return kb_collection

#
# class KbCollectionList(ListView):
#     queryset = kb.models.KbCollection.objects.all()
#     template_name = 'kb/collection_list.html'
# kb_collection_list = KbCollectionList.as_view()
#
#
# class KbCollectionEdit(DetailView):
#     #TODO нужна вьюха?
#     context_object_name = 'kb_collection'
#     pk_url_kwarg = 'kb_collection_id'
#     model = kb.models.KbCollection
#     template_name = 'kb/collection_edit.html'
#
#     def post(self, request, *args, **kwargs):
#         if 'create_usermanuals' in request.POST:
#             kb_collection = self.get_object()
#             return redirect(reverse('kb:collection_edit', kwargs={'kb_collection_id': kb_collection.id}))
# kb_collection_edit = KbCollectionEdit.as_view()


class InstructionCreate(CreateView):
    model = kb.models.Instruction
    form_class = kb.forms.Instruction
    template_name = 'kb/instruction_edit.html'
    success_url = reverse_lazy('kb:instruction_list')
instruction_add = InstructionCreate.as_view()


class InstructionUpdate(UpdateView):
    model = kb.models.Instruction
    form_class = kb.forms.Instruction
    template_name = 'kb/instruction_edit.html'
    success_url = reverse_lazy('kb:instruction_list')


    def get_form_kwargs(self):
        kwargs= super(InstructionUpdate, self).get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
            kwargs['initial']['usermanuals'] = self.object.usermanuals.all()
        return kwargs
instruction_edit = InstructionUpdate.as_view()


class InstructionDelete(DeleteView):
    model = kb.models.Instruction
    form_class = kb.forms.Instruction
    template_name = 'kb/confirm_delete.html'
    success_url = reverse_lazy('kb:instruction_list')
instruction_delete = InstructionDelete.as_view()


class InstructionList(FormMixin, ListView):
    model = kb.models.Instruction
    template_name = 'kb/instruction_list.html'
    form_class = kb.forms.InstructionSearch

    def get_queryset(self):
        self.queryset = super(InstructionList, self).get_queryset()
        form = self.get_form()
        if form.is_valid():
            if form.cleaned_data.get('instruction'):
                self.queryset = self.queryset.filter(name__icontains=form.cleaned_data.get('instruction'))

            if form.cleaned_data.get('instruction'):
                self.queryset = self.queryset.filter(name__icontains=form.cleaned_data.get('instruction'))
            if form.cleaned_data.get('departament'):
                self.queryset = self.queryset.filter(departaments=form.cleaned_data.get('departament'))
        return self.queryset

    def get_form_kwargs(self):
        kwargs = super(InstructionList, self).get_form_kwargs()
        kwargs.update({
                'data': self.request.GET,
                'files': self.request.FILES,
            })
        return kwargs
instruction_list = InstructionList.as_view()


class UserManualView(DetailView):
    pk_url_kwarg = 'user_manual_id'
    model = kb.models.UserManual
    template_name = 'kb/user_manual_view.html'
user_manual_view = UserManualView.as_view()


class UserManualCreate(CreateView):
    pk_url_kwarg = 'user_manual_id'
    model = kb.models.UserManual
    template_name = 'kb/user_manual_edit.html'
    form_class = kb.forms.UserManual
    success_url = reverse_lazy('kb:user_manual_list')

    def get_form_kwargs(self):
        kwargs = super(UserManualCreate, self).get_form_kwargs()
        if self.request.POST.get('name'):
            kwargs['initial'] = {'name': self.request.POST.get('name')}
        return kwargs

    def post(self, request, *args, **kwargs):
        return super(UserManualCreate, self).post(request, *args, **kwargs)
user_manual_add = UserManualCreate.as_view()


class UserManualEdit(UpdateView):
    pk_url_kwarg = 'user_manual_id'
    model = kb.models.UserManual
    template_name = 'kb/user_manual_edit.html'
    form_class = kb.forms.UserManual
    success_url = reverse_lazy('kb:user_manual_list')
user_manual_edit = UserManualEdit.as_view()


class UserManualDelete(DeleteView):
    pk_url_kwarg = 'user_manual_id'
    model = kb.models.UserManual
    # template_name = 'kb/user_manual_edit.html'
    template_name = 'kb/confirm_delete.html'
    form_class = kb.forms.UserManual
    success_url = reverse_lazy('kb:user_manual_list')
user_manual_delete = UserManualDelete.as_view()




class UserManualJson(DetailView):
    slug_field = 'view_path'
    slug_url_kwarg = 'view_path'
    model = kb.models.UserManual

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        um = self.object
        d = {
            'name': um.name,
            'view_path': um.view_path,
            'departaments': list(um.departaments().values_list('name', flat=True)),
            'description': um.description,

        }
        instructions_info = []
        for instruction in um.instructions.all():
            instruction_dict = {
                'name': instruction.name,
                'departments': list(instruction.departaments.values_list('name', flat=True)),
                'file': request.build_absolute_uri(instruction.file.url) if instruction.file else ''
            }
            instructions_info.append(instruction_dict)
        d['instructions'] = instructions_info
        return JsonResponse(d)
user_manual_json = UserManualJson.as_view()

from django.contrib.auth.mixins import LoginRequiredMixin

class UserManualList(LoginRequiredMixin, FormMixin, ListView):
    queryset = kb.models.UserManual.objects.all()
    template_name = 'kb/user_manual_list.html'
    form_class = kb.forms.Departament
    login_url = '/login/'

    def get_queryset(self):
        self.queryset = super(UserManualList, self).get_queryset()
        form = self.get_form()
        if form.is_valid():
            if form.cleaned_data.get('app'):
                self.queryset = self.queryset.filter(view_path__startswith=form.cleaned_data.get('app').code)
            if form.cleaned_data.get('usermanual'):
                self.queryset = self.queryset.filter(name__icontains=form.cleaned_data.get('usermanual'))
            if form.cleaned_data.get('departament'):
                self.queryset = self.queryset.filter(instructions__departaments=form.cleaned_data.get('departament')).distinct()
        return self.queryset

    def get_form_kwargs(self):
        kwargs = super(UserManualList, self).get_form_kwargs()
        kwargs.update({
                'data': self.request.GET,
                'files': self.request.FILES,
            })
        return kwargs
user_manual_list = UserManualList.as_view()

class KbNameList(ListView):
    queryset = kb.models.KbUserManualName.objects.all()
    
    def get(self, request, *args, **kwargs):
        self.term = kwargs.get('term', request.GET.get('term', ''))
        self.object_list = self.get_queryset()
        apps_dict = dict(kb.models.App.objects.values_list('code', 'name'))
        r = defaultdict(list)
        r = dict()
        for kb_name in self.object_list:
            app_code = kb_name.view_path.split('.')[0]
            item_data = {'text': smart_text(kb_name.kb_name), 'id': smart_text(kb_name.kb_name), 'view_path': kb_name.view_path}
            has_user_manuals = kb.models.UserManual.objects.filter(view_path=kb_name.view_path).exists()
            if has_user_manuals:
                item_data['disabled'] = 'true'
            if app_code in apps_dict:
                if apps_dict[app_code] not in r:
                    r.setdefault(apps_dict[app_code], [])
                r[apps_dict[app_code]].append(item_data)
            else:
                r[kb_name.kb_name] = item_data
        results = []
        for kb_name_or_group_name, data in r.items():
            if isinstance(data, list):
                results.append({'text': kb_name_or_group_name, 'children': data})
            else:
                results.append(data)
        return JsonResponse({
            'results': results
        })
kb_name_list_json = KbNameList.as_view()


class UploadCollection(FormView):
    form_class = kb.forms.UploadFileForm
    template_name = 'kb/upload_json.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            kb.models.KbUserManualName.load_from_json(request.FILES['json_file'])
            return redirect(reverse('admin:index'))
            # c['kb_collection'] = kb_collection
            # return redirect(reverse('kb:collection_edit', args=(kb_collection.id,)))
        return render(request, self.template_name, {'form': form})

    def get_form_kwargs(self):
        kwargs = super(UploadCollection, self).get_form_kwargs()
        return kwargs

upload = UploadCollection.as_view()


# @login_required(login_url='/admin/login/') #TODO сделать,когда научусь конектиться remote
def schema(request):
    result = {}
    for um in kb.models.UserManual.objects.all():
        result[um.view_path] = request.build_absolute_uri(reverse('kb:user_manual_view', args=(um.id,)))
    response = JsonResponse(result)
    # response['CONTENT-DISPOSITION'] = 'attachment; filename=kb_links.json'
    return response
import json
import datetime
from django.core.exceptions import ValidationError

from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe


def upload_json(instance, filename):
    now = datetime.datetime.now()
    filename = '{0}_{1}'.format(now.strftime('%Y-%m-%d_%H-%M_%s'), filename)
    return filename


class KbUserManualName(models.Model):
    kb_name = models.CharField(max_length=255)
    view_path = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Название справки'
        verbose_name_plural = 'Названия справок'

    def __str__(self):
        return '%s ^ %s' % (self.kb_name, self.view_path)
        # return '%s' % self.kb_name

    @staticmethod
    def load_from_json(json_file):
        chunks = list(json_file.chunks())
        json_str = ''.join([chunk.decode('utf-8') for chunk in chunks])
        json_as_dict = json.loads(json_str.encode('unicode_escape').decode('utf8'))
        for view_path, data in json_as_dict.items():
            kb_name = data.get('kb_name')
            kb_user_manual_name, created = KbUserManualName.objects.get_or_create(view_path=view_path)
            kb_user_manual_name.kb_name = kb_name
            kb_user_manual_name.save(0)


class App(models.Model):
    name = models.CharField('Имя приложения', max_length=255, help_text='Никакой доп инфы нету')
    code = models.CharField('На латинице как во вьюхе', max_length=255)
    class Meta:
        verbose_name = 'Приложение'
        verbose_name_plural = 'Приложения'

    def __str__(self):
        return '%s' % self.name


class Departament(models.Model):
    name = models.CharField('Отдел (департамент)', max_length=255, help_text='Департамент, которых касается инструкция')
    color = models.CharField('Цвет из bootstrap', max_length=255, blank=True)
    apps = models.ManyToManyField(App, verbose_name=u'Приложения', help_text='Приложения с которыми работает отдел', blank=True)

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'

    def __str__(self):
        return '%s' % self.name

    def as_html_label(self):
        return mark_safe("<span class='label label-{color}'>{name}</span>".format(color=self.color, name=self.name))

    def as_search_button_usermanuals(self):
        url = reverse('kb:user_manual_list') + '?departament=%s' % self.id
        return mark_safe("<a href={href} class='btn btn-xs btn-{color}'>{name}</a>".format(color=self.color, name=self.name, href=url))

    def as_search_button_instructions(self):
        url = reverse('kb:instruction_list') + '?departament=%s' % self.id
        return mark_safe("<a href={href} class='btn btn-xs btn-{color}'>{name}</a>".format(color=self.color, name=self.name, href=url))


class UserManual(models.Model):
    name = models.CharField('Название', max_length=255, help_text='Названия предзагружаются из МИС ММ. Если справка уже создана, то ее название выбрать нельзя')
    view_path = models.CharField('view path в проекте', max_length=255, blank=True)
    instructions = models.ManyToManyField('Instruction', verbose_name=u'Пользовательские инструкции', related_name='usermanuals', null=True, blank=True)
    description = models.TextField('Описание', blank=True)
    dm = models.DateTimeField('Дата модификации', auto_now=True)

    def departaments(self):
        departments_ids = set()
        for instruction in self.instructions.all():
            departments_ids.update(instruction.departaments.values_list('id', flat=True))

        return Departament.objects.filter(id__in=departments_ids)

    def get_app(self):
        app = App.objects.filter(code=self.view_path.split('.')[0])[0]
        return app.name if app else ''

    def get_absolute_url(self):
        return reverse('kb.views.user_manual_edit', args=(self.id,))

    class Meta:
        verbose_name = 'Справка'
        verbose_name_plural = 'Справки'

    def __str__(self):
        return '%s' % self.name


def validate_file_extension(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError('Только pdf файлы')


class Instruction(models.Model):
    name = models.CharField('Название', max_length=255)
    departaments = models.ManyToManyField(Departament, verbose_name=u'Отделы', blank=True)
    url = models.URLField('Ссылка на googledocs', blank=True)
    file = models.FileField('Файл', blank=True, validators=[validate_file_extension])
    class Meta:
        verbose_name = 'Пользовательская инструкция'
        verbose_name_plural = 'Пользовательские инструкции'

    def __str__(self):
        return '%s' % self.name


class Document(models.Model):
    name = models.CharField('Название', max_length=255)
    url = models.URLField('Ссылка на googledocs', blank=True)
    file = models.FileField('Файл', blank=True, validators=[validate_file_extension])

    def __str__(self):
        file_or_url = self.url or self.file.url
        file_or_url = file_or_url[:30]
        return '%s [%s]' % (self.name, file_or_url)

    def get_file_id(self):
        index = self.url.rfind('id=')
        assert not (index == -1), 'id= Не найдено в ссылке %s' % self.url
        return self.url[index+3:]

    def pdf_link(self):
        return self.url
        file_id = self.get_file_id()
        file = settings.GOOGLE_DOC_SERVICE.files().get(fileId=file_id).execute()
        if 'exportLinks' in file:
            print(file['exportLinks']['application/pdf'])
            return file['exportLinks']['application/pdf']
        else:
            print("NO EXPORT LINKS")
            return 'no pdf'


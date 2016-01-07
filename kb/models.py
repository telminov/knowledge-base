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


# class KbCollection(models.Model):
#     """ Хранение истории загруженных файлов за время работы программы.
#     """
#     name = models.CharField(u'Название загруженного файла', max_length=255, unique=True)
#     kb_json = models.TextField(u'Текст json из проекта')
#     dc = models.DateTimeField(u'Время загрузки', auto_now_add=True)
#     file = models.FileField(u'Файл json', upload_to=upload_json, blank=True)
#
#     class Meta:
#         verbose_name = u'Загруженные json файлы'
#         verbose_name_plural = u'Загруженные json файлы'
#         ordering = ('-dc', )
#
#     def __str__(self):
#         return '%s | %s' % (self.dc, self.kb_json[:15])
#
#     def get_dictionary(self):
#         d_info = json.loads(self.kb_json.encode('unicode_escape').decode('utf8'))
#         for view_path, kb_info in d_info.items():
#             # view_path = kb_info.get('view_path')
#             url = kb_info.get('url')
#             if view_path:
#                 user_manuals = UserManual.objects.filter(view_path=view_path)
#                 kb_info['user_manuals'] = user_manuals
#                 if user_manuals:
#                     kb_info['id'] = user_manuals.first().id
#         return d_info


class App(models.Model):
    name = models.CharField('Имя приложения', max_length=255, help_text='Никакой доп инфы нету')

    class Meta:
        verbose_name = 'Приложение'
        verbose_name_plural = 'Приложения'

    def __str__(self):
        return '%s' % self.name


class Departament(models.Model):
    name = models.CharField('Департамент', max_length=255, help_text='Департамент, которых касается инструкция')
    color = models.CharField('Цвет из bootstrap', max_length=255, blank=True)
    apps = models.ManyToManyField(App, verbose_name=u'Приложения', help_text='Приложения с которыми работает департамент', blank=True)

    class Meta:
        verbose_name = 'Департамент'
        verbose_name_plural = 'Департаменты'

    def __str__(self):
        return '%s' % self.name

    def as_html_label(self):
        return mark_safe("<span class='label label-{color}'>{name}</span>".format(color=self.color, name=self.name))

    def as_html_href(self):
        url = reverse('kb:user_manual_list') + '?departament=%s' % self.id
        return mark_safe("<a href={href} class='btn btn-xs btn-{color}'>{name}</a>".format(color=self.color, name=self.name, href=url))


class UserManual(models.Model):
    # DEPARTAMENT_CHOICES = (
    #     ('Регистраторы','Регистраторы'),
    #     ('Менеджеры','Менеджеры'),
    #     ('Проф департамент','Проф департамент'),
    #     ('Аналитика','Аналитика'),
    #     ('Контроль качества','Контроль качества'),
    # )
    name = models.CharField('Название', max_length=255, help_text='Копируется из kb_name')
    view_path = models.CharField('view path в проекте', max_length=255, blank=True)
    departaments = models.ManyToManyField(Departament, verbose_name=u'Отделы', blank=True)
    description = models.TextField('Описание', blank=True)
    dm = models.DateTimeField('Дата модификации', auto_now=True)

    def get_absolute_url(self):
        return reverse('kb.views.user_manual_edit', args=(self.id,))

    class Meta:
        verbose_name = 'Мануал'
        verbose_name_plural = 'Мануалы'

    def __str__(self):
        return '%s' % self.name


def validate_file_extension(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError('Только pdf файлы')


class Instruction(models.Model):
    name = models.CharField('Название', max_length=255)
    departaments = models.ManyToManyField(Departament, verbose_name=u'Отделы', blank=True)
    # document = models.OneToOneField('Document', verbose_name=u'Документ', blank=True, null=True)
    manual = models.ForeignKey(UserManual, verbose_name=u'Мануал', related_name='instructions', blank=True, null=True)
    url = models.URLField('Ссылка на googledocs', blank=True)
    file = models.FileField('Файл', blank=True, validators=[validate_file_extension])
    class Meta:
        verbose_name = 'Инструкция'
        verbose_name_plural = 'Инструкции'

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


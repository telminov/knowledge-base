__author__ = 'g10k'

"""Потом убрать в миграции"""
    #     ('Регистраторы','Регистраторы'),
    #     ('Менеджеры','Менеджеры'),
    #     ('Проф департамент','Проф департамент'),
    #     ('Аналитика','Аналитика'),
    #     ('Контроль качества','Контроль качества'),
import kb.models

departaments = {
    'Регистраторы': {
        'apps': ['lmk', 'prof'],
        'color': 'blue',
    },
    'Менеджеры': {
        'apps': ['crm', 'out'],
        'color': 'green'
    },
    'Проф департамент': {
        'apps': ['prof', 'crm', 'out'],
        'color': 'purple',
    },
    'Аналитики': {
        'apps': ['analytic', 'crm', 'lmk', 'prof'],
        'color': 'red'
    },
    'Контроль качества': {
        'apps': ['qq'],
        'color': 'pink'
    }
}


def fill_departaments():
    set_apps = set()
    for department_name, info in departaments.items():
        for app in set_apps:
            kb.models.App.objects.get_or_create(name=app)
        apps = info.get('apps')
        color = info.get('color')
        departament, created = kb.models.Departament.objects.get_or_create(name=department_name)
        app_objects = kb.models.App.objects.filter(name__in=apps)
        departament.apps.set(app_objects, clear=True)
        departament.color = color
        departament.save()

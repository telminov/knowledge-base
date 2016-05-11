import json
from django.core.management.base import BaseCommand
import kb.models

from django.conf import settings
# setings.KB_NAME_FILE_PATH = '/home/g10k/git/knowledge_base/kb_links.json'

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        json_file = open(settings.KB_NAME_FILE_PATH, 'r')

        json_str = ''.join([line for line in json_file.readlines()])
        json_as_dict = json.loads(json_str)
        for view_path, data in json_as_dict.items():
            kb_name = data.get('kb_name')
            kb_user_manual_name, created = kb.models.KbUserManualName.objects.get_or_create(view_path=view_path)
            kb_user_manual_name.kb_name = kb_name
            kb_user_manual_name.save()


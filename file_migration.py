import os
from django.conf import settings
from shutil import copyfile

#https://lalasol-bootcamp-backend-production.up.railway.app
# def run():
#     base_dir = settings.BASE_DIR
#     media_dir = os.path.join(base_dir,'project_name/media')

#     for file in Files.objects.all():
#         old_file_path = os.path.join(media_dir, file.image.name)
#         dir_name = '/{}-{}/{}-{}/'.format(file.theme,file.name,file.id, file.name)
#         if not os.path.exists(os.path.join(media_dir, dir_name)):
#             os.makedirs(os.path.join(media_dir, dir_name))
#         new_file_name = '/{}-{}/{}-{}/{}-{}.txt'.format(file.theme,file.name,file.id, file.name, file.id, file.name)
#         new_file_path = os.path.join(media_dir, new_file_name)
#         copyfile(old_file_path, new_file_path)
#         file.image.url = new_file_name
#         file.save()
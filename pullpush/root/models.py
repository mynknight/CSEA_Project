from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# from django.db.models.signals import pre_delete
# from django.dispatch import receiver
# import os

# def delete_file(instance, **kwargs):
#     if instance.file:
#         if os.path.isfile(instance.file.path):
#             os.remove(instance.file.path)

# @receiver(pre_delete, sender=User)
# def delete_files(sender, instance, **kwargs):
#     for blog_post in instance.blogpost_set.all():
#         delete_file(blog_post)


class AllFiles(models.Model):
    owner= models.ForeignKey(User, on_delete=models.CASCADE)
    title= models.CharField(max_length=100)
    file=models.FileField(upload_to='all_files/', default='')
    caption=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True,)

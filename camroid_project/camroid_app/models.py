# Create your models here.
from PIL import Image
from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

class CategoryList(models.Model):
    Category = models.CharField(max_length=200)
    Cat_Img = models.ImageField(upload_to='cat_media')
    Active = models.BooleanField(default=True)

    def __str__(self):
        return self.Category


class ImgDetails(models.Model):
    Img = models.ImageField(upload_to='media')
    Category = models.ForeignKey(CategoryList, default=1, on_delete=models.SET_DEFAULT, null=False)
    keywords = models.CharField(max_length=255)
    User = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    Valid = models.BooleanField(default=False)
    UploadDate = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        self.Img.delete()
        super().delete(*args, **kwargs)

    def image_tag(self):
        return mark_safe('<img src="{}" width=45px; height=45px;/>'.format(self.Img.url))
        
    image_tag.allow_tags = True
       
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_img = models.ImageField(upload_to='ProfileImg', default='ProfileImg/default-avatar.png')

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.profile_img.path)
        if img.height > 300 or img.width > 400:
            output_size = (300,400)
            img.thumbnail(output_size)
            img.save(self.profile_img.path)


    def get_profile_picture(self):
        if self.profile_img:
            return self.profile_img
        else:
            return 'ProfileImg/default-avatar.png'

    # def delete(self, *args, **kwargs):
    #     self.profile_img.delete()
    #     super().delete(*args, **kwargs)
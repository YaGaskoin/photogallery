import hashlib
from django.db import models
from sorl.thumbnail import get_thumbnail
from django.contrib.auth.models import User


class Image(models.Model):

    THUMBNAIL_S = ('100x100', 70)
    THUMBNAIL_M = ('300x200', 80)
    THUMBNAIL_L = ('500x500', 95)

    user = models.ForeignKey(User, verbose_name='Пользователь', related_name='images',on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Изображение',
                              upload_to='images/',
                              blank=True, null=True)
    image_md5 = models.CharField(verbose_name='Хэш изображения', blank=True,
                                 default='', max_length=63,
                                 help_text='Заполняется автоматически')

    def image_hash(self):
        """ Получение хэша картинки """
        md5 = self.image_md5
        if not md5:
            md5 = self.calc_image_hash(save=False)
        return md5

    def calc_image_hash(self, save=True):
        """ Вычисление хэша картинки """
        self.image_md5 = ""
        if self.image:
            self.image_md5 = hashlib.md5(self.image.read()).hexdigest()
        if save:
            self.save(update_fields=['image_md5'])
        return self.image_md5

    def save_with_hash(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.calc_image_hash()

    def get_thumbnail(self, props):
        """
        Получение миниатюры

        props - кортеж из двух элементов (размер миниатюры, качество)
        """
        if self.image:
            size, quality = props
            return get_thumbnail(
                self.image,
                size,
                quality=quality)

    @property
    def image_s(self):
        # return self.get_thumbnail(self.THUMBNAIL_S)
        return self.image

    @property
    def image_m(self):
        # return self.get_thumbnail(self.THUMBNAIL_M)
        return self.image

    @property
    def image_l(self):
        # return self.get_thumbnail(self.THUMBNAIL_L)
        return self.image



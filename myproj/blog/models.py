from django.db import models
from django.utils import timezone
from .extensions.utils import convert_to_jalali


class CategoryManager(models.Manager):
    def available(self):
        return self.filter(status=True)


class Category(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='لینک')
    thumbnail = models.ImageField(upload_to='categories/images', verbose_name='تصویر اصلی', blank=True)
    position = models.SmallIntegerField(verbose_name='ترتیب')
    status = models.BooleanField(default=True, verbose_name='فعال باشد؟')
    
    objects = CategoryManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'
        ordering = ['position']
    


class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='p')


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'پیش‌نویس'),
        ('p', 'منتشرشده'),
    )

    title = models.CharField(max_length=200, verbose_name='عنوان')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='لینک')
    description = models.TextField(verbose_name='متن')
    thumbnail = models.ImageField(upload_to='articles/images', verbose_name='تصویر اصلی')
    category = models.ManyToManyField(Category, related_name='articles', verbose_name='دسته‌بندی')
    published = models.DateTimeField(default=timezone.now, verbose_name='زمان انتشار')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='وضعیت')

    objects = ArticleManager()

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'مطلب'
        verbose_name_plural = 'مطالب'
        ordering = ['-published']

    def jpublished(self):
        return convert_to_jalali(self.published)
    jpublished.short_description = published.verbose_name
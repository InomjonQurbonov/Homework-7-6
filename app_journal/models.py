from django.contrib.auth import get_user_model
from django.db import models
from ckeditor.fields import RichTextField


class Category(models.Model):
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "Categories"
        db_table = "category"


class News(models.Model):
    news_title = models.CharField(max_length=255)
    news_description = RichTextField()
    news_image = models.ImageField(upload_to='news/')
    news_content = RichTextField()
    news_date = models.DateTimeField(auto_now_add=True)
    news_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    news_views_count = models.IntegerField(default=0)
    news_author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.news_title

    class Meta:
        verbose_name_plural = "News"
        db_table = "news"

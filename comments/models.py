from django.db import models
from recipes.models import Recipe
from django.contrib.auth.models import User

# Create your models here.
class Comments(models.Model):
    title_comment = models.CharField(max_length=255, verbose_name='Título do comentário:')
    email_comment = models.EmailField(verbose_name='E-mail:')
    comment = models.TextField(verbose_name='Comentário:')
    recipe_comment = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    datatime_comment = models.DateTimeField(auto_now_add=True)
    published_comment = models.BooleanField(default=False)

    def __str__(self):
        return self.title_comment
    
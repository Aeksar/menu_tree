from django.db import models
from django.urls import reverse, NoReverseMatch

class MenuItem(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    menu_name = models.CharField(max_length=100, verbose_name='Имя')
    url = models.CharField(max_length=200, blank=True, verbose_name='Имя')
    named_url = models.CharField(max_length=100, blank=True, verbose_name='Имя')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children', verbose_name='Имя')
    position = models.PositiveIntegerField(default=0, verbose_name='Имя')

    class Meta:
        ordering = ['position']
        unique_together = ['menu_name', 'name']
        verbose_name = 'Объект меню'
        verbose_name_plural = 'Объекты меню'

    def __str__(self):
        return f"{self.menu_name}: {self.name}"

    def get_url(self):
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                return self.url
        return self.url
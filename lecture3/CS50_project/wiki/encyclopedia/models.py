from django.db import models

# Create your models here.
class MarkdownContent(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    class Meta:
      verbose_name_plural = "Markdown content"

    def __str__(self):
      return self.title
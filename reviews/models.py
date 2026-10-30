
from django.db import models
from django.conf import settings
from perfumes.models import Perfume


class Review(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    perfume = models.ForeignKey(
        Perfume,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.PositiveIntegerField(
        choices=[
            (1, '1 Star'),
            (2, '2 Stars'),
            (3, '3 Stars'),
            (4, '4 Stars'),
            (5, '5 Stars'),
        ]
    )

    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'perfume'],
                name='unique_user_perfume_review'
            )
        ]

    def __str__(self):
        return f'{self.user} - {self.perfume.name}'
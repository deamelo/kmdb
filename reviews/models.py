from unittest.mock import DEFAULT
from django.db import models

class RecomendationOptions(models.TextChoices):
    MUST_WATCH = "Must Watch"
    SHOLD_WATCH = "Should Watch"
    AVOID_WATCH = "Avoid Watch"
    DEFAULT = "No Opinion"


class Review(models.Model):
    stars = models.IntegerField()
    review = models.TextField()
    spoilers = models.BooleanField(null=True, blank=True, default=False)
    recomendation = models.CharField(max_length=50, choices=RecomendationOptions.choices, default=RecomendationOptions.DEFAULT)

    user = models.ForeignKey("accounts.Account", on_delete=models.CASCADE, related_name="reviews")
    movie = models.ForeignKey("movies.Movie", on_delete=models.CASCADE, related_name="reviews")

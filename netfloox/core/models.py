from django.db import models


class Films(models.Model):
    tconst = models.CharField(max_length=12, blank=True, null=True)
    originaltitle = models.CharField(max_length=450, blank=True, null=True)
    runtimeminutes = models.FloatField(blank=True, null=True, default=0.0)
    averagerating = models.FloatField(blank=True, null=True, default=0.0)
    numvotes = models.IntegerField(blank=True, null=True)
    movie_features = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['originaltitle']),]

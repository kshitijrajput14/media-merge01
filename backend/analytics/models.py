from django.db import models
from django.utils import timezone

class UserWatchHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('core.UserProfile', on_delete=models.CASCADE, related_name='watch_history')
    asset = models.ForeignKey('assets.MediaAsset', on_delete=models.CASCADE, related_name='watch_history')
    last_playback_position_seconds = models.IntegerField(default=0)
    total_duration_seconds = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_watch_history'
        unique_together = ('user', 'asset')
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.full_name} -> {self.asset.title} ({self.last_playback_position_seconds}s)"


class UserRatingReview(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('core.UserProfile', on_delete=models.CASCADE, related_name='reviews')
    asset = models.ForeignKey('assets.MediaAsset', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()  # 1 to 5
    review_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'user_ratings_reviews'
        unique_together = ('user', 'asset')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.full_name} -> {self.asset.title} ({self.rating}/5)"


class Recommendation(models.Model):
    recommendation_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('core.UserProfile', on_delete=models.CASCADE, related_name='recommendations')
    asset = models.ForeignKey('assets.MediaAsset', on_delete=models.CASCADE, related_name='recommendations')
    score = models.DecimalField(max_digits=4, decimal_places=3, default=0.850)
    recommendation_algorithm = models.CharField(max_length=80, default='CollaborativeFiltering+GenreMatch')
    generated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'recommendations'
        unique_together = ('user', 'asset')
        ordering = ['-score']

    def __str__(self):
        return f"{self.user.full_name} -> {self.asset.title} (Score: {self.score})"

from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'users'

    def __str__(self):
        return self.username


class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column='user_id', related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'posts'

    def __str__(self):
        return self.title

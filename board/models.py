from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, null=False, on_delete=models.CASCADE, related_name="comments")
    # models.ForeignKey의 related_name : 역참조 할 때 사용 (정참조, 역참조에 대해 검색해보시는 것을 추천합니당 :D)
    comment = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
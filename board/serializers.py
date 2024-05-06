from django.utils import timezone
from rest_framework import serializers

from .models import Post, Comment

# 게시글 작성/수정 시 request 객체로써 사용 : title, body만 받아옴
class PostRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'body']

# 전체 게시글 조회 시 response 객체로서 사용 : id, title, body만 return하면 됨
class PostSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'body']

# 게시글 작성/수정/삭제 후 return 시 response 객체로서 사용 : Post 모델의 모든 필드 return하면 됨
class PostResponseSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    # 이미 존재하는 필드의 데이터를 변경해서 리턴하려면
    # 변경하려는_필드명 = serializers.SerializerMethodField() 정의

    class Meta:
        model = Post
        fields = '__all__'

    def get_created_at(self, obj): # get_변경하려는_필드명 이라는 함수 안에 데이터를 어떻게 변경할지 정의 후 return
        time = timezone.localtime(obj.created_at)
        return time.strftime('%Y-%m-%d')

# 댓글 작성 시 request 객체로써 사용 : comment만 받아옴
class CommentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment']

# 댓글 목록 조회 시 response 객체로써 사용 : Comment 모델의 모든 필드 return하면 됨
class CommentResponseSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = '__all__'

    def get_created_at(self, obj):
        time = timezone.localtime(obj.created_at) # 처리하는 객체에서 created_at 데이터 뽑아오기
        return time.strftime('%Y-%m-%d')

# 게시글 상세 조회 시 response 객체로써 사용 : Post 모델의 모든 필드 + 해당 Post를 FK로 가지는 모든 Comment return하면 됨
class PostDetailSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    comments = CommentResponseSerializer(many=True, read_only=True)
    # 역참조하려면 아까 정의했던 related_name을 가지는 변수에, 원하는 return값 필드들을 가지는 시리얼라이저를 넣으면 됨
    # 여러 댓글을 시리얼라이저에 넣을 것이기 때문에 many=True
    # 단순히 댓글들을 조회해서 뱉는 역할만 하면 되므로 read_only=True

    class Meta:
        model = Post
        fields = '__all__'

    def get_created_at(self, obj):
        time = timezone.localtime(obj.created_at)
        return time.strftime('%Y-%m-%d')
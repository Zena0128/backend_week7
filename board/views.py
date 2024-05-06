from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Post, Comment
from .serializers import *

# request 파라미터는 우리가 정의한 함수 내에서 사용되지 않더라도 꼭 정의해줘야 함
@api_view(['GET'])
def get_post_list(request):
    posts = Post.objects.all()
    serializer = PostSimpleSerializer(posts, many=True) # 응답용 시리얼라이저에 데이터 보냄
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def post_post(request):
    serializer = PostRequestSerializer(data=request.data) # 들어오는 데이터를 시리얼라이저로 보냄
    if serializer.is_valid():
        post = serializer.save() # save 함수는 객체를 저장해주는 동시에 객체를 return함
        response = PostResponseSerializer(post) # return된 객체를 응답용 시리얼라이저로 보냄
        return Response(response.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_post_detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    serializer = PostDetailSerializer(post) # 응답용 시리얼라이저에 데이터 보냄
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    serializer = PostRequestSerializer(post, data=request.data) # 들어오는 데이터와 원래 데이터 비교해 수정
    if serializer.is_valid():
        updated_post = serializer.save()
        response = PostResponseSerializer(updated_post) # save 함수로부터 return된 객체를 응답용 시리얼라이저로 보냄
        return Response(response.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def create_comment(request, post_id):
    post = Post.objects.get(pk=post_id)
    serializer = CommentRequestSerializer(data=request.data) # 들어오는 데이터를 시리얼라이저로 보냄
    if serializer.is_valid():
        new_comment = serializer.save(post=post)
        response = CommentResponseSerializer(new_comment) # 응답용 시리얼라이저에 데이터 보냄
        return Response(response.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_comments(request, post_id):
    post = Post.objects.get(pk=post_id)
    comments = Comment.objects.filter(post=post)
    # filter 함수 : 조건에 맞는 객체를 필터링해서 가져옴.
    # 1개의 데이터만 가져올 수 있고, 2개 이상이나 0개의 데이터가 탐색되면 에러를 발생시키는 get과 다르게
    # 0개나 여러개의 데이터가 가져와져도 에러 발생시키지 않음
    serializer = CommentResponseSerializer(comments, many=True) # 응답용 시리얼라이저에 데이터 보냄
    return Response(serializer.data, status=status.HTTP_200_OK)
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from MBTIAPP.forms import Signupform,MbtiForm,CommentForm
from .models import Post, Profile, Comment,Category
from .serializers import PostSerializer,CommentSerializer
# from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
def main(request):
    
    return render(request, 'MBTIAPP/main.html')

def detail(request, pk):
    post_detail = get_object_or_404(Post, pk=pk)
    comments = post_detail.comment_set.all()
    context = {
        'post' : post_detail,
        'comments' : comments
    }
    return render(request, 'MBTIAPP/detail.html', context)

def edit(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        post.title=request.POST['title']
        post.content=request.POST['content']
        post.save()  
        return redirect('MBTIAPP:detail', pk)
    else:
        context = {
            'post' : post
        }
        return render(request, 'MBTIAPP/edit.html', context)
    
def delete(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('MBTIAPP:blog')

def blog(request):
    posts = Post.objects.all()
    context = {'posts':posts}
    return render(request, 'MBTIAPP/blog.html', context)

def new(request):
    context={'post':Post.objects.all()}
    return render(request, 'MBTIAPP/postcreate.html',context)

def postcreate(request):
    if(request.method == 'POST'):
        post = Post()
        post.title=request.POST['title']
        post.content=request.POST['content']
        post.poster = request.user
        post.catego=request.POST['category']
        #cate=Category()
        #cate.name=request.POST['category']
        #post.catego=cate.name
        post.save() 
        #cate.save()    
    return redirect('MBTIAPP:blog')

def comment_create(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm()
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.commenter = request.user
                comment.save()
                return redirect('MBTIAPP:detail', pk)
        else:
            form = CommentForm()
        return render(request, 'MBTIAPP/detail.html', {'post':post, 'form': form})



def comment_delete(request, post_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.commenter:
            comment.delete()
    return redirect('MBTIAPP:detail', post_pk) 

def comment_edit(request, post_pk, comment_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment = Comment.objects.get(pk=comment_pk)
    if request.method == 'POST':
            comment.content=request.POST['content']
            comment.save()  
            return redirect('MBTIAPP:detail', post_pk)
    else:
        context = {
            'comment' : comment,
            'post' : post,
            'comment_content' : comment.content
        }
        return render(request, 'MBTIAPP/comment_edit.html', context)   

def mbtitest(request):
    form = MbtiForm()
    return render(request, 'MBTIAPP/mbti_test.html', {'form':form})

def result(request):
    if request.method == 'POST':
        form = MbtiForm(request.POST)
        if form.is_valid():
            EI = form.cleaned_data['EI']
            NS = form.cleaned_data['NS']
            TF = form.cleaned_data['TF']
            PJ = form.cleaned_data['PJ']
            arr=[EI, NS, TF, PJ]
            my_mbti = ''.join(arr)
            user = request.user
            user.user_mbti = my_mbti
            user.save()
            context = {'mymbti':my_mbti}
            return render(request, 'MBTIAPP/result.html', context)
    else:
        form = MbtiForm()
        context = {'form': form}
        return render(request, 'MBTIAPP/result.html',context)



def signup(request):
    if request.method == "POST":
        form = Signupform(request.POST)
        if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('MBTIAPP:main')
    else:
        form = Signupform()
    return render(request, 'MBTIAPP/signup.html', {'form' : form})

#serializer 이용

class PostCreateView(CreateAPIView):
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(poster_id=self.request.user.id)
    
class PostDetailView(APIView):
    
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)


class PostEditView(APIView):
    def put(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDeleteView(APIView):
    def delete(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryClass(APIView):
    def get(self,request,category_id):
        category = get_object_or_404(Category, pk=category_id)
        posts = Post.objects.filter(catego=category)
        if not posts:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)  
    
class PersonalPost(APIView):
    permission_classes = [IsAuthenticated]  # 자기자신
    def get(self, request, format=None):
        profile_id = request.user.id  # 자기자신의 id가져오기
        posts = Post.objects.filter(poster_id=profile_id)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PersonalComment(APIView):
    permission_classes = [IsAuthenticated]  # 자기자신
    def get(self, request, format=None):
        profile_id = request.user.id  # 자기자신의 id가져오기
        comments = Comment.objects.filter(commenter_id=profile_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PeoplePost(APIView):
   def get(self, request, profile_id, format=None):
    posts = Post.objects.filter(poster_id=profile_id)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

          
       
def profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    context = {'profile': profile}
    return render(request, 'MBTIAPP/profile_detail.html', context)

    
from django.shortcuts import render, redirect
from .forms import NoticeBoardPostForm, CommentForm
from .models import *
from django.http import HttpResponse
from accounts.models import Users
from django.core.paginator import Paginator
    
def board(request):
    if request.method == 'POST':

        #print(1)
        #print(request.POST)

        title = request.POST['title']
        content = request.POST['content']
        user = request.session['user_id']
        user_id = Users.objects.get(user_id = user)
        print(user)
        print(user_id)
        #imgfile = request.FILES['imgfile']
        imgfile = request.FILES['imgfile'] if 'imgfile' in request.FILES else None  # 이미지 파일이 없으면 None으로 설정
            
        board = NoticeBoardPost(
            title=title,
            content=content,
            imgfile=imgfile,
        )
        #print(title, content)
        #print(board)
        board.writer=user_id
        board.save()
        
        
        return redirect('/board/board_list/') # Redirect to a success page or wherever you want
    else:
        form = NoticeBoardPostForm()
    return render(request, 'board/create_board.html', {'form': form})



def read(request, board_id):
    
    board_detail = NoticeBoardPost.objects.get(id = board_id)

    writer_id = board_detail.writer_id

    # 해당하는 사용자의 닉네임 가져오기
    user = Users.objects.get(id=writer_id)
    writer_nickname = user.nickname

    # article = Comment.objects.get(pk = board_id)
    # print(article)
    #댓글 조회, 생성
    comment_form = CommentForm()
    comments = board_detail.comment_set.all()

    for comment in comments:
        try:
            user = Users.objects.get(id=comment.writer_id)
            comment.writer_nickname = user.nickname
        except Users.DoesNotExist:
            comment.writer_nickname = "Unknown"
    context = {
        "board_detail" : board_detail,
        "writer_nickname": writer_nickname,
        "comments": comments,
        'comment_form' : comment_form,
    }
    
    #print(request.POST['text'])
    #return HttpResponse(f"{board_detail.id} = id <br> {board_detail.title} = title <br> {board_detail.content} = content")
    return render(request, 'board/board_detail.html', context)


def comment_create(request, pk):
    
    board_detail = NoticeBoardPost.objects.get(pk = pk)  
    comment_form = CommentForm(request.POST)
    user = request.session['user_id']
    user_id = Users.objects.get(user_id = user)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.commentId  = board_detail
        comment.writer=user_id
        comment.save()
    return redirect(f'/board/board_detail/{pk}/')

def comment_delete(request, board_pk, comment_pk):
    if request.method == "POST":
        comment = Comment.objects.get(pk=comment_pk)
        comment.delete()
    return redirect(f'/board/board_detail/{board_pk}/')

def boardList(request):
    if request.method == "GET":
        if not request.user.is_authenticated:   
            return redirect('accounts:login')
        lists = NoticeBoardPost.objects.all()
        # Paginator 객체 생성 (각 페이지에 10개의 게시글)
        paginator = Paginator(lists, 10)
         # 요청된 페이지 가져오기
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        #list1 = NoticeBoardPost.objects.get(id = 1)
        #print(list1)
        #lists = NoticeBoardPost.objects.values('content').all()
        #print(lists)
        context = {
           # "list1" : list1,
            "lists" : lists,
            "page_obj" : page_obj
        }
        return render(request, 'board/board_list.html', context)
    else:
        return HttpResponse("Invalid request method", status=405)
    #return HttpResponse('working!')


def boardEdit(request, pk):
    board = NoticeBoardPost.objects.get(id=pk)
    if request.method == "POST":
        #print(1)
        board.title = request.POST['title']
        board.content = request.POST['content']
        #board.imgfile = request.FILES['imgfile'] if 'imgfile' in request.FILES else None  # 이미지 파일이 없으면 None으로 설정
        board.save()
        form = NoticeBoardPostForm(request.POST, instance=board)

        if form.is_valid():
            form.save()
            return redirect(f'/board/board_detail/{pk}')

    else:
        boardForm = NoticeBoardPostForm(instance=board)
       # print(2)
        return render(request, 'board/update_board.html', {'boardForm':boardForm})
    

def boardDelete(request, pk):
    board = NoticeBoardPost.objects.get(id=pk)
    print(board)
    board.delete()
    return redirect('/board/board_list')

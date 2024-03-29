from django.shortcuts import render, redirect, HttpResponse

from app01 import models


# 列出所有书籍
def list_book(request):
    all_books = models.Book.objects.all()
    return render(request, 'list_book.html', {'all_books': all_books})


# 添加书籍
def add_book(request):
    error = ''
    if request.method == 'POST':
        title = request.POST.get('book_name')
        pk = request.POST.get('id')
        print(title, pk)
        book_set = models.Book.objects.filter(title=title, pub_id=pk)

        if book_set:
            error = '书籍已存在'

        if not title: error = '请输入书名'

        if not error:
            models.Book.objects.create(title=title, pub_id=pk)
            return redirect('/list_book/')

    all_publisher = models.Publisher.objects.all()
    return render(request, 'add_book.html', {'all_publisher': all_publisher, 'error': error})


# 删除书籍
def del_book(request):
    if request.method == 'GET':
        pk = request.GET.get('id')
        models.Book.objects.filter(id=pk).delete()
        return redirect('/list_book/')


# 编辑书籍
def edit_book(request):
    error = ''
    pk = request.GET.get('id')
    book = models.Book.objects.get(pk=pk)
    if request.method == 'POST':
        title = request.POST.get('book_name')
        pub_id = request.POST.get('id')
        print(type(title), type(book.title), type(pub_id), type(book.pub_id))
        if book.title == title and book.pub_id == int(pub_id):
            error = '未做任何修改'
        if not title: error = '请输入书名'
        if models.Book.objects.filter(title=title, pub_id=pub_id):
            error = '该书籍已存在'
        if not error:
            book.title = title
            book.pub_id = pub_id
            book.save()
            return redirect('/list_book/')

    all_publisher = models.Publisher.objects.all().order_by('pid')
    return render(request, 'edit_book.html', {'book': book, 'all_publisher': all_publisher, 'error': error})


# 列出所有的出版社
def list_publisher(request):
    all_publisher = models.Publisher.objects.all().order_by('pid')
    return render(request, 'list_publisher.html', {'all_publisher': all_publisher})


# 增加出版社
def add_publisher(request):
    error = ''
    if request.method == 'POST':
        publisher_name = request.POST.get('publisher_name')
        if models.Publisher.objects.filter(name=publisher_name):
            error = '出版社已存在'
        if not publisher_name:
            error = '内容不能为空'
        if not error:
            models.Publisher.objects.create(name=publisher_name)
            return redirect('/list_publisher/')
    return render(request, 'add_publisher.html', {'error': error})


# 删除出版社
def del_publisher(request):
    if request.method == 'GET':
        pk = request.GET.get('id')
        obj_li = models.Publisher.objects.filter(pk=pk)
        if obj_li: obj_li.delete()
        return redirect('/list_publisher/')


# 修改出版社
def edit_publisher(request):
    pk = request.GET.get('id')
    obj_li = models.Publisher.objects.filter(pk=pk)
    if not obj_li:
        return HttpResponse('编辑的信息不存在')

    error = ''
    obj = obj_li[0]
    if request.method == 'POST':
        name = request.POST.get('publisher_name')
        if not name:
            error = '内容不能为空'
        if models.Publisher.objects.filter(name=name):
            error = '出版社名称已存在'
        if obj.name == name:
            error = '未做修改'
        if not error:
            obj.name = name
            obj.save()
            return redirect('/list_publisher/')
    print(error)
    return render(request, 'edit_publisher.html', {'name': obj.name, 'error': error})

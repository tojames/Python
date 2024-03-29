from django.http import HttpResponse
from django.shortcuts import render, redirect
# 删除功能三合一
from django.urls import reverse
from django.views import View

from app01 import models


def delete(request, table, pk):
    obj = getattr(models, table.capitalize())
    obj.objects.filter(pk=pk).delete()
    return redirect(reverse('display', args=(table,)))


def display(request, table):
    obj = getattr(models, table.capitalize())
    all_item = obj.objects.all()
    return render(request, 'list_{}.html'.format(table, ), {'all_item': all_item, 'table': table})


def add_item(request, table):
    if request.method == 'POST':
        error = ''
        author_name = request.POST.get('author_name')
        if models.Author.objects.filter(name=author_name):
            error = '作者已存在'
        books = request.POST.getlist('books')
        if not (author_name and books):
            error = '作者和作品信息不完整'
        if not error:
            author = models.Author.objects.create(name=author_name)
            author.books.set(books)
            return redirect('/list_author/')
        all_book = models.Book.objects.all()
        return render(request, 'add_author.html', {'all_book': all_book, 'error': error})
    return display(request, table)


"""作者相关"""


class ListAuthor(View):

    def get(self, request):
        all_author = models.Author.objects.all()
        return render(request, 'list_author.html', {'all_author': all_author})


class AddAuthor(View):

    def get(self, request, table):
        all_book = models.Book.objects.all()
        return render(request, 'add_{}.html'.format(table, ), {'all_item': all_book})

    def post(self, request, table):
        error = ''
        author_name = request.POST.get('author_name')
        if models.Author.objects.filter(name=author_name):
            error = '作者已存在'
        books = request.POST.getlist('books')
        if not (author_name and books):
            error = '作者和作品信息不完整'
        if not error:
            author = models.Author.objects.create(name=author_name)
            author.books.set(books)
            return redirect(reverse('display', args=('author',)))
        all_book = models.Book.objects.all()
        return render(request, 'add_author.html', {'all_item': all_book, 'error': error, 'table': table})


class DelAuthor(View):

    def get(self, request):
        pk = request.GET.get('pk')
        models.Author.objects.filter(pk=pk).delete()
        return redirect('/list_author/')


class EditAuthor(View):

    def get(self, request, pk):
        author = models.Author.objects.get(pk=pk)
        all_book = models.Book.objects.all()
        return render(request, 'edit_author.html', {'author': author, 'all_book': all_book})

    def post(self, request, pk):
        error = ''
        author = models.Author.objects.get(pk=pk)
        author_name = request.POST.get('author_name')
        books = request.POST.getlist('books')
        if not author_name:
            error = '请输入作者姓名'
        if not error:
            author.name = author_name
            author.save()
            author.books.set(books)
            return redirect(reverse('author'))
        all_book = models.Book.objects.all()
        return render(request, 'edit_author.html', {'author': author, 'all_book': all_book, 'error': error})


"""书籍相关"""


class ListBook(View):

    def get(self, request):
        all_books = models.Book.objects.all()
        return render(request, 'list_book.html', {'all_books': all_books})


class AddBook(View):

    def get(self, request):
        all_publisher = models.Publisher.objects.all()
        return render(request, 'add_book.html', {'all_publisher': all_publisher})

    def post(self, request):
        error = ''
        title = request.POST.get('book_name')
        pk = request.POST.get('id')
        book_set = models.Book.objects.filter(title=title, pub_id=pk)
        if book_set:
            error = '书籍已存在'
        if not title: error = '请输入书名'
        if not error:
            models.Book.objects.create(title=title, pub_id=pk)
            return redirect(reverse('display', args=('book',)))
        all_publisher = models.Publisher.objects.all()
        return render(request, 'add_book.html', {'all_publisher': all_publisher, 'error': error})


class DelBook(View):

    def get(self, request):
        pk = request.GET.get('id')
        models.Book.objects.filter(id=pk).delete()
        return redirect('/list_book/')


class EditBook(View):

    def get(self, request, pk):
        book = models.Book.objects.get(pk=pk)
        all_publisher = models.Publisher.objects.all().order_by('pid')
        return render(request, 'edit_book.html', {'book': book, 'all_publisher': all_publisher})

    def post(self, request, pk):
        error = ''
        # pk = request.GET.get('id')
        book = models.Book.objects.get(pk=pk)
        title = request.POST.get('book_name')
        pub_id = request.POST.get('id')
        if book.title == title and book.pub_id == int(pub_id):
            error = '未做任何修改'
        if not title: error = '请输入书名'
        if models.Book.objects.filter(title=title, pub_id=pub_id):
            error = '该书籍已存在'
        if not error:
            book.title = title
            book.pub_id = pub_id
            book.save()
            return redirect(reverse('display', args=('book',)))
        all_publisher = models.Publisher.objects.all().order_by('pid')
        return render(request, 'edit_book.html', {'book': book, 'all_publisher': all_publisher, 'error': error})


"""出版社管理"""


class ListPublisher(View):

    def get(self, request):
        all_publisher = models.Publisher.objects.all().order_by('pid')
        return render(request, 'list_publisher.html', {'all_publisher': all_publisher})


class AddPublisher(View):

    def get(self, request):
        return render(request, 'add_publisher.html')

    def post(self, request):
        error = ''
        publisher_name = request.POST.get('publisher_name')
        if models.Publisher.objects.filter(name=publisher_name):
            error = '出版社已存在'
        if not publisher_name:
            error = '内容不能为空'
        if not error:
            models.Publisher.objects.create(name=publisher_name)
            return redirect(reverse('display', args=('publisher',)))
        return render(request, 'add_publisher.html', {'error': error})


class DelPublisher(View):

    def get(self, request):
        pk = request.GET.get('id')
        obj_li = models.Publisher.objects.filter(pk=pk)
        if obj_li: obj_li.delete()
        return redirect('/list_publisher/')


class EditPublisher(View):

    def get(self, request, pk):
        obj_li = models.Publisher.objects.filter(pk=pk)
        if not obj_li:
            return HttpResponse('编辑的信息不存在')
        obj = obj_li[0]
        return render(request, 'edit_publisher.html', {'name': obj.name})

    def post(self, request):
        error = ''
        pk = request.GET.get('id')
        obj_li = models.Publisher.objects.filter(pk=pk)
        if not obj_li:
            return HttpResponse('编辑的信息不存在')
        obj = obj_li[0]
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
            return redirect(reverse('display', args=('publisher',)))
        return render(request, 'edit_publisher.html', {'name': obj.name, 'error': error})


# def list_author(request):
#     all_author = models.Author.objects.all()
#     return render(request, 'list_author.html', {'all_author': all_author})


# 删除指定作者
# def del_author(request):
#     pk = request.GET.get('pk')
#     models.Author.objects.filter(pk=pk).delete()
#     return redirect('/list_author/')


# 编辑作者
# def edit_author(request):
#     error = ''
#     pk = request.GET.get('pk')
#     author = models.Author.objects.get(pk=pk)
#     if request.method == 'POST':
#         author_name = request.POST.get('author_name')
#         books = request.POST.getlist('books')
#         if not author_name:
#             error = '请输入作者姓名'
#         if not error:
#             author.name = author_name
#             author.save()
#             author.books.set(books)
#             return redirect('/list_author/')
#     all_book = models.Book.objects.all()
#     print(all_book, type(all_book))
#     return render(request, 'edit_author.html', {'author': author, 'all_book': all_book, 'error': error})


# # 增加作者
# def add_author(request):
#     error = ''
#     if request.method == 'POST':
#         author_name = request.POST.get('author_name')
#         if models.Author.objects.filter(name=author_name):
#             error = '作者已存在'
#         books = request.POST.getlist('books')
#         if not (author_name and books):
#             error = '作者和作品信息不完整'
#         if not error:
#             author = models.Author.objects.create(name=author_name)
#             author.books.set(books)
#             return redirect('/list_author/')
#     all_book = models.Book.objects.all()
#     return render(request, 'add_author.html', {'all_book': all_book, 'error': error})


# # 列出所有书籍
# def list_book(request):
#     all_books = models.Book.objects.all()
#     return render(request, 'list_book.html', {'all_books': all_books})


# # 添加书籍
# def add_book(request):
#     error = ''
#     if request.method == 'POST':
#         title = request.POST.get('book_name')
#         pk = request.POST.get('id')
#         # print(title, pk)
#         book_set = models.Book.objects.filter(title=title, pub_id=pk)
#
#         if book_set:
#             error = '书籍已存在'
#
#         if not title: error = '请输入书名'
#
#         if not error:
#             models.Book.objects.create(title=title, pub_id=pk)
#             return redirect('/list_book/')
#
#     all_publisher = models.Publisher.objects.all()
#     return render(request, 'add_book.html', {'all_publisher': all_publisher, 'error': error})


# 删除书籍
# def del_book(request):
#     if request.method == 'GET':
#         pk = request.GET.get('id')
#         models.Book.objects.filter(id=pk).delete()
#         return redirect('/list_book/')


# # 编辑书籍
# def edit_book(request):
#     error = ''
#     pk = request.GET.get('id')
#     book = models.Book.objects.get(pk=pk)
#     if request.method == 'POST':
#         title = request.POST.get('book_name')
#         pub_id = request.POST.get('id')
#         # print(type(title), type(book.title), type(pub_id), type(book.pub_id))
#         if book.title == title and book.pub_id == int(pub_id):
#             error = '未做任何修改'
#         if not title: error = '请输入书名'
#         if models.Book.objects.filter(title=title, pub_id=pub_id):
#             error = '该书籍已存在'
#         if not error:
#             book.title = title
#             book.pub_id = pub_id
#             book.save()
#             return redirect('/list_book/')
#
#     all_publisher = models.Publisher.objects.all().order_by('pid')
#     return render(request, 'edit_book.html', {'book': book, 'all_publisher': all_publisher, 'error': error})


# # 列出所有的出版社
# def list_publisher(request):
#     all_publisher = models.Publisher.objects.all().order_by('pid')
#     return render(request, 'list_publisher.html', {'all_publisher': all_publisher})


# 增加出版社
# def add_publisher(request):
#     error = ''
#     if request.method == 'POST':
#         publisher_name = request.POST.get('publisher_name')
#         if models.Publisher.objects.filter(name=publisher_name):
#             error = '出版社已存在'
#         if not publisher_name:
#             error = '内容不能为空'
#         if not error:
#             models.Publisher.objects.create(name=publisher_name)
#             return redirect('/list_publisher/')
#     return render(request, 'add_publisher.html', {'error': error})


# # 删除出版社
# def del_publisher(request):
#     if request.method == 'GET':
#         pk = request.GET.get('id')
#         obj_li = models.Publisher.objects.filter(pk=pk)
#         if obj_li: obj_li.delete()
#         return redirect('/list_publisher/')


# # 修改出版社
# def edit_publisher(request):
#     pk = request.GET.get('id')
#     obj_li = models.Publisher.objects.filter(pk=pk)
#     if not obj_li:
#         return HttpResponse('编辑的信息不存在')
#
#     error = ''
#     obj = obj_li[0]
#     if request.method == 'POST':
#         name = request.POST.get('publisher_name')
#         if not name:
#             error = '内容不能为空'
#         if models.Publisher.objects.filter(name=name):
#             error = '出版社名称已存在'
#         if obj.name == name:
#             error = '未做修改'
#         if not error:
#             obj.name = name
#             obj.save()
#             return redirect('/list_publisher/')
#     return render(request, 'edit_publisher.html', {'name': obj.name, 'error': error})


# def add_info(request):
#     error = ''
#     all_publisher = models.Publisher.objects.all()
#     if request.method == 'POST':
#         author_name = request.POST.get('author_name')
#         book_name = request.POST.get('book_name')
#         pub_id = request.POST.get('publisher')
#         if models.Book.objects.filter(title=book_name, pub_id=pub_id):
#             error = '书籍信息已存在'
#         if models.Author.objects.filter(name=author_name):
#             error = '作者信息已存在'
#         if not (author_name and book_name):
#             error = '信息不完整'
#         if not request.POST.get('cancel'):
#             if not error:
#                 author = models.Author.objects.create(name=author_name, )
#                 book = models.Book.objects.create(title=book_name, pub_id=pub_id)
#                 author.books.set([str(book.pk)])
#             return redirect('/list_author/')
#     return render(request, 'add_info.html', {'all_publisher': all_publisher, 'error': error})


# def tags_test(request):
#     return render(request, 'tags_test.html')


def upload(request):
    if request.method == 'POST':
        data = request.FILES.get('file')
        with open(data.name, 'wb') as f:
            for i in data.chunks():
                print('正在写入中')
                f.write(i)
        return HttpResponse('文件传输完成')
    return render(request, 'upload.html')


def test(request):
    return render(request, 'test.html')

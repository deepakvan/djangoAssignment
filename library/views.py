from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Books,Details
from django.http import HttpResponse
# Create your views here.
def home(request):
    return HttpResponse("<H1>Hello api</H1>")
class AddBook(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_data = User.objects.get(username=request.user)
        if user_data.details.role_type=="librarian":
            print(user_data.details.role_type)
            ISBN_Code = request.data['ISBN_Code'] if 'ISBN_Code' in request.data else None
            Book_Title= request.data['Book_Title'] if 'Book_Title' in request.data else None
            Book_Author = request.data['Book_Author'] if 'Book_Author' in request.data else None
            Status =request.data['Status'] if 'Status' in request.data else None
            Borrowed_By = request.data['Borrowed_By'] if 'Borrowed_By' in request.data else None
            Publication_year = request.data['Publication_year'] if 'Publication_year' in request.data else None
            print(ISBN_Code,Book_Title,Book_Author,Borrowed_By,Status,Publication_year)
            if ISBN_Code is None or Book_Title is None or Book_Author is None or Status is None or Borrowed_By is None or Publication_year is None :
                content = {'ISBN_Code': 'Required', 'Book_Title': 'Required','Book_Author': 'Required',
                           'Status': 'Required','Borrowed_By': 'Required', 'Publication_year':'Required'}
                return Response(content)
            else:
                existing_book=Books.objects.get(ISBN_Code=ISBN_Code)
                if existing_book is None:
                    book_data=Books.objects.create(ISBN_Code=ISBN_Code,Book_Title=Book_Title,Book_Author=Book_Author,
                                               Status=Status,Borrowed_By=Borrowed_By,
                                               Publication_year=Publication_year)
                    book_data.save()
                    content = {'message': 'book Successfully added'}
                    return Response(content)
                else:
                    content = {'message': 'book Already exist..'}
                    return Response(content)
        else:
            content = {'message': 'you have no permission to add book', 'role_type': user_data.details.role_type}
            return Response(content)

class DeleteBook(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_data = User.objects.get(username=request.user)
        if user_data.details.role_type=="librarian":
            ISBN_Code = request.data['ISBN_Code'] if 'ISBN_Code' in request.data else None
            if ISBN_Code is not None:
                try:
                    delbook = Books.objects.get(ISBN_Code=ISBN_Code)
                    print(delbook.ISBN_Code)
                    if delbook:
                        delbook.delete()
                        content = {'message': 'book Successfully Deleted'}
                        return Response(content)
                    else:
                        content = {'message': 'book Not exists...'}
                        return Response(content)
                except ObjectDoesNotExist as DoesNotExist:
                    content = {'message': 'book Not exists...'}
                    return Response(content)

            else:
                content = {'ISBN_Code': 'Required'}
                return Response(content)
        else:
            content = {'message': 'you have no permission to Delete book'}
            return Response(content)


class UpdateBook(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_data = User.objects.get(username=request.user)
        if user_data.details.role_type=="librarian":
            ISBN_Code = request.data['ISBN_Code'] if 'ISBN_Code' in request.data else None
            Book_Title = request.data['Book_Title'] if 'Book_Title' in request.data else None
            Book_Author = request.data['Book_Author'] if 'Book_Author' in request.data else None
            Status = request.data['Status'] if 'Status' in request.data else None
            Borrowed_By = request.data['Borrowed_By'] if 'Borrowed_By' in request.data else None
            Publication_year = request.data['Publication_year'] if 'Publication_year' in request.data else None
            if ISBN_Code is not None:
                try:
                    update_book = Books.objects.get(ISBN_Code=ISBN_Code)
                    if update_book:
                        if Book_Title is not None: update_book.Book_Title=Book_Title
                        if Book_Author is not None: update_book.Book_Author = Book_Author
                        if Status is not None: update_book.Status = Status
                        if Borrowed_By is not None: update_book.Borrowed_By = Borrowed_By
                        if Publication_year is not None: update_book.Publication_year = Publication_year
                        update_book.save()
                        content = {'message': 'book updated successfully...'}
                        return Response(content)
                    else:
                        content = {'message': 'book Not exists...'}
                        return Response(content)
                except ObjectDoesNotExist as DoesNotExist:
                    content = {'message': 'book Not exists...'}
                    return Response(content)
            else:
                content = {'ISBN_Code': 'Required'}
                return Response(content)
        else:
            content = {'message': 'you have no permission to Delete book'}
            return Response(content)


class ViewBook(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_data = User.objects.get(username=request.user)
        if user_data.details.role_type=="librarian" or user_data.details.role_type=="member":
            ISBN_Code = request.data['ISBN_Code'] if 'ISBN_Code' in request.data else None
            if ISBN_Code is not None:
                try:
                    view_book = Books.objects.get(ISBN_Code=ISBN_Code)
                    print(view_book.ISBN_Code)
                    if view_book:
                        content = {'ISBN_Code': view_book.ISBN_Code, 'Book_Title': view_book.Book_Title, 'Book_Author': view_book.Book_Author,
                                   'Status': view_book.Status, 'Borrowed_By': view_book.Borrowed_By, 'Publication_year': view_book.Publication_year}
                        return Response(content)
                    else:
                        content = {'message': 'book Not exists...'}
                        return Response(content)
                except ObjectDoesNotExist as DoesNotExist:
                    content = {'message': 'book Not exists...'}
                    return Response(content)

            else:
                content = {'ISBN_Code': 'Required'}
                return Response(content)
        else:
            content = {'message': 'you have no permission to Delete book'}
            return Response(content)


class ViewAllBook(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_data = User.objects.get(username=request.user)
        if user_data.details.role_type=="librarian" or user_data.details.role_type=="member":
            allbooks = Books.objects.all()
            if allbooks:
                content={}
                for book in allbooks:
                    content[book.ISBN_Code]={'ISBN_Code': book.ISBN_Code, 'Book_Title': book.Book_Title, 'Book_Author': book.Book_Author,
                                   'Status': book.Status, 'Borrowed_By': book.Borrowed_By, 'Publication_year': book.Publication_year}
                    return Response(content)
            else:
                content = {'message': 'No books Available'}
                return Response(content)
        else:
            content = {'message': 'you have no permission to Delete book'}
            return Response(content)


class BorrowBook(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_data = User.objects.get(username=request.user)
        if user_data.details.role_type=="member":
            ISBN_Code = request.data['ISBN_Code'] if 'ISBN_Code' in request.data else None
            if ISBN_Code is not None:
                try:
                    book = Books.objects.get(ISBN_Code=ISBN_Code)
                    print(book.ISBN_Code)
                    if book:
                        if book.Status=="Available":
                            book.Status="Borrowed"
                            book.Borrowed_By=user_data.username
                            book.save()
                            content = {'message': 'book borrowed Successfully'}
                            return Response(content)
                        else:
                            content = {'message': 'book Not Available...'}
                            return Response(content)
                    else:
                        content = {'message': 'book Not exists...'}
                        return Response(content)
                except ObjectDoesNotExist as DoesNotExist:
                    content = {'message': 'book Not exists...'}
                    return Response(content)
            else:
                content = {'ISBN_Code': 'Required'}
                return Response(content)
        else:
            content = {'message': 'you have no permission to Borrow book'}
            return Response(content)


class ReturnBook(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_data = User.objects.get(username=request.user)
        if user_data.details.role_type == "member":
            ISBN_Code = request.data['ISBN_Code'] if 'ISBN_Code' in request.data else None
            if ISBN_Code is not None:
                try:
                    book = Books.objects.get(ISBN_Code=ISBN_Code)
                    print(book.ISBN_Code)
                    if book:
                        if book.Status == "Borrowed" and book.Borrowed_By==user_data.username:
                            book.Status = "Available"
                            book.Borrowed_By = ""
                            book.save()
                            content = {'message': 'book returned Successfully'}
                            return Response(content)
                        else:
                            content = {'message': 'book is Not borrowed by you...'}
                            return Response(content)
                    else:
                        content = {'message': 'book Not exists...'}
                        return Response(content)
                except ObjectDoesNotExist as DoesNotExist:
                    content = {'message': 'book Not exists...'}
                    return Response(content)
            else:
                content = {'ISBN_Code': 'Required'}
                return Response(content)
        else:
            content = {'message': 'you have no permission to Return book'}
            return Response(content)


class AddMember(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_data = User.objects.get(username=request.user)
        if user_data.details.role_type=="librarian":
            print(user_data.details.role_type)
            username = request.data['username'] if 'username' in request.data else None
            password= request.data['password'] if 'password' in request.data else None
            email = request.data['email'] if 'email' in request.data else ""
            first_name =request.data['first_name'] if 'first_name' in request.data else ""
            last_name = request.data['last_name'] if 'last_name' in request.data else ""
            #print(ISBN_Code,Book_Title,Book_Author,Borrowed_By,Status,Publication_year)
            if username is None or password is None:
                content = {'username': 'Required', 'password': 'Required','email': 'optional',
                           'first_name': 'optional','last_name': 'optional',}
                return Response(content)
            else:
                exiting_member=User.objects.get(username=username)
                if exiting_member is None:
                    member=User.objects.create_user(username=username,password=password,email=email,
                                               first_name=first_name,last_name=last_name)
                    member.save()
                    member_details=Details.objects.create(role_type="member",user_id=member.id)
                    member_details.save()
                    content = {'message': 'Member Successfully added'}
                    return Response(content)
                else:
                    content = {'message': 'Member Already Exist..'}
                    return Response(content)
        else:
            content = {'message': 'you have no permission to add member', 'role_type': user_data.details.role_type}
            return Response(content)


class DeleteMember(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_data = User.objects.get(username=request.user)
        username = request.data['username'] if 'username' in request.data else None
        if user_data.details.role_type == "librarian" or username==user_data.username:
            print(user_data.details.role_type)
            if username is None:
                content = {'username': 'Required'}
                return Response(content)
            else:
                try:
                    member = User.objects.get(username=username)
                    if member is not None:
                        books=Books.objects.filter(Borrowed_By=member.username)
                        if not books.exists():
                            member_details = Details.objects.get(user_id=member.id)
                            member_details.delete()
                            member.delete()
                            content = {'message': 'Member Deleted Successfully'}
                            return Response(content)
                        else:
                            content = {'message': 'Member has Following books to return'}
                            for book in books:
                                content[book.ISBN_Code] = {'ISBN_Code': book.ISBN_Code, 'Book_Title': book.Book_Title,
                                                       'Book_Author': book.Book_Author,
                                                       'Status': book.Status, 'Borrowed_By': book.Borrowed_By,
                                                       'Publication_year': book.Publication_year}
                                return Response(content)
                    else:
                        content = {'message': 'Member not exist...'}
                        return Response(content)
                except ObjectDoesNotExist as DoesNotExist:
                    content = {'message': 'Member Not exists exception...'}
                    return Response(content)
        else:
            content = {'message': 'you have no permission to delete member', 'role_type': user_data.details.role_type}
            return Response(content)


class UpdateMember(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_data = User.objects.get(username=request.user)
        if user_data.details.role_type == "librarian":
            print(user_data.details.role_type)
            username = request.data['username'] if 'username' in request.data else None
            password = request.data['password'] if 'password' in request.data else None
            email = request.data['email'] if 'email' in request.data else None
            first_name = request.data['first_name'] if 'first_name' in request.data else None
            last_name = request.data['last_name'] if 'last_name' in request.data else None
            # print(ISBN_Code,Book_Title,Book_Author,Borrowed_By,Status,Publication_year)
            if username is None:
                content = {'username': 'Required', 'password': 'Optional', 'email': 'optional',
                           'first_name': 'optional', 'last_name': 'optional', }
                return Response(content)
            else:
                try:
                    member = User.objects.get(username=username)
                    if member:
                        if password is not None: member.password = password
                        if email is not None: member.email = email
                        if first_name is not None: member.first_name = first_name
                        if last_name is not None: member.last_name = last_name
                        member.save()
                        content = {'message': 'Member updated successfully...'}
                        return Response(content)
                    else:
                        content = {'message': 'Member Not exist...'}
                        return Response(content)
                except ObjectDoesNotExist as DoesNotExist:
                    content = {'message': 'Member Not exist...'}
                    return Response(content)
        else:
            content = {'message': 'you have no permission to update Member', 'role_type': user_data.details.role_type}
            return Response(content)


class ViewMember(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_data = User.objects.get(username=request.user)
        if user_data.details.role_type == "librarian":
            username = request.data['username'] if 'username' in request.data else None
            if username is not None:
                try:
                    view_user = User.objects.get(username=username)
                    #print(view_book.ISBN_Code)
                    if view_user:
                        content = {'username': view_user.username, 'password': view_user.password,
                                   'email': view_user.email,
                                   'first_name': view_user.first_name, 'last_name': view_user.last_name}
                        return Response(content)
                    else:
                        content = {'message': 'Member Not exist...'}
                        return Response(content)
                except ObjectDoesNotExist as DoesNotExist:
                    content = {'message': 'Member Not exists...'}
                    return Response(content)

            else:
                content = {'username': 'Required'}
                return Response(content)
        else:
            content = {'message': 'you have no permission to view member'}
            return Response(content)


class ViewAllMember(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_data = User.objects.get(username=request.user)
        if user_data.details.role_type == "librarian":
            allusers = User.objects.all()
            if allusers:
                content = {}
                for view_user in allusers:
                    content[view_user.username] = {'username': view_user.username, 'password': view_user.password,
                                   'email': view_user.email,
                                   'first_name': view_user.first_name, 'last_name': view_user.last_name}
                    return Response(content)
            else:
                content = {'message': 'No Members Available'}
                return Response(content)
        else:
            content = {'message': 'you have no permission to view members'}
            return Response(content)
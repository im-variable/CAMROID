import os

from django.contrib import messages
from django.contrib.auth import authenticate
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.functions import TruncYear, TruncMonth, ExtractMonth, ExtractYear
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import ImgDetails, CategoryList, UserProfile
from pathlib import Path
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import calendar
# import getpass
# import random
# import string
# Create your views here.

UPLOAD_FOLDER = (Path(__file__).parent.parent/ "media/").resolve()

# for carousel in index page
def cat_suggestions():
    category_ = categoryList()
    cat_suggestions = []
    i = 0
    while i < len(category_):
        cat_suggestions.append(category_[i:i+9])
        i+=9

    # print('suggestion', cat_suggestions)
    return cat_suggestions

# # for random string generator for file name
# def get_random_alphanumeric_string(length):
#     letters_and_digits = string.ascii_letters + string.digits
#     result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
#     # print("Random alphanumeric String is:", result_str)
#     return result_str

# for category list
def categoryList():
    _catList = CategoryList.objects.all().values_list('id', 'Category').order_by('Category')
    # print("Catlist:", _catList)
    return _catList


# ---------------------------------------------------------------------------------------------------------


def index(request):
    val = int(request.GET.get('val')) if request.GET.get('val') != None else 1

    category_ = cat_suggestions()
    print('val: ',val)
    # print(CategoryList)
    if request.method == 'GET':
        if val == 1:
            imgList = ImgDetails.objects.filter(Valid=True)
        else:
            imgList = ImgDetails.objects.filter(Category_id=val, Valid=True)

            # form = ImgDetails(instance=imgList)
        print("imgList: ",imgList)
        lst = []
        for x in imgList:
            lst.append(x.Img.url)

        page_number = request.GET.get('page')
        paginator = Paginator(lst, 15)
        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'arrList': page_obj, 'category_': category_})


ALLOWED_EXTENTIONS = ['png','jpg','jpeg']

@login_required(login_url='login')
def myspace(request):
    # for categoryList in dd
    Upload_catList = categoryList()

    user = User.objects.get(id=request.user.id)

    if request.method == "POST":

        if request.POST['action'] == 'Upload':

            keywords = request.POST['keywords']
            print("kw:", keywords)
            Cat = request.POST['Category']

            for count, x in enumerate(request.FILES.getlist("files[]")):

                if x.name.endswith(tuple(ALLOWED_EXTENTIONS)):
                    imgname = str(user.id) + '-' + str(x)
                    already_Uploaded = ImgDetails.objects.filter(Img=imgname).exists()

                    # print ('already: ',already_Uploaded)
                    if bool(already_Uploaded) == False:
                        def process(f):
                            imgdetail = ImgDetails.objects.create(Img=imgname, keywords=keywords, User_id=user.id, Category_id=Cat)
                            with open(str(UPLOAD_FOLDER) + '/' + imgname, 'wb+') as destination:
                                for chunk in f.chunks():
                                    destination.write(chunk)
                            messages.success(request, '{0} uploaded successfully'.format(imgname))
                        process(x)
            # return render(request, 'myspace.html', {"Upload_catList": Upload_catList, "uploadedList": uploadedList, 'col_queryset': col_queryset, 'pro_queryset': pro_queryset})

        elif request.POST['action'] == 'del_img':

            pk = request.POST['confirm_del'] if request.POST['confirm_del'] is not None else 0

            img_del = ImgDetails.objects.filter(pk=pk)
            img_del.delete()
            messages.info(request, 'Image deleted successfully')

        elif request.POST['action'] == 'save-upload':

            if request.FILES['profile-upload'] is not None:

                profile_img = request.FILES['profile-upload']

                if profile_img.name.endswith(tuple(ALLOWED_EXTENTIONS)):
                    if user.userprofile.profile_img is not None:
                        os.remove(user.userprofile.profile_img.name)
                        user.userprofile.profile_img = None
                    user.userprofile.profile_img = profile_img
                    user.save()
                    messages.success(request, 'Profile image updated successfully')
                else:
                    messages.error(request, 'Choose a correct file format(ex: {0})'.format(ALLOWED_EXTENTIONS))
                    return redirect('myspace')
            else:
                messages.warning(request, 'Select an image to upload')

        elif request.POST['action'] == 'update-account':

            id_ = request.POST['id']

            if id_ is not None:

                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                email = request.POST['email']

                updateField = User.objects.get(pk=id_)

                updateField.first_name = first_name
                updateField.last_name = last_name
                updateField.email = email

                updateField.save()
                messages.success(request, 'Profile detail updated successfully')

        elif request.POST['action'] == 'change-pass':
             username = request.POST['username']
             print("id: ",username)
             old_pass = request.POST['oldPassword']
             print("old: ",old_pass)
             new_pass = request.POST['newPassword']
             print("new: ",new_pass)
             if username is not None:
                user_data = authenticate(username=username, password=old_pass)
                print('user: ', user_data)
                if user_data is not None:
                    user_data.set_password(new_pass)
                    user_data.save()
                    messages.success(request, 'Password updated successfully')
    # get request
    process_queryset = ImgDetails.objects.filter(User_id=user.id, Valid=False).annotate(
        month=ExtractMonth('UploadDate'), year=ExtractYear('UploadDate'))

    pro_queryset = []
    print(process_queryset)
    for result in process_queryset:
        pro_queryset.append({'id': result.id, 'Img': result.Img.url,
                             'UploadDate': calendar.month_name[result.month] + "-" + str(result.year)})

    collect_queryset = ImgDetails.objects.filter(User_id=user.id, Valid=True).annotate(month=ExtractMonth('UploadDate'),
                                                                                       year=ExtractYear('UploadDate'))
    col_queryset = []
    print(collect_queryset)
    for result in collect_queryset:
        col_queryset.append({'id': result.id, 'Img': result.Img.url,
                             'UploadDate': calendar.month_name[result.month] + "-" + str(result.year)})

    user = User.objects.get(id=request.user.id)

    return render(request, 'myspace.html', {"Upload_catList": Upload_catList, 'col_queryset': col_queryset, 'pro_queryset': pro_queryset, 'user': user})


def category(request):

    catList = categoryList()

    imgList = CategoryList.objects.all()

    arrList = []
    for x in imgList:
        arrList.append([x.id, x.Category, x.Cat_Img.url])

    print(arrList)
    return render(request, 'category.html', {'arrList': arrList})


def getTags(request):

        TagList = ImgDetails.objects.values_list('keywords', flat=True).order_by('keywords')

        print('TagList: ', TagList)

        tagsuggestions = set([item for sublist in TagList for item in str(sublist).split(',')])

        print("tagsuggestions: ", tagsuggestions)

        return JsonResponse(list(tagsuggestions), safe=False)

import os

from django.contrib import messages
from django.contrib.auth import authenticate
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.functions import ExtractMonth, ExtractYear
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import ImgDetails, CategoryList
from pathlib import Path
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import calendar
import re
from django.views import View

# Create your views here.

UPLOAD_FOLDER =  os.path.abspath(os.path.dirname(__name__))

<<<<<<< HEAD
print("UPLOAD_FOLDER", UPLOAD_FOLDER)
=======
>>>>>>> 3fdd9a2e17ecbbf4222c6f59cecf13d4c92acbf1
# UPLOAD_FOLDER = (Path(__file__).parent.parent/ "media/").resolve()

# for carousel in index page
def cat_suggestions():
    category_ = categoryList()
    cat_suggestions = []
    i = 0
    while i < len(category_):
        cat_suggestions.append(category_[i:i+6])
        i+=6

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

# for search suggestion
def getSuggestion(request):

    if request.method == "GET":

        SuggestList = ImgDetails.objects.values_list('keywords', flat=True).order_by('keywords')

        suggestions = list(set([item for sublist in SuggestList for item in str(sublist).split(',')]))

    return JsonResponse(suggestions, safe=False)


# ---------------------------------------------------------------------------------------------------------


def index(request):
    catVal = int(request.GET.get('val')) if request.GET.get('val') != None else 1

    category_ = cat_suggestions()
    if request.method == 'GET':
        if catVal == 1:
            imgList = ImgDetails.objects.filter(Valid=True)
        else:
            imgList = ImgDetails.objects.filter(Category_id=catVal, Valid=True)

    elif request.POST['action'] == "search-icon":

        searchVal = str(request.POST['search-field'])

        print("searchVal: ", searchVal)
        arrSearch = re.findall(r"[\w']+", searchVal)



        imgList = None
        for val in arrSearch:
            imgList = ImgDetails.objects.filter(Valid=True, keywords__icontains=val)

    if imgList == None:
        imgList = ImgDetails.objects.filter(Valid=True)

    lst = []
    for x in imgList:
        lst.append(x.Img.url)

    page_number = request.GET.get('page')
    paginator = Paginator(lst, 20)
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

            keywords = request.POST.get('keywords', 'images')
            
            Cat = request.POST.get('Category', 1)

            for count, x in enumerate(request.FILES.getlist("files[]")):

                if x.name.endswith(tuple(ALLOWED_EXTENTIONS)):
                    imgname = str(user.id) + '-' + str(x)
                    already_Uploaded = ImgDetails.objects.filter(Img=imgname).exists()

                    if bool(already_Uploaded) == False:
                        def process(f):
                            imgdetail = ImgDetails.objects.create(Img=imgname, keywords=keywords, User_id=user.id, Category_id=Cat)
                            with open(str(UPLOAD_FOLDER) + '/static/media/' + imgname, 'wb+') as destination:
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

                print('profile image:', user.userprofile.profile_img.name )
                if profile_img.name.endswith(tuple(ALLOWED_EXTENTIONS)):
                    if user.userprofile.profile_img is not None and user.userprofile.profile_img.name != 'ProfileImg/default-avatar.png':
                        try:
                            os.remove("static/media/"+user.userprofile.profile_img.name)
                        except Exception as identifier:
                            messages.error(request, "Something went wrong")
                        finally:
                            user.userprofile.profile_img = None
                    user.userprofile.profile_img = profile_img
                    user.save()
                    messages.success(request, 'Profile image updated successfully')
                else:
                    messages.error(request, 'Choose a correct file format(ex: {0})'.format(ALLOWED_EXTENTIONS))
                    return redirect('myspace')
            else:
                messages.warning(request, 'Select an image to upload')

        elif request.POST['action'] == 'delete-upload':

            if user.userprofile.profile_img is not None and user.userprofile.profile_img.name != 'ProfileImg/default-avatar.png':
                
                try:
                    os.remove("static/media/"+user.userprofile.profile_img.name)
                    user.userprofile.profile_img = ''
                    messages.info(request, 'Profile image deleted successfully')
                    user.userprofile.profile_img = 'ProfileImg/default-avatar.png'
                    user.save()
                except Exception as identifier:
                    pass

        elif request.POST['action'] == 'update-account':

                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                email = request.POST.get('email')

                user.first_name = first_name
                user.last_name = last_name
                user.email = email

                user.save()
                messages.success(request, 'Profile detail updated successfully')

        elif request.POST['action'] == 'change-pass':
            username = request.POST.get('username')
            old_pass = request.POST.get('oldPassword')
            new_pass = request.POST.get('newPassword')
            if username is not None:
                user_data = authenticate(username=username, password=old_pass)
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

    for x in pro_queryset:
        print("x", x)
        
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

    return render(request, 'category.html', {'arrList': arrList})


class AboutUs(View):

    def get(self, request):
    
        admin_user = User.objects.get(is_superuser=True)
        user = User.objects.filter(id=request.user.id).first()

        if not user:

            print('authentication req')
            return render(request, "aboutus.html", {'admin_user': admin_user})
        else:
        
            if self.request.is_ajax() and self.request.method == "GET":

                sentiment_Value = request.GET.get("sentiment_Value", None)
            
                user.userprofile.feedback = sentiment_Value 
                user.save()            
                print('feedback saved')
            
                return render(request, "aboutus.html", {'admin_user': admin_user, 'user': user})
        
        return render(request, "aboutus.html", {'admin_user': admin_user, 'user': user})

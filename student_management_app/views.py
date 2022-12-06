import datetime
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
import requests, json

from student_management_app.EmailBackEnd import EmailBackEnd
from student_management_app.models import CustomUser


# Create your views here. 
def showDemoPage(request):
    return render(request, "demo.html")

def ShowLoginPage(request):
    return render(request, "login_page.html")

def dologin(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        # print("Captcha: "+request.POST.get("g-recaptcha-response"))
        captcha_token = request.POST.get("g-recaptcha-response")
        cap_url = "https://www.google.com/recaptcha/api/siteverify"
        cap_secret = "6LdTnkIjAAAAAG1mWavJM3sx4oXbHR0Iy84Fom3k"
        cap_data = {"secret":cap_secret,"response":captcha_token}
        cap_server_response = requests.post(url=cap_url,data=cap_data)
        # print(cap_server_response.text)
        cap_json = json.loads(cap_server_response.text)
        if cap_json['success']==False:
            messages.error(request, "Invalid Captcha, Try Again")
            return HttpResponseRedirect("/")

        user = EmailBackEnd.authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
        if user!=None:
            login(request, user)
            if user.user_type == "1":
                return HttpResponseRedirect("/admin_home")
            elif user.user_type == "2":
                return HttpResponseRedirect(reverse("staff_home"))
            else:
                return HttpResponseRedirect(reverse("student_home"))
            #return HttpResponse("Email: "+request.POST.get("email")+" Password: "+request.POST.get("password"))
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("/")

def GetUserDetails(request):
    if request.user!=None:
        return HttpResponse("User: "+request.user.email+" UserType: "+request.user.user_type)
    else:
        return HttpResponse("Please Login First")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")

def showFirebaseJS(request):
    data = 'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-app.js");'\
            'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-messaging.js");'\
            'var firebaseConfig = {'\
            '   apiKey: "AIzaSyA-RPW0lSoEEfUKoAhRpE1VB6vzxtPZYXs",'\
            '   authDomain: "studentmanagementsystem-ece81.firebaseapp.com",'\
            '   projectId: "studentmanagementsystem-ece81",'\
            '   storageBucket: "studentmanagementsystem-ece81.appspot.com",'\
            '   messagingSenderId: "801623938034",'\
            '   appId: "1:801623938034:web:b946ddb3ad2f4fae63d16b",'\
            '   measurementId: "G-RJTYTYN0L9"'\
            '};'\
            'firebase.initializeApp(firebaseConfig);'\
            'const messaging=firebase.messaging();'\
            'messaging.setBackgroundMessageHandler(function (payload) {'\
            '    console.log(payload);'\
            '    const notification=JSON.parse(payload);'\
            '    const notificationOption={'\
            '        body:notification.body,'\
            '        icon:notification.icon'\
            '    };'\
            '    return self.registration.showNotification(payload.notification.title,notificationOption);'\
            '});'

    return HttpResponse(data)

# def signup_admin(request):
#     return render(request, "signup_admin_page.html")

# def do_admin_signup(request):
#     username = request.POST.get("username")
#     email = request.POST.get("email")
#     password = request.POST.get("password")

#     try:
#         user = CustomUser.objects.create_user(
#             user_type  = 1,
#             username = username,
#             email = email,
#             password = password,
#         )
#         user.save()
#         messages.success(request, "Successfully Signed Up as Admin")
#         return HttpResponseRedirect(reverse("show_login"))
#     except:
#         messages.error(request, "Failed to Sign Up as Admin")
#         return HttpResponseRedirect(reverse("show_login"))

# def signup_student(request):
#     return render(request, "signup_student_page.html")

# def do_student_signup(request):
#     username = request.POST.get("username")
#     email = request.POST.get("email")
#     password = request.POST.get("password")
#     address = request.POST.get("address")

#     try:
#         user = CustomUser.objects.create_user(
#             user_type  = 3,
#             username = username,
#             email = email,
#             password = password,
#         )
#         user.students.address = address
#         user.save()
#         messages.success(request, "Successfully Signed Up as Student")
#         return HttpResponseRedirect(reverse("show_login"))
#     except:
#         messages.error(request, "Failed to Sign Up as Student")
#         return HttpResponseRedirect(reverse("show_login"))

# def signup_staff(request):
#     return render(request, "signup_staff_page.html")

# def do_staff_signup(request):
#     username = request.POST.get("username")
#     email = request.POST.get("email")
#     password = request.POST.get("password")
#     address = request.POST.get("address")

#     try:
#         user = CustomUser.objects.create_user(
#             user_type  = 2,
#             username = username,
#             email = email,
#             password = password,
#         )
#         user.staffs.address = address
#         user.save()
#         messages.success(request, "Successfully Signed Up as Staff")
#         return HttpResponseRedirect(reverse("show_login"))
#     except:
#         messages.error(request, "Failed to Sign Up as Staff")
#         return HttpResponseRedirect(reverse("show_login"))

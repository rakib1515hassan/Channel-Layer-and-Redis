from django.shortcuts import render

# Create your views here.

def home(request, group_name):
    print("----------------------")
    print("Group Name = ", group_name)
    print("----------------------")
    return render(request, 'index.html', {"group_name": group_name})

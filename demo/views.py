from django.shortcuts import render, HttpResponse


# Create your views here.
# localhost:8000/demo/hello


def say_hello(request):
    return HttpResponse("Hello welcome to Django!")


def welcome(request, name: str):
    print(name)
    if len(name) < 3:
        name = ""
    return render(request, "index.html", {"name": name})

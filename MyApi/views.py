from django.shortcuts import render, redirect
from .models import MyFile

def index(request):
    if request.method == "POST":
        img = request.FILES['image']
        data = MyFile.objects.create(image = img)   # image is the column name in the table(Model) in database
        url = "http://127.0.0.1:8000" + data.image.url
        return redirect(url)

    return render(request, "index.html")
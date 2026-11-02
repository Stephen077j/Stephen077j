import os
from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import JsonResponse
from django.urls import path

if not settings.configured:
    settings.configure(SECRET_KEY=os.environ.get("DJANGO_SECRET_KEY","local-development-only-not-for-production"),DEBUG=False,ROOT_URLCONF=__name__,ALLOWED_HOSTS=["localhost","127.0.0.1","testserver"],INSTALLED_APPS=[],MIDDLEWARE=[])

STUDENTS = [{"id":1,"name":"Aina","level":"L1"},{"id":2,"name":"Miora","level":"L2"}]

def students(request):
    if request.method != "GET":
        return JsonResponse({"error":"Method not allowed"},status=405)
    return JsonResponse({"students":STUDENTS})

urlpatterns=[path("api/students/",students)]

if __name__=="__main__":
    execute_from_command_line()

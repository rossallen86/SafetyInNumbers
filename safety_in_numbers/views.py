from django.shortcuts import render
from django.views import View


class Index(View):

    def get(self, request):
        return render(request, "index.html")

    def post(self, request):
        pass


class Profile(View):
    def get(self, request):
        return render(request, 'accounts/profile.html')

    def post(self, request):
        pass
        '''return render(request, 'accounts/profile.html')'''
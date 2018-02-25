import requests

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.auth import login,authenticate

from .forms import TokenForm
from .models import Project, User


class HomeView(TemplateView):
    template_name = "project_admin/home.html"

    def get(self, request, *args, **kwargs):
        token = None
        self.member_data = None

        if 'master_access_token' in request.session:
            token = request.session['master_access_token']
            self.member_data = self.token_for_memberlist(token)
            if not self.member_data:
                del request.session['master_access_token']

        if self.member_data:
            return super().get(request, *args, **kwargs)
        else:
            return redirect('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['member_data'] = self.member_data
        return context


    #def form_valid(self, form):
    def token_for_memberlist(self, token):
        req_url = ('https://www.openhumans.org/api/direct-sharing/project/'
                   'members/?access_token={}'.format(token))
        req = requests.get(req_url)
        if req.status_code == 200:
            return req.json()
        else:
            messages.error(self.request, 'Token not valid. Maybe a fresh one is needed?')
            return None


class LoginView(FormView):
    template_name = 'project_admin/login.html'
    form_class = TokenForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):

        token = form.cleaned_data['token']
        username = form.cleaned_data['username']
        if(username):
           print(username)

           user = form.save()
           print(user)
           login(self.request,user, backend='django.contrib.auth.backends.ModelBackend')
           print("success")
           return redirect('home')

        req_url = ("https://www.openhumans.org/api/direct-sharing/project/?access_token={}".format(token))
        params = {'token': token}
        r = requests.get(req_url, params=params).json()
        print(Project.objects.filter(id = r['id']).exists())
        if (Project.objects.filter(id = r['id']).exists()):
            try:
                Project.objects.update(id=r['id'], defaults=r)
                self.request.session['master_access_token'] = token
            except Exception as e:
                # Handle expired master tokens, or serve error message
                if 'Expired token' in r['detail']:
                    messages.error(self.request,
                                   'Token has expired. Refresh your token in the project management interface.')
                else:
                    messages.error(self.request, e)

                return redirect('home')
        else:
            try:
                user = User.objects.create(username = r['id_label'])
                r['user'] = user
                project = Project.objects.create(id=r['id'], defaults=r)
            except Exception as e:
                # Handle expired master tokens, or serve error message
                if 'Expired token' in r['detail']:
                    messages.error(self.request,
                                   'Token has expired. Refresh your token in the project management interface.')
                else:
                    messages.error(self.request, e)

                self.request.session['master_access_token'] = token
                return redirect('home')
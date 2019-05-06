from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from safety_in_numbers.forms import SafetyInUserForm
from safety_in_numbers.models import SafetyInUser, Transit


@method_decorator(login_required, name='dispatch')
class Index(View):

    def get(self, request):
        return render(request, "index.html")

    def post(self, request):
        pass


@method_decorator(login_required, name='dispatch')
class Profile(UpdateView):
    template_name = 'accounts/profile.html'
    form_class = SafetyInUserForm
    success_url = reverse_lazy('Profile')

    def get_object(self):
        return get_object_or_404(SafetyInUser, email=self.request.user.email)

    def get_queryset(self):
        return SafetyInUser.objects.filter(id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.request.user,
                                          initial={'first_name': self.request.user.first_name,
                                                   'last_name': self.request.user.last_name,
                                                   'username': self.request.user.username,
                                                   'email': self.request.user.email,
                                                   'telephone': self.request.user.telephone,
                                                   'is_volunteer': self.request.user.is_volunteer})
        return context

    def get(self, request, *args, **kwargs):
        super(Profile, self).get(request, *args, **kwargs)
        form = self.form_class
        return self.render_to_response(self.get_context_data(
            object=self.request.user.id, form=form))

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()

        return super(Profile, self).form_valid(form)

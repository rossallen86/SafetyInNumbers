from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic.edit import UpdateView, CreateView, FormView
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from safety_in_numbers.forms import SafetyInUserForm, TransitForm, EmailForm
from safety_in_numbers.models import SafetyInUser, Transit, JoinedTransit


@method_decorator(login_required, name='dispatch')
class Index(View):

    def get(self, request):
        return redirect('My_Transits')

    def post(self, request):
        return redirect('My_Transits')


@method_decorator(login_required, name='dispatch')
class Profile(UpdateView):
    template_name = 'accounts/profile.html'
    form_class = SafetyInUserForm
    success_url = reverse_lazy('My_Transits')

    def get_queryset(self):
        return SafetyInUser.objects.filter(id=self.request.user.id)

    def get_object(self, queryset=None):
        return get_object_or_404(SafetyInUser, id=self.request.user.id)

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


@method_decorator(login_required, name='dispatch')
class CreateTransit(CreateView):
    template_name = 'transit/create_transit.html'
    form_class = TransitForm
    success_url = reverse_lazy('My_Transits')

    def form_valid(self, form):
        transit_obj = form.save(commit=False)
        transit_obj.save()
        me = SafetyInUser.objects.get(id=self.request.user.id)
        trans = Transit.objects.get(id=transit_obj.id)
        JoinedTransit.objects.create(safety_in_user=me,
                                     transit=trans)
        return super(CreateTransit, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class MyTransits(ListView):
    template_name = 'transit/my_transits.html'
    context_object_name = 'my_transits'

    def get_queryset(self):
        if JoinedTransit.objects.filter(safety_in_user=self.request.user.id).exists():
            my_joined_trans = JoinedTransit.objects.filter(safety_in_user=self.request.user.id)
            joined_trans_ids = []
            for t in my_joined_trans:
                joined_trans_ids.append(t.transit_id)
            return Transit.objects.filter(id__in=joined_trans_ids)
        else:
            return None

    def delete(self, transit_id=None):
        transit_obj = Transit.objects.get(id=transit_id)
        transit_obj.delete()
        return redirect('My_Transits')


@method_decorator(login_required, name='dispatch')
class JoinTransits(ListView):
    template_name = 'transit/join_transits.html'
    context_object_name = 'transits'

    def get_queryset(self):
        try:
            other_joined_trans = JoinedTransit.objects.exclude(safety_in_user=self.request.user.id)
            print(other_joined_trans)
            joined_trans_ids = []
            for t in other_joined_trans:
                joined_trans_ids.append(t.transit_id)
            print(joined_trans_ids)
            return Transit.objects.filter(id__in=joined_trans_ids)
        except JoinedTransit.DoesNotExist:
            return None

    def join(self, transit_id=None):
        me = SafetyInUser.objects.get(id=self.user.id)
        transit_obj = Transit.objects.get(id=transit_id)
        JoinedTransit.objects.create(safety_in_user=me, transit=transit_obj)
        return redirect('Join_Transits')


@method_decorator(login_required, name='dispatch')
class Volunteers(ListView):
    template_name = 'volunteers/volunteers.html'
    context_object_name = 'volunteers'

    def get_queryset(self):
        try:
            volunteers = SafetyInUser.objects.filter(is_volunteer=True)
            try:
                volunteers.exclude(id=self.request.user.id)
            finally:
                return volunteers
        except SafetyInUser.DoesNotExist:
            return None


@method_decorator(login_required, name='dispatch')
class ContactVolunteer(FormView):
    template_name = 'volunteers/contact_volunteer.html'
    form_class = EmailForm

    def get_context_data(self, **kwargs):
        volunteer_id = self.kwargs['volunteer_id']
        context = super(ContactVolunteer, self).get_context_data(**kwargs)
        volunteer_email = SafetyInUser.objects.get(id=volunteer_id).email
        context['form'] = self.form_class(initial={'from_email': self.request.user,
                                                   'to_email': volunteer_email})
        return context

    def form_valid(self, form):
        try:
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['body']
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [form.cleaned_data['to_email']]
            send_mail(subject, message, email_from, recipient_list)
            return redirect('My_Transits')
        finally:
            print('failed to send email')
            return redirect('volunteers')

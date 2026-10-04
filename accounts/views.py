from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm
from .models import CustomUser, Profile


class SignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('shop:all_products')

    def form_valid(self, form):
        response = super().form_valid(form)

        customer_group, created = Group.objects.get_or_create(
            name='Customer'
        )

        self.object.groups.add(customer_group)
        login(self.request, self.object)

        return response


class ProfileEditView(UpdateView):
    model = Profile
    template_name = 'registration/edit_profile.html'
    fields = ['date_of_birth', 'fav_author']


class ProfilePageView(DetailView):
    model = Profile
    template_name = 'registration/user_profile.html'
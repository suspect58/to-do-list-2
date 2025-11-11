from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView #all these are built in fuctions
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin #restrict the user from accessing pages without logging in.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login  #log the user in directly after registration.

# Imports for Reordering Feature
from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from .models import Task
from .forms import PositionForm

# Create your views here.
class CustomLoginView(LoginView):
  template_name = 'base/login.html'
  fields = '__all__'
  redirect_authenticated_user = True #redirect authenticated user 

  def get_success_url(self):
    return reverse_lazy('tasks')
  
class RegisterPage(FormView):
  template_name = 'base/register.html'
  form_class = UserCreationForm #using django in built creation form
  redirect_authenticated_user = True #redirect authenticated user # seems not to be working we are manually overwriting it
  success_url = reverse_lazy('tasks')

  def form_valid(self, form): #passing the registration form. 
    user = form.save()
    if user is not None:
      login(self.request, user)
    return super(RegisterPage, self).form_valid(form)

  def get(self, *args, **kwargs): #manual overwrite of authenticated user redirecting
    if self.request.user.is_authenticated:
      return redirect('tasks')
    return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
  model = Task
  context_object_name = 'tasks'

  def get_context_data(self, **kwargs):   # ensure the user logged in sees his own data only
    context = super().get_context_data(**kwargs)
    context['tasks'] = context['tasks'].filter(user=self.request.user)  #to only get the users tasks
    context['count'] = context['tasks'].filter(complete=False).count()  #to count incomplete tasks 

    search_input = self.request.GET.get('search-area') or '' #for the search fuctionality
    if search_input:
      context['tasks'] = context['tasks'].filter(
        title__startswith=search_input)

    context['search_input'] = search_input  

    return context

class TaskDetail(LoginRequiredMixin, DetailView):
  model = Task
  context_object_name = 'task' #modify object name otherwise we would use objectname in the template
  template_name = 'base/task.html' 

class TaskCreate(LoginRequiredMixin, CreateView):
  model = Task
  fields = ['title', 'description', 'complete']
  success_url = reverse_lazy('tasks') #after submission where to send the user

  def form_valid(self, form):              # to make sure when task is created it automatically gets user.
    form.instance.user = self.request.user
    return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
  model = Task
  fields = ['title', 'description', 'complete'] #the fields which will be visible in the template
  success_url = reverse_lazy('tasks')  

class DeleteView(LoginRequiredMixin, DeleteView):
  model = Task
  context_object_name ='task'  
  success_url = reverse_lazy('tasks')  

class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))  

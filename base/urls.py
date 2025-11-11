from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, DeleteView, CustomLoginView, RegisterPage, TaskReorder
from django.contrib.auth.views import LogoutView # we call the logoutview here 


urlpatterns = [
  path('login/', CustomLoginView.as_view(), name ='login'),
  path('logout/', LogoutView.as_view(next_page='login'), name ='logout'),# "next_page" where the user is sent after logout
  path('register/', RegisterPage.as_view(), name ='register'),
  
  path('', TaskList.as_view(), name ='tasks'),
  path('task/<int:pk>/', TaskDetail.as_view(), name ='task'),
  path('task-create/', TaskCreate.as_view(), name ='task-create'),
  path('task-update/<int:pk>/', TaskUpdate.as_view(), name ='task-update'), # pk gives every task a primary key to indetify a specific task
  path('task-delete/<int:pk>/', DeleteView.as_view(), name ='task-delete'),
  path('task-reorder/', TaskReorder.as_view(), name='task-reorder'),
]
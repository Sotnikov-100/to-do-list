from django.views import generic

from tasks.models import Task


class TaskListView(generic.ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory, TestCase
from django.urls import reverse

from tasks.models import Tag, Task
from tasks.views import toggle_task_status


class TaskViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.task = Task.objects.create(content="Test task", is_done=False)
        cls.tag = Tag.objects.create(name="Test tag")

    def test_task_list_view(self):
        response = self.client.get(reverse("tasks:task-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_list.html")
        self.assertContains(response, "Test task")

    def test_task_create_view(self):
        response = self.client.post(
            reverse("tasks:task-create"),
            {"content": "New task", "is_done": False, "tags": [self.tag.id]},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(content="New task").exists())

    def test_toggle_task_status(self):
        factory = RequestFactory()
        request = factory.get("/fake-url/")

        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)

        response = toggle_task_status(request, self.task.id)
        self.assertEqual(response.status_code, 302)
        updated_task = Task.objects.get(id=self.task.id)
        self.assertTrue(updated_task.is_done)

    def test_tag_list_view(self):
        response = self.client.get(reverse("tasks:tag-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/tag_list.html")
        self.assertContains(response, "Test tag")

    def test_tag_create_view(self):
        response = self.client.post(reverse("tasks:tag-create"), {"name": "New tag"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Tag.objects.filter(name="New tag").exists())

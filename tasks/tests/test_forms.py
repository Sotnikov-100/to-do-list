from django.test import TestCase
from django.utils import timezone

from tasks.forms import TagForm, TaskForm
from tasks.models import Tag


class FormsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tag = Tag.objects.create(name="Test Tag")

    def test_task_form_valid_data(self):
        print("\nTesting TaskForm with valid data...")
        future_date = timezone.now() + timezone.timedelta(days=1)
        form_data = {
            "content": "Test task content",
            "deadline": future_date.strftime("%Y-%m-%dT%H:%M"),
            "tags": [self.tag.id],
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())
        task = form.save()
        self.assertEqual(task.content, "Test task content")
        self.assertEqual(task.tags.first(), self.tag)
        print("TaskForm valid data test - OK")

    def test_task_form_empty_content(self):
        print("\nTesting TaskForm with empty content...")
        form_data = {"content": "", "deadline": "", "tags": []}
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)
        print("TaskForm empty content test - OK")

    def test_task_form_past_deadline(self):
        print("\nTesting TaskForm with past deadline (should be valid)...")
        past_date = timezone.now() - timezone.timedelta(days=1)
        form_data = {
            "content": "Test task",
            "deadline": past_date.strftime("%Y-%m-%dT%H:%M"),
            "tags": [self.tag.id],
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())
        if form.is_valid():
            task = form.save()
            self.assertEqual(task.content, "Test task")
            self.assertTrue(task.deadline < timezone.now())
        print("TaskForm with past deadline is valid - OK")

    def test_tag_form_valid_data(self):
        print("\nTesting TagForm with valid data...")
        form_data = {"name": "New Tag"}
        form = TagForm(data=form_data)
        self.assertTrue(form.is_valid())
        tag = form.save()
        self.assertEqual(tag.name, "New Tag")
        print("TagForm valid data test - OK")

    def test_tag_form_empty_name(self):
        print("\nTesting TagForm with empty name...")
        form_data = {"name": ""}
        form = TagForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        print("TagForm empty name test - OK")

    def test_tag_form_duplicate_name(self):
        print("\nTesting TagForm with duplicate name...")
        Tag.objects.create(name="Existing Tag")

        form_data = {"name": "Existing Tag"}
        form = TagForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        print("TagForm duplicate name test - OK")

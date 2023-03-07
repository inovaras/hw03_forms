from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms
from django.conf import settings

from ..models import User, Group,  Post


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='author')
        cls.group = Group.objects.create(slug='slug')
        cls.another_group = Group.objects.create(slug='another_slug')
        cls.post = Post.objects.create(
            text='Тут какой-то текст:)',
            author=cls.user,
            group=cls.group
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={'slug': self.group.slug}): 'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': self.user.username}): 'posts/profile.html',
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}): 'posts/post_detail.html',
            reverse('posts:create'): 'posts/create.html',
            reverse('posts:edit', kwargs={'post_id': f'{self.post.id}'}):'posts/create.html'
        }

        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def check_context(self, post):
        self.assertEqual(post.text, self.post.text)
        self.assertEqual(post.author, self.post.author)
        self.assertEqual(post.group, self.post.group)

    def test_index_pages_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = (self.authorized_client.
                    get(reverse('posts:profile', kwargs={'username': self.user.username})))
        post = response.context['page_obj'][0]
        self.check_context(post)

    def test_group_posts_pages_show_correct_context(self):
        """Шаблон group_post сформирован с правильным контекстом."""
        response = (self.authorized_client.
                    get(reverse('posts:group_list', kwargs={'slug': self.group.slug})))
        post = response.context['page_obj'][0]
        self.check_context(post)
        group = response.context['group']
        self.assertEqual(group.slug, self.group.slug)

    def test_profile_pages_show_correct_context(self):
        """Шаблон group_post сформирован с правильным контекстом."""
        response = (self.authorized_client.
                    get(reverse('posts:profile', kwargs={'username': self.user.username})))
        post = response.context['page_obj'][0]
        self.check_context(post)
        self.assertEqual(post.author, self.user)

    def test_post_detail_pages_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = (self.authorized_client.
                    get(reverse('posts:post_detail', kwargs={'post_id': self.post.id})))
        post = response.context['post']
        self.check_context(post)

    def test_post_create_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_edit_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:edit', kwargs={'post_id': f'{self.post.id}'}))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }
        # Проверяем, что типы полей формы в словаре context соответствуют ожиданиям
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_doesnt_appear_in_another_group(self):
        response = (self.authorized_client.
                    get(
            reverse('posts:group_list', kwargs={'slug': self.another_group.slug})))
        posts = response.context['page_obj']
        self.assertEqual(len(posts), 0)

class PaginatorViewsTest(TestCase):
    pass


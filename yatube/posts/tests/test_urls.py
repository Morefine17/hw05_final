from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Group, Post

User = get_user_model()


class PostURLTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тест групп',
            slug='test-slug'
        )
        cls.user_more = User.objects.create_user(username='test')
        cls.user = User.objects.create_user(username='author')
        cls.post = Post.objects.create(
            text='Какой то текст',
            author=cls.user,
            group=cls.group
        )
        cls.post_more = Post.objects.create(
            text='ещё 1 пост',
            author=cls.user_more,
            group=None
        )
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.guest_client = Client()

    def test_availability_check_all(self):
        """Проверка доступности стр. неавтор-му польз-ю"""
        list_html_status = {
            '/': 200,
            '/group/test-slug/': 200,
            '/profile/author/': 200,
            '/posts/1/': 200,
        }
        for adress, status_code in list_html_status.items():
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                self.assertEqual(response.status_code, status_code)

    def test_urls_current_use_template(self):
        """Проверка использования шаблонов для страниц"""
        templates_urls_use = {
            '/group/test-slug/': 'posts/group_list.html',
            '/profile/author/': 'posts/profile.html',
            '/posts/1/': 'posts/post_detail.html',
            '/create/': 'posts/post_create.html',
            '/posts/1/edit/': 'posts/post_create.html'
        }
        for adress, template in templates_urls_use.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template)

    def test_availability_check_404(self):
        """Проверка при переходе по несуществующему url"""
        adress_404 = '/unexisting_page/'
        response = self.guest_client.get(adress_404)
        self.assertEqual(response.status_code, 404)

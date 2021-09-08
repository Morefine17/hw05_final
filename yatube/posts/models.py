from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


class Group(models.Model):
    title = models.CharField("Название группы", max_length=200,
                             help_text='Создайте название группы')
    description = models.TextField("Описание группы")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField("Текст", help_text='Поле для текста')
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(User, verbose_name="Автор",
                               on_delete=models.CASCADE,
                               related_name="posts")
    group = models.ForeignKey(Group, verbose_name="Группа",
                              help_text='Поле группы',
                              on_delete=models.SET_NULL,
                              blank=True, null=True, related_name='posts')
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True,
        help_text='Изображение, которое относится к посту'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    post = models.ForeignKey(Post, verbose_name='Комментарий',
                             on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey(User, verbose_name='Автор',
                               on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField('Текст', help_text='Поле ввода комментария')
    created = models.DateTimeField('Дата и время публикации комментария',
                                   auto_now_add=True)

    class Meta:
        ordering = ('post',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    user = models.ForeignKey(User, verbose_name='Подписчик',
                             on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(User, verbose_name='Издатель',
                               on_delete=models.CASCADE,
                               related_name='following')

    class Meta:
        verbose_name = 'Фалловер'
        verbose_name_plural = 'Фалловеры'
        UniqueConstraint(fields=['user', 'author'],
                         name='uniq_follow_following')

from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Адресный идентификатор')
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name

class Profile(models.Model):
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
    avatar = CloudinaryField(blank=True, null=True, verbose_name='Аватар')
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='profile')
    short_bio = models.TextField(verbose_name='Краткая биография')
    rating = models.DecimalField(verbose_name='Рейтинг', default=1.0, validators=[
        MinValueValidator(1.0),
        MaxValueValidator(10.0)],max_digits=3, decimal_places=2)
    proposals_count = models.IntegerField(default=0, verbose_name='Количество предложений')
    completed_lessons_count = models.IntegerField(default=0, verbose_name='Количество завершённых занятий')

    def __str__(self):
        return self.user.username

class Review(models.Model):
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
    review = models.TextField(verbose_name='Текст отзыва')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    uploaded_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор отзыва', related_name='reviews')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Профиль', related_name='reviews', null=True, blank=True)
    rating = models.DecimalField(verbose_name='Оценка', default=1.0, validators=[
        MinValueValidator(1.0),
        MaxValueValidator(5.0)
    ],max_digits=3, decimal_places=2)
    proposal = models.ForeignKey('SkillProposal', on_delete=models.CASCADE, related_name='reviews', null=True, blank=True, verbose_name='Предложение')
    lesson_request = models.OneToOneField('LessonRequest', on_delete=models.CASCADE, related_name='review', null=True, blank=True, verbose_name='Запрос на занятие')
    def __str__(self):
        return self.review

class SkillProposal(models.Model):
    class Meta:
        verbose_name = 'Предложение навыка'
        verbose_name_plural = 'Предложения навыков'
    class Levels(models.TextChoices):
        BEGINNER = 'beginner', 'Начальный',
        INTERMEDIATE = 'intermediate', 'Средний',
        Advanced = 'advanced', 'Продвинутый',
    class Format(models.TextChoices):
        ONLINE = 'online', 'Онлайн',
        OFFLINE = 'offline', 'Очно',
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Черновик'
        PENDING = 'pending', 'На проверке'
        PUBLISHED = 'published', 'Опубликовано'
        REJECTED = 'rejected', 'Отклонено'
    name = models.CharField(max_length=100, verbose_name='Название')
    image = CloudinaryField(blank=True, null=True, verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    uploaded_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    rating = models.DecimalField(verbose_name='Рейтинг', default=1.0, validators=[
        MinValueValidator(1.0),
        MaxValueValidator(5.0)
    ], max_digits=3, decimal_places=2)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name='Категория',
        related_name='skill_proposals')
    level = models.CharField(choices=Levels.choices, default=Levels.BEGINNER, max_length=15, verbose_name='Уровень')
    online = models.CharField(choices=Format.choices, default=Format.ONLINE, max_length=15, verbose_name='Формат')
    lesson_duration = models.IntegerField(default=1, verbose_name='Длительность занятия', validators=[
        MinValueValidator(1)
    ])
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='skill_proposals')
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING, verbose_name='Статус')
    def __str__(self):
        return self.name

class Favorites(models.Model):
    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные предложения'
    proposal = models.ForeignKey(SkillProposal, on_delete=models.CASCADE, related_name='favorites', verbose_name='Предложение')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name='Пользователь')


class LessonRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Ожидает ответа'
        ACCEPTED = 'accepted', 'Принят'
        REJECTED = 'rejected', 'Отклонён'
        COMPLETED = 'completed', 'Завершён'
        CANCELLED = 'cancelled', 'Отменён'

    proposal = models.ForeignKey(SkillProposal, on_delete=models.CASCADE, related_name='lesson_requests', verbose_name='Предложение')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_requests', verbose_name='Ученик')
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING, verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['proposal', 'student'], condition=models.Q(status__in=['pending', 'accepted']),
            name='one_active_lesson_request',
        )]

    def __str__(self):
        return f'{self.student} - {self.proposal}'

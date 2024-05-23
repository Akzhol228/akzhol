from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class CityProblem(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    location = models.CharField(max_length=255, blank=True, verbose_name="Местоположение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='city_problems', verbose_name="Автор")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категория")
    collected_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,
                                           verbose_name="Собранная сумма")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Необходимая сумма")

    def __str__(self):
        return self.title

    def progress_percentage(self):
        if self.total_amount > 0:
            return (self.collected_amount / self.total_amount) * 100
        return 0

    class Meta:
        verbose_name = "IT проект"
        verbose_name_plural = "IT проекты"

class Donation(models.Model):
    city_problem = models.ForeignKey(CityProblem, on_delete=models.CASCADE, related_name='donations')
    name = models.CharField(max_length=100, verbose_name="Имя")
    phone_number = models.CharField(max_length=15, verbose_name="Номер телефона")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")

    def __str__(self):
        return f"{self.name} - {self.amount} для {self.city_problem.title}"

    class Meta:
        verbose_name = "Инвестор"
        verbose_name_plural = "Инвесторы"

class SolutionProposal(models.Model):
    problem = models.ForeignKey(CityProblem, on_delete=models.CASCADE, related_name='solutions', verbose_name="IT проект")
    description = models.TextField(verbose_name="Описание идеи")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solutions', verbose_name="Автор идеи")
    votes = models.IntegerField(default=0, verbose_name="Голоса")

    def __str__(self):
        return f"Solution by {self.author.username} for problem: {self.problem.title}"

    class Meta:
        verbose_name = "Предложение идеи"
        verbose_name_plural = "Предложения идей"

class Vote(models.Model):
    solution = models.ForeignKey(SolutionProposal, on_delete=models.CASCADE, related_name='vote_set', verbose_name="Решение")
    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes', verbose_name="Голосующий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата голосования")
    value = models.IntegerField(default=1, verbose_name="Значение голоса")

    class Meta:
        unique_together = ('solution', 'voter')
        verbose_name = "Голос"
        verbose_name_plural = "Голоса"

class Finalist(models.Model):
    solution = models.OneToOneField(SolutionProposal, on_delete=models.CASCADE, related_name='finalist_status', verbose_name="Решение")
    votes_in_final = models.IntegerField(default=0, verbose_name="Голоса в финале")

    def __str__(self):
        return f"Finalist: {self.solution.description}"

    class Meta:
        verbose_name = "Финалист"
        verbose_name_plural = "Финалисты"


class Poll(models.Model):
    question = models.TextField(verbose_name="Вопрос")

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"

class Answer(models.Model):
    poll = models.ForeignKey(Poll, related_name='answers', on_delete=models.CASCADE, verbose_name="Опрос")
    answer_text = models.CharField(max_length=255, verbose_name="Текст ответа")
    votes = models.PositiveIntegerField(default=0, verbose_name="Количество голосов")

    def __str__(self):
        return f"{self.answer_text} ({self.votes} голосов)"

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"



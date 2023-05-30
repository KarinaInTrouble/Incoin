from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils import timezone

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    name = models.CharField(max_length=255, verbose_name='Название проекта')
    description = models.TextField(max_length=255, verbose_name="Описание", blank=True)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        db_table = 'projects'
    
    def __str__ (self):
        return self.name


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    name = models.CharField(max_length=255, verbose_name='Название категории')
    icon = models.ImageField(upload_to='category_icons/', verbose_name='Иконка', blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'categories'
    
    def __str__ (self):
        return self.name


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],
    verbose_name='Сумма дохода')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Проект')
    description = models.CharField(max_length=255, verbose_name="Описание", blank=True)
    date = models.DateField(default=timezone.now, verbose_name='Дата')

    class Meta:
        verbose_name = 'Доход'
        verbose_name_plural = 'Доходы'
        db_table = 'incomes'
    
    def __str__ (self):
        return str(self.amount)


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],
    verbose_name='Сумма расхода')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Проект')
    description = models.CharField(max_length=255, verbose_name="Описание", blank=True)
    date = models.DateField(default=timezone.now, verbose_name='Дата')

    class Meta:
        verbose_name = 'Расход'
        verbose_name_plural = 'Расходы'
        db_table = 'expenses'

class Urgency(models.Model):
    name = models.CharField(max_length=255, verbose_name='Степень срочности')

    class Meta:
        verbose_name = 'Срочность'
        verbose_name_plural = 'Срочность'
        db_table = 'urgencies'

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    title = models.CharField(max_length=255, verbose_name='Название задачи')
    description = models.TextField(verbose_name='Описание задачи')
    date = models.DateField(validators=[MinValueValidator(timezone.now().date())], verbose_name='Дата выполнения задачи')
    urgency = models.ForeignKey(Urgency, on_delete=models.CASCADE, verbose_name='Срочность')

    class Meta:
        verbose_name = 'задача'
        verbose_name_plural = 'задачи'
        db_table = 'tasks'



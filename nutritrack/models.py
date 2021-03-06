from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Nutrient(models.Model):
    kcal = models.IntegerField(default=0)
    fat = models.FloatField(default=0)
    carb = models.FloatField(default=0)
    sugar = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    sodium = models.FloatField(default=0)
    vA = models.FloatField(default=0)
    vC = models.FloatField(default=0)
    iron = models.FloatField(default=0)
    calcium = models.FloatField(default=0)

    def __str__(self):
        return f'{self.kcal} kcal, {self.fat} g total fat, {self.carb} g total carbohydrate, {self.sugar} g sugars, ' \
               f'{self.protein} g protein, {self.sodium} mg sodium, {self.vA}% Vitamin A, {self.vC}% Vitamin C, ' \
               f'{self.iron}% Iron, {self.calcium}% Calcium '

    def __add__(self, other):
        self.kcal += other.kcal
        self.fat += other.fat
        self.carb += other.carb
        self.sugar += other.sugar
        self.protein += other.protein
        self.sodium += other.sodium
        self.vA += other.vA
        self.vC += other.vC
        self.iron += other.iron
        self.calcium += other.calcium
        return self

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            self.kcal *= other.kcal
            self.fat *= other.fat
            self.carb *= other.carb
            self.sugar *= other.sugar
            self.protein *= other.protein
            self.sodium *= other.sodium
            self.vA *= other.vA
            self.vC *= other.vC
            self.iron *= other.iron
            self.calcium *= other.calcium
        else:
            self.kcal *= other
            self.fat *= other
            self.carb *= other
            self.sugar *= other
            self.protein *= other
            self.sodium *= other
            self.vA *= other
            self.vC *= other
            self.iron *= other
            self.calcium *= other
        return self


class Ingredient(models.Model):
    name = models.CharField(max_length=256, default='')
    amount = models.FloatField()

    def __str__(self):
        return f'{self.name} - {self.amount} g'


class Meal(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, default='')
    description = models.TextField(default='')
    ingredients = models.ManyToManyField(Ingredient)
    servings = models.FloatField(default=1)
    nutrients = models.ForeignKey(Nutrient, blank=True, default=None)

    def __str__(self):
        return self.name


class MealReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    meal = models.ForeignKey(Meal)
    amount = models.FloatField(default=1)

    def __str__(self):
        return f'{self.timestamp} - {self.user.username} - {self.meal.name}'


ACTIVITY_CHOICES = (
    (0, 'sedentary'),
    (1, 'lightly active'),
    (2, 'moderately active'),
    (3, 'pretty active'),
    (4, 'extraordinarily active'),
)

SEX_CHOICES = (
    (0, 'male'),
    (1, 'female')
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(blank=True, default=18)
    sex = models.IntegerField(choices=SEX_CHOICES, default=0)
    height = models.FloatField(blank=True, default=170)
    weight = models.FloatField(blank=True, default=60)
    activity_level = models.IntegerField(choices=ACTIVITY_CHOICES, default=0)

    @property
    def bmi(self):
        try:
            return self.weight / (self.height / 100) ** 2
        except ZeroDivisionError:
            return 0

    @property
    def bmr(self):
        try:
            if self.sex == 0:
                out = 66 + (13.7 * self.weight) + (5 * self.height) - (6.8 * self.age)
            else:
                out = 655 + (9.6 * self.weight) + (1.8 * self.height) - (4.7 * self.age)
            return out * (0.7 / 4 * self.activity_level + 1.2)
        except ZeroDivisionError:
            return 0


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

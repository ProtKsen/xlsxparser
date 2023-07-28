from django.db import models


class City(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "cities"


class MonthYear(models.Model):
    month = models.DateField(unique=True)

    class Meta:
        verbose_name_plural = "months"


class Billboard(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    surface_type = models.CharField(max_length=100)
    has_backlight = models.BooleanField()
    side = models.CharField(max_length=5)
    address = models.CharField(max_length=200)
    internal_key = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=17, decimal_places=15)
    longitude = models.DecimalField(max_digits=18, decimal_places=15)
    image_url = models.URLField()
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    number_of_displays = models.IntegerField(blank=True, null=True)
    grp = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    ots = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    aspar_code = models.CharField(max_length=20, null=True)
    month = models.ManyToManyField(
        MonthYear, through="Occupation", through_fields=("billboard", "month")
    )
    fabric = models.CharField(max_length=200, null=True)
    restrictions = models.CharField(null=True)
    district = models.CharField(null=True)
    technical_requirements = models.URLField(null=True)
    price_per_installation = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    price_per_update = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    permitted_until = models.DateField(null=True)
    comment = models.CharField(null=True)


class Occupation(models.Model):
    FREE = "FR"
    SOLD = "SO"
    PARTLY = "PR"
    RESERVED = "RE"
    NOT_INSTALLED = "NI"
    OTHER = "OR"

    OCCUPATION_STATE_CHOICES = [
        (FREE, "free"),
        (SOLD, "sold"),
        (PARTLY, "partly"),
        (RESERVED, "reserved"),
        (NOT_INSTALLED, "not installed"),
        (OTHER, "other"),
    ]

    billboard = models.ForeignKey(Billboard, on_delete=models.CASCADE)
    month = models.ForeignKey(MonthYear, on_delete=models.CASCADE)
    state = models.CharField(choices=OCCUPATION_STATE_CHOICES, default=None)
    comment = models.CharField(null=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["billboard", "month"], name="uniquej")]

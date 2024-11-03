from django.db import models

from df_cards.fields import (
    AvatarImageField,
    FullImageField,
    IconImageField,
    ThumbnailImageField,
)


class DescriptionMixin(models.Model):
    description = models.TextField(blank=True, default="")

    class Meta:
        abstract = True


class SequenceMixin(models.Model):
    sequence = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True


class ThumbnailMixin(models.Model):
    thumbnail = ThumbnailImageField()

    class Meta:
        abstract = True


class IconMixin(models.Model):
    icon = IconImageField()

    class Meta:
        abstract = True


class FullImageMixin(models.Model):
    full_image = FullImageField()

    class Meta:
        abstract = True


class AvatarMixin(models.Model):
    avatar = AvatarImageField()

    class Meta:
        abstract = True


class BaseCard(DescriptionMixin, SequenceMixin, models.Model):
    class Meta:
        abstract = True


class NamedCard(BaseCard):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

    class Meta:
        abstract = True


class TitledCard(BaseCard):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title

    class Meta:
        abstract = True

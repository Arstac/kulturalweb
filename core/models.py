from django.db import models
from cms.models.pluginmodel import CMSPlugin
from djangocms_text_ckeditor.fields import HTMLField
from cms.models.fields import PageField

class HeroPluginModel(CMSPlugin):
    background_image = models.ImageField(upload_to='hero_images/')
    logo_image = models.ImageField(upload_to='hero_logos/', blank=True, null=True, help_text="Sube un logo para mostrar en lugar del título de texto.")
    title = models.CharField(max_length=255, blank=True, null=True, help_text="Texto del título (si no hay logo) o texto alternativo para el logo.")
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    internal_page = PageField(
        verbose_name="Página interna",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="Si seleccionas una página, este enlace tendrá prioridad sobre la URL externa.",
        related_name='hero_plugin_link'
    )
    button_text = models.CharField(max_length=50, blank=True, null=True)
    button_url = models.URLField(blank=True, null=True, verbose_name="Enlace externo", help_text="Úsalo solo si no has seleccionado una página interna.")

    def __str__(self):
        return self.title or "Hero Header"

class CardPluginModel(CMSPlugin):
    ALIGNMENT_CHOICES = [
        ('left', 'Imagen Izquierda - Texto Derecha'),
        ('right', 'Imagen Derecha - Texto Izquierda'),
    ]

    image = models.ImageField(upload_to='card_images/')
    title = models.CharField(max_length=255)
    description = HTMLField()
    internal_page = PageField(
        verbose_name="Página interna",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="Si seleccionas una página, este enlace tendrá prioridad sobre la URL externa.",
        related_name='card_plugin_link'
    )
    button_text = models.CharField(max_length=50, blank=True, null=True)
    button_url = models.URLField(blank=True, null=True, verbose_name="Enlace externo", help_text="Úsalo solo si no has seleccionado una página interna.")
    alignment = models.CharField(
        max_length=10,
        choices=ALIGNMENT_CHOICES,
        default='left'
    )

    def __str__(self):
        return self.title

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _
from .models import HeroPluginModel, CardPluginModel, EventsGridPluginModel, ShopShowcasePluginModel, CTAPluginModel

@plugin_pool.register_plugin
class HeroPlugin(CMSPluginBase):
    model = HeroPluginModel
    name = _("Hero Header")
    render_template = "core/plugins/hero.html"
    cache = False

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context

@plugin_pool.register_plugin
class CardPlugin(CMSPluginBase):
    model = CardPluginModel
    name = _("Card (Image+Text)")
    render_template = "core/plugins/card.html"
    cache = False

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context

@plugin_pool.register_plugin
class EventsGridPlugin(CMSPluginBase):
    model = EventsGridPluginModel
    name = _("Grilla de Eventos")
    render_template = "core/plugins/events_grid.html"
    cache = False

    def render(self, context, instance, placeholder):
        from eventos.models import Evento
        from django.utils import timezone
        
        now = timezone.now()
        # Eventos futuros ordenados por fecha, limitados por 'count'
        eventos = Evento.objects.filter(fecha__gte=now).order_by('fecha')[:instance.count]
        
        context = super().render(context, instance, placeholder)
        context['eventos'] = eventos
        return context

@plugin_pool.register_plugin
class ShopShowcasePlugin(CMSPluginBase):
    model = ShopShowcasePluginModel
    name = _("Escaparate Tienda")
    render_template = "core/plugins/shop_showcase.html"
    cache = False

    def render(self, context, instance, placeholder):
        from tienda.models import Producto
        
        # Productos activos, ordenados por ID (lo más nuevo al final)
        # Usamos reverse() o -id para los más nuevos primero
        productos = Producto.objects.filter(activo=True).order_by('-id')[:instance.count]
        
        context = super().render(context, instance, placeholder)
        context['productos'] = productos
        return context

@plugin_pool.register_plugin
class CTAPlugin(CMSPluginBase):
    model = CTAPluginModel
    name = _("Call to Action (CTA)")
    render_template = "core/plugins/cta.html"
    cache = False

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context

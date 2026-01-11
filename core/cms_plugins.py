from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _
from .models import HeroPluginModel, CardPluginModel

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

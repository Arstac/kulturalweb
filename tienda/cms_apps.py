from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import gettext_lazy as _

@apphook_pool.register
class TiendaApp(CMSApp):
    app_name = "tienda"
    name = _("Tienda Application")

    def get_urls(self, page=None, language=None, **kwargs):
        return ["tienda.urls"]

from django.views.generic import TemplateView


class SentryErrorView(TemplateView):
    """
    Render a template. Pass keyword arguments from the URLconf to the context.
    """

    def get(self, request, *args, **kwargs):
        division_by_zore = 1 / 0
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

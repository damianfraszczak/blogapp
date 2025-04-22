from django.contrib.sites.shortcuts import get_current_site

from users.models import Company


class MultiTenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            site = get_current_site(request)
            tenant = Company.objects.get(site=site)
        except:
            tenant = None
        request.tenant = tenant
        # domysly kod
        response = self.get_response(request)
        return response

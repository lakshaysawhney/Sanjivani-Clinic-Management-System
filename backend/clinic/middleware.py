import secrets
from django.conf import settings
from django.http import JsonResponse


class ProxyBoundaryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not settings.DEBUG and request.path not in ["/api/health/", "/api/maintenance/"]:
            if not settings.PROXY_SECRET or not secrets.compare_digest(
                request.headers.get("X-Clinic-Proxy", ""), settings.PROXY_SECRET
            ):
                return JsonResponse({"detail": "Use the clinic application origin."}, status=403)
        return self.get_response(request)


class PrivateResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Cache-Control"] = "no-store, private"
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "DENY"
        return response

from django.utils.deprecation import MiddlewareMixin

class AjaxMiddleware(MiddlewareMixin):
    """
    Middleware to add CORS headers for AJAX requests
    """
    def process_response(self, request, response):
        # Add CORS headers for AJAX requests
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-CSRFToken'
        return response

class SameOriginMiddleware(MiddlewareMixin):
    """
    Middleware to ensure CSRF works with fetch API calls
    """
    def process_response(self, request, response):
        # Add security headers for CSRF protection
        response['X-Frame-Options'] = 'SAMEORIGIN'
        response['X-Content-Type-Options'] = 'nosniff'
        return response
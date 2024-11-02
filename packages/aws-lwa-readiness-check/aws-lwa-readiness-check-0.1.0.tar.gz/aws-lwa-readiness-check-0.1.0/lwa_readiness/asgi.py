"""
ASGI middleware for handling AWS Lambda Web Adapter readiness check requests.

This module provides middleware that intercepts HTTP requests to a configurable path
and returns an empty HTTP 200 response.

Environment Variables:
    AWS_LWA_READINESS_CHECK_PATH: The URL path to intercept (e.g., "/lwa-readiness-check")

Example:
    To use this middleware with any ASGI application:

    ```python
    from lwa_readiness.asgi import ReadinessCheckMiddleware
    
    app = ReadinessCheckMiddleware(your_asgi_app())
    ```
"""

import os


class ReadinessCheckMiddleware:
    """
    ASGI middleware that handles readiness check requests by returning an HTTP 200 response.
    
    This middleware intercepts requests to a configured path and returns an immediate
    HTTP 200 response without forwarding the request to the wrapped application.
    All other requests are passed through to the wrapped application unchanged.
    """

    def __init__(self, app):
        """
        Initialize the middleware with the wrapped ASGI application.

        Args:
            app: The ASGI application to wrap.

        Raises:
            ValueError: If AWS_LWA_READINESS_CHECK_PATH environment variable is not set.
        """
        self.app = app
        self.health_check_path = os.environ.get('AWS_LWA_READINESS_CHECK_PATH')

        if not self.health_check_path:
            raise ValueError(
                'Environment variable AWS_LWA_READINESS_CHECK_PATH must be set'
            )

    async def __call__(self, scope, receive, send):
        """
        Process an incoming ASGI request.

        If the request matches the configured health check path, returns an immediate
        HTTP 200 response. Otherwise, forwards the request to the wrapped application.

        Args:
            scope: The ASGI connection scope.
            receive: The ASGI receive channel.
            send: The ASGI send channel.

        Returns:
            None
        """

        # Check if this is a health check request
        if scope['type'] == 'http' and scope['path'] == self.health_check_path:
            # Send HTTP 200 response headers
            await send({
                'type': 'http.response.start',
                'status': 200,
                'headers': [
                    (b'content-type', b'application/json'),
                    (b'content-length', b'0')
                ]
            })
            # Send empty response body
            await send({
                'type': 'http.response.body',
                'body': b'',
                'more_body': False
            })
            return

        # Not a health check request, pass through to the wrapped application
        await self.app(scope, receive, send)

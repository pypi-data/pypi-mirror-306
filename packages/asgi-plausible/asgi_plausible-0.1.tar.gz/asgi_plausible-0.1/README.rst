==============
asgi-plausible
==============

Provides an asgi middleware for request to plausible.io.

The middleware

- should make it harder to generally block requests to plausible.io
- while masking ip addresses to overall achieve more privacy for clients
- handles requests asynchronously, so they may fail.

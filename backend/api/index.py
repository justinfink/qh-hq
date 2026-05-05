"""Vercel Python serverless entrypoint. FastAPI app exposed as ASGI handler.

Vercel routes all /api/* requests here via the parent vercel.json rewrite.
"""
from app.main import app

# Vercel Python runtime auto-detects the `app` ASGI callable.
handler = app

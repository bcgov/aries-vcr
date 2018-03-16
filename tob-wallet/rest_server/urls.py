"""rest server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""
from django.conf.urls import url, include
from django.conf.urls import include

urlpatterns = [
    # the next line is for DRF tokens, comment out for JWT tokens
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api/v1/', include('api.urls')),
]

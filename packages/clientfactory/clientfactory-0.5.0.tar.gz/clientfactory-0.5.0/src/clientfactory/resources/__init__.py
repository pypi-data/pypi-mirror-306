# resources/__init__.py
from .base import Resource, ResourceConfig
from .decorators import resource, get, post, put, patch, delete, preprocess, postprocess

__all__ = [
    'Resource', 'ResourceConfig',
    'resource', 'get', 'post', 'put', 'patch', 'delete',
    'preprocess', 'postprocess'
]

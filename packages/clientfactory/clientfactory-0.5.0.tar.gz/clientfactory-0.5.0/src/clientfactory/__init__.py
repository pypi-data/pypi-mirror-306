# ~/clientfactory/src/clientfactory/__init__.py
"""
ClientFactory
------------
A framework for building API clients with minimal boilerplate.
"""

__version__ = "0.5.0"
__author__ = "Joel Yisrael"
__license__ = "MIT"

# Core exports
from .client import Client
from .builder import ClientBuilder

# Auth exports
from .auth import (
    BaseAuth,
    OAuth2Auth,
    SessionAuth,
    ApiKeyAuth,
    TokenAuth,
    BasicAuth,
    NoAuth
)

# Resource exports
from .resources import (
    resource,
    get,
    post,
    put,
    patch,
    delete,
    preprocess,
    postprocess
)

# Session exports
from .session import (
    BaseSession,
    SessionConfig,
    DiskPersist,
    MemoryPersist
)

# Utils exports
from .utils import (
    Request,
    Response,
    RequestMethod,
    FileUpload,
    UploadConfig
)

# Define what's available on import *
__all__ = [
    'Client',
    'ClientBuilder',
    # Auth
    'BaseAuth',
    'OAuth2Auth',
    'SessionAuth',
    'ApiKeyAuth',
    'TokenAuth',
    'BasicAuth',
    'NoAuth',
    # Resources
    'resource',
    'get',
    'post',
    'put',
    'patch',
    'delete',
    'preprocess',
    'postprocess',
    # Session
    'BaseSession',
    'SessionConfig',
    'DiskPersist',
    'MemoryPersist',
    # Utils
    'Request',
    'Response',
    'RequestMethod',
    'FileUpload',
    'UploadConfig'
]

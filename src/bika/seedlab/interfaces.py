# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IBikaSeedlabLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IGrades(Interface):
    """Marker interface for grades setup folder
    """


class IGrade(Interface):
    """Marker interface for grade
    """


class ICertifications(Interface):
    """Marker interface fo certifications setup folder
    """


class ICertification(Interface):
    """Marker interface for certification
    """

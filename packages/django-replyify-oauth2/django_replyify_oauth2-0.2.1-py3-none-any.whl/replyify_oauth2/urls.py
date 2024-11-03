#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#
from __future__ import unicode_literals
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^authorize/', views.authorize, name='authorize'),
    re_path(r'^callback/', views.callback, name='callback'),
    re_path(r'^refresh/', views.refresh, name='refresh'),
    re_path(r'^$', views.index, name='index'),
]

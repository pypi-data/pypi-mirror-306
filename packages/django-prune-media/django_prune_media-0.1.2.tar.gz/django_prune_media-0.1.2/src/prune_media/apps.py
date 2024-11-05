# apps.py
#
# Copyright (c) 2024 Daniel Andrlik
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from django.apps import AppConfig
from django.core.checks import Error, register
from django.core.files.storage import default_storage


class PruneMediaConfig(AppConfig):
    name = "prune_media"


@register()
def check_for_media(app_configs, **kwargs):  # noqa: ARG001
    errors = []
    try:
        dirs, files = default_storage.listdir(".")
    except FileNotFoundError as fnf:
        msg = "Your media root does not exist!"
        errors.append(Error(msg, hint=str(fnf)))
    except NotImplementedError as nie:
        msg = "Your storage backend does not support listdir!"
        errors.append(Error(msg, hint=str(nie)))
    return errors

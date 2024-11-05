# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at http://www.comet.com
#  Copyright (C) 2015-2024 Comet ML INC
#  This source code is licensed under the MIT license.
# *******************************************************
import logging
import os
from typing import Callable

from comet_ml import authhook

from requests import Session

LOGGER = logging.getLogger(__name__)


def _in_aws_sagemaker() -> bool:
    return os.getenv("AWS_PARTNER_APP_AUTH") is not None


def _aws_sagemaker_session_hook(auth_provider) -> Callable[[Session], None]:

    def _aws_session_hook(session: Session):
        session.auth = auth_provider.get_auth()

    return _aws_session_hook


def _login_aws_sagemaker() -> None:
    if not _in_aws_sagemaker():
        return

    LOGGER.debug("AWS partner SDK authentication initialization commenced")

    # setup sagemaker partner SDK authentication provider
    from sagemaker import PartnerAppAuthProvider

    auth_provider = PartnerAppAuthProvider()
    authhook.http_session_hook = _aws_sagemaker_session_hook(auth_provider)

    LOGGER.debug("AWS partner SDK authentication initialized")

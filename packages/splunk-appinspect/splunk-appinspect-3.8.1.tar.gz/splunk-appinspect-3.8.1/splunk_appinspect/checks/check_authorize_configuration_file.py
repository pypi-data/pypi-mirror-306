# Copyright 2019 Splunk Inc. All rights reserved.

"""
### Authorize.conf file standards

Ensure that the authorize configuration file located in the **/default** folder is well-formed and valid. For more, see [authorize.conf](https://docs.splunk.com/Documentation/Splunk/latest/Admin/authorizeconf).
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Generator

from splunk_appinspect.check_messages import CheckMessage, FailMessage
from splunk_appinspect.checks import Check, CheckConfig
from splunk_appinspect.constants import Tags
from splunk_appinspect.splunk_defined_authorize_capability_list import (
    SPLUNK_DEFINED_CAPABILITY_NAME,
    SPLUNK_DEFINED_WINDOWS_SPECIFIC_CAPABILITY_NAME,
)

if TYPE_CHECKING:
    from splunk_appinspect import App
    from splunk_appinspect.configuration_file import ConfigurationProxy


logger = logging.getLogger(__name__)


class CheckAuthorizeConfCapabilityNotModified(Check):
    def __init__(self) -> None:
        super().__init__(
            config=CheckConfig(
                name="check_authorize_conf_capability_not_modified",
                description="Check that authorize.conf does not contain any modified capabilities. ",
                tags=(
                    Tags.SPLUNK_APPINSPECT,
                    Tags.CLOUD,
                    Tags.PRIVATE_APP,
                    Tags.PRIVATE_VICTORIA,
                    Tags.MIGRATION_VICTORIA,
                    Tags.PRIVATE_CLASSIC,
                ),
                depends_on_config=("authorize",),
            )
        )

    def check_config(self, app: "App", config: "ConfigurationProxy") -> Generator[CheckMessage, Any, None]:
        for authorize in config["authorize"].sections():
            filename = config["authorize"].get_relative_path()
            if (
                authorize.name.startswith("capability::")
                and authorize.name in SPLUNK_DEFINED_CAPABILITY_NAME | SPLUNK_DEFINED_WINDOWS_SPECIFIC_CAPABILITY_NAME
            ):
                # ONLY fail if the custom capability stanza matches a Splunkwide capability
                lineno = authorize.lineno
                yield FailMessage(
                    f"The following capability was modified: {authorize.name}. "
                    "Capabilities that exist in Splunk Cloud can not be modified. ",
                    file_name=filename,
                    line_number=lineno,
                )


class CheckAuthorizeConfHasNoO11yCapabilities(Check):
    def __init__(self) -> None:
        super().__init__(
            config=CheckConfig(
                name="check_authorize_conf_has_no_o11y_capabilities",
                description="Checks that authorize.conf has no capabilities starting with o11y_.",
                tags=(
                    Tags.SPLUNK_APPINSPECT,
                    Tags.CLOUD,
                    Tags.PRIVATE_APP,
                    Tags.PRIVATE_VICTORIA,
                    Tags.MIGRATION_VICTORIA,
                    Tags.PRIVATE_CLASSIC,
                ),
                depends_on_config=("authorize",),
            )
        )

    def check_config(self, app: "App", config: "ConfigurationProxy") -> Generator[CheckMessage, Any, None]:
        for authorize in config["authorize"].sections():
            filename = config["authorize"].get_relative_path()
            if authorize.name.startswith("capability::o11y_"):
                lineno = authorize.lineno
                yield FailMessage(
                    f"Found stanza [{authorize.name}]. Capabilities starting with o11y_ are reserved for o11y.",
                    file_name=filename,
                    line_number=lineno,
                )

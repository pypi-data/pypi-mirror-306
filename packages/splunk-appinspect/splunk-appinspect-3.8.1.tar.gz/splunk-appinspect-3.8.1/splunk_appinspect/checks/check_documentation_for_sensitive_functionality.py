# Copyright 2019 Splunk Inc. All rights reserved.

"""
### Appropriate use of sensitive functionality
"""
import logging
from typing import TYPE_CHECKING

import splunk_appinspect
from splunk_appinspect.constants import Tags

if TYPE_CHECKING:
    from splunk_appinspect import App
    from splunk_appinspect.reporter import Reporter


# TODO: each of these checks should check for the functionality and only
# manual_check if it's used

report_display_order = 51
logger = logging.getLogger(__name__)


@splunk_appinspect.tags(Tags.SPLUNK_APPINSPECT, Tags.MANUAL)
def check_uses_eventgen(app: "App", reporter: "Reporter") -> None:
    """Check that use of 'eventgen.conf' is explained in the app's
    documentation.
    """
    if app.file_exists("default", "eventgen.conf"):
        reporter.manual_check("Documentation will be read during code review.", "default/eventgen.conf")
    else:
        reporter.not_applicable("No eventgen.conf file exists.")


@splunk_appinspect.tags(Tags.SPLUNK_APPINSPECT, Tags.MANUAL)
def check_implements_tscollect(app: "App", reporter: "Reporter") -> None:
    """Check that use of
    ['tscollect'](https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/Tscollect)
    is explained in the app's documentation.
    """
    # TODO: Only in saved searches?
    if app.search_for_pattern("tscollect"):
        reporter.manual_check("Documentation will be read during code review.")
    else:
        reporter.not_applicable("No use of 'tscollect' found.")


@splunk_appinspect.tags(Tags.SPLUNK_APPINSPECT, Tags.MANUAL)
def check_implements_data_models(app: "App", reporter: "Reporter") -> None:
    """Check that the use of datamodels is explained in the app's
    documentation.
    """
    if app.file_exists("default", "datamodels.conf"):
        reporter.manual_check("Documentation will be read during code review.")
    else:
        reporter.not_applicable("No datamodels.conf file exists.")


@splunk_appinspect.tags(Tags.SPLUNK_APPINSPECT, Tags.MANUAL)
def check_implements_inputcsv(app: "App", reporter: "Reporter") -> None:
    """Check that the use of
    [inputcsv](https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/Inputcsv)
    is explained in the app's documentation.
    """
    if app.search_for_pattern("inputcsv"):
        reporter.manual_check("Documentation will be read during code review.")
    else:
        reporter.not_applicable("No use of 'inputcsv' found.")


@splunk_appinspect.tags(Tags.SPLUNK_APPINSPECT, Tags.MANUAL)
def check_implements_outputcsv(app: "App", reporter: "Reporter") -> None:
    """Check that the use of
    [outputcsv](https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/Outputcsv)
    is explained in the app's documentation.
    """
    if app.search_for_pattern("outputcsv"):
        reporter.manual_check("Documentation will be read during code review.")
    else:
        reporter.not_applicable("No use of 'outputcsv' found.")


@splunk_appinspect.tags(Tags.SPLUNK_APPINSPECT, Tags.MANUAL)
def check_initiates_outbound_communications(app: "App", reporter: "Reporter") -> None:
    """Check that any outbound network communications in
    [outputs.conf](https://docs.splunk.com/Documentation/Splunk/latest/Admin/Outputsconf)
    are explained in the app's documentation.
    """
    if app.file_exists("default", "outputs.conf"):
        reporter.manual_check(
            "Can't read documentation, can't scan for outbound connections",
            "default/outputs.conf",
        )
    else:
        reporter.not_applicable("No outputs.conf exists.")


@splunk_appinspect.tags(Tags.SPLUNK_APPINSPECT, Tags.MANUAL)
def check_requires_access_to_files_outside_apps_dir(reporter: "Reporter") -> None:
    """Check that file access outside the app's home directory,
    $SPLUNK_HOME/var/log, $SPLUNK_HOME/var/run, and system temporary directories
    is explained in the app's documentation.
    """
    reporter.manual_check("File access will be inspected during code review.")

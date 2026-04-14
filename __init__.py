# -*- coding: utf-8 -*-
import logging

_logger = logging.getLogger(__name__)

# The original report_name in survey.certification_report_view
# (defined in addons/survey/report/survey_certification.xml)
ORIGINAL_REPORT_NAME = 'survey.certification_report'
SURVEY_CERT_XMLID    = 'survey.certification_report_view'


def uninstall_hook(env):
    """
    Restore survey.certification_report_view to Odoo's built-in template
    when this module is uninstalled, so the default certificate still works.
    """
    try:
        cert_report = env.ref(SURVEY_CERT_XMLID)
        cert_report.write({'report_name': ORIGINAL_REPORT_NAME})
        _logger.info(
            'shafa_elearning_certificate: Restored "%s" → "%s".',
            SURVEY_CERT_XMLID, ORIGINAL_REPORT_NAME,
        )
    except Exception as exc:
        _logger.error(
            'shafa_elearning_certificate: Could not restore certificate report: %s',
            exc,
        )

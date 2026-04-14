# -*- coding: utf-8 -*-
import logging

_logger = logging.getLogger(__name__)

# The exact XML ID of the survey certification report action
SURVEY_CERT_XMLID = 'survey.certification_report_view'

# Our replacement template
SHAFA_TEMPLATE    = 'shafa_elearning_certificate.report_slide_channel_certification'

# System parameters used to persist the original value for uninstall
PARAM_ORIG_NAME   = 'shafa_elearning_certificate.original_report_name'
PARAM_ORIG_ID     = 'shafa_elearning_certificate.original_report_id'


def post_init_hook(env):
    """
    After install: redirect survey.certification_report_view to use
    the Shafa custom QWeb template.

    We look up the report action via its known XML ID so we always
    hit the correct record, regardless of Odoo version or local
    module loading order.
    """
    try:
        cert_report = env.ref(SURVEY_CERT_XMLID)
    except ValueError:
        _logger.error(
            'shafa_elearning_certificate: Could not find report action "%s". '
            'Make sure the "survey" module is installed.',
            SURVEY_CERT_XMLID,
        )
        return

    # Persist original report_name so uninstall_hook can fully restore it
    env['ir.config_parameter'].sudo().set_param(PARAM_ORIG_NAME, cert_report.report_name)
    env['ir.config_parameter'].sudo().set_param(PARAM_ORIG_ID,   str(cert_report.id))

    cert_report.write({'report_name': SHAFA_TEMPLATE})

    _logger.info(
        'shafa_elearning_certificate: "%s" (id=%s) redirected '
        'from "%s" → "%s".',
        SURVEY_CERT_XMLID, cert_report.id,
        cert_report.report_name, SHAFA_TEMPLATE,
    )


def uninstall_hook(env):
    """
    On uninstall: restore survey.certification_report_view to its
    original report_name so Odoo's built-in certificate keeps working.
    """
    original_name   = env['ir.config_parameter'].sudo().get_param(PARAM_ORIG_NAME)
    original_id_str = env['ir.config_parameter'].sudo().get_param(PARAM_ORIG_ID)

    if not original_name or not original_id_str:
        _logger.warning(
            'shafa_elearning_certificate: Saved parameters not found — '
            'cannot restore original certificate report automatically.'
        )
        return

    try:
        report = env['ir.actions.report'].browse(int(original_id_str))
        if report.exists():
            report.write({'report_name': original_name})
            _logger.info(
                'shafa_elearning_certificate: Restored report_name → "%s".',
                original_name,
            )
    except Exception as exc:
        _logger.error(
            'shafa_elearning_certificate: Error restoring certificate report: %s',
            exc,
        )

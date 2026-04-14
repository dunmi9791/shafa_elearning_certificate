# -*- coding: utf-8 -*-
import logging

_logger = logging.getLogger(__name__)

SHAFA_TEMPLATE = 'shafa_elearning_certificate.report_slide_channel_certification'
PARAM_ORIG_NAME = 'shafa_elearning_certificate.original_report_name'
PARAM_ORIG_ID   = 'shafa_elearning_certificate.original_report_id'


def _find_cert_report(env):
    """
    Locate the eLearning channel certification report action.
    Searches slide.channel reports and picks the one whose
    report_name contains 'certif' (covers all known Odoo naming variants).
    """
    reports = env['ir.actions.report'].search([
        ('model', '=', 'slide.channel'),
        ('report_type', 'in', ['qweb-pdf', 'qweb-html']),
    ])
    cert = reports.filtered(
        lambda r: 'certif' in (r.report_name or '').lower()
    )
    return cert[:1]


def post_init_hook(env):
    """
    After install: redirect the existing certification report action
    to use the Shafa custom QWeb template.
    The original report_name is saved as a system parameter so
    uninstall_hook can fully restore it.
    """
    cert = _find_cert_report(env)
    if not cert:
        _logger.warning(
            'shafa_elearning_certificate: No certification report found for '
            'slide.channel — the Shafa template was NOT wired in automatically. '
            'Please set the report_name manually to: %s', SHAFA_TEMPLATE
        )
        return

    # Persist original values so uninstall can restore them
    env['ir.config_parameter'].sudo().set_param(PARAM_ORIG_NAME, cert.report_name)
    env['ir.config_parameter'].sudo().set_param(PARAM_ORIG_ID,   str(cert.id))

    cert.write({'report_name': SHAFA_TEMPLATE})
    _logger.info(
        'shafa_elearning_certificate: Certificate report (id=%s) redirected '
        'from "%s" → "%s"', cert.id, cert.report_name, SHAFA_TEMPLATE
    )


def uninstall_hook(env):
    """
    On uninstall: restore the certification report action to its
    original report_name so Odoo's built-in certificate still works.
    """
    original_name   = env['ir.config_parameter'].sudo().get_param(PARAM_ORIG_NAME)
    original_id_str = env['ir.config_parameter'].sudo().get_param(PARAM_ORIG_ID)

    if not original_name or not original_id_str:
        _logger.warning(
            'shafa_elearning_certificate: Could not restore original certificate '
            'report — saved parameters not found.'
        )
        return

    try:
        report = env['ir.actions.report'].browse(int(original_id_str))
        if report.exists():
            report.write({'report_name': original_name})
            _logger.info(
                'shafa_elearning_certificate: Certificate report restored to "%s".',
                original_name
            )
    except Exception as exc:
        _logger.error(
            'shafa_elearning_certificate: Error restoring certificate report: %s', exc
        )

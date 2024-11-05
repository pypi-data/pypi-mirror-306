from odoo import models, api


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    @api.model
    def default_get(self, fields):
        result = super(MailComposeMessage, self).default_get(fields)
        if result.get("composition_mode") and result["composition_mode"] == "comment":
            result["subject"] = self._context.get("default_subject", result["subject"])
        return result

    @api.multi
    @api.onchange("template_id")
    def onchange_template_id_wrapper(self):
        """
        Prevent onchange from messing with defaults when the template is set from
        the mass mailing wizard in the helpdesk ticket form view
        """
        if self._context and self._context.get("skip_onchange_template_id"):
            return
        super(MailComposeMessage, self).onchange_template_id_wrapper()

    @api.model
    def generate_email_for_composer(self, template_id, res_ids, fields=None):
        """
        Override (for helpdesk tickets only) to avoid the email composer to suggest
        addresses based on ticket partners, since it was causing duplicates for gmail
        accounts. (See also helpdesk_automatic_stage_changes/models/helpdesk_ticket.py)
        """
        template_values = super(MailComposeMessage, self).generate_email_for_composer(
            template_id, res_ids, fields
        )

        # Remove partner_ids from template_values for helpdesk tickets
        if self._context.get("active_model") == "helpdesk.ticket":
            [template_values[res_id].update({"partner_ids": []}) for res_id in res_ids]

        return template_values

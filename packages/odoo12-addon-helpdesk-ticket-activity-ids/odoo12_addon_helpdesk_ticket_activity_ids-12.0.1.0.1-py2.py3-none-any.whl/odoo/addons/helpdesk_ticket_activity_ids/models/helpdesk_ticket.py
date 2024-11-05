from odoo import models, fields


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    ticket_activity_ids = fields.One2many(related="activity_ids")

    def action_new_activity(self):
        self.ensure_one()
        context = self.env.context.copy()
        context.update(
            {
                "default_res_id": self.id,
                "default_res_model": self._name,
                "default_res_model_id": self.env.ref(
                    "helpdesk_mgmt.model_helpdesk_ticket"
                ).id,
            }
        )
        return {
            "type": "ir.actions.act_window",
            "name": "New Activity",
            "res_model": "mail.activity",
            "view_type": "form",
            "view_mode": "form",
            "view_id": self.env.ref("mail.mail_activity_view_form_popup").id,
            "target": "new",
            "context": context,
        }

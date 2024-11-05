# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    show_message_notes = fields.Boolean(default=True)
    show_emails_received = fields.Boolean(default=True)
    show_emails_sent = fields.Boolean(default=True)

    @api.one
    @api.depends(
        "message_ids", "show_message_notes", "show_emails_received", "show_emails_sent"
    )
    def _compute_emails(self):
        if not self.message_ids:
            return

        available_mail_messages_types = []

        if self.show_message_notes:
            available_mail_messages_types.append("note")
        if self.show_emails_received:
            available_mail_messages_types.append("email_received")
        if self.show_emails_sent:
            available_mail_messages_types.append("email_sent")

        self.message_emails_ids = self.message_ids.filtered(
            lambda msg: msg.message_type_mail in available_mail_messages_types
        )

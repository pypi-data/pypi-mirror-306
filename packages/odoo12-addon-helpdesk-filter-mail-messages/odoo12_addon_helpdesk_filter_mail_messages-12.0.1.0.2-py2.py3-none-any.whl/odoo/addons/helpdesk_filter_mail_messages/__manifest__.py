# Copyright 2023-SomItCoop SCCL(<https://gitlab.com/somitcoop>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "SomItCoop Odoo helpdesk filter mail messages",
    "version": "12.0.1.0.2",
    "depends": [
        "helpdesk_ticket_mail_message",
    ],
    "author": """
        Som It Cooperatiu SCCL,
        Som Connexió SCCL,
        Odoo Community Association (OCA)
    """,
    "category": "Helpdesk",
    "website": "https://gitlab.com/somitcoop/erp-research/odoo-helpdesk",
    "license": "AGPL-3",
    "summary": "Filter helpdesk ticket related messages by their type",
    "description": """
        Filter mail messages from helpdesk tickets view depending on their type:
        - notes
        - received emails
        - sent emails
    """,
    "data": [
        "views/helpdesk_ticket_view.xml",
    ],
    "application": False,
    "installable": True,
}

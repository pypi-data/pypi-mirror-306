# Copyright 2023 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Account Timesheet Time Type",
    "summary": "Time type in analytic account lines views",
    "version": "16.0.1.0.0",
    "category": "Analytic",
    "website": "https://github.com/sygel-technology/sy-account-analytic",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "analytic",
        "hr_timesheet_time_type",
    ],
    "data": ["views/analytic_account_view.xml"],
}

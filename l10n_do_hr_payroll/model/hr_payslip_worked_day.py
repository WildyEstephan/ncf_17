# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class HrPayslipWorkedDays(models.Model):
    _inherit = 'hr.payslip.worked_days'

    @api.depends('is_paid', 'number_of_hours', 'payslip_id', 'contract_id.wage', 'payslip_id.sum_worked_hours')
    def _compute_amount(self):
        super_self = self.env['hr.payslip.worked_days']
        for worked_day in self:
            if worked_day.payslip_id.state not in ['draft', 'verify'] \
                    or worked_day.payslip_id.edited \
                    or worked_day.payslip_id.contract_id.work_entry_source != "import_hours" \
                    or not worked_day.is_paid:
                super_self += worked_day
                continue
            elif worked_day.code == "WORK100":
                working_hours_import_ids = self.env['working.hours.import'].search([('employee_id', '=', worked_day.payslip_id.employee_id.id),
                                                                                ('date_from', '>=', worked_day.payslip_id.date_from),
                                                                                ('date_to', '<=', worked_day.payslip_id.date_to)])
                normal_hours = sum(working_hours_import_ids.mapped('hours_amount'))
                amount = 0.0
                if worked_day.payslip_id.contract_id.wage_type == 'hourly':
                    amount = worked_day.payslip_id.contract_id.hourly_wage
                else:
                    if worked_day.payslip_id.contract_id.wage > 0:
                        amount = worked_day.payslip_id.contract_id.wage / 23.83 / 8
                amount = amount * normal_hours
                worked_day.amount = amount
                worked_day.number_of_hours = normal_hours

        super(HrPayslipWorkedDays, super_self)._compute_amount()

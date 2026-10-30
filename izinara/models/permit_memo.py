from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class IzinaraMemo(models.Model):
    """Memo/permintaan antar bagian dengan tenggat jawab, supaya serah-terima tercatat dan waktu respons terukur."""

    _name = "izinara.memo"
    _description = "Memo antar bagian"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "state, date_deadline, id desc"

    name = fields.Char(string="Nomor", required=True, copy=False, readonly=True, default=lambda self: _("Baru"))
    subject = fields.Char(string="Perihal", required=True, tracking=True)
    kind = fields.Selection([("request", "Permintaan dokumen/data"), ("question", "Pertanyaan"),
                             ("info", "Informasi/serah-terima"), ("escalation", "Eskalasi")],
                            string="Jenis", default="request", required=True)
    priority = fields.Selection([("0", "Normal"), ("1", "Penting"), ("2", "Mendesak")], default="0")
    from_party_id = fields.Many2one("izinara.party", string="Dari bagian", required=True)
    to_party_id = fields.Many2one("izinara.party", string="Kepada bagian", required=True, tracking=True)
    user_id = fields.Many2one("res.users", string="Pengirim", default=lambda self: self.env.user, required=True)
    assignee_id = fields.Many2one("res.users", string="Penerima", tracking=True)
    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company)
    shipment_id = fields.Many2one("izinara.shipment", string="Pengapalan")
    application_id = fields.Many2one("izinara.application", string="Pengurusan")
    step_id = fields.Many2one("izinara.application.step", string="Aktivitas")
    body = fields.Html(string="Isi")
    answer = fields.Html(string="Jawaban")
    date_sent = fields.Datetime(string="Dikirim", readonly=True, copy=False)
    date_deadline = fields.Date(string="Tenggat jawab", tracking=True)
    date_answered = fields.Datetime(string="Dijawab", readonly=True, copy=False)
    response_hours = fields.Float(string="Waktu respons (jam)", readonly=True, copy=False, aggregator="avg")
    on_time = fields.Boolean(string="Tepat waktu", readonly=True, copy=False)
    state = fields.Selection([("draft", "Draf"), ("open", "Menunggu jawaban"), ("answered", "Dijawab"),
                              ("closed", "Selesai")], default="draft", tracking=True, copy=False)
    overdue = fields.Boolean(string="Lewat tenggat", compute="_compute_overdue", search="_search_overdue")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("Baru")) == _("Baru"):
                vals["name"] = self.env["ir.sequence"].next_by_code("izinara.memo") or _("Baru")
        return super().create(vals_list)

    @api.onchange("to_party_id")
    def _onchange_to_party(self):
        self.assignee_id = self.to_party_id._default_user()

    @api.onchange("step_id")
    def _onchange_step(self):
        if self.step_id:
            self.application_id = self.step_id.application_id
            self.shipment_id = self.step_id.shipment_id

    def _compute_overdue(self):
        today = fields.Date.context_today(self)
        for memo in self:
            memo.overdue = memo.state == "open" and bool(memo.date_deadline) and memo.date_deadline < today

    def _search_overdue(self, operator, value):
        today = fields.Date.context_today(self)
        if (operator == "=") == bool(value):
            return [("state", "=", "open"), ("date_deadline", "<", today)]
        return ["|", ("state", "!=", "open"), ("date_deadline", ">=", today)]

    def action_send(self):
        todo = self.env.ref("mail.mail_activity_data_todo", raise_if_not_found=False)
        for memo in self:
            if not memo.assignee_id:
                memo.assignee_id = memo.to_party_id._default_user()
            if not memo.date_deadline:
                days = {"2": 1, "1": 2}.get(memo.priority, 3)
                memo.date_deadline = fields.Date.context_today(memo) + timedelta(days=days)
            memo.write({"state": "open", "date_sent": fields.Datetime.now()})
            partners = (memo.to_party_id.user_ids | memo.assignee_id).partner_id
            memo.message_subscribe(partner_ids=(partners | memo.user_id.partner_id).ids)
            memo.message_post(body=memo.body or memo.subject, subject=memo.subject, partner_ids=partners.ids,
                              message_type="comment", subtype_xmlid="mail.mt_comment")
            if todo and memo.assignee_id:
                memo.activity_schedule(activity_type_id=todo.id, user_id=memo.assignee_id.id,
                                       date_deadline=memo.date_deadline,
                                       summary=_("Jawab memo %(no)s: %(s)s", no=memo.name, s=memo.subject)[:200])
            target = memo.step_id or memo.application_id or memo.shipment_id
            if target:
                target.message_post(body=_("Memo %(no)s ke %(party)s: %(s)s", no=memo.name,
                                           party=memo.to_party_id.name, s=memo.subject))
        return True

    def action_answer(self):
        for memo in self:
            if memo.state != "open":
                continue
            if not memo.answer or memo.answer in ("<p><br></p>", "<p></p>"):
                raise UserError(_("Tulis jawaban untuk memo %s.", memo.name))
            now = fields.Datetime.now()
            hours = (now - memo.date_sent).total_seconds() / 3600.0 if memo.date_sent else 0.0
            memo.write({"state": "answered", "date_answered": now, "response_hours": round(hours, 1),
                        "on_time": not memo.date_deadline or now.date() <= memo.date_deadline})
            memo.message_post(body=memo.answer, partner_ids=memo.user_id.partner_id.ids,
                              message_type="comment", subtype_xmlid="mail.mt_comment")
            memo.activity_ids.action_feedback(feedback=_("Dijawab"))
        return True

    def action_close(self):
        self.write({"state": "closed"})
        self.activity_ids.unlink()

    def action_reopen(self):
        self.write({"state": "open"})

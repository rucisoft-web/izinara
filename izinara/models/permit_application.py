from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError

STATES = [
    ("draft", "Draf"),
    ("progress", "Diproses"),
    ("submitted", "Diajukan ke instansi"),
    ("approved", "Terbit"),
    ("rejected", "Ditolak"),
    ("cancel", "Batal"),
]


class IzinaraApplication(models.Model):
    """Satu pengurusan izin: aktivitas dari template, dikerjakan per bagian, sampai izin terbit."""

    _name = "izinara.application"
    _description = "Pengurusan izin impor"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_deadline, id desc"

    name = fields.Char(string="Nomor", required=True, copy=False, readonly=True, default=lambda self: _("Baru"))
    type_id = fields.Many2one("izinara.type", string="Jenis izin", required=True, tracking=True)
    scope = fields.Selection(related="type_id.scope")
    authority = fields.Char(related="type_id.authority")
    party_id = fields.Many2one("izinara.party", string="Bagian penanggung jawab",
                               compute="_compute_party_id", store=True, readonly=False)
    template_id = fields.Many2one("izinara.template", string="Template pengurusan",
                                  help="Sumber aktivitas. Kosong = langkah standar jenis izin.")
    food_group = fields.Selection(related="template_id.food_group", store=True, string="Kelompok pengurusan")
    company_id = fields.Many2one("res.company", string="Perusahaan", required=True,
                                 default=lambda self: self.env.company)
    user_id = fields.Many2one("res.users", string="PIC", tracking=True, default=lambda self: self.env.user)
    shipment_id = fields.Many2one("izinara.shipment", string="Pengapalan", tracking=True)
    partner_id = fields.Many2one("res.partner", string="Pemasok/produsen")
    product_tmpl_ids = fields.Many2many("product.template", string="Item code")
    state = fields.Selection(STATES, string="Status", default="draft", required=True, tracking=True, copy=False)
    date_start = fields.Date(string="Mulai", copy=False)
    date_deadline = fields.Date(string="Target terbit", tracking=True,
                                help="Diisi otomatis dari ETA pengapalan dikurangi waktu clearance, bisa diubah.")
    date_submitted = fields.Date(string="Tanggal diajukan", copy=False)
    step_ids = fields.One2many("izinara.application.step", "application_id", string="Aktivitas", copy=False)
    progress = fields.Float(string="Progres (%)", compute="_compute_progress", store=True)
    overdue = fields.Boolean(string="Terlambat", compute="_compute_overdue", search="_search_overdue")
    license_id = fields.Many2one("izinara.license", string="Izin terbit", copy=False, readonly=True)
    permit_number = fields.Char(string="Nomor izin terbit", copy=False, tracking=True)
    date_issue = fields.Date(string="Tanggal terbit", copy=False)
    date_expiry = fields.Date(string="Berlaku sampai", copy=False)
    quota = fields.Float(string="Kuota/volume (kg)")
    reject_reason = fields.Text(string="Alasan penolakan", copy=False)
    note = fields.Text(string="Catatan")
    regulation_ids = fields.Many2many(related="type_id.regulation_ids", string="Referensi peraturan")
    legal_basis = fields.Text(related="type_id.legal_basis")
    document_ids = fields.One2many("izinara.document", "application_id", string="Dokumen")
    doc_review_count = fields.Integer(string="Dokumen menunggu verifikasi", compute="_compute_doc_counts")
    doc_missing_count = fields.Integer(string="Dokumen wajib belum lengkap", compute="_compute_doc_counts")
    memo_ids = fields.One2many("izinara.memo", "application_id", string="Memo")
    memo_open_count = fields.Integer(string="Memo terbuka", compute="_compute_doc_counts")

    @api.depends("document_ids.state", "memo_ids.state")
    def _compute_doc_counts(self):
        for app in self:
            docs = app.document_ids
            app.doc_review_count = len(docs.filtered(lambda d: d.state == "review"))
            app.doc_missing_count = len(docs.filtered(lambda d: d.required and d.state != "verified"))
            app.memo_open_count = len(app.memo_ids.filtered(lambda m: m.state == "open"))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("Baru")) == _("Baru"):
                vals["name"] = self.env["ir.sequence"].next_by_code("izinara.application") or _("Baru")
        return super().create(vals_list)

    @api.depends("type_id")
    def _compute_party_id(self):
        for app in self:
            app.party_id = app.type_id.party_id

    @api.depends("step_ids.done", "state")
    def _compute_progress(self):
        for app in self:
            if app.state == "approved":
                app.progress = 100.0
            elif app.step_ids:
                app.progress = 100.0 * len(app.step_ids.filtered("done")) / len(app.step_ids)
            else:
                app.progress = 0.0

    def _compute_overdue(self):
        today = fields.Date.context_today(self)
        for app in self:
            app.overdue = bool(app.state in ("draft", "progress", "submitted") and app.date_deadline
                               and app.date_deadline < today)

    def _search_overdue(self, operator, value):
        today = fields.Date.context_today(self)
        if (operator == "=") == bool(value):
            return [("state", "in", ("draft", "progress", "submitted")), ("date_deadline", "<", today)]
        return ["|", "|", ("state", "not in", ("draft", "progress", "submitted")),
                ("date_deadline", "=", False), ("date_deadline", ">=", today)]

    def _activity_source(self):
        self.ensure_one()
        if self.template_id:
            acts = self.template_id._activities_for(self.type_id)
            if acts:
                return [{"sequence": a.sequence, "name": a.name, "party_id": a.party_id.id,
                         "duration_days": a.duration_days, "instructions": a.instructions,
                         "deliverable": a.deliverable,
                         "regulation_ids": [(6, 0, (a.regulation_ids or self.type_id.regulation_ids).ids)],
                         "document_ids": [(0, 0, v) for v in a.doc_spec_ids._copy_vals()]} for a in acts]
        return [{"sequence": s.sequence, "name": s.name, "party_id": s.party_id.id,
                 "duration_days": s.duration_days, "instructions": s.instructions,
                 "deliverable": s.deliverable,
                 "regulation_ids": [(6, 0, (s.regulation_ids or self.type_id.regulation_ids).ids)],
                 "document_ids": [(0, 0, v) for v in s.doc_spec_ids._copy_vals()]} for s in self.type_id.step_ids]

    def action_start(self):
        Party = self.env["izinara.party"]
        for app in self:
            if app.state != "draft":
                continue
            start = fields.Date.context_today(app)
            if not app.step_ids:
                planned = start
                steps = []
                for src in app._activity_source():
                    planned = planned + timedelta(days=src["duration_days"] or 0)
                    user = Party.browse(src["party_id"])._default_user()
                    steps.append(dict(src, application_id=app.id, date_planned=planned, user_id=user.id))
                self.env["izinara.application.step"].create(steps)
            app.write({"state": "progress", "date_start": start})
            if not app.date_deadline:
                app.date_deadline = max(app.step_ids.mapped("date_planned") or [start])
            app._schedule_next_step()
        return True

    def _schedule_next_step(self):
        todo = self.env.ref("mail.mail_activity_data_todo", raise_if_not_found=False)
        for app in self:
            step = app.step_ids.filtered(lambda s: not s.done)[:1]
            if not step or not todo:
                continue
            user = step.user_id or app.user_id
            if user:
                app.activity_schedule(
                    activity_type_id=todo.id, user_id=user.id, date_deadline=step.date_planned,
                    summary=step.name[:200],
                    note=_("Bagian: %(party)s", party=step.party_id.name))

    def action_submit(self):
        self.write({"state": "submitted", "date_submitted": fields.Date.context_today(self)})

    def action_approve(self):
        License = self.env["izinara.license"]
        for app in self:
            if not app.permit_number:
                raise UserError(_("Isi nomor izin terbit sebelum menandai %s terbit.", app.name))
            open_steps = app.step_ids.filtered(lambda s: not s.done)
            open_steps.write({"done": True, "done_date": fields.Date.context_today(app), "done_by_id": self.env.uid})
            if open_steps:
                app.message_post(body=_("Izin terbit; %s aktivitas yang belum ditandai ikut ditutup.", len(open_steps)))
            expiry = app.date_expiry
            if not expiry and app.type_id.validity_months:
                expiry = (app.date_issue or fields.Date.context_today(app)) + timedelta(
                    days=round(app.type_id.validity_months * 30.4))
            lic = License.create({
                "name": app.permit_number,
                "type_id": app.type_id.id,
                "company_id": app.company_id.id,
                "partner_id": app.partner_id.id,
                "product_tmpl_ids": [(6, 0, app.product_tmpl_ids.ids)],
                "shipment_id": app.shipment_id.id if app.type_id.scope == "shipment" else False,
                "application_id": app.id,
                "date_issue": app.date_issue or fields.Date.context_today(app),
                "date_expiry": expiry,
                "quota": app.quota,
            })
            app.write({"state": "approved", "license_id": lic.id, "date_expiry": expiry})
            app.activity_ids.action_feedback(feedback=_("Izin terbit: %s", app.permit_number))
        return True

    def action_reject(self):
        for app in self:
            if not app.reject_reason:
                raise UserError(_("Isi alasan penolakan untuk %s.", app.name))
        self.write({"state": "rejected"})
        self.activity_ids.unlink()

    def action_restart(self):
        """Ajukan ulang setelah ditolak: aktivitas yang belum selesai dijadwalkan lagi."""
        self.write({"state": "progress"})
        self._schedule_next_step()

    def action_cancel(self):
        self.write({"state": "cancel"})
        self.activity_ids.unlink()


class IzinaraApplicationStep(models.Model):
    _name = "izinara.application.step"
    _description = "Aktivitas pengurusan izin"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "application_id, sequence, id"

    application_id = fields.Many2one("izinara.application", required=True, ondelete="cascade", index=True)
    type_id = fields.Many2one(related="application_id.type_id", store=True, string="Jenis izin")
    shipment_id = fields.Many2one(related="application_id.shipment_id", store=True, string="Pengapalan")
    company_id = fields.Many2one(related="application_id.company_id", store=True)
    app_state = fields.Selection(related="application_id.state", string="Status pengurusan")
    sequence = fields.Integer(default=10)
    name = fields.Char(string="Aktivitas", required=True)
    party_id = fields.Many2one("izinara.party", string="Bagian", required=True)
    user_id = fields.Many2one("res.users", string="Petugas")
    duration_days = fields.Integer(string="Durasi (hari)")
    date_planned = fields.Date(string="Target")
    instructions = fields.Text(string="Petunjuk")
    deliverable = fields.Char(string="Dokumen hasil")
    done = fields.Boolean(string="Selesai", readonly=True)
    done_date = fields.Date(string="Tanggal selesai", readonly=True)
    done_by_id = fields.Many2one("res.users", string="Diselesaikan oleh", readonly=True)
    overdue = fields.Boolean(string="Terlambat", compute="_compute_overdue")
    note = fields.Text(string="Catatan")
    regulation_ids = fields.Many2many("izinara.regulation", "izinara_app_step_regulation_rel",
                                      string="Referensi peraturan")
    document_ids = fields.One2many("izinara.document", "step_id", string="Dokumen")
    doc_status = fields.Char(string="Dokumen terverifikasi", compute="_compute_doc_status")
    docs_ready = fields.Boolean(string="Dokumen lengkap", compute="_compute_doc_status")

    @api.depends("document_ids.state", "document_ids.required")
    def _compute_doc_status(self):
        for step in self:
            docs = step.document_ids
            verified = docs.filtered(lambda d: d.state == "verified")
            step.doc_status = f"{len(verified)}/{len(docs)}" if docs else ""
            step.docs_ready = all(d.state == "verified" for d in docs if d.required)

    def _compute_display_name(self):
        for step in self:
            step.display_name = f"{step.application_id.name} – {step.name}" if step.application_id else step.name

    def _compute_overdue(self):
        today = fields.Date.context_today(self)
        for step in self:
            step.overdue = bool(not step.done and step.date_planned and step.date_planned < today
                                and step.app_state in ("progress", "submitted"))

    def action_done(self):
        apps = self.env["izinara.application"]
        for step in self.filtered(lambda s: not s.done):
            if step.application_id.state not in ("progress", "submitted"):
                raise UserError(_("Mulai pengurusan %s dulu.", step.application_id.name))
            if not step.docs_ready and not self.env.context.get("permit_skip_doc_check"):
                pending = step.document_ids.filtered(lambda d: d.required and d.state != "verified")
                raise UserError(_("Aktivitas \"%(step)s\" belum bisa selesai. Dokumen wajib belum terverifikasi:\n%(d)s",
                                  step=step.name, d="\n".join(
                                      "- %s (%s)" % (d.name, dict(d._fields["state"].selection)[d.state])
                                      for d in pending)))
            step.write({"done": True, "done_date": fields.Date.context_today(step), "done_by_id": self.env.uid})
            apps |= step.application_id
        for app in apps:
            app.activity_ids.action_feedback(
                feedback=_("Selesai: %s", ", ".join(self.filtered(lambda s: s.application_id == app).mapped("name"))))
            if all(app.step_ids.mapped("done")) and app.state == "progress":
                app.action_submit()
            else:
                app._schedule_next_step()
        return True

    def action_undo(self):
        self.write({"done": False, "done_date": False, "done_by_id": False})

    def action_open(self):
        self.ensure_one()
        return {"type": "ir.actions.act_window", "res_model": self._name, "res_id": self.id, "view_mode": "form"}

    def action_new_memo(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window", "res_model": "izinara.memo", "view_mode": "form",
            "target": "new",
            "context": {"default_step_id": self.id, "default_application_id": self.application_id.id,
                        "default_shipment_id": self.shipment_id.id, "default_from_party_id": self.party_id.id,
                        "default_subject": self.name},
        }

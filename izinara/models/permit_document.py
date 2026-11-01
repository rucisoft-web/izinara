import os

from odoo import _, api, fields, models
from odoo.exceptions import UserError

DEFAULT_EXTENSIONS = "pdf,jpg,jpeg,png,doc,docx,xls,xlsx,csv,zip"
DOC_STATES = [
    ("missing", "Belum diunggah"),
    ("review", "Menunggu verifikasi"),
    ("verified", "Terverifikasi"),
    ("rejected", "Ditolak, perlu perbaikan"),
]


class IzinaraDocSpec(models.Model):
    """Spesifikasi dokumen yang wajib diunggah pada satu aktivitas, beserta kriteria verifikasinya."""

    _name = "izinara.doc.spec"
    _description = "Spesifikasi dokumen aktivitas"
    _order = "sequence, id"

    type_step_id = fields.Many2one("izinara.type.step", ondelete="cascade", index=True)
    activity_id = fields.Many2one("izinara.template.activity", ondelete="cascade", index=True)
    sequence = fields.Integer(default=10)
    name = fields.Char(string="Dokumen", required=True)
    required = fields.Boolean(string="Wajib", default=True)
    extensions = fields.Char(string="Jenis file diizinkan", default=DEFAULT_EXTENSIONS,
                             help="Ekstensi dipisah koma. Kosong = semua jenis file.")
    check_expiry = fields.Boolean(string="Cek masa berlaku",
                                  help="Pengunggah wajib mengisi tanggal berlaku dokumen; harus masih berlaku saat ETA.")
    criteria = fields.Text(string="Kriteria verifikasi", help="Satu kriteria per baris.")
    verifier_party_id = fields.Many2one("izinara.party", string="Bagian verifikator")

    def _copy_vals(self):
        return [{"sequence": s.sequence, "name": s.name, "required": s.required, "extensions": s.extensions,
                 "check_expiry": s.check_expiry, "criteria": s.criteria,
                 "verifier_party_id": s.verifier_party_id.id} for s in self]


class IzinaraDocument(models.Model):
    """Dokumen pada aktivitas pengurusan: bisa berisi banyak file, diperiksa otomatis lalu diverifikasi manual."""

    _name = "izinara.document"
    _description = "Dokumen aktivitas pengurusan izin"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "step_id, sequence, id"

    step_id = fields.Many2one("izinara.application.step", string="Aktivitas", required=True,
                              ondelete="cascade", index=True)
    application_id = fields.Many2one(related="step_id.application_id", store=True, string="Pengurusan")
    shipment_id = fields.Many2one(related="step_id.shipment_id", store=True, string="Pengapalan")
    company_id = fields.Many2one(related="step_id.company_id", store=True)
    uploader_party_id = fields.Many2one(related="step_id.party_id", store=True, string="Bagian pengunggah")
    sequence = fields.Integer(default=10)
    name = fields.Char(string="Dokumen", required=True)
    required = fields.Boolean(string="Wajib", default=True)
    extensions = fields.Char(string="Jenis file diizinkan", default=DEFAULT_EXTENSIONS)
    check_expiry = fields.Boolean(string="Cek masa berlaku")
    criteria = fields.Text(string="Kriteria verifikasi")
    verifier_party_id = fields.Many2one("izinara.party", string="Bagian verifikator")
    attachment_ids = fields.Many2many("ir.attachment", "izinara_document_attachment_rel", "document_id",
                                      "attachment_id", string="File")
    file_count = fields.Integer(string="Jumlah file", compute="_compute_file_count")
    doc_number = fields.Char(string="Nomor dokumen")
    date_expiry = fields.Date(string="Berlaku sampai")
    state = fields.Selection(DOC_STATES, string="Status", default="missing", required=True, tracking=True)
    auto_check = fields.Text(string="Hasil cek otomatis", readonly=True)
    check_ids = fields.One2many("izinara.document.check", "document_id", string="Checklist verifikasi")
    uploaded_by_id = fields.Many2one("res.users", string="Diunggah oleh", readonly=True)
    uploaded_date = fields.Datetime(string="Diajukan", readonly=True)
    verified_by_id = fields.Many2one("res.users", string="Diverifikasi oleh", readonly=True)
    verified_date = fields.Datetime(string="Tanggal verifikasi", readonly=True)
    reject_reason = fields.Text(string="Catatan perbaikan")
    revision = fields.Integer(string="Revisi ke", readonly=True)

    @api.depends("attachment_ids")
    def _compute_file_count(self):
        for doc in self:
            doc.file_count = len(doc.attachment_ids)

    @api.model_create_multi
    def create(self, vals_list):
        docs = super().create(vals_list)
        for doc in docs:
            doc._sync_checks()
        return docs

    def write(self, vals):
        res = super().write(vals)
        if "criteria" in vals:
            for doc in self:
                doc._sync_checks()
        if "attachment_ids" in vals:
            # File baru di dokumen yang sudah diverifikasi/ditolak harus diperiksa ulang.
            self.filtered(lambda d: d.state in ("verified", "rejected") and d.attachment_ids).write(
                {"state": "missing"})
            self.attachment_ids.filtered(lambda a: not a.res_id).write({"res_model": self._name, "res_id": self[:1].id})
        return res

    def _sync_checks(self):
        self.ensure_one()
        lines = [l.strip(" -•\t") for l in (self.criteria or "").splitlines() if l.strip(" -•\t")]
        self.check_ids.unlink()
        self.env["izinara.document.check"].create(
            [{"document_id": self.id, "sequence": i, "name": line} for i, line in enumerate(lines, 1)])

    def _automatic_check(self):
        """Pemeriksaan yang bisa dilakukan mesin. Mengembalikan daftar masalah (kosong = lolos)."""
        self.ensure_one()
        problems = []
        if not self.attachment_ids:
            problems.append(_("Belum ada file."))
        allowed = {e.strip().lower().lstrip(".") for e in (self.extensions or "").split(",") if e.strip()}
        for att in self.attachment_ids:
            ext = os.path.splitext(att.name or "")[1].lower().lstrip(".")
            if allowed and ext not in allowed:
                problems.append(_("%(file)s: jenis file .%(ext)s tidak diizinkan (boleh: %(allowed)s).",
                                  file=att.name, ext=ext or "?", allowed=", ".join(sorted(allowed))))
            if not att.file_size:
                problems.append(_("%s: file kosong.", att.name))
        if self.check_expiry:
            eta = self.shipment_id.eta or fields.Date.context_today(self)
            if not self.date_expiry:
                problems.append(_("Isi tanggal berlaku dokumen."))
            elif self.date_expiry < eta:
                problems.append(_("Dokumen habis berlaku %(exp)s, sebelum ETA/tanggal pakai %(eta)s.",
                                  exp=self.date_expiry, eta=eta))
        return problems

    def action_submit_review(self):
        todo = self.env.ref("mail.mail_activity_data_todo", raise_if_not_found=False)
        for doc in self:
            problems = doc._automatic_check()
            doc.auto_check = "\n".join(problems) if problems else _("Lolos: %s file, jenis file sesuai.", doc.file_count)
            if problems:
                raise UserError(_("Dokumen %(doc)s belum memenuhi syarat:\n%(p)s", doc=doc.name, p="\n".join(problems)))
            doc.check_ids.write({"ok": False})
            doc.write({"state": "review", "uploaded_by_id": self.env.uid, "uploaded_date": fields.Datetime.now(),
                       "revision": doc.revision + 1})
            verifier = doc.verifier_party_id._default_user() if doc.verifier_party_id else doc.step_id.user_id
            if todo and verifier:
                doc.activity_schedule(activity_type_id=todo.id, user_id=verifier.id,
                                      summary=_("Verifikasi dokumen: %s", doc.name)[:200])
        return True

    def action_verify(self):
        for doc in self:
            if doc.state != "review":
                raise UserError(_("Dokumen %s belum diajukan untuk verifikasi.", doc.name))
            open_checks = doc.check_ids.filtered(lambda c: not c.ok)
            if open_checks:
                raise UserError(_("Checklist belum lengkap untuk %(doc)s:\n%(c)s", doc=doc.name,
                                  c="\n".join("- " + c.name for c in open_checks)))
            doc.write({"state": "verified", "verified_by_id": self.env.uid, "verified_date": fields.Datetime.now(),
                       "reject_reason": False})
            doc.activity_ids.action_feedback(feedback=_("Terverifikasi"))
            doc.step_id.message_post(body=_("Dokumen %(doc)s terverifikasi oleh %(user)s.",
                                            doc=doc.name, user=self.env.user.name))
        return True

    def action_reject(self):
        todo = self.env.ref("mail.mail_activity_data_todo", raise_if_not_found=False)
        for doc in self:
            if not doc.reject_reason:
                raise UserError(_("Tulis catatan perbaikan untuk %s.", doc.name))
            doc.write({"state": "rejected", "verified_by_id": self.env.uid, "verified_date": fields.Datetime.now()})
            doc.activity_ids.action_feedback(feedback=_("Ditolak: %s", doc.reject_reason))
            owner = doc.uploaded_by_id or doc.step_id.user_id
            if todo and owner:
                doc.activity_schedule(activity_type_id=todo.id, user_id=owner.id,
                                      summary=_("Perbaiki dokumen: %s", doc.name)[:200], note=doc.reject_reason)
            doc.step_id.message_post(body=_("Dokumen %(doc)s ditolak: %(r)s", doc=doc.name, r=doc.reject_reason))
        return True

    def action_open(self):
        self.ensure_one()
        return {"type": "ir.actions.act_window", "res_model": self._name, "res_id": self.id, "view_mode": "form",
                "target": "new"}


class IzinaraDocumentCheck(models.Model):
    _name = "izinara.document.check"
    _description = "Checklist verifikasi dokumen"
    _order = "document_id, sequence, id"

    document_id = fields.Many2one("izinara.document", required=True, ondelete="cascade")
    sequence = fields.Integer(default=10)
    name = fields.Char(string="Kriteria", required=True)
    ok = fields.Boolean(string="Sesuai")
    note = fields.Char(string="Catatan")

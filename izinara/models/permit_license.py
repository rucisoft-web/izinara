from datetime import timedelta

from odoo import _, api, fields, models


class IzinaraLicense(models.Model):
    """Register izin/sertifikat yang sudah terbit, dipakai untuk memeriksa kelengkapan tiap pengapalan."""

    _name = "izinara.license"
    _description = "Register izin dan sertifikat impor"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_expiry, id desc"

    name = fields.Char(string="Nomor izin/sertifikat", required=True, tracking=True)
    type_id = fields.Many2one("izinara.type", string="Jenis izin", required=True, tracking=True)
    scope = fields.Selection(related="type_id.scope")
    party_id = fields.Many2one(related="type_id.party_id", store=True, string="Bagian")
    company_id = fields.Many2one("res.company", string="Perusahaan", required=True,
                                 default=lambda self: self.env.company)
    partner_id = fields.Many2one("res.partner", string="Pemasok/produsen",
                                 help="Untuk izin per pemasok (mis. persetujuan unit usaha asal, sertifikat halal produsen).")
    product_tmpl_ids = fields.Many2many("product.template", string="Item code")
    shipment_id = fields.Many2one("izinara.shipment", string="Pengapalan")
    application_id = fields.Many2one("izinara.application", string="Pengurusan")
    date_issue = fields.Date(string="Tanggal terbit", tracking=True)
    date_expiry = fields.Date(string="Berlaku sampai", tracking=True)
    quota = fields.Float(string="Kuota/volume (kg)", help="Untuk PI/rekomendasi berkuota.")
    state = fields.Selection([("valid", "Berlaku"), ("expiring", "Segera habis"), ("expired", "Kedaluwarsa"),
                              ("revoked", "Dicabut")], string="Status", default="valid", tracking=True)
    days_to_expiry = fields.Integer(string="Sisa hari", compute="_compute_days_to_expiry")
    note = fields.Text(string="Catatan")

    @api.depends("date_expiry")
    def _compute_days_to_expiry(self):
        today = fields.Date.context_today(self)
        for lic in self:
            lic.days_to_expiry = (lic.date_expiry - today).days if lic.date_expiry else 0

    def _is_valid_on(self, day):
        self.ensure_one()
        return self.state in ("valid", "expiring") and (not self.date_expiry or self.date_expiry >= day)

    def action_revoke(self):
        self.state = "revoked"

    @api.model
    def _cron_check_expiry(self):
        """Tandai izin kedaluwarsa/segera habis dan buat aktivitas perpanjangan untuk bagian penanggung jawab."""
        today = fields.Date.context_today(self)
        self.search([("state", "in", ("valid", "expiring")), ("date_expiry", "<", today)]).write({"state": "expired"})
        todo = self.env.ref("mail.mail_activity_data_todo", raise_if_not_found=False)
        for lic in self.search([("state", "=", "valid"), ("date_expiry", "!=", False)]):
            if lic.date_expiry - timedelta(days=lic.type_id.renew_days or 0) > today:
                continue
            lic.state = "expiring"
            user = lic.type_id.party_id._default_user() or lic.create_uid
            if todo and user:
                lic.activity_schedule(
                    activity_type_id=todo.id, user_id=user.id, date_deadline=lic.date_expiry,
                    summary=_("Perpanjang %(type)s %(no)s", type=lic.type_id.name, no=lic.name))

from odoo import fields, models

SCOPES = [
    ("company", "Per perusahaan"),
    ("supplier", "Per pemasok/unit usaha asal"),
    ("product", "Per barang (item code)"),
    ("shipment", "Per pengapalan"),
]


class IzinaraType(models.Model):
    """Jenis izin, rekomendasi, sertifikat atau dokumen yang harus dipenuhi sebelum barang impor beredar."""

    _name = "izinara.type"
    _description = "Jenis izin impor"
    _order = "sequence, id"

    name = fields.Char(string="Nama izin", required=True, translate=True)
    code = fields.Char(string="Kode", required=True)
    sequence = fields.Integer(string="Urutan", default=10,
                              help="Urutan pengurusan; izin dengan urutan lebih kecil biasanya menjadi syarat izin berikutnya.")
    authority = fields.Char(string="Instansi penerbit")
    system = fields.Char(string="Sistem/portal")
    party_id = fields.Many2one("izinara.party", string="Bagian penanggung jawab", required=True)
    scope = fields.Selection(SCOPES, string="Cakupan", required=True, default="product")
    legal_basis = fields.Text(string="Dasar hukum (ringkas)")
    regulation_ids = fields.Many2many("izinara.regulation", "izinara_type_regulation_rel",
                                      string="Referensi peraturan")
    description = fields.Text(string="Keterangan", translate=True)
    lead_days = fields.Integer(string="Waktu proses (hari)", help="Perkiraan hari kalender dari mulai sampai terbit.")
    validity_months = fields.Integer(string="Masa berlaku (bulan)", help="0 = tidak kedaluwarsa atau mengikuti dokumen.")
    renew_days = fields.Integer(string="Ingatkan perpanjangan (hari)", default=90)
    step_ids = fields.One2many("izinara.type.step", "type_id", string="Langkah standar", copy=True)
    active = fields.Boolean(default=True)

    _sql_constraints = [("code_uniq", "unique(code)", "Kode jenis izin harus unik.")]


class IzinaraTypeStep(models.Model):
    _name = "izinara.type.step"
    _description = "Langkah standar pengurusan izin"
    _order = "type_id, sequence, id"

    type_id = fields.Many2one("izinara.type", required=True, ondelete="cascade")
    sequence = fields.Integer(default=10)
    name = fields.Char(string="Aktivitas", required=True, translate=True)
    party_id = fields.Many2one("izinara.party", string="Bagian", required=True)
    duration_days = fields.Integer(string="Durasi (hari)", default=1)
    instructions = fields.Text(string="Petunjuk", translate=True)
    deliverable = fields.Char(string="Dokumen hasil")
    regulation_ids = fields.Many2many("izinara.regulation", "izinara_type_step_regulation_rel",
                                      string="Referensi peraturan")
    doc_spec_ids = fields.One2many("izinara.doc.spec", "type_step_id", string="Dokumen wajib", copy=True)

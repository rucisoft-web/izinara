from odoo import fields, models


class IzinaraRegulation(models.Model):
    """Referensi peraturan perundang-undangan yang menjadi dasar aktivitas pengurusan."""

    _name = "izinara.regulation"
    _description = "Referensi peraturan"
    _order = "year desc, name"

    code = fields.Char(string="Kode", required=True)
    name = fields.Char(string="Peraturan", required=True, help="Nama singkat, mis. Permendag 16/2025")
    title = fields.Char(string="Tentang")
    issuer = fields.Char(string="Penerbit")
    year = fields.Integer(string="Tahun")
    url = fields.Char(string="Tautan")
    note = fields.Char(string="Catatan", help="Mis. sudah diubah, cek versi terbaru.")
    active = fields.Boolean(default=True)

    _sql_constraints = [("code_uniq", "unique(code)", "Kode peraturan harus unik.")]

    def _compute_display_name(self):
        for reg in self:
            reg.display_name = f"{reg.name} – {reg.title}" if reg.title else reg.name

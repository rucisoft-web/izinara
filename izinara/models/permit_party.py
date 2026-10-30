from odoo import fields, models


class IzinaraParty(models.Model):
    """Pihak (bagian) yang mengerjakan langkah pengurusan izin."""

    _name = "izinara.party"
    _description = "Pihak pengurusan izin impor"
    _order = "sequence, id"

    name = fields.Char(string="Nama bagian", required=True, translate=True)
    code = fields.Char(string="Kode", required=True)
    sequence = fields.Integer(default=10)
    user_ids = fields.Many2many("res.users", string="Petugas",
                                help="Petugas bagian ini. Petugas pertama menjadi penanggung jawab default langkah.")
    responsibility = fields.Text(string="Tanggung jawab", translate=True)
    color = fields.Integer(string="Warna")
    active = fields.Boolean(default=True)

    _sql_constraints = [("code_uniq", "unique(code)", "Kode bagian harus unik.")]

    def _default_user(self):
        self.ensure_one()
        return self.user_ids[:1]

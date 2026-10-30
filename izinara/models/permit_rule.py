import re

from odoo import fields, models

ORIGINS = [("any", "Semua"), ("import", "Impor"), ("domestic", "Lokal (Indonesia)")]
HALAL = [("any", "Semua"), ("halal", "Halal"), ("non_halal", "Non-halal")]


def _tokens(text):
    return [t.strip().upper() for t in (text or "").split(",") if t.strip()]


def _norm(text):
    return re.sub(r"\s+", " ", (text or "").strip().upper())


class IzinaraRule(models.Model):
    """Aturan pemetaan item master ke template pengurusan. Aturan pertama (urutan terkecil) yang cocok dipakai.

    Semua kondisi yang diisi harus cocok; kondisi kosong berarti bebas."""

    _name = "izinara.rule"
    _description = "Aturan pemetaan item ke template izin"
    _order = "sequence, id"

    sequence = fields.Integer(string="Urutan", default=10)
    name = fields.Char(string="Nama aturan", required=True)
    template_id = fields.Many2one("izinara.template", string="Template", required=True, ondelete="cascade")
    origin = fields.Selection(ORIGINS, string="Asal barang", default="any", required=True)
    group_codes = fields.Char(string="Kode grup", help="Huruf depan kolom 03.Group, pisahkan dengan koma. Mis. A,D")
    subgroups = fields.Char(string="Subgrup", help="Nilai kolom 04.SubGroup, pisahkan dengan koma. Mis. PORK,BEEF")
    hs_prefixes = fields.Char(string="Awalan HS", help="Awalan kode HS, pisahkan dengan koma. Mis. 0201,0202")
    keywords = fields.Char(string="Kata di nama barang", help="Salah satu kata harus ada di nama barang. Mis. PORK,BACON")
    halal = fields.Selection(HALAL, string="Status halal", default="any", required=True)
    active = fields.Boolean(default=True)

    def _matches(self, item):
        """`item` adalah dict: group_code, subgroup, hs_code, name, is_import, non_halal."""
        self.ensure_one()
        if self.origin == "import" and not item["is_import"]:
            return False
        if self.origin == "domestic" and item["is_import"]:
            return False
        if self.halal == "halal" and item["non_halal"]:
            return False
        if self.halal == "non_halal" and not item["non_halal"]:
            return False
        groups = _tokens(self.group_codes)
        if groups and (item["group_code"] or "").upper() not in groups:
            return False
        subgroups = [_norm(s) for s in _tokens(self.subgroups)]
        if subgroups and _norm(item["subgroup"]) not in subgroups:
            return False
        prefixes = _tokens(self.hs_prefixes)
        hs = re.sub(r"\D", "", item["hs_code"] or "")
        if prefixes and not any(hs.startswith(p) for p in prefixes):
            return False
        keywords = _tokens(self.keywords)
        name = (item["name"] or "").upper()
        if keywords and not any(re.search(r"\b%s\b" % re.escape(k), name) for k in keywords):
            return False
        return True

    def _find_template(self, item):
        for rule in self.search([]):
            if rule._matches(item):
                return rule.template_id
        return self.env["izinara.template"]

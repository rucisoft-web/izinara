import re

from odoo import _, api, fields, models


# Kata di nama barang yang menandakan produk babi/non-halal walau kolom U_Non_Halal kosong.
NON_HALAL_WORDS = re.compile(r"\b(PORK|BABI|LARD|KUROBUTA|IBERICO|PROSCIUTTO|PANCETTA|CHORIZO)\b")
OFFAL_WORDS = re.compile(r"\b(LIVER|TONGUE|TRIPE|HEART|KIDNEY|OFFAL|INTESTINE|BRAIN|LIDAH|HATI|BABAT|JEROAN|"
                         r"OMASUM|HONEYCOMB|TENDON|SKIRT ?FAT)\b")
CARCASS_WORDS = re.compile(r"\b(CARCASS|CARCASE|KARKAS|WHOLE BIRD)\b")
CRUSTACEAN_WORDS = re.compile(r"\b(SHRIMP|PRAWN|LOBSTER|CRAB|UDANG|KEPITING|RAJUNGAN|LANGOUSTINE)\b")
MOLLUSC_WORDS = re.compile(r"\b(SQUID|OCTOPUS|CUTTLE ?FISH|SCALLOPS?|MUSSELS?|CLAMS?|OYSTERS?|CUMI|SOTONG|GURITA|"
                           r"KERANG|ABALONE)\b")
# HS karkas (utuh/setengah) daging sapi, babi, domba/kambing.
CARCASS_HS = ("020110", "020210", "020311", "020321", "020410", "020421", "020430", "020441", "020450")
PRODUCT_KINDS = [
    ("karkas", "Karkas"),
    ("daging", "Daging"),
    ("jeroan", "Jeroan (edible offal)"),
    ("unggas", "Daging unggas"),
    ("daging_olahan", "Daging olahan"),
    ("ikan", "Ikan (bersirip)"),
    ("krustasea", "Krustasea (udang, kepiting, lobster)"),
    ("moluska", "Moluska (cumi, gurita, kerang)"),
    ("olahan_ikan", "Olahan ikan/seafood"),
    ("sayur", "Sayuran"),
    ("buah", "Buah"),
    ("susu", "Susu & olahan susu"),
    ("pangan_olahan", "Pangan olahan lain"),
    ("non_pangan", "Non-pangan"),
]


def product_kind(group_code, subgroup, hs_code, name):
    """Jenis produk menurut istilah peraturan (Permentan 42/2019 untuk produk hewan, kategori PSAI/PSAT)."""
    g = (group_code or "").upper()
    hs = re.sub(r"\D", "", hs_code or "")
    name = (name or "").upper()
    sub = re.sub(r"\s+", " ", (subgroup or "").upper().strip())
    if g in ("L", "O"):
        return "non_pangan"
    if hs.startswith(("1604", "1605")) or sub in ("PROCESSED SEAFOOD", "CAVIAR"):
        return "olahan_ikan"
    if hs.startswith(("1601", "1602")) or g == "D":
        return "daging_olahan"
    if g in ("A", "C"):
        if hs.startswith("0206") or OFFAL_WORDS.search(name):
            return "jeroan"
        if hs.startswith(CARCASS_HS) or CARCASS_WORDS.search(name):
            return "karkas"
        if g == "C" or hs.startswith("0207"):
            return "unggas"
        return "daging"
    if g == "B":
        if hs.startswith("0306") or CRUSTACEAN_WORDS.search(name):
            return "krustasea"
        if hs.startswith("0307") or MOLLUSC_WORDS.search(name):
            return "moluska"
        return "ikan"
    if g == "E":
        if hs.startswith("08"):
            return "buah"
        if hs.startswith("07"):
            return "sayur"
        return "pangan_olahan"
    if g == "F":
        return "susu"
    return "pangan_olahan"


class ProductTemplate(models.Model):
    _inherit = "product.template"

    permit_template_id = fields.Many2one("izinara.template", string="Template pengurusan izin",
                                         tracking=True, index=True)
    permit_template_manual = fields.Boolean(
        string="Template dipilih manual",
        help="Bila dicentang, aturan pemetaan tidak akan mengganti template barang ini.")
    permit_country_id = fields.Many2one("res.country", string="Negara asal")
    permit_origin_label = fields.Char(string="Negara asal (item master)")
    permit_category = fields.Char(string="Kategori (item master)", help="Kolom 02.Category, mis. 2-FROZEN")
    permit_group = fields.Char(string="Grup (item master)", help="Kolom 03.Group, mis. A-MEAT")
    permit_group_code = fields.Char(string="Kode grup", compute="_compute_permit_group_code", store=True)
    permit_subgroup = fields.Char(string="Subgrup (item master)")
    permit_brand = fields.Char(string="Merek (item master)")
    permit_hs_code = fields.Char(string="Kode HS")
    permit_non_halal = fields.Boolean(string="Non-halal")
    permit_food_group = fields.Selection(string="Kelompok pengurusan",
                                         related="permit_template_id.food_group", store=True)
    permit_product_kind = fields.Selection(PRODUCT_KINDS, string="Jenis produk", compute="_compute_permit_product_kind",
                                           store=True, readonly=False)
    permit_is_import = fields.Boolean(string="Barang impor", compute="_compute_permit_is_import", store=True)
    permit_type_ids = fields.Many2many("izinara.type", string="Izin yang diperlukan",
                                       compute="_compute_permit_type_ids")

    @api.depends("permit_group")
    def _compute_permit_group_code(self):
        for product in self:
            product.permit_group_code = (product.permit_group or "")[:1].upper() or False

    @api.depends("permit_group", "permit_subgroup", "permit_hs_code", "name")
    def _compute_permit_product_kind(self):
        for product in self:
            if product.permit_group:
                product.permit_product_kind = product_kind(product.permit_group_code, product.permit_subgroup,
                                                           product.permit_hs_code, product.name)
            else:
                product.permit_product_kind = False

    @api.depends("permit_country_id", "permit_origin_label")
    def _compute_permit_is_import(self):
        for product in self:
            if product.permit_country_id:
                product.permit_is_import = product.permit_country_id.code != "ID"
            else:
                product.permit_is_import = not (product.permit_origin_label or "").upper().startswith("ID")

    @api.depends("permit_template_id.line_ids.type_id")
    def _compute_permit_type_ids(self):
        for product in self:
            product.permit_type_ids = product.permit_template_id.line_ids.type_id

    def _permit_item(self):
        self.ensure_one()
        return {
            "group_code": self.permit_group_code,
            "subgroup": self.permit_subgroup,
            "hs_code": self.permit_hs_code,
            "name": self.name,
            "is_import": self.permit_is_import,
            "non_halal": self.permit_non_halal or bool(NON_HALAL_WORDS.search((self.name or "").upper()))
            or (self.permit_subgroup or "").strip().upper() == "PORK",
        }

    def action_apply_permit_rules(self):
        """Tetapkan template pengurusan dari aturan pemetaan. Barang bertemplate manual dilewati."""
        Rule = self.env["izinara.rule"]
        rules = Rule.search([])
        changed = 0
        for product in self.filtered(lambda p: not p.permit_template_manual):
            item = product._permit_item()
            if item["non_halal"] and not product.permit_non_halal:
                product.permit_non_halal = True
            template = next((r.template_id for r in rules if r._matches(item)), Rule.browse().template_id)
            if template != product.permit_template_id:
                product.permit_template_id = template
                changed += 1
        return changed

    def action_apply_permit_rules_notify(self):
        changed = self.action_apply_permit_rules()
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {"title": _("Aturan pemetaan diterapkan"),
                       "message": _("%(n)s barang mendapat template baru.", n=changed),
                       "type": "success", "sticky": False},
        }

    @api.onchange("permit_template_id")
    def _onchange_permit_template_manual(self):
        if self.permit_template_id:
            self.permit_template_manual = True

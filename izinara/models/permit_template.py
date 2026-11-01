from odoo import _, api, fields, models
from odoo.exceptions import UserError

FOOD_GROUPS = [
    ("psah", "PSAH – Pangan Segar Asal Hewan"),
    ("psai", "PSAI – Pangan Segar Asal Ikan"),
    ("psat", "PSAT – Pangan Segar Asal Tumbuhan"),
    ("ml", "BPOM ML – pangan olahan impor"),
    ("md", "BPOM MD – pangan olahan dalam negeri"),
    ("non_food", "Non-pangan"),
]


class IzinaraTemplate(models.Model):
    """Template pengurusan: paket izin beserta aktivitasnya untuk sekelompok item code."""

    _name = "izinara.template"
    _description = "Template pengurusan izin barang"
    _inherit = ["mail.thread"]
    _order = "sequence, id"

    name = fields.Char(string="Nama template", required=True, tracking=True)
    code = fields.Char(string="Kode", required=True)
    sequence = fields.Integer(default=10)
    food_group = fields.Selection(FOOD_GROUPS, string="Kelompok pengurusan", required=True, default="ml",
                                  tracking=True,
                                  help="Kategori pangan: PSAH/PSAI/PSAT untuk pangan segar, ML/MD untuk pangan olahan. "
                                       "Halal, karantina dan persetujuan impor adalah persyaratan tambahan di dalamnya.")
    description = fields.Text(string="Keterangan")
    line_ids = fields.One2many("izinara.template.line", "template_id", string="Izin yang diperlukan", copy=True)
    activity_ids = fields.One2many("izinara.template.activity", "template_id", string="Aktivitas", copy=True)
    product_tmpl_ids = fields.One2many("product.template", "permit_template_id", string="Item code")
    product_count = fields.Integer(string="Jumlah item", compute="_compute_product_count")
    total_days = fields.Integer(string="Perkiraan waktu (hari)", compute="_compute_total_days",
                                help="Jalur terpanjang dari aktivitas izin wajib.")
    active = fields.Boolean(default=True)

    _sql_constraints = [("code_uniq", "unique(code)", "Kode template harus unik.")]

    def _compute_product_count(self):
        counts = dict(self.env["product.template"]._read_group(
            [("permit_template_id", "in", self.ids)], ["permit_template_id"], ["__count"]))
        for template in self:
            template.product_count = counts.get(template, 0)

    @api.depends("line_ids.mandatory", "activity_ids.duration_days")
    def _compute_total_days(self):
        for template in self:
            mandatory = template.line_ids.filtered("mandatory").type_id
            per_type = [sum(template.activity_ids.filtered(lambda a, t=t: a.type_id == t).mapped("duration_days"))
                        for t in mandatory]
            template.total_days = max(per_type or [0])

    def action_load_standard_activities(self):
        """Isi aktivitas dari langkah standar tiap jenis izin yang belum punya aktivitas di template ini."""
        Activity = self.env["izinara.template.activity"]
        for template in self:
            have = template.activity_ids.type_id
            for line in template.line_ids.sorted(lambda l: (l.sequence, l.type_id.sequence)):
                if line.type_id in have:
                    continue
                for step in line.type_id.step_ids:
                    Activity.create({
                        "regulation_ids": [(6, 0, (step.regulation_ids or line.type_id.regulation_ids).ids)],
                        "doc_spec_ids": [(0, 0, v) for v in step.doc_spec_ids._copy_vals()],
                        "template_id": template.id,
                        "type_id": line.type_id.id,
                        "sequence": step.sequence,
                        "name": step.name,
                        "party_id": step.party_id.id,
                        "duration_days": step.duration_days,
                        "instructions": step.instructions,
                        "deliverable": step.deliverable,
                    })
        return True

    def action_reset_activities(self):
        self.activity_ids.unlink()
        return self.action_load_standard_activities()

    def action_view_products(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Item code: %s", self.name),
            "res_model": "product.template",
            "view_mode": "list,form",
            "domain": [("permit_template_id", "=", self.id)],
            "context": {"default_permit_template_id": self.id},
        }

    def _activities_for(self, permit_type):
        self.ensure_one()
        return self.activity_ids.filtered(lambda a: a.type_id == permit_type).sorted("sequence")

    def copy(self, default=None):
        default = dict(default or {})
        default.setdefault("code", _("%s-SALIN", self.code))
        default.setdefault("name", _("%s (salinan)", self.name))
        return super().copy(default)

    @api.ondelete(at_uninstall=False)
    def _unlink_if_unused(self):
        if self.product_tmpl_ids:
            raise UserError(_("Template masih dipakai item code. Pindahkan item ke template lain dulu."))


class IzinaraTemplateLine(models.Model):
    _name = "izinara.template.line"
    _description = "Izin dalam template pengurusan"
    _order = "template_id, sequence, id"

    template_id = fields.Many2one("izinara.template", required=True, ondelete="cascade")
    sequence = fields.Integer(default=10)
    type_id = fields.Many2one("izinara.type", string="Jenis izin", required=True)
    mandatory = fields.Boolean(string="Wajib", default=True,
                               help="Izin tidak wajib (mis. SKA untuk tarif preferensi) tidak menghambat status siap clearance.")
    note = fields.Char(string="Catatan")
    party_id = fields.Many2one(related="type_id.party_id", string="Bagian")
    scope = fields.Selection(related="type_id.scope")

    _sql_constraints = [("type_uniq", "unique(template_id, type_id)", "Jenis izin sudah ada di template ini.")]


class IzinaraTemplateActivity(models.Model):
    _name = "izinara.template.activity"
    _description = "Aktivitas template pengurusan izin"
    _order = "template_id, type_sequence, type_id, sequence, id"

    template_id = fields.Many2one("izinara.template", required=True, ondelete="cascade")
    type_id = fields.Many2one("izinara.type", string="Jenis izin", required=True)
    type_sequence = fields.Integer(related="type_id.sequence", store=True)
    sequence = fields.Integer(default=10)
    name = fields.Char(string="Aktivitas", required=True)
    party_id = fields.Many2one("izinara.party", string="Bagian", required=True)
    duration_days = fields.Integer(string="Durasi (hari)", default=1)
    instructions = fields.Text(string="Petunjuk")
    deliverable = fields.Char(string="Dokumen hasil")
    regulation_ids = fields.Many2many("izinara.regulation", "izinara_template_activity_regulation_rel",
                                      string="Referensi peraturan")
    doc_spec_ids = fields.One2many("izinara.doc.spec", "activity_id", string="Dokumen wajib", copy=True)
    doc_count = fields.Integer(string="Dokumen", compute="_compute_doc_count")

    def _compute_doc_count(self):
        for act in self:
            act.doc_count = len(act.doc_spec_ids)

    def action_open(self):
        self.ensure_one()
        return {"type": "ir.actions.act_window", "res_model": self._name, "res_id": self.id, "view_mode": "form",
                "target": "new"}

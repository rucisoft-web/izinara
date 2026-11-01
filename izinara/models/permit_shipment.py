from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError

ACTIVE_APP = ("draft", "progress", "submitted")


class IzinaraShipment(models.Model):
    """Rencana impor (satu pengapalan/PO). Dari barangnya dihitung izin yang wajib ada sebelum barang tiba."""

    _name = "izinara.shipment"
    _description = "Pengapalan impor"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "eta, id desc"

    name = fields.Char(string="Nomor", required=True, copy=False, readonly=True, default=lambda self: _("Baru"))
    company_id = fields.Many2one("res.company", string="Perusahaan", required=True,
                                 default=lambda self: self.env.company)
    user_id = fields.Many2one("res.users", string="PIC procurement", default=lambda self: self.env.user, tracking=True)
    partner_id = fields.Many2one("res.partner", string="Eksportir/pemasok", required=True, tracking=True)
    producer_id = fields.Many2one("res.partner", string="Produsen/unit usaha asal",
                                  help="Establishment (RPH/pabrik) di negara asal. Kosong = sama dengan eksportir.")
    country_id = fields.Many2one("res.country", string="Negara asal")
    po_ref = fields.Char(string="No. PO", tracking=True)
    transport = fields.Selection([("sea", "Laut (reefer)"), ("air", "Udara")], string="Moda", default="sea")
    port = fields.Char(string="Pelabuhan tujuan", default="Tanjung Priok")
    etd = fields.Date(string="ETD", tracking=True)
    eta = fields.Date(string="ETA", tracking=True)
    days_to_eta = fields.Integer(string="Hari ke ETA", compute="_compute_days_to_eta")
    state = fields.Selection([
        ("draft", "Rencana"),
        ("permits", "Pengurusan izin"),
        ("ready", "Siap clearance"),
        ("cleared", "Sudah keluar pelabuhan"),
        ("done", "Selesai"),
        ("cancel", "Batal"),
    ], string="Status", default="draft", tracking=True, copy=False)
    line_ids = fields.One2many("izinara.shipment.line", "shipment_id", string="Barang", copy=True)
    requirement_ids = fields.One2many("izinara.requirement", "shipment_id", string="Kebutuhan izin",
                                      copy=False)
    application_ids = fields.One2many("izinara.application", "shipment_id", string="Pengurusan", copy=False)
    application_count = fields.Integer(compute="_compute_counts")
    readiness = fields.Float(string="Kesiapan izin (%)", compute="_compute_readiness")
    missing_count = fields.Integer(string="Izin belum ada", compute="_compute_readiness")
    no_template_count = fields.Integer(string="Barang tanpa template", compute="_compute_readiness")
    note = fields.Text(string="Catatan")
    memo_ids = fields.One2many("izinara.memo", "shipment_id", string="Memo antar bagian")
    memo_count = fields.Integer(compute="_compute_counts")
    document_ids = fields.One2many("izinara.document", "shipment_id", string="Dokumen")
    doc_review_count = fields.Integer(string="Dokumen menunggu verifikasi", compute="_compute_counts")
    channel_id = fields.Many2one("discuss.channel", string="Ruang diskusi", copy=False, readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("Baru")) == _("Baru"):
                vals["name"] = self.env["ir.sequence"].next_by_code("izinara.shipment") or _("Baru")
        return super().create(vals_list)

    def _compute_days_to_eta(self):
        today = fields.Date.context_today(self)
        for shp in self:
            shp.days_to_eta = (shp.eta - today).days if shp.eta else 0

    def _compute_counts(self):
        for shp in self:
            shp.application_count = len(shp.application_ids)
            shp.memo_count = len(shp.memo_ids)
            shp.doc_review_count = len(shp.document_ids.filtered(lambda d: d.state == "review"))

    @api.depends("requirement_ids.state", "line_ids.permit_template_id")
    def _compute_readiness(self):
        for shp in self:
            mandatory = shp.requirement_ids.filtered("mandatory")
            covered = mandatory.filtered(lambda r: r.state == "covered")
            shp.readiness = 100.0 * len(covered) / len(mandatory) if mandatory else 0.0
            shp.missing_count = len(mandatory) - len(covered)
            shp.no_template_count = len(shp.line_ids.filtered(lambda l: not l.permit_template_id))

    def action_compute_requirements(self):
        """Susun daftar izin dari template tiap barang. Kebutuhan yang sudah punya pengurusan tidak dihapus."""
        Req = self.env["izinara.requirement"]
        for shp in self:
            shp.requirement_ids.filtered(lambda r: not r.application_id).unlink()
            existing = {(r.type_id.id, r.product_tmpl_id.id): r for r in shp.requirement_ids}
            wanted = {}
            for line in shp.line_ids:
                for tline in line.permit_template_id.line_ids:
                    ptype = tline.type_id
                    product = line.product_tmpl_id if ptype.scope == "product" else self.env["product.template"]
                    key = (ptype.id, product.id)
                    wanted.setdefault(key, {"mandatory": False, "template": line.permit_template_id})
                    wanted[key]["mandatory"] |= tline.mandatory
            for (type_id, product_id), info in wanted.items():
                if (type_id, product_id) in existing:
                    existing[(type_id, product_id)].mandatory = info["mandatory"]
                    continue
                Req.create({"shipment_id": shp.id, "type_id": type_id, "product_tmpl_id": product_id or False,
                            "template_id": info["template"].id, "mandatory": info["mandatory"]})
            if shp.state == "draft":
                shp.state = "permits"
        return True

    def action_create_applications(self):
        """Buat dan mulai pengurusan untuk setiap kebutuhan izin yang belum tertutup izin berlaku."""
        App = self.env["izinara.application"]
        for shp in self:
            if not shp.requirement_ids:
                shp.action_compute_requirements()
            todo = shp.requirement_ids.filtered(
                lambda r: r.state == "missing" and not (r.application_id and r.application_id.state in ACTIVE_APP))
            groups = {}
            for req in todo:
                groups.setdefault((req.type_id, req.template_id), self.env["izinara.requirement"])
                groups[(req.type_id, req.template_id)] |= req
            new_apps = App
            for (ptype, template), reqs in sorted(groups.items(), key=lambda g: (g[0][0].sequence, g[0][0].id)):
                deadline = shp.eta
                if deadline and ptype.scope != "shipment":
                    deadline = deadline - timedelta(days=7)
                app = App.create({
                    "type_id": ptype.id,
                    "template_id": template.id,
                    "company_id": shp.company_id.id,
                    "shipment_id": shp.id,
                    "partner_id": (shp.producer_id or shp.partner_id).id,
                    "product_tmpl_ids": [(6, 0, reqs.product_tmpl_id.ids)],
                    "date_deadline": deadline,
                    "user_id": (ptype.party_id._default_user() or self.env.user).id,
                })
                reqs.application_id = app
                new_apps |= app
            new_apps.action_start()
        return self.action_view_applications()

    def action_check_ready(self):
        for shp in self:
            missing = shp.requirement_ids.filtered(lambda r: r.mandatory and r.state != "covered")
            if missing:
                raise UserError(_("Izin belum lengkap:\n%s", "\n".join(
                    "- %s%s" % (r.type_id.name, f" ({r.product_tmpl_id.default_code})" if r.product_tmpl_id else "")
                    for r in missing[:30])))
            shp.state = "ready"

    def action_cleared(self):
        self.write({"state": "cleared"})

    def action_done(self):
        self.write({"state": "done"})

    def action_cancel(self):
        self.application_ids.filtered(lambda a: a.state in ACTIVE_APP).action_cancel()
        self.write({"state": "cancel"})

    def action_view_applications(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Pengurusan %s", self.name),
            "res_model": "izinara.application",
            "view_mode": "list,kanban,form",
            "domain": [("shipment_id", "=", self.id)],
            "context": {"default_shipment_id": self.id},
        }

    def _channel_partners(self):
        self.ensure_one()
        users = self.user_id | self.application_ids.user_id | self.application_ids.step_ids.user_id
        users |= self.application_ids.step_ids.party_id.user_ids
        return users.partner_id

    def action_open_channel(self):
        """Ruang diskusi (Discuss) per pengapalan, berisi semua petugas bagian yang terlibat."""
        self.ensure_one()
        if not self.channel_id:
            channel = self.env["discuss.channel"].create({
                "channel_type": "channel",
                "name": _("%(no)s – %(partner)s", no=self.name, partner=self.partner_id.name),
                "description": _("Diskusi pengurusan izin pengapalan %(no)s (PO %(po)s, ETA %(eta)s)",
                                 no=self.name, po=self.po_ref or "-", eta=self.eta or "-"),
            })
            self.channel_id = channel
        partners = self._channel_partners() | self.env.user.partner_id
        missing = partners - self.channel_id.channel_member_ids.partner_id
        if missing:
            self.channel_id.add_members(partner_ids=missing.ids, post_joined_message=False)
        return {
            "type": "ir.actions.client",
            "tag": "mail.action_discuss",
            "params": {"active_id": f"discuss.channel_{self.channel_id.id}"},
            "context": {"active_id": self.channel_id.id},
        }

    def action_view_memos(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Memo %s", self.name),
            "res_model": "izinara.memo",
            "view_mode": "list,form",
            "domain": [("shipment_id", "=", self.id)],
            "context": {"default_shipment_id": self.id},
        }

    def action_view_documents(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Dokumen %s", self.name),
            "res_model": "izinara.document",
            "view_mode": "list,form",
            "domain": [("shipment_id", "=", self.id)],
        }

    @api.model
    def _cron_check_eta(self):
        """Ingatkan PIC bila ETA tinggal 14 hari tetapi izin wajib belum lengkap."""
        todo = self.env.ref("mail.mail_activity_data_todo", raise_if_not_found=False)
        today = fields.Date.context_today(self)
        for shp in self.search([("state", "=", "permits"), ("eta", "!=", False),
                                ("eta", "<=", today + timedelta(days=14))]):
            if shp.missing_count and todo and shp.user_id and not shp.activity_ids:
                shp.activity_schedule(activity_type_id=todo.id, user_id=shp.user_id.id, date_deadline=shp.eta,
                                      summary=_("%s izin wajib belum terbit, ETA %s", shp.missing_count, shp.eta))


class IzinaraShipmentLine(models.Model):
    _name = "izinara.shipment.line"
    _description = "Barang dalam pengapalan impor"

    shipment_id = fields.Many2one("izinara.shipment", required=True, ondelete="cascade")
    product_tmpl_id = fields.Many2one("product.template", string="Item", required=True)
    default_code = fields.Char(related="product_tmpl_id.default_code", string="Item code")
    hs_code = fields.Char(related="product_tmpl_id.permit_hs_code", string="HS")
    permit_template_id = fields.Many2one(related="product_tmpl_id.permit_template_id", string="Template izin")
    non_halal = fields.Boolean(related="product_tmpl_id.permit_non_halal", string="Non-halal")
    food_group = fields.Selection(related="product_tmpl_id.permit_food_group", string="Kelompok")
    product_kind = fields.Selection(related="product_tmpl_id.permit_product_kind", string="Jenis produk")
    qty_kg = fields.Float(string="Jumlah (kg)")


class IzinaraRequirement(models.Model):
    """Satu izin yang dibutuhkan pengapalan, beserta izin berlaku atau pengurusan yang menutupnya."""

    _name = "izinara.requirement"
    _description = "Kebutuhan izin pengapalan"
    _order = "shipment_id, type_sequence, type_id, product_tmpl_id"

    shipment_id = fields.Many2one("izinara.shipment", required=True, ondelete="cascade", index=True)
    type_id = fields.Many2one("izinara.type", string="Jenis izin", required=True)
    type_sequence = fields.Integer(related="type_id.sequence", store=True)
    scope = fields.Selection(related="type_id.scope")
    party_id = fields.Many2one(related="type_id.party_id", string="Bagian", store=True)
    product_tmpl_id = fields.Many2one("product.template", string="Item")
    template_id = fields.Many2one("izinara.template", string="Template")
    mandatory = fields.Boolean(string="Wajib", default=True)
    application_id = fields.Many2one("izinara.application", string="Pengurusan")
    license_id = fields.Many2one("izinara.license", string="Izin berlaku", compute="_compute_state")
    state = fields.Selection([("covered", "Lengkap"), ("progress", "Diurus"), ("rejected", "Ditolak"),
                              ("missing", "Belum ada")], string="Status", compute="_compute_state")

    def _license_domain(self):
        shp = self.shipment_id
        domain = [("type_id", "=", self.type_id.id), ("company_id", "=", shp.company_id.id),
                  ("state", "in", ("valid", "expiring"))]
        if self.scope == "supplier":
            domain.append(("partner_id", "in", (shp.producer_id | shp.partner_id).ids))
        elif self.scope == "product":
            domain.append(("product_tmpl_ids", "in", self.product_tmpl_id.ids))
        elif self.scope == "shipment":
            domain.append(("shipment_id", "=", shp.id))
        return domain

    @api.depends("application_id.state", "application_id.license_id")
    def _compute_state(self):
        License = self.env["izinara.license"]
        today = fields.Date.context_today(self)
        for req in self:
            day = req.shipment_id.eta or today
            lic = License.search(req._license_domain()).filtered(lambda l: l._is_valid_on(day))[:1]
            req.license_id = lic
            app_state = req.application_id.state
            if lic:
                req.state = "covered"
            elif app_state in ACTIVE_APP:
                req.state = "progress"
            elif app_state == "rejected":
                req.state = "rejected"
            else:
                req.state = "missing"

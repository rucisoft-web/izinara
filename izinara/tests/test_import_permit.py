import base64
from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install", "izinara")
class TestImportPermit(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Product = cls.env["product.template"]
        cls.supplier = cls.env["res.partner"].create({"name": "AMH Australia"})
        cls.au = cls.env.ref("base.au")

    def item(self, code, name, group, subgroup, hs, origin="AU-AUSTRALIA", non_halal=False):
        product = self.Product.create({
            "name": name, "default_code": code, "permit_group": group, "permit_subgroup": subgroup,
            "permit_hs_code": hs, "permit_origin_label": origin, "permit_non_halal": non_halal,
        })
        product.action_apply_permit_rules()
        return product

    def test_rules_map_item_master_groups(self):
        cases = [
            ("AAU1AMH005", "AUS CHL 2243 RIBEYE 3.1KG UP", "A-MEAT", "BEEF", "02013000", "T_MEAT_HALAL"),
            ("ADK2DAN002", "DMK FRZ DANE PORK BELLY SKINLESS", "A-MEAT", "PORK", "02032900", "T_PORK"),
            ("X1", "US FRZ KUROBUTA CT BUTT", "A-MEAT", "", "02032900", "T_PORK"),
            ("X2", "NOR FRZ SALMON FILLET", "B-SEAFOOD", "FISH", "03048100", "T_SEAFOOD"),
            ("X3", "DMK BEEF FRANKFURTER", "D-PROCESSED MEAT & DELICATESSENS", "SAUSAGES", "16010000",
             "T_PROC_MEAT"),
            ("X4", "ESP PORK CHORIZO", "D-PROCESSED MEAT & DELICATESSENS", "COLD CUTS", "16010000", "T_PROC_PORK"),
            ("X5", "ARG FRZ BUTTER 25KG", "F-DAIRY & ALTERNATIVES", "BUTTER", "04051000", "T_DAIRY"),
            ("X6", "BEL FRZ FRIES 9MM", "E-VEGETABLES, FRUITS & POTATOES", "POTATOES", "20041000", "T_PROCESSED"),
            ("X7", "CHN FRZ BROCCOLI", "E-VEGETABLES, FRUITS & POTATOES", "VEGETABLES", "07108000", "T_FRESH_PLANT"),
            ("X8", "ITA PASTA PENNE", "G-GROCERY & INGREDIENTS", "PASTA / GRAINS", "19021900", "T_PROCESSED"),
            ("X9", "BOX KARTON", "O-OTHERS", "PACKAGING", "", "T_NONFOOD"),
        ]
        for code, name, group, sub, hs, expected in cases:
            product = self.item(code, name, group, sub, hs)
            self.assertEqual(product.permit_template_id.code, expected, name)
        local = self.item("L1", "BEEF SALAMI 500GR", "D-PROCESSED MEAT & DELICATESSENS", "COLD CUTS", "",
                          origin="ID-INDONESIA")
        self.assertEqual(local.permit_template_id.code, "T_LOCAL_MD")
        self.assertEqual(local.permit_food_group, "md")
        local_beef = self.item("L2", "LOCAL BEEF TENDERLOIN", "A-MEAT", "BEEF", "02013000", origin="ID-INDONESIA")
        self.assertEqual(local_beef.permit_food_group, "psah")

    def test_food_group_and_product_kind(self):
        cases = [
            ("AUS FRZ BEEF TONGUE", "A-MEAT", "BEEF", "02062100", "psah", "jeroan"),
            ("AUS FRZ BEEF STRIPLOIN", "A-MEAT", "BEEF", "02023000", "psah", "daging"),
            ("NZ FRZ LAMB CARCASS", "A-MEAT", "LAMB", "02043000", "psah", "karkas"),
            ("BRA FRZ CHICKEN LEG", "C-POULTRY", "CHICKEN", "02071400", "psah", "unggas"),
            ("NOR FRZ SALMON", "B-SEAFOOD", "FISH", "03031300", "psai", "ikan"),
            ("VNM FRZ VANNAMEI SHRIMP", "B-SEAFOOD", "SHRIMP", "03061700", "psai", "krustasea"),
            ("JPN FRZ HOKKAIDO SCALLOP", "B-SEAFOOD", "SCALLOP", "03072200", "psai", "moluska"),
            ("CHN FRZ BROCCOLI", "E-VEGETABLES, FRUITS & POTATOES", "VEGETABLES", "07108000", "psat", "sayur"),
            ("ITA PASTA PENNE", "G-GROCERY & INGREDIENTS", "PASTA / GRAINS", "19021900", "ml", "pangan_olahan"),
        ]
        for i, (name, group, sub, hs, food, kind) in enumerate(cases):
            product = self.item(f"K{i}", name, group, sub, hs)
            self.assertEqual((product.permit_food_group, product.permit_product_kind), (food, kind), name)

    def test_manual_template_is_kept(self):
        product = self.item("AAU1", "AUS CHL STRIPLOIN", "A-MEAT", "BEEF", "02013000")
        dairy = self.env.ref("izinara.template_t_dairy")
        product.write({"permit_template_id": dairy.id, "permit_template_manual": True})
        product.action_apply_permit_rules()
        self.assertEqual(product.permit_template_id, dairy)

    def test_templates_have_activities_with_parties(self):
        templates = self.env["izinara.template"].search([])
        self.assertTrue(templates)
        for template in templates:
            self.assertEqual(set(template.activity_ids.type_id.ids), set(template.line_ids.type_id.ids), template.name)
            self.assertTrue(all(template.activity_ids.mapped("party_id")))
        purchasing = self.env.ref("izinara.party_purchasing")
        shln = self.env.ref("izinara.type_shln")
        self.assertEqual(shln.step_ids[0].party_id, purchasing, "kontak prinsipal lewat Purchasing")

    def test_shipment_flow(self):
        beef = self.item("AAU1AMH005", "AUS CHL 2243 RIBEYE", "A-MEAT", "BEEF", "02013000")
        eta = fields.Date.today() + timedelta(days=30)
        nib = self.env.ref("izinara.type_nib_api")
        self.env["izinara.license"].create({"name": "NIB-123", "type_id": nib.id})
        shipment = self.env["izinara.shipment"].create({
            "partner_id": self.supplier.id, "country_id": self.au.id, "eta": eta,
            "line_ids": [(0, 0, {"product_tmpl_id": beef.id, "qty_kg": 20000})],
        })
        shipment.action_compute_requirements()
        codes = set(shipment.requirement_ids.type_id.mapped("code"))
        self.assertTrue({"RP_KEMENTAN", "PI_KEMENDAG", "SHLN", "QUARANTINE_ANIMAL", "CUSTOMS_PIB"} <= codes)
        nib_req = shipment.requirement_ids.filtered(lambda r: r.type_id == nib)
        self.assertEqual(nib_req.state, "covered")
        self.assertLess(shipment.readiness, 100)
        with self.assertRaises(UserError):
            shipment.action_check_ready()

        shipment.action_create_applications()
        apps = shipment.application_ids
        self.assertNotIn(nib, apps.type_id, "izin yang sudah berlaku tidak diurus ulang")
        self.assertTrue(all(a.state == "progress" and a.step_ids for a in apps))

        rp = apps.filtered(lambda a: a.type_id.code == "RP_KEMENTAN")
        self.assertEqual(rp.product_tmpl_ids, beef)
        with self.assertRaises(UserError):
            rp.step_ids.filtered("document_ids")[:1].action_done()
        rp.step_ids.with_context(permit_skip_doc_check=True).action_done()
        self.assertEqual(rp.state, "submitted")
        with self.assertRaises(UserError):
            rp.action_approve()
        rp.permit_number = "RP-2026-001"
        rp.action_approve()
        self.assertEqual(rp.state, "approved")
        self.assertEqual(rp.license_id.product_tmpl_ids, beef)
        self.assertTrue(rp.license_id.date_expiry)
        rp_req = shipment.requirement_ids.filtered(lambda r: r.type_id.code == "RP_KEMENTAN")
        self.assertEqual(rp_req.state, "covered")

        for app in apps - rp:
            app.permit_number = "NO-%s" % app.id
            app.action_approve()
        shipment.invalidate_recordset()
        self.assertEqual(shipment.readiness, 100)
        shipment.action_check_ready()
        self.assertEqual(shipment.state, "ready")

        second = shipment.copy({"eta": eta + timedelta(days=10)})
        second.action_compute_requirements()
        covered = second.requirement_ids.filtered(lambda r: r.state == "covered").type_id.mapped("code")
        self.assertIn("RP_KEMENTAN", covered, "izin per barang dipakai ulang pengapalan berikutnya")
        self.assertNotIn("CUSTOMS_PIB", covered, "izin per pengapalan harus diurus lagi")

    def test_license_expiry_cron(self):
        ml = self.env.ref("izinara.type_ml_bpom")
        lic = self.env["izinara.license"].create({
            "name": "ML 123", "type_id": ml.id, "date_expiry": fields.Date.today() + timedelta(days=30)})
        old = self.env["izinara.license"].create({
            "name": "ML 001", "type_id": ml.id, "date_expiry": fields.Date.today() - timedelta(days=1)})
        self.env["izinara.license"]._cron_check_expiry()
        self.assertEqual(lic.state, "expiring")
        self.assertEqual(old.state, "expired")

    def test_item_master_import_csv(self):
        text = ("ITEMCODE,ITEMNAME,01.Country,02.Category,03.Group,04.SubGroup,05.Brand,11. HS Code,U_Non_Halal\n"
                "AAU1BLP001,AUS CHL TOMAHAWK,AU-AUSTRALIA,1-CHILLED,A-MEAT,BEEF,BLP-BLACK PEARL,02012000,\n"
                "AUS2FAR017,US FRZ PORK TENDERLOIN,US-UNITED STATES,2-FROZEN,A-MEAT,PORK,FAR,02032900,Y\n"
                "NNW2SAL001,NOR FRZ SALMON,NW-NORWAY,2-FROZEN,B-SEAFOOD,FISH,-,03031300,\n")
        wizard = self.env["izinara.item.import"].create({
            "file": base64.b64encode(text.encode()), "file_name": "item.csv"})
        wizard.action_import()
        products = self.Product.search([("default_code", "in", ["AAU1BLP001", "AUS2FAR017", "NNW2SAL001"])])
        self.assertEqual(len(products), 3)
        by_code = {p.default_code: p for p in products}
        self.assertEqual(by_code["AAU1BLP001"].permit_template_id.code, "T_MEAT_HALAL")
        self.assertEqual(by_code["AUS2FAR017"].permit_template_id.code, "T_PORK")
        self.assertEqual(by_code["NNW2SAL001"].permit_country_id.code, "NO")
        self.assertIn("3 barang dibuat", wizard.result)

    def test_document_verification_and_memo(self):
        beef = self.item("AAU2", "AUS FRZ RIBEYE", "A-MEAT", "BEEF", "02023000")
        shipment = self.env["izinara.shipment"].create({
            "partner_id": self.supplier.id, "eta": fields.Date.today() + timedelta(days=30),
            "line_ids": [(0, 0, {"product_tmpl_id": beef.id})]})
        shipment.action_create_applications()
        shln = shipment.application_ids.filtered(lambda a: a.type_id.code == "SHLN")
        step = shln.step_ids[0]
        doc = step.document_ids[:1]
        self.assertTrue(doc, "langkah pertama SHLN meminta sertifikat halal LN")
        self.assertTrue(step.regulation_ids, "referensi peraturan ikut ke aktivitas")
        with self.assertRaises(UserError):
            doc.action_submit_review()  # belum ada file
        Att = self.env["ir.attachment"]
        files = Att.create([
            {"name": "halal.pdf", "datas": base64.b64encode(b"%PDF-1.4 contoh")},
            {"name": "daftar_produk.xlsx", "datas": base64.b64encode(b"PK contoh")},
            {"name": "foto.jpg", "datas": base64.b64encode(b"jpeg contoh")},
        ])
        doc.attachment_ids = [(6, 0, files.ids)]
        doc.date_expiry = fields.Date.today() + timedelta(days=5)
        with self.assertRaises(UserError):
            doc.action_submit_review()  # habis sebelum ETA
        doc.date_expiry = fields.Date.today() + timedelta(days=400)
        bad = Att.create({"name": "virus.exe", "datas": base64.b64encode(b"MZ")})
        doc.attachment_ids = [(4, bad.id)]
        with self.assertRaises(UserError):
            doc.action_submit_review()  # jenis file tidak diizinkan
        doc.attachment_ids = [(3, bad.id)]
        doc.action_submit_review()
        self.assertEqual(doc.state, "review")
        with self.assertRaises(UserError):
            doc.action_verify()  # checklist belum dicentang
        doc.reject_reason = "Daftar produk tidak mencakup item AAU2"
        doc.action_reject()
        self.assertEqual(doc.state, "rejected")
        doc.action_submit_review()
        doc.check_ids.write({"ok": True})
        doc.action_verify()
        self.assertEqual(doc.state, "verified")
        self.assertEqual(doc.revision, 2)
        step.action_done()
        self.assertTrue(step.done)

        halal = self.env.ref("izinara.party_halal")
        purchasing = self.env.ref("izinara.party_purchasing")
        buyer = self.env["res.users"].create({"name": "Budi Purchasing", "login": "budi.purchasing@example.com"})
        purchasing.user_ids = [(6, 0, buyer.ids)]
        memo = self.env["izinara.memo"].create({
            "subject": "Mohon sertifikat halal terbaru dari prinsipal", "from_party_id": halal.id,
            "to_party_id": purchasing.id, "shipment_id": shipment.id, "application_id": shln.id})
        memo.action_send()
        self.assertEqual(memo.state, "open")
        self.assertEqual(memo.assignee_id, buyer)
        with self.assertRaises(UserError):
            memo.action_answer()
        memo.answer = "<p>Sudah diminta, dikirim besok.</p>"
        memo.action_answer()
        self.assertEqual(memo.state, "answered")
        self.assertTrue(memo.on_time)

        data = self.env["izinara.dashboard"].get_dashboard_data()
        self.assertGreaterEqual(data["kpi"]["apps_open"], 1)
        self.assertTrue(any(p["name"] == purchasing.name for p in data["parties"]))
        action = shipment.action_open_channel()
        self.assertTrue(shipment.channel_id)
        self.assertEqual(action["tag"], "mail.action_discuss")

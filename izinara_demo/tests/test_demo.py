from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install", "izinara")
class TestDemo(TransactionCase):
    def test_demo_covers_features(self):
        env = self.env
        self.assertEqual(env["izinara.shipment"].search_count([]), 7)
        types = env["izinara.application"].search([]).type_id.mapped("code")
        all_types = env["izinara.type"].search([]).mapped("code")
        licensed = env["izinara.license"].search([]).type_id.mapped("code")
        self.assertFalse(set(all_types) - set(types) - set(licensed), "setiap jenis izin punya data contoh")
        states = set(env["izinara.application"].search([]).mapped("state"))
        self.assertTrue({"progress", "submitted", "approved", "rejected"} <= states, states)
        doc_states = set(env["izinara.document"].search([]).mapped("state"))
        self.assertTrue({"review", "verified", "rejected"} <= doc_states, doc_states)
        self.assertTrue(env["izinara.memo"].search([("overdue", "=", True)]))
        self.assertTrue(env["izinara.license"].search([("state", "=", "expiring")]))
        self.assertTrue(env["izinara.license"].search([("state", "=", "expired")]))
        data = env["izinara.dashboard"].get_dashboard_data()
        self.assertTrue(data["kpi"]["shipments_risk"])
        self.assertTrue(data["late_steps"])
        ex = env["izinara.dashboard"].get_executive_data()["executive"]
        self.assertGreater(ex["items_mapped"], 0)
        self.assertLessEqual(ex["items_mapped"], ex["items_total"])
        self.assertEqual(ex["docs_total"], env["izinara.document"].search_count([]))
        self.assertTrue(ex["apps_approved"])
        guide = env["izinara.dashboard"].get_permit_guide_data()
        rp = next(t for t in guide["types"] if t["code"] == "RP_KEMENTAN")
        self.assertIn("Kapan diperlukan", rp["description"])
        self.assertTrue(all(s["instructions"] for s in rp["steps"]))

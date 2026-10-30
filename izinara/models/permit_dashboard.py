from datetime import timedelta

from odoo import api, fields, models

from .permit_template import FOOD_GROUPS

OPEN_APP = ("draft", "progress", "submitted")


class IzinaraDashboard(models.AbstractModel):
    """Data untuk dashboard progres pengurusan izin (client action OWL)."""

    _name = "izinara.dashboard"
    _description = "Dashboard izin impor"

    @api.model
    def get_dashboard_data(self):
        today = fields.Date.context_today(self)
        Shipment = self.env["izinara.shipment"]
        App = self.env["izinara.application"]
        Step = self.env["izinara.application.step"]
        Doc = self.env["izinara.document"]
        Memo = self.env["izinara.memo"]
        License = self.env["izinara.license"]
        Party = self.env["izinara.party"]

        open_steps = Step.search([("done", "=", False), ("app_state", "in", ("progress", "submitted"))])
        late_steps = open_steps.filtered(lambda s: s.date_planned and s.date_planned < today)
        open_apps = App.search([("state", "in", OPEN_APP)])
        open_memos = Memo.search([("state", "=", "open")])
        answered = Memo.search([("state", "in", ("answered", "closed")), ("date_answered", "!=", False)])
        expiring = License.search([("state", "in", ("valid", "expiring")), ("date_expiry", "!=", False),
                                   ("date_expiry", "<=", today + timedelta(days=90))], order="date_expiry")

        shipments = []
        for shp in Shipment.search([("state", "in", ("draft", "permits", "ready"))], order="eta", limit=12):
            shipments.append({
                "id": shp.id, "name": shp.name, "partner": shp.partner_id.name, "po": shp.po_ref or "",
                "eta": fields.Date.to_string(shp.eta) if shp.eta else "", "days_to_eta": shp.days_to_eta,
                "readiness": round(shp.readiness), "missing": shp.missing_count,
                "state": dict(shp._fields["state"].selection)[shp.state],
                "risk": bool(shp.eta and shp.missing_count and shp.days_to_eta <= 14),
            })

        parties = []
        for party in Party.search([]):
            p_steps = open_steps.filtered(lambda s: s.party_id == party)
            p_done = Step.search_count([("party_id", "=", party.id), ("done", "=", True)])
            p_memos = answered.filtered(lambda m: m.to_party_id == party)
            parties.append({
                "id": party.id, "name": party.name,
                "open": len(p_steps),
                "late": len(p_steps.filtered(lambda s: s.date_planned and s.date_planned < today)),
                "done": p_done,
                "docs_review": Doc.search_count([("verifier_party_id", "=", party.id), ("state", "=", "review")]),
                "memos_open": len(open_memos.filtered(lambda m: m.to_party_id == party)),
                "memo_hours": round(sum(p_memos.mapped("response_hours")) / len(p_memos), 1) if p_memos else None,
                "memo_on_time": round(100.0 * len(p_memos.filtered("on_time")) / len(p_memos)) if p_memos else None,
            })

        types = []
        for ptype in self.env["izinara.type"].search([]):
            apps = App.search([("type_id", "=", ptype.id)])
            if not apps:
                continue
            states = {s: len(apps.filtered(lambda a, s=s: a.state == s)) for s in
                      ("draft", "progress", "submitted", "approved", "rejected")}
            types.append({"id": ptype.id, "name": ptype.name, "party": ptype.party_id.name, "total": len(apps),
                          **states})

        groups = []
        Product = self.env["product.template"]
        for code, label in FOOD_GROUPS:
            apps = App.search([("food_group", "=", code)])
            items = Product.search_count([("permit_food_group", "=", code)])
            if not apps and not items:
                continue
            groups.append({
                "code": code, "name": label, "items": items, "total": len(apps),
                "approved": len(apps.filtered(lambda a: a.state == "approved")),
                "open": len(apps.filtered(lambda a: a.state in OPEN_APP)),
                "late": len(apps.filtered("overdue")),
                "pct": round(100.0 * len(apps.filtered(lambda a: a.state == "approved")) / len(apps)) if apps else 0,
            })

        return {
            "groups": groups,
            "kpi": {
                "shipments": Shipment.search_count([("state", "in", ("draft", "permits", "ready"))]),
                "shipments_risk": len([s for s in shipments if s["risk"]]),
                "apps_open": len(open_apps),
                "apps_late": len(open_apps.filtered("overdue")),
                "steps_open": len(open_steps),
                "steps_late": len(late_steps),
                "docs_review": Doc.search_count([("state", "=", "review")]),
                "docs_rejected": Doc.search_count([("state", "=", "rejected")]),
                "memos_open": len(open_memos),
                "memos_late": len(open_memos.filtered("overdue")),
                "licenses_expiring": len(expiring),
                "approved_30d": App.search_count([("state", "=", "approved"),
                                                  ("write_date", ">=", fields.Datetime.now() - timedelta(days=30))]),
            },
            "shipments": shipments,
            "parties": parties,
            "types": types,
            "licenses": [{"id": l.id, "name": l.name, "type": l.type_id.name,
                          "expiry": fields.Date.to_string(l.date_expiry), "days": l.days_to_expiry,
                          "expired": l.date_expiry < today} for l in expiring[:10]],
            "late_steps": [{"id": s.id, "name": s.name, "app": s.application_id.name, "party": s.party_id.name,
                            "user": s.user_id.name or "", "planned": fields.Date.to_string(s.date_planned),
                            "days": (today - s.date_planned).days}
                           for s in late_steps.sorted("date_planned")[:10]],
        }

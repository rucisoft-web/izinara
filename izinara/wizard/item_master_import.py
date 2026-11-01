import base64
import csv
import io
import re

from odoo import _, fields, models
from odoo.exceptions import UserError

# Kolom laporan item master SAP (Report_item master). Nama kolom dicocokkan tanpa peduli huruf besar/kecil.
COLUMNS = {
    "code": "ITEMCODE",
    "name": "ITEMNAME",
    "country": "01.COUNTRY",
    "category": "02.CATEGORY",
    "group": "03.GROUP",
    "subgroup": "04.SUBGROUP",
    "brand": "05.BRAND",
    "hs": "11. HS CODE",
    "non_halal": "U_NON_HALAL",
}
# Kode negara di item master yang tidak sama dengan ISO 3166.
COUNTRY_FIX = {"NW": "NO", "SZ": "CH"}


def _clean(value):
    if value is None:
        return ""
    value = str(value).strip()
    return "" if value in ("-", "--NONE--", "None") else value


class IzinaraItemImport(models.TransientModel):
    _name = "izinara.item.import"
    _description = "Impor item master untuk pemetaan izin"

    file = fields.Binary(string="File item master (.xlsx/.csv)", required=True)
    file_name = fields.Char(string="Nama file")
    create_missing = fields.Boolean(string="Buat barang yang belum ada", default=True)
    apply_rules = fields.Boolean(string="Terapkan aturan pemetaan", default=True)
    result = fields.Text(string="Hasil", readonly=True)

    def _rows(self):
        raw = base64.b64decode(self.file)
        if (self.file_name or "").lower().endswith(".csv"):
            text = raw.decode("utf-8-sig")
            dialect = csv.Sniffer().sniff(text[:2048], delimiters=",;\t")
            rows = list(csv.reader(io.StringIO(text), dialect))
        else:
            import openpyxl
            ws = openpyxl.load_workbook(io.BytesIO(raw), read_only=True, data_only=True).active
            rows = [list(r) for r in ws.iter_rows(values_only=True)]
        if not rows:
            raise UserError(_("File kosong."))
        header = [re.sub(r"\s+", " ", str(h or "")).strip().upper() for h in rows[0]]
        index = {}
        for key, col in COLUMNS.items():
            if col in header:
                index[key] = header.index(col)
        if "code" not in index or "name" not in index:
            raise UserError(_("Kolom ITEMCODE dan ITEMNAME wajib ada di baris pertama."))
        for row in rows[1:]:
            item = {key: _clean(row[i]) if i < len(row) else "" for key, i in index.items()}
            if item["code"]:
                yield item

    def _country(self, label, cache):
        if label in cache:
            return cache[label]
        code = label.split("-", 1)[0].strip().upper()
        code = COUNTRY_FIX.get(code, code)
        country = self.env["res.country"].search([("code", "=", code)], limit=1)
        cache[label] = country
        return country

    def action_import(self):
        self.ensure_one()
        Product = self.env["product.template"].with_context(active_test=False)
        seen, created, updated, countries = set(), 0, 0, {}
        touched = Product.browse()
        for item in self._rows():
            if item["code"] in seen:
                continue
            seen.add(item["code"])
            country = self._country(item.get("country", ""), countries) if item.get("country") else False
            vals = {
                "permit_origin_label": item.get("country") or False,
                "permit_country_id": country.id if country else False,
                "permit_category": item.get("category") or False,
                "permit_group": item.get("group") or False,
                "permit_subgroup": item.get("subgroup") or False,
                "permit_brand": item.get("brand") or False,
                "permit_hs_code": re.sub(r"\D", "", item.get("hs", "")) or False,
                "permit_non_halal": item.get("non_halal", "").upper() == "Y",
            }
            product = Product.search([("default_code", "=", item["code"])], limit=1)
            if product:
                product.write(vals)
                updated += 1
            elif self.create_missing:
                product = Product.create(dict(vals, name=item["name"], default_code=item["code"]))
                created += 1
            else:
                continue
            touched |= product
        changed = touched.action_apply_permit_rules() if self.apply_rules else 0
        summary = {}
        for product in touched:
            key = product.permit_template_id.name or _("(tanpa template)")
            summary[key] = summary.get(key, 0) + 1
        lines = [_("%(c)s barang dibuat, %(u)s diperbarui, %(t)s template berubah.", c=created, u=updated, t=changed), ""]
        lines += ["%s: %s" % (name, count) for name, count in sorted(summary.items(), key=lambda kv: -kv[1])]
        self.result = "\n".join(lines)
        return {
            "type": "ir.actions.act_window",
            "res_model": self._name,
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
        }

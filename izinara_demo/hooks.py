"""Data demo Izinara.

Membuat petugas tiap bagian, item code contoh (diambil dari item master Indoguna), izin yang sudah dimiliki dan
tujuh pengapalan dalam tahap berbeda, sehingga setiap fitur terlihat: kesiapan izin per pengapalan, aktivitas per
bagian, unggah banyak file, verifikasi dokumen (lolos/ditolak), memo antar bagian dengan tenggat, ruang diskusi,
register izin yang segera habis dan dashboard. Tanggal dibuat relatif terhadap hari instalasi.
"""
import base64
import io
import zipfile
from datetime import timedelta

from odoo import fields

PASSWORD = "izinara"
JPG = base64.b64decode("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")

USERS = [
    # login, nama, bagian
    ("rina.ml", "Rina Wulandari", "pangan"),
    ("hasan.halal", "Hasan Basri", "halal"),
    ("dewi.izin", "Dewi Lestari", "perizinan"),
    ("budi.purchasing", "Budi Santoso", "purchasing"),
    ("andi.impor", "Andi Pratama", "impor"),
]

PARTNERS = {
    "au": ("Southern Cross Meat Exports Pty Ltd (contoh)", "au"),
    "au_est": ("Establishment 2243 – Southern Cross Abattoir (contoh)", "au"),
    "dk": ("Nordic Pork Export A/S (contoh)", "dk"),
    "dk_est": ("Establishment 1327 – Jutland Pork Plant (contoh)", "dk"),
    "no": ("Fjord Seafood AS (contoh)", "no"),
    "it": ("Tuscany Fine Foods S.r.l. (contoh)", "it"),
    "fr": ("Loire Frozen Vegetables SAS (contoh)", "fr"),
    "ar": ("Pampas Dairy S.A. (contoh)", "ar"),
    "cn": ("Zhejiang Ocean Foods Co. Ltd (contoh)", "cn"),
    "id": ("CV Sumber Daging Nusantara (contoh)", "id"),
}

# item code dari item master: kode, nama, negara, kategori, grup, subgrup, HS, non-halal
ITEMS = [
    ("AAU1AMH005", "AUS CHL 2243 RIBEYE 3.1KG UP", "AU-AUSTRALIA", "1-CHILLED", "A-MEAT", "BEEF", "02013000", False),
    ("AID2LOC055", "AUS BEEF LUNG (PARU) 1KG", "AU-AUSTRALIA", "2-FROZEN", "A-MEAT", "BEEF", "02062900", False),
    ("AID2LOC043", "AUS BEEF CUT SAIKORO", "AU-AUSTRALIA", "2-FROZEN", "A-MEAT", "BEEF", "16025000", False),
    ("AAU1MUL099", "AUS CHL B/IN LAMB HINDSHANK", "AU-AUSTRALIA", "1-CHILLED", "A-MEAT", "LAMB", "02044200", False),
    ("ADK2DAN001", "DMK FRZ DANE PORK BELLY SKIN ON", "DK-DENMARK", "2-FROZEN", "A-MEAT", "PORK", "02032900", True),
    ("DNO1STL004", "NW. FRESH SALMON ORGANIC SIZE 4-5KG", "NW-NORWAY", "1-CHILLED", "B-SEAFOOD", "FISH", "03021400",
     False),
    ("DCN2ZHE001", "FRZ SQUID RING 10 X1KG", "CN-CHINA", "2-FROZEN", "B-SEAFOOD", "SQUID", "03074390", False),
    ("EIT3DEC028", "DE CECCO ALFABETTO OSX0173 24/500 GR", "IT-ITALY", "3-DRY", "G-GROCERY & INGREDIENTS",
     "PASTA / GRAINS", "19021920", False),
    ("EIT3CIA001", "CIAO BAKED BEANS 24X400GR", "IT-ITALY", "3-DRY", "G-GROCERY & INGREDIENTS",
     "PRESERVED CANNED / JARS", "20019090", False),
    ("GFR3DAU019", "DAUCY EXTRA CRISP SWEET CORN 12 X 680GR", "FR-FRANCE", "2-FROZEN",
     "E-VEGETABLES, FRUITS & POTATOES", "VEGETABLES", "07108000", False),
    ("HAU2SAP002", "ARG FRZ UNSALTED SWEET CREAM BUTTER 25KG/CTN", "AR-ARGENTINA", "2-FROZEN",
     "F-DAIRY & ALTERNATIVES", "BUTTER", "04051000", False),
    ("BID2IGU054", "BEEF BOCKWURST SAUSAGE 1KG", "ID-INDONESIA", "2-FROZEN", "D-PROCESSED MEAT & DELICATESSENS",
     "SAUSAGES", "16010000", False),
    ("AID2ALN001", "015 FROZEN BUFFALO MEAT 80 VL ALLANA", "ID-INDONESIA", "2-FROZEN", "A-MEAT", "BUFFALO", "02023000",
     False),
    ("OIT3DEC001", "DE CECCO EMPTY TINS M0BO01CO", "IT-ITALY", "4-NON FOOD", "L-NON FOOD", "PACKAGING", "", False),
]


def _pdf(title):
    text = title.replace("(", "[").replace(")", "]")[:80]
    stream = f"BT /F1 14 Tf 50 780 Td (CONTOH DOKUMEN - {text}) Tj ET".encode("latin-1", "replace")
    objs = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 4 0 R "
        b"/Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    out, offsets = io.BytesIO(), []
    out.write(b"%PDF-1.4\n")
    for i, obj in enumerate(objs, 1):
        offsets.append(out.tell())
        out.write(b"%d 0 obj\n" % i + obj + b"\nendobj\n")
    xref = out.tell()
    out.write(b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1))
    for off in offsets:
        out.write(b"%010d 00000 n \n" % off)
    out.write(b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, xref))
    return out.getvalue()


def _xlsx(title):
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Contoh", title])
    ws.append(["Item code", "Nama", "Jumlah (kg)"])
    ws.append(["AAU1AMH005", "AUS CHL 2243 RIBEYE", 1200])
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


def _docx(title):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("[Content_Types].xml",
                   '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/'
                   '2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-'
                   'package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override '
                   'PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.'
                   'wordprocessingml.document.main+xml"/></Types>')
        z.writestr("_rels/.rels",
                   '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/'
                   'package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/'
                   'officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
        z.writestr("word/document.xml",
                   '<?xml version="1.0" encoding="UTF-8"?><w:document xmlns:w="http://schemas.openxmlformats.org/'
                   'wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>CONTOH DOKUMEN - %s</w:t></w:r></w:p>'
                   '</w:body></w:document>' % title.replace("&", "dan"))
    return buf.getvalue()


class Demo:
    def __init__(self, env):
        self.env = env
        self.today = fields.Date.context_today(env["izinara.application"])
        self.ref = lambda x: env.ref("izinara." + x)
        self.users = {}
        self.partners = {}
        self.products = {}

    # ---------- master ----------
    def setup(self):
        env = self.env
        company = env.ref("base.main_company")
        if company.name in ("My Company", "YourCompany"):
            company.name = "Indoguna Group"
        group = self.ref("group_permit_user")
        manager = self.ref("group_permit_manager")
        for login, name, party in USERS:
            user = env["res.users"].with_context(no_reset_password=True).create({
                "name": name, "login": login, "password": PASSWORD, "email": f"{login}@contoh.indoguna.test",
                "groups_id": [(6, 0, [group.id, env.ref("base.group_user").id])],
            })
            self.ref("party_" + party).user_ids = [(4, user.id)]
            self.users[party] = user
        env["res.users"].with_context(no_reset_password=True).create({
            "name": "Sari Manajer Izin", "login": "sari.manajer", "password": PASSWORD,
            "email": "sari.manajer@contoh.indoguna.test",
            "groups_id": [(6, 0, [manager.id, env.ref("base.group_user").id])],
        })
        for key, (name, country) in PARTNERS.items():
            self.partners[key] = env["res.partner"].create({
                "name": name, "is_company": True, "country_id": env.ref("base." + country).id})
        Product = env["product.template"]
        for code, name, origin, cat, group_, sub, hs, non_halal in ITEMS:
            product = Product.search([("default_code", "=", code)], limit=1) or Product.create(
                {"name": name, "default_code": code})
            iso = {"NW": "no"}.get(origin[:2], origin[:2].lower())
            product.write({
                "permit_origin_label": origin, "permit_country_id": env.ref("base." + iso).id,
                "permit_category": cat, "permit_group": group_, "permit_subgroup": sub, "permit_hs_code": hs or False,
                "permit_non_halal": non_halal, "permit_template_manual": False,
            })
            product.action_apply_permit_rules()
            self.products[code] = product

    def license(self, type_code, number, issue_days, expiry_days, products=(), partner=None, quota=0.0):
        return self.env["izinara.license"].create({
            "name": number, "type_id": self.ref("type_" + type_code.lower()).id,
            "product_tmpl_ids": [(6, 0, [self.products[p].id for p in products])],
            "partner_id": partner.id if partner else False,
            "date_issue": self.today + timedelta(days=issue_days),
            "date_expiry": self.today + timedelta(days=expiry_days) if expiry_days is not None else False,
            "quota": quota,
        })

    # ---------- alur ----------
    def shipment(self, partner, producer, items, eta_days, po, transport="sea", note=""):
        shp = self.env["izinara.shipment"].with_user(self.users["purchasing"]).create({
            "partner_id": self.partners[partner].id,
            "producer_id": self.partners[producer].id if producer else False,
            "country_id": self.partners[partner].country_id.id, "po_ref": po, "transport": transport,
            "etd": self.today + timedelta(days=eta_days - 18), "eta": self.today + timedelta(days=eta_days),
            "user_id": self.users["purchasing"].id, "note": note,
            "line_ids": [(0, 0, {"product_tmpl_id": self.products[c].id, "qty_kg": q}) for c, q in items],
        })
        shp.action_compute_requirements()
        shp.action_create_applications()
        return shp

    def app(self, shp, code):
        return shp.application_ids.filtered(lambda a: a.type_id.code == code)[:1]

    def age(self, app, days):
        """Geser jadwal pengurusan seolah dimulai beberapa hari lalu."""
        if not app:
            return
        app.date_start = app.date_start - timedelta(days=days)
        for step in app.step_ids:
            step.date_planned = step.date_planned - timedelta(days=days)
        if app.date_deadline:
            app.date_deadline = min(app.date_deadline, max(app.step_ids.mapped("date_planned") or [self.today]))

    def files_for(self, doc, kinds=("pdf",)):
        atts = self.env["ir.attachment"]
        for kind in kinds:
            data = {"pdf": _pdf, "xlsx": _xlsx, "docx": _docx}.get(kind)
            raw = data(doc.name) if data else JPG
            name = "%s.%s" % (doc.name.lower().replace(" ", "_").replace("/", "-")[:40], kind)
            atts |= self.env["ir.attachment"].create({
                "name": name, "datas": base64.b64encode(raw), "res_model": "izinara.document", "res_id": doc.id})
        return atts

    def upload(self, doc, kinds=("pdf",)):
        uploader = self.users.get(doc.uploader_party_id.code) or self.env.user
        doc = doc.with_user(uploader)
        doc.attachment_ids = [(6, 0, self.files_for(doc, kinds).ids)]
        vals = {"doc_number": "DOK-%s-%04d" % (self.today.year, doc.id)}
        if doc.check_expiry:
            vals["date_expiry"] = self.today + timedelta(days=365)
        doc.write(vals)
        doc.action_submit_review()
        return doc

    def verify(self, doc):
        verifier = self.users.get(doc.verifier_party_id.code) or self.env.user
        doc = doc.with_user(verifier)
        doc.check_ids.write({"ok": True})
        doc.action_verify()

    def reject(self, doc, reason, ok_first=1):
        verifier = self.users.get(doc.verifier_party_id.code) or self.env.user
        doc = doc.with_user(verifier)
        doc.check_ids[:ok_first].write({"ok": True})
        doc.check_ids[ok_first:ok_first + 1].write({"note": "Tidak sesuai"})
        doc.reject_reason = reason
        doc.action_reject()

    def complete_step(self, step, kinds=("pdf",)):
        for doc in step.document_ids:
            if doc.state in ("missing", "rejected"):
                self.upload(doc, kinds)
            if doc.state == "review":
                self.verify(doc)
        user = step.user_id or self.env.user
        step.with_user(user).action_done()

    def advance(self, app, n_steps, kinds=("pdf",)):
        for step in app.step_ids.sorted("sequence")[:n_steps]:
            if not step.done:
                self.complete_step(step, kinds)

    def approve(self, app, number, expiry_days=None, quota=0.0):
        self.advance(app, len(app.step_ids))
        app.write({"permit_number": number, "date_issue": self.today - timedelta(days=1), "quota": quota,
                   "date_expiry": self.today + timedelta(days=expiry_days) if expiry_days else False})
        app.action_approve()

    def memo(self, frm, to, subject, body, shp=None, app=None, step=None, kind="request", priority="0",
             sent_days_ago=0, deadline_days=2, answer=None, answer_hours=None, close=False):
        memo = self.env["izinara.memo"].with_user(self.users[frm]).create({
            "subject": subject, "body": f"<p>{body}</p>", "kind": kind, "priority": priority,
            "from_party_id": self.ref("party_" + frm).id, "to_party_id": self.ref("party_" + to).id,
            "user_id": self.users[frm].id, "shipment_id": shp.id if shp else False,
            "application_id": app.id if app else False, "step_id": step.id if step else False,
        })
        memo.action_send()
        sent = fields.Datetime.now() - timedelta(days=sent_days_ago)
        memo.sudo().write({"date_sent": sent, "date_deadline": (sent + timedelta(days=deadline_days)).date()})
        if answer:
            memo = memo.with_user(self.users[to])
            memo.answer = f"<p>{answer}</p>"
            memo.action_answer()
            answered = sent + timedelta(hours=answer_hours)
            memo.sudo().write({"date_answered": answered, "response_hours": answer_hours,
                               "on_time": answered.date() <= memo.date_deadline})
            if close:
                memo.with_user(self.users[frm]).action_close()
        return memo

    # ---------- skenario ----------
    def run(self):
        self.setup()
        p = self.partners
        # Izin yang sudah dimiliki perusahaan/barang
        self.license("NIB_API", "9120001234567 (contoh)", -900, None)
        self.license("NKV", "NKV-CS-3372-0001 (contoh)", -400, 1425)
        self.license("EST_APPROVAL", "EST-AU-2243 (contoh)", -300, 65, partner=p["au_est"])
        self.license("EST_APPROVAL", "EST-NO-FJ01 (contoh)", -200, 165, partner=p["no"])
        self.license("EST_APPROVAL", "EST-CN-ZJ88 (contoh)", -100, 265, partner=p["cn"])
        self.license("RP_KEMENTAN", "RP-PKH/2026/0457 (contoh)", -60, 62, products=["AAU1MUL099"], quota=24000)
        self.license("PI_KEMENDAG", "PI-04.PI-05.26.0912 (contoh)", -55, 62, products=["AAU1MUL099"], quota=24000)
        self.license("ML_BPOM", "BPOM RI ML 236509001100 (contoh)", -1780, 45, products=["EIT3DEC028"])
        self.license("ML_BPOM", "BPOM RI ML 236509001187 (contoh)", -700, 1100, products=["EIT3CIA001"])
        self.license("SHLN", "SHLN-ID-AR-2024-0193 (contoh)", -720, -10, products=["HAU2SAP002"])
        self.license("SHLN", "SHLN-ID-IT-2025-0412 (contoh)", -300, 430, products=["EIT3DEC028", "EIT3CIA001"])
        self.license("ML_BPOM", "BPOM RI ML 266301002210 (contoh)", -600, 1200, products=["HAU2SAP002"])
        self.license("RPHP_KKP", "REK-KKP/2026/1180 (contoh)", -40, 120, products=["DCN2ZHE001"], quota=8000)
        self.license("PI_KEMENDAG", "PI-KKP-26.0331 (contoh)", -35, 120, products=["DCN2ZHE001"], quota=8000)

        # 1. Daging sapi Australia (PSAH + 1 olahan ML): ETA 12 hari, berisiko
        s1 = self.shipment("au", "au_est", [("AAU1AMH005", 12000), ("AID2LOC055", 2000), ("AID2LOC043", 1500)], 12,
                           "PO-IGU-2610-031", note="Reefer 40 ft, pelabuhan Tanjung Priok.")
        for code, days in (("RP_KEMENTAN", 20), ("PI_KEMENDAG", 12), ("SHLN", 15), ("ML_BPOM", 30),
                           ("LARTAS_CHECK", 6), ("QUARANTINE_ANIMAL", 5), ("CUSTOMS_PIB", 2), ("COO", 4),
                           ("SKI_BPOM", 6), ("LABEL_ID", 3), ("HALAL_SH", 10)):
            self.age(self.app(s1, code), days)
        self.approve(self.app(s1, "RP_KEMENTAN"), "RP-PKH/2026/0611 (contoh)", 62, quota=40000)
        self.approve(self.app(s1, "LARTAS_CHECK"), "INSW-CEK-%s-0031" % self.today.year)
        pi = self.app(s1, "PI_KEMENDAG")
        self.advance(pi, len(pi.step_ids))
        shln = self.app(s1, "SHLN")
        self.advance(shln, 2, kinds=("pdf", "xlsx", "jpg"))
        ml = self.app(s1, "ML_BPOM")
        ml_doc = ml.step_ids.sorted("sequence")[0].document_ids[:1]
        self.upload(ml_doc, ("pdf", "docx", "xlsx"))
        self.reject(ml_doc, "Komposisi belum 100% (bumbu marinasi tidak dirinci) dan sertifikat HACCP kedaluwarsa. "
                            "Mohon Purchasing minta versi terbaru ke prinsipal.")
        q = self.app(s1, "QUARANTINE_ANIMAL")
        self.upload(q.step_ids.sorted("sequence")[0].document_ids[:1], ("pdf", "jpg"))
        self.advance(self.app(s1, "COO"), 1)
        self.memo("pangan", "purchasing", "Komposisi lengkap Beef Cut Saikoro",
                  "Evaluator BPOM minta komposisi 100% termasuk bumbu marinasi. Mohon diminta ke prinsipal.",
                  shp=s1, app=ml, step=ml.step_ids.sorted("sequence")[0], sent_days_ago=1, deadline_days=2)
        self.memo("impor", "perizinan", "Jadwal pemeriksaan karantina",
                  "Kapal tiba %s. Mohon konfirmasi jadwal pemeriksaan di instalasi karantina." % s1.eta,
                  shp=s1, app=q, kind="question", priority="1", sent_days_ago=3, deadline_days=1,
                  answer="Sudah dilaporkan; pemeriksaan dijadwalkan H+1 setelah sandar.", answer_hours=20)

        # 2. Daging babi Denmark (PSAH non-halal): RP ditolak, unit usaha belum disetujui
        s2 = self.shipment("dk", "dk_est", [("ADK2DAN001", 18000)], 40, "PO-IGU-2610-044")
        for code, days in (("EST_APPROVAL", 25), ("RP_KEMENTAN", 18), ("NONHALAL", 6)):
            self.age(self.app(s2, code), days)
        est = self.app(s2, "EST_APPROVAL")
        self.advance(est, 2)
        rp = self.app(s2, "RP_KEMENTAN")
        self.advance(rp, 3)
        rp.reject_reason = "Unit usaha 1327 belum ada di daftar unit usaha yang disetujui Ditjen PKH."
        rp.action_reject()
        self.approve(self.app(s2, "NONHALAL"), "NH-CHECK-%s-0007" % self.today.year)
        self.memo("perizinan", "purchasing", "Minta prinsipal ajukan penilaian unit usaha 1327",
                  "RP ditolak karena establishment 1327 belum disetujui. Mohon hubungi prinsipal agar otoritas "
                  "veteriner Denmark mengajukan penilaian, atau alihkan ke establishment yang sudah terdaftar.",
                  shp=s2, app=est, kind="escalation", priority="2", sent_days_ago=4, deadline_days=2)

        # 3. Salmon Norwegia (PSAI): semua izin terbit, barang sudah keluar pelabuhan
        s3 = self.shipment("no", None, [("DNO1STL004", 3000)], -2, "PO-IGU-2610-019", transport="air")
        for app in s3.application_ids:
            self.age(app, 14)
            self.approve(app, "%s-%s (contoh)" % (app.type_id.code, app.id), 365 if app.type_id.validity_months else None)
        s3.action_check_ready()
        s3.action_cleared()
        self.memo("purchasing", "impor", "Salmon diterbangkan lebih awal",
                  "AWB sudah terbit, pesawat tiba 2 hari lebih cepat.", shp=s3, kind="info",
                  sent_days_ago=6, deadline_days=1, answer="Siap, PIB disiapkan hari ini.", answer_hours=3, close=True)

        # 4. Pasta & baked beans Italia (BPOM ML): ML sudah ada, tinggal SKI dan label
        s4 = self.shipment("it", None, [("EIT3DEC028", 4800), ("EIT3CIA001", 3600), ("OIT3DEC001", 200)], 30,
                           "PO-IGU-2610-052")
        ski = self.app(s4, "SKI_BPOM")
        self.age(ski, 2)
        self.advance(ski, 1, kinds=("pdf", "xlsx"))
        self.upload(ski.step_ids.sorted("sequence")[1].document_ids[:1]) if ski.step_ids.sorted("sequence")[1].document_ids else None
        self.memo("impor", "pangan", "Nomor SKI untuk PIB",
                  "Mohon nomor SKI dikirim paling lambat H-3 ETA supaya PIB bisa diajukan.", shp=s4, app=ski,
                  sent_days_ago=0, deadline_days=3)

        # 5. Sweet corn beku Prancis (PSAT): registrasi PSAT terlambat
        s5 = self.shipment("fr", None, [("GFR3DAU019", 6000)], 25, "PO-IGU-2610-058")
        for code, days in (("PSAT", 30), ("RIPH", 20), ("QUARANTINE_PLANT", 4)):
            self.age(self.app(s5, code), days)
        self.advance(self.app(s5, "PSAT"), 1, kinds=("pdf", "xlsx"))
        riph = self.app(s5, "RIPH")
        self.advance(riph, 1)
        self.memo("perizinan", "pangan", "Status registrasi PSAT sweet corn",
                  "RIPH menunggu nomor PSAT. Bagaimana status evaluasinya?", shp=s5, kind="question",
                  sent_days_ago=5, deadline_days=2,
                  answer="Masih menunggu koreksi data CoA dari prinsipal.", answer_hours=70)

        # 6. Butter Argentina (BPOM ML): SHLN lama sudah habis, perlu registrasi ulang
        s6 = self.shipment("ar", None, [("HAU2SAP002", 10000)], 20, "PO-IGU-2610-061")
        shln6 = self.app(s6, "SHLN")
        self.age(shln6, 21)
        self.memo("halal", "purchasing", "Sertifikat halal produsen butter yang baru",
                  "SHLN-ID-AR-2024-0193 sudah habis. Mohon minta sertifikat halal terbaru beserta daftar produk dari "
                  "Pampas Dairy.", shp=s6, app=shln6, step=shln6.step_ids.sorted("sequence")[0], priority="2",
                  sent_days_ago=5, deadline_days=2)

        # 7. Cumi Tiongkok (PSAI): rencana, kebutuhan izin baru dihitung
        s7 = self.env["izinara.shipment"].with_user(self.users["purchasing"]).create({
            "partner_id": p["cn"].id, "country_id": p["cn"].country_id.id, "po_ref": "PO-IGU-2611-003",
            "etd": self.today + timedelta(days=30), "eta": self.today + timedelta(days=45),
            "user_id": self.users["purchasing"].id,
            "line_ids": [(0, 0, {"product_tmpl_id": self.products["DCN2ZHE001"].id, "qty_kg": 5000})],
        })
        s7.action_compute_requirements()

        # Pengurusan tanpa pengapalan: produk lokal dan izin perusahaan
        App = self.env["izinara.application"]
        local = App.create({"type_id": self.ref("type_local_supplier").id,
                            "template_id": self.ref("template_t_local_psah").id, "partner_id": p["id"].id,
                            "product_tmpl_ids": [(6, 0, self.products["AID2ALN001"].ids)],
                            "user_id": self.users["purchasing"].id})
        local.action_start()
        self.age(local, 10)
        self.approve(local, "VER-LOKAL-%s-0012" % self.today.year, 365)
        md = App.create({"type_id": self.ref("type_md_bpom").id, "template_id": self.ref("template_t_local_md").id,
                         "product_tmpl_ids": [(6, 0, self.products["BID2IGU054"].ids)],
                         "user_id": self.users["pangan"].id})
        md.action_start()
        self.age(md, 14)
        self.advance(md, 2, kinds=("pdf", "docx"))
        repack = App.create({"type_id": self.ref("type_halal_sh").id,
                             "template_id": self.ref("template_t_meat_halal").id,
                             "product_tmpl_ids": [(6, 0, self.products["AAU1AMH005"].ids)],
                             "user_id": self.users["halal"].id,
                             "note": "Sertifikasi halal untuk porsi steak yang dipotong dan dikemas ulang (Pack ID)."})
        repack.action_start()
        self.age(repack, 9)
        self.advance(repack, 1, kinds=("pdf", "docx"))

        for shp in (s1, s2, s4, s5, s6):
            shp.with_user(self.users["purchasing"]).action_open_channel()
        s1.channel_id.message_post(
            body="Tim, kapal reefer AU tiba %s. RP sudah terbit; PI menunggu. SHLN dan karantina mohon diprioritaskan."
                 % s1.eta, author_id=self.users["purchasing"].partner_id.id, message_type="comment",
            subtype_xmlid="mail.mt_comment")
        self.env["izinara.license"]._cron_check_expiry()


def post_init_hook(env):
    Demo(env).run()

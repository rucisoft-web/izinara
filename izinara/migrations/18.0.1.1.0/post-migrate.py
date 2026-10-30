"""Lengkapi keterangan jenis izin dan petunjuk langkah standar pada database yang sudah terpasang.

Data jenis izin bertanda noupdate, jadi teks baru dari permit_type_data.xml tidak ikut saat upgrade.
Teks hanya diganti bila masih kosong atau masih berupa teks lama (teks baru selalu diawali teks lama),
sehingga perubahan yang dibuat pengguna tidak tertimpa.
"""
from lxml import etree

from odoo import SUPERUSER_ID, api
from odoo.tools import file_path

FIELDS = {"izinara.type": "description", "izinara.type.step": "instructions"}


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    tree = etree.parse(file_path("izinara/data/permit_type_data.xml"))
    for record in tree.iterfind("record"):
        fname = FIELDS.get(record.get("model"))
        node = record.find(f"field[@name='{fname}']") if fname else None
        if node is None or not node.text:
            continue
        target = env.ref(f"izinara.{record.get('id')}", raise_if_not_found=False)
        if not target:
            continue
        current = (target[fname] or "").strip()
        if not current or node.text.startswith(current):
            target[fname] = node.text

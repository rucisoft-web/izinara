{
    "name": "Izinara – Tema Indoguna Group",
    "summary": "Tema ringan dan sederhana untuk Izinara: navbar hitam dengan garis biru tua, aksen navy, halaman "
               "login Indoguna Group (hanya CSS, tanpa font atau gambar tambahan)",
    "version": "18.0.1.0.0",
    "category": "Inventory/Izinara",
    "license": "LGPL-3",
    "author": "Indoguna Group",
    "depends": ["web", "izinara"],
    "data": [
        "views/login_templates.xml",
    ],
    "assets": {
        "web._assets_primary_variables": [
            ("before", "web/static/src/scss/primary_variables.scss",
             "izinara_theme/static/src/scss/primary_variables.scss"),
        ],
        "web.assets_backend": [
            "izinara_theme/static/src/scss/backend.scss",
        ],
        "web.assets_frontend": [
            "izinara_theme/static/src/scss/login.scss",
        ],
    },
    "installable": True,
}

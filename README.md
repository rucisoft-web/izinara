# Izinara

Modul Odoo 18 Community untuk memantau pengurusan izin impor pangan Indoguna Group: dari rencana impor sampai
barang keluar pelabuhan. Izinara menentukan izin yang dibutuhkan tiap item code, membagi aktivitas ke tiap bagian,
memverifikasi dokumen yang diunggah, mencatat komunikasi antar bagian, dan mengingatkan izin yang segera habis.

| Add-on | Isi |
|---|---|
| `izinara` | Modul utama. Kelompok PSAH, PSAI, PSAT, BPOM ML dan BPOM MD dengan jenis produk (karkas, daging, jeroan, daging olahan; ikan, krustasea, moluska; sayur/buah). Template aktivitas per item code, aturan pemetaan item master SAP, pengapalan dan kesiapan izin, tugas per bagian, unggah banyak file dengan verifikasi dokumen, memo antar bagian, ruang diskusi per pengapalan, register izin, referensi peraturan di setiap aktivitas, dashboard, dan menu **Panduan** (ringkasan fungsi, panduan per peran, tangkapan layar). Hanya bergantung pada `mail` dan `product`. |
| `izinara_demo` | Data demo (terpisah): 6 petugas, 14 item code dari item master, 7 pengapalan di berbagai tahap, dokumen, memo dan izin contoh. |
| `izinara_theme` | Tema ringan: navbar hitam bergaris biru tua dan halaman login Indoguna Group. |

Proses, langkah per jenis izin dan daftar dasar hukum: [`izinara/docs/PROSES-PERIZINAN-IMPOR.md`](izinara/docs/PROSES-PERIZINAN-IMPOR.md).
Peraturan bertanda "cek versi terbaru" perlu dikonfirmasi ke JDIH instansi terkait sebelum dipakai.

## Bagian yang terlibat

| Bagian | Tanggung jawab utama |
|---|---|
| Makanan Luar (BPOM) | NIE ML/MD, SKI per pengapalan, label Bahasa Indonesia, registrasi PSAT |
| Sertifikasi Halal | Registrasi SHLN, sertifikat halal produk dikemas ulang, keterangan tidak halal |
| Perizinan | NIB/NKV, persetujuan unit usaha asal, rekomendasi Kementan/KKP, RIPH, karantina |
| Purchasing | Satu-satunya penghubung dengan prinsipal/eksportir luar negeri |
| Impor & Kepabeanan | Cek lartas INSW, Persetujuan Impor, PIB, BM/PDRI, SPPB |

## Memasang

Tambahkan folder repositori ini ke `addons_path` Odoo 18, lalu pasang `izinara` (dan `izinara_theme` bila ingin
tema Indoguna). Pasang `izinara_demo` hanya di database percobaan. Dengan Docker:

```sh
docker compose up        # http://localhost:8069, buat database lalu pasang Izinara
```

Login demo setelah `izinara_demo` terpasang (kata sandi `izinara`): `rina.ml`, `hasan.halal`, `dewi.izin`,
`budi.purchasing`, `andi.impor`, `sari.manajer`.

Untuk data sebenarnya, buka **Izinara > Konfigurasi > Impor item master** dan unggah laporan item master SAP
(.xlsx/.csv). Template izin dipasang otomatis oleh aturan pemetaan dan bisa diubah per item code.

## Tes

```sh
scripts/run-tests.sh --db_host=localhost --db_user=odoo --db_password=odoo
```

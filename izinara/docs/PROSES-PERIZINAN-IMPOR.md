# Izinara – proses pengurusan izin impor pangan Indoguna

Dokumen ini menjelaskan peraturan yang berlaku, kelompok pengurusan, pembagian tugas antar bagian dan langkah
pengurusan tiap izin, sesuai isi modul Odoo 18 **izinara**. Semua data di bawah juga ada di menu
*Izinara > Konfigurasi* dan bisa diubah tanpa pemrograman.

> **Penting.** Nomor dan judul peraturan dikumpulkan per Oktober 2026. Peraturan bertanda *cek versi terbaru* sudah
> diubah atau nomornya perlu dikonfirmasi ke JDIH instansi. Mohon tim legal/perizinan memeriksa daftar ini sebelum
> dipakai sebagai acuan resmi. Lartas per kode HS selalu dicek ulang di INSW untuk setiap pengapalan.

## 1. Kelompok pengurusan

Setiap item code masuk ke satu kelompok. Kelompok menentukan jalur otoritas utama; halal, karantina dan persetujuan
impor adalah persyaratan tambahan di dalam kelompok, bukan kelompok tersendiri.

| Kelompok | Arti | Contoh produk Indoguna | Jalur otoritas utama |
|---|---|---|---|
| **PSAH** | Pangan Segar Asal Hewan | Daging sapi, kerbau, wagyu, domba, babi, unggas, jeroan; segar/dingin/beku | Kementan (Ditjen PKH), Barantin |
| **PSAI** | Pangan Segar Asal Ikan | Ikan, krustasea (udang, kepiting, lobster), moluska (cumi, gurita, kerang, scallop) | KKP, Barantin |
| **PSAT** | Pangan Segar Asal Tumbuhan | Sayur dan buah segar/beku dengan pengolahan minimal | Badan Pangan Nasional, Kementan (RIPH), Barantin |
| **BPOM ML** | Pangan olahan produksi luar negeri | Pasta, saus, keju, mentega, kentang goreng beku, sosis/cold cut impor, kaviar | BPOM |
| **BPOM MD** | Pangan olahan produksi dalam negeri | Sosis dan cold cut bermerek Indoguna, pangan olahan pemasok lokal | BPOM |

Selain kelompok, Izinara memberi **jenis produk** menurut istilah peraturan (dibaca otomatis dari kode HS dan nama
barang): karkas, daging, jeroan (*edible offal*), daging unggas, daging olahan — keempat jenis produk hewan ini
mengikuti Permentan 42/2019 — lalu ikan, krustasea, moluska, olahan ikan, sayuran, buah, susu & olahan susu, pangan
olahan lain dan non-pangan.

## 2. Pihak dan tanggung jawab

| Bagian | Tanggung jawab |
|---|---|
| **Bagian Makanan Luar (Izin Edar ML BPOM)** | Registrasi izin edar ML pangan olahan di BPOM, rancangan label Bahasa Indonesia, SKI BPOM per pengapalan, registrasi PSAT. |
| **Bagian Sertifikasi Halal** | Registrasi Sertifikat Halal Luar Negeri (SHLN) di BPJPH, sertifikasi halal produk yang dikemas ulang, Sistem Jaminan Produk Halal, keterangan tidak halal dan pemisahan produk babi. |
| **Bagian Perizinan (Kementan, KKP, Barantin)** | NIB/API dan NKV, persetujuan unit usaha asal, Rekomendasi Pemasukan Kementan (daging, unggas, olahan), rekomendasi KKP (ikan), RIPH, karantina hewan/ikan/tumbuhan. |
| **Purchasing (Procurement)** | Satu-satunya bagian yang berhubungan dengan prinsipal/eksportir luar negeri: rencana impor, PO, permintaan dokumen (LoA, health certificate, CoA, sertifikat halal, data establishment, SKA, dokumen pengapalan asli) dan data tambahan yang diminta instansi. Juga verifikasi pemasok lokal. |
| **Bagian Impor & Kepabeanan** | Cek lartas HS di INSW, Persetujuan Impor (PI) Kemendag, PIB/BC 2.0, pembayaran BM & PDRI, jalur pemeriksaan, SPPB dan pengeluaran kontainer. |

**Aturan komunikasi:** hanya **Purchasing** yang berhubungan dengan prinsipal/eksportir luar negeri. Bagian lain yang
butuh dokumen atau data dari prinsipal mengirim **memo antar bagian** ke Purchasing di Izinara (dengan tenggat
jawab), bukan menghubungi prinsipal langsung.

## 3. Alur satu pengapalan

1. **Purchasing** membuat *Pengapalan impor* (eksportir, unit usaha asal, PO, ETD/ETA, item code) dan menekan
   *Hitung izin yang diperlukan*. Izinara membaca template izin tiap item code.
2. Izin yang sudah dimiliki dan masih berlaku pada tanggal ETA (NIB, NKV, NIE ML, SHLN, RP/PI berkuota, approval
   unit usaha) otomatis ditandai **Lengkap**.
3. *Buat & mulai pengurusan* membuat satu pengurusan untuk setiap izin yang belum ada, membagi aktivitas ke tiap
   bagian sesuai template, dan mengirim *activity* Odoo ke petugas aktivitas pertama.
4. Tiap petugas mengunggah dokumen (boleh banyak file: PDF, JPG, DOC, XLS, dll.), lalu *Ajukan verifikasi*.
   Izinara mengecek otomatis: ada file, jenis file diizinkan, file tidak kosong, dan dokumen masih berlaku saat ETA.
5. **Bagian verifikator** memeriksa checklist kriteria dokumen. Dokumen *Terverifikasi* atau *Ditolak* dengan
   catatan perbaikan (pengunggah otomatis mendapat tugas perbaikan). Aktivitas baru bisa ditandai selesai bila semua
   dokumen wajibnya terverifikasi.
6. Saat izin terbit, petugas mengisi nomor, tanggal terbit dan masa berlaku. Izin masuk **Register izin** dan dipakai
   ulang oleh pengapalan berikutnya selama masih berlaku.
7. Bila semua izin wajib lengkap, *Cek siap clearance* mengubah status menjadi **Siap clearance**; setelah SPPB,
   **Sudah keluar pelabuhan**.

Urutan umum: NIB/NKV → approval unit usaha asal → rekomendasi teknis (RP Kementan / KKP / RIPH) → PI Kemendag →
izin edar (ML/MD/PSAT) dan SHLN → cek lartas INSW → SKI BPOM, karantina, label → PIB dan SPPB.

**Alat komunikasi:** memo antar bagian (penerima, prioritas, tenggat, waktu respons dan ketepatan waktu tercatat),
diskusi (chatter) di setiap aktivitas, dokumen dan pengurusan, serta *Ruang diskusi* (kanal Discuss) per pengapalan
yang otomatis berisi semua petugas yang terlibat. Dashboard menampilkan rata-rata waktu respons dan persentase
tepat waktu per bagian.

## 4. Template pengurusan per kelompok

W = wajib, O = opsional (tidak menghambat status siap clearance). Jumlah item dari item master Oktober 2026.

| Template | Kelompok | Item | Izin wajib | Opsional |
|---|---|---|---|---|
| Daging merah impor (halal) | PSAH | 1278 | NIB sebagai Angka Pengenal Importir (API-U), Cek HS dan lartas di INSW, PIB (BC 2.0), pembayaran BM/PDRI dan SPPB, NKV unit usaha produk hewan (cold storage/meat shop), Persetujuan negara & unit usaha asal (establishment), Rekomendasi Pemasukan Produk Hewan (RP), Persetujuan Impor (PI) Kemendag, Registrasi Sertifikat Halal Luar Negeri (SHLN), Karantina hewan (produk hewan) | Surat Keterangan Asal (SKA/CoO) untuk tarif preferensi, Sertifikat halal Indonesia (produk dipotong/dikemas ulang) |
| Daging babi impor (non-halal) | PSAH | 51 | NIB sebagai Angka Pengenal Importir (API-U), Cek HS dan lartas di INSW, PIB (BC 2.0), pembayaran BM/PDRI dan SPPB, NKV unit usaha produk hewan (cold storage/meat shop), Persetujuan negara & unit usaha asal (establishment), Rekomendasi Pemasukan Produk Hewan (RP), Persetujuan Impor (PI) Kemendag, Keterangan tidak halal & pemisahan produk non-halal, Karantina hewan (produk hewan) | Surat Keterangan Asal (SKA/CoO) untuk tarif preferensi |
| Unggas impor (halal) | PSAH | 1 | NIB sebagai Angka Pengenal Importir (API-U), Cek HS dan lartas di INSW, PIB (BC 2.0), pembayaran BM/PDRI dan SPPB, NKV unit usaha produk hewan (cold storage/meat shop), Persetujuan negara & unit usaha asal (establishment), Rekomendasi Pemasukan Produk Hewan (RP), Persetujuan Impor (PI) Kemendag, Registrasi Sertifikat Halal Luar Negeri (SHLN), Karantina hewan (produk hewan) | Surat Keterangan Asal (SKA/CoO) untuk tarif preferensi |
| Ikan & seafood impor | PSAI | 41 | NIB sebagai Angka Pengenal Importir (API-U), Cek HS dan lartas di INSW, PIB (BC 2.0), pembayaran BM/PDRI dan SPPB, Rekomendasi Pemasukan Hasil Perikanan, Persetujuan Impor (PI) Kemendag, Karantina ikan | Surat Keterangan Asal (SKA/CoO) untuk tarif preferensi |
| Olahan daging impor (halal) | BPOM ML | 17 | NIB sebagai Angka Pengenal Importir (API-U), Cek HS dan lartas di INSW, PIB (BC 2.0), pembayaran BM/PDRI dan SPPB, Persetujuan negara & unit usaha asal (establishment), Rekomendasi Pemasukan Produk Hewan (RP), Persetujuan Impor (PI) Kemendag, Izin edar pangan olahan ML (BPOM), Registrasi Sertifikat Halal Luar Negeri (SHLN), SKI BPOM (border/post-border) per pengapalan, Pelabelan Bahasa Indonesia sebelum edar, Karantina hewan (produk hewan) | Surat Keterangan Asal (SKA/CoO) untuk tarif preferensi |
| Olahan daging babi impor (non-halal) | BPOM ML | 0 | NIB sebagai Angka Pengenal Importir (API-U), Cek HS dan lartas di INSW, PIB (BC 2.0), pembayaran BM/PDRI dan SPPB, Persetujuan negara & unit usaha asal (establishment), Rekomendasi Pemasukan Produk Hewan (RP), Persetujuan Impor (PI) Kemendag, Izin edar pangan olahan ML (BPOM), Keterangan tidak halal & pemisahan produk non-halal, SKI BPOM (border/post-border) per pengapalan, Pelabelan Bahasa Indonesia sebelum edar, Karantina hewan (produk hewan) | Surat Keterangan Asal (SKA/CoO) untuk tarif preferensi |
| Olahan ikan/seafood impor | BPOM ML | 18 | NIB sebagai Angka Pengenal Importir (API-U), Cek HS dan lartas di INSW, PIB (BC 2.0), pembayaran BM/PDRI dan SPPB, Izin edar pangan olahan ML (BPOM), Registrasi Sertifikat Halal Luar Negeri (SHLN), SKI BPOM (border/post-border) per pengapalan, Pelabelan Bahasa Indonesia sebelum edar, Karantina ikan | Surat Keterangan Asal (SKA/CoO) untuk tarif preferensi |
| Susu & olahan susu impor | BPOM ML | 59 | NIB sebagai Angka Pengenal Importir (API-U), Cek HS dan lartas di INSW, PIB (BC 2.0), pembayaran BM/PDRI dan SPPB, Izin edar pangan olahan ML (BPOM), Registrasi Sertifikat Halal Luar Negeri (SHLN), SKI BPOM (border/post-border) per pengapalan, Pelabelan Bahasa Indonesia sebelum edar, Karantina hewan (produk hewan) | Surat Keterangan Asal (SKA/CoO) untuk tarif preferensi |
| Sayur & buah beku impor | PSAT | 60 | NIB sebagai Angka Pengenal Importir (API-U), Cek HS dan lartas di INSW, PIB (BC 2.0), pembayaran BM/PDRI dan SPPB, Registrasi PSAT impor (pangan segar asal tumbuhan), Rekomendasi Impor Produk Hortikultura (RIPH), Karantina tumbuhan | Surat Keterangan Asal (SKA/CoO) untuk tarif preferensi |
| Pangan olahan impor (halal) | BPOM ML | 474 | NIB sebagai Angka Pengenal Importir (API-U), Cek HS dan lartas di INSW, PIB (BC 2.0), pembayaran BM/PDRI dan SPPB, Izin edar pangan olahan ML (BPOM), Registrasi Sertifikat Halal Luar Negeri (SHLN), SKI BPOM (border/post-border) per pengapalan, Pelabelan Bahasa Indonesia sebelum edar | Surat Keterangan Asal (SKA/CoO) untuk tarif preferensi |
| Pangan olahan impor (non-halal) | BPOM ML | 0 | NIB sebagai Angka Pengenal Importir (API-U), Cek HS dan lartas di INSW, PIB (BC 2.0), pembayaran BM/PDRI dan SPPB, Izin edar pangan olahan ML (BPOM), Keterangan tidak halal & pemisahan produk non-halal, SKI BPOM (border/post-border) per pengapalan, Pelabelan Bahasa Indonesia sebelum edar | Surat Keterangan Asal (SKA/CoO) untuk tarif preferensi |
| Kemasan & non-pangan impor | Non-pangan | 5 | NIB sebagai Angka Pengenal Importir (API-U), Cek HS dan lartas di INSW, PIB (BC 2.0), pembayaran BM/PDRI dan SPPB | Surat Keterangan Asal (SKA/CoO) untuk tarif preferensi |
| Daging & unggas lokal (PSAH) | PSAH | 447 | Verifikasi legalitas produk & pemasok lokal, NKV unit usaha produk hewan (cold storage/meat shop) | Sertifikat halal Indonesia (produk dipotong/dikemas ulang) |
| Ikan & seafood lokal (PSAI) | PSAI | 41 | Verifikasi legalitas produk & pemasok lokal | – |
| Sayur & buah lokal (PSAT) | PSAT | 0 | Verifikasi legalitas produk & pemasok lokal | Registrasi PSAT impor (pangan segar asal tumbuhan) |
| Pangan olahan dalam negeri (BPOM MD) | BPOM MD | 333 | Izin edar pangan olahan MD (produksi dalam negeri), Verifikasi legalitas produk & pemasok lokal | Sertifikat halal Indonesia (produk dipotong/dikemas ulang) |
| Kemasan & non-pangan lokal | Non-pangan | 39 |  | Verifikasi legalitas produk & pemasok lokal |

Item code dipetakan ke template oleh *aturan pemetaan* (urutan pertama yang cocok dipakai) berdasarkan negara asal,
grup, subgrup, awalan HS, kata di nama barang dan status halal. Template bisa dipilih manual per item code; pilihan
manual tidak ditimpa aturan.

## 5. Langkah per jenis izin

### NIB sebagai Angka Pengenal Importir (API-U)

- **Instansi:** Kementerian Investasi/BKPM · **Sistem:** OSS RBA · **Cakupan:** per perusahaan
- **Penanggung jawab:** Bagian Perizinan (Kementan, KKP, Barantin) · **Perkiraan waktu:** 7 hari
- **Dasar hukum:** PP 28/2025 tentang Penyelenggaraan Perizinan Berusaha Berbasis Risiko; UU 6/2023 tentang Penetapan Perppu 2/2022 tentang Cipta Kerja menjadi Undang-Undang; Permendag 16/2025 tentang Kebijakan dan Pengaturan Impor
- Syarat dasar semua impor. NIB juga menjadi akses kepabeanan (registrasi kepabeanan otomatis).
- Kapan diperlukan: sekali untuk perusahaan, sebelum impor pertama, dan setiap kali data usaha berubah.
- Hasil: NIB yang berlaku sebagai Angka Pengenal Importir Umum (API-U) dan akses kepabeanan.
- Perhatian: KBLI, alamat gudang dan penanggung jawab harus sama di OSS, INSW dan CEISA; perbedaan data membuat pengajuan rekomendasi, PI dan PIB ditolak.

| # | Aktivitas | Bagian | Hari | Dokumen & kriteria verifikasi | Referensi |
|---|---|---|---|---|---|
| 1 | Periksa KBLI perdagangan besar/impor pangan aktif di NIB — Cocokkan KBLI dengan komoditas: daging, ikan, pangan olahan, susu, sayur beku. Unduh NIB terbaru dari OSS dan bandingkan KBLI dengan kelompok barang yang diimpor. | Bagian Perizinan (Kementan, KKP, Barantin) | 1 | **Cetak NIB**: File terbaca jelas dan lengkap semua halaman; Nama perusahaan, produk/item code sesuai pengurusan | PP 28/2025, UU 6/2023, Permendag 16/2025 |
| 2 | Perbarui data NIB/API-U dan hak akses kepabeanan di OSS — Pastikan alamat gudang, penanggung jawab dan NPWP sama dengan data INSW/CEISA. Ubah data di OSS bila ada perbedaan; tunggu sinkronisasi ke INSW/CEISA sebelum pengajuan berikutnya. | Bagian Perizinan (Kementan, KKP, Barantin) | 3 | – | PP 28/2025, UU 6/2023, Permendag 16/2025 |
| 3 | Simpan NIB ke register izin — Isi nomor NIB, tanggal terbit dan unggah PDF NIB ke register izin agar dipakai semua pengapalan. | Bagian Perizinan (Kementan, KKP, Barantin) | 1 | **NIB/API**: Nomor dan tanggal terbit terbaca; Item/HS, volume dan negara asal sesuai rencana impor | PP 28/2025, UU 6/2023, Permendag 16/2025 |

### NKV unit usaha produk hewan (cold storage/meat shop)

- **Instansi:** Dinas Provinsi bidang Kesmavet · **Sistem:** OSS / Dinas Provinsi · **Cakupan:** per perusahaan
- **Penanggung jawab:** Bagian Perizinan (Kementan, KKP, Barantin) · **Perkiraan waktu:** 30 hari · **Masa berlaku:** 60 bulan
- **Dasar hukum:** Permentan 11/2020 tentang Sertifikasi Nomor Kontrol Veteriner Unit Usaha Produk Hewan; PP 95/2012 tentang Kesehatan Masyarakat Veteriner dan Kesejahteraan Hewan; UU 18/2009 jo. UU 41/2014 tentang Peternakan dan Kesehatan Hewan
- Sertifikat higiene-sanitasi gudang/unit usaha produk hewan; dilampirkan saat mengajukan Rekomendasi Pemasukan.
- Kapan diperlukan: sebelum mengajukan Rekomendasi Pemasukan produk hewan, untuk setiap gudang/unit usaha yang menyimpan atau menangani daging, unggas dan jeroan.
- Hasil: sertifikat Nomor Kontrol Veteriner dengan level tertentu, diperiksa ulang lewat surveilans berkala.
- Perhatian: perubahan alamat, tata letak atau fungsi gudang perlu dilaporkan karena memengaruhi NKV.

| # | Aktivitas | Bagian | Hari | Dokumen & kriteria verifikasi | Referensi |
|---|---|---|---|---|---|
| 1 | Siapkan dokumen higiene-sanitasi, SOP rantai dingin dan denah gudang — Kumpulkan denah gudang, SOP rantai dingin (suhu, pencatatan, kalibrasi), program sanitasi dan pengendalian hama, serta daftar alat. Unggah sebagai satu dokumen dengan beberapa file. | Bagian Perizinan (Kementan, KKP, Barantin) | 7 | – | Permentan 11/2020, PP 95/2012, UU 18/2009 jo. UU 41/2014 |
| 2 | Ajukan sertifikasi NKV dan jadwalkan audit dinas — Ajukan lewat OSS/dinas provinsi, unggah bukti pengajuan, dan catat jadwal audit di aktivitas ini. | Bagian Perizinan (Kementan, KKP, Barantin) | 14 | – | Permentan 11/2020, PP 95/2012, UU 18/2009 jo. UU 41/2014 |
| 3 | Tindak lanjuti temuan audit — Catat setiap temuan auditor, tetapkan penanggung jawab dan tenggat perbaikan, lalu kirim bukti perbaikan ke dinas. | Bagian Perizinan (Kementan, KKP, Barantin) | 7 | – | Permentan 11/2020, PP 95/2012, UU 18/2009 jo. UU 41/2014 |
| 4 | Simpan sertifikat NKV dan jadwalkan surveilans — Isi nomor dan level NKV, tanggal terbit dan masa berlaku di register; catat jadwal surveilans berikutnya. | Bagian Perizinan (Kementan, KKP, Barantin) | 1 | **Sertifikat NKV** (cek masa berlaku): Nomor dan tanggal terbit terbaca; Item/HS, volume dan negara asal sesuai rencana impor; Masa berlaku mencakup ETA pengapalan | Permentan 11/2020, PP 95/2012, UU 18/2009 jo. UU 41/2014 |

### Persetujuan negara & unit usaha asal (establishment)

- **Instansi:** Kementan – Ditjen PKH · **Sistem:** SIMREK Ditjen PKH · **Cakupan:** per pemasok/unit usaha asal
- **Penanggung jawab:** Bagian Perizinan (Kementan, KKP, Barantin) · **Perkiraan waktu:** 5 hari · **Masa berlaku:** 12 bulan
- **Dasar hukum:** Permentan 42/2019 tentang Pemasukan Karkas, Daging, Jeroan, dan/atau Olahannya ke dalam Wilayah Negara Republik Indonesia; Permentan 19/2025 tentang Persyaratan Pemasukan Produk Hewan dalam Hal Tertentu yang Berasal dari Negara atau Zona dalam Suatu Negara Asal Pemasukan; PP 95/2012 tentang Kesehatan Masyarakat Veteriner dan Kesejahteraan Hewan; UU 18/2009 jo. UU 41/2014 tentang Peternakan dan Kesehatan Hewan
- Produk hewan hanya boleh dimasukkan dari negara/zona dan unit usaha (RPH, pabrik) yang sudah disetujui Kementan, termasuk penyembelihan halal untuk produk halal.
- Kapan diperlukan: untuk setiap pemasok/unit usaha asal produk hewan (RPH, pabrik pengolahan, cold storage) sebelum PO pertama.
- Hasil: bukti bahwa negara/zona dan unit usaha asal sudah disetujui Kementan; dipakai ulang untuk semua pengapalan dari unit usaha yang sama.
- Perhatian: jangan menerbitkan PO ke unit usaha yang belum disetujui; prosesnya bisa memakan waktu lama.

| # | Aktivitas | Bagian | Hari | Dokumen & kriteria verifikasi | Referensi |
|---|---|---|---|---|---|
| 1 | Minta nomor establishment, alamat RPH/pabrik dan sertifikat halal penyembelihan — Dari eksportir/prinsipal. Purchasing meminta nomor establishment, nama dan alamat RPH/pabrik, serta sertifikat halal penyembelihan dari prinsipal. Pastikan nomor establishment sama dengan yang tercetak di health certificate. | Purchasing (Procurement) | 3 | **Data establishment**: Nomor establishment dan alamat RPH/pabrik; Bukti penyembelihan halal (untuk produk halal) | Permentan 42/2019, Permentan 19/2025, PP 95/2012, UU 18/2009 jo. UU 41/2014 |
| 2 | Cek negara/zona dan unit usaha ada di daftar yang disetujui Kementan — Daftar unit usaha di SIMREK/Ditjen PKH. Bagian Perizinan mencari negara, zona dan nomor establishment di daftar unit usaha yang disetujui. Unggah tangkapan layar atau cetakan hasil pencarian. | Bagian Perizinan (Kementan, KKP, Barantin) | 2 | – | Permentan 19/2025, Permentan 42/2019 |
| 3 | Bila belum disetujui: minta prinsipal mengajukan penilaian unit usaha lewat otoritas veteriner negara asal — Perizinan menyiapkan daftar persyaratan; Purchasing yang menghubungi prinsipal. Bila belum terdaftar, Perizinan menyiapkan daftar persyaratan dan Purchasing meneruskannya ke prinsipal. Prinsipal mengajukan lewat otoritas veteriner negaranya. | Purchasing (Procurement) | 3 | – | Permentan 42/2019, Permentan 19/2025, PP 95/2012, UU 18/2009 jo. UU 41/2014 |
| 4 | Pantau penilaian unit usaha di Kementan — Proses audit bisa berbulan-bulan; tandai pemasok belum bisa dipakai. Catat perkembangan penilaian di catatan aktivitas. Selama belum disetujui, pemasok ditandai belum bisa dipakai untuk produk hewan. | Bagian Perizinan (Kementan, KKP, Barantin) | 60 | – | Permentan 42/2019, Permentan 19/2025, PP 95/2012, UU 18/2009 jo. UU 41/2014 |
| 5 | Simpan bukti persetujuan unit usaha — Unggah surat/daftar persetujuan dan isi masa berlaku di register izin pemasok. | Bagian Perizinan (Kementan, KKP, Barantin) | 1 | **Bukti approval establishment**: Nomor dan tanggal terbit terbaca; Item/HS, volume dan negara asal sesuai rencana impor | Permentan 42/2019, Permentan 19/2025, PP 95/2012, UU 18/2009 jo. UU 41/2014 |

### Rekomendasi Pemasukan Produk Hewan (RP)

- **Instansi:** Kementan – Ditjen PKH · **Sistem:** SIMREK / SINSW · **Cakupan:** per item code
- **Penanggung jawab:** Bagian Perizinan (Kementan, KKP, Barantin) · **Perkiraan waktu:** 14 hari · **Masa berlaku:** 12 bulan
- **Dasar hukum:** Permentan 42/2019 tentang Pemasukan Karkas, Daging, Jeroan, dan/atau Olahannya ke dalam Wilayah Negara Republik Indonesia; Perpres 32/2022 tentang Neraca Komoditas; PP 95/2012 tentang Kesehatan Masyarakat Veteriner dan Kesejahteraan Hewan; UU 18/2009 jo. UU 41/2014 tentang Peternakan dan Kesehatan Hewan
- Rekomendasi teknis sebelum Persetujuan Impor untuk karkas, daging, jeroan, unggas dan olahannya. Berlaku untuk jenis, HS, negara, unit usaha dan volume yang disebut.
- Kapan diperlukan: setiap rencana impor karkas, daging, jeroan, unggas dan olahannya (PSAH dan daging olahan), sebelum mengajukan Persetujuan Impor.
- Hasil: Rekomendasi Pemasukan yang menyebut jenis produk, HS, negara, unit usaha asal, volume dan masa berlaku.
- Perhatian: impor hanya boleh sesuai isi rekomendasi; produk, HS atau unit usaha yang berbeda memerlukan rekomendasi baru.

| # | Aktivitas | Bagian | Hari | Dokumen & kriteria verifikasi | Referensi |
|---|---|---|---|---|---|
| 1 | Susun rencana impor: jenis, HS 8 digit, volume, negara, unit usaha, pelabuhan — Purchasing menyusun rencana impor per item: jenis produk (karkas/daging/jeroan/olahan), HS 8 digit, volume, negara, nomor establishment dan pelabuhan tujuan. | Purchasing (Procurement) | 3 | **Rencana impor**: Jenis, HS 8 digit, volume dan negara asal lengkap; Sesuai alokasi Neraca Komoditas | Perpres 32/2022, Permentan 42/2019 |
| 2 | Lengkapi dokumen: NIB, NKV gudang, kapasitas cold storage, kontrak/LoI, sertifikat halal unit usaha — Bagian Perizinan memeriksa NIB, NKV, kapasitas cold storage, kontrak/LoI dan sertifikat halal unit usaha sudah lengkap dan masih berlaku. | Bagian Perizinan (Kementan, KKP, Barantin) | 3 | – | Permentan 42/2019, Permentan 11/2020 |
| 3 | Ajukan RP di SIMREK/SINSW — Ajukan permohonan di SIMREK/SINSW sesuai rencana impor dan unggah bukti pengajuan. | Bagian Perizinan (Kementan, KKP, Barantin) | 1 | **Bukti pengajuan**: Nomor transaksi/aju terbaca; Nilai dan tanggal sesuai | Permentan 42/2019, Perpres 32/2022, PP 95/2012, UU 18/2009 jo. UU 41/2014 |
| 4 | Pantau verifikasi dan jawab koreksi — Pantau status setiap hari. Bila diminta koreksi, perbaiki data atau minta dokumen tambahan ke prinsipal lewat memo ke Purchasing. | Bagian Perizinan (Kementan, KKP, Barantin) | 7 | – | Permentan 42/2019, Perpres 32/2022, PP 95/2012, UU 18/2009 jo. UU 41/2014 |
| 5 | Unduh RP terbit, catat volume dan masa berlaku — Unggah rekomendasi yang terbit, lalu isi nomor, volume dan masa berlakunya. Rekomendasi otomatis menutup kebutuhan izin item yang disebut. | Bagian Perizinan (Kementan, KKP, Barantin) | 1 | **RP Kementan** (cek masa berlaku): Nomor dan tanggal terbit terbaca; Item/HS, volume dan negara asal sesuai rencana impor; Masa berlaku mencakup ETA pengapalan | Permentan 42/2019, Perpres 32/2022, PP 95/2012, UU 18/2009 jo. UU 41/2014 |

### Rekomendasi Pemasukan Hasil Perikanan

- **Instansi:** KKP – Ditjen PDSPKP · **Sistem:** SINSW / sistem KKP · **Cakupan:** per item code
- **Penanggung jawab:** Bagian Perizinan (Kementan, KKP, Barantin) · **Perkiraan waktu:** 14 hari · **Masa berlaku:** 12 bulan
- **Dasar hukum:** Permen KP 58/2018 tentang Rekomendasi Pemasukan Komoditas Perikanan Selain Ikan Hidup; Permendag 19/2025 tentang Kebijakan dan Pengaturan Impor Garam dan Komoditas Perikanan; Perpres 32/2022 tentang Neraca Komoditas; UU 31/2004 jo. UU 45/2009 tentang Perikanan
- Rekomendasi teknis sebelum PI untuk ikan dan hasil perikanan. Peruntukan (hotel, restoran, katering, ritel modern, bahan baku) harus sesuai.
- Kapan diperlukan: setiap rencana impor ikan, krustasea dan moluska (PSAI), sebelum Persetujuan Impor.
- Hasil: rekomendasi pemasukan hasil perikanan sesuai jenis, volume, negara dan peruntukan.
- Perhatian: barang hanya boleh dijual ke peruntukan yang disebut dalam rekomendasi (mis. hotel, restoran, katering, ritel modern atau bahan baku industri).

| # | Aktivitas | Bagian | Hari | Dokumen & kriteria verifikasi | Referensi |
|---|---|---|---|---|---|
| 1 | Susun rencana impor ikan: jenis, HS, volume, negara, peruntukan — Purchasing menyusun rencana impor per jenis ikan/krustasea/moluska: HS, volume, negara asal dan peruntukan penjualan. | Purchasing (Procurement) | 3 | **Rencana impor**: Jenis, HS 8 digit, volume dan negara asal lengkap; Sesuai alokasi Neraca Komoditas | Permen KP 58/2018, Permendag 19/2025, Perpres 32/2022, UU 31/2004 jo. UU 45/2009 |
| 2 | Lengkapi dokumen: NIB, kapasitas cold storage, kontrak, contoh health certificate — Bagian Perizinan memeriksa NIB, kapasitas cold storage, kontrak dan contoh health certificate dari otoritas negara asal. | Bagian Perizinan (Kementan, KKP, Barantin) | 3 | – | Permen KP 58/2018, Permendag 19/2025, Perpres 32/2022, UU 31/2004 jo. UU 45/2009 |
| 3 | Ajukan rekomendasi pemasukan hasil perikanan — Ajukan rekomendasi di sistem KKP/SINSW dan unggah bukti pengajuan. | Bagian Perizinan (Kementan, KKP, Barantin) | 1 | – | Permen KP 58/2018, Permendag 19/2025, Perpres 32/2022, UU 31/2004 jo. UU 45/2009 |
| 4 | Pantau verifikasi dan jawab koreksi — Pantau verifikasi dan jawab koreksi. Data dari prinsipal diminta lewat memo ke Purchasing. | Bagian Perizinan (Kementan, KKP, Barantin) | 7 | – | Permen KP 58/2018, Permendag 19/2025, Perpres 32/2022, UU 31/2004 jo. UU 45/2009 |
| 5 | Unduh rekomendasi terbit, catat volume dan masa berlaku — Unggah rekomendasi yang terbit, lalu catat volume, peruntukan dan masa berlakunya di register. | Bagian Perizinan (Kementan, KKP, Barantin) | 1 | **Rekomendasi KKP** (cek masa berlaku): Nomor dan tanggal terbit terbaca; Item/HS, volume dan negara asal sesuai rencana impor; Masa berlaku mencakup ETA pengapalan | Permen KP 58/2018, Permendag 19/2025, Perpres 32/2022, UU 31/2004 jo. UU 45/2009 |

### Rekomendasi Impor Produk Hortikultura (RIPH)

- **Instansi:** Kementan – Ditjen Hortikultura · **Sistem:** SIMPEL/SINSW · **Cakupan:** per item code
- **Penanggung jawab:** Bagian Perizinan (Kementan, KKP, Barantin) · **Perkiraan waktu:** 14 hari · **Masa berlaku:** 12 bulan
- **Dasar hukum:** Permentan 39/2019 tentang Rekomendasi Impor Produk Hortikultura; Permendag 18/2025 tentang Kebijakan dan Pengaturan Impor Barang Pertanian dan Peternakan; UU 13/2010 tentang Hortikultura
- Untuk sayur/buah segar atau beku yang termasuk lartas. Cek HS di INSW dulu; bila tidak wajib, tandai selesai dengan catatan.
- Kapan diperlukan: untuk sayur/buah segar atau beku yang HS-nya terkena lartas hortikultura.
- Hasil: RIPH sebagai dasar Persetujuan Impor; bila HS tidak wajib, cukup catatan hasil cek INSW.
- Perhatian: periksa lartas setiap kali HS atau jenis produk berubah.

| # | Aktivitas | Bagian | Hari | Dokumen & kriteria verifikasi | Referensi |
|---|---|---|---|---|---|
| 1 | Cek HS di INSW apakah wajib RIPH — Bagian Impor mencari HS 8 digit di INSW dan mengunggah hasilnya. Bila tidak wajib RIPH, tandai aktivitas berikutnya selesai dengan catatan. | Bagian Impor & Kepabeanan | 1 | **Hasil cek INSW**: Semua HS item sudah dicek; Daftar lartas border/post-border tercatat | Permentan 39/2019, Permendag 18/2025, UU 13/2010 |
| 2 | Lengkapi dokumen RIPH — Lengkapi dokumen yang diminta: NIB, data gudang, rencana impor dan dokumen produk dari prinsipal. | Bagian Perizinan (Kementan, KKP, Barantin) | 3 | – | Permentan 39/2019, Permendag 18/2025, UU 13/2010 |
| 3 | Ajukan RIPH — Ajukan RIPH di sistem Kementan/SINSW dan unggah bukti pengajuan. | Bagian Perizinan (Kementan, KKP, Barantin) | 1 | – | Permentan 39/2019, Permendag 18/2025, UU 13/2010 |
| 4 | Pantau dan unduh RIPH terbit — Pantau sampai terbit, lalu unggah RIPH dan catat volume serta masa berlakunya. | Bagian Perizinan (Kementan, KKP, Barantin) | 7 | **RIPH** (cek masa berlaku): Nomor dan tanggal terbit terbaca; Item/HS, volume dan negara asal sesuai rencana impor; Masa berlaku mencakup ETA pengapalan | Permentan 39/2019, Permendag 18/2025, UU 13/2010 |

### Registrasi PSAT impor (pangan segar asal tumbuhan)

- **Instansi:** Badan Pangan Nasional · **Sistem:** e-PSAT · **Cakupan:** per item code
- **Penanggung jawab:** Bagian Makanan Luar (Izin Edar ML BPOM) · **Perkiraan waktu:** 21 hari · **Masa berlaku:** 60 bulan
- **Dasar hukum:** Peraturan Badan Pangan Nasional tentang Pendaftaran Pangan Segar Asal Tumbuhan; PP 86/2019 tentang Keamanan Pangan; UU 18/2012 tentang Pangan
- Izin edar untuk sayur/buah segar atau beku tanpa pengolahan lanjut.
- Kapan diperlukan: sebelum mengedarkan pangan segar asal tumbuhan (sayur/buah segar atau beku tanpa pengolahan lanjut).
- Hasil: nomor registrasi PSAT yang wajib dicantumkan pada label.
- Perhatian: produk yang sudah diolah (dimasak, diberi bumbu) masuk BPOM ML, bukan PSAT.

| # | Aktivitas | Bagian | Hari | Dokumen & kriteria verifikasi | Referensi |
|---|---|---|---|---|---|
| 1 | Kumpulkan spesifikasi, CoA dan dokumen produsen — Purchasing meminta spesifikasi produk, CoA (residu pestisida, cemaran), dokumen produsen dan foto label asli. | Purchasing (Procurement) | 5 | – | Peraturan Badan Pangan Nasional, PP 86/2019, UU 18/2012 |
| 2 | Ajukan registrasi PSAT — Bagian Makanan Luar mengajukan registrasi di sistem PSAT dan mengunggah bukti pengajuan. | Bagian Makanan Luar (Izin Edar ML BPOM) | 2 | – | Peraturan Badan Pangan Nasional, PP 86/2019, UU 18/2012 |
| 3 | Pantau evaluasi dan jawab koreksi — Tanggapi permintaan data tambahan dari evaluator; data dari prinsipal diminta lewat Purchasing. | Bagian Makanan Luar (Izin Edar ML BPOM) | 12 | – | Peraturan Badan Pangan Nasional, PP 86/2019, UU 18/2012 |
| 4 | Catat nomor registrasi dan label — Catat nomor registrasi di register izin dan pastikan nomor tercantum di rancangan label. | Bagian Makanan Luar (Izin Edar ML BPOM) | 2 | **Nomor PSAT** (cek masa berlaku): Nomor dan tanggal terbit terbaca; Item/HS, volume dan negara asal sesuai rencana impor; Masa berlaku mencakup ETA pengapalan | Peraturan Badan Pangan Nasional, PP 86/2019, UU 18/2012 |

### Persetujuan Impor (PI) Kemendag

- **Instansi:** Kemendag – Ditjen Perdagangan Luar Negeri · **Sistem:** INATRADE / SINSW · **Cakupan:** per item code
- **Penanggung jawab:** Bagian Impor & Kepabeanan · **Perkiraan waktu:** 14 hari · **Masa berlaku:** 12 bulan
- **Dasar hukum:** Permendag 16/2025 tentang Kebijakan dan Pengaturan Impor; Permendag 18/2025 tentang Kebijakan dan Pengaturan Impor Barang Pertanian dan Peternakan; Permendag 19/2025 tentang Kebijakan dan Pengaturan Impor Garam dan Komoditas Perikanan; Perpres 32/2022 tentang Neraca Komoditas
- Diterbitkan berdasarkan rekomendasi teknis (RP/KKP/RIPH) dan Neraca Komoditas. Catat volume dan realisasi.
- Kapan diperlukan: setelah rekomendasi teknis (RP Kementan, rekomendasi KKP atau RIPH) terbit, sebelum barang dikapalkan.
- Hasil: Persetujuan Impor dengan volume, HS, negara, pelabuhan dan masa berlaku; realisasi impor wajib dilaporkan.
- Perhatian: volume PI tidak boleh terlampaui; catat realisasi setiap pengapalan.

| # | Aktivitas | Bagian | Hari | Dokumen & kriteria verifikasi | Referensi |
|---|---|---|---|---|---|
| 1 | Pastikan rekomendasi teknis (RP/KKP/RIPH) sudah terbit — Buka tab Kebutuhan izin pada pengapalan dan pastikan rekomendasi teknis tiap item berstatus lengkap. | Bagian Impor & Kepabeanan | 1 | – | Permendag 16/2025, Permendag 18/2025, Permendag 19/2025, Perpres 32/2022 |
| 2 | Ajukan PI di SINSW sesuai Neraca Komoditas — Ajukan PI di SINSW sesuai volume pada rekomendasi dan Neraca Komoditas, lalu unggah bukti pengajuan. | Bagian Impor & Kepabeanan | 1 | **Bukti pengajuan**: Nomor transaksi/aju terbaca; Nilai dan tanggal sesuai | Permendag 16/2025, Perpres 32/2022 |
| 3 | Pantau penerbitan PI — Pantau status penerbitan; tanggapi permintaan perbaikan data. | Bagian Impor & Kepabeanan | 7 | – | Permendag 16/2025, Permendag 18/2025, Permendag 19/2025, Perpres 32/2022 |
| 4 | Catat nomor PI, volume, pelabuhan dan masa berlaku — Unggah PI, isi nomor, volume, pelabuhan dan masa berlaku. PI dipakai untuk PIB dan pengapalan berikutnya selama volume masih tersedia. | Bagian Impor & Kepabeanan | 1 | **PI** (cek masa berlaku): Nomor dan tanggal terbit terbaca; Item/HS, volume dan negara asal sesuai rencana impor; Masa berlaku mencakup ETA pengapalan | Permendag 16/2025, Permendag 18/2025, Permendag 19/2025, Perpres 32/2022 |
| 5 | Bila diwajibkan: atur verifikasi Laporan Surveyor (LS) di pelabuhan muat — Bila PI mewajibkan Laporan Surveyor, Purchasing meminta prinsipal menjadwalkan pemeriksaan surveyor di pelabuhan muat dan mengunggah LS. | Purchasing (Procurement) | 3 | **LS**: Nomor dan tanggal terbit terbaca; Item/HS, volume dan negara asal sesuai rencana impor | Permendag 16/2025 |

### Izin edar pangan olahan ML (BPOM)

- **Instansi:** BPOM · **Sistem:** e-Registration BPOM · **Cakupan:** per item code
- **Penanggung jawab:** Bagian Makanan Luar (Izin Edar ML BPOM) · **Perkiraan waktu:** 60 hari · **Masa berlaku:** 60 bulan
- **Dasar hukum:** Per BPOM 27/2017 tentang Pendaftaran Pangan Olahan; Per BPOM 31/2018 jo. 20/2021 tentang Label Pangan Olahan; PP 86/2019 tentang Keamanan Pangan; UU 18/2012 tentang Pangan
- Nomor ML wajib sebelum pangan olahan impor diedarkan. Berlaku 5 tahun dan dipakai untuk SKI tiap pengapalan.
- Kapan diperlukan: untuk setiap produk pangan olahan impor (termasuk daging olahan, olahan ikan, susu, pasta, makanan beku) sebelum diedarkan.
- Hasil: Nomor Izin Edar ML yang berlaku 5 tahun dan menjadi dasar SKI setiap pengapalan.
- Perhatian: satu NIE berlaku untuk satu produk dengan merek, komposisi, ukuran kemasan dan produsen tertentu; perubahan memerlukan registrasi variasi.

| # | Aktivitas | Bagian | Hari | Dokumen & kriteria verifikasi | Referensi |
|---|---|---|---|---|---|
| 1 | Minta dokumen prinsipal: LoA, Certificate of Free Sale/Health Certificate, GMP/HACCP/ISO 22000, komposisi, spesifikasi, CoA, alur proses, foto label asli — Purchasing meminta semua dokumen prinsipal sekaligus agar evaluasi tidak tertunda. Unggah setiap dokumen sebagai file terpisah dalam satu dokumen. | Purchasing (Procurement) | 14 | **Dokumen prinsipal**: Surat penunjukan (LoA) bertanggal dan ditandatangani prinsipal; Certificate of Free Sale/Health Certificate dari otoritas negara asal; Sertifikat GMP/HACCP/ISO 22000 masih berlaku; Komposisi lengkap 100% dan spesifikasi produk; CoA lot terbaru | Per BPOM 27/2017, Per BPOM 31/2018 jo. 20/2021, PP 86/2019, UU 18/2012 |
| 2 | Tentukan kategori pangan, cek BTP, klaim dan batas cemaran — Bagian Makanan Luar menentukan kategori pangan, memeriksa BTP dan batas cemaran terhadap peraturan BPOM, dan menilai klaim pada label asli. | Bagian Makanan Luar (Izin Edar ML BPOM) | 3 | – | Per BPOM 27/2017, Per BPOM 31/2018 jo. 20/2021, PP 86/2019, UU 18/2012 |
| 3 | Susun rancangan label Bahasa Indonesia (nama, komposisi, berat bersih, importir, negara asal, kedaluwarsa, kode produksi, logo halal/keterangan tidak halal) — Susun rancangan label Bahasa Indonesia lengkap dan unggah file desainnya untuk diverifikasi. | Bagian Makanan Luar (Izin Edar ML BPOM) | 3 | **Rancangan label**: Nama produk, komposisi, berat bersih, negara asal; Nama dan alamat importir (Indoguna); Tanggal kedaluwarsa dan kode produksi; Logo halal Indonesia atau keterangan tidak halal sesuai status produk | Per BPOM 31/2018 jo. 20/2021, PP 42/2024 |
| 4 | Ajukan di e-Registration BPOM dan bayar PNBP — Ajukan registrasi di e-Registration BPOM, bayar PNBP dan unggah bukti bayar. | Bagian Makanan Luar (Izin Edar ML BPOM) | 1 | **Bukti bayar**: Nomor transaksi/aju terbaca; Nilai dan tanggal sesuai | Per BPOM 27/2017, Per BPOM 31/2018 jo. 20/2021, PP 86/2019, UU 18/2012 |
| 5 | Tanggapi tambahan data hasil evaluasi — Data yang harus datang dari prinsipal diminta lewat Purchasing. Pantau hasil evaluasi. Bila evaluator meminta data tambahan dari prinsipal, kirim memo ke Purchasing dari aktivitas ini. | Bagian Makanan Luar (Izin Edar ML BPOM) | 20 | – | Per BPOM 27/2017, Per BPOM 31/2018 jo. 20/2021, PP 86/2019, UU 18/2012 |
| 6 | Unduh NIE ML dan catat masa berlaku — Unggah NIE ML, isi nomor dan masa berlaku di register; NIE dipakai otomatis untuk SKI pengapalan berikutnya. | Bagian Makanan Luar (Izin Edar ML BPOM) | 1 | **NIE ML** (cek masa berlaku): Nomor dan tanggal terbit terbaca; Item/HS, volume dan negara asal sesuai rencana impor; Masa berlaku mencakup ETA pengapalan | Per BPOM 27/2017, Per BPOM 31/2018 jo. 20/2021, PP 86/2019, UU 18/2012 |

### Registrasi Sertifikat Halal Luar Negeri (SHLN)

- **Instansi:** BPJPH · **Sistem:** SIHALAL · **Cakupan:** per item code
- **Penanggung jawab:** Bagian Sertifikasi Halal · **Perkiraan waktu:** 14 hari
- **Dasar hukum:** PP 42/2024 tentang Penyelenggaraan Bidang Jaminan Produk Halal; Keputusan Kepala BPJPH tentang Registrasi Sertifikat Halal Luar Negeri dan Lembaga Halal Luar Negeri yang diakui; UU 33/2014 tentang Jaminan Produk Halal; UU 6/2023 tentang Penetapan Perppu 2/2022 tentang Cipta Kerja menjadi Undang-Undang
- Sertifikat halal produsen luar negeri wajib diregistrasi di BPJPH sebelum produk beredar. Hanya dari Lembaga Halal Luar Negeri (LHLN) yang punya kerja sama saling pengakuan dengan BPJPH. Masa berlaku mengikuti sertifikat asal.
- Kapan diperlukan: untuk produk halal impor (daging, unggas, olahan, pangan olahan berbahan hewani) sebelum beredar di Indonesia.
- Hasil: nomor registrasi Sertifikat Halal Luar Negeri dari BPJPH.
- Perhatian: sertifikat asal harus diterbitkan Lembaga Halal Luar Negeri yang diakui BPJPH dan mencakup produk serta unit usaha yang diimpor.

| # | Aktivitas | Bagian | Hari | Dokumen & kriteria verifikasi | Referensi |
|---|---|---|---|---|---|
| 1 | Minta sertifikat halal produsen beserta daftar produk dan nomor establishment — Purchasing meminta sertifikat halal produsen yang masih berlaku, lengkap dengan daftar produk dan nomor establishment. | Purchasing (Procurement) | 7 | **Sertifikat halal LN** (cek masa berlaku): Diterbitkan Lembaga Halal Luar Negeri yang diakui BPJPH; Nama dan alamat produsen/establishment sesuai; Daftar produk mencakup item code yang diimpor; Masih berlaku saat ETA | PP 42/2024, Keputusan Kepala BPJPH, UU 33/2014, UU 6/2023 |
| 2 | Cek lembaga penerbit termasuk LHLN yang diakui BPJPH — Bagian Halal mencocokkan lembaga penerbit dengan daftar LHLN yang diakui BPJPH, serta nama produsen dan daftar produk dengan item code. | Bagian Sertifikasi Halal | 1 | – | Keputusan Kepala BPJPH, PP 42/2024 |
| 3 | Ajukan registrasi SHLN di SIHALAL dan bayar — Ajukan registrasi di SIHALAL, bayar tarif layanan dan unggah bukti pengajuan. | Bagian Sertifikasi Halal | 1 | **Bukti pengajuan**: Nomor transaksi/aju terbaca; Nilai dan tanggal sesuai | PP 42/2024, Keputusan Kepala BPJPH, UU 33/2014, UU 6/2023 |
| 4 | Pantau verifikasi sampai nomor registrasi terbit — Pantau verifikasi; catat nomor registrasi dan masa berlaku yang mengikuti sertifikat asal. | Bagian Sertifikasi Halal | 10 | **Nomor registrasi SHLN**: Nomor dan tanggal terbit terbaca; Item/HS, volume dan negara asal sesuai rencana impor | PP 42/2024, Keputusan Kepala BPJPH, UU 33/2014, UU 6/2023 |
| 5 | Pastikan label halal Indonesia dan nomor registrasi tercantum di label/stiker — Periksa label/stiker memuat logo halal Indonesia dan nomor registrasi sebelum barang dirilis. | Bagian Sertifikasi Halal | 2 | – | Per BPOM 31/2018 jo. 20/2021, PP 42/2024 |

### Sertifikat halal Indonesia (produk dipotong/dikemas ulang)

- **Instansi:** BPJPH, LPH, Komite Fatwa · **Sistem:** SIHALAL · **Cakupan:** per item code
- **Penanggung jawab:** Bagian Sertifikasi Halal · **Perkiraan waktu:** 30 hari
- **Dasar hukum:** PP 42/2024 tentang Penyelenggaraan Bidang Jaminan Produk Halal; UU 33/2014 tentang Jaminan Produk Halal; UU 6/2023 tentang Penetapan Perppu 2/2022 tentang Cipta Kerja menjadi Undang-Undang
- Untuk produk yang dipotong, diporsi atau dikemas ulang oleh Indoguna dengan merek/label sendiri.
- Kapan diperlukan: bila Indoguna memotong, memorsi atau mengemas ulang produk dengan label sendiri.
- Hasil: sertifikat halal Indonesia untuk produk dan fasilitas Indoguna.
- Perhatian: perubahan bahan, pemasok atau fasilitas harus dilaporkan dan dapat memerlukan audit ulang.

| # | Aktivitas | Bagian | Hari | Dokumen & kriteria verifikasi | Referensi |
|---|---|---|---|---|---|
| 1 | Tetapkan Penyelia Halal dan dokumen Sistem Jaminan Produk Halal (SJPH) — Tunjuk Penyelia Halal bersertifikat dan susun manual Sistem Jaminan Produk Halal (bahan, proses, ketertelusuran, pelatihan, audit internal). | Bagian Sertifikasi Halal | 7 | **Manual SJPH**: File terbaca jelas dan lengkap semua halaman; Nama perusahaan, produk/item code sesuai pengurusan | PP 42/2024, UU 33/2014, UU 6/2023 |
| 2 | Daftar di SIHALAL dan pilih LPH — Daftar di SIHALAL, pilih Lembaga Pemeriksa Halal (LPH) dan unggah bukti pendaftaran. | Bagian Sertifikasi Halal | 2 | – | PP 42/2024, UU 33/2014, UU 6/2023 |
| 3 | Audit LPH di fasilitas — Siapkan fasilitas dan dokumen untuk audit LPH; unggah laporan audit dan tindak lanjutnya. | Bagian Sertifikasi Halal | 14 | **Laporan audit**: File terbaca jelas dan lengkap semua halaman; Nama perusahaan, produk/item code sesuai pengurusan | PP 42/2024, UU 33/2014, UU 6/2023 |
| 4 | Sidang fatwa dan terbit sertifikat halal — Pantau sidang fatwa; unggah sertifikat halal dan isi masa berlakunya di register. | Bagian Sertifikasi Halal | 7 | **Sertifikat halal**: Nomor dan tanggal terbit terbaca; Item/HS, volume dan negara asal sesuai rencana impor | PP 42/2024, UU 33/2014, UU 6/2023 |
| 5 | Pelihara SJPH, laporkan perubahan bahan/fasilitas — Jalankan audit internal berkala dan laporkan perubahan bahan atau fasilitas ke BPJPH. | Bagian Sertifikasi Halal | 0 | – | PP 42/2024, UU 33/2014, UU 6/2023 |

### Keterangan tidak halal & pemisahan produk non-halal

- **Instansi:** BPJPH (pengawasan) · **Sistem:** – · **Cakupan:** per item code
- **Penanggung jawab:** Bagian Sertifikasi Halal · **Perkiraan waktu:** 3 hari
- **Dasar hukum:** UU 33/2014 tentang Jaminan Produk Halal; PP 42/2024 tentang Penyelenggaraan Bidang Jaminan Produk Halal; Per BPOM 31/2018 jo. 20/2021 tentang Label Pangan Olahan
- Untuk daging babi dan olahannya: label 'tidak halal', penyimpanan, alat dan pengiriman terpisah.
- Kapan diperlukan: untuk setiap item babi dan olahannya, serta produk lain yang mengandung bahan tidak halal.
- Hasil: label dengan keterangan tidak halal dan bukti pemisahan penyimpanan, alat dan pengiriman.
- Perhatian: pemisahan harus nyata di gudang, alat potong, kendaraan dan pencatatan stok.

| # | Aktivitas | Bagian | Hari | Dokumen & kriteria verifikasi | Referensi |
|---|---|---|---|---|---|
| 1 | Tandai item sebagai non-halal di master barang — Pastikan item bertanda Non-halal di menu Item code & template izin; perbaiki item master bila belum. | Bagian Sertifikasi Halal | 1 | – | UU 33/2014, PP 42/2024, Per BPOM 31/2018 jo. 20/2021 |
| 2 | Pastikan keterangan tidak halal pada label/stiker — Foto label/stiker yang memuat keterangan tidak halal dan unggah untuk diverifikasi. | Bagian Sertifikasi Halal | 1 | **Foto label**: Stiker terbaca dan menempel rapi; Isi stiker sama dengan rancangan disetujui | UU 33/2014, PP 42/2024, Per BPOM 31/2018 jo. 20/2021 |
| 3 | Verifikasi pemisahan gudang, alat potong dan pengiriman — Isi checklist pemisahan (area gudang, rak, alat potong, kemasan, kendaraan) dan unggah fotonya. | Bagian Sertifikasi Halal | 1 | **Checklist pemisahan**: Area simpan non-halal terpisah dan berlabel; Alat potong/kemas terpisah; Pengiriman tidak dicampur produk halal | UU 33/2014, PP 42/2024, Per BPOM 31/2018 jo. 20/2021 |

### Cek HS dan lartas di INSW

- **Instansi:** LNSW · **Sistem:** INSW · **Cakupan:** per pengapalan
- **Penanggung jawab:** Bagian Impor & Kepabeanan · **Perkiraan waktu:** 1 hari
- **Dasar hukum:** Permendag 16/2025 tentang Kebijakan dan Pengaturan Impor; PMK 26/2022 tentang Penetapan Sistem Klasifikasi Barang dan Pembebanan Tarif Bea Masuk atas Barang Impor (BTKI 2022)
- Memastikan izin yang ditempelkan template sesuai dengan lartas HS terbaru.
- Kapan diperlukan: untuk setiap pengapalan, sebelum mengajukan PI dan PIB.
- Hasil: daftar lartas border dan post-border per HS yang dipakai untuk memastikan template izin sesuai.
- Perhatian: ketentuan lartas dapat berubah; jangan mengandalkan hasil cek pengapalan sebelumnya.

| # | Aktivitas | Bagian | Hari | Dokumen & kriteria verifikasi | Referensi |
|---|---|---|---|---|---|
| 1 | Konfirmasi HS 8 digit tiap item di invoice — Cocokkan HS 8 digit pada invoice dengan HS di item master; catat perbedaan. | Bagian Impor & Kepabeanan | 1 | – | PMK 26/2022 |
| 2 | Cek lartas border/post-border tiap HS di INSW — Cari setiap HS di INSW dan unggah hasilnya. | Bagian Impor & Kepabeanan | 1 | **Hasil cek INSW**: Semua HS item sudah dicek; Daftar lartas border/post-border tercatat | Permendag 16/2025, PMK 26/2022 |
| 3 | Laporkan bila izin di template berbeda dengan INSW — Perbarui template barang di menu Konfigurasi bila perlu. Kirim memo ke manajer bila izin di template tidak sama dengan hasil INSW, agar template diperbarui. | Bagian Impor & Kepabeanan | 0 | – | Permendag 16/2025, PMK 26/2022 |

### SKI BPOM (border/post-border) per pengapalan

- **Instansi:** BPOM · **Sistem:** e-BPOM / SINSW · **Cakupan:** per pengapalan
- **Penanggung jawab:** Bagian Makanan Luar (Izin Edar ML BPOM) · **Perkiraan waktu:** 5 hari
- **Dasar hukum:** Per BPOM 28/2023 tentang Pengawasan Pemasukan Obat dan Makanan ke dalam Wilayah Indonesia; UU 18/2012 tentang Pangan
- Surat Keterangan Impor untuk setiap pengapalan pangan olahan ber-NIE ML.
- Kapan diperlukan: setiap pengapalan pangan olahan yang memiliki NIE ML.
- Hasil: Surat Keterangan Impor yang dicantumkan pada PIB.
- Perhatian: SKI diajukan per NIE dan per pengapalan; data lot dan jumlah harus sesuai invoice.

| # | Aktivitas | Bagian | Hari | Dokumen & kriteria verifikasi | Referensi |
|---|---|---|---|---|---|
| 1 | Terima invoice, packing list, CoA per lot dan health certificate — Purchasing meneruskan invoice, packing list, CoA per lot dan health certificate dari prinsipal begitu diterima. | Purchasing (Procurement) | 1 | – | Per BPOM 28/2023, UU 18/2012 |
| 2 | Ajukan SKI per NIE di e-BPOM/SINSW — Ajukan SKI di e-BPOM/SINSW untuk setiap NIE pada pengapalan dan unggah bukti pengajuan. | Bagian Makanan Luar (Izin Edar ML BPOM) | 1 | **Bukti pengajuan**: Nomor transaksi/aju terbaca; Nilai dan tanggal sesuai | Per BPOM 28/2023, UU 18/2012 |
| 3 | Pantau persetujuan SKI — Pantau persetujuan; tanggapi permintaan data tambahan. | Bagian Makanan Luar (Izin Edar ML BPOM) | 2 | – | Per BPOM 28/2023, UU 18/2012 |
| 4 | Kirim nomor SKI ke bagian impor untuk PIB — Unggah SKI dan kirim nomornya ke bagian Impor lewat ruang diskusi pengapalan. | Bagian Makanan Luar (Izin Edar ML BPOM) | 1 | **SKI**: Nomor dan tanggal terbit terbaca; Item/HS, volume dan negara asal sesuai rencana impor | Per BPOM 28/2023, UU 18/2012 |

### Pelabelan Bahasa Indonesia sebelum edar

- **Instansi:** BPOM (pengawasan) · **Sistem:** – · **Cakupan:** per pengapalan
- **Penanggung jawab:** Bagian Makanan Luar (Izin Edar ML BPOM) · **Perkiraan waktu:** 3 hari
- **Dasar hukum:** Per BPOM 31/2018 jo. 20/2021 tentang Label Pangan Olahan; PP 86/2019 tentang Keamanan Pangan; UU 18/2012 tentang Pangan
- Stiker label sesuai rancangan yang disetujui saat registrasi.
- Kapan diperlukan: setiap pengapalan pangan olahan atau PSAT, sebelum barang dijual.
- Hasil: stiker label Bahasa Indonesia terpasang sesuai rancangan yang disetujui.
- Perhatian: isi stiker (nama, komposisi, NIE, importir, halal/tidak halal) harus sama persis dengan rancangan.

| # | Aktivitas | Bagian | Hari | Dokumen & kriteria verifikasi | Referensi |
|---|---|---|---|---|---|
| 1 | Cetak stiker label sesuai rancangan yang disetujui — Cetak stiker berdasarkan rancangan label terverifikasi; periksa nomor NIE dan tanggal kedaluwarsa. | Bagian Makanan Luar (Izin Edar ML BPOM) | 2 | – | Per BPOM 31/2018 jo. 20/2021, PP 86/2019, UU 18/2012 |
| 2 | Tempel dan verifikasi sampel sebelum dirilis ke gudang jual — Tempel pada sampel, foto dan unggah sebelum barang dirilis ke gudang jual. | Bagian Makanan Luar (Izin Edar ML BPOM) | 1 | **Foto label**: Stiker terbaca dan menempel rapi; Isi stiker sama dengan rancangan disetujui | Per BPOM 31/2018 jo. 20/2021, PP 86/2019, UU 18/2012 |

### Karantina hewan (produk hewan)

- **Instansi:** Badan Karantina Indonesia (Barantin) · **Sistem:** Best Trust / PTK Online · **Cakupan:** per pengapalan
- **Penanggung jawab:** Bagian Perizinan (Kementan, KKP, Barantin) · **Perkiraan waktu:** 3 hari
- **Dasar hukum:** UU 21/2019 tentang Karantina Hewan, Ikan, dan Tumbuhan; PP 29/2023 tentang Peraturan Pelaksanaan UU 21/2019 tentang Karantina Hewan, Ikan, dan Tumbuhan; Perpres 45/2023 tentang Badan Karantina Indonesia; Permentan 42/2019 tentang Pemasukan Karkas, Daging, Jeroan, dan/atau Olahannya ke dalam Wilayah Negara Republik Indonesia
- Sertifikat kesehatan veteriner negara asal, pemeriksaan dokumen/fisik/lab, sertifikat pelepasan.
- Kapan diperlukan: setiap pengapalan produk hewan.
- Hasil: sertifikat pelepasan karantina yang diperlukan untuk PIB/pengeluaran barang.
- Perhatian: health certificate harus asli, sesuai nomor kontainer/segel, unit usaha dan jumlah barang.

| # | Aktivitas | Bagian | Hari | Dokumen & kriteria verifikasi | Referensi |
|---|---|---|---|---|---|
| 1 | Pastikan veterinary health certificate dan sertifikat halal penyembelihan asli dari negara asal — Purchasing memastikan prinsipal menerbitkan veterinary health certificate dan sertifikat halal penyembelihan, lalu mengunggah salinannya sebelum kapal tiba. | Purchasing (Procurement) | 3 | **Health certificate**: Asli dan ditandatangani otoritas veteriner/kompeten negara asal; Nomor establishment sesuai daftar yang disetujui; Produk, jumlah karton dan berat sesuai packing list; Tanggal produksi/penyembelihan tercantum | UU 21/2019, Permentan 42/2019, PP 42/2024 |
| 2 | Laporkan rencana pemasukan sebelum barang tiba — Bagian Perizinan melaporkan rencana pemasukan ke Barantin sebelum barang tiba dan mencatat nomor permohonan. | Bagian Perizinan (Kementan, KKP, Barantin) | 1 | **Nomor permohonan**: File terbaca jelas dan lengkap semua halaman; Nama perusahaan, produk/item code sesuai pengurusan | UU 21/2019, PP 29/2023, Perpres 45/2023, Permentan 42/2019 |
| 3 | Dampingi pemeriksaan dokumen/fisik/uji lab — Dampingi pemeriksaan dokumen, fisik dan pengambilan sampel; catat hasilnya. | Bagian Perizinan (Kementan, KKP, Barantin) | 2 | – | UU 21/2019, PP 29/2023, Perpres 45/2023, Permentan 42/2019 |
| 4 | Terima sertifikat pelepasan karantina dan kirim ke bagian impor — Unggah sertifikat pelepasan dan kabari bagian Impor lewat ruang diskusi pengapalan. | Bagian Perizinan (Kementan, KKP, Barantin) | 1 | **Sertifikat pelepasan**: Nomor dan tanggal terbit terbaca; Item/HS, volume dan negara asal sesuai rencana impor | UU 21/2019, PP 29/2023, Perpres 45/2023, Permentan 42/2019 |

### Karantina ikan

- **Instansi:** Badan Karantina Indonesia (Barantin) · **Sistem:** Best Trust / PTK Online · **Cakupan:** per pengapalan
- **Penanggung jawab:** Bagian Perizinan (Kementan, KKP, Barantin) · **Perkiraan waktu:** 3 hari
- **Dasar hukum:** UU 21/2019 tentang Karantina Hewan, Ikan, dan Tumbuhan; PP 29/2023 tentang Peraturan Pelaksanaan UU 21/2019 tentang Karantina Hewan, Ikan, dan Tumbuhan; Perpres 45/2023 tentang Badan Karantina Indonesia
- Health certificate ikan dari otoritas negara asal, pemeriksaan dan pelepasan karantina.
- Kapan diperlukan: setiap pengapalan ikan, krustasea dan moluska.
- Hasil: sertifikat pelepasan karantina ikan.
- Perhatian: health certificate harus diterbitkan otoritas kompeten negara asal dan sesuai isi kontainer.

| # | Aktivitas | Bagian | Hari | Dokumen & kriteria verifikasi | Referensi |
|---|---|---|---|---|---|
| 1 | Pastikan health certificate ikan asli dari negara asal — Purchasing memastikan health certificate dari otoritas negara asal sudah terbit dan mengunggah salinannya. | Purchasing (Procurement) | 3 | **Health certificate**: Asli dan ditandatangani otoritas veteriner/kompeten negara asal; Nomor establishment sesuai daftar yang disetujui; Produk, jumlah karton dan berat sesuai packing list; Tanggal produksi/penyembelihan tercantum | UU 21/2019, PP 29/2023, Perpres 45/2023 |
| 2 | Laporkan rencana pemasukan sebelum barang tiba — Laporkan rencana pemasukan ke Barantin sebelum barang tiba. | Bagian Perizinan (Kementan, KKP, Barantin) | 1 | – | UU 21/2019, PP 29/2023, Perpres 45/2023 |
| 3 | Dampingi pemeriksaan dokumen/fisik/uji lab — Dampingi pemeriksaan dan pengambilan sampel; catat hasilnya. | Bagian Perizinan (Kementan, KKP, Barantin) | 2 | – | UU 21/2019, PP 29/2023, Perpres 45/2023 |
| 4 | Terima sertifikat pelepasan karantina dan kirim ke bagian impor — Unggah sertifikat pelepasan dan kabari bagian Impor. | Bagian Perizinan (Kementan, KKP, Barantin) | 1 | **Sertifikat pelepasan**: Nomor dan tanggal terbit terbaca; Item/HS, volume dan negara asal sesuai rencana impor | UU 21/2019, PP 29/2023, Perpres 45/2023 |

### Karantina tumbuhan

- **Instansi:** Badan Karantina Indonesia (Barantin) · **Sistem:** Best Trust / PTK Online · **Cakupan:** per pengapalan
- **Penanggung jawab:** Bagian Perizinan (Kementan, KKP, Barantin) · **Perkiraan waktu:** 3 hari
- **Dasar hukum:** UU 21/2019 tentang Karantina Hewan, Ikan, dan Tumbuhan; PP 29/2023 tentang Peraturan Pelaksanaan UU 21/2019 tentang Karantina Hewan, Ikan, dan Tumbuhan; Perpres 45/2023 tentang Badan Karantina Indonesia
- Phytosanitary certificate negara asal untuk sayur/buah segar atau beku.
- Kapan diperlukan: setiap pengapalan sayur/buah segar atau beku.
- Hasil: sertifikat pelepasan karantina tumbuhan.
- Perhatian: phytosanitary certificate harus sesuai jenis, jumlah dan negara asal pada invoice.

| # | Aktivitas | Bagian | Hari | Dokumen & kriteria verifikasi | Referensi |
|---|---|---|---|---|---|
| 1 | Pastikan phytosanitary certificate asli dari negara asal — Purchasing memastikan phytosanitary certificate asli dari negara asal dan mengunggah salinannya. | Purchasing (Procurement) | 3 | **Phytosanitary**: Diterbitkan NPPO negara asal; Produk dan jumlah sesuai packing list; Bebas OPTK sesuai pernyataan tambahan | UU 21/2019, PP 29/2023, Perpres 45/2023 |
| 2 | Laporkan rencana pemasukan sebelum barang tiba — Laporkan rencana pemasukan ke Barantin sebelum barang tiba. | Bagian Perizinan (Kementan, KKP, Barantin) | 1 | – | UU 21/2019, PP 29/2023, Perpres 45/2023 |
| 3 | Dampingi pemeriksaan dan terima pelepasan karantina — Dampingi pemeriksaan, lalu unggah sertifikat pelepasan dan kabari bagian Impor. | Bagian Perizinan (Kementan, KKP, Barantin) | 2 | **Sertifikat pelepasan**: Nomor dan tanggal terbit terbaca; Item/HS, volume dan negara asal sesuai rencana impor | UU 21/2019, PP 29/2023, Perpres 45/2023 |

### Surat Keterangan Asal (SKA/CoO) untuk tarif preferensi

- **Instansi:** Otoritas negara asal / DJBC · **Sistem:** e-SKA / CEISA · **Cakupan:** per pengapalan
- **Penanggung jawab:** Purchasing (Procurement) · **Perkiraan waktu:** 3 hari
- **Dasar hukum:** PMK Tarif Preferensi FTA tentang Tata cara pengenaan tarif bea masuk dalam rangka perjanjian internasional (AANZFTA, IA-CEPA, IJEPA, ACFTA, AKFTA, RCEP); UU 10/1995 jo. UU 17/2006 tentang Kepabeanan
- Tidak wajib, tetapi tanpa SKA tarif preferensi tidak bisa dipakai.
- Kapan diperlukan: bila ingin memakai tarif bea masuk preferensi perjanjian dagang (mis. IA-CEPA, AANZFTA, ACFTA).
- Hasil: SKA/Certificate of Origin yang dilampirkan pada PIB.
- Perhatian: SKA yang salah format atau terlambat membuat tarif preferensi gugur dan bea masuk dihitung normal.

| # | Aktivitas | Bagian | Hari | Dokumen & kriteria verifikasi | Referensi |
|---|---|---|---|---|---|
| 1 | Minta SKA/CoO ke eksportir sebelum kapal berangkat — Purchasing meminta SKA/CoO sesuai skema perjanjian dagang sebelum kapal berangkat dan mengunggah salinannya. | Purchasing (Procurement) | 3 | **SKA** (cek masa berlaku): Form sesuai perjanjian (mis. AANZFTA Form AANZ); HS dan uraian barang sama dengan invoice; Ditandatangani otoritas penerbit | PMK Tarif Preferensi FTA |
| 2 | Cek kesesuaian SKA dengan invoice dan HS — Bagian Impor mencocokkan HS, uraian barang, jumlah dan nomor invoice pada SKA. | Bagian Impor & Kepabeanan | 1 | – | PMK Tarif Preferensi FTA, UU 10/1995 jo. UU 17/2006 |

### PIB (BC 2.0), pembayaran BM/PDRI dan SPPB

- **Instansi:** DJBC · **Sistem:** CEISA · **Cakupan:** per pengapalan
- **Penanggung jawab:** Bagian Impor & Kepabeanan · **Perkiraan waktu:** 3 hari
- **Dasar hukum:** UU 10/1995 jo. UU 17/2006 tentang Kepabeanan; PMK Ketentuan Kepabeanan di Bidang Impor tentang Ketentuan Kepabeanan di Bidang Impor; Permendag 16/2025 tentang Kebijakan dan Pengaturan Impor
- Dokumen pemberitahuan impor setelah semua lartas terpenuhi. Barang keluar setelah SPPB.
- Kapan diperlukan: setiap pengapalan, setelah semua lartas terpenuhi.
- Hasil: PIB (BC 2.0) dengan bukti bayar dan SPPB untuk mengeluarkan barang dari pelabuhan.
- Perhatian: keterlambatan dokumen memicu biaya penumpukan dan demurrage kontainer reefer.

| # | Aktivitas | Bagian | Hari | Dokumen & kriteria verifikasi | Referensi |
|---|---|---|---|---|---|
| 1 | Pastikan prinsipal mengirim dokumen pengapalan asli (invoice, packing list, B/L-AWB, SKA, health certificate) — Purchasing memastikan prinsipal mengirim dokumen pengapalan asli dan mengunggah salinannya sebelum kapal tiba. | Purchasing (Procurement) | 2 | **Dokumen asli**: Invoice, packing list dan B/L/AWB asli diterima; Nama barang dan HS sama di semua dokumen | UU 10/1995 jo. UU 17/2006, PMK Ketentuan Kepabeanan di Bidang Impor, Permendag 16/2025 |
| 2 | Kumpulkan dokumen PIB: invoice, packing list, B/L-AWB, polis asuransi, SKA, PI, SKI, sertifikat karantina — Bagian Impor mengumpulkan semua dokumen PIB lewat tombol Dokumen pada pengapalan. | Bagian Impor & Kepabeanan | 1 | – | Permendag 16/2025, Per BPOM 28/2023, UU 21/2019 |
| 3 | Hitung dan bayar BM, PPN, PPh 22 lewat billing — Hitung bea masuk dan pajak impor, terbitkan billing, bayar dan unggah bukti bayar. | Bagian Impor & Kepabeanan | 1 | **Bukti bayar**: Nomor transaksi/aju terbaca; Nilai dan tanggal sesuai | PMK Ketentuan Kepabeanan di Bidang Impor, UU 10/1995 jo. UU 17/2006 |
| 4 | Kirim PIB BC 2.0 lewat CEISA/PPJK — Kirim PIB lewat CEISA atau PPJK dan catat nomor aju. | Bagian Impor & Kepabeanan | 1 | **Nomor aju PIB**: File terbaca jelas dan lengkap semua halaman; Nama perusahaan, produk/item code sesuai pengurusan | UU 10/1995 jo. UU 17/2006, PMK Ketentuan Kepabeanan di Bidang Impor, Permendag 16/2025 |
| 5 | Tangani jalur merah/kuning dan SPTNP bila ada — Bila jalur merah/kuning, siapkan dokumen tambahan dan dampingi pemeriksaan fisik. | Bagian Impor & Kepabeanan | 3 | – | UU 10/1995 jo. UU 17/2006, PMK Ketentuan Kepabeanan di Bidang Impor, Permendag 16/2025 |
| 6 | Terima SPPB, keluarkan kontainer reefer ke gudang — Unggah SPPB, atur pengeluaran kontainer ke gudang, lalu tekan Barang keluar pada pengapalan. | Bagian Impor & Kepabeanan | 1 | **SPPB**: Nomor SPPB dan tanggal terbaca; Nomor kontainer sesuai B/L | UU 10/1995 jo. UU 17/2006, PMK Ketentuan Kepabeanan di Bidang Impor, Permendag 16/2025 |

### Izin edar pangan olahan MD (produksi dalam negeri)

- **Instansi:** BPOM · **Sistem:** e-Registration BPOM · **Cakupan:** per item code
- **Penanggung jawab:** Bagian Makanan Luar (Izin Edar ML BPOM) · **Perkiraan waktu:** 45 hari · **Masa berlaku:** 60 bulan
- **Dasar hukum:** Per BPOM 27/2017 tentang Pendaftaran Pangan Olahan; Per BPOM 31/2018 jo. 20/2021 tentang Label Pangan Olahan; PP 86/2019 tentang Keamanan Pangan; UU 18/2012 tentang Pangan
- Untuk pangan olahan produksi dalam negeri. Bila diproduksi/dikemas oleh Indoguna dengan merek sendiri, Indoguna mendaftarkan MD; bila dibeli dari produsen lokal, cukup verifikasi nomor MD pemasok.
- Kapan diperlukan: untuk pangan olahan produksi dalam negeri yang dijual Indoguna.
- Hasil: NIE MD milik Indoguna (bila diproduksi/dikemas sendiri) atau bukti verifikasi NIE MD pemasok.
- Perhatian: produk yang diproduksi pihak lain dengan merek Indoguna tetap memerlukan izin edar yang sesuai.

| # | Aktivitas | Bagian | Hari | Dokumen & kriteria verifikasi | Referensi |
|---|---|---|---|---|---|
| 1 | Tentukan: produksi sendiri (daftar MD) atau produk pemasok (verifikasi MD) — Tentukan apakah produk dibuat/dikemas Indoguna (daftar MD sendiri) atau dibeli jadi dari pemasok (cukup verifikasi nomor MD pemasok di cekbpom). | Bagian Makanan Luar (Izin Edar ML BPOM) | 1 | – | Per BPOM 27/2017, Per BPOM 31/2018 jo. 20/2021, PP 86/2019, UU 18/2012 |
| 2 | Siapkan izin usaha industri, hasil pemeriksaan sarana/CPPOB, komposisi, proses dan rancangan label — Siapkan izin usaha industri, hasil pemeriksaan sarana/CPPOB, komposisi, alur proses dan rancangan label. | Bagian Makanan Luar (Izin Edar ML BPOM) | 10 | **Rancangan label**: Nama produk, komposisi, berat bersih, negara asal; Nama dan alamat importir (Indoguna); Tanggal kedaluwarsa dan kode produksi; Logo halal Indonesia atau keterangan tidak halal sesuai status produk | Per BPOM 27/2017, Per BPOM 31/2018 jo. 20/2021, PP 86/2019, UU 18/2012 |
| 3 | Ajukan MD di e-Registration BPOM dan bayar PNBP — Ajukan di e-Registration BPOM, bayar PNBP dan unggah bukti bayar. | Bagian Makanan Luar (Izin Edar ML BPOM) | 1 | **Bukti bayar**: Nomor transaksi/aju terbaca; Nilai dan tanggal sesuai | Per BPOM 27/2017, Per BPOM 31/2018 jo. 20/2021, PP 86/2019, UU 18/2012 |
| 4 | Tanggapi evaluasi dan unduh NIE MD — Tanggapi evaluasi, lalu unggah NIE MD dan catat masa berlakunya. | Bagian Makanan Luar (Izin Edar ML BPOM) | 25 | **NIE MD** (cek masa berlaku): Nomor dan tanggal terbit terbaca; Item/HS, volume dan negara asal sesuai rencana impor; Masa berlaku mencakup ETA pengapalan | Per BPOM 27/2017, Per BPOM 31/2018 jo. 20/2021, PP 86/2019, UU 18/2012 |

### Verifikasi legalitas produk & pemasok lokal

- **Instansi:** Internal · **Sistem:** Cek BPOM / SIHALAL · **Cakupan:** per item code
- **Penanggung jawab:** Purchasing (Procurement) · **Perkiraan waktu:** 7 hari · **Masa berlaku:** 12 bulan
- **Dasar hukum:** UU 18/2012 tentang Pangan; UU 33/2014 tentang Jaminan Produk Halal; PP 42/2024 tentang Penyelenggaraan Bidang Jaminan Produk Halal
- Untuk item asal Indonesia: izin edar MD/PIRT atau PSAT, sertifikat halal, NKV pemasok produk hewan.
- Kapan diperlukan: untuk setiap pemasok lokal baru dan saat izin pemasok mendekati masa berlaku.
- Hasil: berkas legalitas pemasok lokal (NIB, izin edar, halal, NKV) yang tersimpan dengan masa berlaku.
- Perhatian: verifikasi keaslian di sistem resmi, jangan hanya dari salinan dokumen.

| # | Aktivitas | Bagian | Hari | Dokumen & kriteria verifikasi | Referensi |
|---|---|---|---|---|---|
| 1 | Minta NIB, izin edar MD/PIRT/PSAT, sertifikat halal dan NKV pemasok — Purchasing meminta NIB, izin edar MD/PIRT/PSAT, sertifikat halal dan NKV (untuk produk hewan) dari pemasok. | Purchasing (Procurement) | 5 | – | UU 18/2012, UU 33/2014, PP 42/2024 |
| 2 | Verifikasi sertifikat halal di SIHALAL dan izin edar di cekbpom — Bagian Halal memverifikasi sertifikat halal di SIHALAL dan izin edar di cekbpom; unggah hasil pengecekan. | Bagian Sertifikasi Halal | 1 | – | UU 33/2014, UU 18/2012 |
| 3 | Simpan dokumen dan catat masa berlaku — Simpan semua dokumen dan isi masa berlaku agar pengingat perpanjangan berjalan. | Purchasing (Procurement) | 1 | – | UU 18/2012, UU 33/2014, PP 42/2024 |

## 6. Daftar referensi peraturan

| Peraturan | Tentang | Penerbit | Catatan |
|---|---|---|---|
| UU 18/2012 | Pangan | DPR & Presiden |  |
| UU 33/2014 | Jaminan Produk Halal | DPR & Presiden | Diubah oleh UU 6/2023 |
| UU 6/2023 | Penetapan Perppu 2/2022 tentang Cipta Kerja menjadi Undang-Undang | DPR & Presiden |  |
| UU 18/2009 jo. UU 41/2014 | Peternakan dan Kesehatan Hewan | DPR & Presiden |  |
| UU 31/2004 jo. UU 45/2009 | Perikanan | DPR & Presiden |  |
| UU 13/2010 | Hortikultura | DPR & Presiden |  |
| UU 21/2019 | Karantina Hewan, Ikan, dan Tumbuhan | DPR & Presiden |  |
| UU 10/1995 jo. UU 17/2006 | Kepabeanan | DPR & Presiden |  |
| PP 86/2019 | Keamanan Pangan | Presiden |  |
| PP 95/2012 | Kesehatan Masyarakat Veteriner dan Kesejahteraan Hewan | Presiden |  |
| PP 42/2024 | Penyelenggaraan Bidang Jaminan Produk Halal | Presiden | Produk luar negeri wajib bersertifikat halal paling lambat 17 Oktober 2026 |
| PP 29/2023 | Peraturan Pelaksanaan UU 21/2019 tentang Karantina Hewan, Ikan, dan Tumbuhan | Presiden |  |
| [PP 28/2025](https://jdih.kemenkeu.go.id/api/download/b71d04f2-c2be-4eaa-9637-c944ae584f46/2025PP028.pdf) | Penyelenggaraan Perizinan Berusaha Berbasis Risiko | Presiden |  |
| Perpres 32/2022 | Neraca Komoditas | Presiden | Cek perubahan terbaru |
| Perpres 45/2023 | Badan Karantina Indonesia | Presiden |  |
| [Permendag 16/2025](https://peraturan.bpk.go.id/Details/323106) | Kebijakan dan Pengaturan Impor | Kementerian Perdagangan |  |
| [Permendag 18/2025](https://peraturan.bpk.go.id/Details/323120) | Kebijakan dan Pengaturan Impor Barang Pertanian dan Peternakan | Kementerian Perdagangan | Sudah diubah; cek perubahan terbaru |
| [Permendag 19/2025](https://peraturan.bpk.go.id/Details/323136) | Kebijakan dan Pengaturan Impor Garam dan Komoditas Perikanan | Kementerian Perdagangan |  |
| [Permentan 42/2019](https://peraturan.bpk.go.id/Download/195208/Permentan%20Nomor%2042%20Tahun%202019.pdf) | Pemasukan Karkas, Daging, Jeroan, dan/atau Olahannya ke dalam Wilayah Negara Republik Indonesia | Kementerian Pertanian | Cek perubahan terbaru |
| [Permentan 19/2025](https://peraturan.bpk.go.id/Details/323268) | Persyaratan Pemasukan Produk Hewan dalam Hal Tertentu yang Berasal dari Negara atau Zona dalam Suatu Negara Asal Pemasukan | Kementerian Pertanian |  |
| Permentan 11/2020 | Sertifikasi Nomor Kontrol Veteriner Unit Usaha Produk Hewan | Kementerian Pertanian | Cek versi terbaru |
| Permentan 39/2019 | Rekomendasi Impor Produk Hortikultura | Kementerian Pertanian | Sudah beberapa kali diubah; cek versi terbaru dan lartas HS di INSW |
| [Permen KP 58/2018](https://peraturan.bpk.go.id/Download/158697/Permen%20KP%2058%20Tahun-2018.pdf) | Rekomendasi Pemasukan Komoditas Perikanan Selain Ikan Hidup | Kementerian Kelautan dan Perikanan | Cek perubahan terbaru |
| Per BPOM 27/2017 | Pendaftaran Pangan Olahan | BPOM | Sudah diubah beberapa kali; cek versi terbaru |
| Per BPOM 31/2018 jo. 20/2021 | Label Pangan Olahan | BPOM |  |
| [Per BPOM 28/2023](https://peraturan.go.id/files/peraturan-bpom-no-28-tahun-2023.pdf) | Pengawasan Pemasukan Obat dan Makanan ke dalam Wilayah Indonesia | BPOM | Cek perubahan terbaru |
| Peraturan Badan Pangan Nasional | Pendaftaran Pangan Segar Asal Tumbuhan | Badan Pangan Nasional | Cek nomor dan versi terbaru |
| Keputusan Kepala BPJPH | Registrasi Sertifikat Halal Luar Negeri dan Lembaga Halal Luar Negeri yang diakui | BPJPH | Cek daftar LHLN yang berlaku |
| PMK Ketentuan Kepabeanan di Bidang Impor | Ketentuan Kepabeanan di Bidang Impor | Kementerian Keuangan | Cek nomor dan versi terbaru |
| PMK 26/2022 | Penetapan Sistem Klasifikasi Barang dan Pembebanan Tarif Bea Masuk atas Barang Impor (BTKI 2022) | Kementerian Keuangan | Cek perubahan terbaru |
| PMK Tarif Preferensi FTA | Tata cara pengenaan tarif bea masuk dalam rangka perjanjian internasional (AANZFTA, IA-CEPA, IJEPA, ACFTA, AKFTA, RCEP) | Kementerian Keuangan | Satu PMK per perjanjian |

Sumber yang diperiksa: [Permendag 16/2025](https://peraturan.bpk.go.id/Details/323106),
[Permendag 18/2025](https://peraturan.bpk.go.id/Details/323120), [Permendag 19/2025](https://peraturan.bpk.go.id/Details/323136),
[Permentan 19/2025](https://peraturan.bpk.go.id/Details/323268), [Permentan 42/2019](https://peraturan.bpk.go.id/Download/195208/Permentan%20Nomor%2042%20Tahun%202019.pdf),
[Per BPOM 28/2023](https://peraturan.go.id/files/peraturan-bpom-no-28-tahun-2023.pdf),
[BPJPH: wajib halal 2026 mencakup produk impor](https://www.antaranews.com/berita/5605380/bpjph-wajib-halal-mencakup-produk-impor-yang-beredar-di-indonesia),
[PP 28/2025](https://jdih.kemenkeu.go.id/api/download/b71d04f2-c2be-4eaa-9637-c944ae584f46/2025PP028.pdf).

## 7. Temuan pada item master

Hasil pemetaan 2.864 item code ada di file *pemetaan-item-ke-izin.xlsx* (sheet *Temuan data item master*):

- **522 item** kode HS kosong, bukan 8 digit atau rusak (mis. `20130`, `00232900`). Lartas ditentukan dari HS,
  jadi kolom ini perlu dibersihkan di SAP.
- **38 item babi** tidak bertanda `U_Non_Halal = Y` (hanya 13 dari 51 yang bertanda). Izinara menandai otomatis dari
  subgrup PORK dan kata di nama barang, tetapi sumber datanya sebaiknya diperbaiki.
- **4 item cokelat/snack** memakai HS 1605 (olahan moluska) — kemungkinan salah ketik.
- Kode negara **NW** (Norwegia) dan **SZ** (Swiss) bukan kode ISO; Izinara memetakannya ke NO dan CH.

## 8. Menu Izinara

| Menu | Untuk |
|---|---|
| Dashboard izin impor | KPI, kesiapan per pengapalan, beban kerja & waktu respons per bagian, progres per kelompok dan jenis izin, aktivitas terlambat, izin segera habis |
| Pengapalan impor | Rencana impor, kebutuhan izin, tombol ruang diskusi |
| Pengurusan izin | Kanban per status, aktivitas, dokumen, dasar hukum, memo |
| Tugas per bagian | Daftar aktivitas terbuka per bagian/petugas, filter *Tugas saya* dan *Terlambat* |
| Verifikasi dokumen | Antrean dokumen menunggu verifikasi per bagian verifikator |
| Memo antar bagian | Permintaan/pertanyaan antar bagian dengan tenggat dan waktu respons |
| Register izin & sertifikat | Semua izin yang dimiliki, kalender masa berlaku, pengingat perpanjangan |
| Konfigurasi | Item code & template, template pengurusan (aktivitas, dokumen wajib, kriteria), jenis izin, referensi peraturan, aturan pemetaan, bagian/petugas, impor item master |

Add-on **izinara_demo** (terpisah) mengisi data contoh: 6 petugas (kata sandi `izinara`: rina.ml, hasan.halal,
dewi.izin, budi.purchasing, andi.impor, sari.manajer), 14 item code dari item master, 7 pengapalan (daging sapi
Australia, babi Denmark, salmon Norwegia, pasta Italia, sweet corn Prancis, butter Argentina, cumi Tiongkok) dengan
pengurusan di semua status, dokumen terverifikasi/ditolak/menunggu, memo terlambat dan tepat waktu, serta izin yang
segera habis dan kedaluwarsa.

## 9. Tangkapan layar

Gambar di bawah diambil dari database demo dan juga tampil di menu **Panduan**. Tangkapan layar portal pemerintah
(SIHALAL, e-Reg BPOM, SINSW, INSW, CEISA) dapat ditambahkan di `izinara/static/img/guide/`.

| | |
|---|---|
| ![Dashboard](../static/img/guide/dashboard.jpg)<br>Dashboard izin impor | ![Kebutuhan izin](../static/img/guide/kebutuhan-izin.jpg)<br>Pengapalan, tab Kebutuhan izin |
| ![Aktivitas](../static/img/guide/aktivitas.jpg)<br>Aktivitas dengan dokumen wajib | ![Verifikasi dokumen](../static/img/guide/verifikasi-dokumen.jpg)<br>Verifikasi dokumen (banyak file) |
| ![Memo](../static/img/guide/memo.jpg)<br>Memo antar bagian | ![Register izin](../static/img/guide/register-izin.jpg)<br>Register izin & sertifikat |
| ![Item code](../static/img/guide/item-code.jpg)<br>Item code & template izin | ![Template](../static/img/guide/template.jpg)<br>Template pengurusan |
| ![Pengurusan](../static/img/guide/pengurusan-form.jpg)<br>Pengurusan izin | ![Impor item master](../static/img/guide/impor-item-master.jpg)<br>Impor item master SAP |
| ![Dokumen prinsipal](../static/img/guide/dokumen-prinsipal.jpg)<br>Dokumen prinsipal ditolak, minta revisi | ![Bukti BPOM](../static/img/guide/bukti-pengajuan-bpom.jpg)<br>Bukti pengajuan SKI BPOM |
| ![Rancangan label](../static/img/guide/rancangan-label.jpg)<br>Rancangan label Bahasa Indonesia | ![SHLN](../static/img/guide/shln.jpg)<br>Sertifikat halal LN untuk SHLN |
| ![Bukti RP](../static/img/guide/bukti-pengajuan-rp.jpg)<br>Bukti pengajuan RP Kementan | ![Pelepasan karantina](../static/img/guide/pelepasan-karantina.jpg)<br>Sertifikat pelepasan karantina |
| ![Cek lartas](../static/img/guide/cek-lartas.jpg)<br>Hasil cek lartas INSW | ![SPPB](../static/img/guide/sppb.jpg)<br>SPPB |

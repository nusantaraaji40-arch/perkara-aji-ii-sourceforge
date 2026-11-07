# Contoh Konektor SourceForge — PERKARA AJI II

Contoh pemakaian konektor SourceForge (custom.sourceforge) dari workspace Muse, khusus operasi **read-only** yang aman. Repo ini bagian dari proyek PERKARA AJI II — agen AI yang membuat video YouTube 8 menit dari foto presenter.

SourceForge masih menjadi rumah proyek video open source yang dipakai di pipeline video (mis. VirtualDub2 untuk potong/encode klip, dan Apache Allura — mesin forge + REST API di balik SourceForge itu sendiri). Proyek publik bisa dibaca lewat API tanpa login, jadi contoh di sini tetap berguna sebagai pembaca direktori proyek, meski tokennya belum terbukti.

## Isi repo

| File | Konektor | Perintah |
|---|---|---|
| `sourceforge_example.py` | custom.sourceforge | `project`, `profile` |

## Cara pakai

```bash
python3 sourceforge_example.py project allura
python3 sourceforge_example.py project vdfiltermod
python3 sourceforge_example.py profile <username>
```

Syarat: helper konektor harus ada di mesinmu, yaitu `~/workspace/custom-connectors/custom.sourceforge/bin/sourceforge.py`. Kalau helper-mu ada di tempat lain, atur lewat environment variable:

```bash
SOURCEFORGE_HELPER=/path/ke/sourceforge.py python3 sourceforge_example.py
```

## Tanpa secret

File-file di repo ini **tidak berisi API key, token, atau rahasia apa pun**. Semua otentikasi dilakukan helper konektor, yang memakai surrogate dari secure storage Muse. Bearer token SourceForge dibuat di `https://sourceforge.net/auth/oauth/` — yang dimasukkan harus bearer token, bukan consumer key. Jangan pernah menaruh token di file, di `.env`, atau di commit.

## Status verifikasi — jujur (2026-11-07)

Konektor SourceForge **belum terbukti bekerja** pada 2026-11-07: `project forge` (GET /rest/p/forge/) dijawab HTTP 401 Unauthorized, padahal panggilan yang sama tanpa kredensial dijawab 200. Artinya bearer token yang tersimpan ditolak SourceForge — kemungkinan invalid/kedaluwarsa, atau yang dimasukkan adalah consumer key, bukan bearer token.

Perbaikan: buat bearer token baru di `https://sourceforge.net/auth/oauth/`, lalu reconnect. **Update 2026-11-07 ~03:01:** link reconnect sudah dikirim — status di atas bisa berubah begitu reconnect diisi. Identitas akun SourceForge Mas Aji juga belum diketahui (Allura tidak punya endpoint whoami — `/rest/u/me/profile` itu 404; profil dibaca lewat `/rest/u/<username>/profile`). Jangan klaim konektor ini bekerja sebelum ada panggilan terautentikasi yang berhasil.

## Repo terkait (hasil screening)

Repo open source terbaik yang berhubungan dengan SourceForge (bukan bagian repo ini, lisensinya masing-masing):

- **Apache Allura** — https://sourceforge.net/p/allura/ — mesin forge + REST API di balik SourceForge itu sendiri, lisensi Apache-2.0. Referensi definitif API Allura + contoh pemakaian (`scripts/project_export`); bukan dipakai langsung di pipeline video.
- **VirtualDub2 (vdfiltermod)** — https://sourceforge.net/p/vdfiltermod/ — editor video open source, lisensi GPLv2. Cocok untuk potong/encode klip 10 detik di pipeline video. Catatan: update terakhir 2020-03-19 (stale), praktisnya Windows.

Catatan: tidak ditemukan client library/SDK Python khusus Allura/SourceForge — yang ada hanya dokumentasi API resmi + contoh di dalam repo Allura sendiri.

## Lisensi

Code contoh di repo ini berlisensi **MIT** (lihat `LICENSE`). Dependensi/repo terkait di atas punya lisensinya sendiri-sendiri — periksa sebelum memakai.

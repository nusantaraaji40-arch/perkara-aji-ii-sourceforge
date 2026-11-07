#!/usr/bin/env python3
"""Contoh pemakaian konektor SourceForge (custom.sourceforge) untuk PERKARA AJI II.

STATUS VERIFIKASI — JUJUR, per 2026-11-07 (dicek ulang hari ini):
  GAGAL / BELUM TERBUKTI. `project forge` (GET /rest/p/forge/) masih
  mengembalikan HTTP 401 Unauthorized, padahal panggilan yang sama TANPA
  kredensial mengembalikan 200. Artinya bearer token yang tersimpan
  DITOLAK SourceForge — kemungkinan invalid/kedaluwarsa, atau yang
  dimasukkan adalah consumer key, bukan bearer token (halaman
  https://sourceforge.net/auth/oauth/ menampilkan keduanya).
  Perbaikan yang sudah diminta: buat bearer token baru di /auth/oauth/
  lalu reconnect; link reconnect sudah dikirim ke Mas Aji sekitar
  2026-11-07 03:01. Identitas akun SourceForge Mas Aji juga belum
  diketahui (Allura TIDAK punya endpoint whoami — /rest/u/me/profile
  itu 404; profil dibaca lewat /rest/u/<username>/profile).
  JANGAN klaim konektor ini bekerja sebelum ada panggilan terautentikasi
  yang berhasil.

File ini TIDAK berisi API key/token/rahasia apa pun. Semua panggilan
dilewatkan ke helper resmi `bin/sourceforge.py` yang memakai surrogate
dari secure storage. Hanya operasi READ-ONLY yang aman (project,
profile). Jangan ubah helper/CONNECTOR.md/connector.yaml.

Cara pakai:
    python3 examples/konektor/sourceforge_example.py project allura
    python3 examples/konektor/sourceforge_example.py project vdfiltermod
    python3 examples/konektor/sourceforge_example.py profile <username>

Kenapa SourceForge relevan untuk PERKARA AJI II:
  SourceForge masih menjadi rumah proyek video open source yang dipakai
  di pipeline video (mis. VirtualDub2 untuk potong/encode klip, dan
  Apache Allura — mesin forge + REST API di balik SourceForge itu
  sendiri). Proyek publik bisa dibaca lewat API TANPA login, jadi
  contoh di bawah tetap berguna sebagai pembaca direktori proyek,
  meski tokennya belum terbukti. Repo yang sudah di-clone:
  data/konektor-repo-screening/sourceforge/allura (Apache-2.0) dan
  data/konektor-repo-screening/sourceforge/vdfiltermod (GPLv2).
"""
import json
import subprocess
import sys

import os

HELPER = os.environ.get("SOURCEFORGE_HELPER", "/home/hatch/workspace/custom-connectors/custom.sourceforge/bin/sourceforge.py")


def run(*args):
    """Panggil helper resmi; kembalikan dict hasil atau None bila gagal."""
    proc = subprocess.run(
        [sys.executable, HELPER, *args],
        capture_output=True, text=True, timeout=60,
    )
    if proc.returncode != 0:
        print(f"[sourceforge] helper gagal (exit {proc.returncode}):", file=sys.stderr)
        print((proc.stderr or proc.stdout).strip()[-500:], file=sys.stderr)
        print("[sourceforge] Ingat: verifikasi konektor ini masih GAGAL "
              "(401, token ditolak). Pembacaan proyek publik tetap bisa "
              "dilakukan anonim lewat REST API, tapi itu TIDAK membuktikan "
              "token bekerja.", file=sys.stderr)
        return None
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        print("[sourceforge] output helper bukan JSON:", proc.stdout[:300],
              file=sys.stderr)
        return None


def main(argv):
    cmd = argv[1] if len(argv) > 1 else "project"
    if cmd == "project":
        project = argv[2] if len(argv) > 2 else "allura"
        data = run("project", project)
        if data:
            print("shortname:", data.get("shortname"), "| nama:", data.get("name"))
            print("url:", data.get("url"), "| private:", data.get("private"))
            print("ringkasan:", (data.get("summary") or "")[:200])
    elif cmd == "profile":
        username = argv[2]
        data = run("profile", username)
        if data:
            print("username:", data.get("username"), "| nama:", data.get("name"))
            print("url:", data.get("url"))
    else:
        print("perintah: project <shortname> | profile <username>", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

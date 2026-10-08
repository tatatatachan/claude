#!/usr/bin/env python3
"""ダウンロードフォルダ自動管理 (macOS向け / 標準ライブラリのみ)

  organize     種類・年月で仕分け + 先頭に日付を付与
  archive      21日以上前のファイルを _アーカイブ へ移動 (削除はしない)
  new-project  企業名/日付_案件 の雛形フォルダを作成
  undo         直近の実行分の移動を元に戻す

デフォルトは試走(dry-run)。実際に動かすには --apply を付ける。
  例: python3 folder_manager.py organize
      python3 folder_manager.py --apply organize
"""
import argparse, json, re, shutil, sys, time
from datetime import datetime
from pathlib import Path

DOWNLOADS = Path.home() / "Downloads"
PROJECTS = Path.home() / "Documents" / "案件"
ARCHIVE_DAYS = 21
LOG = Path.home() / ".folder_manager_log.jsonl"
ARCHIVE_DIR = "_アーカイブ"

CATEGORIES = {
    "書類": {".pdf", ".doc", ".docx", ".txt", ".md", ".pages", ".rtf"},
    "表・資料": {".xls", ".xlsx", ".csv", ".numbers", ".ppt", ".pptx", ".key"},
    "画像": {".jpg", ".jpeg", ".png", ".gif", ".heic", ".webp", ".svg", ".psd", ".ai"},
    "動画・音声": {".mp4", ".mov", ".mp3", ".wav", ".m4a"},
    "圧縮": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "インストーラ": {".dmg", ".pkg"},
}
OTHER = "その他"
SKIP_SUFFIX = {".crdownload", ".download", ".part", ".tmp"}
SUBFOLDERS = ["資料", "議事録", "見積・請求", "契約", "成果物"]
DATE_PREFIX = re.compile(r"^\d{8}_")


def category(p: Path) -> str:
    ext = p.suffix.lower()
    return next((c for c, exts in CATEGORIES.items() if ext in exts), OTHER)


def unique(dest: Path) -> Path:
    if not dest.exists():
        return dest
    n = 2
    while (d := dest.with_name(f"{dest.stem}_{n}{dest.suffix}")).exists():
        n += 1
    return d


def move(src: Path, dest: Path, apply: bool) -> None:
    dest = unique(dest)
    print(f"  {src.name}\n    -> {dest.relative_to(DOWNLOADS)}")
    if not apply:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dest))
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"t": datetime.now().isoformat(), "from": str(src), "to": str(dest)}, ensure_ascii=False) + "\n")


def mode(a) -> str:
    return "" if a.apply else " 試走(dry-run)"


def cmd_organize(a):
    print("[organize]" + mode(a))
    n = 0
    for p in sorted(DOWNLOADS.iterdir()):
        if not p.is_file() or p.name.startswith(".") or p.suffix.lower() in SKIP_SUFFIX:
            continue
        mtime = datetime.fromtimestamp(p.stat().st_mtime)
        name = p.name if DATE_PREFIX.match(p.name) else f"{mtime:%Y%m%d}_{p.name}"
        move(p, DOWNLOADS / category(p) / f"{mtime:%Y-%m}" / name, a.apply)
        n += 1
    print(f"{n} 件")


def cmd_archive(a):
    print(f"[archive] {a.days}日以上前" + mode(a))
    cutoff = time.time() - a.days * 86400
    n = 0
    for cat in [*CATEGORIES, OTHER]:
        base = DOWNLOADS / cat
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*")):
            if p.is_file() and not p.name.startswith(".") and p.stat().st_mtime < cutoff:
                move(p, DOWNLOADS / ARCHIVE_DIR / p.relative_to(DOWNLOADS), a.apply)
                n += 1
    print(f"{n} 件")


def cmd_new_project(a):
    root = PROJECTS / a.company / f"{datetime.now():%Y%m%d}_{a.project}"
    print(f"[new-project] {root}" + mode(a))
    for s in SUBFOLDERS:
        print(f"  {s}/")
        if a.apply:
            (root / s).mkdir(parents=True, exist_ok=True)


def cmd_undo(a):
    if not LOG.exists():
        sys.exit("ログがありません")
    rows = [json.loads(l) for l in LOG.read_text(encoding="utf-8").splitlines() if l]
    if not rows:
        sys.exit("ログが空です")
    last = rows[-1]["t"][:16]  # 直近の実行(分単位)をまとめて戻す
    batch = [r for r in rows if r["t"][:16] == last]
    print(f"[undo] {len(batch)} 件" + mode(a))
    for r in reversed(batch):
        src, dest = Path(r["to"]), unique(Path(r["from"]))
        print(f"  {src.name} -> {dest}")
        if a.apply and src.exists():
            shutil.move(str(src), str(dest))
    if a.apply:
        keep = [r for r in rows if r not in batch]
        LOG.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in keep), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true", help="実際に実行する(省略時は試走)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("organize").set_defaults(fn=cmd_organize)
    s = sub.add_parser("archive")
    s.add_argument("--days", type=int, default=ARCHIVE_DAYS)
    s.set_defaults(fn=cmd_archive)
    s = sub.add_parser("new-project")
    s.add_argument("company")
    s.add_argument("project")
    s.set_defaults(fn=cmd_new_project)
    sub.add_parser("undo").set_defaults(fn=cmd_undo)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()

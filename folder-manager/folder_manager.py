#!/usr/bin/env python3
"""ダウンロード自動整理 (macOS向け / 標準ライブラリのみ)

触るのは ~/Downloads/自動整理くん/ の直下と _アーカイブ だけ。Downloads直下は触らない。

  organize     自動整理くん直下のファイルを、ファイル名の企業名・案件名から
               Googleドライブの案件フォルダ(企業名/日付_案件/資料 など)へ移す。
               判断できないものは動かさず、「要確認」として毎回知らせる。
  archive      自動整理くん直下に21日以上残ったファイルを
               _アーカイブ/種類/年月/ へ移す (削除はしない)
  new-project  企業名/日付_案件 の雛形フォルダを案件フォルダ内に作成
  undo         直近の実行分の移動を元に戻す

デフォルトは試走(dry-run)。実際に動かすには --apply を付ける。
設定は同じフォルダの config.json (config.example.json を参考に)。
"""
import argparse, json, re, shutil, subprocess, sys, time
from datetime import datetime
from pathlib import Path

ROOT = Path.home() / "Downloads" / "自動整理くん"
LOG = Path.home() / ".folder_manager_log.jsonl"
CONFIG = Path(__file__).with_name("config.json")
ARCHIVE_DIR = "_アーカイブ"
REPORT = ROOT / "_要確認.txt"

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
DEFAULT_SUB = "資料"
SUB_KEYWORDS = {
    "議事録": ["議事録", "minutes"],
    "見積・請求": ["見積", "請求", "invoice"],
    "契約": ["契約", "NDA", "覚書"],
    "成果物": ["納品", "成果物"],
}
DATE_PREFIX = re.compile(r"^\d{8}_")


def load_config() -> dict:
    if not CONFIG.exists():
        sys.exit(f"{CONFIG} がありません。config.example.json をコピーして作成してください")
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def projects_root(cfg) -> Path:
    p = Path(cfg["projects_root"]).expanduser()
    if not p.is_dir():
        sys.exit(f"案件フォルダが見つかりません: {p}\n(Googleドライブが同期済みか、config.json の projects_root を確認)")
    return p


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


def show(p: Path, base: Path) -> str:
    try:
        return str(p.relative_to(base))
    except ValueError:
        return str(p)


def move(src: Path, dest: Path, apply: bool, base: Path = ROOT) -> None:
    dest = unique(dest)
    print(f"  {src.name}\n    -> {show(dest, base)}")
    if not apply:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dest))
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"t": datetime.now().isoformat(), "from": str(src), "to": str(dest)}, ensure_ascii=False) + "\n")


def mode(a) -> str:
    return "" if a.apply else " 試走(dry-run)"


def inbox_files():
    if not ROOT.is_dir():
        sys.exit(f"{ROOT} がありません。先に作成してください")
    for p in sorted(ROOT.iterdir()):
        if p.is_file() and not p.name.startswith((".", "_")) and p.suffix.lower() not in SKIP_SUFFIX:
            yield p


def find_company(name: str, companies: dict):
    best = None
    for company, aliases in companies.items():
        for al in [company, *aliases]:
            if al and al in name and (best is None or len(al) > best[1]):
                best = (company, len(al))
    return best[0] if best else None


def find_project(name: str, company_dir: Path):
    best = None
    for d in company_dir.iterdir():
        if not d.is_dir() or d.name.startswith((".", "_")):
            continue
        proj = DATE_PREFIX.sub("", d.name)
        if proj and proj in name and (best is None or len(proj) > len(best[1])):
            best = (d, proj)
    return best


def pick_sub(name: str) -> str:
    low = name.lower()
    for sub, kws in SUB_KEYWORDS.items():
        if any(k.lower() in low for k in kws):
            return sub
    return DEFAULT_SUB


def notify(text: str) -> None:
    if sys.platform == "darwin":
        subprocess.run(["osascript", "-e", f'display notification "{text}" with title "自動整理くん"'], check=False)


def cmd_organize(a):
    cfg = load_config()
    root = projects_root(cfg)
    print("[organize]" + mode(a))
    moved, unresolved = 0, []
    for p in inbox_files():
        company = find_company(p.name, cfg.get("companies", {}))
        if not company:
            unresolved.append((p, "ファイル名に企業名が見つからない"))
            continue
        cdir = root / company
        if not cdir.is_dir():
            unresolved.append((p, f"企業フォルダがない: {company}"))
            continue
        hit = find_project(p.name, cdir)
        if not hit:
            unresolved.append((p, f"{company} のどの案件か分からない"))
            continue
        pdir, proj = hit
        date = datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y%m%d")
        stripped = DATE_PREFIX.sub("", p.name)
        if re.match(rf"^\d{{8}}_{re.escape(company)}_", p.name):
            new = p.name
        elif stripped.startswith(f"{company}_{proj}"):
            new = f"{date}_{stripped}"
        else:
            new = f"{date}_{company}_{proj}_{stripped}"
        move(p, pdir.joinpath(pick_sub(p.name), new), a.apply, base=root)
        moved += 1
    print(f"{moved} 件を案件フォルダへ")
    if unresolved:
        print(f"\n[要確認] {len(unresolved)} 件 (動かしていません)")
        for p, why in unresolved:
            print(f"  {p.name}  <- {why}")
    if a.apply:
        lines = [f"{datetime.now():%Y-%m-%d %H:%M} 時点の要確認 ({len(unresolved)} 件)"] + [f"- {p.name}  ({why})" for p, why in unresolved]
        REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
        if unresolved:
            notify(f"{len(unresolved)}件が分かりません。_要確認.txt を見てください")


def cmd_archive(a):
    days = a.days if a.days is not None else load_config().get("archive_days", 21)
    print(f"[archive] {days}日以上前" + mode(a))
    cutoff = time.time() - days * 86400
    n = 0
    for p in inbox_files():
        st = p.stat().st_mtime
        if st < cutoff:
            ym = datetime.fromtimestamp(st).strftime("%Y-%m")
            move(p, ROOT / ARCHIVE_DIR / category(p) / ym / p.name, a.apply)
            n += 1
    print(f"{n} 件")


def cmd_new_project(a):
    root = projects_root(load_config())
    proj = root / a.company / f"{datetime.now():%Y%m%d}_{a.project}"
    print(f"[new-project] {proj}" + mode(a))
    for s in SUBFOLDERS:
        print(f"  {s}/")
        if a.apply:
            (proj / s).mkdir(parents=True, exist_ok=True)


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
    s.add_argument("--days", type=int, default=None)
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

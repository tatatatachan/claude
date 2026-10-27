#!/usr/bin/env python3
"""tokens.json の色・書体を、Googleスライド用の batchUpdate リクエストに変換する。

使い方:
  python3 apply_tokens.py tokens.json spec1.json spec2.json spec3.json > requests.json
spec*.json は、スライドを組んだときの要素定義（slides_helper.py build と同じ形式）。
出力は update_presentation の requests の配列（スライドごとのリストのリスト）。
既存の要素IDをそのまま使うので、Driveで複製したデッキにも適用できる。
"""
import json, sys

EMU = 914400
def emu(x): return int(round(x * EMU))
def col(h):
    h = h.lstrip('#')
    return {"rgbColor": {"red": round(int(h[0:2], 16) / 255, 3), "green": round(int(h[2:4], 16) / 255, 3), "blue": round(int(h[4:6], 16) / 255, 3)}}

def tstyle(oid, font=None, color=None, bold=None, size=None, rng=None, cell=None):
    st, f = {}, []
    if font: st["fontFamily"] = font; f.append("fontFamily")
    if color: st["foregroundColor"] = {"opaqueColor": col(color)}; f.append("foregroundColor")
    if bold is not None: st["bold"] = bold; f.append("bold")
    if size: st["fontSize"] = {"magnitude": size, "unit": "PT"}; f.append("fontSize")
    r = {"objectId": oid, "textRange": rng or {"type": "ALL"}, "style": st, "fields": ",".join(f)}
    if cell: r["cellLocation"] = cell
    return {"updateTextStyle": r}

def fill(oid, color):
    return {"updateShapeProperties": {"objectId": oid, "shapeProperties": {"shapeBackgroundFill": {"solidFill": {"color": col(color)}}}, "fields": "shapeBackgroundFill.solidFill.color"}}

# 旧デッキの色 → トークン名
OLD = {"#1F2937": "ink", "#6B7280": "sub", "#1F3864": "jp", "#9DB7E0": "sky", "#DCE6F5": "mist", "#E8F0FA": "paper", "#FFFFFF": "white"}

def restyle(tok, spec, page_numbers):
    C, F = tok["colors"], tok["fonts"]
    out = []
    for s in spec["slides"]:
        R = []
        pg = s["id"]
        is_divider = any(e["type"] == "rect" and e.get("fill") == "#1F3864" for e in s["elements"])
        for e in s["elements"]:
            oid, t = e["id"], e["type"]
            if t == "table":
                # 表：見出し行と1列目は太字のまま。見出し行の文字を jp に
                nr, nc = len(e["rows"]), len(e["rows"][0])
                for c in range(nc):  # 見出し行だけ jp に。本文はテーマの黒のまま
                    if not e["rows"][0][c]: continue
                    R.append(tstyle(oid, color=C["jp"], cell={"rowIndex": 0, "columnIndex": c}))
                continue
            if t == "rect" and e.get("fill") == "#1F3864":
                R.append(fill(oid, C["jp"])); continue
            if e.get("fill"):
                R.append(fill(oid, C[OLD.get(e["fill"].upper(), "paper")]))
            if not e.get("text"): continue
            oldc = (e.get("color") or "#1F2937").upper()
            role = OLD.get(oldc, "ink")
            if is_divider:
                if role == "sky": R.append(tstyle(oid, font=F["latin"], color=C["sky"]))
                elif role == "white": R.append(tstyle(oid, font=F["heading"], color=C["white"]))
                else: R.append(tstyle(oid, font=F["body"], color=C["paper"]))
                continue
            if oid.endswith("_title"):
                R.append(tstyle(oid, font=F["heading"], color=C["ink"]))
            elif oid.endswith("_foot"):
                R.append(tstyle(oid, font=F["body"], color=C["sub"]))
            elif role == "white":  # 青い面の白文字（理念カード）
                R.append(tstyle(oid, font=F["heading"], color=C["white"]))
            elif role == "jp" and e.get("fill"):  # 数字カード
                first = e["text"].split("\n")[0]
                R.append(tstyle(oid, font=F["body"], color=C["jp"]))
                R.append(tstyle(oid, font=F["number"], size=22, rng={"type": "FIXED_RANGE", "startIndex": 0, "endIndex": len(first)}))
            elif role == "jp":  # 小見出し
                R.append(tstyle(oid, font=F["body"], color=C["sky-text"]))
            else:
                R.append(tstyle(oid, font=F["body"], color=C["body"]))
        # サイドバーとページ番号
        n = page_numbers[pg]
        P = tok["page"]
        if not is_divider:
            R.append({"createShape": {"objectId": f"{pg}_bar", "shapeType": "RECTANGLE", "elementProperties": {"pageObjectId": pg, "size": {"width": {"magnitude": emu(P["sidebar_w_in"]), "unit": "EMU"}, "height": {"magnitude": emu(P["height_in"]), "unit": "EMU"}}, "transform": {"scaleX": 1, "scaleY": 1, "translateX": emu(P["sidebar_x_in"]), "translateY": 0, "unit": "EMU"}}}})
            R.append({"updateShapeProperties": {"objectId": f"{pg}_bar", "shapeProperties": {"shapeBackgroundFill": {"solidFill": {"color": col(C["jp"])}}, "outline": {"propertyState": "NOT_RENDERED"}}, "fields": "shapeBackgroundFill.solidFill.color,outline.propertyState"}})
        # 番号の箱はサイドバーより広く（0.5in）して、2桁でも折り返さないようにする。中心はサイドバーの中心
        nw = 0.5
        nx = P["sidebar_x_in"] + P["sidebar_w_in"] / 2 - nw / 2
        R.append({"createShape": {"objectId": f"{pg}_num", "shapeType": "TEXT_BOX", "elementProperties": {"pageObjectId": pg, "size": {"width": {"magnitude": emu(nw), "unit": "EMU"}, "height": {"magnitude": emu(0.3), "unit": "EMU"}}, "transform": {"scaleX": 1, "scaleY": 1, "translateX": emu(nx), "translateY": emu(P["height_in"] - 0.35), "unit": "EMU"}}}})
        R.append({"insertText": {"objectId": f"{pg}_num", "text": str(n)}})
        R.append(tstyle(f"{pg}_num", font=F["number"], color=C["white"], size=10))
        R.append({"updateParagraphStyle": {"objectId": f"{pg}_num", "textRange": {"type": "ALL"}, "style": {"alignment": "CENTER"}, "fields": "alignment"}})
        out.append((pg, R))
    return out

if __name__ == "__main__":
    tok = json.load(open(sys.argv[1]))
    specs = [json.load(open(p)) for p in sys.argv[2:]]
    slides = [s for sp in specs for s in sp["slides"]]
    nums = {s["id"]: i + 2 for i, s in enumerate(slides)}  # 表紙が1
    out = []
    for sp in specs:
        out += restyle(tok, sp, nums)
    json.dump(out, sys.stdout, ensure_ascii=False, separators=(",", ":"))

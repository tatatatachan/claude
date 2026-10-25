#!/usr/bin/env python3
"""デザインハーネス 第3層(検証): 画像の使い回し(ほぼ同一画像)を見つける。
使い方: python3 dupcheck.py <画像フォルダ> [--threshold 4]
知覚ハッシュ(dHash 16x16)で比較し、ハミング距離が threshold 以下のペアを出す。
シリーズ物で「画像だけでは、どの回か分からない」(HR-007)を機械的に防ぐ。"""
import sys, os, itertools, warnings
warnings.filterwarnings("ignore")
from PIL import Image

def dhash(path, size=16):
    im = Image.open(path).convert('L').resize((size + 1, size), Image.LANCZOS)
    px = list(im.getdata()); bits = 0
    for y in range(size):
        for x in range(size):
            bits = (bits << 1) | (px[y * (size + 1) + x] > px[y * (size + 1) + x + 1])
    return bits

def main():
    args = sys.argv[1:]
    if not args: print(__doc__); sys.exit(2)
    folder = args[0]; th = int(args[args.index('--threshold') + 1]) if '--threshold' in args else 4
    files = sorted(f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')))
    hs = {f: dhash(os.path.join(folder, f)) for f in files}
    pairs = [(a, b, bin(hs[a] ^ hs[b]).count('1')) for a, b in itertools.combinations(files, 2)]
    dup = sorted([p for p in pairs if p[2] <= th], key=lambda p: p[2])
    print(f'{len(files)} 枚を比較。ほぼ同一(距離 <= {th}): {len(dup)} 組')
    for a, b, d in dup: print(f'  [FAIL] duplicate: {a} と {b} (距離 {d})')
    sys.exit(1 if dup else 0)

main()

import sys,re,json,urllib.parse,subprocess,base64,io,html,time
from PIL import Image
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124.0 Safari/537.36'
def get(url,binary=False,t=20):
    r=subprocess.run(['curl','-sSL','-m',str(t),'-A',UA,url],capture_output=True)
    return r.stdout if binary else r.stdout.decode('utf8','ignore')
def norm(s):return re.sub(r'[\W_]','',s)[:14]
def real_url(title):
    q=urllib.parse.quote(title[:60])
    x=get(f'https://www.bing.com/news/search?q={q}&format=rss&setmkt=ja-JP')
    for m in re.finditer(r'<item>.*?</item>',x,re.S):
        it=m.group(0)
        t=html.unescape(re.search(r'<title>(.*?)</title>',it,re.S).group(1))
        if norm(t)[:8]==norm(title)[:8]:
            u=re.search(r'url=([^&]+)&amp;',it)
            if u:return urllib.parse.unquote(u.group(1))
    return None
def og(url):
    h=get(url)[:200000]
    for pat in [r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)',r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']',r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)']:
        m=re.search(pat,h,re.I)
        if m:return urllib.parse.urljoin(url,html.unescape(m.group(1)))
def thumb(imgurl):
    b=get(imgurl,True)
    im=Image.open(io.BytesIO(b)).convert('RGB')
    im.thumbnail((360,203));
    o=io.BytesIO();im.save(o,'JPEG',quality=62,optimize=True)
    return 'data:image/jpeg;base64,'+base64.b64encode(o.getvalue()).decode()
if __name__=='__main__':
    # 使い方: python3 thumb.py 入力JSON  （crawl.py の出力に realUrl と thumb を追記して上書き）
    # realUrl = Bingニュース経由で見つけた記事の本当のURL、thumb = 記事先頭画像(og:image)を縮小したdata URI
    path=sys.argv[1];w=json.load(open(path));n=0
    for it in w:
        if it.get('thumb'):continue
        try:
            u=real_url(it['title'])
            if not u:continue
            it['realUrl']=u
            i=og(u)
            if i:it['thumb']=thumb(i);n+=1
        except Exception:pass
        time.sleep(0.5)
    json.dump(w,open(path,'w'),ensure_ascii=False,indent=0);print(n,'thumbs ->',path)

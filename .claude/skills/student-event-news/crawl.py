#!/usr/bin/env python3
"""学生向けイベントの最新情報を、日本のWebから集める（Googleニュース RSS）。
使い方: python3 crawl.py [出力JSON] [何日前まで(既定2)]
出力: [{id,title,source,url,pubDate,eventDate,area,category,summary,query}]
"""
import sys,re,json,html,hashlib,subprocess,urllib.parse,datetime,time
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
OUT=sys.argv[1] if len(sys.argv)>1 else 'webnews.json'
DAYS=int(sys.argv[2]) if len(sys.argv)>2 else 2
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124.0 Safari/537.36'
QUERIES=['学生 イベント','大学生 イベント 開催','学生団体 イベント','インカレ イベント','学生 ビジコン','大学生 コンテスト 募集','学生 ハッカソン','就活 イベント 学生','学生 アワード','学生 フェス','学生 起業 イベント','キャリア イベント 大学生','学生 ボランティア イベント','学生 交流会','大学生 セミナー 参加者募集','学生 ピッチ コンテスト','インターン 説明会 大学生','学生 地域活性 プロジェクト 募集','学生 SDGs イベント','高校生 大学生 イベント 参加無料','11月 開催 学生 イベント','12月 開催 大学生 イベント','1月 開催 学生 イベント 参加者募集','来月 開催 大学生 参加者募集','学生 イベント 開催決定','学生 カンファレンス 開催']
WHO=re.compile(r'学生|大学生|大学|インカレ|高校生|学生団体|就活|新卒|院生|ゼミ|サークル')
WHAT=re.compile(r'イベント|開催|募集|参加|コンテスト|ビジコン|フェス|セミナー|説明会|ハッカソン|交流会|アワード|カンファレンス|ワークショップ|フォーラム|大会|シンポジウム|ピッチ|講座|プログラム|ツアー|インターン')
NOISE=re.compile(r'野球|サッカー|ラグビー|駅伝|優勝|試合|決勝|訃報|逮捕|事件|殺人|死亡|詐欺|不祥事|容疑|火災|事故|台風|地震|株価|決算|合格者|偏差値|入試|受験|ランキング|中止|延期のお知らせ|調印|協定|提携|竣工|開所')
PREFS=['北海道','青森','岩手','宮城','秋田','山形','福島','茨城','栃木','群馬','埼玉','千葉','東京','神奈川','新潟','富山','石川','福井','山梨','長野','岐阜','静岡','愛知','三重','滋賀','京都','大阪','兵庫','奈良','和歌山','鳥取','島根','岡山','広島','山口','徳島','香川','愛媛','高知','福岡','佐賀','長崎','熊本','大分','宮崎','鹿児島','沖縄']
CATS=[('起業・ビジコン',r'ビジコン|起業|ピッチ|スタートアップ|アントレ'),('テック',r'ハッカソン|プログラミング|AI|DX|データ|ロボット'),('キャリア・就活',r'就活|インターン|説明会|キャリア|採用|新卒|企業'),('コンテスト・アワード',r'コンテスト|アワード|表彰|グランプリ|コンペ'),('社会・地域',r'ボランティア|地域|まちづくり|SDGs|環境|防災|福祉|農'),('交流・フェス',r'フェス|祭|交流|サークル|インカレ')]
def fetch(url):
    for _ in range(2):
        r=subprocess.run(['curl','-sS','-m','25','-A',UA,url],capture_output=True)
        if r.returncode==0 and r.stdout:return r.stdout.decode('utf8','ignore')
        time.sleep(2)
    return ''
def jst(dt):return (dt.astimezone(datetime.timezone(datetime.timedelta(hours=9)))).date()
today=jst(datetime.datetime.now(datetime.timezone.utc))
def event_date(text,pub):
    m=re.search(r'(\d{1,2})月(\d{1,2})日',text) or re.search(r'(?<!\d)(\d{1,2})/(\d{1,2})(?!\d)',text)
    if not m:return ''
    mo,d=int(m.group(1)),int(m.group(2))
    try:dt=datetime.date(pub.year,mo,d)
    except ValueError:return ''
    if dt<pub-datetime.timedelta(days=3):
        try:dt=datetime.date(pub.year+1,mo,d)
        except ValueError:return ''
        if (dt-pub).days>120:return ''
    if (dt-pub).days>240:return ''
    return dt.isoformat()
def category(t):
    for name,rx in CATS:
        if re.search(rx,t):return name
    return 'その他'
items={}
for q in QUERIES:
    url='https://news.google.com/rss/search?q='+urllib.parse.quote(f'{q} when:{DAYS}d')+'&hl=ja&gl=JP&ceid=JP:ja'
    xml=fetch(url)
    try:root=ET.fromstring(xml)
    except Exception:continue
    for it in root.iter('item'):
        title=html.unescape(it.findtext('title') or '').strip()
        link=(it.findtext('link') or '').strip()
        src=html.unescape(it.findtext('source') or '').strip()
        if src and title.endswith(' - '+src):title=title[:-len(src)-3].strip()
        try:pub=jst(parsedate_to_datetime(it.findtext('pubDate')))
        except Exception:pub=today
        if not link or not title:continue
        if not(WHO.search(title) and WHAT.search(title)) or NOISE.search(title):continue
        key=hashlib.sha1(re.sub(r'\W','',title).encode()).hexdigest()[:12]
        if key in items:continue
        pref=[p for p in PREFS if p in title]
        items[key]={'id':'w_'+key,'title':title,'source':src,'url':link,'pubDate':pub.isoformat(),'eventDate':event_date(title,pub),'area':(pref[0] if pref else ''),'category':category(title),'summary':'','query':q}
    time.sleep(1.5)
res=sorted(items.values(),key=lambda x:x['pubDate'],reverse=True)
json.dump(res,open(OUT,'w'),ensure_ascii=False,indent=0)
print(len(res),'items ->',OUT)

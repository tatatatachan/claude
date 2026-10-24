/**
 * 齋藤健用 日程予約ツール バックエンド（Google Apps Script）
 *
 * セットアップ
 *  1. script.google.com で新規プロジェクト → このコードを Code.gs に、appsscript.json を
 *     （設定で「appsscript.json をエディタで表示」をオン）同名ファイルに貼る
 *  2. 「プロジェクトの設定」→ スクリプト プロパティに追加
 *       ADMIN_PASSCODE … 予約ページ作成用の合言葉（必須。無いと誰でも作れてしまうため）
 *       SLACK_WEBHOOK  … Slack Incoming Webhook URL（任意。予約・変更・キャンセルを通知）
 *  3. 「デプロイ」→ ウェブアプリ（実行：自分 / アクセス：全員）→ URL を index.html の API_URL へ
 *
 * 保存先：スクリプト紐づきスプレッドシート（初回に自動作成）
 *  pages    … 予約ページ（種類・所要時間・入れていい曜日と時間帯など）
 *  bookings … 予約（token で本人がキャンセル・変更できる）
 */
const TZ = 'Asia/Tokyo';
const PAGE_COLS = ['id', 'title', 'description', 'type', 'duration', 'windows', 'horizon', 'lead', 'meeting', 'adminKey', 'created'];
const BOOK_COLS = ['token', 'pageId', 'slot', 'name', 'email', 'note', 'extra', 'status', 'eventId', 'created'];

/* ---------- ユーティリティ ---------- */
function props_() { return PropertiesService.getScriptProperties(); }

function ss_() {
  let id = props_().getProperty('SS_ID');
  if (id) return SpreadsheetApp.openById(id);
  const ss = SpreadsheetApp.create('齋藤健 日程予約ツール（データ）');
  ss.getActiveSheet().setName('pages').appendRow(PAGE_COLS);
  ss.insertSheet('bookings').appendRow(BOOK_COLS);
  props_().setProperty('SS_ID', ss.getId());
  return ss;
}

function rid_(n) {
  const c = 'abcdefghijklmnopqrstuvwxyz0123456789';
  let s = '';
  for (let i = 0; i < n; i++) s += c[Math.floor(Math.random() * c.length)];
  return s;
}

function json_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}

function rows_(name, cols) {
  const sh = ss_().getSheetByName(name);
  return sh.getDataRange().getValues().slice(1).map((r, i) => {
    const o = { _row: i + 2 };
    cols.forEach((c, j) => o[c] = r[j]);
    return o;
  });
}

function findPage_(id) {
  const p = rows_('pages', PAGE_COLS).filter(r => r.id === id)[0];
  if (p) p.windows = JSON.parse(p.windows);
  return p;
}

function findBooking_(token) {
  return rows_('bookings', BOOK_COLS).filter(r => r.token === token)[0];
}

function toDate_(slot) { return new Date(slot.replace(' ', 'T') + ':00+09:00'); }
function fmt_(d, f) { return Utilities.formatDate(d, TZ, f); }

function slack_(text) {
  const url = props_().getProperty('SLACK_WEBHOOK');
  if (!url) return;
  try {
    UrlFetchApp.fetch(url, { method: 'post', contentType: 'application/json', payload: JSON.stringify({ text: text }) });
  } catch (e) { /* 通知失敗で予約を止めない */ }
}

/* ---------- 空き枠の計算 ---------- */
// 入れていい曜日・時間帯（windows）から枠を作り、過去・直近・予約済み・カレンダーの予定と重なる枠を除く
function availableSlots_(page, ignoreToken) {
  const now = new Date();
  const earliest = new Date(now.getTime() + page.lead * 3600000);
  const day0 = Utilities.parseDate(fmt_(now, 'yyyy-MM-dd'), TZ, 'yyyy-MM-dd');
  const rangeEnd = new Date(day0.getTime() + (page.horizon + 1) * 86400000);

  const busy = CalendarApp.getDefaultCalendar().getEvents(day0, rangeEnd)
    .filter(ev => ev.getMyStatus() !== CalendarApp.GuestStatus.NO)
    .map(ev => [ev.getStartTime().getTime(), ev.getEndTime().getTime()]);
  const taken = rows_('bookings', BOOK_COLS)
    .filter(b => b.pageId === page.id && b.status === 'confirmed' && b.token !== ignoreToken)
    .map(b => b.slot);

  const out = [];
  for (let i = 0; i <= page.horizon; i++) {
    const d = new Date(day0.getTime() + i * 86400000);
    const dow = Number(fmt_(d, 'u')) % 7; // 0=日 … 6=土
    const ds = fmt_(d, 'yyyy-MM-dd');
    page.windows.forEach(w => {
      if (w.days.indexOf(dow) < 0) return;
      const [sh, sm] = w.start.split(':').map(Number), [eh, em] = w.end.split(':').map(Number);
      for (let m = sh * 60 + sm; m + page.duration <= eh * 60 + em; m += page.duration) {
        const slot = ds + ' ' + ('0' + Math.floor(m / 60)).slice(-2) + ':' + ('0' + (m % 60)).slice(-2);
        if (out.indexOf(slot) >= 0 || taken.indexOf(slot) >= 0) continue;
        const s = toDate_(slot).getTime(), e = s + page.duration * 60000;
        if (s < earliest.getTime()) continue;
        if (busy.some(b => s < b[1] && e > b[0])) continue;
        out.push(slot);
      }
    });
  }
  return out.sort();
}

/* ---------- API ---------- */
// GET ?action=page&id=…[&key=…] / ?action=manage&token=…
function doGet(e) {
  const q = e.parameter;
  if (q.action === 'page') {
    const p = findPage_(q.id);
    if (!p) return json_({ error: 'ページが見つかりません' });
    const out = {
      id: p.id, title: p.title, description: p.description, type: p.type,
      duration: p.duration, meeting: p.meeting ? 'url' : 'meet', slots: availableSlots_(p),
    };
    if (q.key && q.key === p.adminKey) {
      out.bookings = rows_('bookings', BOOK_COLS).filter(b => b.pageId === p.id && b.status === 'confirmed')
        .map(b => ({ slot: b.slot, name: b.name, email: b.email, note: b.note, extra: b.extra }));
    }
    return json_(out);
  }
  if (q.action === 'manage') {
    const b = findBooking_(q.token);
    if (!b) return json_({ error: '予約が見つかりません' });
    const p = findPage_(b.pageId);
    return json_({
      pageId: b.pageId, title: p.title, duration: p.duration, slot: b.slot, name: b.name,
      status: b.status, slots: b.status === 'confirmed' ? availableSlots_(p, b.token) : [],
    });
  }
  return json_({ error: 'bad request' });
}

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    const d = JSON.parse(e.postData.contents);
    const fn = { create: create_, book: book_, cancel: cancel_, reschedule: reschedule_ }[d.action];
    return json_(fn ? fn(d) : { error: 'bad request' });
  } catch (err) {
    return json_({ error: String(err) });
  } finally {
    lock.releaseLock();
  }
}

function create_(d) {
  const pass = props_().getProperty('ADMIN_PASSCODE');
  if (!pass || d.passcode !== pass) return { error: '合言葉が違います（スクリプト プロパティ ADMIN_PASSCODE を設定してください）' };
  if (!d.title || !d.windows || !d.windows.length) return { error: 'タイトルと入れていい時間帯が必要です' };
  const id = 'h-' + rid_(6), key = rid_(16);
  ss_().getSheetByName('pages').appendRow([
    id, d.title, d.description || '', d.type === 'client' ? 'client' : 'student',
    Number(d.duration) || 60, JSON.stringify(d.windows), Number(d.horizon) || 14, Number(d.lead) || 24,
    d.meetingUrl || '', key, new Date(),
  ]);
  return { id: id, adminKey: key };
}

function addEvent_(page, slot, name, email, desc) {
  const s = toDate_(slot), en = new Date(s.getTime() + page.duration * 60000);
  const res = {
    summary: page.title + '（' + name + '様）',
    description: desc,
    start: { dateTime: s.toISOString(), timeZone: TZ },
    end: { dateTime: en.toISOString(), timeZone: TZ },
    attendees: [{ email: email }],
  };
  if (page.meeting) {
    res.location = page.meeting;
  } else {
    res.conferenceData = { createRequest: { requestId: rid_(12), conferenceSolutionKey: { type: 'hangoutsMeet' } } };
  }
  const ev = Calendar.Events.insert(res, 'primary', { conferenceDataVersion: 1, sendUpdates: 'all' });
  return ev;
}

function describe_(page, d) {
  const extra = Object.keys(d.extra || {}).map(k => k + '：' + d.extra[k]).join('\n');
  return [page.description, extra, d.note ? 'メモ：' + d.note : ''].filter(Boolean).join('\n\n');
}

function validate_(d) {
  if (!d.name || !/^[^@\s]+@[^@\s]+$/.test(d.email || '')) return 'お名前とメールアドレスを入力してください';
}

function book_(d) {
  const page = findPage_(d.id);
  if (!page) return { error: 'ページが見つかりません' };
  const bad = validate_(d);
  if (bad) return { error: bad };
  if (availableSlots_(page).indexOf(d.slot) < 0) return { error: 'この日時は埋まってしまいました。別の日時を選んでください。' };

  const ev = addEvent_(page, d.slot, d.name, d.email, describe_(page, d));
  const token = rid_(20);
  ss_().getSheetByName('bookings').appendRow([
    token, page.id, d.slot, d.name, d.email, d.note || '', JSON.stringify(d.extra || {}),
    'confirmed', ev.id, new Date(),
  ]);
  const extra = Object.keys(d.extra || {}).map(k => k + '：' + d.extra[k]).join(' / ');
  slack_(':calendar: *予約が入りました*\n' + page.title + '\n' + d.slot + '〜 ' + d.name + '様（' + d.email + '）\n' + extra + (ev.hangoutLink ? '\n' + ev.hangoutLink : ''));
  return { ok: true, token: token, meetUrl: ev.hangoutLink || page.meeting || '' };
}

function cancel_(d) {
  const b = findBooking_(d.token);
  if (!b || b.status !== 'confirmed') return { error: '予約が見つからないか、すでにキャンセル済みです' };
  try { Calendar.Events.remove('primary', b.eventId, { sendUpdates: 'all' }); } catch (e) { /* 既に削除済み */ }
  ss_().getSheetByName('bookings').getRange(b._row, BOOK_COLS.indexOf('status') + 1).setValue('cancelled');
  slack_(':x: *キャンセル*\n' + b.slot + '〜 ' + b.name + '様');
  return { ok: true };
}

function reschedule_(d) {
  const b = findBooking_(d.token);
  if (!b || b.status !== 'confirmed') return { error: '予約が見つかりません' };
  const page = findPage_(b.pageId);
  if (availableSlots_(page, b.token).indexOf(d.slot) < 0) return { error: 'この日時は埋まってしまいました。別の日時を選んでください。' };
  const s = toDate_(d.slot), en = new Date(s.getTime() + page.duration * 60000);
  Calendar.Events.patch({
    start: { dateTime: s.toISOString(), timeZone: TZ },
    end: { dateTime: en.toISOString(), timeZone: TZ },
  }, 'primary', b.eventId, { sendUpdates: 'all' });
  ss_().getSheetByName('bookings').getRange(b._row, BOOK_COLS.indexOf('slot') + 1).setValue(d.slot);
  slack_(':arrows_counterclockwise: *日程変更*\n' + b.slot + ' → ' + d.slot + '〜 ' + b.name + '様');
  return { ok: true };
}

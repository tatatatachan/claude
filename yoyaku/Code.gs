/**
 * 日程予約ツール バックエンド（Google Apps Script）
 * 使い方：
 *  1. script.google.com で新しいプロジェクトを作り、このコードを貼り付ける
 *  2. 「デプロイ」→「新しいデプロイ」→ 種類「ウェブアプリ」
 *     実行ユーザー：自分 / アクセス：全員 → デプロイ
 *  3. 発行された URL（…/exec）を index.html の API_URL に貼る
 * 保存先：このスクリプトに紐づくスプレッドシート（初回に自動作成）
 *  ・pages    … 予約ページ（id, title, description, duration, slots, adminKey, created）
 *  ・bookings … 予約（pageId, slot, name, email, note, created）
 * 予約が入ると自分のGoogleカレンダーに予定を作り、相手にも招待を送ります。
 */
const SS_PROP = 'SS_ID';

function ss_() {
  const p = PropertiesService.getScriptProperties();
  let id = p.getProperty(SS_PROP);
  if (id) return SpreadsheetApp.openById(id);
  const ss = SpreadsheetApp.create('日程予約ツール（データ）');
  ss.getActiveSheet().setName('pages').appendRow(['id', 'title', 'description', 'duration', 'slots', 'adminKey', 'created']);
  ss.insertSheet('bookings').appendRow(['pageId', 'slot', 'name', 'email', 'note', 'created']);
  p.setProperty(SS_PROP, ss.getId());
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

function findPage_(id) {
  const rows = ss_().getSheetByName('pages').getDataRange().getValues();
  for (let i = 1; i < rows.length; i++) {
    if (rows[i][0] === id) {
      return {
        id: rows[i][0], title: rows[i][1], description: rows[i][2],
        duration: rows[i][3], slots: JSON.parse(rows[i][4]), adminKey: rows[i][5],
      };
    }
  }
  return null;
}

function bookings_(id) {
  const rows = ss_().getSheetByName('bookings').getDataRange().getValues();
  return rows.slice(1).filter(r => r[0] === id)
    .map(r => ({ slot: r[1], name: r[2], email: r[3], note: r[4] }));
}

// GET ?action=get&id=xxx[&key=adminKey]
function doGet(e) {
  const q = e.parameter;
  if (q.action !== 'get') return json_({ error: 'bad request' });
  const page = findPage_(q.id);
  if (!page) return json_({ error: 'ページが見つかりません' });
  const list = bookings_(page.id);
  const out = {
    id: page.id, title: page.title, description: page.description,
    duration: page.duration, slots: page.slots, taken: list.map(b => b.slot),
  };
  if (q.key && q.key === page.adminKey) out.bookings = list;
  return json_(out);
}

// POST（text/plain の JSON）{action:'create'|'book', ...}
function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    const d = JSON.parse(e.postData.contents);
    if (d.action === 'create') return json_(create_(d));
    if (d.action === 'book') return json_(book_(d));
    return json_({ error: 'bad request' });
  } catch (err) {
    return json_({ error: String(err) });
  } finally {
    lock.releaseLock();
  }
}

function create_(d) {
  if (!d.title || !d.slots || !d.slots.length) return { error: 'タイトルと候補日時が必要です' };
  const id = 'h-' + rid_(6), key = rid_(16);
  ss_().getSheetByName('pages').appendRow([
    id, d.title, d.description || '', d.duration || 60, JSON.stringify(d.slots), key, new Date(),
  ]);
  return { id: id, adminKey: key };
}

function book_(d) {
  const page = findPage_(d.id);
  if (!page) return { error: 'ページが見つかりません' };
  if (page.slots.indexOf(d.slot) < 0) return { error: '無効な日時です' };
  if (!d.name || !/^[^@\s]+@[^@\s]+$/.test(d.email || '')) return { error: 'お名前とメールアドレスを入力してください' };
  if (bookings_(page.id).some(b => b.slot === d.slot)) return { error: 'この日時はすでに予約済みです。別の日時を選んでください。' };

  ss_().getSheetByName('bookings').appendRow([page.id, d.slot, d.name, d.email, d.note || '', new Date()]);

  const start = new Date(d.slot.replace(' ', 'T') + ':00+09:00');
  const end = new Date(start.getTime() + page.duration * 60000);
  CalendarApp.getDefaultCalendar().createEvent(page.title + '（' + d.name + '様）', start, end, {
    description: (page.description || '') + '\n\nメモ: ' + (d.note || ''),
    guests: d.email,
    sendInvites: true,
  });
  return { ok: true };
}

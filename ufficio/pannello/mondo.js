/* mondo.js - il mondo dell'Ufficio Notturno (versione con mappa dipinta).
   Un'unica mappa con l'edificio centrale e un villaggio per ogni progetto (fino a 6).
   Le immagini (mappa + edifici) stanno in immagini/; persone, luci, fumo, meteo e giorno/notte sono disegnati dal codice. */
(function () {
'use strict';
var DPR = Math.max(1, Math.min(2, window.devicePixelRatio || 1));
var MAPW = 2752, MAPH = 1536, IMGDIR = 'immagini/';
var Mondo = { onSelect: null, onCommand: null };
window.Mondo = Mondo;

var STATUS_COL = { in_coda: '#8793AC', in_corso: '#7FA8FF', bloccato: '#E8B44F', da_approvare: '#E8B44F', incompleto: '#F28A63', fallito: '#EF5B6B', completato: '#4CC38A' };
var STATUS_LABEL = { in_coda: 'In coda', in_corso: 'In corso', bloccato: 'Bloccato', da_approvare: 'Da approvare', incompleto: 'Da rivedere', fallito: 'Fallito', completato: 'Completato' };
var ZONE_OF = { in_coda: 'locanda', in_corso: 'lab', bloccato: 'torre', da_approvare: 'torre', incompleto: 'fucina', fallito: 'fucina', completato: 'archivio' };
var ZONE_TIP = { archivio: 'Completati', torre: 'In attesa di te', lab: 'In lavorazione', locanda: 'In coda', fucina: 'Da rivedere o falliti' };
Mondo.STATUS_COL = STATUS_COL;

var theme = { night: [14, 24, 72] };
/* ---------------- utilita' ---------------- */
function rng(seed) { var a = seed >>> 0; return function () { a |= 0; a = a + 0x6D2B79F5 | 0; var t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
function hash(s) { var h = 0; s = String(s); for (var i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0; return Math.abs(h); }
function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
function smooth(a, b, x) { var t = clamp((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t); }
function hex(c) { var m = /^#?([0-9a-f]{6})$/i.exec(c || ''); if (!m) return [128, 128, 128]; var n = parseInt(m[1], 16); return [n >> 16, (n >> 8) & 255, n & 255]; }
function rgb(a, al) { return 'rgba(' + (a[0] | 0) + ',' + (a[1] | 0) + ',' + (a[2] | 0) + ',' + (al == null ? 1 : al) + ')'; }
function mix(a, b, f) { a = typeof a === 'string' ? hex(a) : a; b = typeof b === 'string' ? hex(b) : b; return [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f, a[2] + (b[2] - a[2]) * f]; }
function shade(col, f) { var a = typeof col === 'string' ? hex(col) : col; return rgb(f > 0 ? mix(a, [255, 255, 255], f) : mix(a, [0, 0, 0], -f)); }
function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
function poly(c, pts, fill, stroke, lw) {
  c.beginPath(); c.moveTo(pts[0][0], pts[0][1]); for (var i = 1; i < pts.length; i++) c.lineTo(pts[i][0], pts[i][1]); c.closePath();
  if (fill) { c.fillStyle = fill; c.fill(); } if (stroke) { c.strokeStyle = stroke; c.lineWidth = lw || 1; c.lineJoin = 'round'; c.stroke(); }
}
function vgrad(c, y0, y1, a, b) { var g = c.createLinearGradient(0, y0, 0, y1); g.addColorStop(0, a); g.addColorStop(1, b); return g; }
function hgrad(c, x0, x1, a, b, m) { var g = c.createLinearGradient(x0, 0, x1, 0); g.addColorStop(0, a); if (m) g.addColorStop(.5, m); g.addColorStop(1, b); return g; }
function ell(c, x, y, rx, ry, fill) { c.beginPath(); c.ellipse(x, y, rx, ry, 0, 0, Math.PI * 2); c.fillStyle = fill; c.fill(); }
function rrect(c, x, y, w, h, r, fill) { c.beginPath(); c.moveTo(x + r, y); c.arcTo(x + w, y, x + w, y + h, r); c.arcTo(x + w, y + h, x, y + h, r); c.arcTo(x, y + h, x, y, r); c.arcTo(x, y, x + w, y, r); c.closePath(); c.fillStyle = fill; c.fill(); }
var SKINS = ['#F1C7A0', '#E0AC83', '#C98E64', '#8D5A3B', '#F6D3B8'], HAIRS = ['#2B1E1A', '#6B3F22', '#1F2A44', '#9A6B2F', '#3B2A4F', '#B5532F', '#D8C58A'];
function drawPerson(c, X, Y, a, dd, t) {
  var sc = .86 * (a.k || 1), st = a.task.stato, col = (dd.dep && dd.dep.colore) || '#7FA8FF', walk = a.moving, ph = a.ft, bob = walk ? Math.abs(Math.sin(ph)) * 1.4 : (a.mode === 'sleep' ? 0 : Math.sin(t * 2 + a.h) * .35);
  var front = a.sy >= 0, side = a.sx >= 0 ? 1 : -1;
  c.save(); c.translate(X, Y); c.scale(sc, sc);
  ell(c, 0, 1, 9, 3.6, 'rgba(10,25,5,.3)');
  var sitDrop = a.mode === 'sleep' ? 5 : 0;
  if (a.mode !== 'sleep') { var sw = walk ? Math.sin(ph) * 3 : 0; rrect(c, -4.5 + sw * .2, -9 - bob, 3.6, 9, 1.6, a.pants); rrect(c, .9 - sw * .2, -9 - bob, 3.6, 9, 1.6, shade(a.pants, -.15)); rrect(c, -5 + sw * .3, -1.8, 4.4, 2.6, 1.2, '#2A2230'); rrect(c, .6 - sw * .3, -1.8, 4.4, 2.6, 1.2, '#2A2230'); }
  else { rrect(c, -7, -5, 14, 4.4, 2, a.pants); rrect(c, -9, -2, 5, 2.8, 1.2, '#2A2230'); rrect(c, 4, -2, 5, 2.8, 1.2, '#2A2230'); }
  var by = -22 - bob + sitDrop * .5, g = c.createLinearGradient(-6, by, 6, by + 14); g.addColorStop(0, shade(col, .2)); g.addColorStop(1, shade(col, -.3));
  rrect(c, -6, by, 12, 14 - sitDrop * .3, 4.5, g);
  var armCol = shade(col, -.15);
  if (a.mode === 'work') { var sw2 = Math.sin(t * 9 + a.h) * 3; rrect(c, -8.6, by + 2, 3, 9, 1.5, armCol); rrect(c, 5.4, by - 3 + sw2, 3, 9, 1.5, armCol); c.fillStyle = '#9AA3B2'; c.fillRect(6, by - 6 + sw2, 4, 3); }
  else if (a.mode === 'wait') { var sw3 = Math.sin(t * 5 + a.h) * .25; rrect(c, -8.6, by + 2, 3, 9, 1.5, armCol); c.save(); c.translate(7, by + 3); c.rotate(-2.7 + sw3); rrect(c, -1.5, -1, 3, 10, 1.5, armCol); ell(c, 0, 11, 2.2, 2.2, a.skin); c.restore(); }
  else { var sw4 = walk ? Math.sin(ph) * 3 : 0; rrect(c, -8.6, by + 1.5 + sw4 * .3, 3, 9, 1.5, armCol); rrect(c, 5.6, by + 1.5 - sw4 * .3, 3, 9, 1.5, armCol); }
  var hy = by - 6 + (a.mode === 'sleep' ? 2 : 0), hg = c.createRadialGradient(-2, hy - 2, 1, 0, hy, 8); hg.addColorStop(0, shade(a.skin, .15)); hg.addColorStop(1, shade(a.skin, -.12)); c.fillStyle = hg; c.beginPath(); c.arc(0, hy, 6.6, 0, 7); c.fill();
  c.fillStyle = a.hair; c.beginPath(); if (front) { c.arc(0, hy - 1, 6.9, Math.PI * 1.02, Math.PI * 1.98); c.lineTo(5.5, hy - 2.5); c.quadraticCurveTo(0, hy - 5, -5.5, hy - 2.5); } else c.arc(0, hy, 7, 0, 7); c.fill();
  if (front) { if (a.mode === 'sleep') { c.strokeStyle = '#3A2A2A'; c.lineWidth = 1; c.beginPath(); c.moveTo(-3.8 + side, hy + .6); c.lineTo(-1.6 + side, hy + .6); c.moveTo(1.6 + side, hy + .6); c.lineTo(3.8 + side, hy + .6); c.stroke(); } else { c.fillStyle = '#1B1626'; c.beginPath(); c.arc(-2.4 + side * .8, hy + .6, .9, 0, 7); c.arc(2.4 + side * .8, hy + .6, .9, 0, 7); c.fill(); } }
  c.restore();
  var sc2 = STATUS_COL[st] || '#8793AC', py = Y - 53 * sc + Math.sin(t * 2.4 + a.h) * 2.4;
  c.save(); c.translate(X, py); c.fillStyle = rgb(hex(sc2), .3); c.beginPath(); c.arc(0, 0, 10, 0, 7); c.fill();
  c.beginPath(); c.moveTo(0, -7); c.lineTo(4.6, 0); c.lineTo(0, 7); c.lineTo(-4.6, 0); c.closePath(); c.fillStyle = sc2; c.fill(); c.strokeStyle = 'rgba(255,255,255,.75)'; c.lineWidth = 1; c.stroke();
  c.beginPath(); c.moveTo(0, -7); c.lineTo(4.6, 0); c.lineTo(0, 0); c.closePath(); c.fillStyle = 'rgba(255,255,255,.35)'; c.fill(); c.restore();
  if (a.mode === 'wait') { var bx = X + 13, by2 = py - 2; rrect(c, bx - 7, by2 - 12, 15, 15, 5, '#FFF8E0'); c.fillStyle = '#B07A10'; c.font = 'bold 11px sans-serif'; c.textAlign = 'center'; c.fillText(st === 'da_approvare' ? '✓?' : '?', bx + .5, by2); }
}

function overcast() { return (env.cat === 'nuvoloso' || env.cat === 'pioggia' || env.cat === 'temporale' || env.cat === 'nebbia' || env.cat === 'neve') ? .6 : 0; }
function drawWeatherFront(c, w, h, dt) {
  var cat = env.cat;
  if (cat === 'pioggia' || cat === 'temporale') { var need = cat === 'temporale' ? 380 : 240; while (rain.length < need) rain.push({ x: Math.random() * (w + 200), y: Math.random() * h, v: 700 + Math.random() * 400, l: 10 + Math.random() * 12 }); c.strokeStyle = 'rgba(200,220,255,.5)'; c.lineWidth = 1.1; c.beginPath(); for (var i = 0; i < need; i++) { var d = rain[i]; if (!d.l) { d.l = 12; d.v = 800; } d.y += d.v * dt; d.x -= d.v * .22 * dt; if (d.y > h) { d.y = -20; d.x = Math.random() * (w + 200); } c.moveTo(d.x, d.y); c.lineTo(d.x + d.l * .22, d.y - d.l); } c.stroke(); c.fillStyle = 'rgba(40,52,80,' + (cat === 'temporale' ? .22 : .12) + ')'; c.fillRect(0, 0, w, h); }
  else if (cat === 'neve') { while (rain.length < 220) rain.push({ x: Math.random() * (w + 100), y: Math.random() * h, v: 40 + Math.random() * 50, r: 1 + Math.random() * 2, ph: Math.random() * 6 }); c.fillStyle = 'rgba(255,255,255,.9)'; for (var j = 0; j < 220; j++) { var f = rain[j]; if (!f.r) { f.r = 1.5; f.v = 50; f.ph = 0; } f.y += f.v * dt; f.x += Math.sin(tShow + f.ph) * 20 * dt; if (f.y > h) { f.y = -5; f.x = Math.random() * w; } c.beginPath(); c.arc(f.x, f.y, f.r, 0, 7); c.fill(); } c.fillStyle = 'rgba(230,240,255,.1)'; c.fillRect(0, 0, w, h); }
  else rain.length = 0;
  if (cat === 'nebbia') { for (var k = 0; k < 4; k++) { var cx = ((tShow * 8 + k * w / 3) % (w * 1.4)) - w * .2, gy = h * (.3 + k * .18), g = c.createRadialGradient(cx, gy, 10, cx, gy, w * .5); g.addColorStop(0, 'rgba(225,230,238,.32)'); g.addColorStop(1, 'rgba(225,230,238,0)'); c.fillStyle = g; c.fillRect(0, 0, w, h); } c.fillStyle = 'rgba(215,222,232,.18)'; c.fillRect(0, 0, w, h); }
  if (cat === 'temporale') { flashT -= dt; if (flashT <= 0) { flash = 1; flashT = 4 + Math.random() * 8; } if (flash > 0) { c.fillStyle = 'rgba(230,236,255,' + (flash * .5) + ')'; c.fillRect(0, 0, w, h); flash -= dt * 2.2; } }
}

/* ---------------- ciclo di disegno ---------------- */
function drawLabel(c, text, x, y, col, s) {
  c.save(); c.font = '600 ' + Math.round(12 * s) + 'px system-ui,sans-serif'; var tw = c.measureText(text).width + 24 * s, th = 22 * s;
  rrect(c, x - tw / 2, y - th, tw, th, th / 2, 'rgba(14,19,34,.82)'); c.fillStyle = col; c.beginPath(); c.arc(x - tw / 2 + 11 * s, y - th / 2, 3.4 * s, 0, 7); c.fill();
  c.fillStyle = '#EEF2FF'; c.textAlign = 'left'; c.textBaseline = 'middle'; c.fillText(text, x - tw / 2 + 19 * s, y - th / 2 + .5); c.restore();
}

/* ---------------- immagini ---------------- */
var IMG = {};
function loadImg(key, url, alt) {
  var im = new Image(); IMG[key] = im; im.onerror = function () { if (alt && !im._alt) { im._alt = 1; im.src = alt; } }; im.src = url; return im;
}
function ready(key) { var im = IMG[key]; return im && im.complete && im.naturalWidth > 0 ? im : null; }
var NAMES = ['academia', 'archivio', 'laboratorio', 'fucina', 'arena', 'fontana', 'pg1', 'pg2'];
function loadAll() {
  loadImg('mappa', IMGDIR + 'mappa.jpg', IMGDIR + 'mappa.png');
  NAMES.forEach(function (n) { loadImg(n, IMGDIR + 'edifici/' + n + '.png'); });
}

/* ---------------- disegno del mondo ----------------
   Coordinate in pixel della mappa (2752 x 1536). Ogni edificio e' un progetto e ha la sua piazza.
   (x, y) = centro del bordo basso dell'edificio. */
var PERSON_H = 30; /* altezza di un personaggio sulla mappa, in pixel: tutte le altre misure ne derivano */
var ACADEMY = { x: 1560, y: 705, w: 430 };
var BUILDINGS = [
  { name: 'laboratorio', x: 764, y: 510, w: 200, zone: 'lab', pref: /candidatur|cv|lavor/i },
  { name: 'archivio', x: 2140, y: 445, w: 180, zone: 'archivio', pref: /timelive|time/i },
  { name: 'fucina', x: 633, y: 955, w: 160, zone: 'fucina', pref: /mercatin|mercato/i },
  { name: 'arena', x: 2215, y: 1335, w: 780, zone: 'locanda', flat: true },
  { name: 'fontana', x: 2435, y: 830, w: 115, zone: 'archivio' }
];
var objs = [], villages = [], agents = {};
var W = { sig: '', built: false };
var cam = { x: MAPW / 2, y: MAPH / 2, z: .5, tx: null, ty: null, tz: null, userMoved: false };
var env = { cat: 'sereno', temp: null, city: '', hour: 12 }, nightF = 0, sunF = 1;
var parts = [], rain = [], flash = 0, flashT = 6, tShow = 0, started = false, lastT = 0, sizeW = 0, sizeH = 0;
var root, cv, ctx, tip, hud, hover = null, tasksNow = [];
var WEATHER_ON = false; /* meteo e notte spenti: sempre giorno */

function dimOf(o) { var im = ready(o.img); if (!im) return null; var w = o.w, h = w * im.naturalHeight / im.naturalWidth; return { w: w, h: h, im: im }; }

function rebuildWorld(dips) {
  objs = []; villages = [];
  objs.push({ id: '_cmd', img: 'academia', x: ACADEMY.x, y: ACADEMY.y, w: ACADEMY.w, key: ACADEMY.y, zone: 'cmd', lights: [] });
  var free = BUILDINGS.slice(), pairs = [];
  dips.slice(0, 5).forEach(function (d) { var i = free.findIndex(function (b) { return b.pref && b.pref.test(d.nome + ' ' + d.id); }); if (i >= 0) pairs.push([d, free.splice(i, 1)[0]]); else pairs.push([d, null]); });
  pairs.forEach(function (pr) { if (!pr[1]) pr[1] = free.shift(); });
  BUILDINGS.forEach(function (b) {
    var pr = pairs.filter(function (q) { return q[1] === b; })[0], v = { id: pr ? pr[0].id : null, dep: pr ? pr[0] : null, b: b };
    var o = { id: v.id, vill: v, img: b.name, x: b.x, y: b.y, w: b.w, zone: b.zone, flat: b.flat, key: b.y - (b.flat ? 500 : 0), lights: [] };
    v.o = o; objs.push(o); if (pr) villages.push(v);
  });
  objs.sort(function (a, b) { return a.key - b.key; });
}
function countsOf(v) { var c = {}; tasksNow.forEach(function (t) { if (t.dip === v.id) c[t.stato] = (c[t.stato] || 0) + 1; }); return c; }
var PRI = { bloccato: 0, da_approvare: 0, fallito: 1, incompleto: 1, in_corso: 2, in_coda: 3, completato: 4 };
function areaOf(v) {
  var o = v.o, d = dimOf(o); if (!d) return null;
  if (o.flat) return { cx: o.x, cy: o.y - d.h * .42, rx: d.w * .3, ry: d.h * .16 };
  return { cx: o.x, cy: o.y + 24, rx: Math.max(40, d.w * .55), ry: 11 };
}
function rndIn(ar) { var a = Math.random() * 6.283, r = Math.sqrt(Math.random()); return [ar.cx + Math.cos(a) * ar.rx * r, ar.cy + Math.sin(a) * ar.ry * r]; }
function syncAgents(tasks) {
  tasksNow = tasks || []; var keep = {};
  villages.forEach(function (v) {
    var list = tasksNow.filter(function (t) { return t.dip === v.id; }).sort(function (x, y) { return (PRI[x.stato] || 5) - (PRI[y.stato] || 5); }).slice(0, 4);
    list.forEach(function (t) {
      keep[t.id] = 1; var a = agents[t.id], ar = areaOf(v);
      if (!a || a.v !== v) { var h = hash(t.id), st = ar ? rndIn(ar) : [v.o.x, v.o.y]; a = agents[t.id] = { id: t.id, v: v, h: h, x: st[0], y: st[1], tx: null, ty: null, wt: Math.random() * 3, img: h % 2 ? 'pg1' : 'pg2', flip: false, ph: Math.random() * 6, moving: false }; }
      a.task = t;
    });
  });
  Object.keys(agents).forEach(function (k) { if (!keep[k]) delete agents[k]; });
}
function updateAgent(a, dt) {
  var ar = areaOf(a.v); if (!ar) return; a.moving = false;
  var wait = a.task.stato === 'bloccato' || a.task.stato === 'da_approvare';
  if (a.tx != null) {
    var dx = a.tx - a.x, dy = a.ty - a.y, dl = Math.hypot(dx, dy), sp = 17 * dt;
    if (dl <= sp) { a.x = a.tx; a.y = a.ty; a.tx = null; a.wt = wait ? 6 + Math.random() * 8 : 2 + Math.random() * 6; } else { a.x += dx / dl * sp; a.y += dy / dl * sp; a.flip = dx > 0; a.moving = true; }
    return;
  }
  a.wt -= dt; if (a.wt <= 0) { var p = rndIn(ar); a.tx = p[0]; a.ty = p[1]; }
}
function drawAgent(c, a) {
  var im = ready(a.img); if (!im) return; var h = PERSON_H, w = h * im.naturalWidth / im.naturalHeight, bob = a.moving ? Math.abs(Math.sin(tShow * 8 + a.ph)) * 1.4 : 0;
  c.fillStyle = 'rgba(10,25,5,.28)'; c.beginPath(); c.ellipse(a.x, a.y, w * .5, 2.6, 0, 0, 7); c.fill();
  c.save(); c.translate(a.x, a.y - bob); if (a.flip) c.scale(-1, 1); c.drawImage(im, -w / 2, -h, w, h); c.restore();
  var col = STATUS_COL[a.task.stato] || '#8793AC', y = a.y - h - 9 - Math.sin(tShow * 2.4 + a.ph) * 1.6;
  c.beginPath(); c.moveTo(a.x, y - 5); c.lineTo(a.x + 3.4, y); c.lineTo(a.x, y + 5); c.lineTo(a.x - 3.4, y); c.closePath(); c.fillStyle = col; c.fill(); c.strokeStyle = 'rgba(255,255,255,.85)'; c.lineWidth = 1; c.stroke();
  if (a.task.stato === 'bloccato' || a.task.stato === 'da_approvare') { c.fillStyle = '#FFF8E0'; c.beginPath(); c.arc(a.x + 10, y - 3, 6, 0, 7); c.fill(); c.fillStyle = '#B07A10'; c.font = 'bold 9px sans-serif'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText('?', a.x + 10, y - 2.5); }
}

/* ---------------- luce e meteo ---------------- */
function hourNow() { if (env.hour != null) return env.hour; var n = new Date(); return n.getHours() + n.getMinutes() / 60; }
function sunAt(h) { return (h >= 6 && h <= 20) ? Math.max(0, Math.sin(Math.PI * (h - 6) / 14)) : 0; }
function lightsFor(z, w, h) {
  var out = [];
  function add(wx, wy, r, col, i, fl) { var sx = (wx - cam.x) * z + w / 2, sy = (wy - cam.y) * z + h / 2; if (sx < -r * z || sy < -r * z || sx > w + r * z || sy > h + r * z) return; out.push({ x: sx, y: sy, r: r * z, col: col, i: i, fl: fl }); }
  objs.forEach(function (o) { var d = dimOf(o); if (!d) return; var x0 = o.x - d.w / 2, y0 = o.y - d.h, s = o.zone === 'cmd' ? 1 : o.k; (o.lights || []).forEach(function (l) { add(x0 + l[0] * d.w, y0 + l[1] * d.h, l[2] * (o.zone === 'cmd' ? 1.15 : 1.05 * s), l[3], l[4], l[5]); }); });
  return out;
}
function drawCloudShadows(c, dt) {
  var n = env.cat === 'sereno' ? 3 : 8, al = (env.cat === 'sereno' ? .1 : .16) * (1 - nightF * .8);
  if (al < .01) return;
  c.save(); c.globalCompositeOperation = 'multiply';
  for (var i = 0; i < n; i++) { var s = 260 + (i * 97) % 220, px = ((tShow * (6 + i % 3 * 2) + i * 540) % (MAPW + 700)) - 350, py = 160 + (i * 311) % (MAPH - 300), g = c.createRadialGradient(px, py, 10, px, py, s); g.addColorStop(0, 'rgba(70,80,100,' + (al * 3) + ')'); g.addColorStop(1, 'rgba(70,80,100,0)'); c.fillStyle = g; c.fillRect(px - s, py - s, s * 2, s * 2); }
  c.restore();
}

/* ---------------- camera ---------------- */
function minZoom() { return Math.max(sizeW / MAPW, sizeH / MAPH); }
function clampCam() {
  var z = cam.z = clamp(cam.z, minZoom(), 2.4), hw = sizeW / 2 / z, hh = sizeH / 2 / z;
  cam.x = clamp(cam.x, hw, MAPW - hw); cam.y = clamp(cam.y, hh, MAPH - hh);
}
function focusTo(x, y, z, instant) { if (instant) { cam.x = x; cam.y = y; cam.z = z; cam.tx = cam.ty = cam.tz = null; clampCam(); } else { cam.tx = x; cam.ty = y; cam.tz = z; } }
function fitCamera(instant) { focusTo(MAPW / 2, MAPH / 2, minZoom(), instant); }
function resize() {
  var r = root.getBoundingClientRect(), w = Math.max(300, r.width), h = Math.max(300, r.height);
  if (w === sizeW && h === sizeH) return; sizeW = w; sizeH = h; cv.width = Math.round(w * DPR); cv.height = Math.round(h * DPR); cv.style.width = w + 'px'; cv.style.height = h + 'px';
  if (!cam.userMoved) fitCamera(true); else clampCam();
}
Mondo.focus = function (id) {
  cam.userMoved = true;
  if (id === '_cmd') return focusTo(ACADEMY.x, ACADEMY.y - 230, clamp(Math.min(sizeW / 760, sizeH / 600), minZoom(), 2.4), false);
  var v = villages.filter(function (q) { return q.id === id; })[0]; if (!v) return;
  focusTo(v.o.x, v.o.y - 90, clamp(Math.min(sizeW / (v.o.w + 420), sizeH / 520), minZoom(), 2.4), false);
};
Mondo.reset = function () { cam.userMoved = false; fitCamera(false); };

/* ---------------- ciclo di disegno ---------------- */
var _ov = null; function overlay(w, h) { if (!_ov) _ov = document.createElement('canvas'); if (_ov.width !== Math.round(w) || _ov.height !== Math.round(h)) { _ov.width = Math.round(w); _ov.height = Math.round(h); } return _ov; }
function drawObj(c, o) {
  var d = dimOf(o); if (!d) return; c.drawImage(d.im, o.x - d.w / 2, o.y - d.h, d.w, d.h);
}
function frame(now) {
  requestAnimationFrame(frame);
  if (document.hidden || !W.built) { lastT = now; return; }
  var dt = Math.min(.1, (now - lastT) / 1000); lastT = now; if (dt <= 0) return; tShow += dt;
  resize();
  var h24 = hourNow(); sunF = sunAt(h24); nightF = 1 - smooth(.02, .4, sunF);
  if (cam.tx != null) { var k = 1 - Math.pow(.0012, dt); cam.x += (cam.tx - cam.x) * k; cam.y += (cam.ty - cam.y) * k; cam.z += (cam.tz - cam.z) * k; if (Math.abs(cam.tx - cam.x) < .5 && Math.abs(cam.tz - cam.z) < .002) cam.tx = null; }
  clampCam();


  for (var i = parts.length - 1; i >= 0; i--) { var p = parts[i]; p.life -= dt; if (p.life <= 0) { parts.splice(i, 1); continue; } p.z += (p.vz || 0) * dt; p.x += (p.vx || 0) * dt; if (p.k === 'spark') p.vz -= 40 * dt; }

  var c = ctx, w = sizeW, h = sizeH, z = cam.z; c.setTransform(DPR, 0, 0, DPR, 0, 0);
  c.fillStyle = '#2d4a2a'; c.fillRect(0, 0, w, h);
  c.save(); c.translate(w / 2, h / 2); c.scale(z, z); c.translate(-cam.x, -cam.y);
  c.imageSmoothingEnabled = true; c.imageSmoothingQuality = 'high';
  var mp = ready('mappa'); if (mp) c.drawImage(mp, 0, 0, MAPW, MAPH); else { c.fillStyle = '#EEF2FF'; c.font = '600 28px system-ui,sans-serif'; c.textAlign = 'center'; c.fillText(IMG.mappa && IMG.mappa._alt ? 'Immagini non trovate: chiudi la finestra nera e riapri AVVIA_PANNELLO.bat' : 'Carico la mappa...', MAPW / 2, MAPH / 2); }

  Object.keys(agents).forEach(function (k) { updateAgent(agents[k], dt); });
  var list = objs.map(function (o) { return { k: o.key, f: function () { drawObj(c, o); } }; });

  Object.keys(agents).forEach(function (id) { var a = agents[id]; list.push({ k: a.y, f: function () { drawAgent(c, a); } }); });
  list.sort(function (a, b) { return a.k - b.k; }).forEach(function (it) { it.f(); });
  if (hover && hover.o) { var d = dimOf(hover.o); if (d) { c.strokeStyle = 'rgba(255,255,255,.55)'; c.lineWidth = 2 / z; c.setLineDash([6 / z, 5 / z]); c.strokeRect(hover.o.x - d.w / 2 + d.w * .06, hover.o.y - d.h + d.h * .06, d.w * .88, d.h * .9); c.setLineDash([]); } }

  parts.forEach(function (p) {
    var f = p.life / p.max, x = p.x, y = p.y - p.z;
    if (p.k === 'smoke') { c.fillStyle = 'rgba(205,205,210,' + (.45 * f) + ')'; c.beginPath(); c.arc(x, y, (p.r || 2) + (1 - f) * 9, 0, 7); c.fill(); }
    else if (p.k === 'spark') { c.fillStyle = 'rgba(255,200,90,' + f + ')'; c.fillRect(x, y, 1.8, 1.8); }
    else if (p.k === 'ember') { c.fillStyle = 'rgba(255,120,60,' + f + ')'; c.fillRect(x, y, 1.6, 1.6); }
    else if (p.k === 'zzz') { c.fillStyle = 'rgba(255,255,255,' + f + ')'; c.font = 'bold ' + (8 + (1 - f) * 5) + 'px sans-serif'; c.textAlign = 'center'; c.fillText('z', x, y); }
  });
  c.restore();
  var duskK = (1 - smooth(.04, .5, sunF)) * (1 - nightF);
  if (duskK > .02) { c.globalCompositeOperation = 'multiply'; c.fillStyle = 'rgba(255,150,90,' + (duskK * .22) + ')'; c.fillRect(0, 0, w, h); c.globalCompositeOperation = 'source-over'; }
  var ovCat = env.cat === 'sereno' ? 0 : (env.cat === 'temporale' ? .22 : .12);
  if (nightF > .02 || ovCat) {
    var ov = overlay(w, h), o2 = ov.getContext('2d'); o2.setTransform(1, 0, 0, 1, 0, 0); o2.clearRect(0, 0, ov.width, ov.height); o2.globalCompositeOperation = 'source-over';
    var na = clamp(nightF * .72 + ovCat * (1 - nightF * .5), 0, .8); o2.fillStyle = rgb(mix([120, 130, 150], theme.night, nightF), na); o2.fillRect(0, 0, ov.width, ov.height);
    var L = lightsFor(z, w, h);
    if (nightF > .03) { o2.globalCompositeOperation = 'destination-out'; L.forEach(function (l) { var fl = l.fl ? .85 + .15 * Math.sin(tShow * 9 + l.x) : 1, g = o2.createRadialGradient(l.x, l.y, 0, l.x, l.y, l.r); g.addColorStop(0, 'rgba(0,0,0,' + (.95 * l.i * fl * nightF) + ')'); g.addColorStop(1, 'rgba(0,0,0,0)'); o2.fillStyle = g; o2.fillRect(l.x - l.r, l.y - l.r, l.r * 2, l.r * 2); }); }
    c.drawImage(ov, 0, 0, w, h);
    if (nightF > .03) { c.globalCompositeOperation = 'lighter'; L.forEach(function (l) { var fl = l.fl ? .85 + .15 * Math.sin(tShow * 9 + l.x) : 1, g = c.createRadialGradient(l.x, l.y, 0, l.x, l.y, l.r * .8); g.addColorStop(0, rgb(hex(l.col), .24 * l.i * fl * nightF)); g.addColorStop(1, rgb(hex(l.col), 0)); c.fillStyle = g; c.fillRect(l.x - l.r, l.y - l.r, l.r * 2, l.r * 2); }); c.globalCompositeOperation = 'source-over'; }
  }
  drawWeatherFront(c, w, h, dt);
  var s = clamp(z * 1.1, .75, 1.25);
  villages.forEach(function (v) {
    var d = dimOf(v.o); if (!d) return; var sx = (v.o.x - cam.x) * z + w / 2, top = (v.o.y - d.h - cam.y) * z + h / 2, bot = (v.o.y - cam.y) * z + h / 2;
    drawLabel(c, v.dep.nome, sx, top - 28 * s, v.dep.colore || '#7FA8FF', s);
    var bot = top, cn = countsOf(v), keys = Object.keys(STATUS_COL).filter(function (k) { return cn[k]; }), x = sx - (keys.length * 40 * s) / 2;
    keys.forEach(function (k) { c.save(); rrect(c, x, top - 24 * s, 36 * s, 20 * s, 10 * s, 'rgba(14,19,34,.85)'); c.fillStyle = STATUS_COL[k]; c.beginPath(); c.arc(x + 10 * s, top - 24 * s + 10 * s, 5 * s, 0, 7); c.fill(); c.fillStyle = '#EEF2FF'; c.font = '700 ' + Math.round(12 * s) + 'px system-ui,sans-serif'; c.textAlign = 'left'; c.textBaseline = 'middle'; c.fillText(cn[k], x + 19 * s, top - 24 * s + 10.5 * s); c.restore(); x += 40 * s; });
  });
  var cp = [(ACADEMY.x - cam.x) * z + w / 2, (ACADEMY.y - ACADEMY.w * .98 - cam.y) * z + h / 2]; drawLabel(c, 'Centro di comando', cp[0], cp[1], '#7FA8FF', s);
}

/* ---------------- mouse e tocco ---------------- */
function toWorld(sx, sy) { return [(sx - sizeW / 2) / cam.z + cam.x, (sy - sizeH / 2) / cam.z + cam.y]; }

function pick(sx, sy) {
  var wp = toWorld(sx, sy), best = null, bd = 20 / Math.max(.5, cam.z) + 6;

  if (best) return best;
  var bd = 18, best = null; Object.keys(agents).forEach(function (k) { var a = agents[k], dd = Math.hypot(a.x - wp[0], a.y - PERSON_H * .5 - wp[1]); if (dd < bd) { bd = dd; best = { type: 'agent', a: a }; } }); if (best) return best;
  for (var i = objs.length - 1; i >= 0; i--) {
    var o = objs[i], d = dimOf(o); if (!d) continue; var x0 = o.x - d.w / 2, y0 = o.y - d.h;
    if (wp[0] > x0 + d.w * .06 && wp[0] < x0 + d.w * .94 && wp[1] > y0 + d.h * .06 && wp[1] < y0 + d.h * .96) return { type: 'build', o: o, zone: o.zone };
  }

  return null;
}
function bindEvents() {
  var down = null;
  cv.addEventListener('mousedown', function (e) { down = { x: e.clientX, y: e.clientY, cx: cam.x, cy: cam.y, moved: false }; cam.tx = null; });
  window.addEventListener('mouseup', function (e) {
    if (!down) return; var d = down; down = null; cv.style.cursor = 'grab';
    if (!d.moved && e.target === cv) { var r = cv.getBoundingClientRect(), h = pick(e.clientX - r.left, e.clientY - r.top); if (h && h.type === 'agent' && Mondo.onSelect) Mondo.onSelect(h.a.id); else if (h && h.type === 'build' && (h.zone === 'cmd' || h.o.vill.dep) && Mondo.onCommand) Mondo.onCommand(); }
  });
  window.addEventListener('mousemove', function (e) {
    var r = cv.getBoundingClientRect();
    if (down) { var dx = e.clientX - down.x, dy = e.clientY - down.y; if (Math.abs(dx) + Math.abs(dy) > 4) { down.moved = true; cam.userMoved = true; cv.style.cursor = 'grabbing'; } if (down.moved) { cam.x = down.cx - dx / cam.z; cam.y = down.cy - dy / cam.z; clampCam(); tip.hidden = true; return; } }
    if (e.target !== cv) { tip.hidden = true; hover = null; return; }
    var h = pick(e.clientX - r.left, e.clientY - r.top); cv.style.cursor = h ? 'pointer' : 'grab'; hover = h && h.type === 'build' && (h.zone === 'cmd' || h.o.vill.dep) ? h : null;
    if (!h) { tip.hidden = true; return; }
    var html;
    if (h.type === 'agent') html = '<b>' + esc(h.a.task.nome) + '</b> · ' + esc(STATUS_LABEL[h.a.task.stato] || h.a.task.stato) + '<br><span>' + esc(h.a.task.titolo || '') + '</span>';
    else if (h.zone === 'cmd') html = '<b>Centro di comando</b><br><span>Clicca per aprire il pannello</span>';
    else { var vv = h.o.vill; if (!vv.dep) html = '<b>Libero</b><br><span>Nessun progetto qui</span>'; else { var cn = countsOf(vv), tx = Object.keys(cn).map(function (k) { return cn[k] + ' ' + (STATUS_LABEL[k] || k).toLowerCase(); }).join(', '); html = '<b>' + esc(vv.dep.nome) + '</b><br><span>' + (tx || 'nessun task') + '</span>'; } }
    tip.innerHTML = html; tip.hidden = false; tip.style.left = Math.min(r.width - 230, e.clientX - r.left + 14) + 'px'; tip.style.top = Math.min(r.height - 70, e.clientY - r.top + 14) + 'px';
  });
  cv.addEventListener('wheel', function (e) { e.preventDefault(); var r = cv.getBoundingClientRect(), sx = e.clientX - r.left, sy = e.clientY - r.top, before = toWorld(sx, sy); cam.z = clamp(cam.z * Math.exp(-e.deltaY * .0013), minZoom(), 2.4); cam.tx = null; var after = toWorld(sx, sy); cam.x += before[0] - after[0]; cam.y += before[1] - after[1]; cam.userMoved = true; clampCam(); }, { passive: false });
  var pinch = null, td = null;
  cv.addEventListener('touchstart', function (e) { cam.tx = null; if (e.touches.length === 1) td = { x: e.touches[0].clientX, y: e.touches[0].clientY, cx: cam.x, cy: cam.y, moved: false }; if (e.touches.length === 2) pinch = { d: Math.hypot(e.touches[0].clientX - e.touches[1].clientX, e.touches[0].clientY - e.touches[1].clientY), z: cam.z }; }, { passive: true });
  cv.addEventListener('touchmove', function (e) { e.preventDefault(); if (e.touches.length === 2 && pinch) { cam.z = pinch.z * Math.hypot(e.touches[0].clientX - e.touches[1].clientX, e.touches[0].clientY - e.touches[1].clientY) / pinch.d; cam.userMoved = true; clampCam(); } else if (td && e.touches.length === 1) { var dx = e.touches[0].clientX - td.x, dy = e.touches[0].clientY - td.y; if (Math.abs(dx) + Math.abs(dy) > 6) { td.moved = true; cam.userMoved = true; } if (td.moved) { cam.x = td.cx - dx / cam.z; cam.y = td.cy - dy / cam.z; clampCam(); } } }, { passive: false });
  cv.addEventListener('touchend', function () { pinch = null; td = null; });
}

/* ---------------- barra in basso e API ---------------- */
function rebuildHud() {
  if (!hud) return;
  var h = '<button type="button" data-f="">Tutto</button><button type="button" data-f="_cmd">Centro</button>';
  villages.forEach(function (v) { h += '<button type="button" data-f="' + esc(v.id) + '"><i style="background:' + esc(v.dep.colore || '#7FA8FF') + '"></i>' + esc(v.dep.nome) + '</button>'; });
  hud.innerHTML = h;
  Array.prototype.forEach.call(hud.querySelectorAll('button'), function (b) { b.onclick = function () { var f = b.getAttribute('data-f'); if (f) Mondo.focus(f); else Mondo.reset(); }; });
}
function injectCss() {
  if (document.getElementById('mondoCss')) return; var s = document.createElement('style'); s.id = 'mondoCss';
  s.textContent = '.mondo-root{position:absolute;inset:0;overflow:hidden;background:#2d4a2a}.mondo-root canvas{display:block;touch-action:none;cursor:grab}.m-tip{position:absolute;max-width:220px;pointer-events:none;background:rgba(14,19,34,.92);color:#EEF2FF;border:1px solid rgba(255,255,255,.14);border-radius:8px;padding:6px 9px;font:12px/1.35 system-ui,sans-serif;z-index:5}.m-tip span{color:#AEB8D6}.m-hud{position:absolute;left:50%;bottom:14px;transform:translateX(-50%);display:flex;gap:6px;flex-wrap:wrap;justify-content:center;max-width:70%;z-index:4}.m-hud button{background:rgba(14,19,34,.82);color:#EEF2FF;border:1px solid rgba(255,255,255,.16);border-radius:99px;padding:6px 13px;font:600 12px system-ui,sans-serif;cursor:pointer;display:flex;gap:6px;align-items:center;backdrop-filter:blur(6px)}.m-hud button:hover{background:rgba(40,50,86,.92)}.m-hud i{width:9px;height:9px;border-radius:50%;display:inline-block}';
  document.head.appendChild(s);
}
Mondo.registerTheme = function () { };
Mondo.themes = function () { return [{ id: 'campagna', nome: 'Campagna', citta: '' }]; };
Mondo.has = function (id) { return id === 'campagna'; };
Mondo.setWeather = function (w) { if (WEATHER_ON && w) { env.cat = w.cat || 'sereno'; env.temp = w.temp; env.hour = w.hour; env.city = w.city || ''; } };
Mondo.sync = function (opts) {
  root = opts.root; injectCss();
  if (!cv || cv.parentNode !== root) {
    root.innerHTML = ''; root.classList.add('mondo-root'); cv = document.createElement('canvas'); ctx = cv.getContext('2d'); root.appendChild(cv);
    tip = document.createElement('div'); tip.className = 'm-tip'; tip.hidden = true; root.appendChild(tip);
    hud = document.createElement('div'); hud.className = 'm-hud'; root.appendChild(hud); bindEvents(); sizeW = 0; W.sig = ''; loadAll();
  }
  var sig = opts.dips.slice(0, 6).map(function (d) { return d.id + ':' + d.nome + ':' + d.colore; }).join('|');
  if (sig !== W.sig) { W.sig = sig; rebuildWorld(opts.dips); rebuildHud(); }
  if (opts.weather) Mondo.setWeather(opts.weather);
  syncAgents(opts.tasks);
  W.built = true; resize();
  if (!started) { fitCamera(true); lastT = performance.now(); requestAnimationFrame(frame); started = true; }
  return true;
};
})();

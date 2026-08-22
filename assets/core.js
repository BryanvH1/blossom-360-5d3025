/* Blossom 360 — codec + scoring engine. Shared by the form and the console. */
(function (global) {
  'use strict';
  var D = global.B360_DATA;
  var PREFIX = 'B360-1.';

  /* ---------- base64url helpers (UTF-8 safe) ---------- */
  function b64enc(str) {
    var bytes = new TextEncoder().encode(str), bin = '';
    for (var i = 0; i < bytes.length; i++) bin += String.fromCharCode(bytes[i]);
    return btoa(bin).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
  }
  function b64dec(s) {
    s = String(s).replace(/-/g, '+').replace(/_/g, '/');
    while (s.length % 4) s += '=';
    var bin = atob(s), bytes = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    return new TextDecoder().decode(bytes);
  }
  /* short checksum so a truncated paste fails loudly instead of silently */
  function checksum(str) {
    var h = 5381;
    for (var i = 0; i < str.length; i++) { h = ((h << 5) + h + str.charCodeAt(i)) >>> 0; }
    return h.toString(36).slice(-4).padStart(4, '0');
  }

  /* scores object -> fixed 30-char string, '-' for not observed */
  function packScores(scores) {
    return D.items.map(function (it) {
      var v = scores[it.code];
      return (v >= 1 && v <= 5) ? String(v) : '-';
    }).join('');
  }
  function unpackScores(s) {
    var out = {};
    D.items.forEach(function (it, i) {
      var ch = s.charAt(i);
      if (ch >= '1' && ch <= '5') out[it.code] = parseInt(ch, 10);
    });
    return out;
  }

  function encode(resp) {
    var payload = {
      e: resp.evaluee, r: resp.rater, l: resp.relationship,
      d: resp.date, s: packScores(resp.scores), o: resp.open || []
    };
    var body = b64enc(JSON.stringify(payload));
    return PREFIX + body + '.' + checksum(body);
  }

  function decode(text) {
    var raw = String(text || '').trim().replace(/\s+/g, '');
    if (!raw) throw new Error('Nothing pasted.');
    var i = raw.indexOf(PREFIX);
    if (i === -1) throw new Error('That does not look like a response code — it should start with "' + PREFIX + '".');
    raw = raw.slice(i);
    var parts = raw.split('.');
    if (parts.length < 3) throw new Error('The code looks incomplete. Ask for the whole block to be re-sent.');
    var body = parts[1], sum = parts[2];
    if (checksum(body) !== sum) throw new Error('This code is damaged or was cut short in transit — ask for it to be re-sent, or pasted as plain text.');
    var p;
    try { p = JSON.parse(b64dec(body)); }
    catch (e) { throw new Error('Could not read the code. It may have been altered after it was copied.'); }
    if (!p.e || !p.r || !p.l || typeof p.s !== 'string' || p.s.length !== D.items.length) {
      throw new Error('The code is missing information — it may be from an older version of the form.');
    }
    return {
      evaluee: p.e, rater: p.r, relationship: p.l, date: p.d || '',
      scores: unpackScores(p.s), open: p.o || [],
      id: p.e + '|' + p.r + '|' + p.l + '|' + (p.d || '')
    };
  }

  /* ---------- scoring ---------- */
  function mean(a) { return a.length ? a.reduce(function (x, y) { return x + y; }, 0) / a.length : null; }
  function r2(v) { return v === null ? null : Math.round(v * 100) / 100; }

  /** responses: array for ONE evaluee. Returns full computed model. */
  function score(responses) {
    var self = responses.filter(function (r) { return r.relationship === 'self'; });
    var mgr = responses.filter(function (r) { return r.relationship === 'manager'; });
    var peer = responses.filter(function (r) { return r.relationship === 'peer'; });
    var others = mgr.concat(peer);

    var rows = D.items.map(function (it) {
      function vals(list) {
        return list.map(function (r) { return r.scores[it.code]; })
                   .filter(function (v) { return typeof v === 'number'; });
      }
      var selfV = mean(vals(self)), othersV = mean(vals(others));
      var row = {
        code: it.code, text: it.text, dim: it.dim, importance: it.importance,
        self: r2(selfV), mgr: r2(mean(vals(mgr))), peer: r2(mean(vals(peer))),
        others: r2(othersV),
        blind: (selfV !== null && othersV !== null) ? r2(selfV - othersV) : null,
        gap: othersV !== null ? r2(it.importance * (5 - othersV)) : null,
        perRater: responses.map(function (r) { return r.scores[it.code]; })
      };
      return row;
    });

    /* Rank by gap desc. Ties are common with few raters and whole-number scores, so the
       tie-break is explicit and identical to the workbook's:
         gap -> importance (the role needs it more) -> blind spot -> item order.
       Anything still tied at the cut line is a judgement call, and the console says so. */
    var order = D.items.map(function (it) { return it.code; });
    function key(r) {
      return Math.round(r.gap * 100) * 1e6
           + r.importance * 1e5
           + Math.round(Math.max(0, r.blind === null ? 0 : r.blind) * 100) * 1e2
           + (order.length - order.indexOf(r.code));
    }
    var ranked = rows.filter(function (r) { return r.gap !== null; }).slice()
      .sort(function (a, b) { return key(b) - key(a); });
    ranked.forEach(function (r, i) { r.rank = i + 1; });
    /* how many items sit at the same gap as the 5th, i.e. contested for the last slot */
    var cut = ranked[4] ? ranked[4].gap : null;
    var tiedAtCut = cut === null ? 0 : ranked.filter(function (r) { return r.gap === cut; }).length;

    var dims = D.dimensions.map(function (d) {
      var sub = rows.filter(function (r) { return r.dim === d.code; });
      function avg(key) { return r2(mean(sub.map(function (r) { return r[key]; }).filter(function (v) { return v !== null; }))); }
      var s = avg('self'), o = avg('others');
      return {
        code: d.code, name: d.name, question: d.question,
        self: s, mgr: avg('mgr'), peer: avg('peer'), others: o,
        pct: o === null ? null : o / 5,
        blind: (s !== null && o !== null) ? r2(s - o) : null
      };
    });
    function overallOf(key) { return r2(mean(dims.map(function (d) { return d[key]; }).filter(function (v) { return v !== null; }))); }
    var os = overallOf('self'), oo = overallOf('others');
    var overall = {
      code: '', name: 'OVERALL', self: os, mgr: overallOf('mgr'), peer: overallOf('peer'),
      others: oo, pct: oo === null ? null : oo / 5,
      blind: (os !== null && oo !== null) ? r2(os - oo) : null
    };

    var blindSpots = rows.filter(function (r) { return r.blind !== null; })
      .slice().sort(function (a, b) { return b.blind - a.blind || (a.code < b.code ? -1 : 1); });

    return {
      rows: rows, ranked: ranked, top5: ranked.slice(0, 5), dims: dims, overall: overall,
      blindSpots: blindSpots,
      counts: { self: self.length, manager: mgr.length, peer: peer.length, total: responses.length },
      tie: { gap: cut, count: tiedAtCut, contested: ranked.filter(function (r) { return r.gap === cut; }).map(function (r) { return r.code; }) },
      responses: responses
    };
  }

  function band(v) { if (v === null || v === undefined) return ''; return v < 3 ? 'b-red' : (v < 4 ? 'b-amb' : 'b-grn'); }
  function fmt(v, dp) { return (v === null || v === undefined) ? '—' : Number(v).toFixed(dp === undefined ? 2 : dp); }
  function signed(v) { return (v === null || v === undefined) ? '—' : (v > 0 ? '+' : '') + Number(v).toFixed(2); }

  global.B360 = {
    PREFIX: PREFIX, encode: encode, decode: decode, score: score,
    band: band, fmt: fmt, signed: signed, packScores: packScores, checksum: checksum
  };
})(window);

/* ============================================================
   Marque Publishing — Self-Publishing Cost Calculator
   KDP 2026 US (Amazon.com) paperback print-cost model.
   Source: https://kdp.amazon.com/en_US/help/topic/G201834340
   ============================================================ */

const ROYALTY = 0.60; // KDP standard paperback royalty rate

// Returns { cost } printing cost per book in USD, or { error }.
function printCost(pages, ink, trim) {
  pages = Math.round(pages);
  const reg = trim === 'reg';
  if (ink === 'bw') {
    if (pages < 24)  return { error: 'Black & white books need at least 24 pages.' };
    if (pages > 828) return { error: 'Maximum is 828 pages.' };
    if (pages <= 110) return { cost: reg ? 2.30 : 2.84 };            // flat, no per-page
    return { cost: 1.00 + pages * (reg ? 0.012 : 0.017) };
  }
  if (ink === 'std') { // standard color, 72–600 pages
    if (pages < 72)  return { error: 'Standard color needs at least 72 pages. Try premium color for shorter books.' };
    if (pages > 600) return { error: 'Standard color tops out at 600 pages. Try premium color.' };
    return { cost: 1.00 + pages * (reg ? 0.0255 : 0.0402) };
  }
  // premium color
  if (pages < 24)  return { error: 'Premium color books need at least 24 pages.' };
  if (pages > 828) return { error: 'Maximum is 828 pages.' };
  if (pages <= 40) return { cost: reg ? 3.60 : 4.20 };              // flat, no per-page
  return { cost: 1.00 + pages * (reg ? 0.065 : 0.08) };
}

// --- helpers ---------------------------------------------------
const $ = id => document.getElementById(id);
const round2 = n => Math.round(n * 100) / 100;
const money = n => '$' + n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const money0 = n => '$' + Math.round(n).toLocaleString('en-US');
const whole = n => n.toLocaleString('en-US');

const inkLabel = { bw: 'black & white', std: 'standard color', prem: 'premium color' };
const UPFRONT_IDS = ['ed', 'cover', 'fmt', 'isbn', 'mktg', 'other'];

let mode = 'pod';

function upfrontTotal() {
  return UPFRONT_IDS.reduce((sum, id) => sum + (+$(id).value || 0), 0);
}

function setMode(m) {
  mode = m;
  $('m-pod').classList.toggle('active', m === 'pod');
  $('m-run').classList.toggle('active', m === 'run');
  $('m-pod').setAttribute('aria-selected', m === 'pod');
  $('m-run').setAttribute('aria-selected', m === 'run');
  $('copies-label').textContent = m === 'pod'
    ? 'How many copies do you expect to sell?'
    : 'How many copies will you print?';
  $('res-title').textContent = m === 'pod' ? 'If You Sell on Amazon' : 'If You Print & Sell Them Yourself';
  calc();
}

// Build one line of the worked calculation.
function step(op, label, value, kind) {
  return `<div class="step ${kind || ''}">
            <span class="op">${op || ''}</span>
            <span class="step-label">${label}</span>
            <span class="step-val">${value}</span>
          </div>`;
}

function calc() {
  const pages   = +$('pages').value || 0;
  const ink     = $('ink').value;
  const trim    = $('trim').value;
  const price   = +$('price').value || 0;
  const copies  = Math.max(0, Math.round(+$('copies').value || 0));
  const invest  = round2(upfrontTotal());
  const note = $('note');
  note.className = 'note';

  // live subtotal in the up-front card
  $('invest-total').textContent = money0(invest);

  const pc = printCost(pages, ink, trim);
  if (pc.error) {
    $('results').innerHTML = '';
    note.className = 'note warn';
    note.textContent = pc.error;
    return;
  }
  const cost = round2(pc.cost);
  const inkTxt = inkLabel[ink];
  let html = '';

  if (mode === 'pod') {
    const amazonShare = round2(price * (1 - ROYALTY));      // 40%
    const perBook = round2(price - amazonShare - cost);     // your share
    const royalties = round2(perBook * copies);
    const net = round2(royalties - invest);

    html += step('',  'Sale price (what the reader pays)', money(price), 'lead');
    html += step('&ndash;', `Amazon&rsquo;s share (40% of the sale price)`, money(amazonShare));
    html += step('&ndash;', `Printing cost (${whole(Math.round(pages))} pages, ${inkTxt})`, money(cost));
    html += step('=', 'Your share per book', money(perBook), perBook < 0 ? 'sub neg' : 'sub');
    html += step('&times;', 'Copies sold', whole(copies));

    if (invest > 0) {
      html += step('=', 'Royalties from sales', money0(royalties), royalties < 0 ? 'sub neg' : 'sub');
      html += step('&ndash;', 'Your up-front investment', money0(invest));
      html += step('=', 'Your net profit', money0(net), net < 0 ? 'total neg' : 'total');
      if (perBook > 0) {
        const be = Math.ceil(invest / perBook);
        html += step('&raquo;', 'Copies sold to recoup your investment',
          whole(be) + (be > copies ? ' (more than you expect to sell)' : ''),
          be > copies ? 'be neg' : 'be');
      }
    } else {
      html += step('=', 'Your total earnings', money0(royalties), royalties < 0 ? 'total neg' : 'total');
    }
    $('results').innerHTML = html;

    const minPrice = round2(cost / ROYALTY);
    if (perBook < 0) {
      note.className = 'note warn';
      note.innerHTML = `Your sale price is too low to cover printing. Amazon&rsquo;s minimum list price for this book would be about <strong>${money(minPrice)}</strong>.`;
    } else {
      note.innerHTML = `Amazon keeps 40% of the sale price and charges you to print each copy &mdash; with no money down. Your up-front investment is what you spend before the first sale. Minimum sale price for this book: about <strong>${money(minPrice)}</strong>.`;
    }
  } else {
    const perBook = round2(price - cost);          // profit per book
    const printBill = round2(cost * copies);
    const totalCost = round2(printBill + invest);
    const total = round2(price * copies - totalCost);

    html += step('',  'Sale price (what the reader pays)', money(price), 'lead');
    html += step('&ndash;', `Printing cost per book (${whole(Math.round(pages))} pages, ${inkTxt})`, money(cost));
    html += step('=', 'Your profit per book', money(perBook), perBook < 0 ? 'sub neg' : 'sub');
    html += step('',  'Up-front to print them all', money0(printBill), 'group');
    if (invest > 0) html += step('+', 'Your up-front investment (editing, cover&hellip;)', money0(invest));
    html += step('=', 'Total up-front cost', money0(totalCost), 'sub');
    if (perBook > 0) {
      const be = Math.ceil(totalCost / price);
      html += step('&raquo;', 'Copies you must sell to break even',
        whole(be) + (be > copies ? ' (more than you printed)' : ''),
        be > copies ? 'be neg' : 'be');
    }
    html += step('=', `Total profit if you sell all ${whole(copies)}`, money0(total), total < 0 ? 'total neg' : 'total');
    $('results').innerHTML = html;

    if (perBook < 0) {
      note.className = 'note warn';
      note.innerHTML = 'Each copy costs more to print than your sale price &mdash; you&rsquo;d lose money on every book.';
    } else {
      note.innerHTML = 'You pay to print the copies and cover your up-front costs first, then keep the full sale price on each one you sell. Printing uses KDP&rsquo;s author-copy cost; a bulk offset printer can be cheaper at high volumes.';
    }
  }
}

['pages', 'ink', 'trim', 'price', 'copies', ...UPFRONT_IDS].forEach(id => {
  $(id).addEventListener('input', calc);
});
setMode('pod');

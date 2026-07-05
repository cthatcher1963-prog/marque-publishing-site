# Self-Publishing Cost Calculator

A free tool for the Marque Publishing site. A visitor enters their book details and
sees, step by step, what self-publishing would cost and what they'd earn. It doubles
as a soft advertisement for Marque's publishing services.

Lives at: `/calculator/` (e.g. https://www.marquepublishing.com/calculator/).

## Files

- `index.html` — markup and copy.
- `calculator.css` — styling. Self-contained; mirrors the site palette (ink / brass /
  oxblood / paper) and supports dark mode, so the folder renders correctly on its own.
- `calculator.js` — all the logic and the KDP print-cost math.

Just three files, no build step. Open `index.html` to run it.

## The two modes

**Sell on Amazon (print-on-demand).** No money down. Amazon keeps 40% of the sale
price and charges a per-book printing cost; you keep the rest as royalty.

**Print & sell yourself.** You pay to print copies up front, then keep the full sale
price on each one you sell. Shows the up-front bill and the break-even point.

## The math (KDP 2026, US / Amazon.com, paperback)

Printing cost = fixed cost + (page count x per-page cost):

| Interior        | Pages      | Regular trim          | Large trim            |
|-----------------|------------|-----------------------|-----------------------|
| Black & white   | 24–110     | $2.30 flat            | $2.84 flat            |
| Black & white   | 110–828    | $1.00 + $0.012/pg     | $1.00 + $0.017/pg     |
| Standard color  | 72–600     | $1.00 + $0.0255/pg    | $1.00 + $0.0402/pg    |
| Premium color   | 24–40      | $3.60 flat            | $4.20 flat            |
| Premium color   | 42–828     | $1.00 + $0.065/pg     | $1.00 + $0.08/pg      |

Paperback royalty rate: **60%** of the sale price, minus the printing cost.
Minimum sale price = printing cost / 0.60.

Verified against KDP's own published examples (e.g. a 300-page B&W regular paperback
prints for exactly $4.60).

Source: https://kdp.amazon.com/en_US/help/topic/G201834340

> All figures are estimates for the US marketplace. Update the rates in `calculator.js`
> (the `printCost` function and `ROYALTY` constant) if KDP changes its pricing.

## Adding it to the site

Link to it from the nav and/or the Labs page, for example:

```html
<a href="/calculator/">Publishing Cost Calculator</a>
```

To embed it inside an existing page instead of linking out, copy the `.calc-wrap`
block from `index.html` and the contents of `calculator.css` / `calculator.js`
into that page.

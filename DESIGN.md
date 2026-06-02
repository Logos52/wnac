# WNAC — Design language (reverse-engineered from Copilot Money)

Source: a real Copilot Money dashboard screenshot, pixel-sampled 2026-06-01 (see `tokens.css` for the
extracted values, tagged exact/approx). Dark is the **primary** theme — it is Copilot's signature.

## The feel in one paragraph
Near-black navy canvas (`--surface-base #000610`) with cards that are *barely* lighter
(`--surface-card #010E21`) — depth comes from a hair of border + soft shadow, not big contrast.
Cool-white text on near-black. One calm blue accent. Color is **reserved for data**: a vivid
green/amber/orange/red pace scale and a small set of category hues. Generous padding, big rounded
corners (~20px), heavy large numerals. It reads premium because it's *restrained* — most of the
screen is dark, and color means something.

## Signature patterns (these are the "sight")
1. **Follow-the-line (monthly spending).** A thick spending line whose **color is a gradient along its
   length by pace** — red where overspending, green where under — with a dashed trend baseline and an
   end **callout pill** ("$100 under" in green). This is the hero. Portable: SVG path + gradient stroke.
2. **Pace everywhere.** The same green→amber→orange→red scale colors category progress bars, the line,
   and badges — always meaning "vs where you should be." One shared `paceToken()` function (PRD §7.4.2).
3. **Chip tags.** Category labels are small pills: a **dark-tinted background of the category's own hue**
   + a **vivid UPPERCASE label** + an emoji (e.g. teal bg + cyan "SUBSCRIPTIONS", magenta bg + pink
   "SHOPS"). Same recipe for +/-% badges (dark green/red tint + colored arrow + number).
4. **Net worth = dual lines.** Assets (blue `--accent-bright`) and Debts (coral `--debt-coral`) as two
   horizontal lines with end nodes, plus a range selector row (1W/1M/3M/YTD/1Y/ALL) as pills, active = soft pill.
5. **Category rows.** emoji + name + spent + a pace-colored progress bar + budget cap, nestable (counts + carets).
6. **Active nav = filled blue pill** (`--accent`); inactive = icon + label in `--text-secondary`.
   Account list items = a colored dot + name + balance.

## Layout
- Left sidebar (dark `--surface-sidebar`, ~13–14% width): search, primary nav, grouped account lists, footer (Explore/Help/Settings).
- Main = a 2×2 grid of rounded cards with `--gap-grid` between. For WNAC (single screen, PRD §7.4.3):
  hero row (Net worth · Flex number · Pay-down dial), then Cash flow + AI insight, then Spending donut + recent transactions.

## Motion
- Dials/rings fill with `--ease-spring` over ~`--dur-ring`; big numbers count up over ~`--dur-count`.
- Standard transitions use `--ease-standard`. (Durations are sensible defaults — Copilot's exact easing
  isn't published; tune by eye.)

## Typography
- A clean grotesque sans (Copilot's is custom; **Inter** is the free near-match). Large heavy numerals
  (700), medium labels (500), uppercase tracked chips (600). Exact font/weights not pixel-detectable.

## Copilot feature surface (for scope decisions — not all in WNAC v1)
- **Track your Spending / Follow the Line** → adopt (the hero line). · **Cash Flow** → adopt (income vs spend).
- **Rollovers** → optional per-category, but WNAC leads with the flex number (rollover never moves the headline flex #).
- **Spot Subscriptions** (recurring detection) → P2 AI insight. 
- **Investments: Tickers, Allocation** → OUT for debt-first v1 (no holdings to track); the visual language
  (allocation donut, % breakdown) is reusable later if investment accounts get added.

---

## Component anatomy (per-card teardown from the screenshot)

> Surface/text/accent/pace/chip colors below reference the exact tokens in `tokens.css`. The few small
> sub-elements I could NOT pixel-sample (transaction avatars, category count-badges, expand carets) are
> flagged **[re-sample]** — re-save the screenshot to `refs/` and I'll nail their hex.

### Global chrome
- **Top bar** (on `--surface-base`, no fill): app glyph (paper-plane, accent) far left; muted icon buttons
  back / forward / refresh / sidebar-toggle in `--text-secondary`; page title ("Dashboard") in `--text-primary`.
- **Card header pattern** (every card): bold title left (`--text-primary`, ~600) + right-aligned **section
  link** "Name ›" in `--accent`. Card = `--surface-card`, `--radius-card`, generous padding, `--shadow-card`, hairline `--border-subtle`.
- **Grid:** multi-row, two cards per row (Monthly spending | Net worth · Transactions to review | Top categories · Next two weeks | …), `--gap-grid` gutters.

### Left sidebar (`--surface-sidebar`, ~13% width, full height)
- **Search**: rounded inset field, magnifier + "Search" placeholder in `--text-muted`.
- **Primary nav** (icon + label): **active** = filled `--accent` rounded-rect pill, white icon+label @600;
  **inactive** = outline icon + label in `--text-secondary`. (Dashboard · Transactions · Accounts · Investments · Categories · Recurrings.)
- **Account groups** = collapsible headers with ▼/▶ carets (`--text-secondary`). "Credit cards" expanded →
  rows of **[colored dot] name … [right-aligned balance]** (e.g. a checking account = blue dot, a credit card = red dot). "Depository" / "Investment" collapsed.
- **Footer** pinned to bottom: Explore · Get help · Settings (icon + label, `--text-secondary`).

### Monthly spending (hero)
- Header + "Transactions ›". Big "$1,000 spent" @700 + "$500 spent last month" in `--text-secondary`.
- **Follow-the-line**: a spending-trajectory line over a dashed **ideal/trend line**. **Color = signed distance
  from the dashed line at each x**, by how far:
    - line **ABOVE** the ideal (outspending the pace) → ramps **green → amber → red** with distance ⇒ the **peaks
      that poke above the dashed line render RED (overspending)**;
    - line **at/BELOW** the ideal (under pace) → **green** ⇒ the **valleys are green**.
  *(Correction: it's peaks=red / valleys=green — I had it inverted earlier.)*
  Ends green when you finish under budget; faint green area-fill under the green tail; a green **end-node** +
  a **callout pill** with the final delta ("$X under/over") in the end color. No axes.
  - Implementation: SVG polyline, each segment stroke = `lerp(green→amber→red, clamp((line_y − ideal_y)/scale))`;
    `line_y − ideal_y > 0` (above) warms toward red, `≤ 0` (below) stays green. Same green/amber/red as the pace tokens.

### Net worth
- Header + "Accounts ›". Two stat blocks: **• Assets** → "$100,000" + green up-badge "↗ 32%" (`--chip-green`);
  **• Debts** → "$5,000" + red down-badge "↙ 16%" (`--chip-red`). (Copilot tints the debt badge red regardless of direction — decide our own rule.)
- **Dual end-noded lines**: Assets in `--accent-bright`, Debts in `--debt-coral`, each with a filled circle node at the right.
- **Range pills**: 1W · 1M · 3M · **YTD (active)** · 1Y · ALL — active = soft filled pill (`--surface-card-alt`, `--text-primary`); rest plain `--text-secondary`.

### Transactions to review
- Header + "View all ›". **Date subheaders** (TODAY / YESTERDAY) = small uppercase, tracked, `--text-secondary`.
- **Row** = `[avatar] Merchant … [category chip] $amount`:
  - **Avatar = a ~38px circle / rounded-square** [re-sample]: real **brand logo** when known (Apple Music, Lyft,
    Target render their actual full-color mark on its own bg), else a colored circle with an initial. *Per-merchant colors, not the fixed palette.*
  - **Category chip** = dark-tinted-bg pill + vivid UPPERCASE label + emoji (SUBSCRIPTIONS teal · GROCERIES green ·
    TRANSPORTATION orange · ENTERTAINMENT purple · RESTAURANTS orange · SHOPS magenta — `tokens.css --chip-*`).
  - Amount right, `--text-primary`.
  - **Review state**: the row being reviewed swaps the avatar for a **checkbox** and gets a subtly highlighted row bg.
- Footer: **"✓ Mark N as reviewed"** pill button (`--surface-card-alt` bg, `--text-primary`).

### Top categories
- Header + "Categories ›". **Group row** = `[caret ▼/▶] [count-badge] emoji Name … $spent [pace bar on dark track] $cap`:
  - **Count-badge** [re-sample] = small rounded-square with a number, bg a category-hued vivid color (≈ violet/blue/green/orange).
  - **Progress bar** = rounded; filled portion `paceToken()`-colored (Groceries renders **red** — over its cap); track = `--surface-card-alt`; cap in `--text-secondary`.
  - **Expandable**: "Food & Drink" (▼) expands to **indented child rows** (Restaurants/Groceries/Coffee), each with
    emoji + spent + own pace bar + cap, joined by a vertical guide; collapsed groups (Necessities/Shopping/Fun, ▶) hide children.

### Next two weeks (bottom; mostly cut off in this shot)
- Only the header is visible: "Next two weeks" + "Recurrings ›". **Inferred** (cut off): an upcoming-14-days
  recurring/bills list, same row anatomy as Transactions-to-review (avatar + name + date/amount) showing predicted
  charges. **Confirm against a fuller screenshot.**

### Now sampled (exact) — added to `tokens.css`
- **Selected/review row**: bg `--row-selected-bg #071931`, checkbox ring `--checkbox-stroke #20324C`.
- **Progress bar track**: `--bar-track #172842` (fill = `paceToken()`).
- **Active range pill** (YTD): `--pill-active-bg #0D1F38`.
- **"Mark reviewed" button**: `--btn-subtle-bg #08182E`.
- **"$100 under" callout**: solid green `--callout-green #0AC34D` (white text).
- **Count-badge + caret system** (badge bg = dark hue tint, caret/number = vivid hue):
  Food&Drink **purple** (`#B36EF5` / bg `#1F2045`) · Necessities **green** (`#00BB36` / `#0D2B27`) ·
  Shopping **orange** (`#E66A37` / `#291E26`) · Fun **blue** (`#409DF8` / `#0D2749`).
- **Entertainment chip fg** refined exact to `#B36EF5`.

### Still open (need a different/fuller capture — not blocking)
- **Transaction avatars**: this mockup renders them minimally (only the selected row shows a checkbox). The
  rich per-merchant **brand-logo circles** are a real-app feature — they're brand marks, not a fixed palette,
  so WNAC's spec is "circular avatar container; brand logo if known, else colored initial."
- **Spend-line gradient stops**: line too thin to pixel-hit; it uses the **pace ramp** (red `#F3241A` → amber
  `#ED8001` → green `#0AC34D`), confirmed by the green end-node.
- **"Next two weeks" body** + the Transactions/Accounts/Investments screens: still off-frame — grab a scrolled/other-screen shot when convenient.

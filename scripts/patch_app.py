with open('d:/RR/dashboard/src/App.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

# Add num helper after export default function App() {
helper = '''export default function App() {
  const num = (v: any, d: number = 2): string => (v != null && !isNaN(Number(v))) ? Number(v).toFixed(d) : '—';'''

if 'const num = ' not in text:
    text = text.replace('export default function App() {', helper, 1)

# Safe replacements
text = text.replace('{target.ppr.toFixed(1)}', '{num(target?.ppr, 1)}')
text = text.replace('({normPpr.toFixed(1)})', '({num(normPpr, 1)})')
text = text.replace('{target.aor.toFixed(1)}', '{num(target?.aor, 1)}')
text = text.replace('{finalSrr.toFixed(2)}', '{num(finalSrr, 2)}')
text = text.replace('₹{target.est_price_cr.toFixed(2)} Cr', '₹{num(target?.est_price_cr, 2)} Cr')

text = text.replace('{b.press_sr.toFixed(2)}', '{num(b?.press_sr, 2)}')
text = text.replace('{b.base_sr.toFixed(2)}', '{num(b?.base_sr, 2)}')
text = text.replace('{b.delta_sr >= 0 ? `+${b.delta_sr.toFixed(2)}` : b.delta_sr.toFixed(2)}', '{(Number(b?.delta_sr) >= 0 ? "+" : "") + num(b?.delta_sr, 2)}')
text = text.replace('{b.ppr.toFixed(2)}', '{num(b?.ppr, 2)}')

text = text.replace('{b.press_econ.toFixed(2)}', '{num(b?.press_econ, 2)}')
text = text.replace('{b.base_econ.toFixed(2)}', '{num(b?.base_econ, 2)}')
text = text.replace('{b.delta_econ >= 0 ? `+${b.delta_econ.toFixed(2)}` : b.delta_econ.toFixed(2)}', '{(Number(b?.delta_econ) >= 0 ? "+" : "") + num(b?.delta_econ, 2)}')

text = text.replace('{gem.ppr.toFixed(1)}', '{num(gem?.ppr, 1)}')
text = text.replace('{gem.aor.toFixed(1)}', '{num(gem?.aor, 1)}')
text = text.replace('{gem.srr_pct.toFixed(1)}', '{num(gem?.srr_pct, 1)}')
text = text.replace('₹{gem.rec_price_cr.toFixed(2)} Cr', '₹{num(gem?.rec_price_cr, 2)} Cr')

text = text.replace('₹{currentScenario.total_spend_cr.toFixed(2)} Cr', '₹{num(currentScenario?.total_spend_cr, 2)} Cr')
text = text.replace('₹{currentScenario.remaining_buffer_cr.toFixed(2)} Cr', '₹{num(currentScenario?.remaining_buffer_cr, 2)} Cr')
text = text.replace("{player.aor_score ? player.aor_score.toFixed(1) : '—'}", '{num(player?.aor_score, 1)}')

# Image fallbacks
text = text.replace('src="./rr_logo.png"', 'src="/rr_logo.png" onError={(e) => { e.currentTarget.src = "./rr_logo.png"; }}')

with open('d:/RR/dashboard/src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(text)

print('App.tsx successfully updated!')

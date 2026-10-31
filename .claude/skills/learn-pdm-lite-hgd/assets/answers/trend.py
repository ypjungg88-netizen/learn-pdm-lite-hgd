"""Block 1 정답 — 노이즈 vs 추세 판정, 그래프 한 장(index.html), expected.json.

실행: 현재 폴더에 sensor_50_virtual.csv 가 있어야 한다.
    python3 -I trend.py
규칙 (원본 PdM_Lab_Manual Block 3):
  - 설비 × 센서마다 처음 12점(08:00~11:40)을 기준선으로, 상한 = 평균 + 3σ
  - 상한을 3번 연속 넘으면 '추세'(첫 점 = 추세 시작), 연속 3번이 안 되면 '노이즈'
  - 비교: 25점 전체 평균 ± 2σ(원본 본 강의 ③ 전처리)의 첫 이상 후보
"""
import csv, json, statistics as st
from datetime import datetime
from pathlib import Path

SRC = "sensor_50_virtual.csv"
COLS = {"진동(mm/s)": "진동", "온도(℃)": "온도", "압력(bar)": "압력"}

rows = list(csv.DictReader(open(SRC, encoding="utf-8-sig")))
equips = sorted({r["설비"] for r in rows})


def hhmm(r):
    return r["시간"][-5:]


# 1) 판정 — 설비 × 센서마다
judge = []       # trend_judgement.csv 행
series = {}      # 그래프용 {(설비, 센서): [(시각, 값)]}
sigma2 = []      # 평균 ± 2σ 이상 후보 (시각, 설비, 센서, 값)
for eq in equips:
    rs = [r for r in rows if r["설비"] == eq]
    t = [hhmm(r) for r in rs]
    for col, name in COLS.items():
        v = [float(r[col]) for r in rs]
        series[(eq, name)] = list(zip(t, v))
        base = v[:12]
        upper = st.mean(base) + 3 * st.stdev(base)
        i = 0
        while i < len(v):
            if v[i] > upper:
                j = i
                while j < len(v) and v[j] > upper:
                    j += 1
                kind = "추세" if j - i >= 3 else "노이즈"
                judge.append({"설비": eq, "센서": name, "판정": kind, "시작": t[i],
                              "끝": t[j - 1], "점 수": j - i, "최고값": max(v[i:j]),
                              "기준선 상한": round(upper, 3)})
                i = j
            else:
                i += 1
        m, s = st.mean(v), st.stdev(v)
        sigma2 += [(t[k], eq, name, v[k]) for k in range(len(v)) if abs(v[k] - m) > 2 * s]

with open("trend_judgement.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(judge[0].keys()))
    w.writeheader()
    w.writerows(judge)


def pick(eq_key, sensor, kind):
    return [j for j in judge if eq_key in j["설비"] and j["센서"] == sensor and j["판정"] == kind]


b_temp = pick("설비B", "온도", "추세")[0]
b_vib = pick("설비B", "진동", "추세")[0]
a_noise = pick("설비A", "진동", "노이즈")[0]
trends = [j["시작"] for j in judge if j["판정"] == "추세"]
earliest = min(trends)
sig_b = min(x[0] for x in sigma2 if "설비B" in x[1])
lead = int((datetime.strptime(sig_b, "%H:%M") - datetime.strptime(earliest, "%H:%M")).seconds / 60)

# 2) 그래프 한 장 — 설비A·B 진동(왼쪽 축), 설비B 온도(오른쪽 축), 인라인 SVG
W, H, L, R, T, B = 760, 380, 52, 56, 24, 46
times = [x for x, _ in series[(equips[0], "진동")]]
X = lambda i: L + i * (W - L - R) / (len(times) - 1)
VY = lambda y: T + (H - T - B) * (1 - (y - 0) / 4.0)          # 진동 0~4 mm/s
TY = lambda y: T + (H - T - B) * (1 - (y - 50) / 20.0)        # 온도 50~70 ℃


def path(pts, fy):
    return " ".join(f"{'M' if k == 0 else 'L'}{X(k):.1f},{fy(v):.1f}" for k, (_, v) in enumerate(pts))


eqA = [e for e in equips if "설비A" in e][0]
eqB = [e for e in equips if "설비B" in e][0]
ti = {x: k for k, x in enumerate(times)}
svg = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="설비A·B 진동과 설비B 온도 선 그래프">']
for y in range(0, 5):
    svg.append(f'<line class="grid" x1="{L}" x2="{W-R}" y1="{VY(y):.1f}" y2="{VY(y):.1f}"/>'
               f'<text class="ax" x="{L-8}" y="{VY(y)+4:.1f}" text-anchor="end">{y}</text>')
for y in range(50, 71, 5):
    svg.append(f'<text class="ax" x="{W-R+8}" y="{TY(y)+4:.1f}">{y}</text>')
for k, x in enumerate(times):
    if k % 3 == 0:
        svg.append(f'<text class="ax" x="{X(k):.1f}" y="{H-B+18}" text-anchor="middle">{x}</text>')
svg.append(f'<text class="ax" x="{L-8}" y="{T-8}" text-anchor="end">mm/s</text>'
           f'<text class="ax" x="{W-R+8}" y="{T-8}">℃</text>')
# 평균 ± 2σ 첫 후보 세로선
svg.append(f'<line class="sig" x1="{X(ti[sig_b]):.1f}" x2="{X(ti[sig_b]):.1f}" y1="{T}" y2="{H-B}"/>'
           f'<text class="lbl sigt" x="{X(ti[sig_b])-4:.1f}" y="{T+12}" text-anchor="end">±2σ 첫 후보 {sig_b}</text>')
svg.append(f'<path class="l-a" d="{path(series[(eqA, "진동")], VY)}"/>')
svg.append(f'<path class="l-b" d="{path(series[(eqB, "진동")], VY)}"/>')
svg.append(f'<path class="l-t" d="{path(series[(eqB, "온도")], TY)}"/>')
# 추세 시작·노이즈 표시
bt = dict(series[(eqB, "온도")])[b_temp["시작"]]
bv = dict(series[(eqB, "진동")])[b_vib["시작"]]
svg.append(f'<circle class="d-t" cx="{X(ti[b_temp["시작"]]):.1f}" cy="{TY(bt):.1f}" r="6"/>'
           f'<text class="lbl" x="{X(ti[b_temp["시작"]])+10:.1f}" y="{TY(bt)+20:.1f}">B 온도 추세 시작 {b_temp["시작"]}</text>')
svg.append(f'<circle class="d-b" cx="{X(ti[b_vib["시작"]]):.1f}" cy="{VY(bv):.1f}" r="6"/>'
           f'<text class="lbl" x="{X(ti[b_vib["시작"]])+8:.1f}" y="{VY(bv)+40:.1f}" text-anchor="end">B 진동 추세 시작 {b_vib["시작"]}</text>')
svg.append(f'<circle class="d-a" cx="{X(ti[a_noise["시작"]]):.1f}" cy="{VY(a_noise["최고값"]):.1f}" r="6"/>'
           f'<text class="lbl" x="{X(ti[a_noise["시작"]])+10:.1f}" y="{VY(a_noise["최고값"])+4:.1f}">A 노이즈 {a_noise["최고값"]}</text>')
svg.append("</svg>")

html = f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>노이즈 vs 추세</title>
<style>
:root{{--bg:#fbfaf7;--fg:#1d1d1b;--mute:#6b6a65;--grid:#e4e2dc;--a:#8a8780;--b:#c2410c;--t:#1d4ed8;--sig:#9ca3af}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#161614;--fg:#ecebe6;--mute:#a3a29c;--grid:#2e2d2a;--a:#9a978f;--b:#fb923c;--t:#60a5fa;--sig:#6b7280}}}}
:root[data-theme="dark"]{{--bg:#161614;--fg:#ecebe6;--mute:#a3a29c;--grid:#2e2d2a;--a:#9a978f;--b:#fb923c;--t:#60a5fa;--sig:#6b7280}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,-apple-system,"Apple SD Gothic Neo","Malgun Gothic",sans-serif}}
main{{max-width:820px;margin:0 auto;padding:28px 16px 40px}}
h1{{font-size:1.45rem;margin:0 0 6px}}p{{margin:0 0 14px}}.mute{{color:var(--mute);font-size:.88rem}}
svg{{width:100%;height:auto;display:block}}.grid{{stroke:var(--grid)}}.ax{{fill:var(--mute);font-size:12px}}
.lbl{{fill:var(--fg);font-size:12.5px;font-weight:600}}.sigt{{fill:var(--mute);font-weight:500}}
path{{fill:none;stroke-width:2.4;stroke-linejoin:round}}.l-a{{stroke:var(--a)}}.l-b{{stroke:var(--b)}}.l-t{{stroke:var(--t);stroke-dasharray:6 4}}
.sig{{stroke:var(--sig);stroke-dasharray:3 4}}.d-a{{fill:var(--a)}}.d-b{{fill:var(--b)}}.d-t{{fill:var(--t)}}
@media (max-width:600px){{.ax{{font-size:17px}}.lbl{{font-size:18px}}}}
.key{{display:flex;flex-wrap:wrap;gap:6px 18px;margin:10px 0 18px;font-size:.9rem}}.key i{{display:inline-block;width:18px;height:3px;margin-right:6px;vertical-align:middle}}
</style></head><body><main>
<h1>한 번의 튐은 노이즈, 꾸준한 상승이 신호다</h1>
<p>설비B 온도 추세 시작 <b>{b_temp["시작"]}</b> · 진동 {b_vib["시작"]} — 평균 ± 2σ 첫 후보({sig_b})보다 <b>{lead}분</b> 빠르다. 설비A 진동 {a_noise["최고값"]}({a_noise["시작"]})은 한 번 튄 노이즈.</p>
<div class="key"><span><i style="background:var(--a)"></i>설비A 진동 (프레스 메인모터)</span><span><i style="background:var(--b)"></i>설비B 진동 (차체 용접로봇 감속기)</span><span><i style="background:var(--t)"></i>설비B 온도 (오른쪽 축)</span></div>
{''.join(svg)}
<p class="mute">판정: 설비 × 센서마다 처음 12점(08:00~11:40) 평균 + 3σ를 상한으로, 3번 연속 넘으면 추세(첫 점 = 추세 시작). 2026-09-15 08:00~16:00, 20분 간격.</p>
<p class="mute">실습용 가상 데이터 · 출처: keerhee/kma-auto-genai-3-1 data/Day5/Day5_설비센서_50건_가상.csv · learn-pdm-lite-hgd</p>
</main></body></html>
"""
Path("index.html").write_text(html, encoding="utf-8")

# 3) expected.json — 블록 본문에 쓰는 값
values = {
    "trend_start_b_temp": {"value": b_temp["시작"], "decimals": None, "block": 1},
    "trend_start_b_vib": {"value": b_vib["시작"], "decimals": None, "block": 1},
    "trend_start_earliest": {"value": earliest, "decimals": None, "block": 1},
    "noise_a_value": {"value": a_noise["최고값"], "decimals": 1, "block": 1},
    "noise_a_time": {"value": a_noise["시작"], "decimals": None, "block": 1},
    "sigma2_first": {"value": sig_b, "decimals": None, "block": 1},
    "lead_minutes": {"value": lead, "decimals": 0, "block": 1},
}
Path("expected.json").write_text(json.dumps({"values": values}, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"추세: 설비B 온도 {b_temp['시작']} · 진동 {b_vib['시작']} / 노이즈: 설비A 진동 {a_noise['최고값']}({a_noise['시작']}) / ±2σ 첫 후보 {sig_b} → {lead}분 빠름")

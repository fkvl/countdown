"""
Armina's Race-Day Countdown
===========================
A live countdown to the inaugural IRONMAN 70.3 Northern California
(Redding, CA — Sunday, August 16, 2026), which also happens to be
Armina's birthday. The race opens at sunrise with a swim in
Whiskeytown Lake, so the whole app is built around dawn over the lake.

Run it with:
    pip install -r requirements.txt
    streamlit run app.py
"""

from datetime import datetime, time as dtime
from zoneinfo import ZoneInfo

import streamlit as st
import streamlit.components.v1 as components

# --------------------------------------------------------------------------- #
# Page setup
# --------------------------------------------------------------------------- #
st.set_page_config(
    page_title="Armina's Race-Day Countdown",
    page_icon="🏊‍♀️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Brand palette (mpathic)
MAGENTA, MAGENTA_D = "#ff00c1", "#8f006b"
YELLOW, YELLOW_D = "#FEDA00", "#f3ac02"
CYAN, CYAN_D = "#67dedf", "#1d8587"
PURPLE, LIGHT_GRAY = "#6700a9", "#F9F8F8"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rubik:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,400;1,500&display=swap');
    html, body, [class*="css"], .stApp {{ font-family:'Rubik',sans-serif; }}
    .stApp {{ background:{LIGHT_GRAY}; }}
    #MainMenu, header, footer {{ visibility:hidden; }}
    /* Hide the settings sidebar entirely (and its open arrow) for a clean shared link.
       To re-enable the controls, delete these two rules. */
    section[data-testid="stSidebar"] {{ display:none !important; }}
    [data-testid="stSidebarCollapsedControl"], [data-testid="collapsedControl"] {{ display:none !important; }}
    .block-container {{ padding-top:1.1rem; padding-bottom:2rem; max-width:1120px; }}
    section[data-testid="stSidebar"] {{ background:#fff; border-right:3px solid {MAGENTA}; }}
    section[data-testid="stSidebar"] * {{ font-family:'Rubik',sans-serif; }}
    .sb-title {{ font-weight:800; font-size:1.1rem; color:{MAGENTA_D}; margin:0 0 .15rem; }}
    .sb-sub {{ color:#6b6b6b; font-size:.82rem; margin-bottom:1rem; }}
    .sb-readout {{ background:{LIGHT_GRAY}; border-left:3px solid {CYAN_D};
                   border-radius:0 10px 10px 0; padding:12px 14px; margin-top:8px;
                   font-size:.85rem; color:#2a2a2a; line-height:1.5; }}
    .sb-readout b {{ color:{MAGENTA_D}; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------- #
# Sidebar — configure the countdown target
# --------------------------------------------------------------------------- #
TIMEZONES = {
    "Pacific (Redding, CA), race time": "America/Los_Angeles",
    "Mountain": "America/Denver",
    "Central": "America/Chicago",
    "Eastern": "America/New_York",
    "UTC": "UTC",
}

with st.sidebar:
    st.markdown('<div class="sb-title">Countdown settings</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sb-sub">Pre-filled for IRONMAN 70.3 Northern California. '
        "Adjust anything you like.</div>",
        unsafe_allow_html=True,
    )
    athlete = st.text_input("Athlete", value="Armina")
    race_date = st.date_input("Race day", value=datetime(2026, 8, 16).date())
    start_time = st.time_input("Gun time (local)", value=dtime(6, 40))
    tz_label = st.selectbox("Time zone", list(TIMEZONES.keys()), index=0)

    tz = ZoneInfo(TIMEZONES[tz_label])
    target_dt = datetime.combine(race_date, start_time, tzinfo=tz)
    target_ms = int(target_dt.timestamp() * 1000)

    st.markdown(
        f'<div class="sb-readout">Counting down to<br>'
        f'<b>{target_dt.strftime("%A, %B %-d, %Y")}</b><br>'
        f'gun at <b>{target_dt.strftime("%-I:%M %p")}</b> '
        f'({tz_label.split(",")[0]})</div>',
        unsafe_allow_html=True,
    )

safe_name = (
    athlete.strip().replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    or "Armina"
)
date_long = target_dt.strftime("%B %-d, %Y").upper()

# --------------------------------------------------------------------------- #
# Hero component: dawn over the lake. All HTML/CSS/JS so the clock ticks live,
# client-side, with motion spent in one place — the water and the swimmer.
# --------------------------------------------------------------------------- #
HERO = r"""
<link href="https://fonts.googleapis.com/css2?family=Rubik:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,400;1,500&display=swap" rel="stylesheet">
<style>
  :root{
    --mag:#ff00c1; --mag-d:#8f006b; --yel:#FEDA00; --yel-d:#f3ac02;
    --cy:#67dedf; --cy-d:#1d8587; --purple:#6700a9; --ink:#1a1620; --gray:#F9F8F8;
  }
  *{ box-sizing:border-box; margin:0; padding:0; }
  body{ font-family:'Rubik',sans-serif; background:transparent; color:var(--ink); }
  .wrap{ max-width:1040px; margin:0 auto; }

  /* ---------- HERO ---------- */
  .stage{
    position:relative; overflow:hidden; border-radius:20px;
    min-height:clamp(540px,68vh,660px);
    box-shadow:0 24px 50px rgba(44,10,74,.22); isolation:isolate;
  }
  .sky{ position:absolute; inset:0;
    background:linear-gradient(177deg,
      #2c0a4a 0%, var(--purple) 16%, var(--mag-d) 38%,
      var(--mag) 58%, var(--yel-d) 84%, var(--yel) 100%); }
  .sun{ position:absolute; left:64%; bottom:20%; width:128px; height:128px;
    border-radius:50%;
    background:radial-gradient(circle at 50% 45%, #fffce8 0%, var(--yel) 58%, var(--yel-d) 100%);
    box-shadow:0 0 60px 18px rgba(254,218,0,.45); }

  .content{ position:relative; z-index:3;
    padding:clamp(30px,4.4vw,52px) clamp(26px,5vw,58px) clamp(190px,26vh,224px); }
  .eyebrow{ color:rgba(255,255,255,.82); font-weight:600;
    letter-spacing:.2em; text-transform:uppercase; font-size:clamp(.62rem,1.5vw,.74rem); }
  .title{ color:#fff; font-weight:900; line-height:.96; letter-spacing:-.015em;
    font-size:clamp(1.7rem,5.2vw,3rem); margin-top:14px;
    text-shadow:0 6px 30px rgba(44,10,74,.4); }
  .title em{ font-style:normal; display:block; }
  .loc{ color:rgba(255,255,255,.9); font-weight:400; margin-top:12px;
    font-size:clamp(.85rem,2.1vw,1rem); max-width:30ch; line-height:1.4; }

  .count{ display:flex; align-items:flex-end; gap:clamp(16px,3vw,30px);
    flex-wrap:wrap; margin-top:clamp(20px,3vw,34px); }
  .hours{ font-weight:900; color:#fff; line-height:.8; letter-spacing:-.04em;
    font-size:clamp(4.6rem,17vw,9.5rem); font-variant-numeric:tabular-nums;
    text-shadow:0 12px 44px rgba(44,10,74,.45); }
  .hours-lab{ color:rgba(255,255,255,.92); font-weight:500; font-style:italic;
    font-size:clamp(.95rem,2.4vw,1.25rem); padding-bottom:clamp(8px,1.4vw,16px); }

  .split{ display:flex; gap:clamp(18px,3.4vw,40px); margin-top:clamp(20px,3vw,30px); }
  .unit{ position:relative; padding-left:clamp(14px,2.6vw,28px); }
  .unit:first-child{ padding-left:0; }
  .unit:not(:first-child)::before{ content:""; position:absolute; left:0; top:4px;
    bottom:4px; width:1px; background:rgba(255,255,255,.28); }
  .unit .v{ font-weight:800; color:#fff; line-height:1;
    font-size:clamp(1.5rem,4.6vw,2.3rem); font-variant-numeric:tabular-nums; }
  .unit .k{ color:rgba(255,255,255,.7); font-weight:600; text-transform:uppercase;
    letter-spacing:.16em; font-size:clamp(.56rem,1.5vw,.66rem); margin-top:7px; }

  /* ---------- WATER ---------- */
  .ocean{ position:absolute; left:0; right:0; bottom:0;
    height:clamp(160px,24vh,200px); z-index:2; }
  .ocean svg{ position:absolute; left:0; bottom:0; width:200%; height:100%; }
  .w1{ fill:#bcf0f1; opacity:.5; animation:slide 13s linear infinite; }
  .w2{ fill:var(--cy); opacity:.7; animation:slide 9s linear infinite reverse; }
  .w3{ fill:var(--cy-d); animation:slide 7s linear infinite; }
  @keyframes slide{ to{ transform:translateX(-50%); } }
  .swimmer{ position:absolute; bottom:clamp(104px,15.5vh,128px); left:6%;
    width:clamp(74px,12vw,104px); z-index:3;
    filter:drop-shadow(0 4px 5px rgba(15,76,78,.45));
    animation:lap 12s ease-in-out infinite; }
  @keyframes lap{
    0%{ left:6%; transform:scaleX(1) translateY(0); }
    24%{ transform:scaleX(1) translateY(-4px); }
    48%{ left:80%; transform:scaleX(1) translateY(0); }
    50%{ left:80%; transform:scaleX(-1) translateY(0); }
    74%{ transform:scaleX(-1) translateY(-4px); }
    98%{ left:6%; transform:scaleX(-1) translateY(0); }
    100%{ left:6%; transform:scaleX(1) translateY(0); } }

  /* ---------- BELOW THE FOLD ---------- */
  .place{ display:flex; align-items:center; gap:14px; margin:26px 2px 4px;
    color:#7a7280; font-weight:600; letter-spacing:.18em; text-transform:uppercase;
    font-size:clamp(.62rem,1.5vw,.72rem); }
  .place .ln{ flex:1; height:1px; background:#e2dde6; }

  .course{ display:grid; grid-template-columns:repeat(3,1fr);
    border:1px solid #ece8ef; border-radius:16px; overflow:hidden; background:#fff; }
  @media(max-width:640px){ .course{ grid-template-columns:1fr; } }
  .leg{ padding:22px 24px; border-left:1px solid #ece8ef; }
  .leg:first-child{ border-left:0; }
  @media(max-width:640px){ .leg{ border-left:0; border-top:1px solid #ece8ef; }
    .leg:first-child{ border-top:0; } }
  .leg .nm{ font-weight:800; text-transform:uppercase; letter-spacing:.1em;
    font-size:.74rem; }
  .leg.s .nm{ color:var(--cy-d); } .leg.b .nm{ color:var(--mag); } .leg.r .nm{ color:var(--yel-d); }
  .leg .dist{ font-weight:900; font-size:2rem; color:var(--ink); line-height:1; margin-top:6px; }
  .leg .dist small{ font-size:.92rem; font-weight:600; color:#9a93a1; margin-left:4px; }
  .leg .desc{ color:#6e6776; font-size:.86rem; line-height:1.45; margin-top:9px; }

  .foot{ margin-top:20px; padding-left:2px; }
  .credit{ color:#a59eac; font-weight:500; letter-spacing:.04em; font-size:.78rem; }

  @media (prefers-reduced-motion:reduce){
    .w1,.w2,.w3,.swimmer{ animation:none !important; } }
  #confetti{ position:absolute; inset:0; z-index:5; pointer-events:none; }
</style>

<div class="wrap">
  <div class="stage">
    <div class="sky"><div class="sun"></div></div>

    <div class="content">
      <div class="eyebrow">__NAME__'S RACE MORNING,  __DATE_LONG__</div>
      <h1 class="title"><em>IRONMAN 70.3</em><em>Northern California</em></h1>
      <p class="loc">Armina celebrates her birthday by challenging her spirit to this race.</p>

      <div class="count">
        <div class="hours" id="hours">—</div>
        <div class="hours-lab" id="bigword">hours until it starts!</div>
      </div>

      <div class="split">
        <div class="unit"><div class="v" id="d">0</div><div class="k">days</div></div>
        <div class="unit"><div class="v" id="h">0</div><div class="k">hours</div></div>
        <div class="unit"><div class="v" id="m">0</div><div class="k">minutes</div></div>
        <div class="unit"><div class="v" id="sec">0</div><div class="k">seconds</div></div>
      </div>
    </div>

    <div class="ocean">
      <svg viewBox="0 0 1200 200" preserveAspectRatio="none"><path class="w1" d="M0 80 C150 40 300 120 600 80 C900 40 1050 120 1200 80 L1200 200 0 200 Z M1200 80 C1350 40 1500 120 1800 80 C2100 40 2250 120 2400 80 L2400 200 1200 200 Z"/></svg>
      <svg viewBox="0 0 1200 200" preserveAspectRatio="none"><path class="w2" d="M0 110 C200 80 400 150 600 110 C800 70 1000 150 1200 110 L1200 200 0 200 Z M1200 110 C1400 80 1600 150 1800 110 C2000 70 2200 150 2400 110 L2400 200 1200 200 Z"/></svg>
      <svg viewBox="0 0 1200 200" preserveAspectRatio="none"><path class="w3" d="M0 142 C200 122 400 172 600 147 C800 122 1000 172 1200 147 L1200 200 0 200 Z M1200 142 C1400 122 1600 172 1800 147 C2000 122 2200 172 2400 147 L2400 200 1200 200 Z"/></svg>
    </div>

    <svg class="swimmer" viewBox="0 0 190 96" xmlns="http://www.w3.org/2000/svg">
      <g fill="none" stroke="#0f5e60" stroke-width="9" stroke-linecap="round" stroke-linejoin="round">
        <path d="M118 52 C110 26 88 20 68 33"/>
        <path d="M56 57 C40 60 27 56 13 62"/>
      </g>
      <g fill="#0f5e60">
        <path d="M50 52 C78 43 108 43 130 50 C121 59 96 61 73 61 C63 61 55 59 50 57 Z"/>
        <circle cx="135" cy="52" r="9"/>
        <path d="M139 50 C151 46 163 48 174 53 C163 59 151 59 141 56 Z"/>
      </g>
      <g fill="#bcf0f1">
        <circle cx="176" cy="49" r="2.6"/><circle cx="11" cy="60" r="2"/><circle cx="66" cy="30" r="1.9"/>
      </g>
    </svg>
    <canvas id="confetti"></canvas>
  </div>

  <div class="place"><span>Redding, California</span><span class="ln"></span><span>Whiskeytown Lake</span></div>

  <div class="course">
    <div class="leg s"><div class="nm">Swim</div><div class="dist">1.2<small>mi</small></div>
      <div class="desc">A sunrise start in Whiskeytown Lake, the leg that's hers.</div></div>
    <div class="leg b"><div class="nm">Bike</div><div class="dist">56<small>mi</small></div>
      <div class="desc">Rolling Shasta County hills, a net downhill made for speed.</div></div>
    <div class="leg r"><div class="nm">Run</div><div class="dist">13.1<small>mi</small></div>
      <div class="desc">The Sacramento River Trail across the Sundial Bridge.</div></div>
  </div>

  <div class="foot">
    <span class="credit">#shamwowcreations</span>
  </div>
</div>

<script>
  const TARGET = __TARGET_MS__;
  const NAME = "__NAME__";
  const pad = n => String(n).padStart(2,'0');
  const fmt = n => n.toLocaleString('en-US');
  const $ = id => document.getElementById(id);
  const elHours=$('hours'), elBig=$('bigword'), elD=$('d'), elH=$('h'),
        elM=$('m'), elS=$('sec');

  let fired=false;
  function tick(){
    const diff = TARGET - Date.now();
    if(diff<=0){
      elHours.textContent = fmt(Math.floor(-diff/3600000));
      elBig.textContent = "hours into the adventure";
      elD.textContent="—"; elH.textContent="—"; elM.textContent="—"; elS.textContent="—";
      if(!fired){ fired=true; celebrate(); }
      return;
    }
    elHours.textContent = fmt(Math.floor(diff/3600000));
    elD.textContent = Math.floor(diff/86400000);
    elH.textContent = pad(Math.floor(diff/3600000)%24);
    elM.textContent = pad(Math.floor(diff/60000)%60);
    elS.textContent = pad(Math.floor(diff/1000)%60);
  }

  function celebrate(){
    const cv=$('confetti'), ctx=cv.getContext('2d'), st=cv.parentElement;
    cv.width=st.clientWidth; cv.height=st.clientHeight;
    const cols=['#ff00c1','#FEDA00','#67dedf','#6700a9','#8f006b'];
    const bits=Array.from({length:150},()=>({x:Math.random()*cv.width,y:-20-Math.random()*cv.height,
      r:4+Math.random()*6,c:cols[(Math.random()*cols.length)|0],vx:(Math.random()-.5)*2.4,
      vy:2+Math.random()*3.4,a:Math.random()*6.28,va:(Math.random()-.5)*.3}));
    let f=0;(function loop(){ctx.clearRect(0,0,cv.width,cv.height);
      bits.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.a+=p.va;if(p.y>cv.height+20)p.y=-20;
        ctx.save();ctx.translate(p.x,p.y);ctx.rotate(p.a);ctx.fillStyle=p.c;
        ctx.fillRect(-p.r/2,-p.r/2,p.r,p.r*1.6);ctx.restore();});
      if(f++<470)requestAnimationFrame(loop);else ctx.clearRect(0,0,cv.width,cv.height);})();
  }
  tick(); setInterval(tick,1000);
</script>
"""

HERO = (
    HERO.replace("__TARGET_MS__", str(target_ms))
    .replace("__NAME__", safe_name)
    .replace("__DATE_LONG__", date_long)
)

components.html(HERO, height=1120, scrolling=True)

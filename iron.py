"""
Armina's Race-Day Countdown
===========================
A live countdown to the inaugural IRONMAN 70.3 Northern California
(Redding, CA -- Sunday, August 16, 2026), which also happens to be
Armina's birthday. The race opens at sunrise with a swim in
Whiskeytown Lake, so the whole app is built around dawn-over-the-lake.

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
    initial_sidebar_state="expanded",
)

# Brand palette (mpathic) --------------------------------------------------- #
MAGENTA_L, MAGENTA, MAGENTA_D = "#ffb1ff", "#ff00c1", "#8f006b"
YELLOW_L, YELLOW, YELLOW_D = "#fef5c2", "#FEDA00", "#f3ac02"
CYAN_L, CYAN, CYAN_D = "#bcf0f1", "#67dedf", "#1d8587"
PURPLE, GREEN, LIGHT_GRAY = "#6700a9", "#66bb03", "#F9F8F8"

# App-wide theming (Rubik + brand colors, hide default Streamlit chrome) ----- #
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rubik:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,500&display=swap');

    html, body, [class*="css"], .stApp {{
        font-family: 'Rubik', sans-serif;
    }}
    .stApp {{ background: {LIGHT_GRAY}; }}

    /* Hide Streamlit's default header / footer / menu for a clean canvas */
    #MainMenu, header, footer {{ visibility: hidden; }}
    .block-container {{ padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1180px; }}

    /* Sidebar styling */
    section[data-testid="stSidebar"] {{
        background: #ffffff;
        border-right: 3px solid {MAGENTA};
    }}
    section[data-testid="stSidebar"] * {{ font-family: 'Rubik', sans-serif; }}
    .sb-title {{
        font-weight: 800; font-size: 1.15rem; letter-spacing:.02em;
        color: {MAGENTA_D}; margin: 0 0 .15rem 0;
    }}
    .sb-sub {{ color:#6b6b6b; font-size:.82rem; margin-bottom:1rem; }}
    .sb-readout {{
        background: linear-gradient(135deg, {CYAN_L}, {MAGENTA_L});
        border-radius: 14px; padding: 14px 16px; margin-top: 8px;
        font-size:.86rem; color:#2a2a2a; line-height:1.45;
    }}
    .sb-readout b {{ color:{MAGENTA_D}; }}
    div[data-baseweb="input"] input, div[data-baseweb="select"] {{ font-family:'Rubik'; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------- #
# Sidebar — configure the countdown target
# --------------------------------------------------------------------------- #
TIMEZONES = {
    "Pacific (Redding, CA) — race time": "America/Los_Angeles",
    "Mountain": "America/Denver",
    "Central": "America/Chicago",
    "Eastern": "America/New_York",
    "UTC": "UTC",
}

with st.sidebar:
    st.markdown('<div class="sb-title">⚙️ Countdown settings</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sb-sub">Pre-filled for IRONMAN 70.3 Northern California. '
        "Tweak anything you like.</div>",
        unsafe_allow_html=True,
    )

    athlete = st.text_input("Athlete", value="Armina")
    race_date = st.date_input("Race day", value=datetime(2026, 8, 16).date())
    start_time = st.time_input("Gun time (local)", value=dtime(6, 40))
    tz_label = st.selectbox("Time zone", list(TIMEZONES.keys()), index=0)

    tz = ZoneInfo(TIMEZONES[tz_label])
    target_dt = datetime.combine(race_date, start_time, tzinfo=tz)
    target_ms = int(target_dt.timestamp() * 1000)

    nice_date = target_dt.strftime("%A, %B %-d, %Y")
    nice_time = target_dt.strftime("%-I:%M %p")
    st.markdown(
        f'<div class="sb-readout">Counting down to:<br><b>{nice_date}</b><br>'
        f"Gun at <b>{nice_time}</b> ({tz_label.split(' — ')[0]})</div>",
        unsafe_allow_html=True,
    )

# Light HTML-escape for the athlete name before injecting into the component
safe_name = (
    athlete.strip().replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    or "Armina"
)
date_label = target_dt.strftime("%b %-d, %Y").upper()

# --------------------------------------------------------------------------- #
# The hero component — a self-contained sunrise-over-the-lake countdown.
# Everything inside is HTML/CSS/JS so the clock ticks live, client-side,
# with smooth animation and no server reruns.
# Placeholders (__LIKE_THIS__) are swapped in below to dodge f-string braces.
# --------------------------------------------------------------------------- #
HERO = r"""
<!-- fonts -->
<link href="https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
  :root{
    --mag-l:#ffb1ff; --mag:#ff00c1; --mag-d:#8f006b;
    --yel-l:#fef5c2; --yel:#FEDA00; --yel-d:#f3ac02;
    --cy-l:#bcf0f1;  --cy:#67dedf;  --cy-d:#1d8587;
    --purple:#6700a9; --green:#66bb03; --gray:#F9F8F8; --red:#fc0002;
  }
  *{ box-sizing:border-box; margin:0; padding:0; }
  body{ font-family:'Rubik',sans-serif; background:transparent; }

  .wrap{ max-width:1100px; margin:0 auto; }

  /* ---------- HERO STAGE ---------- */
  .stage{
    position:relative; overflow:hidden;
    border-radius:28px;
    min-height:clamp(560px, 72vh, 720px);
    box-shadow:0 26px 60px rgba(143,0,107,.20);
    isolation:isolate;
  }
  .sky{
    position:absolute; inset:0;
    background:
      linear-gradient(180deg,
        #6700a9 0%,
        var(--mag-d) 22%,
        var(--mag) 44%,
        var(--yel-d) 70%,
        var(--yel) 88%,
        var(--yel-l) 100%);
  }
  /* CMYK "multiply overlay" blobs — literally the brand's color-build method */
  .blob{ position:absolute; border-radius:50%; filter:blur(42px);
         mix-blend-mode:multiply; opacity:.55; }
  .blob.m{ width:340px;height:340px; background:var(--mag);  top:-60px; left:8%;  animation:drift1 17s ease-in-out infinite; }
  .blob.y{ width:300px;height:300px; background:var(--yel);  top:30px;  right:6%; animation:drift2 21s ease-in-out infinite; }
  .blob.c{ width:260px;height:260px; background:var(--cy);   top:120px; left:42%; animation:drift3 19s ease-in-out infinite; }
  @keyframes drift1{ 50%{ transform:translate(40px,30px) scale(1.08); } }
  @keyframes drift2{ 50%{ transform:translate(-34px,24px) scale(1.10); } }
  @keyframes drift3{ 50%{ transform:translate(20px,-22px) scale(.94); } }

  .sun{
    position:absolute; left:50%; transform:translateX(-50%);
    bottom:30%; width:150px; height:150px; border-radius:50%;
    background:radial-gradient(circle at 50% 50%, #fffbe6 0%, var(--yel) 55%, var(--yel-d) 100%);
    box-shadow:0 0 70px 26px rgba(254,218,0,.55), 0 0 140px 60px rgba(243,172,2,.35);
    animation:sunpulse 6s ease-in-out infinite;
  }
  @keyframes sunpulse{ 50%{ box-shadow:0 0 90px 34px rgba(254,218,0,.65), 0 0 170px 70px rgba(243,172,2,.4);} }

  /* ---------- CONTENT ---------- */
  .content{
    position:relative; z-index:3; text-align:center;
    padding:clamp(26px,4vw,46px) 22px clamp(190px,26vh,230px);
  }
  .eyebrow{
    display:inline-flex; align-items:center; gap:9px;
    background:rgba(255,255,255,.22); backdrop-filter:blur(6px);
    border:1px solid rgba(255,255,255,.45);
    color:#fff; font-weight:600; letter-spacing:.16em; text-transform:uppercase;
    font-size:clamp(.6rem,1.4vw,.72rem);
    padding:7px 16px; border-radius:999px;
  }
  .eyebrow .dot{ width:7px;height:7px;border-radius:50%;background:var(--green);
                 box-shadow:0 0 0 0 rgba(102,187,3,.7); animation:live 1.8s infinite; }
  @keyframes live{ 70%{ box-shadow:0 0 0 9px rgba(102,187,3,0);} 100%{box-shadow:0 0 0 0 rgba(102,187,3,0);} }

  .title{
    color:#fff; font-weight:800; line-height:1.02;
    font-size:clamp(1.5rem,4.6vw,2.7rem); margin-top:16px;
    text-shadow:0 3px 22px rgba(143,0,107,.45);
  }
  .title .race{ display:block; font-weight:900; letter-spacing:-.01em; }
  .title .sub{ display:block; font-weight:500; font-size:.5em; opacity:.95; margin-top:6px; }

  .bignum{
    font-weight:900; color:#fff; line-height:.86;
    font-size:clamp(5rem,20vw,11.5rem);
    letter-spacing:-.03em; margin-top:6px;
    text-shadow:0 6px 0 rgba(143,0,107,.25), 0 22px 50px rgba(143,0,107,.45);
    font-variant-numeric:tabular-nums;
  }
  .biglabel{
    color:#fff; font-weight:700; text-transform:uppercase;
    letter-spacing:.34em; font-size:clamp(.8rem,2.4vw,1.15rem);
    margin-top:2px; text-shadow:0 2px 12px rgba(143,0,107,.4);
  }

  /* breakdown tiles */
  .tiles{ display:flex; gap:clamp(8px,1.6vw,16px); justify-content:center;
          flex-wrap:wrap; margin-top:26px; }
  .tile{ min-width:clamp(70px,15vw,96px); padding:14px 8px 11px;
         border-radius:18px; color:#fff; box-shadow:0 10px 24px rgba(0,0,0,.16);}
  .tile .v{ font-weight:900; font-size:clamp(1.5rem,5vw,2.3rem);
            line-height:1; font-variant-numeric:tabular-nums; }
  .tile .k{ font-weight:600; text-transform:uppercase; letter-spacing:.14em;
            font-size:clamp(.55rem,1.5vw,.66rem); opacity:.92; margin-top:6px; }
  .tile.d{ background:linear-gradient(160deg,var(--cy),var(--cy-d)); }
  .tile.h{ background:linear-gradient(160deg,var(--mag),var(--mag-d)); }
  .tile.m{ background:linear-gradient(160deg,var(--yel-d),#c98a00); }
  .tile.s{ background:linear-gradient(160deg,var(--purple),#4a0078); }
  #sec.pulse{ animation:pop .9s ease-out; }
  @keyframes pop{ 0%{transform:scale(1.14);} 100%{transform:scale(1);} }

  /* ---------- WATER ---------- */
  .ocean{ position:absolute; left:0; right:0; bottom:0;
          height:clamp(160px,24vh,210px); z-index:2; }
  .ocean svg{ position:absolute; left:0; bottom:0; width:200%; height:100%; }
  .w1{ fill:var(--cy-l);  opacity:.55; animation:slide 11s linear infinite; }
  .w2{ fill:var(--cy);    opacity:.7;  animation:slide 8s  linear infinite reverse; }
  .w3{ fill:var(--cy-d);              animation:slide 6s  linear infinite; }
  @keyframes slide{ to{ transform:translateX(-50%); } }

  .swimmer{
    position:absolute; bottom:clamp(96px,15vh,128px); left:0; z-index:3;
    font-size:clamp(2rem,6vw,2.8rem);
    filter:drop-shadow(0 4px 6px rgba(29,133,135,.5));
    animation:lap 9s ease-in-out infinite, bob 1.4s ease-in-out infinite;
  }
  @keyframes lap{
    0%   { left:4%;  transform:scaleX(1); }
    47%  { left:88%; transform:scaleX(1); }
    50%  { left:88%; transform:scaleX(-1); }
    97%  { left:4%;  transform:scaleX(-1); }
    100% { left:4%;  transform:scaleX(1); }
  }
  @keyframes bob{ 50%{ margin-bottom:6px; } }

  /* ---------- META STRIP ---------- */
  .meta{ display:flex; flex-wrap:wrap; gap:10px 22px; justify-content:center;
         align-items:center; margin:22px 0 4px; color:#555;
         font-weight:500; font-size:clamp(.78rem,2vw,.92rem); }
  .meta b{ color:var(--mag-d); font-weight:700; }
  .bday{ background:linear-gradient(135deg,var(--yel),var(--yel-d));
         color:#5a3d00; font-weight:700; padding:6px 14px; border-radius:999px;
         box-shadow:0 6px 16px rgba(243,172,2,.35); }

  /* ---------- COURSE CARDS ---------- */
  .cards{ display:grid; grid-template-columns:repeat(3,1fr); gap:16px; margin-top:22px; }
  @media(max-width:680px){ .cards{ grid-template-columns:1fr; } }
  .card{ background:#fff; border-radius:20px; padding:22px 22px 20px;
         box-shadow:0 12px 30px rgba(0,0,0,.07); border-top:6px solid var(--cy);
         transition:transform .18s ease, box-shadow .18s ease; }
  .card:hover{ transform:translateY(-4px); box-shadow:0 18px 40px rgba(0,0,0,.12); }
  .card.swim{ border-color:var(--cy); }
  .card.bike{ border-color:var(--mag); }
  .card.run{  border-color:var(--yel-d); }
  .card .ico{ font-size:1.7rem; }
  .card .leg{ font-weight:800; letter-spacing:.04em; text-transform:uppercase;
              font-size:.78rem; color:#888; margin-top:8px; }
  .card .dist{ font-weight:900; font-size:1.7rem; color:#1d1d1d; line-height:1; margin-top:2px; }
  .card .where{ color:#666; font-size:.86rem; margin-top:8px; line-height:1.35; }
  .card.swim .leg{ color:var(--cy-d); }
  .card.bike .leg{ color:var(--mag); }
  .card.run  .leg{ color:var(--yel-d); }

  /* ---------- PHASE / MOTIVATION ---------- */
  .phase{ margin-top:22px; text-align:center; }
  .phase .badge{ display:inline-block; font-weight:700; letter-spacing:.12em;
                 text-transform:uppercase; font-size:.72rem; color:#fff;
                 background:var(--purple); padding:6px 16px; border-radius:999px; }
  .phase .line{ font-weight:600; color:#3a3a3a; font-size:clamp(1rem,2.6vw,1.25rem);
                margin-top:12px; }
  .phase .line span{ color:var(--mag); }

  @media (prefers-reduced-motion: reduce){
    .blob,.sun,.w1,.w2,.w3,.swimmer,.eyebrow .dot,#sec{ animation:none !important; }
  }
  #confetti{ position:absolute; inset:0; z-index:5; pointer-events:none; }
</style>

<div class="wrap">
  <div class="stage">
    <div class="sky">
      <div class="blob m"></div><div class="blob y"></div><div class="blob c"></div>
      <div class="sun"></div>
    </div>

    <div class="content">
      <span class="eyebrow"><span class="dot"></span>__NAME__'S FIRST 70.3 · __DATE__</span>
      <h1 class="title">
        <span class="race">IRONMAN 70.3</span>
        <span class="race">NORTHERN CALIFORNIA</span>
        <span class="sub">Sunrise swim · Whiskeytown Lake, Redding CA</span>
      </h1>

      <div class="bignum" id="hours">—</div>
      <div class="biglabel" id="bigword">hours to go</div>

      <div class="tiles">
        <div class="tile d"><div class="v" id="d">0</div><div class="k">days</div></div>
        <div class="tile h"><div class="v" id="h">0</div><div class="k">hours</div></div>
        <div class="tile m"><div class="v" id="m">0</div><div class="k">minutes</div></div>
        <div class="tile s"><div class="v" id="sec">0</div><div class="k">seconds</div></div>
      </div>
    </div>

    <div class="ocean">
      <svg viewBox="0 0 1200 200" preserveAspectRatio="none">
        <path class="w1" d="M0 80 C150 40 300 120 600 80 C900 40 1050 120 1200 80 L1200 200 0 200 Z M1200 80 C1350 40 1500 120 1800 80 C2100 40 2250 120 2400 80 L2400 200 1200 200 Z"/>
      </svg>
      <svg viewBox="0 0 1200 200" preserveAspectRatio="none">
        <path class="w2" d="M0 110 C200 80 400 150 600 110 C800 70 1000 150 1200 110 L1200 200 0 200 Z M1200 110 C1400 80 1600 150 1800 110 C2000 70 2200 150 2400 110 L2400 200 1200 200 Z"/>
      </svg>
      <svg viewBox="0 0 1200 200" preserveAspectRatio="none">
        <path class="w3" d="M0 140 C200 120 400 170 600 145 C800 120 1000 170 1200 145 L1200 200 0 200 Z M1200 140 C1400 120 1600 170 1800 145 C2000 120 2200 170 2400 145 L2400 200 1200 200 Z"/>
      </svg>
    </div>
    <div class="swimmer">🏊‍♀️</div>
    <canvas id="confetti"></canvas>
  </div>

  <div class="meta">
    <span>📍 <b>Whiskeytown Lake</b>, Redding, California</span>
    <span>🗓️ <b>__DATE__</b></span>
    <span class="bday">🎂 ...and it's __NAME__'s birthday</span>
  </div>

  <div class="cards">
    <div class="card swim">
      <div class="ico">🏊‍♀️</div><div class="leg">Swim</div>
      <div class="dist">1.2 mi</div>
      <div class="where">Sunrise start in the glassy waters of Whiskeytown Lake — her home turf.</div>
    </div>
    <div class="card bike">
      <div class="ico">🚴‍♀️</div><div class="leg">Bike</div>
      <div class="dist">56 mi</div>
      <div class="where">Rolling Shasta County hills with a net downhill — built for speed.</div>
    </div>
    <div class="card run">
      <div class="ico">🏃‍♀️</div><div class="leg">Run</div>
      <div class="dist">13.1 mi</div>
      <div class="where">Sacramento River Trail across the iconic Sundial Bridge to downtown.</div>
    </div>
  </div>

  <div class="phase">
    <span class="badge" id="phaseBadge">—</span>
    <div class="line" id="phaseLine"></div>
  </div>
</div>

<script>
  const TARGET = __TARGET_MS__;
  const NAME = "__NAME__";
  const pad = n => String(n).padStart(2,'0');
  const fmt = n => n.toLocaleString('en-US');

  const elHours = document.getElementById('hours');
  const elBig   = document.getElementById('bigword');
  const elD = document.getElementById('d'), elH = document.getElementById('h');
  const elM = document.getElementById('m'), elS = document.getElementById('sec');
  const badge = document.getElementById('phaseBadge');
  const pline = document.getElementById('phaseLine');

  // Triathlon periodization — real training phases keyed to days out.
  function phase(days){
    if(days > 70) return ["Base season",   `Long, easy meters in the pool. <span>${NAME}</span> is building the engine.`];
    if(days > 35) return ["Build block",   `Intensity rising. Every hard set this month pays off on the lake.`];
    if(days > 14) return ["Sharpening",    `Race-pace work and brick sessions. The fitness is in the bank.`];
    if(days > 7)  return ["Taper window",  `Volume drops, legs come back. Trust the training, <span>${NAME}</span>.`];
    if(days > 1)  return ["Race week",     `Bags packed, goggles ready. The lake is waiting at dawn.`];
    if(days === 1)return ["Tomorrow",      `One sleep to go. Glassy water at first light. <span>${NAME}</span> — this is it.`];
    return ["Race day", `🎉 Happy birthday and happy race day, <span>${NAME}</span>! Dive in.`];
  }

  let fired = false;
  function tick(){
    const diff = TARGET - Date.now();

    if(diff <= 0){
      const since = Math.floor(-diff/3600000);
      elHours.textContent = fmt(since);
      elBig.textContent = "hours into the adventure";
      elD.textContent = "🎂"; elH.textContent = "🏊‍♀️"; elM.textContent = "🚴‍♀️"; elS.textContent = "🏃‍♀️";
      const [b,l] = phase(0); badge.textContent = b; pline.innerHTML = l;
      if(!fired){ fired = true; celebrate(); }
      return;
    }

    const totalHours = Math.floor(diff/3600000);
    const days = Math.floor(diff/86400000);
    const hours = Math.floor(diff/3600000) % 24;
    const mins  = Math.floor(diff/60000) % 60;
    const secs  = Math.floor(diff/1000) % 60;

    elHours.textContent = fmt(totalHours);
    elD.textContent = days;
    elH.textContent = pad(hours);
    elM.textContent = pad(mins);
    elS.textContent = pad(secs);
    elS.classList.remove('pulse'); void elS.offsetWidth; elS.classList.add('pulse');

    const [b,l] = phase(days);
    badge.textContent = b; pline.innerHTML = l;
  }

  // ---- lightweight confetti in brand colors, for race day ----
  function celebrate(){
    const cv = document.getElementById('confetti');
    const ctx = cv.getContext('2d');
    const stage = cv.parentElement;
    cv.width = stage.clientWidth; cv.height = stage.clientHeight;
    const colors = ['#ff00c1','#FEDA00','#67dedf','#6700a9','#66bb03','#ffb1ff'];
    const bits = Array.from({length:160}, () => ({
      x: Math.random()*cv.width, y: -20 - Math.random()*cv.height,
      r: 4 + Math.random()*6, c: colors[(Math.random()*colors.length)|0],
      vx:(Math.random()-.5)*2.4, vy: 2 + Math.random()*3.5,
      a: Math.random()*Math.PI, va:(Math.random()-.5)*.3
    }));
    let frames = 0;
    (function loop(){
      ctx.clearRect(0,0,cv.width,cv.height);
      bits.forEach(p=>{
        p.x+=p.vx; p.y+=p.vy; p.a+=p.va; if(p.y>cv.height+20) p.y=-20;
        ctx.save(); ctx.translate(p.x,p.y); ctx.rotate(p.a); ctx.fillStyle=p.c;
        ctx.fillRect(-p.r/2,-p.r/2,p.r,p.r*1.6); ctx.restore();
      });
      if(frames++ < 460) requestAnimationFrame(loop); else ctx.clearRect(0,0,cv.width,cv.height);
    })();
  }

  tick();
  setInterval(tick, 1000);
</script>
"""

HERO = (
    HERO.replace("__TARGET_MS__", str(target_ms))
    .replace("__NAME__", safe_name)
    .replace("__DATE__", date_label)
)

components.html(HERO, height=1240, scrolling=True)

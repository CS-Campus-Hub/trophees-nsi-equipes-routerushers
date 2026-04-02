# routex_jeu.py
# Projet Trophee NSI 2026
# Lance la page d accueil et le jeu RouteRush

import webbrowser
import http.server
import threading
import socket
import time

# page d accueil
PAGE_ACCUEIL = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>RouteX</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Cormorant+Garamond:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --forest-deep:   #0a1a0d;
            --forest-mid:    #0e2712;
            --forest-light:  #1a3d1c;
            --leaf-green:    #3a7d44;
            --moss:          #5c8a3c;
            --fern:          #7ab648;
            --bark:          #5c3d1e;
            --earth:         #2e1a0e;
            --sunbeam:       #e8c96d;
            --gold:          #d4a017;
            --white-mist:    rgba(255,255,255,0.85);
            --mist:          rgba(200,230,200,0.12);
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        html { scroll-behavior: smooth; }

        body {
            font-family: 'Cormorant Garamond', Georgia, serif;
            background: var(--forest-deep);
            color: #d8efca;
            min-height: 100vh;
            overflow-x: hidden;
        }

        .nature-bg {
            position: fixed;
            inset: 0;
            z-index: 0;
            pointer-events: none;
            overflow: hidden;
        }

        .nature-bg::before {
            content: "";
            position: absolute;
            inset: 0;
            background:
                radial-gradient(ellipse 80% 40% at 50% -10%, rgba(60,120,40,0.35) 0%, transparent 70%),
                radial-gradient(ellipse 60% 30% at 20% 0%, rgba(20,80,30,0.4) 0%, transparent 60%),
                radial-gradient(ellipse 50% 50% at 80% 10%, rgba(30,90,20,0.3) 0%, transparent 60%),
                linear-gradient(to bottom, #061208 0%, #0a1a0d 30%, #06100a 70%, #020804 100%);
        }

        .nature-bg::after {
            content: "";
            position: absolute;
            inset: 0;
            background-image:
                radial-gradient(circle at 1px 1px, rgba(90,160,60,0.04) 1px, transparent 0);
            background-size: 28px 28px;
            opacity: 0.7;
        }

        .fireflies {
            position: fixed;
            inset: 0;
            z-index: 1;
            pointer-events: none;
        }
        .firefly {
            position: absolute;
            width: 4px; height: 4px;
            border-radius: 50%;
            background: #c8ff80;
            box-shadow: 0 0 6px 2px rgba(180,255,80,0.8);
            animation: drift var(--d) ease-in-out infinite alternate, glow 2s ease-in-out infinite alternate;
        }
        @keyframes drift {
            0%   { transform: translate(0,0); opacity: 0; }
            20%  { opacity: 1; }
            80%  { opacity: 0.8; }
            100% { transform: translate(var(--tx), var(--ty)); opacity: 0; }
        }
        @keyframes glow {
            0%   { box-shadow: 0 0 4px 1px rgba(180,255,80,0.5); }
            100% { box-shadow: 0 0 10px 4px rgba(200,255,100,0.95); }
        }

        .grain {
            position: fixed;
            inset: 0;
            z-index: 2;
            pointer-events: none;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
            opacity: 0.35;
            mix-blend-mode: overlay;
        }

        .page {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            padding: 60px 20px 40px;
            position: relative;
            z-index: 10;
        }

        .top-text {
            color: var(--fern);
            letter-spacing: 8px;
            font-size: 13px;
            text-transform: uppercase;
            opacity: 0.85;
            margin-bottom: 18px;
            font-family: 'Cormorant Garamond', serif;
            font-weight: 600;
        }

        .hero {
            width: 100%;
            max-width: 1000px;
            text-align: center;
            z-index: 1;
        }

        .title-wrap {
            position: relative;
            display: inline-block;
            margin-bottom: 10px;
        }

        .title {
            font-family: 'Playfair Display', serif;
            font-weight: 900;
            font-size: 110px;
            letter-spacing: 6px;
            color: transparent;
            -webkit-text-stroke: 3px #a8d878;
            text-transform: uppercase;
            text-shadow:
                0 0 40px rgba(100,200,60,0.3),
                0 0 80px rgba(80,160,40,0.15);
            position: relative;
            z-index: 2;
        }

        .title-glow {
            position: absolute;
            inset: 0;
            transform: translateY(6px) scale(1.01);
            font-family: 'Playfair Display', serif;
            font-weight: 900;
            font-size: 110px;
            letter-spacing: 6px;
            color: rgba(60, 160, 40, 0.18);
            z-index: 0;
            filter: blur(8px);
            user-select: none;
        }

        .title-desc {
            color: rgba(180,220,140,0.65);
            font-size: 15px;
            max-width: 620px;
            margin: 12px auto 0;
            line-height: 1.8;
            letter-spacing: 1px;
        }

        .year-line {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            margin: 28px 0 28px;
        }
        .year-line .line {
            width: 100px;
            height: 1px;
            background: linear-gradient(to right, transparent, var(--fern), transparent);
        }
        .year {
            font-family: 'Playfair Display', serif;
            font-size: 48px;
            color: var(--sunbeam);
            font-weight: 900;
            letter-spacing: 8px;
            text-shadow: 0 0 24px rgba(232,201,109,0.7);
        }

        .description {
            color: rgba(180,220,140,0.5);
            text-transform: uppercase;
            letter-spacing: 7px;
            font-size: 13px;
            line-height: 2.5;
            max-width: 800px;
            margin: 0 auto 40px;
        }

        .cta {
            display: inline-block;
            background: linear-gradient(135deg, #2e7d32, #5a9e30);
            color: #efffdf;
            text-decoration: none;
            font-family: 'Playfair Display', serif;
            font-size: 22px;
            letter-spacing: 6px;
            text-transform: uppercase;
            padding: 22px 64px;
            border-radius: 2px;
            border: 1px solid rgba(120,200,80,0.4);
            box-shadow:
                0 0 20px rgba(80,180,40,0.5),
                0 0 50px rgba(60,140,30,0.2),
                inset 0 1px 0 rgba(255,255,255,0.1);
            transition: 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        .cta::after {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, rgba(255,255,255,0.07), transparent);
        }
        .cta:hover {
            transform: translateY(-2px) scale(1.03);
            box-shadow:
                0 0 30px rgba(100,220,50,0.65),
                0 0 70px rgba(80,180,40,0.3),
                inset 0 1px 0 rgba(255,255,255,0.15);
        }

        .arrow-link { margin-bottom: 30px; z-index: 1; }
        .arrow {
            width: 28px; height: 28px;
            border-right: 3px solid var(--fern);
            border-bottom: 3px solid var(--fern);
            transform: rotate(45deg);
            box-shadow: 0 0 10px rgba(122,182,72,0.6);
            animation: bounce 1.8s infinite;
        }
        @keyframes bounce {
            0%,100% { transform: rotate(45deg) translateY(0); }
            50%      { transform: rotate(45deg) translateY(8px); }
        }

        .forest-floor {
            position: fixed;
            bottom: 0; left: 0; right: 0;
            z-index: 3;
            pointer-events: none;
        }
        .forest-left {
            position: fixed;
            left: 0; top: 0; bottom: 0;
            z-index: 3;
            pointer-events: none;
            width: 220px;
        }
        .forest-right {
            position: fixed;
            right: 0; top: 0; bottom: 0;
            z-index: 3;
            pointer-events: none;
            width: 220px;
        }

        .game-section {
            min-height: 100vh;
            padding: 80px 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
            z-index: 10;
        }
        .game-box {
            width: 100%;
            max-width: 1000px;
            background: rgba(10,26,13,0.85);
            border: 1px solid rgba(90,158,48,0.35);
            box-shadow:
                0 0 40px rgba(60,120,30,0.2),
                inset 0 0 60px rgba(0,0,0,0.4);
            padding: 36px;
            border-radius: 6px;
            text-align: center;
            backdrop-filter: blur(4px);
        }
        .game-box h2 {
            font-family: 'Playfair Display', serif;
            color: var(--fern);
            font-size: 36px;
            margin-bottom: 16px;
            text-transform: uppercase;
            letter-spacing: 4px;
            text-shadow: 0 0 20px rgba(122,182,72,0.4);
        }
        .game-box p {
            color: rgba(180,220,140,0.65);
            font-size: 16px;
            margin-bottom: 20px;
        }

        /* Message si RouteRush.html absent */
        .game-placeholder {
            padding: 60px 20px;
            border: 2px dashed rgba(122,182,72,0.3);
            border-radius: 4px;
            color: rgba(180,220,140,0.5);
            font-size: 15px;
            line-height: 2;
        }
        .game-placeholder strong {
            color: var(--fern);
            display: block;
            font-size: 18px;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>

<div class="nature-bg"></div>
<div class="grain"></div>

<div class="fireflies" id="fireflies"></div>

<svg class="forest-left" viewBox="0 0 220 900" preserveAspectRatio="xMinYMax meet" xmlns="http://www.w3.org/2000/svg">
    <rect x="55" y="380" width="18" height="520" fill="#3b1f08" opacity="0.9"/>
    <rect x="57" y="400" width="4" height="300" fill="#5c3d1e" opacity="0.4"/>
    <ellipse cx="64" cy="370" rx="55" ry="70" fill="#1a4c1e" opacity="0.9"/>
    <ellipse cx="64" cy="310" rx="46" ry="58" fill="#1e5a22" opacity="0.9"/>
    <ellipse cx="64" cy="255" rx="36" ry="50" fill="#246128" opacity="0.85"/>
    <ellipse cx="64" cy="205" rx="26" ry="40" fill="#2e7032" opacity="0.8"/>
    <ellipse cx="50" cy="270" rx="12" ry="20" fill="#3a8c3e" opacity="0.25"/>
    <path d="M30,380 Q20,420 25,450 Q30,430 35,450 Q40,420 35,380Z" fill="#2a6a2e" opacity="0.6"/>
    <path d="M80,360 Q90,400 88,435 Q83,410 78,435 Q73,400 76,360Z" fill="#256028" opacity="0.55"/>
    <rect x="8" y="500" width="10" height="400" fill="#3b1f08" opacity="0.7"/>
    <ellipse cx="13" cy="490" rx="28" ry="38" fill="#163c1a" opacity="0.8"/>
    <ellipse cx="13" cy="450" rx="22" ry="30" fill="#1a4a1e" opacity="0.8"/>
    <ellipse cx="13" cy="415" rx="16" ry="24" fill="#205523" opacity="0.75"/>
    <ellipse cx="30" cy="870" rx="28" ry="10" fill="#1e5c20" opacity="0.7"/>
    <path d="M30,860 Q18,820 10,800 Q22,835 25,855Z" fill="#2a7c2e" opacity="0.8"/>
    <path d="M30,860 Q42,818 50,796 Q38,833 35,855Z" fill="#2a7c2e" opacity="0.8"/>
    <path d="M28,858 Q24,830 26,810 Q30,835 32,855Z" fill="#338035" opacity="0.7"/>
    <ellipse cx="85" cy="875" rx="22" ry="8" fill="#185018" opacity="0.65"/>
    <path d="M85,868 Q75,840 70,822 Q80,848 82,864Z" fill="#206822" opacity="0.75"/>
    <path d="M85,868 Q95,838 100,820 Q90,846 88,864Z" fill="#206822" opacity="0.75"/>
    <path d="M10,895 Q0,860 5,840 Q12,868 14,888Z" fill="#247026" opacity="0.6"/>
    <path d="M10,895 Q-5,870 -2,852 Q8,874 10,890Z" fill="#1e5c20" opacity="0.55"/>
    <ellipse cx="100" cy="892" rx="10" ry="4" fill="#7a3a1a" opacity="0.8"/>
    <path d="M96,892 Q100,878 104,892Z" fill="#c05a28" opacity="0.9"/>
    <ellipse cx="68" cy="898" rx="7" ry="3" fill="#8a4a22" opacity="0.7"/>
    <path d="M65,898 Q68,887 71,898Z" fill="#d06a30" opacity="0.85"/>
</svg>

<svg class="forest-right" viewBox="0 0 220 900" preserveAspectRatio="xMaxYMax meet" xmlns="http://www.w3.org/2000/svg">
    <rect x="147" y="360" width="18" height="540" fill="#3b1f08" opacity="0.9"/>
    <rect x="149" y="380" width="4" height="300" fill="#5c3d1e" opacity="0.4"/>
    <ellipse cx="156" cy="350" rx="58" ry="72" fill="#1a4c1e" opacity="0.9"/>
    <ellipse cx="156" cy="288" rx="48" ry="60" fill="#1e5a22" opacity="0.9"/>
    <ellipse cx="156" cy="232" rx="38" ry="52" fill="#246128" opacity="0.85"/>
    <ellipse cx="156" cy="180" rx="28" ry="42" fill="#2e7032" opacity="0.8"/>
    <ellipse cx="170" cy="248" rx="12" ry="20" fill="#3a8c3e" opacity="0.25"/>
    <path d="M130,360 Q120,400 122,432 Q127,410 132,432 Q137,400 135,360Z" fill="#2a6a2e" opacity="0.6"/>
    <path d="M175,345 Q185,388 182,422 Q177,400 172,422 Q167,388 170,345Z" fill="#256028" opacity="0.55"/>
    <rect x="202" y="480" width="10" height="420" fill="#3b1f08" opacity="0.7"/>
    <ellipse cx="207" cy="470" rx="28" ry="38" fill="#163c1a" opacity="0.8"/>
    <ellipse cx="207" cy="430" rx="22" ry="30" fill="#1a4a1e" opacity="0.8"/>
    <ellipse cx="207" cy="394" rx="16" ry="24" fill="#205523" opacity="0.75"/>
    <ellipse cx="190" cy="870" rx="28" ry="10" fill="#1e5c20" opacity="0.7"/>
    <path d="M190,860 Q178,820 170,800 Q182,835 185,855Z" fill="#2a7c2e" opacity="0.8"/>
    <path d="M190,860 Q202,818 210,796 Q198,833 195,855Z" fill="#2a7c2e" opacity="0.8"/>
    <path d="M188,858 Q184,830 186,810 Q190,835 192,855Z" fill="#338035" opacity="0.7"/>
    <ellipse cx="135" cy="876" rx="22" ry="8" fill="#185018" opacity="0.65"/>
    <path d="M135,868 Q125,840 120,822 Q130,848 132,864Z" fill="#206822" opacity="0.75"/>
    <path d="M135,868 Q145,838 150,820 Q140,846 138,864Z" fill="#206822" opacity="0.75"/>
    <path d="M210,895 Q220,860 215,840 Q208,868 206,888Z" fill="#247026" opacity="0.6"/>
    <ellipse cx="120" cy="890" rx="10" ry="4" fill="#7a3a1a" opacity="0.8"/>
    <path d="M116,890 Q120,876 124,890Z" fill="#c05a28" opacity="0.9"/>
    <ellipse cx="152" cy="896" rx="7" ry="3" fill="#8a4a22" opacity="0.7"/>
    <path d="M149,896 Q152,885 155,896Z" fill="#d06a30" opacity="0.85"/>
</svg>

<svg class="forest-floor" viewBox="0 0 1440 220" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M0,160 Q180,120 360,150 Q540,180 720,140 Q900,100 1080,145 Q1260,185 1440,155 L1440,220 L0,220Z" fill="#0a1a0d" opacity="0.95"/>
    <path d="M0,175 Q200,140 400,165 Q600,190 800,160 Q1000,130 1200,165 Q1360,190 1440,172 L1440,220 L0,220Z" fill="#061008" opacity="0.9"/>
    <path d="M300,185 Q288,148 280,128 Q294,162 298,180Z" fill="#2a7c2e" opacity="0.85"/>
    <path d="M300,185 Q312,146 320,126 Q306,160 302,180Z" fill="#2a7c2e" opacity="0.85"/>
    <path d="M298,183 Q290,155 292,135 Q299,160 301,178Z" fill="#338035" opacity="0.7"/>
    <ellipse cx="300" cy="188" rx="24" ry="8" fill="#1e5c20" opacity="0.6"/>
    <path d="M720,178 Q708,140 700,118 Q714,155 718,172Z" fill="#246028" opacity="0.8"/>
    <path d="M720,178 Q732,138 740,116 Q726,153 722,172Z" fill="#246028" opacity="0.8"/>
    <path d="M716,174 Q702,150 706,130 Q715,155 717,170Z" fill="#2e7032" opacity="0.7"/>
    <ellipse cx="720" cy="180" rx="28" ry="9" fill="#1a4c1e" opacity="0.55"/>
    <path d="M1100,183 Q1088,146 1080,126 Q1094,158 1098,178Z" fill="#256024" opacity="0.8"/>
    <path d="M1100,183 Q1112,144 1120,124 Q1106,157 1102,177Z" fill="#256024" opacity="0.8"/>
    <ellipse cx="1100" cy="186" rx="24" ry="8" fill="#1a5018" opacity="0.6"/>
    <path d="M500,192 Q494,170 496,158 Q500,172 503,188Z" fill="#2a6a2e" opacity="0.65"/>
    <path d="M500,192 Q506,168 508,156 Q503,170 501,188Z" fill="#2a6a2e" opacity="0.65"/>
    <path d="M950,190 Q944,168 946,155 Q950,170 953,186Z" fill="#236022" opacity="0.65"/>
    <path d="M950,190 Q956,166 958,153 Q953,168 951,186Z" fill="#236022" opacity="0.65"/>
    <ellipse cx="440" cy="200" rx="12" ry="4" fill="#7a3a1a" opacity="0.75"/>
    <path d="M435,200 Q440,188 445,200Z" fill="#c05a28" opacity="0.9"/>
    <ellipse cx="860" cy="202" rx="9" ry="3" fill="#8a4a22" opacity="0.7"/>
    <path d="M857,202 Q860,192 863,202Z" fill="#d06a30" opacity="0.85"/>
    <ellipse cx="1240" cy="198" rx="11" ry="4" fill="#7a3a1a" opacity="0.75"/>
    <path d="M1236,198 Q1240,186 1244,198Z" fill="#c05a28" opacity="0.88"/>
    <ellipse cx="600" cy="208" rx="30" ry="8" fill="#0e1a0a" opacity="0.6"/>
    <ellipse cx="1050" cy="210" rx="22" ry="6" fill="#0e1a0a" opacity="0.5"/>
</svg>

<section class="page">
    <div class="hero">
        <div class="top-text">Project &bull; Trophée NSI &bull; 2026</div>
        <div class="title-wrap">
            <div class="title-glow">ROUTEX</div>
            <div class="title">ROUTEX</div>
        </div>
        <p class="title-desc">
            Nous avons créé ce jeu dans le but d'aider les élèves à mieux comprendre la notion de routeur et ses différents types de fonctionnement (OSPF, RIP… etc)
        </p>
        <div class="year-line">
            <div class="line"></div>
            <div class="year">2026</div>
            <div class="line"></div>
        </div>
        <div class="description">
            Jeu Éducatif &amp; Divertissant
        </div>
        <a href="#game" class="cta">Start Game</a>
    </div>
    <a href="#game" class="arrow-link">
        <div class="arrow"></div>
    </a>
</section>

<section id="game" class="game-section">
    <div class="game-box">
        <h2>RouteX</h2>
        <p>Explorez le réseau — naviguez, routez, apprenez.</p>
        <div id="game-container"></div>
    </div>
</section>

<script>
    // Fireflies
    const container = document.getElementById('fireflies');
    for (let i = 0; i < 38; i++) {
        const f = document.createElement('div');
        f.className = 'firefly';
        const x = Math.random() * 100;
        const y = Math.random() * 100;
        const tx = (Math.random() - 0.5) * 160;
        const ty = (Math.random() - 0.5) * 120;
        const d  = (4 + Math.random() * 8).toFixed(1);
        f.style.cssText = `
            left:${x}vw; top:${y}vh;
            --tx:${tx}px; --ty:${ty}px; --d:${d}s;
            animation-delay:${(Math.random()*6).toFixed(1)}s;
            width:${2+Math.random()*3}px; height:${2+Math.random()*3}px;
            opacity:0;
        `;
        container.appendChild(f);
    }

    // Chargement du jeu dans un iframe
    const gc = document.getElementById('game-container');
    const iframe = document.createElement('iframe');
    iframe.src = 'RouteRush.html';
    iframe.width = '100%';
    iframe.height = '600px';
    iframe.style.cssText = 'border:none;border-radius:4px;display:block;';
    iframe.allow = 'fullscreen';
    gc.appendChild(iframe);
</script>
</body>
</html>
"""

# page du jeu
PAGE_JEU = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>RouteRush — Network Routing Simulator</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600;700&display=swap');

:root{
  --bg:#0d0520;--bg1:#150a30;--bg2:#1a0a35;--bg3:#200c40;
  --cyan:#00e5ff;--cg:rgba(0,229,255,.1);--cb:rgba(0,229,255,.18);
  --green:#00ff9d;--gg:rgba(0,255,157,.1);
  --red:#ff2952;--rg:rgba(255,41,82,.1);
  --orange:#ff8c00;--yellow:#ffd600;--purple:#b44fff;--pink:#ff4dff;
  --txt:#c0d8f5;--muted:rgba(192,216,245,.4);
  --border:rgba(0,229,255,.14);--border2:rgba(0,229,255,.06);
  --mono:'Share Tech Mono',monospace;
  --orb:'Orbitron',monospace;
  --raj:'Rajdhani',sans-serif;
}
*{margin:0;padding:0;box-sizing:border-box;}
html,body{width:100%;height:100%;overflow:hidden;background:var(--bg);font-family:var(--raj);color:var(--txt);}

/* ══ SCREENS ══ */
.scr{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;transition:opacity .5s;}
.scr.off{opacity:0;pointer-events:none;}

/* ══════════════════════════════════════════
   INTRO
══════════════════════════════════════════ */
#sIntro{
  flex-direction:column;gap:20px;
  background:radial-gradient(ellipse 120% 80% at 60% 20%, #6b1fa8, #2d0b6e 40%, #0d0520);
}
.intro-grid{position:absolute;inset:0;
  background-image:linear-gradient(rgba(0,229,255,.04) 1px,transparent 1px),
  linear-gradient(90deg,rgba(0,229,255,.04) 1px,transparent 1px);
  background-size:52px 52px;animation:igrid 20s linear infinite;}
@keyframes igrid{to{background-position:52px 52px;}}

.scan-line{position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,var(--cyan),transparent);
  animation:scan 6s linear infinite;opacity:.3;}
@keyframes scan{0%{top:0}100%{top:100%}}

.intro-inner{position:relative;z-index:2;display:flex;flex-direction:column;align-items:center;gap:16px;padding:20px;}
.intro-logo{text-align:center;}
.logo-sub{font-family:var(--orb);font-size:.55rem;letter-spacing:.6em;color:var(--cyan);opacity:.7;margin-bottom:10px;}
.logo-main{font-family:var(--orb);font-weight:900;font-size:clamp(2.8rem,6vw,5rem);
  background:linear-gradient(135deg,#fff 0%,var(--cyan) 40%,#0044cc 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  filter:drop-shadow(0 0 60px rgba(0,229,255,.5));letter-spacing:.15em;}
.logo-tag{font-family:var(--mono);font-size:.7rem;color:rgba(0,229,255,.6);letter-spacing:.2em;margin-top:4px;}

/* Baymax intro */
.bx-hero{animation:bfloat 3.8s ease-in-out infinite;position:relative;}
@keyframes bfloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-18px)}}
.bx-hero::after{content:'';position:absolute;bottom:-16px;left:50%;transform:translateX(-50%);
  width:110px;height:16px;border-radius:50%;
  background:radial-gradient(ellipse,rgba(0,229,255,.3),transparent 70%);
  animation:bshadow 3.8s ease-in-out infinite;}
@keyframes bshadow{0%,100%{transform:translateX(-50%) scaleX(1);opacity:.5}50%{transform:translateX(-50%) scaleX(.6);opacity:.25}}

.intro-desc{
  max-width:600px;text-align:center;font-size:1rem;color:var(--muted);line-height:1.8;
  border:1px solid var(--border2);border-radius:8px;padding:16px 24px;background:rgba(0,229,255,.03);
}
.intro-desc b{color:var(--cyan);}

/* Level selector */
.lvl-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;max-width:780px;width:100%;}
.lvl-card{
  padding:14px 10px;border-radius:8px;text-align:center;cursor:pointer;
  border:1px solid var(--border2);background:rgba(0,229,255,.03);
  transition:all .2s;position:relative;overflow:hidden;}
.lvl-card::before{content:'';position:absolute;inset:0;background:linear-gradient(135deg,transparent,rgba(0,229,255,.04));opacity:0;transition:opacity .2s;}
.lvl-card:hover:not(.locked){border-color:var(--cyan);background:var(--cg);}
.lvl-card:hover:not(.locked)::before{opacity:1;}
.lvl-card.locked{opacity:.3;cursor:not-allowed;}
.lvl-card.active{border-color:var(--cyan);background:var(--cg);box-shadow:0 0 20px rgba(0,229,255,.15);}
.lvl-card.cleared{border-color:var(--green);}
.lvl-card.cleared::after{content:'✓';position:absolute;top:6px;right:8px;color:var(--green);font-family:var(--orb);font-size:.65rem;}
.lc-num{font-family:var(--orb);font-size:1.6rem;font-weight:900;line-height:1;}
.lc-name{font-size:.72rem;font-weight:700;margin:4px 0 2px;letter-spacing:.03em;}
.lc-proto{font-family:var(--mono);font-size:.6rem;color:var(--cyan);margin-bottom:3px;}
.lc-diff{font-size:.6rem;font-weight:700;letter-spacing:.05em;}
.d1{color:#00ff9d}.d2{color:#88ff00}.d3{color:#ffd600}.d4{color:#ff8c00}.d5{color:#ff2952}.d6{color:#b44fff}

.cta-row{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;}
.btn-a{
  background:linear-gradient(135deg,var(--cyan),#004dcc);border:none;border-radius:7px;
  padding:13px 44px;font-family:var(--orb);font-size:.8rem;font-weight:700;color:var(--bg);
  letter-spacing:.12em;cursor:pointer;box-shadow:0 0 24px rgba(0,229,255,.3);transition:all .2s;}
.btn-a:hover{transform:scale(1.05);box-shadow:0 0 50px rgba(0,229,255,.6);}
.btn-b{background:transparent;border:1.5px solid var(--border);border-radius:7px;
  padding:12px 20px;font-family:var(--orb);font-size:.7rem;color:var(--txt);cursor:pointer;transition:all .2s;letter-spacing:.08em;}
.btn-b:hover{border-color:var(--cyan);color:var(--cyan);}

/* ══════════════════════════════════════════
   GAME LAYOUT
══════════════════════════════════════════ */
#sGame{flex-direction:column;align-items:stretch;justify-content:flex-start;}

/* ─ TOP HUD ─ */
.hud{
  height:54px;flex-shrink:0;display:flex;align-items:center;padding:0 14px;gap:12px;
  background:rgba(2,8,16,.98);border-bottom:1px solid var(--border);z-index:40;}
.hud-brand{font-family:var(--orb);font-size:.8rem;font-weight:900;color:var(--cyan);
  letter-spacing:.15em;display:flex;align-items:center;gap:8px;white-space:nowrap;}
.hud-sep{width:1px;height:28px;background:var(--border);flex-shrink:0;}
.hb{display:flex;flex-direction:column;min-width:50px;}
.hl{font-family:var(--orb);font-size:.44rem;letter-spacing:.2em;color:var(--muted);}
.hv{font-family:var(--orb);font-size:.78rem;font-weight:700;}
.cy{color:var(--cyan)}.gr{color:var(--green)}.ye{color:var(--yellow)}.re{color:var(--red);animation:blinkr .7s infinite;}
@keyframes blinkr{0%,100%{opacity:1}50%{opacity:.2}}
.hv.pu{color:var(--purple);}
/* timer */
.hud-timer{display:flex;flex-direction:column;gap:3px;min-width:130px;}
.timer-track{height:5px;border-radius:3px;background:rgba(255,255,255,.07);overflow:hidden;}
.timer-fill{height:100%;border-radius:3px;transition:width .2s linear,background .4s;}
.timer-num{font-family:var(--orb);font-size:.62rem;text-align:right;}
/* protocol badge */
.proto-badge{
  padding:5px 12px;border-radius:5px;font-family:var(--orb);font-size:.65rem;font-weight:700;
  letter-spacing:.1em;border:1px solid;}
.proto-rip{color:#ff8c00;border-color:rgba(255,140,0,.4);background:rgba(255,140,0,.07);}
.proto-ospf{color:var(--purple);border-color:rgba(180,79,255,.4);background:rgba(180,79,255,.07);}
.proto-bgp{color:var(--pink);border-color:rgba(255,77,255,.4);background:rgba(255,77,255,.07);}
/* tries */
.tries-row{display:flex;gap:4px;}
.pip{width:9px;height:9px;border-radius:50%;transition:all .3s;}
.pip.on{background:var(--green);box-shadow:0 0 6px rgba(0,255,157,.5);}
.pip.off{background:rgba(255,255,255,.1);}
/* back */
.btn-back{margin-left:auto;background:transparent;border:1px solid var(--border);border-radius:5px;
  padding:5px 12px;font-family:var(--orb);font-size:.58rem;color:var(--muted);cursor:pointer;
  transition:all .2s;letter-spacing:.08em;}
.btn-back:hover{border-color:var(--cyan);color:var(--cyan);}

/* ─ MAIN AREA ─ */
.main-area{flex:1;display:flex;min-height:0;}
#cv{flex:1;min-width:0;display:block;cursor:crosshair;}

/* ─ RIGHT PANEL ─ */
.rpanel{
  width:310px;flex-shrink:0;
  background:rgba(6,15,30,.98);border-left:1px solid var(--border);
  display:flex;flex-direction:column;overflow:hidden;}

/* Panel tabs */
.ptabs{display:flex;border-bottom:1px solid var(--border);}
.ptab{flex:1;padding:9px 4px;text-align:center;font-family:var(--orb);font-size:.5rem;
  letter-spacing:.1em;color:var(--muted);cursor:pointer;transition:all .2s;border-bottom:2px solid transparent;}
.ptab:hover{color:var(--txt);}
.ptab.active{color:var(--cyan);border-bottom-color:var(--cyan);}

.tab-pane{display:none;flex-direction:column;overflow:hidden;flex:1;}
.tab-pane.show{display:flex;}

/* Section */
.ps{padding:11px 13px;border-bottom:1px solid var(--border2);flex-shrink:0;}
.ps.grow{flex:1;overflow:hidden;display:flex;flex-direction:column;}
.pt{font-family:var(--orb);font-size:.48rem;letter-spacing:.25em;color:var(--cyan);
  margin-bottom:8px;display:flex;align-items:center;gap:6px;}
.pt::after{content:'';flex:1;height:1px;background:linear-gradient(to right,var(--border),transparent);}

/* Mission card */
.mc{background:linear-gradient(135deg,rgba(0,229,255,.05),rgba(0,50,180,.03));
  border:1px solid var(--border);border-radius:7px;padding:11px;}
.mc-h{display:flex;gap:9px;align-items:flex-start;margin-bottom:8px;}
.mc-ico{width:38px;height:38px;border-radius:7px;flex-shrink:0;
  background:var(--cg);border:1px solid var(--border);
  display:flex;align-items:center;justify-content:center;font-size:1.3rem;}
.mc-ttl{font-size:.88rem;font-weight:700;line-height:1.25;margin-bottom:2px;}
.mc-sub{font-family:var(--mono);font-size:.58rem;color:var(--cyan);}
.mc-route{display:flex;align-items:center;gap:6px;padding:6px 8px;
  background:rgba(0,0,0,.3);border-radius:5px;margin-bottom:6px;flex-wrap:wrap;}
.rn{font-family:var(--mono);font-size:.62rem;font-weight:700;padding:3px 8px;border-radius:3px;}
.rn.s{color:var(--green);background:rgba(0,255,157,.1);border:1px solid rgba(0,255,157,.25);}
.rn.d{color:var(--orange);background:rgba(255,140,0,.1);border:1px solid rgba(255,140,0,.25);}
.mc-reqs{display:flex;flex-direction:column;gap:3px;}
.req{display:flex;align-items:center;gap:6px;font-size:.72rem;padding:4px 7px;border-radius:4px;}
.req.ok{color:var(--green);background:rgba(0,255,157,.06);border:1px solid rgba(0,255,157,.15);}
.req.fail{color:var(--red);background:rgba(255,41,82,.06);border:1px solid rgba(255,41,82,.15);}
.req.neutral{color:var(--muted);background:rgba(255,255,255,.02);border:1px solid var(--border2);}
.req-key{font-family:var(--mono);font-size:.6rem;opacity:.7;min-width:90px;}

/* Routing table */
.rt{width:100%;border-collapse:collapse;}
.rt th{font-family:var(--orb);font-size:.45rem;letter-spacing:.1em;color:var(--muted);
  padding:4px 5px;text-align:left;border-bottom:1px solid var(--border2);}
.rt td{padding:4px 5px;font-family:var(--mono);font-size:.63rem;border-bottom:1px solid var(--border2);}
.rt tr:hover td{background:rgba(0,229,255,.03);}
.st{font-family:var(--orb);font-size:.48rem;font-weight:700;padding:2px 5px;border-radius:2px;}
.st.ok{color:var(--green);background:rgba(0,255,157,.08);}
.st.dn{color:var(--red);background:rgba(255,41,82,.09);}
.st.sel{color:var(--cyan);background:rgba(0,229,255,.09);}
.st.con{color:var(--purple);background:rgba(180,79,255,.09);}
.st.sat{color:var(--orange);background:rgba(255,140,0,.09);}

/* Gateway selector */
.gw-section{display:flex;flex-direction:column;gap:5px;}
.gw-row{
  display:flex;align-items:center;gap:6px;padding:6px 8px;border-radius:5px;
  border:1px solid var(--border2);background:rgba(0,0,0,.2);cursor:pointer;transition:all .2s;}
.gw-row:hover{border-color:var(--cyan);background:var(--cg);}
.gw-row.selected{border-color:var(--green);background:rgba(0,255,157,.06);}
.gw-row.blocked{opacity:.35;cursor:not-allowed;pointer-events:none;}
.gw-ip{font-family:var(--mono);font-size:.65rem;color:var(--cyan);flex:1;}
.gw-mask{font-family:var(--mono);font-size:.58rem;color:var(--muted);}
.gw-metric{font-family:var(--orb);font-size:.6rem;padding:2px 6px;border-radius:3px;}

/* Path builder */
.pb{min-height:34px;padding:6px 8px;background:rgba(0,0,0,.3);
  border:1px solid var(--border2);border-radius:5px;
  display:flex;flex-wrap:wrap;gap:3px;align-items:center;margin-bottom:7px;}
.pchip{padding:2px 8px;border-radius:3px;font-family:var(--mono);font-size:.58rem;
  border:1px solid;cursor:pointer;transition:filter .15s;display:flex;align-items:center;gap:3px;}
.pchip:hover{filter:brightness(1.4);}
.pchip.s{color:var(--green);border-color:rgba(0,255,157,.35);background:rgba(0,255,157,.06);}
.pchip.d{color:var(--orange);border-color:rgba(255,140,0,.35);background:rgba(255,140,0,.06);}
.pchip.m{color:var(--cyan);border-color:rgba(0,229,255,.25);background:rgba(0,229,255,.05);}
.pchip.bad{color:var(--red);border-color:rgba(255,41,82,.35);background:rgba(255,41,82,.05);}
.psep{color:var(--muted);font-size:.65rem;}
.pempty{font-size:.72rem;color:var(--muted);}

/* Metrics compare */
.metrics-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:5px;margin-bottom:7px;}
.mg{padding:7px 5px;border-radius:5px;text-align:center;background:rgba(0,0,0,.25);border:1px solid var(--border2);}
.mg-l{font-family:var(--orb);font-size:.44rem;color:var(--muted);letter-spacing:.08em;}
.mg-v{font-family:var(--orb);font-size:.82rem;font-weight:700;}

.btn-send{width:100%;padding:10px;border:none;border-radius:6px;
  background:linear-gradient(135deg,var(--green),#00aa60);
  font-family:var(--orb);font-size:.65rem;font-weight:700;color:var(--bg);
  letter-spacing:.12em;cursor:pointer;transition:all .2s;margin-bottom:5px;
  box-shadow:0 0 14px rgba(0,255,157,.15);}
.btn-send:hover:not(:disabled){transform:translateY(-1px);box-shadow:0 0 28px rgba(0,255,157,.4);}
.btn-send:disabled{opacity:.25;cursor:not-allowed;transform:none;box-shadow:none;}
.btn-rst{width:100%;padding:8px;border:1.5px solid rgba(255,41,82,.2);border-radius:6px;
  background:transparent;font-family:var(--orb);font-size:.6rem;font-weight:700;
  color:var(--red);letter-spacing:.1em;cursor:pointer;transition:all .2s;}
.btn-rst:hover{background:rgba(255,41,82,.06);border-color:var(--red);}

/* Log */
.log{flex:1;overflow-y:auto;display:flex;flex-direction:column;gap:3px;padding:8px 10px;}
.log::-webkit-scrollbar{width:3px;}
.log::-webkit-scrollbar-thumb{background:var(--border);border-radius:2px;}
.le{padding:4px 7px;border-radius:3px;font-family:var(--mono);font-size:.62rem;
  line-height:1.45;border-left:2px solid var(--border2);color:var(--muted);background:rgba(255,255,255,.01);}
.le.ok{border-color:var(--green);color:var(--green);background:rgba(0,255,157,.03);}
.le.er{border-color:var(--red);color:var(--red);background:rgba(255,41,82,.03);}
.le.wa{border-color:var(--yellow);color:var(--yellow);}
.le.in{border-color:var(--cyan);background:rgba(0,229,255,.02);}
.le.pu{border-color:var(--purple);color:var(--purple);}
.le.or{border-color:var(--orange);color:var(--orange);}
.lts{font-size:.5rem;opacity:.4;margin-right:4px;}

/* ── OVERLAY ── */
.ov{position:fixed;inset:0;z-index:500;background:rgba(2,8,16,.92);
  backdrop-filter:blur(16px);display:flex;align-items:center;justify-content:center;
  opacity:0;pointer-events:none;transition:opacity .4s;}
.ov.show{opacity:1;pointer-events:all;}
.ov-box{background:var(--bg2);border:1px solid var(--border);border-radius:12px;
  padding:38px 44px;max-width:500px;width:92%;text-align:center;
  box-shadow:0 0 80px rgba(0,229,255,.08);}
.ov-em{font-size:3rem;margin-bottom:10px;}
.ov-ttl{font-family:var(--orb);font-size:1.35rem;font-weight:900;margin-bottom:6px;}
.ov-ttl.ok{color:var(--green);text-shadow:0 0 24px rgba(0,255,157,.5);}
.ov-ttl.fail{color:var(--red);}
.ov-ttl.win{color:var(--yellow);text-shadow:0 0 24px rgba(255,214,0,.5);}
.ov-sub{color:var(--muted);font-size:.84rem;line-height:1.65;margin-bottom:12px;}
.ov-stats{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin:12px 0;
  padding:14px;background:rgba(0,0,0,.3);border-radius:7px;border:1px solid var(--border2);}
.os{text-align:center;}
.os-l{font-family:var(--orb);font-size:.48rem;letter-spacing:.1em;color:var(--muted);}
.os-v{font-family:var(--orb);font-size:.9rem;font-weight:700;}
.ov-hint{padding:9px 12px;margin-bottom:12px;
  background:rgba(255,140,0,.06);border:1px solid rgba(255,140,0,.18);border-radius:5px;
  font-family:var(--mono);font-size:.7rem;color:var(--orange);line-height:1.6;text-align:left;}
.ov-pts{font-family:var(--orb);font-size:1.15rem;color:var(--yellow);margin-bottom:18px;}
.btn-ov{width:100%;padding:13px;border:none;border-radius:7px;
  background:linear-gradient(135deg,var(--cyan),#004dcc);
  font-family:var(--orb);font-weight:700;font-size:.75rem;color:var(--bg);
  cursor:pointer;letter-spacing:.12em;transition:all .2s;}
.btn-ov:hover{transform:scale(1.03);}

/* ── TOOLTIP ── */
.tooltip{position:fixed;z-index:200;pointer-events:none;
  background:rgba(6,15,30,.97);border:1px solid var(--border);border-radius:6px;
  padding:8px 12px;font-family:var(--mono);font-size:.65rem;line-height:1.7;
  color:var(--txt);box-shadow:0 0 20px rgba(0,0,0,.5);min-width:200px;max-width:280px;
  opacity:0;transition:opacity .15s;}
.tooltip.show{opacity:1;}
.tt-title{font-family:var(--orb);font-size:.62rem;color:var(--cyan);margin-bottom:5px;letter-spacing:.1em;}
.tt-row{display:flex;justify-content:space-between;gap:12px;}
.tt-key{color:var(--muted);}
.tt-val{color:var(--txt);font-weight:700;}

/* Protocol help modal */
.modal{position:fixed;inset:0;z-index:600;background:rgba(2,8,16,.92);backdrop-filter:blur(12px);
  display:flex;align-items:center;justify-content:center;
  opacity:0;pointer-events:none;transition:opacity .3s;}
.modal.show{opacity:1;pointer-events:all;}
.modal-box{background:var(--bg2);border:1px solid var(--border);border-radius:10px;
  padding:28px 32px;max-width:620px;width:94%;max-height:85vh;overflow-y:auto;}
.modal-box::-webkit-scrollbar{width:4px;}
.modal-box::-webkit-scrollbar-thumb{background:var(--border);border-radius:2px;}
.modal-h{font-family:var(--orb);font-size:1rem;color:var(--cyan);margin-bottom:16px;letter-spacing:.1em;}
.modal-section{margin-bottom:16px;}
.modal-section h3{font-family:var(--orb);font-size:.65rem;color:var(--yellow);letter-spacing:.12em;margin-bottom:8px;}
.modal-section p,.modal-section li{font-size:.8rem;color:var(--muted);line-height:1.7;margin-bottom:4px;}
.modal-section code{font-family:var(--mono);color:var(--cyan);background:rgba(0,229,255,.08);
  padding:1px 5px;border-radius:3px;font-size:.72rem;}
.modal-close{width:100%;padding:11px;border:none;border-radius:6px;
  background:var(--cyan);font-family:var(--orb);font-size:.7rem;font-weight:700;
  color:var(--bg);cursor:pointer;letter-spacing:.1em;margin-top:8px;}
</style>
</head>
<body>

<!-- ══════════ INTRO ══════════ -->
<div id="sIntro" class="scr">
  <div class="intro-grid"></div>
  <div class="scan-line"></div>
  <div class="intro-inner">

    <div class="bx-hero">
      <svg width="120" height="138" viewBox="0 0 120 138" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <radialGradient id="bg" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#00e5ff" stop-opacity=".15"/><stop offset="100%" stop-color="transparent"/></radialGradient>
          <linearGradient id="body" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#eaf5ff"/><stop offset="100%" stop-color="#b8d5ee"/></linearGradient>
        </defs>
        <ellipse cx="60" cy="69" rx="55" ry="55" fill="url(#bg)"/>
        <ellipse cx="60" cy="88" rx="36" ry="40" fill="url(#body)"/>
        <ellipse cx="60" cy="46" rx="30" ry="28" fill="url(#body)"/>
        <line x1="32" y1="46" x2="88" y2="46" stroke="#0a1830" stroke-width="1.8"/>
        <ellipse cx="47" cy="44" rx="10" ry="6.5" fill="#0a1830"/>
        <ellipse cx="73" cy="44" rx="10" ry="6.5" fill="#0a1830"/>
        <ellipse cx="49" cy="41" rx="3" ry="2.2" fill="white" opacity=".6"/>
        <ellipse cx="75" cy="41" rx="3" ry="2.2" fill="white" opacity=".6"/>
        <circle cx="60" cy="87" r="13" fill="#060e1f" stroke="#00e5ff" stroke-width="1.5"/>
        <circle cx="60" cy="81" r="2.5" fill="#00e5ff"/>
        <circle cx="53" cy="92" r="2" fill="#00e5ff" opacity=".8"/>
        <circle cx="67" cy="92" r="2" fill="#00e5ff" opacity=".8"/>
        <line x1="60" y1="83.5" x2="53" y2="90" stroke="#00e5ff" stroke-width="1.2"/>
        <line x1="60" y1="83.5" x2="67" y2="90" stroke="#00e5ff" stroke-width="1.2"/>
        <ellipse cx="18" cy="84" rx="9" ry="24" fill="url(#body)" transform="rotate(-5,18,84)"/>
        <ellipse cx="102" cy="84" rx="9" ry="24" fill="url(#body)" transform="rotate(5,102,84)"/>
        <ellipse cx="44" cy="126" rx="9" ry="14" fill="url(#body)"/>
        <ellipse cx="76" cy="126" rx="9" ry="14" fill="url(#body)"/>
      </svg>
    </div>

    <div class="intro-logo">
      <div class="logo-sub">SIMULATEUR DE ROUTAGE RÉSEAU · NSI TERMINALE</div>
      <div class="logo-main">ROUTEX</div>
      <div class="logo-tag">v2.0 · RIP · OSPF · BGP · PROTOCOLS ENGINE</div>
    </div>

    <div class="intro-desc">
      Maîtrise les protocoles <b>RIP</b>, <b>OSPF</b> et <b>BGP</b>. Gère les tables de routage, 
      négocie les passerelles, respecte les contraintes de <b>bande passante</b>, <b>TTL</b> et <b>masques de sous-réseau</b>. 
      Chaque niveau est un vrai scénario réseau d'entreprise — le chemin le plus court <b>n'est pas toujours le meilleur</b>.
    </div>

    <div class="lvl-grid" id="lvlGrid"></div>

    <div class="cta-row">
      <button class="btn-a" id="btnStart" onclick="startSelected()">▶ LANCER LE NIVEAU</button>

    </div>
  </div>
</div>

<!-- ══════════ GAME ══════════ -->
<div id="sGame" class="scr off">
  <div class="hud">
    <div class="hud-brand">⬡ ROUTEX</div>
    <div class="hud-sep"></div>
    <div class="hb"><span class="hl">NIVEAU</span><span class="hv cy" id="hLvl">—</span></div>
    <div class="hud-sep"></div>
    <div class="hb"><span class="hl">PROTOCOLE</span><div id="hProto"></div></div>
    <div class="hud-sep"></div>
    <div class="hb"><span class="hl">SCORE</span><span class="hv ye" id="hScore">0</span></div>
    <div class="hud-sep"></div>
    <div class="hb"><span class="hl">VIES</span><div class="tries-row" id="hTries"></div></div>
    <div class="hud-sep"></div>
    <div class="hb"><span class="hl">PANNES</span><span class="hv re" id="hDowns">0</span></div>
    <div class="hud-sep"></div>
    <div class="hb"><span class="hl">TTL PAQUET</span><span class="hv" id="hTTL" style="color:var(--yellow)">64</span></div>
    <div class="hud-sep"></div>
    <div class="hud-timer">
      <div class="hl">TEMPS RESTANT</div>
      <div class="timer-track"><div class="timer-fill" id="timerFill" style="width:100%"></div></div>
      <div class="timer-num" id="timerNum">60s</div>
    </div>
    <button class="btn-back" onclick="goIntro()">← MENU</button>
  </div>

  <div class="main-area">
    <canvas id="cv"></canvas>
    <div class="rpanel">
      <div class="ptabs">
        <div class="ptab active" data-tab="mission" onclick="switchTab('mission')">MISSION</div>
        <div class="ptab" data-tab="routing" onclick="switchTab('routing')">ROUTAGE</div>
        <div class="ptab" data-tab="path" onclick="switchTab('path')">CHEMIN</div>
        <div class="ptab" data-tab="log" onclick="switchTab('log')">LOG</div>
      </div>

      <!-- TAB: MISSION -->
      <div class="tab-pane show" id="tab-mission">
        <div class="ps">
          <div class="pt">Objectif Mission</div>
          <div class="mc">
            <div class="mc-h">
              <div class="mc-ico" id="mIcon">📦</div>
              <div><div class="mc-ttl" id="mTitle">—</div><div class="mc-sub" id="mSub">—</div></div>
            </div>
            <div class="mc-route">
              <div class="rn s" id="mFrom">—</div>
              <span style="color:var(--muted);font-size:.7rem">──▶</span>
              <div class="rn d" id="mTo">—</div>
              <span style="color:var(--muted);font-size:.65rem;margin-left:4px" id="mVia"></span>
            </div>
            <div class="mc-reqs" id="mReqs"></div>
          </div>
        </div>
        <div class="ps">
          <div class="pt">Contraintes Actives</div>
          <div id="constraintsEl"></div>
        </div>
        <div class="ps">
          <div class="pt">Passerelle Active</div>
          <div class="gw-section" id="gwSection"></div>
        </div>
        <div class="ps" style="border-bottom:none;">
          <div class="pt">Description</div>
          <div style="font-size:.74rem;color:var(--muted);line-height:1.65;" id="mDesc">—</div>
        </div>
      </div>

      <!-- TAB: ROUTING -->
      <div class="tab-pane" id="tab-routing">
        <div class="ps grow" style="border-bottom:none;">
          <div class="pt">Table de Routage Complète</div>
          <div style="overflow-y:auto;flex:1;">
            <table class="rt" id="routingTable">
              <thead><tr>
                <th>Nœud</th><th>IP/Masque</th><th>Proto</th>
                <th>BW(Mbps)</th><th>État</th>
              </tr></thead>
              <tbody id="rtBody"></tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- TAB: PATH -->
      <div class="tab-pane" id="tab-path">
        <div class="ps">
          <div class="pt">Chemin Construit</div>
          <div class="pb" id="pathBuilder"><span class="pempty">Clique sur SOURCE pour démarrer</span></div>
          <div class="metrics-grid">
            <div class="mg"><div class="mg-l">COÛT TOTAL</div><div class="mg-v" id="mgMine" style="color:var(--cyan)">—</div></div>
            <div class="mg"><div class="mg-l">TTL RESTANT</div><div class="mg-v" id="mgTTL" style="color:var(--yellow)">—</div></div>
            <div class="mg"><div class="mg-l">SAUTS</div><div class="mg-v" id="mgHops" style="color:var(--purple)">—</div></div>
          </div>
          <div id="mgOpt" style="display:none"></div>
          <div class="mg" style="margin-bottom:7px;padding:6px 8px;">
            <div class="mg-l">BW GOULOT D'ÉTRANGLEMENT</div>
            <div class="mg-v" id="mgBW" style="color:var(--orange);font-size:.72rem">—</div>
          </div>
          <button class="btn-send" id="btnSend" disabled onclick="sendPacket()">⬆ ENVOYER LE PAQUET</button>
          <button class="btn-rst" onclick="resetPath()">✕ RÉINITIALISER CHEMIN</button>
        </div>
        <div class="ps grow" style="border-bottom:none;">
          <div class="pt">Analyse du Chemin</div>
          <div style="overflow-y:auto;flex:1;" id="pathAnalysis">
            <span style="font-size:.72rem;color:var(--muted)">Construit un chemin pour voir l'analyse.</span>
          </div>
        </div>
      </div>

      <!-- TAB: LOG -->
      <div class="tab-pane" id="tab-log">
        <div class="ps grow" style="border-bottom:none;padding:0;">
          <div class="log" id="logEl"></div>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- TOOLTIP -->
<div class="tooltip" id="tooltip"></div>

<!-- OVERLAY -->
<div class="ov" id="ov">
  <div class="ov-box">
    <div class="ov-em" id="ovEm">🎉</div>
    <div class="ov-ttl ok" id="ovTtl">—</div>
    <div class="ov-sub" id="ovSub">—</div>
    <div class="ov-stats" id="ovStats"></div>
    <div class="ov-hint" id="ovHint" style="display:none"></div>
    <div class="ov-pts" id="ovPts"></div>
    <button class="btn-ov" id="ovBtn">CONTINUER</button>
  </div>
</div>

<!-- PROTOCOL HELP MODAL -->
<div class="modal" id="helpModal">
  <div class="modal-box">
    <div class="modal-h">📡 GUIDE DES PROTOCOLES — TERMINALE NSI</div>
    <div class="modal-section">
      <h3>🔴 RIP — Routing Information Protocol</h3>
      <p>Métrique = <b>nombre de sauts</b> (hops). Maximum 15 sauts. Au-delà = réseau inaccessible.</p>
      <p>Mise à jour toutes les <b>30 secondes</b>. Convergence lente. Utilisé sur les petits réseaux.</p>
      <p>Dans ROUTEX : <code>coût = nb_sauts × 1</code>. Cherche le chemin avec le moins de routeurs intermédiaires.</p>
    </div>
    <div class="modal-section">
      <h3>🟣 OSPF — Open Shortest Path First</h3>
      <p>Métrique = <b>coût inversement proportionnel à la bande passante</b> : <code>coût = 100 / bande_passante(Mbps)</code></p>
      <p>Convergence rapide (LSA flooding). Supporte les grandes topologies. État de lien complet.</p>
      <p>Dans ROUTEX : un lien 1000 Mbps coûte 0.1, un lien 10 Mbps coûte 10. Favorise les liens haut débit.</p>
    </div>
    <div class="modal-section">
      <h3>🟡 BGP — Border Gateway Protocol</h3>
      <p>Protocole de routage <b>inter-AS</b> (entre systèmes autonomes). Politique-driven.</p>
      <p>Métrique = <b>AS-PATH length</b> + attributs de politique. Peut ignorer le chemin le plus court pour des raisons de politique.</p>
      <p>Dans ROUTEX : certains liens ont des politiques BGP qui bloquent ou pénalisent certaines routes.</p>
    </div>
    <div class="modal-section">
      <h3>⚡ TTL — Time To Live</h3>
      <p>Chaque paquet démarre avec TTL=64. Chaque saut <b>décrémente TTL de 1</b>. Si TTL=0 : paquet détruit !</p>
      <p>Sur un chemin de 10 sauts, TTL final = 54. Les chemins trop longs peuvent tuer le paquet.</p>
    </div>
    <div class="modal-section">
      <h3>🔒 Masques de sous-réseau et passerelles</h3>
      <p>Pour qu'un routeur accepte un paquet, son <b>réseau de destination</b> doit correspondre à l'adresse IP cible masquée.</p>
      <p>Ex: IP <code>192.168.1.45</code> avec masque <code>/24</code> → réseau <code>192.168.1.0</code>.</p>
      <p>Tu dois parfois <b>changer de passerelle</b> (gateway) pour traverser un sous-réseau différent.</p>
    </div>
    <div class="modal-section">
      <h3>📶 Bande passante et congestion</h3>
      <p>Chaque lien a une <b>bande passante maximale</b>. Si un lien est saturé (congestion), son coût augmente dynamiquement.</p>
      <p>Le <b>goulot d'étranglement</b> (bottleneck) est le lien le plus lent de ton chemin — il détermine la vitesse globale.</p>
    </div>
    <button class="modal-close" onclick="document.getElementById('helpModal').classList.remove('show')">COMPRIS — FERMER</button>
  </div>
</div>

<script>
'use strict';

// ═══════════════════════════════════════════════════════════════════════
//  DIJKSTRA (générique, supporte plusieurs modes de coût)
// ═══════════════════════════════════════════════════════════════════════
function dijkstra(nodes, edges, downNodes, src, dst, costMode='cost', gatewayFilter=null) {
  const dist={}, prev={}, vis=new Set();
  nodes.forEach(n=>dist[n.id]=Infinity);
  dist[src]=0;
  const q=nodes.map(n=>n.id).filter(id=>!downNodes.includes(id)||id===src||id===dst);
  while(q.length){
    q.sort((a,b)=>dist[a]-dist[b]);
    const u=q.shift();
    if(vis.has(u))continue;
    vis.add(u);
    if(u===dst)break;
    for(const e of edges){
      let nb=null;
      if(e.u===u)nb=e.v; else if(e.v===u)nb=e.u;
      if(!nb)continue;
      if(downNodes.includes(nb)&&nb!==dst)continue;
      if(gatewayFilter&&e.gateway&&e.gateway!==gatewayFilter)continue;
      let w=e.cost;
      if(costMode==='ospf') w=Math.round(100/Math.max(e.bandwidth||1,1)*10)/10;
      else if(costMode==='rip') w=1;
      else if(costMode==='bgp') w=(e.aspath||1);
      const alt=dist[u]+w;
      if(alt<dist[nb]){dist[nb]=alt;prev[nb]=u;}
    }
  }
  if(!isFinite(dist[dst]))return null;
  const path=[]; let c=dst;
  while(c){path.unshift(c);c=prev[c];}
  return{path,cost:Math.round(dist[dst]*100)/100};
}

// ═══════════════════════════════════════════════════════════════════════
//  LEVEL DEFINITIONS — 4 niveaux, topologies réalistes
// ═══════════════════════════════════════════════════════════════════════
const LEVELS=[
// ────── NIVEAU 1 : RIP ──────
{id:1,name:'LAN Entreprise',protocol:'RIP',diff:2,timeLimit:75,
 desc:'Initiation au routage RIP. La métrique est le nombre de sauts. Attention : le chemin direct n\\'est pas forcément le plus court en sauts !',
 nodes:[
  {id:'PC1',  ip:'192.168.1.10',  mask:'/24', x:.06,y:.5,  type:'source',bw:100,proto:'RIP'},
  {id:'R1',   ip:'192.168.1.1',   mask:'/24', x:.2, y:.25, type:'router',bw:100,proto:'RIP'},
  {id:'R2',   ip:'192.168.1.2',   mask:'/24', x:.2, y:.75, type:'router',bw:100,proto:'RIP'},
  {id:'R3',   ip:'192.168.2.1',   mask:'/24', x:.38,y:.15, type:'router',bw:100,proto:'RIP'},
  {id:'R4',   ip:'192.168.2.2',   mask:'/24', x:.38,y:.5,  type:'router',bw:100,proto:'RIP'},
  {id:'R5',   ip:'192.168.2.3',   mask:'/24', x:.38,y:.85, type:'router',bw:100,proto:'RIP'},
  {id:'R6',   ip:'192.168.3.1',   mask:'/24', x:.56,y:.3,  type:'router',bw:100,proto:'RIP'},
  {id:'R7',   ip:'192.168.3.2',   mask:'/24', x:.56,y:.65, type:'router',bw:100,proto:'RIP'},
  {id:'R8',   ip:'192.168.4.1',   mask:'/24', x:.72,y:.45, type:'router',bw:100,proto:'RIP'},
  {id:'SRV',  ip:'192.168.5.100', mask:'/24', x:.88,y:.5,  type:'dest',  bw:100,proto:'RIP'},
 ],
 edges:[
  {u:'PC1',v:'R1', cost:1,bandwidth:100},
  {u:'PC1',v:'R2', cost:1,bandwidth:100},
  {u:'R1', v:'R3', cost:1,bandwidth:100},
  {u:'R1', v:'R4', cost:1,bandwidth:100},
  {u:'R2', v:'R4', cost:1,bandwidth:100},
  {u:'R2', v:'R5', cost:1,bandwidth:100},
  {u:'R3', v:'R6', cost:1,bandwidth:100},
  {u:'R4', v:'R6', cost:1,bandwidth:100},
  {u:'R4', v:'R7', cost:1,bandwidth:100},
  {u:'R5', v:'R7', cost:1,bandwidth:100},
  {u:'R6', v:'R8', cost:1,bandwidth:100},
  {u:'R7', v:'R8', cost:1,bandwidth:100},
  {u:'R8', v:'SRV',cost:1,bandwidth:100},
  {u:'R3', v:'R4', cost:1,bandwidth:100},
 ],
 gateways:[
  {id:'GW-A',ip:'192.168.1.254',mask:'/24',desc:'Passerelle LAN-A',color:'#00ff9d'},
  {id:'GW-B',ip:'192.168.2.254',mask:'/24',desc:'Passerelle LAN-B',color:'#00e5ff'},
 ],
 missions:[
  {from:'PC1',to:'SRV',icon:'📧',type:'E-MAIL',title:'Premier Mail',
   desc:'Envoie un e-mail. En RIP, la métrique = nombre de sauts. Attention : R3 tombe à T+20s et R7 à T+35s. Anticipe les pannes !',
   pts:300,ttl:58,requiredGW:'GW-A',
   downNodes:['R1'],dynamicFailures:[{node:'R3',at:20,type:'overload'},{node:'R7',at:35,type:'fire'}],
   constraints:[
    {key:'Protocole',val:'RIP (sauts)',type:'info'},
    {key:'TTL initial',val:'58',type:'warn'},
    {key:'R1',val:'HORS LIGNE',type:'fail'},
    {key:'R3',val:'Surcharge à T+20s',type:'warn'},
    {key:'R7',val:'Incendie à T+35s',type:'warn'},
    {key:'Passerelle',val:'GW-A obligatoire',type:'warn'},
   ],
   costMode:'rip'},
  {from:'PC1',to:'SRV',icon:'📁',type:'FICHIER',title:'Transfert en Cascade',
   desc:'R4 et R1 déjà hors ligne. R6 tombe à T+15s, R8 à T+25s. Le TTL est serré à 52. Il reste UN chemin viable — trouve-le vite.',
   pts:500,ttl:52,requiredGW:null,
   downNodes:['R4','R1'],dynamicFailures:[{node:'R6',at:15,type:'overload'},{node:'R8',at:25,type:'hack'}],
   constraints:[
    {key:'Protocole',val:'RIP',type:'info'},
    {key:'R4 + R1',val:'HORS LIGNE',type:'fail'},
    {key:'R6',val:'Saturation à T+15s',type:'warn'},
    {key:'R8',val:'Cyberattaque à T+25s',type:'warn'},
    {key:'TTL',val:'52 — SERRÉ',type:'fail'},
   ],
   costMode:'rip'},
 ]
},

// ────── NIVEAU 2 : OSPF ──────
{id:2,name:'WAN Régional',protocol:'OSPF',diff:3,timeLimit:60,
 desc:'OSPF : coût = 100/bande_passante. Tu dois calculer les coûts toi-même. Les métriques ne sont plus affichées — connais ta formule !',
 nodes:[
  {id:'H1',  ip:'10.0.1.1',  mask:'/30',x:.05,y:.5,  type:'source',bw:1000,proto:'OSPF'},
  {id:'A',   ip:'10.0.1.2',  mask:'/30',x:.18,y:.2,  type:'router',bw:1000,proto:'OSPF'},
  {id:'B',   ip:'10.0.2.1',  mask:'/30',x:.18,y:.5,  type:'router',bw:500, proto:'OSPF'},
  {id:'C',   ip:'10.0.3.1',  mask:'/30',x:.18,y:.8,  type:'router',bw:100, proto:'OSPF'},
  {id:'D',   ip:'10.0.4.1',  mask:'/30',x:.34,y:.12, type:'router',bw:1000,proto:'OSPF'},
  {id:'E',   ip:'10.0.4.2',  mask:'/30',x:.34,y:.38, type:'router',bw:100, proto:'OSPF'},
  {id:'F',   ip:'10.0.5.1',  mask:'/30',x:.34,y:.62, type:'router',bw:1000,proto:'OSPF'},
  {id:'G',   ip:'10.0.5.2',  mask:'/30',x:.34,y:.88, type:'router',bw:10,  proto:'OSPF'},
  {id:'I',   ip:'10.0.6.1',  mask:'/30',x:.52,y:.25, type:'router',bw:500, proto:'OSPF'},
  {id:'J',   ip:'10.0.6.2',  mask:'/30',x:.52,y:.55, type:'router',bw:1000,proto:'OSPF'},
  {id:'K',   ip:'10.0.7.1',  mask:'/30',x:.52,y:.8,  type:'router',bw:100, proto:'OSPF'},
  {id:'L',   ip:'10.0.8.1',  mask:'/30',x:.68,y:.35, type:'router',bw:1000,proto:'OSPF'},
  {id:'M',   ip:'10.0.8.2',  mask:'/30',x:.68,y:.65, type:'router',bw:500, proto:'OSPF'},
  {id:'H2',  ip:'10.0.9.1',  mask:'/30',x:.86,y:.5,  type:'dest',  bw:1000,proto:'OSPF'},
 ],
 edges:[
  {u:'H1',v:'A',  bandwidth:1000,cost:0.1},
  {u:'H1',v:'B',  bandwidth:500, cost:0.2},
  {u:'H1',v:'C',  bandwidth:100, cost:1},
  {u:'A', v:'D',  bandwidth:1000,cost:0.1},
  {u:'A', v:'E',  bandwidth:100, cost:1},
  {u:'B', v:'E',  bandwidth:500, cost:0.2},
  {u:'B', v:'F',  bandwidth:1000,cost:0.1},
  {u:'C', v:'F',  bandwidth:100, cost:1},
  {u:'C', v:'G',  bandwidth:10,  cost:10},
  {u:'D', v:'I',  bandwidth:1000,cost:0.1},
  {u:'E', v:'I',  bandwidth:100, cost:1},
  {u:'E', v:'J',  bandwidth:100, cost:1},
  {u:'F', v:'J',  bandwidth:1000,cost:0.1},
  {u:'F', v:'K',  bandwidth:100, cost:1},
  {u:'G', v:'K',  bandwidth:10,  cost:10},
  {u:'I', v:'L',  bandwidth:1000,cost:0.1},
  {u:'J', v:'L',  bandwidth:500, cost:0.2},
  {u:'J', v:'M',  bandwidth:500, cost:0.2},
  {u:'K', v:'M',  bandwidth:100, cost:1},
  {u:'L', v:'H2', bandwidth:1000,cost:0.1},
  {u:'M', v:'H2', bandwidth:500, cost:0.2},
  {u:'D', v:'E',  bandwidth:100, cost:1},
  {u:'I', v:'J',  bandwidth:500, cost:0.2},
 ],
 gateways:[
  {id:'GW-OSPF1',ip:'10.0.0.1',mask:'/30',desc:'Area 0 Backbone',color:'#b44fff'},
  {id:'GW-OSPF2',ip:'10.0.0.2',mask:'/30',desc:'Area 1 Secondaire',color:'#00e5ff'},
 ],
 missions:[
  {from:'H1',to:'H2',icon:'🎥',type:'VIDÉO 4K',title:'Stream 4K Backbone',
   desc:'Streaming vidéo 4K. Maximise la BW (minimise coût OSPF). I et D tombent à T+18s. Calcule le coût optimal AVANT qu\\'ils ne tombent !',
   pts:500,ttl:56,requiredGW:'GW-OSPF1',
   downNodes:['G'],dynamicFailures:[{node:'I',at:18,type:'overload'},{node:'D',at:22,type:'fire'}],
   constraints:[
    {key:'Protocole',val:'OSPF — coût=100/BW',type:'info'},
    {key:'G',val:'HORS LIGNE',type:'fail'},
    {key:'I',val:'Surcharge à T+18s',type:'warn'},
    {key:'D',val:'Incendie à T+22s',type:'warn'},
    {key:'TTL',val:'56',type:'warn'},
    {key:'Passerelle',val:'GW-OSPF1 Area0',type:'warn'},
   ],
   costMode:'ospf'},
  {from:'H1',to:'H2',icon:'💰',type:'BANQUE',title:'Transaction Financière',
   desc:'Transaction critique. E, J et B sont déjà saturés. K tombe à T+12s, F à T+20s. TTL=44. Il te reste peu d\\'options. Réfléchis vite.',
   pts:800,ttl:44,requiredGW:'GW-OSPF1',
   downNodes:['E','B'],dynamicFailures:[{node:'K',at:12,type:'overload'},{node:'F',at:20,type:'fire'},{node:'J',at:25,type:'hack'}],
   constraints:[
    {key:'TTL',val:'44 — CRITIQUE',type:'fail'},
    {key:'E + B',val:'DOWN',type:'fail'},
    {key:'K',val:'Surcharge à T+12s',type:'warn'},
    {key:'F',val:'Incendie à T+20s',type:'warn'},
    {key:'J',val:'Cyberattaque à T+25s',type:'warn'},
   ],
   costMode:'ospf'},
 ]
},

// ────── NIVEAU 3 : OSPF + BGP + Multi-AS ──────
{id:3,name:'Backbone Inter-AS',protocol:'OSPF/BGP',diff:4,timeLimit:50,
 desc:'Réseau multi-AS. Liens BGP bloqués selon politiques. Change de passerelle pour traverser les AS. Aucune aide — débrouille-toi.',
 nodes:[
  {id:'AS1-R1',ip:'172.16.1.1',  mask:'/28',x:.05,y:.5,  type:'source',bw:1000,proto:'BGP',as:1},
  {id:'AS1-R2',ip:'172.16.1.2',  mask:'/28',x:.16,y:.25, type:'router',bw:1000,proto:'BGP',as:1},
  {id:'AS1-R3',ip:'172.16.1.3',  mask:'/28',x:.16,y:.75, type:'router',bw:500, proto:'BGP',as:1},
  {id:'AS1-R4',ip:'172.16.2.1',  mask:'/28',x:.28,y:.15, type:'router',bw:1000,proto:'OSPF',as:1},
  {id:'AS1-R5',ip:'172.16.2.2',  mask:'/28',x:.28,y:.5,  type:'router',bw:100, proto:'OSPF',as:1},
  {id:'AS1-R6',ip:'172.16.2.3',  mask:'/28',x:.28,y:.85, type:'router',bw:500, proto:'OSPF',as:1},
  // AS2
  {id:'AS2-R1',ip:'172.16.10.1', mask:'/28',x:.44,y:.2,  type:'router',bw:1000,proto:'BGP',as:2},
  {id:'AS2-R2',ip:'172.16.10.2', mask:'/28',x:.44,y:.5,  type:'router',bw:500, proto:'BGP',as:2},
  {id:'AS2-R3',ip:'172.16.10.3', mask:'/28',x:.44,y:.8,  type:'router',bw:1000,proto:'BGP',as:2},
  {id:'AS2-R4',ip:'172.16.11.1', mask:'/28',x:.58,y:.35, type:'router',bw:100, proto:'BGP',as:2},
  {id:'AS2-R5',ip:'172.16.11.2', mask:'/28',x:.58,y:.65, type:'router',bw:1000,proto:'BGP',as:2},
  // AS3
  {id:'AS3-R1',ip:'172.16.20.1', mask:'/28',x:.72,y:.25, type:'router',bw:1000,proto:'OSPF',as:3},
  {id:'AS3-R2',ip:'172.16.20.2', mask:'/28',x:.72,y:.55, type:'router',bw:500, proto:'OSPF',as:3},
  {id:'AS3-R3',ip:'172.16.20.3', mask:'/28',x:.72,y:.82, type:'router',bw:100, proto:'OSPF',as:3},
  {id:'AS3-DST',ip:'172.16.21.1',mask:'/28',x:.88,y:.5,  type:'dest',  bw:1000,proto:'OSPF',as:3},
 ],
 edges:[
  // AS1 interne
  {u:'AS1-R1',v:'AS1-R2',bandwidth:1000,cost:0.1,aspath:1},
  {u:'AS1-R1',v:'AS1-R3',bandwidth:500, cost:0.2,aspath:1},
  {u:'AS1-R2',v:'AS1-R4',bandwidth:1000,cost:0.1,aspath:1},
  {u:'AS1-R2',v:'AS1-R5',bandwidth:100, cost:1,  aspath:1},
  {u:'AS1-R3',v:'AS1-R5',bandwidth:500, cost:0.2,aspath:1},
  {u:'AS1-R3',v:'AS1-R6',bandwidth:500, cost:0.2,aspath:1},
  // AS1→AS2 eBGP (peering)
  {u:'AS1-R4',v:'AS2-R1',bandwidth:1000,cost:0.1,aspath:2,ebgp:true},
  {u:'AS1-R5',v:'AS2-R2',bandwidth:100, cost:1,  aspath:2,ebgp:true},
  {u:'AS1-R6',v:'AS2-R3',bandwidth:500, cost:0.2,aspath:2,ebgp:true,blocked:true},
  // AS2 interne
  {u:'AS2-R1',v:'AS2-R2',bandwidth:1000,cost:0.1,aspath:1},
  {u:'AS2-R1',v:'AS2-R4',bandwidth:500, cost:0.2,aspath:1},
  {u:'AS2-R2',v:'AS2-R4',bandwidth:500, cost:0.2,aspath:1},
  {u:'AS2-R2',v:'AS2-R5',bandwidth:1000,cost:0.1,aspath:1},
  {u:'AS2-R3',v:'AS2-R5',bandwidth:1000,cost:0.1,aspath:1},
  // AS2→AS3 eBGP
  {u:'AS2-R4',v:'AS3-R1',bandwidth:1000,cost:0.1,aspath:2,ebgp:true},
  {u:'AS2-R5',v:'AS3-R2',bandwidth:500, cost:0.2,aspath:2,ebgp:true},
  {u:'AS2-R5',v:'AS3-R3',bandwidth:100, cost:1,  aspath:2,ebgp:true},
  // AS3 interne
  {u:'AS3-R1',v:'AS3-R2',bandwidth:500, cost:0.2,aspath:1},
  {u:'AS3-R1',v:'AS3-DST',bandwidth:1000,cost:0.1,aspath:1},
  {u:'AS3-R2',v:'AS3-DST',bandwidth:500, cost:0.2,aspath:1},
  {u:'AS3-R3',v:'AS3-R2',bandwidth:100, cost:1,  aspath:1},
 ],
 gateways:[
  {id:'GW-AS1',ip:'172.16.1.254',mask:'/28',desc:'eBGP AS1 → AS2 Nord',color:'#00e5ff'},
  {id:'GW-AS1B',ip:'172.16.1.253',mask:'/28',desc:'eBGP AS1 → AS2 Centre',color:'#00ff9d'},
 ],
 missions:[
  {from:'AS1-R1',to:'AS3-DST',icon:'🌐',type:'BGP INTER-AS',title:'Peering Inter-AS',
   desc:'Traverse 3 AS. Le lien AS1-R6→AS2-R3 est BLOQUÉ. AS1-R3 tombe à T+15s, AS2-R4 à T+22s. TTL=46. Agis avant les pannes.',
   pts:700,ttl:46,requiredGW:'GW-AS1',
   downNodes:['AS1-R5'],dynamicFailures:[{node:'AS1-R3',at:15,type:'fire'},{node:'AS2-R4',at:22,type:'hack'}],
   constraints:[
    {key:'Lien bloqué',val:'AS1-R6 → AS2-R3',type:'fail'},
    {key:'AS1-R5',val:'DOWN',type:'fail'},
    {key:'AS1-R3',val:'Incendie T+15s',type:'warn'},
    {key:'AS2-R4',val:'Cyberattaque T+22s',type:'warn'},
    {key:'TTL',val:'46 — COURT',type:'fail'},
    {key:'GW requise',val:'GW-AS1 (Nord)',type:'warn'},
   ],
   costMode:'ospf'},
  {from:'AS1-R1',to:'AS3-DST',icon:'🔐',type:'VPN CHIFFRÉ',title:'Tunnel VPN Critique',
   desc:'AS2-R2 tombe à T+10s, AS3-R1 à T+18s, AS2-R1 à T+28s. TTL=42. 50 secondes chrono. Il faut choisir le bon chemin immédiatement.',
   pts:1000,ttl:42,requiredGW:'GW-AS1B',
   downNodes:['AS1-R5','AS1-R3'],dynamicFailures:[{node:'AS2-R2',at:10,type:'hack'},{node:'AS3-R1',at:18,type:'fire'},{node:'AS2-R1',at:28,type:'flood'}],
   constraints:[
    {key:'TTL',val:'42 — TRÈS COURT',type:'fail'},
    {key:'AS1-R5 + AS1-R3',val:'DOWN',type:'fail'},
    {key:'AS2-R2',val:'Cyberattaque T+10s',type:'warn'},
    {key:'AS3-R1',val:'Incendie T+18s',type:'warn'},
    {key:'AS2-R1',val:'Inondation T+28s',type:'warn'},
   ],
   costMode:'ospf'},
 ]
},

// ────── NIVEAU 4 : BOSS — Réseau Opérateur ──────
{id:4,name:'OPÉRATEUR TÉLÉCOM',protocol:'BGP/OSPF',diff:5,timeLimit:40,
 desc:'Infrastructure d\\'opérateur. 16 nœuds actifs, pannes en cascade, contraintes TTL serrées, politiques BGP, 55 secondes. Seuls les experts passent.',
 nodes:[
  {id:'SRC', ip:'10.100.1.1',  mask:'/30',x:.04,y:.5,  type:'source',bw:10000,proto:'BGP',as:100},
  {id:'PE1', ip:'10.100.1.2',  mask:'/30',x:.14,y:.2,  type:'router',bw:10000,proto:'BGP',as:100},
  {id:'PE2', ip:'10.100.1.3',  mask:'/30',x:.14,y:.5,  type:'router',bw:5000, proto:'BGP',as:100},
  {id:'PE3', ip:'10.100.1.4',  mask:'/30',x:.14,y:.8,  type:'router',bw:1000, proto:'BGP',as:100},
  {id:'P1',  ip:'10.100.2.1',  mask:'/30',x:.27,y:.12, type:'router',bw:10000,proto:'BGP',as:100},
  {id:'P2',  ip:'10.100.2.2',  mask:'/30',x:.27,y:.38, type:'router',bw:10000,proto:'BGP',as:100},
  {id:'P3',  ip:'10.100.2.3',  mask:'/30',x:.27,y:.62, type:'router',bw:5000, proto:'BGP',as:100},
  {id:'P4',  ip:'10.100.2.4',  mask:'/30',x:.27,y:.88, type:'router',bw:1000, proto:'BGP',as:100},
  {id:'CR1', ip:'10.200.1.1',  mask:'/30',x:.44,y:.25, type:'router',bw:10000,proto:'OSPF',as:200},
  {id:'CR2', ip:'10.200.1.2',  mask:'/30',x:.44,y:.55, type:'router',bw:10000,proto:'OSPF',as:200},
  {id:'CR3', ip:'10.200.1.3',  mask:'/30',x:.44,y:.82, type:'router',bw:5000, proto:'OSPF',as:200},
  {id:'CE1', ip:'10.200.2.1',  mask:'/30',x:.6, y:.18, type:'router',bw:10000,proto:'OSPF',as:200},
  {id:'CE2', ip:'10.200.2.2',  mask:'/30',x:.6, y:.45, type:'router',bw:5000, proto:'OSPF',as:200},
  {id:'CE3', ip:'10.200.2.3',  mask:'/30',x:.6, y:.75, type:'router',bw:1000, proto:'OSPF',as:200},
  {id:'BR1', ip:'10.300.1.1',  mask:'/30',x:.76,y:.38, type:'router',bw:10000,proto:'OSPF',as:300},
  {id:'BR2', ip:'10.300.1.2',  mask:'/30',x:.76,y:.65, type:'router',bw:5000, proto:'OSPF',as:300},
  {id:'DST', ip:'10.300.2.1',  mask:'/30',x:.9, y:.5,  type:'dest',  bw:10000,proto:'OSPF',as:300},
 ],
 edges:[
  {u:'SRC',v:'PE1',bandwidth:10000,cost:0.01,aspath:1},
  {u:'SRC',v:'PE2',bandwidth:5000, cost:0.02,aspath:1},
  {u:'SRC',v:'PE3',bandwidth:1000, cost:0.1, aspath:1},
  {u:'PE1',v:'P1', bandwidth:10000,cost:0.01,aspath:1},
  {u:'PE1',v:'P2', bandwidth:5000, cost:0.02,aspath:1},
  {u:'PE2',v:'P2', bandwidth:10000,cost:0.01,aspath:1},
  {u:'PE2',v:'P3', bandwidth:5000, cost:0.02,aspath:1},
  {u:'PE3',v:'P3', bandwidth:1000, cost:0.1, aspath:1},
  {u:'PE3',v:'P4', bandwidth:1000, cost:0.1, aspath:1},
  // P→CR (eBGP AS100→AS200)
  {u:'P1',v:'CR1', bandwidth:10000,cost:0.01,aspath:2,ebgp:true},
  {u:'P2',v:'CR1', bandwidth:5000, cost:0.02,aspath:2,ebgp:true},
  {u:'P2',v:'CR2', bandwidth:10000,cost:0.01,aspath:2,ebgp:true},
  {u:'P3',v:'CR2', bandwidth:5000, cost:0.02,aspath:2,ebgp:true},
  {u:'P3',v:'CR3', bandwidth:1000, cost:0.1, aspath:2,ebgp:true},
  {u:'P4',v:'CR3', bandwidth:1000, cost:0.1, aspath:2,ebgp:true,blocked:true},
  // CR interne
  {u:'CR1',v:'CE1',bandwidth:10000,cost:0.01,aspath:1},
  {u:'CR1',v:'CE2',bandwidth:5000, cost:0.02,aspath:1},
  {u:'CR2',v:'CE2',bandwidth:10000,cost:0.01,aspath:1},
  {u:'CR2',v:'CE3',bandwidth:5000, cost:0.02,aspath:1},
  {u:'CR3',v:'CE3',bandwidth:1000, cost:0.1, aspath:1},
  // CE→BR (AS200→AS300)
  {u:'CE1',v:'BR1',bandwidth:10000,cost:0.01,aspath:2,ebgp:true},
  {u:'CE2',v:'BR1',bandwidth:5000, cost:0.02,aspath:2,ebgp:true},
  {u:'CE2',v:'BR2',bandwidth:5000, cost:0.02,aspath:2,ebgp:true},
  {u:'CE3',v:'BR2',bandwidth:1000, cost:0.1, aspath:2,ebgp:true},
  // BR→DST
  {u:'BR1',v:'DST',bandwidth:10000,cost:0.01,aspath:1},
  {u:'BR2',v:'DST',bandwidth:5000, cost:0.02,aspath:1},
  {u:'P1',v:'P2', bandwidth:1000, cost:0.1, aspath:1},
  {u:'CR1',v:'CR2',bandwidth:1000,cost:0.1, aspath:1},
 ],
 gateways:[
  {id:'GW-TELCO-A',ip:'10.100.0.1',mask:'/30',desc:'Peering AS100→AS200 Nord',color:'#00e5ff'},
  {id:'GW-TELCO-B',ip:'10.100.0.2',mask:'/30',desc:'Peering AS100→AS200 Centre',color:'#00ff9d'},
 ],
 missions:[
  {from:'SRC',to:'DST',icon:'📡',type:'BACKBONE',title:'Trafic Cœur Réseau',
   desc:'16 nœuds, 3 AS, liens bloqués BGP. P4→CR3 bloqué. PE2 tombe à T+12s, CR2 à T+20s. TTL=52. 40 secondes. Pas d\\'aide.',
   pts:900,ttl:52,requiredGW:'GW-TELCO-A',
   downNodes:['PE3'],dynamicFailures:[{node:'PE2',at:12,type:'overload'},{node:'CR2',at:20,type:'fire'}],
   constraints:[
    {key:'Lien bloqué',val:'P4 → CR3 (politique)',type:'fail'},
    {key:'PE3',val:'DOWN',type:'fail'},
    {key:'PE2',val:'Surcharge T+12s',type:'warn'},
    {key:'CR2',val:'Incendie T+20s',type:'warn'},
    {key:'TTL',val:'52 — SERRÉ',type:'fail'},
    {key:'GW requise',val:'GW-TELCO-A (Nord)',type:'warn'},
   ],
   costMode:'ospf'},
  {from:'SRC',to:'DST',icon:'🚨',type:'ALERTE CRITIQUE',title:'Coupure Nationale',
   desc:'PE1 et CR1 tombent à T+8s. CE1 à T+15s. BR1 à T+22s. PE3 down au départ. TTL=48. Tu dois DÉJÀ savoir ton chemin !',
   pts:1400,ttl:48,requiredGW:'GW-TELCO-B',
   downNodes:['PE3'],
   dynamicFailures:[
    {node:'PE1',at:8,type:'fire'},{node:'CR1',at:8,type:'flood'},
    {node:'CE1',at:15,type:'hack'},{node:'BR1',at:22,type:'power'}
   ],
   constraints:[
    {key:'PE3',val:'DOWN au départ',type:'fail'},
    {key:'PE1+CR1',val:'Tombent à T+8s',type:'warn'},
    {key:'CE1',val:'Cyberattaque T+15s',type:'warn'},
    {key:'BR1',val:'Panne secteur T+22s',type:'warn'},
    {key:'TTL',val:'48 — CRITIQUE',type:'fail'},
   ],
   costMode:'ospf'},
  {from:'SRC',to:'DST',icon:'💀',type:'CYBERATTAQUE',title:'MISSION IMPOSSIBLE',
   desc:'PE1, P1, CR1, CE1, BR1, PE3 déjà hors ligne. P3 tombe à T+6s. CR2 à T+12s. TTL=40. 40 secondes. Un seul chemin existe. Trouve-le.',
   pts:2000,ttl:40,requiredGW:'GW-TELCO-B',
   downNodes:['PE1','P1','CR1','CE1','BR1','PE3'],
   dynamicFailures:[{node:'P3',at:6,type:'hack'},{node:'CR2',at:12,type:'fire'}],
   constraints:[
    {key:'6 nœuds DOWN',val:'PE1,P1,CR1,CE1,BR1,PE3',type:'fail'},
    {key:'P3',val:'Cyberattaque T+6s',type:'warn'},
    {key:'CR2',val:'Incendie T+12s',type:'warn'},
    {key:'TTL',val:'40 — EXTRÊME',type:'fail'},
    {key:'Chemins viables',val:'1 seul !',type:'warn'},
   ],
   costMode:'ospf'},
 ]
}
];

// ═══════════════════════════════════════════════════════════════════════
//  GAME STATE
// ═══════════════════════════════════════════════════════════════════════
let G={
  selectedLevel:0, levelIdx:0, missionIdx:0,
  score:0, tries:3, path:[], downNodes:[],
  dynamicTimers:[], timerSec:0, timerInterval:null, animRaf:null,
  particles:[], animT:0, optResult:null, cleared:[], activeGW:null,
  currentTTL:64
};

// ═══════════════════════════════════════════════════════════════════════
//  CANVAS
// ═══════════════════════════════════════════════════════════════════════
const cv=document.getElementById('cv');
const ctx=cv.getContext('2d');
function resizeCV(){
  const el=document.querySelector('.main-area');
  if(!el)return;
  cv.width=el.clientWidth-312;
  cv.height=el.clientHeight;
}
window.addEventListener('resize',resizeCV);

// ═══════════════════════════════════════════════════════════════════════
//  INTRO LEVEL CARDS
// ═══════════════════════════════════════════════════════════════════════
const diffLabel=['','Initiation','Modéré','Difficile','Expert','BOSS'];
const diffClass=['','d1','d2','d3','d4','d5'];

function buildCards(){
  const el=document.getElementById('lvlGrid');
  el.innerHTML='';
  LEVELS.forEach((lv,i)=>{
    const locked=i>0&&!G.cleared.includes(i-1);
    const cleared=G.cleared.includes(i);
    const active=G.selectedLevel===i;
    const d=document.createElement('div');
    d.className='lvl-card'+(locked?' locked':'')+(cleared?' cleared':'')+(active?' active':'');
    d.innerHTML=`<div class="lc-num" style="color:${['','#00ff9d','#88ff00','#ffd600','#ff8c00','#b44fff'][lv.diff]}">${lv.id}</div>
      <div class="lc-name">${lv.name}</div>
      <div class="lc-proto">${lv.protocol}</div>
      <div class="lc-diff ${diffClass[lv.diff]}">${diffLabel[lv.diff]} · ${lv.timeLimit}s</div>`;
    if(!locked) d.onclick=()=>{G.selectedLevel=i;buildCards();};
    el.appendChild(d);
  });
}
buildCards();

function startSelected(){ startLevel(G.selectedLevel); }

// ═══════════════════════════════════════════════════════════════════════
//  GAME START
// ═══════════════════════════════════════════════════════════════════════
function startLevel(idx){
  G.levelIdx=idx; G.missionIdx=0; G.score=0; G.tries=3;
  document.getElementById('sIntro').classList.add('off');
  document.getElementById('sGame').classList.remove('off');
  switchTab('mission');
  setTimeout(()=>{ resizeCV(); loadMission(); startRender(); },80);
}

function loadMission(){
  const lv=LEVELS[G.levelIdx];
  const ms=lv.missions[G.missionIdx];
  G.path=[]; G.downNodes=[...ms.downNodes];
  G.dynamicTimers=(ms.dynamicFailures||[]).map(f=>({...f,fired:false}));
  G.timerSec=lv.timeLimit; G.particles=[];
  G.activeGW=ms.requiredGW||lv.gateways[0]?.id||null;
  G.currentTTL=ms.ttl||64;
  G.optResult=dijkstra(lv.nodes,lv.edges,G.downNodes,ms.from,ms.to,ms.costMode);
  clearInterval(G.timerInterval);
  G.timerInterval=setInterval(tickTimer,1000);
  updateHUD(); updateMissionTab(); updateRoutingTab(); updatePathTab();
  logClear();
  log(`═══ ${lv.name} — Mission ${G.missionIdx+1}/${lv.missions.length} ═══`,'in');
  log(`${ms.icon} ${ms.title}`,'in');
  log(`Protocole: ${lv.protocol} · TTL: ${ms.ttl} · Passerelle: ${G.activeGW||'libre'}`,'in');
  if(G.dynamicTimers.length) log(`⚠ Pannes dynamiques programmées en cours de partie !`,'wa');
}

// ═══════════════════════════════════════════════════════════════════════
//  TIMER + DYNAMIC FAILURES
// ═══════════════════════════════════════════════════════════════════════
function tickTimer(){
  G.timerSec--;
  const lv=LEVELS[G.levelIdx],ms=lv.missions[G.missionIdx];
  const elapsed=lv.timeLimit-G.timerSec;
  G.dynamicTimers.forEach(f=>{
    if(!f.fired&&elapsed>=f.at){
      f.fired=true;
      if(!G.downNodes.includes(f.node)){
        G.downNodes.push(f.node);
        log(`🚨 PANNE DYNAMIQUE: ${f.node} [${obsIcon(f.type)}] hors ligne !`,'er');
        burst(f.node,'#ff2952',30);
        G.optResult=dijkstra(lv.nodes,lv.edges,G.downNodes,ms.from,ms.to,ms.costMode);
        if(G.path.some(id=>id===f.node)){log(`⚠ Ton chemin traverse ${f.node} — INVALIDE ! Reconstruit.`,'wa');G.path=[];}
        updateMissionTab(); updateRoutingTab(); updatePathTab();
      }
    }
  });
  updateTimerUI();
  if(G.timerSec<=0){
    clearInterval(G.timerInterval);
    G.tries--;
    if(G.tries<=0) showOv('fail','GAME OVER','Plus de vies. Analyse le réseau et recommence.',0,'','',()=>startLevel(G.levelIdx));
    else showOv('fail',`Temps expiré — ${G.tries} vie${G.tries>1?'s':''} restante${G.tries>1?'s':''}`,`${lv.timeLimit}s écoulées. Calcule les métriques plus vite !`,0,'','',()=>loadMission());
  }
}

function updateTimerUI(){
  const lv=LEVELS[G.levelIdx];
  const pct=Math.max(0,G.timerSec/lv.timeLimit*100);
  const col=pct>50?'var(--green)':pct>25?'var(--yellow)':'var(--red)';
  document.getElementById('timerFill').style.cssText=`width:${pct}%;background:${col}`;
  document.getElementById('timerNum').style.color=col;
  document.getElementById('timerNum').textContent=G.timerSec+'s';
}

// ═══════════════════════════════════════════════════════════════════════
//  RENDER
// ═══════════════════════════════════════════════════════════════════════
function startRender(){ if(G.animRaf)cancelAnimationFrame(G.animRaf); renderLoop(); }
function renderLoop(){ G.animT+=.016; drawScene(); G.animRaf=requestAnimationFrame(renderLoop); }

function drawScene(){
  const W=cv.width,H=cv.height;
  if(!W||!H)return;
  ctx.clearRect(0,0,W,H);

  // BG
  const bg=ctx.createRadialGradient(W*.5,H*.4,0,W*.5,H*.5,Math.max(W,H)*.9);
  bg.addColorStop(0,'#0a1830');bg.addColorStop(1,'#030810');
  ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);

  // Grid
  ctx.strokeStyle='rgba(0,229,255,.035)';ctx.lineWidth=1;
  const gs=42;
  for(let x=0;x<W;x+=gs){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,H);ctx.stroke();}
  for(let y=0;y<H;y+=gs){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke();}

  const lv=LEVELS[G.levelIdx];
  const ms=lv.missions[G.missionIdx];

  // AS zones
  drawASZones(W,H,lv);

  // Roads
  drawRoads(W,H,lv);

  // Edges
  drawEdges(W,H,lv,ms);

  // Obstacle zones
  drawObstacleZones(W,H,lv);

  // Buildings
  drawBuildings(W,H,lv,ms);

  // Nodes
  drawNodes(W,H,lv,ms);

  // Baymax
  const bxId=G.path.length>0?G.path[G.path.length-1]:ms.from;
  const bxN=lv.nodes.find(n=>n.id===bxId);
  if(bxN){
    const NR=nodeR(W,H);
    drawBaymax(ctx,bxN.x*W-NR*1.5,bxN.y*H-NR*3.5,NR*3);
  }

  // Particles
  drawParticles();
}

function nodeR(W,H){return Math.min(W,H)*.038;}

function drawASZones(W,H,lv){
  const asColors={1:'rgba(0,229,255,.02)',2:'rgba(180,79,255,.02)',3:'rgba(0,255,157,.02)'};
  const asBorder={1:'rgba(0,229,255,.08)',2:'rgba(180,79,255,.08)',3:'rgba(0,255,157,.08)'};
  const asLabels={1:'AS 100',2:'AS 200',3:'AS 300'};
  const asNodes={};
  lv.nodes.forEach(n=>{
    if(n.as){
      if(!asNodes[n.as])asNodes[n.as]=[];
      asNodes[n.as].push({x:n.x*W,y:n.y*H});
    }
  });
  Object.entries(asNodes).forEach(([as,pts])=>{
    if(pts.length<2)return;
    let minx=Infinity,miny=Infinity,maxx=-Infinity,maxy=-Infinity;
    pts.forEach(p=>{minx=Math.min(minx,p.x);miny=Math.min(miny,p.y);maxx=Math.max(maxx,p.x);maxy=Math.max(maxy,p.y);});
    const pad=30;
    ctx.save();
    ctx.fillStyle=asColors[as]||'rgba(255,255,255,.01)';
    ctx.strokeStyle=asBorder[as]||'rgba(255,255,255,.06)';
    ctx.lineWidth=1;ctx.setLineDash([6,6]);
    roundRect(ctx,minx-pad,miny-pad,(maxx-minx)+pad*2,(maxy-miny)+pad*2,10);
    ctx.fill();ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle=asBorder[as]||'rgba(255,255,255,.2)';
    ctx.font=`bold 10px 'Orbitron'`;ctx.textAlign='left';ctx.textBaseline='top';
    ctx.fillText(asLabels[as]||`AS${as}`,minx-pad+8,miny-pad+6);
    ctx.restore();
  });
}

function roundRect(ctx,x,y,w,h,r){
  ctx.beginPath();
  ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.arcTo(x+w,y,x+w,y+r,r);
  ctx.lineTo(x+w,y+h-r);ctx.arcTo(x+w,y+h,x+w-r,y+h,r);
  ctx.lineTo(x+r,y+h);ctx.arcTo(x,y+h,x,y+h-r,r);
  ctx.lineTo(x,y+r);ctx.arcTo(x,y,x+r,y,r);ctx.closePath();
}

function drawRoads(W,H,lv){
  ctx.save();
  ctx.strokeStyle='rgba(255,255,255,.025)';ctx.lineWidth=10;
  lv.edges.forEach(e=>{
    const na=lv.nodes.find(n=>n.id===e.u),nb=lv.nodes.find(n=>n.id===e.v);
    ctx.beginPath();ctx.moveTo(na.x*W,na.y*H);ctx.lineTo(nb.x*W,nb.y*H);ctx.stroke();
  });
  ctx.restore();
}

function drawEdges(W,H,lv,ms){
  const NR=nodeR(W,H);
  lv.edges.forEach(e=>{
    const na=lv.nodes.find(n=>n.id===e.u),nb=lv.nodes.find(n=>n.id===e.v);
    const pa={x:na.x*W,y:na.y*H},pb={x:nb.x*W,y:nb.y*H};
    const aDown=G.downNodes.includes(e.u),bDown=G.downNodes.includes(e.v);
    const blocked=e.blocked;
    const inPath=isEdgeInPath(e.u,e.v);
    const isEBGP=e.ebgp;

    ctx.save();
    if(blocked){
      ctx.strokeStyle='rgba(255,41,82,.2)';ctx.lineWidth=2;ctx.setLineDash([4,8]);
    } else if(aDown||bDown){
      ctx.strokeStyle='rgba(255,41,82,.15)';ctx.lineWidth=1.5;ctx.setLineDash([6,6]);
    } else if(inPath){
      const g=ctx.createLinearGradient(pa.x,pa.y,pb.x,pb.y);
      g.addColorStop(0,'rgba(0,255,157,.95)');g.addColorStop(1,'rgba(0,229,255,.95)');
      ctx.strokeStyle=g;ctx.lineWidth=4;
      ctx.shadowColor='rgba(0,255,157,.5)';ctx.shadowBlur=14;
    } else if(isEBGP){
      ctx.strokeStyle='rgba(180,79,255,.35)';ctx.lineWidth=2;ctx.setLineDash([8,4]);
    } else {
      const bwPct=Math.min((e.bandwidth||100)/10000,1);
      const alpha=.15+bwPct*.2;
      ctx.strokeStyle=`rgba(0,229,255,${alpha})`;ctx.lineWidth=1+bwPct*2;
    }
    ctx.beginPath();ctx.moveTo(pa.x,pa.y);ctx.lineTo(pb.x,pb.y);ctx.stroke();
    ctx.restore();

    // Blocked mark
    if(blocked){
      const mx=(pa.x+pb.x)*.5,my=(pa.y+pb.y)*.5;
      ctx.save();
      ctx.fillStyle='rgba(255,41,82,.9)';ctx.font=`bold 13px serif`;
      ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('⊘',mx,my);
      ctx.restore();
    }

    // Cost / BW label on edges — HIDDEN in hard mode, player must calculate
    // (removed to increase difficulty)

    // Animated packet dot on selected path
    if(inPath&&!(aDown||bDown)){
      const t=((G.animT*.8)%1);
      const px2=pa.x+(pb.x-pa.x)*t,py2=pa.y+(pb.y-pa.y)*t;
      ctx.save();
      ctx.fillStyle='#00ff9d';ctx.shadowColor='rgba(0,255,157,.9)';ctx.shadowBlur=10;
      ctx.beginPath();ctx.arc(px2,py2,3,0,Math.PI*2);ctx.fill();
      ctx.restore();
    }
  });
}

function drawObstacleZones(W,H,lv){
  const ms=lv.missions[G.missionIdx];
  const allObs=[...(ms.constraints.filter(c=>c.type==='fail').map(c=>({node:null,type:'warn',label:c.key})))];
  G.downNodes.forEach(id=>{
    const n=lv.nodes.find(nd=>nd.id===id);
    if(!n)return;
    const f=G.dynamicTimers.find(t=>t.node===id&&t.fired)||{type:'fail'};
    allObs.push({node:id,type:f.type||'fail'});
  });
  const seen=new Set();
  allObs.filter(o=>o.node).forEach(obs=>{
    if(seen.has(obs.node))return;seen.add(obs.node);
    const n=lv.nodes.find(nd=>nd.id===obs.node);
    if(!n)return;
    const px=n.x*W,py=n.y*H,NR=nodeR(W,H);
    const col=obsColor(obs.type);
    const pulse=Math.sin(G.animT*3)*.35+.65;
    ctx.save();
    ctx.strokeStyle=col.replace('rgb','rgba').replace(')',`,${.4*pulse})`);
    ctx.lineWidth=2.5;ctx.setLineDash([5,4]);
    ctx.beginPath();ctx.arc(px,py,NR+16,0,Math.PI*2);ctx.stroke();
    ctx.fillStyle=col.replace('rgb','rgba').replace(')',',0.06)');
    ctx.beginPath();ctx.arc(px,py,NR+16,0,Math.PI*2);ctx.fill();
    ctx.setLineDash([]);
    ctx.fillStyle=col.replace('rgb','rgba').replace(')',',0.9)');
    ctx.font=`${Math.round(NR*.6)}px serif`;
    ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.fillText(obsIcon2(obs.type),px,py-NR-14);
    ctx.restore();
  });
}

function drawBuildings(W,H,lv,ms){
  const NR=nodeR(W,H);
  lv.nodes.forEach(n=>{
    const px=n.x*W,py=n.y*H;
    const isDown=G.downNodes.includes(n.id);
    ctx.save();
    // Left building
    const bw=NR*.6,bh=NR;
    ctx.fillStyle=isDown?'rgba(50,5,10,.7)':'rgba(8,18,38,.7)';
    ctx.strokeStyle=isDown?'rgba(255,41,82,.1)':'rgba(0,229,255,.06)';
    ctx.lineWidth=1;
    ctx.fillRect(px-NR*2.6,py-bh*.6,bw,bh);
    ctx.strokeRect(px-NR*2.6,py-bh*.6,bw,bh);
    ctx.fillRect(px+NR*1.6,py-bh*.5,bw*.9,bh*.8);
    ctx.strokeRect(px+NR*1.6,py-bh*.5,bw*.9,bh*.8);
    // Windows
    if(!isDown){
      ctx.fillStyle='rgba(0,229,255,.07)';
      for(let wx=0;wx<2;wx++) for(let wy=0;wy<2;wy++)
        ctx.fillRect(px-NR*2.5+wx*5,py-bh*.4+wy*6,3,3);
    }
    // Lamp post
    ctx.strokeStyle='rgba(255,214,0,.2)';ctx.lineWidth=1;
    ctx.beginPath();ctx.moveTo(px+NR*2.4,py+NR*.3);ctx.lineTo(px+NR*2.4,py-NR*.5);ctx.stroke();
    ctx.fillStyle='rgba(255,214,0,.4)';
    ctx.beginPath();ctx.arc(px+NR*2.4,py-NR*.5,2,0,Math.PI*2);ctx.fill();
    // Tree
    ctx.fillStyle='rgba(0,60,20,.6)';
    ctx.beginPath();ctx.arc(px-NR*3,py+NR*.2,NR*.35,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='rgba(0,90,30,.5)';
    ctx.beginPath();ctx.arc(px-NR*3,py-NR*.1,NR*.45,0,Math.PI*2);ctx.fill();
    ctx.restore();
  });
}

function drawNodes(W,H,lv,ms){
  const NR=nodeR(W,H);
  lv.nodes.forEach(n=>{
    const px=n.x*W,py=n.y*H;
    const isDown=G.downNodes.includes(n.id);
    const inPath=G.path.includes(n.id);
    const isSource=n.id===ms.from,isDest=n.id===ms.to;
    const isDynThreat=G.dynamicTimers.some(f=>!f.fired&&f.node===n.id);

    // Pulse ring
    if(!isDown){
      const pulse=Math.sin(G.animT*2+n.x*9)*.4+.6;
      let rc='rgba(0,229,255,';
      if(isSource)rc='rgba(0,255,157,';
      if(isDest)rc='rgba(255,140,0,';
      if(inPath)rc='rgba(0,255,200,';
      if(isDynThreat)rc='rgba(255,214,0,';
      ctx.save();
      ctx.strokeStyle=rc+(0.14*pulse)+')';ctx.lineWidth=2;
      ctx.beginPath();ctx.arc(px,py,NR+10,0,Math.PI*2);ctx.stroke();
      ctx.restore();
    }

    // Node circle
    ctx.save();ctx.beginPath();ctx.arc(px,py,NR,0,Math.PI*2);
    let fill='#060e20',stroke;
    if(isDown){fill='#120305';stroke=`rgba(255,41,82,${.6+Math.sin(G.animT*5)*.35})`;}
    else if(inPath&&isSource){fill='#001508';stroke='#00ff9d';}
    else if(inPath&&isDest){fill='#140800';stroke='#ff8c00';}
    else if(inPath){fill='#001322';stroke='#00e5ff';}
    else if(isSource){fill='#001508';stroke='rgba(0,255,157,.75)';}
    else if(isDest){fill='#140a00';stroke='rgba(255,140,0,.75)';}
    else if(isDynThreat){fill='#141000';stroke='rgba(255,214,0,.7)';}
    else{fill='#060e20';stroke=`rgba(0,229,255,${.25+.15*Math.sin(G.animT+n.y*5)})`;}
    ctx.fillStyle=fill;ctx.fill();
    ctx.strokeStyle=stroke;ctx.lineWidth=inPath?3:1.8;
    ctx.shadowColor=stroke;ctx.shadowBlur=inPath?18:6;
    ctx.stroke();
    ctx.restore();

    // Label
    const fontSize=Math.max(Math.round(NR*.48),7);
    ctx.save();
    ctx.fillStyle=isDown?'rgba(255,41,82,.8)':inPath?'#00ff9d':isSource?'#00ff9d':isDest?'#ff8c00':'#c0d8f5';
    ctx.font=`bold ${fontSize}px 'Share Tech Mono'`;
    ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.fillText(n.id,px,py-1);
    ctx.restore();

    // IP
    ctx.save();
    ctx.fillStyle='rgba(192,216,245,.25)';
    ctx.font=`${Math.max(Math.round(NR*.27),6)}px 'Share Tech Mono'`;
    ctx.textAlign='center';ctx.textBaseline='top';
    ctx.fillText(n.ip,px,py+NR+4);
    ctx.restore();

    // BW indicator
    if(!isDown&&n.type==='router'){
      const bwLabel=n.bw>=10000?'10G':n.bw>=1000?'1G':n.bw>=500?'500M':n.bw>=100?'100M':'10M';
      const bwCol=n.bw>=1000?'rgba(0,255,157,.5)':n.bw>=100?'rgba(255,214,0,.5)':'rgba(255,140,0,.5)';
      ctx.save();ctx.fillStyle=bwCol;ctx.font=`${Math.max(Math.round(NR*.25),6)}px 'Orbitron'`;
      ctx.textAlign='center';ctx.textBaseline='bottom';
      ctx.fillText(bwLabel,px,py-NR-3);
      ctx.restore();
    }

    // Status overlay
    if(isDown){
      ctx.save();ctx.fillStyle='rgba(255,41,82,.9)';ctx.font=`${Math.round(NR*.55)}px serif`;
      ctx.textAlign='center';ctx.textBaseline='middle';
      ctx.fillText('✕',px+NR*.7,py-NR*.7);ctx.restore();
    } else if(isDynThreat){
      const blink=Math.sin(G.animT*8)>.3;
      if(blink){ctx.save();ctx.fillStyle='rgba(255,214,0,.9)';ctx.font=`${Math.round(NR*.45)}px serif`;
      ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('⚠',px+NR*.7,py-NR*.7);ctx.restore();}
    } else if(isSource){
      ctx.save();ctx.fillStyle='#00ff9d';ctx.font=`${Math.round(NR*.4)}px serif`;
      ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('◉',px+NR*.7,py-NR*.7);ctx.restore();
    } else if(isDest){
      ctx.save();ctx.fillStyle='#ff8c00';ctx.font=`${Math.round(NR*.45)}px serif`;
      ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('⚑',px+NR*.7,py-NR*.7);ctx.restore();
    }
    // Proto badge
    if(n.proto){
      const protoCol={RIP:'#ff8c00',OSPF:'#b44fff',BGP:'#ff4dff'}[n.proto]||'#00e5ff';
      ctx.save();ctx.fillStyle=protoCol;ctx.globalAlpha=.6;
      ctx.font=`${Math.max(Math.round(NR*.23),5)}px 'Orbitron'`;
      ctx.textAlign='right';ctx.textBaseline='bottom';
      ctx.fillText(n.proto,px+NR-.5,py-NR+2);
      ctx.restore();
    }
  });
}

function drawBaymax(ctx,x,y,size){
  const s=size/100;
  ctx.save();ctx.translate(x,y);ctx.scale(s,s);
  ctx.fillStyle='rgba(234,245,255,.93)';
  ctx.beginPath();ctx.ellipse(50,68,30,34,0,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.ellipse(50,36,26,24,0,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#0a1830';
  ctx.beginPath();ctx.ellipse(37,33,8,5,0,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.ellipse(63,33,8,5,0,0,Math.PI*2);ctx.fill();
  ctx.strokeStyle='#0a1830';ctx.lineWidth=1.5;
  ctx.beginPath();ctx.moveTo(26,33);ctx.lineTo(74,33);ctx.stroke();
  ctx.fillStyle='rgba(255,255,255,.6)';
  ctx.beginPath();ctx.ellipse(39,30,2.5,2,0,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.ellipse(65,30,2.5,2,0,0,Math.PI*2);ctx.fill();
  ctx.strokeStyle='#00e5ff';ctx.lineWidth=1.5;
  ctx.beginPath();ctx.arc(50,65,11,0,Math.PI*2);ctx.stroke();
  ctx.fillStyle='#00e5ff';
  ctx.beginPath();ctx.arc(50,59,2.2,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.arc(44,71,1.8,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.arc(56,71,1.8,0,Math.PI*2);ctx.fill();
  ctx.strokeStyle='#00e5ff';ctx.lineWidth=1.2;
  ctx.beginPath();ctx.moveTo(50,61.2);ctx.lineTo(44,69.2);ctx.stroke();
  ctx.beginPath();ctx.moveTo(50,61.2);ctx.lineTo(56,69.2);ctx.stroke();
  ctx.fillStyle='rgba(220,238,255,.88)';
  ctx.beginPath();ctx.ellipse(19,68,8,18,-.2,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.ellipse(81,68,8,18,.2,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.ellipse(38,97,8,13,0,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.ellipse(62,97,8,13,0,0,Math.PI*2);ctx.fill();
  ctx.restore();
}

function drawParticles(){
  for(let i=G.particles.length-1;i>=0;i--){
    const p=G.particles[i];
    p.life-=.02;p.x+=p.vx;p.y+=p.vy;p.vy+=.12;
    if(p.life<=0){G.particles.splice(i,1);continue;}
    ctx.save();ctx.globalAlpha=p.life;
    ctx.fillStyle=p.col;ctx.shadowColor=p.col;ctx.shadowBlur=8;
    ctx.beginPath();ctx.arc(p.x,p.y,p.r*p.life,0,Math.PI*2);ctx.fill();
    ctx.restore();
  }
}

// ═══════════════════════════════════════════════════════════════════════
//  CLICK ON CANVAS
// ═══════════════════════════════════════════════════════════════════════
cv.addEventListener('click',e=>{
  const r=cv.getBoundingClientRect();
  const mx=e.clientX-r.left,my=e.clientY-r.top;
  const lv=LEVELS[G.levelIdx];
  const NR=nodeR(cv.width,cv.height)+10;
  for(const n of lv.nodes){
    if(Math.hypot(mx-n.x*cv.width,my-n.y*cv.height)<=NR){clickNode(n.id);return;}
  }
});

// Tooltip
cv.addEventListener('mousemove',e=>{
  const r=cv.getBoundingClientRect();
  const mx=e.clientX-r.left,my=e.clientY-r.top;
  const lv=LEVELS[G.levelIdx];
  const ms=lv.missions[G.missionIdx];
  const NR=nodeR(cv.width,cv.height)+12;
  let hovered=null;
  for(const n of lv.nodes){
    if(Math.hypot(mx-n.x*cv.width,my-n.y*cv.height)<=NR){hovered=n;break;}
  }
  const tt=document.getElementById('tooltip');
  if(hovered){
    const isDown=G.downNodes.includes(hovered.id);
    const edgesFromNode=lv.edges.filter(e=>e.u===hovered.id||e.v===hovered.id);
    const bwLabel=hovered.bw>=1000?(hovered.bw/1000)+'Gbps':hovered.bw+'Mbps';
    tt.innerHTML=`<div class="tt-title">${hovered.id} — ${hovered.proto||'?'}</div>
      <div class="tt-row"><span class="tt-key">IP / Masque</span><span class="tt-val">${hovered.ip}${hovered.mask}</span></div>
      <div class="tt-row"><span class="tt-key">Bande passante</span><span class="tt-val">${bwLabel}</span></div>
      <div class="tt-row"><span class="tt-key">Système autonome</span><span class="tt-val">AS${hovered.as||'—'}</span></div>
      <div class="tt-row"><span class="tt-key">Voisins directs</span><span class="tt-val">${edgesFromNode.length}</span></div>
      <div class="tt-row"><span class="tt-key">Statut</span><span class="tt-val" style="color:${isDown?'#ff2952':'#00ff9d'}">${isDown?'HORS LIGNE':'OPÉRATIONNEL'}</span></div>`;
    tt.style.left=(e.clientX+15)+'px';tt.style.top=(e.clientY-10)+'px';
    tt.classList.add('show');
  } else tt.classList.remove('show');
});
cv.addEventListener('mouseleave',()=>document.getElementById('tooltip').classList.remove('show'));

// ═══════════════════════════════════════════════════════════════════════
//  NODE CLICK LOGIC
// ═══════════════════════════════════════════════════════════════════════
function clickNode(id){
  const lv=LEVELS[G.levelIdx];
  const ms=lv.missions[G.missionIdx];
  if(G.downNodes.includes(id)){burst(id,'#ff2952',20);log(`✕ ${id} est HORS LIGNE — routage impossible !`,'er');return;}
  if(G.path.length===0){
    if(id!==ms.from){log(`Commence par SOURCE : ${ms.from}`,'wa');return;}
    G.path=[id];log(`▶ ${id} — départ. IP: ${lv.nodes.find(n=>n.id===id).ip}`,'in');
    burst(id,'#00ff9d',12);switchTab('path');updatePathTab();return;
  }
  const last=G.path[G.path.length-1];
  if(G.path.includes(id)){
    const idx=G.path.indexOf(id);G.path=G.path.slice(0,idx+1);
    log(`↩ Retour à ${id}`,'wa');updatePathTab();return;
  }
  // Check BGP blocked edge
  const edge=lv.edges.find(e=>(e.u===last&&e.v===id)||(e.v===last&&e.u===id));
  if(!edge){log(`⚠ Aucun lien direct entre ${last} et ${id} !`,'er');return;}
  if(edge.blocked){burst(id,'#ff2952',15);log(`🚫 POLITIQUE BGP: lien ${last}→${id} BLOQUÉ par politique inter-AS !`,'er');return;}
  // Check TTL
  const ttlAfter=G.currentTTL-(G.path.length);
  if(ttlAfter<=0){log(`⚠ TTL épuisé ! Le paquet serait détruit. Raccourcis ton chemin.`,'er');return;}
  G.path.push(id);
  const bwEdge=edge.bandwidth>=1000?(edge.bandwidth/1000)+'Gbps':edge.bandwidth+'Mbps';
  log(`→ ${id} (${lv.nodes.find(n=>n.id===id).ip}) · lien: ${bwEdge} · sauts: ${G.path.length-1} · TTL: ${ms.ttl-G.path.length+1}`,'in');
  burst(id,'#00e5ff',10);
  updatePathTab();
}

// ═══════════════════════════════════════════════════════════════════════
//  PATH UTILITIES
// ═══════════════════════════════════════════════════════════════════════
function isEdgeInPath(u,v){
  for(let i=0;i<G.path.length-1;i++)
    if((G.path[i]===u&&G.path[i+1]===v)||(G.path[i]===v&&G.path[i+1]===u))return true;
  return false;
}

function computeCost(path,mode){
  const lv=LEVELS[G.levelIdx];let c=0;
  for(let i=0;i<path.length-1;i++){
    const e=lv.edges.find(e=>(e.u===path[i]&&e.v===path[i+1])||(e.v===path[i]&&e.u===path[i+1]));
    if(!e){c+=9999;continue;}
    if(mode==='ospf')c+=Math.round(100/Math.max(e.bandwidth||1,1)*10)/10;
    else if(mode==='rip')c+=1;
    else if(mode==='bgp')c+=(e.aspath||1);
    else c+=e.cost||1;
  }
  return Math.round(c*100)/100;
}

function bottleneckBW(path){
  const lv=LEVELS[G.levelIdx];let min=Infinity;
  for(let i=0;i<path.length-1;i++){
    const e=lv.edges.find(e=>(e.u===path[i]&&e.v===path[i+1])||(e.v===path[i]&&e.u===path[i+1]));
    if(e)min=Math.min(min,e.bandwidth||100);
  }
  return min===Infinity?null:min;
}

function isPathValid(path){
  const lv=LEVELS[G.levelIdx];
  const ms=lv.missions[G.missionIdx];
  if(path.length<2)return{ok:false,reason:'Chemin trop court'};
  if(path[0]!==ms.from)return{ok:false,reason:'Doit commencer à la source'};
  if(path[path.length-1]!==ms.to)return{ok:false,reason:'N\\'atteint pas la destination'};
  for(const id of path)if(G.downNodes.includes(id))return{ok:false,reason:`${id} est hors ligne`};
  for(let i=0;i<path.length-1;i++){
    const e=lv.edges.find(e=>(e.u===path[i]&&e.v===path[i+1])||(e.v===path[i]&&e.u===path[i+1]));
    if(!e)return{ok:false,reason:`Pas de lien ${path[i]}→${path[i+1]}`};
    if(e.blocked)return{ok:false,reason:`Lien ${path[i]}→${path[i+1]} bloqué BGP`};
  }
  const ttlLeft=ms.ttl-path.length+1;
  if(ttlLeft<=0)return{ok:false,reason:`TTL épuisé (${ms.ttl} - ${path.length} sauts)`};
  return{ok:true};
}

function resetPath(){G.path=[];log('↺ Chemin réinitialisé.','wa');updatePathTab();}

// ═══════════════════════════════════════════════════════════════════════
//  SEND PACKET
// ═══════════════════════════════════════════════════════════════════════
function sendPacket(){
  const v=isPathValid(G.path);
  if(!v.ok){log(`✕ ${v.reason}`,'er');return;}
  clearInterval(G.timerInterval);
  const lv=LEVELS[G.levelIdx];const ms=lv.missions[G.missionIdx];
  const myCost=computeCost(G.path,ms.costMode);
  const optCost=G.optResult?G.optResult.cost:Infinity;
  const isOpt=myCost<=optCost;
  const ttlLeft=ms.ttl-G.path.length+1;
  const bw=bottleneckBW(G.path);
  const timeBonus=Math.round(G.timerSec*3);
  const ttlBonus=Math.round(ttlLeft*5);
  let pts=isOpt?ms.pts:Math.round(ms.pts*.3);
  pts+=timeBonus+ttlBonus;
  G.score+=pts;
  if(!isOpt){G.tries--;log(`⚠ Chemin non optimal — vie perdue ! (${G.tries} restante${G.tries>1?'s':''})`, 'er');}
  if(G.tries<=0&&!isOpt){
    burst(G.path[G.path.length-1],'#ff2952',20);
    showOv('fail','GAME OVER — Chemin Sous-Optimal','Tu dois trouver le chemin optimal pour passer. Calcule les métriques correctement.',0,'','',()=>startLevel(G.levelIdx));
    return;
  }
  burst(G.path[G.path.length-1],'#00ff9d',35);
  log(`✅ PAQUET LIVRÉ ! Chemin: ${G.path.join('→')}`,`ok`);
  log(`Coût: ${myCost} | Optimal: ${optCost} | TTL restant: ${ttlLeft} | +${pts}pts`,'ok');
  const stats=`
    <div class="os"><div class="os-l">TON COÛT</div><div class="os-v" style="color:${isOpt?'var(--green)':'var(--red)'}">${myCost}</div></div>
    <div class="os"><div class="os-l">RÉSULTAT</div><div class="os-v" style="color:${isOpt?'var(--green)':'var(--red)'}">${isOpt?'OPTIMAL ⭐':'SOUS-OPTIMAL ⚠'}</div></div>
    <div class="os"><div class="os-l">TTL RESTANT</div><div class="os-v" style="color:var(--cyan)">${ttlLeft}</div></div>
    <div class="os"><div class="os-l">GOULOT BW</div><div class="os-v" style="color:var(--orange)">${bw}Mbps</div></div>
    <div class="os"><div class="os-l">BONUS TEMPS</div><div class="os-v" style="color:var(--yellow)">+${timeBonus}</div></div>
    <div class="os"><div class="os-l">${isOpt?'BONUS TTL':'PÉNALITÉ VIE'}</div><div class="os-v" style="color:${isOpt?'var(--yellow)':'var(--red)'}">${isOpt?'+'+ttlBonus:'-1 vie'}</div></div>
  `;
  const hint=!isOpt?`💡 Chemin non optimal — entraîne toi à calculer les métriques ${ms.costMode.toUpperCase()} de tête !`:`⭐ Chemin OPTIMAL ! Tu maîtrises ${ms.costMode.toUpperCase()}.`;
  showOv('ok','Mission Accomplie !',`${ms.icon} ${ms.title} — Protocole ${lv.protocol}`,pts,stats,hint,()=>nextMission());
}

// ═══════════════════════════════════════════════════════════════════════
//  NEXT MISSION / LEVEL
// ═══════════════════════════════════════════════════════════════════════
function nextMission(){
  const lv=LEVELS[G.levelIdx];
  if(G.missionIdx<lv.missions.length-1){G.missionIdx++;loadMission();}
  else{
    if(!G.cleared.includes(G.levelIdx))G.cleared.push(G.levelIdx);
    if(G.levelIdx<LEVELS.length-1){
      showOv('win',`Niveau ${lv.id} Terminé !`,`${lv.name} — Protocole ${lv.protocol}`,G.score,
        `<div class="os"><div class="os-l">SCORE</div><div class="os-v" style="color:var(--yellow)">${G.score}</div></div>
         <div class="os"><div class="os-l">MISSIONS</div><div class="os-v">${lv.missions.length}/${lv.missions.length}</div></div>`,
        '⭐ Niveau suivant débloqué !',()=>goIntro());
    } else {
      showOv('win','🏆 ROUTEX MAÎTRISÉ !',`Tu as résolu tous les niveaux. Score final: ${G.score}`,G.score,
        `<div class="os"><div class="os-l">SCORE FINAL</div><div class="os-v" style="color:var(--yellow)">${G.score}</div></div>
         <div class="os"><div class="os-l">NIVEAUX</div><div class="os-v">4/4</div></div>`,
        '🎓 Tu maîtrises RIP, OSPF, BGP, TTL et les tables de routage !',()=>goIntro());
    }
  }
}

// ═══════════════════════════════════════════════════════════════════════
//  UI UPDATES
// ═══════════════════════════════════════════════════════════════════════
function updateHUD(){
  const lv=LEVELS[G.levelIdx];const ms=lv.missions[G.missionIdx];
  document.getElementById('hLvl').textContent=lv.id;
  document.getElementById('hScore').textContent=G.score;
  document.getElementById('hDowns').textContent=G.downNodes.length;
  document.getElementById('hTTL').textContent=ms.ttl;
  document.getElementById('hTTL').className='hv'+(ms.ttl<50?' re':ms.ttl<60?' ye':'');
  const tr=document.getElementById('hTries');
  tr.innerHTML='';
  for(let i=0;i<3;i++){const p=document.createElement('div');p.className='pip '+(i<G.tries?'on':'off');tr.appendChild(p);}
  const pb=document.getElementById('hProto');
  pb.innerHTML=`<span class="proto-badge proto-${lv.protocol.split('/')[0].toLowerCase()}">${lv.protocol}</span>`;
}

function updateMissionTab(){
  const lv=LEVELS[G.levelIdx];const ms=lv.missions[G.missionIdx];
  document.getElementById('mIcon').textContent=ms.icon;
  document.getElementById('mTitle').textContent=ms.title;
  document.getElementById('mSub').textContent=`NIVEAU ${lv.id} · MISSION ${G.missionIdx+1}/${lv.missions.length} · ${lv.protocol}`;
  document.getElementById('mFrom').textContent=ms.from;
  document.getElementById('mTo').textContent=ms.to;
  document.getElementById('mDesc').textContent=ms.desc;
  // Constraints
  const ce=document.getElementById('constraintsEl');
  ce.innerHTML='';
  const reqs=document.createElement('div');reqs.className='mc-reqs';
  ms.constraints.forEach(c=>{
    const r=document.createElement('div');
    r.className=`req ${c.type==='fail'?'fail':c.type==='ok'?'ok':c.type==='warn'?'neutral':'neutral'}`;
    r.innerHTML=`<span class="req-key">${c.key}</span><span>${c.val}</span>`;
    reqs.appendChild(r);
  });
  // Dynamic failures pending
  G.dynamicTimers.filter(f=>!f.fired).forEach(f=>{
    const r=document.createElement('div');r.className='req neutral';
    r.innerHTML=`<span class="req-key">${f.node}</span><span>⏱ Tombe à T+${f.at}s</span>`;
    reqs.appendChild(r);
  });
  G.dynamicTimers.filter(f=>f.fired).forEach(f=>{
    const r=document.createElement('div');r.className='req fail';
    r.innerHTML=`<span class="req-key">${f.node}</span><span>${obsIcon(f.type)} TOMBÉ</span>`;
    reqs.appendChild(r);
  });
  ce.appendChild(reqs);
  // Gateways
  const gws=document.getElementById('gwSection');
  gws.innerHTML='';
  lv.gateways.forEach(gw=>{
    const d=document.createElement('div');
    const isSel=G.activeGW===gw.id;
    const isReq=ms.requiredGW===gw.id;
    const isBlocked=ms.requiredGW&&ms.requiredGW!==gw.id;
    d.className='gw-row'+(isSel?' selected':'')+(isBlocked?' blocked':'');
    d.innerHTML=`<div class="gw-ip">${gw.ip}</div>
      <div class="gw-mask">${gw.mask}</div>
      <div class="gw-metric" style="background:${isSel?'rgba(0,255,157,.1)':'rgba(0,229,255,.06)'};color:${isSel?'var(--green)':'var(--muted)'}">${isReq?'REQUIS':'ALT'}</div>
      <span style="font-size:.65rem;color:var(--muted)">${gw.desc}</span>`;
    if(!isBlocked)d.onclick=()=>{G.activeGW=gw.id;log(`🔄 Passerelle changée → ${gw.id} (${gw.ip})`,'pu');updateMissionTab();};
    gws.appendChild(d);
  });
}

function updateRoutingTab(){
  const lv=LEVELS[G.levelIdx];const ms=lv.missions[G.missionIdx];
  const tb=document.getElementById('rtBody');tb.innerHTML='';
  lv.nodes.forEach(n=>{
    const isDown=G.downNodes.includes(n.id);
    const inPath=G.path.includes(n.id);
    const isDynThreat=G.dynamicTimers.some(f=>!f.fired&&f.node===n.id);
    const ospfCost=Math.round(100/Math.max(n.bw||1,1)*10)/10;
    const bwStr=n.bw>=1000?(n.bw/1000)+'G':n.bw+'M';
    let stCls='ok',stLbl='OK';
    if(isDown){stCls='dn';stLbl='DOWN';}
    else if(inPath){stCls='sel';stLbl='ACTIF';}
    else if(isDynThreat){stCls='sat';stLbl='⚠MENACÉ';}
    const tr2=document.createElement('tr');
    tr2.innerHTML=`<td style="font-family:var(--mono);font-size:.6rem;color:${isDown?'var(--red)':inPath?'var(--cyan)':'var(--txt)'}">${n.id}</td>
      <td style="color:var(--muted)">${n.ip}${n.mask}</td>
      <td style="color:${n.proto==='BGP'?'var(--pink)':n.proto==='OSPF'?'var(--purple)':'var(--orange)'}">${n.proto||'?'}</td>
      <td style="color:${n.bw>=1000?'var(--green)':n.bw>=100?'var(--yellow)':'var(--red)'}">${bwStr}</td>
      <td><span class="st ${stCls}">${stLbl}</span></td>`;
    tb.appendChild(tr2);
  });
}

function updatePathTab(){
  const lv=LEVELS[G.levelIdx];const ms=lv.missions[G.missionIdx];
  const pb=document.getElementById('pathBuilder');
  pb.innerHTML='';
  if(!G.path.length){
    pb.innerHTML='<span class="pempty">Clique SOURCE → routeurs → DEST</span>';
  } else {
    G.path.forEach((id,i)=>{
      const v=isPathValid(G.path.slice(0,i+2));
      const chip=document.createElement('span');
      const cls=id===ms.from?'s':id===ms.to?'d':'m';
      chip.className=`pchip ${cls}`;
      chip.textContent=id;
      chip.onclick=()=>{G.path=G.path.slice(0,i+1);updatePathTab();};
      pb.appendChild(chip);
      if(i<G.path.length-1){const sep=document.createElement('span');sep.className='psep';sep.textContent='→';pb.appendChild(sep);}
    });
  }
  const myC=G.path.length>1?computeCost(G.path,ms.costMode):null;
  const optC=G.optResult?G.optResult.cost:null;
  const ttlLeft=ms.ttl-G.path.length+1;
  const bw=G.path.length>1?bottleneckBW(G.path):null;
  document.getElementById('mgMine').textContent=myC!==null?myC:'—';
  document.getElementById('mgMine').style.color=myC!==null?'var(--cyan)':'var(--cyan)';
  document.getElementById('mgOpt').textContent=optC!==null?optC:'∞';
  document.getElementById('mgTTL').textContent=ttlLeft>0?ttlLeft:'ÉPUISÉ';
  document.getElementById('mgTTL').style.color=ttlLeft>20?'var(--green)':ttlLeft>5?'var(--yellow)':'var(--red)';
  document.getElementById('mgHops').textContent=G.path.length>1?(G.path.length-1):'—';
  document.getElementById('mgBW').textContent=bw?`${bw}Mbps (${bw>=1000?'EXCELLENT':bw>=100?'BON':'FAIBLE'})` :'—';
  // Validity button
  const v=isPathValid(G.path);
  document.getElementById('btnSend').disabled=!v.ok;

  // Path analysis
  const pa=document.getElementById('pathAnalysis');
  if(G.path.length<2){pa.innerHTML='<span style="font-size:.72rem;color:var(--muted)">Construit un chemin pour voir l\\'analyse.</span>';return;}
  let html='';
  for(let i=0;i<G.path.length-1;i++){
    const a=G.path[i],b=G.path[i+1];
    const e=lv.edges.find(e=>(e.u===a&&e.v===b)||(e.v===a&&e.u===b));
    const linkCost=ms.costMode==='ospf'?Math.round(100/Math.max(e?.bandwidth||1,1)*10)/10:1;
    const nA=lv.nodes.find(n=>n.id===a),nB=lv.nodes.find(n=>n.id===b);
    const blocked=e?.blocked;
    const col=blocked?'var(--red)':e?.ebgp?'var(--purple)':'var(--muted)';
    html+=`<div style="padding:4px 6px;border-bottom:1px solid var(--border2);font-size:.63rem;">
      <span style="color:var(--cyan);font-family:var(--mono)">${a}</span>
      <span style="color:var(--muted)"> → </span>
      <span style="color:var(--cyan);font-family:var(--mono)">${b}</span>
      <span style="float:right;color:${linkCost>5?'var(--red)':linkCost>1?'var(--yellow)':'var(--green)'};font-family:var(--orb);font-size:.58rem">coût ${linkCost}</span>
      <br><span style="color:${col};font-size:.55rem">${blocked?'🚫 BLOQUÉ BGP':e?.ebgp?'🔗 eBGP inter-AS':e?.bandwidth>=1000?'⚡ Fibre 1G+':'📶 '+e?.bandwidth+'Mbps'}</span>
      <span style="color:var(--muted);font-size:.55rem;float:right">${nA?.ip} → ${nB?.ip}</span>
    </div>`;
  }
  if(!v.ok)html+=`<div style="padding:6px;background:var(--rg);border-radius:4px;font-size:.68rem;color:var(--red);margin-top:4px">⚠ ${v.reason}</div>`;
  pa.innerHTML=html;

  updateHUD();updateRoutingTab();
}

// ═══════════════════════════════════════════════════════════════════════
//  OVERLAY
// ═══════════════════════════════════════════════════════════════════════
function showOv(type,title,sub,pts,stats,hint,cb){
  const el=document.getElementById('ov');
  document.getElementById('ovEm').textContent=type==='ok'?'🎉':type==='fail'?'💥':'🏆';
  const t=document.getElementById('ovTtl');t.className='ov-ttl '+type;t.textContent=title;
  document.getElementById('ovSub').textContent=sub;
  document.getElementById('ovStats').innerHTML=stats||'';
  const he=document.getElementById('ovHint');
  if(hint){he.style.display='';he.textContent=hint;}else he.style.display='none';
  document.getElementById('ovPts').textContent=pts?`+${pts} points`:'';
  const btn=document.getElementById('ovBtn');
  btn.textContent=type==='fail'?'RÉESSAYER':type==='win'?'RETOUR MENU':'CONTINUER';
  btn.onclick=()=>{el.classList.remove('show');if(cb)cb();};
  el.classList.add('show');
}

// ═══════════════════════════════════════════════════════════════════════
//  TABS
// ═══════════════════════════════════════════════════════════════════════
function switchTab(name){
  document.querySelectorAll('.ptab').forEach(t=>t.classList.toggle('active',t.dataset.tab===name));
  document.querySelectorAll('.tab-pane').forEach(p=>p.classList.toggle('show',p.id===`tab-${name}`));
}

// ═══════════════════════════════════════════════════════════════════════
//  LOG
// ═══════════════════════════════════════════════════════════════════════
function log(msg,type='in'){
  const el=document.getElementById('logEl');
  const d=document.createElement('div');d.className=`le ${type}`;
  const n=new Date();
  d.innerHTML=`<span class="lts">${n.getHours().toString().padStart(2,'0')}:${n.getMinutes().toString().padStart(2,'0')}:${n.getSeconds().toString().padStart(2,'0')}</span>${msg}`;
  el.appendChild(d);el.scrollTop=el.scrollHeight;
  while(el.children.length>60)el.removeChild(el.firstChild);
}
function logClear(){document.getElementById('logEl').innerHTML='';}

// ═══════════════════════════════════════════════════════════════════════
//  PARTICLES
// ═══════════════════════════════════════════════════════════════════════
function burst(nodeId,col,n){
  const lv=LEVELS[G.levelIdx];
  const nd=lv.nodes.find(x=>x.id===nodeId);if(!nd)return;
  const px=nd.x*cv.width,py=nd.y*cv.height;
  for(let i=0;i<n;i++)G.particles.push({x:px,y:py,vx:(Math.random()-.5)*9,vy:(Math.random()-.5)*9-2,life:1.3,r:2+Math.random()*4,col});
}

// ═══════════════════════════════════════════════════════════════════════
//  UTILS
// ═══════════════════════════════════════════════════════════════════════
function obsIcon(t){return{fire:'🔥',power:'⚡',flood:'🌊',overload:'📶',hack:'💀',pending:'⏱'}[t]||'⚠';}
function obsIcon2(t){return{fire:'🔥',power:'⚡',flood:'🌊',overload:'📶',hack:'💀'}[t]||'⚠';}
function obsColor(t){return{fire:'rgb(255,100,0)',power:'rgb(255,214,0)',flood:'rgb(0,100,255)',overload:'rgb(180,79,255)',hack:'rgb(255,41,82)'}[t]||'rgb(200,200,200)';}

function goIntro(){
  clearInterval(G.timerInterval);if(G.animRaf)cancelAnimationFrame(G.animRaf);
  document.getElementById('sGame').classList.add('off');
  document.getElementById('sIntro').classList.remove('off');
  document.getElementById('ov').classList.remove('show');
  buildCards();
}
</script>
</body>
</html>
"""

def trouver_port():
    port = 8080
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(("", port))
            s.close()
            return port
        except OSError:
            port += 1

class Handler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            contenu = PAGE_ACCUEIL.encode("utf-8")
        elif self.path == "/RouteRush.html":
            contenu = PAGE_JEU.encode("utf-8")
        else:
            self.send_response(404)
            self.end_headers()
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", len(contenu))
        self.end_headers()
        self.wfile.write(contenu)

    def log_message(self, format, *args):
        pass

def main():
    port = trouver_port()

    serveur = http.server.HTTPServer(("", port), Handler)
    t = threading.Thread(target=serveur.serve_forever)
    t.daemon = True
    t.start()

    url = "http://localhost:" + str(port)
    print("Serveur demarre :", url)
    print("Le jeu va s'ouvrir dans votre navigateur...")
    print("Ctrl+C pour quitter")

    time.sleep(0.5)
    webbrowser.open(url)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Fermeture.")

main()

#!/usr/bin/env python3
# Amir Tracer - All-in-one server
# Upload to VPS, run: python3 server.py
# Then open: http://YOUR-VPS-IP:8080

import http.server
import urllib.request
import urllib.parse
import json
import os

PORT = int(os.environ.get("PORT", 8080))

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Amir Tracer</title>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Space+Mono:wght@400;700&family=Rajdhani:wght@500;600;700&display=swap" rel="stylesheet"/>
<style>
:root {
  --bg: #05050a;
  --surface: #0a0a12;
  --card: #0e0e18;
  --border: #16162a;
  --border2: #1e1e38;
  --red: #e63946;
  --blue: #60a5fa;
  --cyan: #a8dadc;
  --green: #4ade80;
  --yellow: #fbbf24;
  --purple: #a78bfa;
  --text: #f1faee;
  --muted: #3d3d60;
  --muted2: #5a5a88;
}

* { margin:0; padding:0; box-sizing:border-box; }

::selection { background: rgba(230,57,70,0.3); color: #fff; }

html { scroll-behavior: smooth; }

body {
  background: var(--bg);
  color: var(--text);
  font-family: 'Space Mono', monospace;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow-x: hidden;
}

/* ── SCANLINES ── */
body::after {
  content:'';
  position:fixed;
  inset:0;
  background: repeating-linear-gradient(0deg, transparent, transparent 3px, rgba(0,0,0,0.08) 3px, rgba(0,0,0,0.08) 4px);
  pointer-events:none;
  z-index:9999;
}

/* ── HERO ── */
.hero {
  width: 100vw;
  position: relative;
  overflow: hidden;
  flex-shrink: 0;
}

.hero-img {
  width: 100%;
  height: 100vh;
  max-height: 560px;
  object-fit: cover;
  object-position: center 10%;
  display: block;
  filter: saturate(1.3) contrast(1.05) brightness(0.85);
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(to bottom, rgba(5,5,10,0.2) 0%, transparent 25%, transparent 45%, rgba(5,5,10,0.95) 80%, rgba(5,5,10,1) 100%),
    linear-gradient(105deg, rgba(230,57,70,0.18) 0%, transparent 45%, rgba(96,165,250,0.12) 100%);
}

/* Grid overlay */
.hero-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(230,57,70,0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(230,57,70,0.06) 1px, transparent 1px);
  background-size: 60px 60px;
  mask-image: linear-gradient(to bottom, transparent 30%, black 60%, black 70%, transparent 100%);
}

/* Corner HUD brackets */
.hero-corner {
  position: absolute;
  width: 40px;
  height: 40px;
}
.hero-corner.tl { top:20px; left:20px; border-top:2px solid var(--red); border-left:2px solid var(--red); }
.hero-corner.tr { top:20px; right:20px; border-top:2px solid var(--blue); border-right:2px solid var(--blue); }
.hero-corner.bl { bottom:30%; left:20px; border-bottom:2px solid var(--red); border-left:2px solid var(--red); }
.hero-corner.br { bottom:30%; right:20px; border-bottom:2px solid var(--blue); border-right:2px solid var(--blue); }

/* Crosshair */
.hero-crosshair {
  position:absolute;
  top:50%;
  right:18%;
  transform: translate(50%, -60%);
  width: 80px;
  height: 80px;
  opacity: 0.25;
  animation: rotateSlow 12s linear infinite;
}
.hero-crosshair::before, .hero-crosshair::after {
  content:'';
  position:absolute;
  background: var(--red);
}
.hero-crosshair::before { top:50%;left:0;right:0;height:1px;transform:translateY(-50%); }
.hero-crosshair::after { left:50%;top:0;bottom:0;width:1px;transform:translateX(-50%); }
@keyframes rotateSlow { to { transform: translate(50%,-60%) rotate(360deg); } }

/* Scan line animation */
.hero-scan {
  position:absolute;
  left:0;right:0;height:2px;
  background: linear-gradient(90deg, transparent, rgba(230,57,70,0.6), transparent);
  animation: scan 4s ease-in-out infinite;
  pointer-events:none;
}
@keyframes scan {
  0%   { top: 0%; opacity:0; }
  10%  { opacity:1; }
  90%  { opacity:1; }
  100% { top: 75%; opacity:0; }
}

.hero-content {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  padding: 0 24px 48px;
  text-align: center;
}

.hero-eyebrow {
  font-family: 'Rajdhani', sans-serif;
  font-size: 0.65rem;
  letter-spacing: 8px;
  color: var(--red);
  text-transform: uppercase;
  margin-bottom: 10px;
  animation: fadeDown 0.6s 0.2s both;
}

.hero-title {
  font-family: 'Bebas Neue', sans-serif;
  font-size: clamp(3rem, 10vw, 7rem);
  letter-spacing: 10px;
  line-height: 0.9;
  color: var(--text);
  text-shadow: 0 0 60px rgba(230,57,70,0.5);
  animation: fadeDown 0.6s 0.3s both;
}

.hero-title .r { color: var(--red); }

.hero-quote {
  font-family: 'Rajdhani', sans-serif;
  font-weight: 600;
  font-size: clamp(0.8rem, 2.5vw, 1.1rem);
  letter-spacing: 3px;
  color: rgba(241,250,238,0.55);
  text-transform: uppercase;
  margin-top: 12px;
  animation: fadeDown 0.6s 0.4s both;
}

.hero-quote em { color: var(--cyan); font-style: normal; }

/* ── MAIN WRAPPER ── */
.wrapper {
  width: 100%;
  max-width: 720px;
  padding: 0 16px 80px;
  position: relative;
  z-index: 1;
}

/* ── MODE TABS ── */
.mode-tabs {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
  margin-bottom: 20px;
  animation: fadeUp 0.5s 0.1s both;
}

.tab-btn {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 12px 6px 10px;
  color: var(--muted2);
  font-family: 'Rajdhani', sans-serif;
  font-weight: 700;
  font-size: 0.65rem;
  letter-spacing: 2px;
  cursor: pointer;
  text-transform: uppercase;
  transition: all 0.2s;
  text-align: center;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.tab-btn .tab-icon {
  font-size: 1.2rem;
  display: block;
  filter: grayscale(1);
  transition: filter 0.2s;
}

.tab-btn:hover {
  border-color: var(--border2);
  color: var(--text);
}

.tab-btn.active {
  color: var(--text);
  border-color: transparent;
}

.tab-btn.active .tab-icon { filter: none; }

.tab-btn[data-mode="phone"].active {
  background: linear-gradient(135deg, rgba(230,57,70,0.15), rgba(230,57,70,0.05));
  border-color: rgba(230,57,70,0.4);
  box-shadow: 0 0 20px rgba(230,57,70,0.1), inset 0 0 20px rgba(230,57,70,0.05);
  text-shadow: 0 0 8px rgba(230,57,70,0.5);
}

.tab-btn[data-mode="ip"].active {
  background: linear-gradient(135deg, rgba(96,165,250,0.15), rgba(96,165,250,0.05));
  border-color: rgba(96,165,250,0.4);
  box-shadow: 0 0 20px rgba(96,165,250,0.1), inset 0 0 20px rgba(96,165,250,0.05);
  text-shadow: 0 0 8px rgba(96,165,250,0.5);
}

.tab-btn[data-mode="email"].active {
  background: linear-gradient(135deg, rgba(251,191,36,0.15), rgba(251,191,36,0.05));
  border-color: rgba(251,191,36,0.4);
  box-shadow: 0 0 20px rgba(251,191,36,0.1), inset 0 0 20px rgba(251,191,36,0.05);
  text-shadow: 0 0 8px rgba(251,191,36,0.5);
}

.tab-btn[data-mode="username"].active {
  background: linear-gradient(135deg, rgba(167,139,250,0.15), rgba(167,139,250,0.05));
  border-color: rgba(167,139,250,0.4);
  box-shadow: 0 0 20px rgba(167,139,250,0.1), inset 0 0 20px rgba(167,139,250,0.05);
  text-shadow: 0 0 8px rgba(167,139,250,0.5);
}

.tab-btn[data-mode="vehicle"].active {
  background: linear-gradient(135deg, rgba(251,146,60,0.15), rgba(251,146,60,0.05));
  border-color: rgba(251,146,60,0.4);
  box-shadow: 0 0 20px rgba(251,146,60,0.1), inset 0 0 20px rgba(251,146,60,0.05);
  text-shadow: 0 0 8px rgba(251,146,60,0.5);
}

/* ── SEARCH BOX ── */
.search-box {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 24px;
  margin-bottom: 16px;
  position: relative;
  transition: border-color 0.3s, box-shadow 0.3s;
  animation: fadeUp 0.5s 0.15s both;
}

.search-box::before, .search-box::after {
  content:'';
  position:absolute;
  width:14px;
  height:14px;
  transition: all 0.3s;
}
.search-box::before { top:-1px;left:-1px;border-top:2px solid var(--active-color, var(--red));border-left:2px solid var(--active-color, var(--red)); }
.search-box::after  { bottom:-1px;right:-1px;border-bottom:2px solid var(--active-color, var(--red));border-right:2px solid var(--active-color, var(--red)); }

.search-box:focus-within {
  border-color: var(--active-color, var(--red));
  box-shadow: 0 0 0 1px rgba(var(--active-rgb, 230,57,70), 0.15), 0 0 40px rgba(var(--active-rgb, 230,57,70), 0.06);
}

.input-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}

.input-label {
  font-family: 'Rajdhani', sans-serif;
  font-weight: 700;
  font-size: 0.65rem;
  letter-spacing: 4px;
  color: var(--active-color, var(--red));
  text-transform: uppercase;
  display: flex;
  align-items: center;
  gap: 8px;
}

.input-label::before {
  content:'';
  display:inline-block;
  width:20px;height:1px;
  background: var(--active-color, var(--red));
  box-shadow: 0 0 6px var(--active-color, var(--red));
}

.input-desc {
  font-family: 'Rajdhani', sans-serif;
  font-size: 0.65rem;
  color: var(--muted2);
  letter-spacing: 1px;
  font-weight: 500;
}

.input-row {
  display: flex;
  gap: 10px;
}

input {
  flex: 1;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 2px;
  padding: 13px 16px;
  color: var(--text);
  font-family: 'Space Mono', monospace;
  font-size: 0.95rem;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
  letter-spacing: 1px;
}
input::placeholder { color: var(--muted); font-size: 0.8rem; }
input:focus {
  border-color: var(--active-color, var(--red));
  box-shadow: 0 0 0 1px rgba(var(--active-rgb, 230,57,70), 0.12), inset 0 0 20px rgba(var(--active-rgb, 230,57,70), 0.02);
}

.trace-btn {
  background: var(--active-color, var(--red));
  border: none;
  border-radius: 2px;
  padding: 13px 28px;
  color: #fff;
  font-family: 'Bebas Neue', sans-serif;
  font-size: 1.1rem;
  letter-spacing: 3px;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s;
  position: relative;
  overflow: hidden;
  box-shadow: 0 0 0 rgba(var(--active-rgb,230,57,70),0);
}
.trace-btn::before {
  content:'';
  position:absolute;
  inset:0;
  background:linear-gradient(135deg,rgba(255,255,255,0.18) 0%,transparent 60%);
  opacity:0;
  transition:opacity 0.2s;
}
.trace-btn:hover { box-shadow: 0 0 30px rgba(var(--active-rgb,230,57,70),0.5); transform:translateY(-1px); }
.trace-btn:hover::before { opacity:1; }
.trace-btn:active { transform:translateY(0); }
.trace-btn:disabled { opacity:0.35; cursor:not-allowed; transform:none; box-shadow:none; }

.hint-row {
  display:flex;
  align-items:center;
  gap:8px;
  margin-top:12px;
  font-size:0.62rem;
  color:var(--muted2);
  letter-spacing:1px;
}
.hint-row::before { content:'//'; color:var(--active-color,var(--red)); opacity:0.6; font-family:'Space Mono',monospace; }

/* ── QUICK STATS BAR ── */
.stats-bar {
  display:grid;
  grid-template-columns: repeat(4,1fr);
  gap:8px;
  margin-bottom:20px;
  animation: fadeUp 0.5s 0.2s both;
}

.stat-item {
  background:var(--card);
  border:1px solid var(--border);
  border-radius:4px;
  padding:10px 12px;
  text-align:center;
}

.stat-label {
  font-family:'Rajdhani',sans-serif;
  font-size:0.55rem;
  letter-spacing:2px;
  color:var(--muted2);
  text-transform:uppercase;
  font-weight:600;
}

.stat-val {
  font-family:'Bebas Neue',sans-serif;
  font-size:1.2rem;
  letter-spacing:2px;
  margin-top:2px;
}

/* ── STATUS ── */
.status {
  text-align:center;
  padding:20px;
  font-size:0.72rem;
  color:var(--active-color,var(--red));
  letter-spacing:3px;
  display:none;
  text-transform:uppercase;
  font-family:'Rajdhani',sans-serif;
  font-weight:700;
}
.status.active { display:flex; align-items:center; justify-content:center; gap:12px; }
.spinner {
  width:16px; height:16px;
  border:2px solid rgba(var(--active-rgb,230,57,70),0.2);
  border-top-color:var(--active-color,var(--red));
  border-radius:50%;
  animation:spin 0.8s linear infinite;
}
@keyframes spin{ to{transform:rotate(360deg);} }

/* ── RESULT CARD ── */
.result-card {
  background:var(--card);
  border:1px solid var(--border);
  border-radius:4px;
  overflow:hidden;
  display:none;
  position:relative;
  margin-bottom:16px;
}
.result-card::before {
  content:'';
  position:absolute;
  top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg, var(--active-color,var(--red)), var(--cyan));
  box-shadow:0 0 12px rgba(var(--active-rgb,230,57,70),0.5);
}
.result-card.visible { display:block; animation:fadeUp 0.4s ease both; }

.result-header {
  display:flex;align-items:center;justify-content:space-between;
  padding:12px 20px;
  background:var(--surface);
  border-bottom:1px solid var(--border);
  font-family:'Rajdhani',sans-serif;font-size:0.7rem;
  color:var(--muted2);letter-spacing:3px;text-transform:uppercase;font-weight:700;
}
.result-header-left { display:flex;align-items:center;gap:10px; }
.live-dot {
  width:6px;height:6px;border-radius:50%;
  background:var(--active-color,var(--red));
  box-shadow:0 0 8px var(--active-color,var(--red));
  animation:blink 1.5s infinite;
}
@keyframes blink{ 0%,100%{opacity:1;} 50%{opacity:0.2;} }

.copy-btn {
  background:transparent;
  border:1px solid var(--border);border-radius:2px;
  padding:4px 14px;
  color:var(--muted2);
  font-family:'Rajdhani',sans-serif;font-size:0.7rem;font-weight:700;letter-spacing:2px;
  cursor:pointer;transition:all 0.2s;text-transform:uppercase;
}
.copy-btn:hover {
  border-color:var(--cyan);color:var(--cyan);
  box-shadow:0 0 10px rgba(168,218,220,0.2);
  transform:none;opacity:1;
}

/* pretty result cards */
.pretty-results {
  display: none;
}
.pretty-results.visible {
  display: block;
  animation: fadeUp 0.4s ease both;
}

.result-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  padding: 20px;
}

.result-field {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 12px 14px;
  transition: border-color 0.2s;
}

.result-field:hover { border-color: var(--border2); }

.field-label {
  font-family: 'Rajdhani', sans-serif;
  font-size: 0.6rem;
  letter-spacing: 3px;
  color: var(--muted2);
  text-transform: uppercase;
  font-weight: 700;
  margin-bottom: 4px;
}

.field-val {
  font-family: 'Space Mono', monospace;
  font-size: 0.82rem;
  color: var(--text);
  word-break: break-all;
}

.field-val.highlight { color: var(--active-color, var(--red)); }

.result-full-row {
  grid-column: 1 / -1;
}

/* Raw JSON toggle */
.raw-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-top: 1px solid var(--border);
  background: var(--surface);
  cursor: pointer;
  font-family: 'Rajdhani', sans-serif;
  font-size: 0.65rem;
  letter-spacing: 3px;
  color: var(--muted2);
  text-transform: uppercase;
  font-weight: 700;
  transition: color 0.2s;
  user-select: none;
}
.raw-toggle:hover { color: var(--text); }
.raw-toggle::before { content: '{}'; font-family: 'Space Mono', monospace; }

.raw-section {
  display: none;
  border-top: 1px solid var(--border);
}
.raw-section.open { display: block; }

pre {
  padding:20px;
  font-size:0.75rem;line-height:1.8;
  overflow-x:auto;white-space:pre-wrap;word-break:break-word;
  color:var(--text);font-family:'Space Mono',monospace;
}
.key{color:#a8dadc;} .string{color:#a8e6cf;} .number{color:#fbbf24;} .bool{color:var(--red);} .null{color:var(--muted2);}

/* ── ERROR ── */
.error-msg {
  background:rgba(230,57,70,0.06);
  border:1px solid rgba(230,57,70,0.25);border-radius:4px;
  padding:14px 18px;
  color:var(--red);font-size:0.78rem;
  display:none;
  animation:fadeUp 0.3s ease both;
  font-family:'Rajdhani',sans-serif;font-weight:700;letter-spacing:1px;
  align-items:center;gap:10px;
}
.error-msg.visible { display:flex; }
.error-msg::before { content:'⚠'; font-size:1.1rem; }

/* ── HISTORY ── */
.history-section {
  margin-top: 20px;
  animation: fadeUp 0.5s 0.3s both;
}

.history-title {
  font-family: 'Rajdhani', sans-serif;
  font-size: 0.62rem;
  letter-spacing: 4px;
  color: var(--muted2);
  text-transform: uppercase;
  font-weight: 700;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.history-title::after { content:''; flex:1; height:1px; background:var(--border); }

.history-list { display:flex; flex-direction:column; gap:6px; }

.history-item {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 3px;
  padding: 10px 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  transition: all 0.15s;
  font-size: 0.75rem;
}
.history-item:hover {
  border-color: var(--border2);
  background: var(--surface);
}
.history-left { display:flex; align-items:center; gap:10px; }
.history-mode-badge {
  font-family: 'Rajdhani', sans-serif;
  font-size: 0.55rem;
  letter-spacing: 2px;
  padding: 2px 8px;
  border-radius: 2px;
  font-weight: 700;
  text-transform: uppercase;
}
.history-query { color: var(--muted2); font-size: 0.72rem; }
.history-time { color: var(--muted); font-size: 0.6rem; font-family: 'Rajdhani', sans-serif; letter-spacing:1px; }

/* ── WATERMARK ── */
.watermark {
  text-align:center; margin-top:48px;
  font-size:0.62rem; color:var(--muted);
  letter-spacing:4px;
  font-family:'Rajdhani',sans-serif; font-weight:600; text-transform:uppercase;
}
.watermark a { color:var(--cyan); text-decoration:none; transition:color 0.2s; }
.watermark a:hover { color:var(--red); }

/* ── DIVIDER ── */
.divider {
  width:100%;height:1px;
  background:linear-gradient(90deg,transparent,var(--border),transparent);
  margin:0 0 24px;
}

/* ── HEADER ── */
header {
  text-align:center;margin-bottom:32px;
  animation: fadeDown 0.5s 0.1s both;
}
.logo {
  font-family:'Bebas Neue',sans-serif;
  font-size:clamp(2.4rem,6vw,4rem);
  letter-spacing:8px;line-height:1;
  background:linear-gradient(135deg,var(--red),var(--cyan));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  filter:drop-shadow(0 0 20px rgba(230,57,70,0.35));
}
.tagline {
  font-family:'Rajdhani',sans-serif;font-weight:500;
  color:var(--muted2);font-size:0.7rem;letter-spacing:6px;
  text-transform:uppercase;margin-top:4px;
}
.sys-badge {
  display:inline-flex;align-items:center;gap:6px;
  background:rgba(230,57,70,0.08);border:1px solid rgba(230,57,70,0.25);
  border-radius:3px;padding:4px 12px;
  font-size:0.6rem;letter-spacing:3px;color:var(--red);
  margin-top:10px;font-family:'Rajdhani',sans-serif;font-weight:700;text-transform:uppercase;
}
.sys-dot {
  width:5px;height:5px;border-radius:50%;
  background:var(--red);box-shadow:0 0 6px var(--red);
  animation:blink 1.5s infinite;
}

/* animations */
@keyframes fadeDown { from{opacity:0;transform:translateY(-14px);} to{opacity:1;transform:translateY(0);} }
@keyframes fadeUp   { from{opacity:0;transform:translateY(10px);} to{opacity:1;transform:translateY(0);} }

/* mobile */
@media(max-width:520px){
  .mode-tabs { grid-template-columns:repeat(2,1fr); }
  .stats-bar { grid-template-columns:repeat(2,1fr); }
  .result-grid { grid-template-columns:1fr; }
  .input-row { flex-direction:column; }
  .trace-btn { width:100%; }
  .hero-img { max-height:360px; }
}
</style>
</head>
<body>

<!-- ── HERO ── -->
<div class="hero">
  <img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/7QCCUGhvdG9zaG9wIDMuMAA4QklNBAQAAAAAAGYcAigAWkZCTUQyMzAwMDk2YjAxMDAwMGFhOGMwMDAwNjJlZTAwMDAzMDVhMDEwMDdhYjAwMjAwMjQ1NDAzMDAxZTFlMDQwMDg2ZjIwNDAwM2JhMTA1MDA5MGU4MDYwMBwCAAACAAT/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wgARCALgAuADASIAAhEBAxEB/8QAHAAAAQUBAQEAAAAAAAAAAAAAAQACAwQFBgcI/8QAGgEAAwEBAQEAAAAAAAAAAAAAAAECAwQFBv/aAAwDAQACEAMQAAABx92lrVlrZV/HjViv51xz/HbVF0Nwy+z1FTu7d6auMiWPdI6cHxp5L71jyPPgna7rkNe9zCJIxOSeOKREG2YXTTJS9OJSpCL3TQEubD0Q2yqiTgMSwW5Tqt7Pyh0lzPRJLFPh0PenbmZtZGgcrgVn2NTnNxucQYnOQxyemQ4SzVtPFR4/vsiY4o3rBhVcGVj1NTH6hrL1cvVy1uwzZ+u1LSftXm3G06PFveVdmuk7Yq7MbHj585vSb9TTrjizK76cFqhFhpWp9hz3W4VDL9J1zWK1vz7oqR3RzskJhxlzsudkrVKaJAEbnFjIpWiL09MMnCoOcZYkcZtjYzBaqNEVCRegra0xVwqclRPlbCfSv00PgYXDLVctabcuKNrMOenz6unw8sbdqcS0q0zHMqaSBohAkSCcx8sJSBis6DIieNg6jmdOXSmoX9MNHTyN/GoU7QvZoqYd5aOhj7nD3NYcfoZyYuYMKVAGuf2XVyL94cyJ+UVbOOdOOnpIsD0rXPy2/Xn9jpMlafhyZLXs9nOxBK0Q4bUUIOIThMqEyRwTcVLNNExmo3PMuLMnr4uMrOzT3Xs6VefZq1IfKRUm6kKVWak+NbuXBRSmirUJnpLnJ2G+hv8AI6LOmo58pevFl6Mt1rItD6fSw9JbGznaIJrw6TkkCQPkIToYKSOZp9BU1x47oY+0146mhj3M6p5k9XaLePYjWt3SycXm65KWph6YUsLaxXipYNMn1oxVLx5vNpyRvY3czW11Xa8ZtYbw871mL7HBnX62lydWc6UdvExPK3aSU2tegrySPFXdMU2qZ01GXyzValrZOYKuXnc87cOBBE6l/miloSxxi0q+QA2GUow0VlTA6psPIxlpxjoC5YZlnVlDEGlEnDr5MKfo2bx0rrvLHn2pc7nWcfRy6PQoKlyddIseW8tEtBKk5RuHIE2TPeyxpGDpULPX5k1qtDy750T7usRvzNGFas4+Zl2u5a5zlc4CsONYzRXj6JkaHOI5zXgqG+1eh09OiTUxNXLGnn91gdeGXegs8foUYtnG9XzklI92OUkuJ0hTjUpTa5z5prZjLa9UoHZWJh4Rq4jVGcmjmSqVv4MbNLO0dUWVefsNcZpbguKu3DLeLKhptmKSdmctGNlNbDAxBvwhz7OuYnxbe1zVXNjpcaLrdLyay23NPk5pr2SXktmerVNJKrxpZ4X7nJbVLWOdXl62dbotV8+27r49OOSryvjNGnls9E5aHsdcOVwdvHjSmK+qLn7a3UUd3Dk2w9T8r7HQz15WxHo69NToaJmxXisaRq6NXIXJd2cy/wAvXa4Lv+H9Xz3qUvuRkMXGobskRkMtKZRTHOyJLmJj8/llvc6tKMqGzY2hYWl0Xb1lx27awtubXOJl6Ts4tbGq77MSqtejPLsH2dPlgHZLjUHZU+ZQb8/NNVdUuUe10c3Lxo6zOzLiLc9HVrPHzusyVWJX0aHLvL1vGSq/VNnzjp46eo4fHzid30DgNJvo4qF5aVSbSmobWNvzXI31sLXH9BwDnqdPhtq8vRfMuy26nzTX5jZK0BpcneNnI73Nx6IOg4G/K75V+jXVxli3Q9bnmhF7n2ZI3SnGG1U0OHr3eR6njfQ8oSmC++WUyK83SorImkqOTvVMunC1+en5OcxE3r5yrdCNZ50dXWwqy63B59m+N2hDHsoII8M2liAjcpAEkkwkEJAjKCBMekRp4Q1JSAhqZlhSXQ3uPN5bWRdqTUDHjK5tHLa3oy5jUSJl1p1rNeFrY5nq9J7Th9jkee+45DqePZhOc20AUjpfQvGuic9LxPp9HWBjPuxc3Wc507jw2DqKmW3R9Fzuhfod3xHWY687m78Y9DTWpnQ47y+x5Tf46XOdxwvocAkcZ7ijHF03ikksalHOc8eTSmJZHdGToNz9+ok0K1zTnzJ6q6cIqCguxltqR0AlLQAoEkAISTQSQEkhJIEkgDS2WmlSwCkBJqEU2SxCJWoWlQ3mEilnr36llqro3NC/nsDW6fkOi3wfzlzI5uvY5m/FnNeSOW3CrNtqhJq49Lrd/l+radBD2zmfBt+ceb3ZF7md3uy6qOa7n6HT8h0/MV5cU+jMdWPJvczpjsbvI3efq6R2XV385MtwPpgq6XOTs5oyZx52rfyJg2YuuJ0sC53DnmLHRO15a+No5XXjY5+FVqzLEWXSSkUCkCBQgkhgEJoFICKAJIEkkNa9ssIhNqKQGuCGoiQFNQ+NKBCaEb7NR1S+zTfSfLG9luzm17zt1maU3Ey3mUhJHcmntjipWxS2dJ1tKK/z6am7miVX866XqcN/E+gxuprTc0swaLrsPW53XzrOtkx59PTc5ZxtM9LO1Y8u+G/Un04ZNbNtx1x52lzd45vOS4+VRNLTO90mD0bm91+bLrx2XrlN8GZazr6ZstRzuSkUkkxJJCSAEJAgUmAQCQKEEEJJJhIAkWyAgoDXNTaipEx7ENcreelRshJiILlz4xSlDEyzXUlAmYKAXAJrsEOsNss15rI6nN9BeePpu38dbfFdJw/DtoRYettl5v1nIdxrd2v1Tun0MmzZtc/n51yKDPrsZu1Z5+fC16dz0CtLIsOjL0TUM6vNamVeeXmPfGWfLARbne4PXVjRhnzuvjfgX+V01NUHPpDkm0kgSSaSSTQIBJIAkE0kkIEAg5qEkEy1wBBJDCmwy1JBCCA0qCe3GMu+rHPFfG0SRuSkWgQWPmrutPcFQ5PntQO6DrGuI9LvaOBV5zWw899GGGs88jKw9gun6VjUbw4nv+B7XLp665Vsc/aoRnQXoYrPTi/cwBlncpV9bs53S4k0b2MHqsIjIpa8hXKYG1zplFdrb6npur5nW05X85rcp6HPXyLNTDuLgXQKQIFAkkCSQIFAEkDSCmEQhAgECkAEJpAgARLDXMkBQkLC2QTwX89bVTQbj6mXFq5m/kNZPAwghyUSwPY9pz0dVL03Pbuuevo4EeWvU7NGLLJvn9/Ejsv4qh2wMsBDoeg5HTlY+3zm9jp6BDdz+buZW6CCsMu5Ys6XHBSsVx1bNq5p2VJhJGNbN6fnKcnOdTzeenP8vq5WvGNfMuI77V0OT7fNXK7fM30ROZJHQkkxJIEkgSSBJIECgAKBpSTQIBAhCCSYBSAkUNQMtgIkSAQ0EZklqDbx9I6GN0jM3B9P8814M6tKxBRlCCSOXTOMlzBJDJRoz5D9Ju+l+een680XL73A+T6kBow9nOUlahe1Zi6rlbslut2/n8nqtXiaeO/tET3cXVE9HorEuWLPRzhxEbhPahtGxRqBzWlw1c+M9t68Yp8/oXPpfGaFL0POq4Wrlz1V0ktkkgSSEkkNJIEkhJJDQIAApNIIEkkAEIQITCIQwlS2JzUMaW5hnh0M91dly8PVsemc56X1+Pmeceo8mPy9x2cTn+33+A51jvYe/KUtOgUHsbLE9nV9Hyt0xo809mXXGU6si18DCiIGsU2b9o8+9Z4OsuMztenOnsVqhb8zve+N2ugLmdCc5j0OSdDza7nvPn/OvR/M9eaNFaZSa2TJU9XNQv8Abx0M3ew61qJzY1SSGkkJJIaSQkkBkEAg4A0pJgggEQABEgBEstLEFBJmN0cAeyzmxsQDm9iKZbm/m9n0NWzqoaOnSDy30G3teLWH5X017fPn+Pkh7odJC/ZSPY/RIIsc1JgSSI3B0BgljBMkjzFt5vW536rzm9n683lFS/Ujb1aTN1vJ73vr2bcoet7CLgbHNnioTQ6dR5xxl+h0cYThU2BNG6k3uctaY9XlKHswqV9PLnZyBVJJCSSBJJgRCaSQJJAEkhJIYBCEEJYKQNalAkBLaA7Mfbg0Me6wqeo1B3nG+v7csT69gtssdnkcPMdZj+RVPzvq/LvRzYQe/JPYaJnMWo8hUigQCLUAgoETo4AQoe5rUupw17fnN7muri5Hn+lw429G6WtZ8PuUpXVq0oasuBkVC/kNV3bXN1n5rQu1erjrFPGZ4nrWNl2uO3cxZ9uXXgr6HVllCeAsoEaSQJJCQIGkkCSQBFJhIAgghNKlppbI1JQ1E9kCerGet+tYky9CzO/ut/MvapbVxWGS8tQ2WnjapXsXA8Uo62V7WbQk808OoTirUgI1CgUIFiGlMgYUoBJHoS9/0Xz/ANC4+izz/Rcf6HncJp43WY9PpJZX8b0LgyI+/PWp1YhWNLL3NYWPegw6NHk+r46o8xfo4vVyOlNpbyssdbWfCyV7+XdRqald5VpWRb8e9UqaXRlRT47HJpYUiASQBJAgQNAhCSCAkJbXAILXMkaQyG2RtjLR1tU8u+xvZ/W68GjvWZKTw5VbZQ7zKkTmcLFaRvr5eN856J5/sVCk83Fqokex+ieHdTL5Td73iuS9Pj4G9MNjcaUaQkdtY+xFdf1+L0fB0wcrrcX6XBH13nXU82/ZtoOnTTUSqZKzZdsWWa7cti+K5OtHOt89L5vA6fm98bV/Lnnrvek+d+pa8fK8F7txbfB2qkmHoRVtitG2aJZt/Os1YI+jlsy15nqXPa9YxJE8SEtMkkgQSAAqWA5iEEIDG5iYa5+LWiy1z+vCqu/pxdLvaulPPHHIquNwOgJop/DsANycdW7T97n5nyj1rya3VU24o513Z1JfOddt7nHdyKpwHHc3NMk9/AJHVRNczITJYZd7ZyN3Ku76rN1PO6fGsOHrPR5cTe7bL5dNOLQx8dpat+L0cL2fNoxdKzOXFG62Kam807LjldLm9/C1yktVL8dW36Fxvaa8m1Uuiq4vz/2nAU+TaL8bHs1c3Qky9GjBbr68EE9nNrKyxrHE7oH6IuaenmKQpJJICCTDCICx0cstLcyXQq6XP6rM6zsE6fbSbevmpzH4Wwh2NsZJF0kkoXh2Aj1o596n6eGF576PhRpyfQ9pY845nTuNwqrkdRzus4XEdtw3r5JzJOqWJsgoWvbm2tKh3+x5Xt8b7TSz7/ndHl+b3Gx0Y5uJZtMfpTT6uCVZ/ThbZg6Y9EU63PtNoZmljvg8ft89tjnY3Rc5rnJPFLHZ6L1/O9RryWgQMUbjKOX4v1Oq14fd6zg8tdd+fc5/XqT3aJNWtbZv5Vd0Ut5SAjVOdFJtkQQxMdHDACzbopYESPVjHeeZVsPWXft3ejxt6w0pFzHcthzX+ZoGuf1S0FcdBBd0qGdkqjaJ4ryLOhUku18fgN57ni+Pj9XKxHG/vzIcKAk2SNxZmNBuw73ovGd3za9Q4ji2sczGPW4rckT8NZMXTz+iIVpZVTvCle4PQw69urvxW9fOEbcOY30Ueb6LndM7yfFl6Xq3X8t1HR5zkEmGOFDY5G0UuK9DqI8KHpfMwsa9iPw9PZxtl2PfzQt1Ov5+aala1lyI6ckkhMjljzbWuZmw0qC1ceuf149PI9C04tLrs7SrmDCo0bJBLz0XtXl24ltoxvZi05NGiWQHCd5d3Z9RzXMN9HJyTuqSUqHIG0+N7BOYRLayRkDNTM2830fecf2PHtsOI5dfPJOC0vU5uxm871FevHp850ZbRz4sL6zWy3k3zYmy6M7nuy5qHxPQYW/ouQ57ruPudJ1dy6fYejx9nXjSIGGltCaW0FMeOHmeuZK47zb23CF5huYWpx+zFlbeaXlyFvX4EslZ+82ABomhzM2xrmZMSw2M71K6fh6tr2LyX1zfzbE5BLEVNQyNk4qe4P4W1rmw3AhgQjA51iv68cP5x0/MdOTmpEvc12o5wfaieChNMYSscxCY+OR+hnaeT7jvPJPZOLaRJc9/NehmT+tz73cc3t46059LO6c7+vyepmaTXbMPK0nu5Opcn1nHjwZd7D3xq8L23F2y+F2mHue/zHTgmvA2BzapjHimxxax5jkkbXtMDyfB9M8qzrpce63j+ixa9ut2fNucx3ThKGGgxyxIa2RmbAbJlWo5kvP7Wh6b5R6b0eP0yIGxObw2C2TjqREJIFsCYBLLSvajNmZT6F5DkXqECcHXi9B2g5J2iDXxSOY5ICQkUbmyO2Mfrs67TtMLd8/YIrOvmzfze49SG5OxmdODuRuxKbNjGtZX7No5er5ncACqOVqKlQ53r8C44PmNfE68HRujqfY+z879DcuaWptaY7tJobc1Rsc5hTkTXJLxj2fmVPlG3zO9y+vRo62XfNFYrS9XmlzX6IxOahpClsl1pOepb3P7HN6kvfefd4+Lqi13MlGj51idr7SCGiUckONFj2+jKeyH0og5nq/M6XI0bVaGZ4rbIGWK+kOe12uZaWgx7RAk16GMeyHq9pzfac99B0GZpcWqSEvx3d0Oe9jClSfj9OYuHJ53Dez9DN+z38jb8/tLkZsAgFn6NGp8y5Lv+A7MInNl0x7H1zw72RvQY5pTY3K6hUqBscrQY5qB72ukc1yF4jT9P8pitXL2KHP62Q9Lq8OV0UnRJjewGkGHtNxW89bthvf8fdS7bi+p5ctFqdwNEu1lFDRAsdDMM8ENzZB62UVDRzfQVvxT1nxEUcTmzM1yC3PZBXsQb8yeFriGoSBjm5he1oCxD0+bp9jzPofPp0NpLi1BRDzDljP9Bxw5irIs0izChqZVuX7noxS+Z3AoJpJNpIi43zf2vybqx5meGboxHsPjPcOfW2wWTSEuFjUgMtSCFENuewypnRvlQ+L+4cwT5VPVdj6FRmrjViZZq2/G9r2aSwpQ73b8pk8ddw5dTh0P3uZ6DgLToLOiLgWmtC47KIB8U0ND0Gevi/F2MPsnF8n67k02vgmE/cyNPD186KaHs8xArXnY1zYGoDMNmvYTl0a+5k+i6PB7Hj1tIrG0CQ8QyYo/YxaANs4k+LFrTy5pPoZ2Jh+f27+lzfViCIztIgIPL/VvOt8fPGXafZzrewEz3DouJ6suyEKaaQ2HMeEcc8QAIDmmrzSpY3ic/M+E908cC5g6jeb3MZzX9XhSRyN3liShtnh7nJ2dnPy+Ho27/E+pxN+ZkubanQ8dNcE24xytFjwiJBelDOL6zgvQnlsOaCULNW0Gmx65/bGds4/VwhEdPmRAHFxgHNv3cvtM3Wt9bRwt3Wcz2GFpEZtBEPnCQXfT2pwlvTxMje3ORbpul99iT0sr9N6Tn+g4uppKikHAWLxHoHnXTjzOXsZHXzuYUztu+8V9uK1zmalW0Oa3G9iB7DGDSE2Z4HyrJZJEDzj0qAj523YqmXp03aGdWDXQv6eNJEG9jxsuNakuP61zb258XqOONQmLC3QSw51Mx0W8qetaoIB5nGgvUjL8d7LhOxUWJxk2dshpoSQ2cfZtc/0WNVV4y3t+eaQMyLSzrmT3/S8rc4tbnE99w0vqdrK1M2WubLa4EfzvoZlvv788Ph7vHDHNzQSEO503I91D7LoeN63g65UDnSKQZXnHf+ZdfPl50sXVk0Pa1L2/CXFXvDs2R3roixqcAjZIwbGvAw5rhTy154mRpiWeL4j9C+UVeNTbc5vWyHOd0+TGU3SAx2xmabs/tuPp2ekytXglwhnyuJhb2KSKavunzxSwi5rvLuFHE9aPK8ezR63HJHK8XzyNntN6tZntnpXaOPXVhmq+h82wIZ5ncxvQc69LytfE8/bo+T6rmQ6GZKWgUhhLg+cpxH6fQyJ0m/HBHIwyYHNhruuF7jKursx9RxdGLtB2VJKNPM8Z9X8n7efMt1rPViKr0xk0Es33noPh3rDenq4mldWQmjax4BjZ40RyNLJ3sMwYnROjn3Rb8HuddwfPsG3M4mRrXb8q6cRc9LueF9V49bOhAuNsstHPbQ1e5EsD47T7NWzki5rvE1g866jmvVy4CnJH3wnAi1Gx38vYCbIuiKVr4efX0s/o8yvG8V59n13yj3bm0pMNnnrapXVDBCQkUMFEn5/Fe36HqZ6jXX5Cr24s3C17Vm/03zj0nC9/dxNrz+l5BlqraqNcX5h13I+nyi7FW0hSCaim58UubtuIkV+20+U6m66R2TotudGUSMekQJ7KHOaknxOZbFKeNg8P9I89yLuVo0+fuquc7p8z0HDl5flrrPScHd5LOli2uDS5WmZ0jn17HqRCA7oU8sMnNLkGfP7+b833Pn3sycVP68DKLS6Y9CpNHeyR1WpsWTHl2tyNXIvz4ZGX9fL2vXeH63k0i6TP0cWCVIGuQIogEiHzRpZ8vqXCWu35Y0BA0SRQ5fXPIPXOfTX2czT4OiRISzl6fF6R5jVafV5bNR5FPdbLrGbXv52Wis1inp9HxlhX6lreZ9pb6tZ+k2HtkQ2OSME4tEwKlTjms+ctcpZrT8ndAyJ1c9aSSPo5W2qno2D7/D5rpfM0sTLB5NYNTD5H1F6vc8V7X0Mu3VaSnYlqjnejRvZPzmmX5l6j5R6uOXPXsegpJ6tiOs2opp63visLrVS3mTLs7RztfIZdrWKw9a3lJwkuhm6UCSAIpAkkCSQfO7LdT0fQpiavv5RalKewIB6Z5l0WF+vXqOh5vU5FSUvOu78P7Majza7MIZ09q04zdWOFX2crDaNA5090VxaO1saZV3PXeRaNT65JjbDoNKY6ORpNSGHRqsvx3ocPOnwS0sulBx6OBArWY9+rPyve6Rp8rWTiMLoOqYOfDOm7UtCU22Op4ada93W42R5er0sbJ8g1vNd7m/T5ZHRz71JYr62XomN8keknMkXRWzL1TTyXZ96lfANnK7Ax9RchxEmjn35EikIhAUkASIfPyEnb7uXFPD2fPxMnhiQHNkUsSR7D2fhfrfDtsDNysb5zzfRz/R5+hyZa+k7uJ0GXrnpRVJd4jzNWtlpnMvUsLL2lF5+e9buM4jWbu/NFfP8AQD/Ie6qunosxWbvNa3mYR0nWufuqVS++cCeLq5mskbUb3SYWT5ukleiuyWB4aa5qh2IZZs+lstSRaXZc+vG/XZ3Ph+e+JHbJ1hks9EmtWt4e6WvgjscWOrKnS06V+WaOlkXyyehedenri7GWjpcmk9uOWGkiIEICkgSSZ88WczT7fYoVb1LXzFDdrXhGJGmcYKhz9pwr0escdzUUUHB2kz26W1UULBrbTZgv4lFqrM13FHLDi2yKPN6VaLaqMi7cyVd6qyfn9OoNOjWOx1nnRvHdxmXY3ZI6hOkain6vOTmneG36WxlWhx+lQzbHJtohICnCbaQpVyurmfXRiv57xQIrB1iC+uiCds+fTelhnw9+NsE9YOfVEtsczq56WXZrdHiS+o+Wemxj0+vja/JeiSoYRAJIgCECSTPnaatY7fUr1dbOrldVnr3zPfXdrg1pWbCKAJFBebgq3QVtzXLBgmpbE9WxArSD6cDk3MrieHFte1S+i1+R0Nco6vY5DMGwyDn7NepXWXdZnpME6sH7ecZmu6sikrGhKWGuEtoeJGFJCICaa4JGWJk0WEJIh4rMszMvTZZdEttOuLOXp1J4ZaylqWGxpDWv4+3nV43M38Wx3fH+k5Pb183T470EDDCKAIoAkQSSD5otZ1v0dNChYrx0qNOvlrBzdOYIhNApClDAl63A7CseY2ub6Decuhbqa3A8Nxt7oxRLE8AIZHQ64e3JtmidJr7/ABVi897D6KHVc7HZfzddY2qiqKR7t+d6R3kJIGJKWEQgAqRrXCWCEBcxwTUpY4QkbqZ9GdabZNpYLVLPsdJJZnSxFIzL1a7pmac0jk3DqhxdfI7vn4oni/Md7X477jz1dfYr8t6KBkQSGUgIpIEkA+Y3Bvp53VEo6kxprBqcy80k4GBGSZzbYumodVw+uEO5Th6CiiHq0PEtgmARFjoGOTJaSnCo2WLIMsNtCsVYWte/nO2KIsOVZ9iKapBS0ACEAJS0gUMKSA1KWCBJInRJKMXY0kuVpsvVhmMKJGXK60uhHL0nEvnevYQjSOpYyezxZq08O3mUgiuPe9Y809N5q6LP0s/mvRQKAigBCTRCEkkzwPA9b8t9DOMwPqy1NJSRqWkJBBsBd6Cts3hm4u3mbTXhuZ+mhBTpNcAIRBgfHLYHSZkEkUgGtO1OMSMzLopzora1CAXQ1Ta3ygpWprrPT2Okx7JYSSaCKAwiQBzJaSupVoHOzqybUUegYzaWkkVp+Pp156V9OC1WaquNUmXcWPZOubW0393gZ9a/j3wQua+/O7ns+d6Hj07DM1KGFXSkhAoAiBpIIIQHhebei53RHjCtVuyTG9qRa9tISMSBdpbIt21o5OnPhTwy7Usy3U0pJAooNQ9BMQKCFwGTfFIwEiE2giRge2GnsUjZjEl0sOBv9GMVfSo6FITQxqEgMhFDQ+RFeaSBGhmmvCl0oNDH0a0auLoo6eTuPaMxnl9BsrLDdKSG1pyukjk5/TEBob+fq0rZz6qGPpZ3b8zDIyQ5PWtLP2+O+joXqGNaCSQEQBTSMJyQxyQcrp071njXOehef9+aEkdKWKRjE0tSWrlyh0FiSntzRxW8fartS7n1RYHxYelQki01EJsBbmBxjQHhJpODGxzNkiv0nZuaJwmnQFEXdXmJtJ6/OF/fHnq3SuVc3PtZpUFPXoTUcYixpTx350N2jPl6r7FZi6LFiuI6JmtZJYJdn01LQnLTHsy6829Db6fMhIGe1LJ087s+aitVbl8XqHWcZ1nFpuZ9/PyeimuloJCAchopNJIhz8EV7Q53yT2Xx/oiNjxsJj2XISfIyzWuC6zE08rp57WRpZdXYhswOgiGygQjkaE3sLAaQ7MBilG1wAnOhlY1BJsTlLhc5mYhNNJC/QTWNegaFq5iqp6CPHhpXqIfnbJo3AbsNiepz2TZegwyyLcQWXxuonPWszQ/DsLgV0KvYY80TE5Doi8Kmbo5HV8/HNDobeZ2fa8B6Pxdu9m6Ofjz6BCTSSAgppAoZTXCzc3oOboz/K/ROA64ypYL2tx1tDPYxEGS3MrWcplTV1jONtmpDGFdJJAmlqHRyRy3RSwyR2alnNsc00J7HMY8womjIYXqdXWivMi6QkfGcM8ciJ5IyVWh2aauEhzzgk0q7dPRrXMuyq+2V1Mnao7ZYZXPSeJ8fP3V7UL9OR0zXc/aSkupMe2snRo1nCTTvhOLqZHT4TdnG6SuLoO94DvOTTeo3s7FaJBQkU0HNIJJAkiyLkugwm4+L7bL3jyfWy9LbqqVJYdeMuFhTNPabSo9Lkw74zxWKmjrpJ6oJJFpaMhKSEtlzdSWJ+Q8lugSHA9rhooZWzS2vTbJ65ZnoJFdw6KRiBlZgnmz6qcksgOgbYrKSiZmpHz1svWjuQyJypwjuikc9hY8ZdNW5VuVzh7Tz+gkirTSrim+lL3eBaztSjjrRglZ0+FW6LnLyx7nsvPe65n1VK7n89aJDhBIgCkCSTEUmvHJuA0u6PTuQwyjNdEKtjSazumborz5uSSmO9ZrjXO7QuO3nFTXzsEkNIEA1wkrzRLJsbJHm5C00EtLUrTFZLIHWgUKC2yc95XUdPm9KOtdbh1Z+hQbfHbguujpqKKvt52tDn38+uSG8/Luzprb3cUqUdwSTopGCOZrpTkRl2oIEFrhUUppYejzp6dytneSyel2/Mx2IJ3y7npvnfpfNXR52ln81XyiCSTEkgKBBEKl/8QAMhAAAgEDAgUDAwQDAAMBAQAAAQIDAAQRBRIQEyEiMRQgQQYjMjAzNEIVJEAlNUNQJv/aAAgBAQABBQK4c3CW6q7LCqyvuiubhDDKtwtutv8A69pIctbR72HfJ8YyK8gCvjFY2tIv3EQmhG2zG2jQNfC1npjpmhw6bRxApfFAV85zQrFDG7pSZKuxS1Wg3dGzNIMqCDj+oqXKyPIYtNzn2DiOCgex48k91XsFy1QT/cukCozjl2kq27XEImju4zcjTJswmN6Vw9SkLJKXlkT8v2lK7rkngabDLqLma3uL1IIwmHhj6M2+2ucGutwzNmPUdwqKLckcBhNumxSDWKwcYagKwcfHzsGcUCc1mhTLXwMcDwNDoB1raDWOmK+FFGpp446j7kxTDNACtmaUHDOJG/AYVky8NIyEITWOlXR2tA3+kPdjhj2gUwBFxCwMlvCJr62kWkyYpe2LTbp43ftNwpEu5lDAIztziPxs7f08bSMTbZaPPV8VH5vLhbaBp2FSFeYcRXcY5VXqdkWOTPmG0uXLxanZqVsu6SbuuDkNhSI/3Ou/4wK+OPTFEUVoUeAHSvihwxwxTMErFSSorPk0ypBQie4oCsVisVg0uKu8KkbCrhKWJXjgHKGOF13RIzFYboM+KxWOGKx7dtY44q8tRIruHsNTtwtWt0ZmhiSdbS57pMo8aCO3hYvUdsZKSJZLjU7sIilktkGEpxuSW53NCAtTzM8+clov9y4TrJO4S5Pp59RkDwaLNGK9IUq0iMTr0ZCmBSYabaMgZoDq3nArz7PIPFqUZrHAisVihweTFRJsoO056Cg9Q2oDYrHHFSZCUs8EhZBEBNy6DQoTdQivXQ4/yMVNqfW0uARLLcMqS3O6OzkahZQik2gcB7RwFChU0TxyBUubF4uZFbSbLiZUeFULCdDtSBIYHcmKW4KwdzNM336LhFw98NVuoreO9vXm4yFxbXLbLeSPB1WUDV43E0tsWE+lT86LUoWiES9yKSQiCvxnTKtnNdT7zXWlzWOA4isVinJCtNOQWniEsNzKsskyxw2VxKsEU5BM0VLNurn9zzvu50tLJJnnLgTW+J2tgnqItvqBSYwEQkIITHNFUlyGWSSR5ObcXKi2uJXQSpI8VqjRWUET0rnme3Ioe1Q0V1eoHVV3XOnxMAiFpHKwwCVpJdRdpZrsYG7dUS8143HJm1FZGupruS2DrbwGkXc29sECTTp+6Bd8l3qTFbjS5PvXicudmxd9t1ayryLgScuAJ2IS08XRz+Pj2jgTXmhwH5Lxx0AOWZUEt3lUklapC0Je6eULZgC4uGmm5SRR7UJki7FspCFtLdakNgtFrc1vwpu4KW5jSnBceDzXx6qUt6jL89d0Gqvbj/LtLXrXkPrGmrBvai5kUFjfeojFzHm48qcjNHiPcw238qmCW0ttt3DEtmkdy11WpymJYZY7dbUlKmJkuF/cinjgt5GlvqjsobNbmWbUbm9nQjPC3gc1AuLNTlIrwxurC5jtPtNd4L7RNBCwcXsDOzd0kJAa2TeMYoCmFYPt3ZodaNdaHjrw647qlutjb9xZoFaS5jajqG2NphLVtewWwmunnlF0yhb4xo99I5e7yTNDS3caUb+Smmkb9IEbbW+WKdr6x5Mk7TEXALXBV6KPBd21wJgYlZbR2ZaFeKyKbrQPEHhdttM+cQ/Yl5fqzFKRdT9Vs0LxS86KoBFcR28bAhUjuLx+ULyT1FNebYM8NPt1ap7jfVic6cx2WS7paEnN1Ip3bPUVZoyyWfUkuakhjztxJZ9VuciQea+fPswKx0A64rHADhipze8yeS6roDJKrEEA7qB6+oat8twWBUiuZ3PknFJFI1Lp949f4u9wdPuwGtLiOhC9cghVjy3o6a1fLW8qB1bgaXC0JpBUd1kJPJPATPDNbz+oWHbIqtms8fPEL14XgJtxh4ztS4vr15INNUmLVZAYGZoLa1Rbm0UNbXT3SGS4lUC7uikMdvvjIwahXc00hkURKkds4Glao3J0yIHMK8irOUyF5SsdzPgciStSiYSuWU7WzY9Ku+kxoDiaA64rHXHDFCh5x1p5XB508rXjRKK200EUcSqMq1lBHcXhloSMtW/psSyoa9PNUVsVSPMFDULhI/8AKSlW1SXZ/kiR/kPtpfMaedWVZtqbSa2xyR8q2AmSMBhb7JOVWBhosUpfKybJG1AXILpA+kXRgmY7H80fGem00egSZHn60PFOMraH/WuOl3yVcA9mFle/nbeJ2sjPDFqVpulkSKTmVcdj2zcyW52y10qB2So4Nw9THz15q2upRM9xZgb0VpjDHmriOTbfrGY9MnWGtsN3HcWeykDmSwwz31s3MrbmiOnTPHHADqBQrHXFXtz6WG51K4cNNIRwwaSKSSnieOsFjDZySPLp+1Yo9oiiYI6OQLOdzBaYZra2zJb2yDZASNPV6Glwgf423NDTIiE0y1FPp9qC1jBt9HC9RRWYMkPLd4lxvRJJIFWOWNaIatvapODMxXTbhL+KG2iJ9FbUbO3r0kFXojtYLCGWJ91yGM+KhuxJKXyLepus6K5kRVZbiUJFqVWs7iobmXT7i4jiu1vLbeyt6+OFuXcW9s7VDCXJtRED3LKjRhIIZ4LuGexu4rhLqCG0HJzitP3xRGWF7mG3aC4hZrWbfHcLNaxFrJNz6hlKgP284WPGNuaxg8B1oDFKK+RWOrygMzs01062p/tGu97WDl3C28ctW1nHc1ZaNawEuIqt2SKOUsR6mN45rqLfzKaZMiV2Kyk008CJ6iHHq4q9Vb018uGut6tcGvVdY7uMLJcwZN0jVFziZvUqJ5p0MMg3SR9jPvVwm6RGj4KQKt726hq21MSrFcRTVnrqEgvb2133i1cMViktY5YraN3iTmxyQvzLqdjyA5S12NKl2OZZSyJC9rMJVgf0hcJNV/aTW1xKwu47SbbdyLywG58cz5MhJqPrDHcxapCbOawuO1QphMcrMsDRspZjDJe23PWJjFdcxOTaW2ya8R54YRiKh5DDNTH7pofkxUNgcOgEtxvF1dEqCcVHAVUQS3Ai0+Jbex0/1UiDbBPKqxLRusVNeIQzArJeLn1coDSuaJJP6IrxXms4KTSIFvG2mWBjEX2SIMFIjUynHBW6aZdXFuJLmOWOe/kjMF16eLTL+CGrnWYlp7+1kQX1nlL+2WX/ACNmRYxLIZ5uYcBYnuA9zqF6bVWOaVyBY3Swx26y1f23Nhl6O8qzW14C+lpM0bRW6SKsIkk0q6eE3sSXNvY3iXtrLp0qLMD6LEiy74tt2CSZnWKKQuNrrViOXcnLR3n7mBu81ihTdbrwqMBCBgK4d5rlIppfF3LzhLM0h6sbUR2iaZaPeyXTepmnt9xVlgja9kla4vN0lxk0wklZ50gqSR5D+r5rJHDNeOMcjxm11IxrNJbXIcdB0JB4LuFQX88FGSXdNcKTK4dkzUd3NEG1W6av8ldb7fUbqc3Uw0+weZkhd29LqbHm1tOcHhp00iC3kWVNT003lQF4pFCPHbWaxBfuVZQRCo5Nlvp15LA8FvHKun3PMTVYDG7qu2EbmjtjHC0VNKJkgikZbGXc6CQPIWkuEToF2levAY51yDILfuFpN6iredi1vciNbiWMCeVpnAqG3tbS30bTOcLu4ku5oIrfToYbvMl0st88pjjRWCgdTeXf/VzGQP0XJPDJx5reQzMXZFoiRw6ABY46MdaFD9zVnZ7jmb7qRwp1B+dPto5FZIOKQ7Tp8xFJcC5juY47meS5muLowCd4ubc0wwMssCdEsSUjjmR2uIEuYLm25DzOSsMxWtmaZBiKblyJypDNJyquQvrT+A8gZORhBtVD9iCeO3tLNi1mJJHS4uEhDvuqGORyum26tbql1c3d1LdrpziKK+keSSCMqJrlgruUrY9Ty7qx/wBB4RYJbI4eKB7SRRHTlFEK8tmEQj7dsb3FBocaVKkMOrTJhPOrMeaWyR3FYSa8MN2RA7VbS+nltUAMc+8y7UbT4ndIhsF3dpFFHCUtwkSOCqBLloFjlLwLcR3RuIpILoAmoWaOows0k0fTT4jBUy8xL1HjmxgDpQPbIwMd6DtvZdxvisEZ+3arO0bdTUMBkW3i2V6p7tjH6cQxPe1PIsEcffJL1TersZMLNLu/4z7zxPcleeAo4yCOUAiyBrdan5cjrtqKfssY1K30swl5hFXM5neKEGmC7pFdTGtKEyZMUwLvp3244NsEbMJDa4ihcERarcvPKvLFJymnXDGWVGltCq22oOGlknMsQ3VG5elbr6ntg+3FLO8Et8qy27rt4fk0ysZHZpLi6mQrcvvBbspdgpI1arqd5ZbHTXQwWjFpWwzANI3meXmudiRyOW/4z7z7W6kjBIxwzkLgxdd6visjcJcVb7zSXHJeR2lBYYgjZqk2UO0hunqPttjl291LEJJHuDbrtWcvIbWzBrrumueeupRSRSoSH0sb7pOyC2tDz7iCWS3S2MccKx3ERDRiCCW2hTueQbhI7Lc3RDvzjzFkVppk5bfN1MDcxJzp7ubEN5IslxSjJ02GKOrm6e6ns7SOyil/144cQ1PiKlkCVc3LS0/Lt4XYsfn/APAXBTgtDIYnphTTJtoAyU4C0SWNnbc6rp1wScVGnRdrUcGsVZw725RZZz6Sa1t+Wt9I8cXoJjPKiXNYJfSR1kjLM8wtljeNo5fUEo11HK8jxqpF1bWsTQ1PEpGG9UC5vnkWelidTFNU8fIaI7LWWbdUjIC2aUZNou6aKLkafp6sYTi3W2gZi0giNxLzixa5ozJGzMWP/eeAoUeHg/Pmj04Cd1WhR6UTR6CNMmYhaxSRllx32SJlXY3NtAXlISOnF5cywSW5uBcRwySKhk0uMgzyszW3OQR8rEvS55G8yLyzZzTGOJ2klt5Gdp4lq3/lzoQ1vLvjGDUkhq97pby4+43QMK+Ircch1d6tLdLW9MrTzm42R30xmuJBzKubrmUxyf8Aq+PaaFOuwv5fjnPsHAHFZ6rih1KSbUoefw0+xtpJTBbLaR29vPJUUawJdXGEuIrevURXs7hy5O17CYiHrRVRU8j8yZWFQSHDJzEgXmw6endadr1s2ENmnUxupDLd7d7Sc+rkbUYHDDBRMxWcDzXNlEH1BZ+VDa7rZJpGkkZkhW4maZh/1/PuAyUHV/z9/ngPBrFefZZWc90YdGi5Ylt7UTS3NQpIlC5ad7279VcafvMtwptJ7R47+zbo2nx4lEEeBbQktb5mKjbJFS746sGYXEw5NCOIzKhQVinGQm5Emk5lDMNXGeZdpsfGaydtjH6afT8xWNrHuq8m2SOWNTytM/8A2H3irUd7dE+AafrQo+aHAdK80PxFfEMEkjHTGiFnp9lGJrkrSjMVwhhiJMCQkvFqt5FEsrb3iuWzcrDfRWDy2VxcxmKe0271K7cjdRI2s9eJbJQLpnPNu7aFVilMbLskowuryPsq4nJmhRpJBBKVSNRcXMpklq0G+4GZbnVGxbzOtMESa7kbaf8AtPvQdIPBrFL+gKFDyvmwjupIrSxiMrXcVsuno9xcSzFrm8RWmvpjJPdX0rqzmRqifYbK4eMSt6mxncyyWh/2FLbEzzC2FZyVAJpDElWn3Lwo7ziR4Q2yZJeZzIuaKzua8aOFF73vT6exjHKsXwWXxoEfM1HSpY1oq2+4b7skm64uJOZNQ/7D7xgFVGycZqMfaPSpBw8+wdKJ6rTVCvMKNCAZXxc7lktY0sdPspI0ivbt7m4H5SHu8UevCy72s3aO6laNJNHYvOpGyWc8/eEBjyBBkC1BrTXIS4jjc2cWYMNG7srVtkWs4GpS7beCIQRa3Jvi1nEcn9RVjOVn0WLnQ3Uh9bJNiJW7D/2HgeJ4qM0ib3kwGsoPU3c8Zgicfa8x0vlhg0RXxQOK81BKqp6oIgfe2n2cckuqPvS6mzb9WSYGEUa+azhtz3MMpRjpMq+pGQEOE2jcwblgHfXN5Uc0jTC2j5UVSKWFtJJGCsctXFu3rccwXo599qsvNvsUi5V4gJkRLS2kO+WYie3Y9B/2fPEewfjGm2MlpX0bbtuIi9tMiwlWwxFLXlKP4+aHBaHSvmxg58hYW66o4t7aaUGASslZyeGOma8CwuPTzapbJDc2GDP6gTaZqdyscOKIyuOtR7PTWgyvs6VHNLNIesl3cqkueuSFjfbAv27m6kAVX221xlBdD/Y//D2dOX2yPtWPdyoLNrbSY90lpfRtHMwG5+oUEnUoxYaV8mh4+fAxjgK0ycQVp8bTy6vc824pqHA+a8BvNCDN9chuZa3DiKSVTGB0waxweGNwBj2zvy4bQcmz+6oeQCy+L6UTTfDRq8N5K3pB3ySOGpwOX/1nx74kIUACjIObo8fqmzQ7Tq0HMtWBjfSrI38llpkFvf6rdervKFDwK+aIzS1ZiNYZ9XPp5G3GmoUPBoeG4Reby3X1l1bb7q6AEUScySD9j54ihXzwu2wWzFb6uggspG3A8DkmzlzUDepVOyIIWhXuh/7BwNGjSefMkvmZsmCLMukRcuKpVJU7WbVrMx1oFobWxuFSarWx9Rc3wi0+z+aHhePz7D+NHx7PT/ZkTdG0MklxM4le3+7fW23BOAKHDHShxnXfStzp/qV/tSdD8A1joOyTSZFBkOYkQRGMcq4YbT/2ngBmsYSzTMkjd8MGX0qAym3TlJ81ysy+l501Q3Ut3fW4TS7GSRpJa+RQ4HwfafxpqNHwKt4zNPGEa7Y1Mm+71Bf/ACWnZfUR0uvIBGcj2Y4SPsjbKrBF3fUMx9Qep4flUeA0TGN7ebfNJ21drzFn/c/7fmgMFQchvT29hGWmvXJOi27JZD86NIOxPOvXXJt9CszZ2Ou3/q56+BS+fn2/Jo0K8k8PjS1NabF6iUHcHwFvsNWj4/yjyt/lXB27X5iD3XnVH3tfjFvBclnPEbthAxv74dxZZd4DBKuo8D/sPBRmkGaUYqIG4uLk8mTSrN57hVCrH+VN5A+2Ogksedd/U2oFU8jgOB8/I8Cjw+TR8Vnp54xfY0fSIymm7ut9Mf8AH3cKtf26nfY5ksvICgH3P1vLaJ2nv32214BzJwFlHmgzbFXq2cg7Tza/eqKWriHb/wA/x7lGahUYmJMkB9IllF36daelipV+5WOp4X03p7Yu0o9w4n2GvC18GgKvEHM5QQfGpIv+OdwbjTo2lvpbc7o0EcJ45ocWO6lXat9AigPzru5XBrFOhUIcqynEg6/jSdpcjMUm8SIAP+M18ew8NuBCOrvsW1jIkx6wW8QWs8TSV8VqCmaAruDdPYPFL7RXyfLHPAcLV1S40oG5vnO6+NXOCzyFEtWlGtA9OJdRTXKBGvFVYXMkdQlitXRaW52HdeNvuVXdTfuBWe4kg+3G4p481jdQOKLUrVHumqSMp/0Hgg6juK4Wk3SuYhBFo9kIYLfvuKzS9TXwazin6Pcw+munHbw+BR8L7LTS7q5prCwsFmZHnPgUfJoVbQjP07CefZHeDV7MsOpPvMWjRypqeRh5UWpLraN8jUyrErKqLaQMxq6fZbxj/ZYhRuKaKuArHrAM1bR82ayJa+e3CC4je3mUjYy/ckU0i9WBVoXwRIJBIjRPQ9nn9U+w0BmkHZGvTdk2zPFTQbat4zGqIsa1isYr5+PJl/KX8dfhzTH7PAcPgUOpstEuLirewtbeW81meVT5pqHjhGQHVWEOkdltZrstpTtUQSS340i9jqxgjhjilWRekdM8LhJLYiKSJDJsekmcVvlDTyl0s5ObLrUmyw1nCLJERat+UX7Vl2RafvF3a7Jbe/sTT5hkVtygiQSwkVmnXbQqGZHV12NSgtQo0P8AgJ4IpNY3POwFWUQMthaM1wgM+p/14DglfK1L1Rv5OsMIqkAVOJpAWNpo0rVaWNtZJe+omivr2OO34Dw1f14W6BqhZpJ7VNukVKN76rcRyTWVxKklpfstR3kLmZ1a3EKKBGOYYIFKydi8mUIS4WMm4sgOTcDn6xqUjSzahuWOTuki/EfxrDKwCLezQCQXVgrvd20llOnequGE0VAlaCxyGQFT5pWxS+U6DptAG5xhv024gUFzSUMQxxoZZLO1zdWkXLiPg/knn5NfPgcHGU+fqJN2nS9RHG0jjTOXU9tYW9jb6U3Ls4zS8m0STUcRanqct63zTeKbgegqI7I7NSUZR6uptUblTh5BYQb47O0lkkitIbWNwir1dkKm7aXsdgpNu1CUoYpFaW2/jrHHDJcPmxkl57/KL9hxttdKiBtNMO41cwJcR3MSzC+spLCUSZqNiadA1OhSkm7JYtlRttOAaUsKY975DSefn3nieBpaUdoXrPJzH0iy221hYtBwNCvBPnPVKNDwOBxydbz6A2ccKrdTS1a6alssNtIWlgtYAzT3gvkt4pLjTrmeSQAP/b5b8vNNQo8FXe2nIJ54Mtc1GzRSMkV6rctrW1VI5pnQiU82SQxcn04ijjinDx2pEfpiFG0vJZxoksgUX9wBpt323BjMca1u+zedI/p+FZK0wbDwuIFnSIbTrGnNYyxtSMa8mSHqjFakTmKKyQT4zTN2ltzD3/A9sY6L2pO2F0CwF5c2reqn4NQ8/wBmr4HQUeLICmo3LirHQ1eG2tba0SXG+WSWSrewjjku5RHVzNduNS0tYYOPzTeOAqzNaIpWSxBFrV3AnqI7a6jup5opbaDfi03SzyaasgFrEg39/q5aM6bklBSZ9se0iHGa1MkzwgT6pcHN35qEZa7OZPphDVkByONxCs6SRuq3+jvBbq+K5uaDYp4w64aNsrJRDIWxkfiPxJytZ9x/FaPDFfisCUzCgpK2kMkdvGqQpwNf2/u1KKPDFHFea3HmcuKGjkhbd0a2tI4WppCputStLBrzX5palleZq+PijTeRxtf4sABjA2imHrw8ZhiMDlTaSs4sWSCC3MJa8ihee6aRYt6VGsyKVBq8iPLfAukcMuoTY1KwYxU7iK+WoPyvOkmhty9Nthtt+JqRQ6ZeA63pFA4oP0R66GpITnJFSEPXyD0GCu3FYJoez5PgUeEYzQXJQ/bLDdp0YstP0yBsgADh/X5/sfPD5zWOBoDaCMgAKNxlN5qFrY1e67JKxZnb5Wj4+B5+D+XwPHygwdLjytohU8HJRZXlLn1RU+tNCaRFuXBbMZWKPJjjjqSFXDpypZJpJXtIuc9w6xRXcpL7xDCYytpVn+7en71iAuk+3HDY0bavpKyB4WRY3FI+zhMizKUK03Q5qJtrHz7TR8HxwTqJOgnbZVlY81REzyABRxXwK/sPy4+PbNfsxuNQgiN7rVzOD1P9TRocf6nyegNfFQLuqwtjmzy9xw/ye8TXUCutzCLlp5JVt5CF54nE72T1LzCnrUSpJQizhFhztdHbbdEGywXt7xc32oZCHzZfuXfW4sT/AOO/Qki7r21O57BLyIlkMb7GiYMrxhg6mmGCOhzmjj3N4PGBMUSN8Q5smiBpo4QpuOHw1JQpfB9nivPAnFancQ28N/qs97TcR+VeOHy1Gv7eS1Hx82YyLKQ83SI9trQpnVakMbrFsZpZoYIvUF65sqBbf/XhzvhMccYiSJY+6WWMsXtlc6jALdY2bbY2wuxqm0SHzafuyfzbMYh/RlRZBPZrFcanp/rIb20ktJYZsUCGEg75Bjgpx72o18KK/rciomK2MccdlaW6FIeJpfy+V8UePzWa3fb+ppsxCm80tfPH5/s/mv7eWNRg5tso9jEE02yVUtOHqBttt6rAZXkhQc5pBaRvNumNzcuttc3hUSNFUm+Z4VKR8NfwNPhzBLoLGGTV02XVQvsM/W5tOsnsPvMRVtS2yJdQenurVtxl7llOaYbW4buB4njnPD/5aU0Uc0uZJ/Z5pMbvceFw2IGjxDrblroUeA9ooV/YcP7Gk6Atvq39VdxRoscfDpUN08Jh9XfNZ6b6SCaCZqsNJPLm0meZoLAWSS86OomMNC5bZG29a+oG+wwZoZZOU2srgt5j/KTq+kkPF7D7Bw814qSNZF1e2MSI+0qRIjLinbtHA+z4PD4on7oBqDb6PTQEh4GsUaXwPHsPG683H7d42ZOI8DwOtfFfHxX9RS03lD3WMHqtQtgJdS9kSF20/MCC6ka4hut4utTUMuuua/yckVvaJ6q1AG3aM8NdP3Eh/wDINGxE0iyWL/kKNfTu7/Ge35+fYeH1DE7WaYWoX6yjulXp8JwzXz7QOi9wqDuqE8y44eeI4mj4onr8mvN3qT8uxI6cPgcBwPimr+p8/Ao0n5aFac2+gwdU47c1YW+95m7Am0Tz8qIkySxHkR+oFzc6f/A9k1mk11dgBNRRkk1cCKaY7iOlfP0u+bDgeB4Gs0fZ5pgrDV7T00sDYLYaNxgn2fHH4oVb2d1sS0VZFjso59L5W+hRPuNN5+f7/NQ9a+pZNmns2aPCJd7mjS18nx/Y9ac18cbWLMf0yhMuk9fZAmZLaPl2p2s/O5sl1LzHt4yTOa0v+XpRzptA59jAMpysOpxPbXDUPxr6WcovtNfHtXPDXbUTW/h7dtyzDo1fC+OJoV8W9kNn+Q5Nc2SaoLK4LjT3MugRbLbjihx+KPBeE7bIYhti+qJ83TeDWO21/Ob8qWhR4f2bzR8N0IrT9/rYpYrWy08LyOOmWyu9w5JlfJnYrCo3SSNy7cnJs/z0n/1jHJUYHsOFuNa3CVsgUBmvp1+5CGX2GhxFfPE4Nava+murZ8VIO6RcCvFD2Dg2pSSH1rESaheZTmzTafFLbQwrtQmvPtPt+aujlGPXV5Odd56mo8tVucGX8a+eHwPy+aPk9TbpzJRIBPYRLM1uCIONvB6e21CZUCHcJCZJIhsWRy3C1k2PpshfTVUKPbdjs+ogpvZAVNZwdCn9PqNp2j3n2Chw1+2ElqyNFP8AuW8vdXyT7Rw8GrPTnnqCOO1ERNzdWcsUsPEcfmj4+DXyak63eozci1mYseEAwYxtLfsjg3A0PA4N52NnRHit20m0N/dWaD26jenchzV19tA2JJpty8LVjGthEsVp7/QqZbqFo2pRmON9kmnz99H3HiOA4SpvjvraREt5+WPDSLtYYIPsHC2s57torC00tDfT3kttb+tKWfqBGU2kha80OBo/iPApvFGhwmys+uzbbX5bzjaI85cADzb8DwNGv6/FtHvYNi4hG46Cq29pZptX2SHmTjsSRstR4j9iL9v3y7Uk1DpKajbaTWms09lbS8639oo+wUKFEVqVr33MDWl0MqbhdyfiZMFBxFGv8rdrAoeeZoI7e2gkjsbVRdakVMcFPGJJK8DwDR8UPJr5PkHgkm19amMzr0FKM0i5WQ/YX9ivk+KNNwaopdqEcxwgjtV6WcQzL7IYwlvM2+vk0aHCPLWiEFaur9YhBzOT7LiNZYL+ES3kn5Ua0SblXllLyrn3ke0UaYdNVtd8MTisEGZNjZ9g4Grfmc+OKaOTTtMSRtY1wRVoluxjVgwAxXyeB8nyvn4+T+XyxwLqUwW9+AlfFL+FsOh6I6bYeBr4o+aUgNBDVhD6i9cMbuEYurYYh9gZyCO3rwPjgtW1wsVtLrCG302Pc/tNfUA5WpXhUzr0JpTgxSC5toJOZH7zxFDgavYiV1W2WG7ikLx3a5UDqcChR9mmz2FlZKjXUN/qxlXRtM9dPdoxtVURrwalrOaFChQ4AdLntt57kSXchzxQ5S1b7OO+TuWh4NfHjjboHnjgeWtAt0EEffCmXk9pY58GRgWNHim3k3MriyikjlstKOy39rRq+oa7IX1K5G7h8VoE+5TIVUdR7B7RQ9n1BYbERipTEkbjDSY3CjwPDTbSGC31G9mvrjTIDdM11DptjZvJMwonFHwaFSdFfopoV80PF++xBNi2c5PBKj6ND3VjIPBuDcIFCxaXCDTQm203T4+VZc3e0Sj1vA0aFBdxCKZSK8FvZc3ok0/ToebDaDp7Xwt/qS777UFPP4wO0UmnuHW3bkzcD+gKFDhKiyR6vayWV5bSbTcx5fOUFDr7HkLIBubSrWKyhf7k9inLjryW8/2B7ZKbulPD5FfH1NISxw3FRuoGpDiSH8auRtkJxR4P5rq9aFbKa1n+BICtvHDJHe2qbZ/bDisfa4N7Ey8eiuiixPf7dQ6R6tIg1S+KGYcV619P3mx7yIyxW0wnh9p9q0OBrVrMX1qva+d0cybXI6Lw+DwssafbafeTLNaQsxhCgNS+DX9W8TfnAO8HPA+aP46rc+qv2fgvQJ+UibSncB+94q4HRlxTUPLefi0jJa3iWGHU+6StxbWIU2J7VGQ5dA4I4H2bu3Qwsxtt9pJFIkqezVhzYb1xJdTlWmHk8beXlTWcjelJ5dx7DR4fFChxNHx9TWvLuYD1I3x/KZ4mtMtlnmvZX1C40i0SOpZ35cUYhh3bifBp6/tJ+UXRE/H5o1rNz6XT2wlt+RFf0gULUpykH4t0fIAxvLnLv5+OGhwZM0ixRyNzdXrS13XPuUd8rhgDmmGCfPzx+l2RLi2lczyW1yZVuLiP2TvhLltwqPuUgbeBFfT99yDcIOXYzBl4t7V9h81eW6XVuytbXBOKlHUec5Jo+L/baWGHtYNLy8dmOY0jgG2hWCmND8vLS9BJ+QbsTx8jxKwRfqQF7+5YPJwAyWwqItIoWR/xkO5UG2ijcxgu7+tDDS6TDtfWG+zYAtf1bQLbr7gO9164NfmKPkcPj6bgSStOLC4Phfx4SNtj1P7Gn3+OcuMpgJg067TQ8WUvKuLCQwtewlWglWaLgxocDRoV8VmieP1Bac9YyTU3VKHDRLZXfO5n321WFkILFH3OV3OT1ND8U8ynqxyVFLXzWsXCwW5IvrHb3Y4L5wNtvggt98/cLHqAzF2zU3k/iBmrSFp57cf7N550lCtr+hD+cy4iVsUwr4PnhGNz/TibtM03qzfjxmr6lmwGoKTU2CaUFuAp60m75sUU+KRXtr1GWRK+RwNHgKz7JmLGYpDbSIUkGORIMEcJBDa6K0+wfTdr6m+nmaS4WSMUPHmkk5lPUY6HqRQpeBPd9V7zc3rG3n1a4iubmvhUO8CidtP4zsdA3MaoQCk7b5KWtEgZtXsX3Q7d9j7Me23cYuM8ujmt24yrtb5q17p/pVsLpfhvZ5uvqCXfNJ+SDeTQFLlabzWc1HVhqBR/zjWc8sMGBNKazwPAUazwlflxwR7F1y6wyLvrPdIDlujCr24svUzyvO/05iHRxE8MN59mIsIKV1Mv4vndQOI6FA0p6mpCQ31QAItT/kUB0GNyP3KK/InCwnIpBiOg3236Mas03S/TdurIftaTKq7/ANHb1lJwKPA0fNRnB0eDljST9o/uceYI4pZObMoLtFLy4/lgVpSWqddkjDFGreTlyK6q9lqLCrO7Cz5Nq+emK+fev35rqYW8FzK0sxARGbaASvstrd7i42RWVjpdxNcw2P3Z3I9XoMxdRqCRwrtzuGeANIev9kaSWP6jAfSdX6XlL1odGxsjUZru2x4Yuu8zdUV8AZr+1Bitvp8Hp/p2cfePdffoqMt/U+ePngK0p29FpYxbD8+Hga7L6fRjSMVPxt6gnap5Kuo5PEUsm1t8iw6bqSTKgMDUPaeE53soCr9Q3m6eBe/G6i2Sg3lwN3D6VtwZNQ1JtUnvGRYLeNxHd3X2tNMMWj3kz3N1b3M9sbLU4ZkDd240pDBJB6jrm93Q2GfUaFqZ/wB+ozisdOryDvkmP3F6TDqz91dDT9Exmm87dxuV5VnktqcHdd/oyDDEfbPSvFA9SKWm4afLuXTx/qrxuv2dfuDLqXkshUuQWkj2JZBufgO8w2yHh4od1Fels8kb/bkTTtRIit5c+41LIIkt0IXUroWlq+Wk/GOVsBsYXofk8NR/100e32Rx7p7/AFbVI7F9P3SafrbYnDEUjg0PNrcTW9QaxBIPU+sqG7kW9u2xa310J7XQrgHR5nMsqefKr1khUyHoinC0aFTtimGBMcAeT5sUEmp3TBzb4a8sjuX9EjKn9t+tHxXwKbhpE5FxZdLRR28L+dYKmkMhiXfJcovqbSEzuX66X+5dR/dkxLG3mjQ6UDuZUbDzb2S46295hrC7FzGD7DX79xWs3BvLjAFeaJO7HZ8fFabDz76NTqGpXsosrbRQI7W+uDc3miXsFpCXLkeBSsRSnaV2OxDQmJ5d0En/APO/T0gkrTbxbTiKXGEGyJR3D8/LCicv5EvVcd0I3TfTsW/VZs+tscmrHra/or+b4CnxR9qHa+i38clpw8Vr1yskJrStkSxnNWLCC2jXL2wWG9Z8tkq+2mGDwWvUMakHMo5Wl8rMRVhq5VVZXQDpVxIVCKkEesXB5eVzUjYEdfHGx+zYaLFDa2Oo3j3txFdSxwcV8upXgngDNK5jJuBtS6h/wOgts1SbpLwFRjPEGh+J6B1xXQ1KMQt+cTbJNBGTE5M9kf8Ax1oMWv6K9rSd8T0PPgmvjjp6lngS2u7b0m0zRbjfz8+4oyf6i0FVdMi/fn/LP27jHOndd5QPwU4KnBbpSmubTRg0ylaQsKtNSaEWuqwzU022or+B5WmURXl1zXzmmXlpL+UvQOwK8DUsW6tQnWe690b7Sse4YIPN3UXOC2eB4CiuGbxCuKHU0vVW/PO8zHDRLmS8xRoDNfTKgJ+CyjladF0j/Rt2zS/tEdfnyaPj44RO0b2+p3FuRrEk8Wo3sjx8CcxwRdqHJ5eyW8TDRvseRzI54DrwC5WNebFy81uwVUMABIDHTdKEjUl+xqG4sNmoXMUjRgloMNLdTPcTR4FeTx0+D1F7dybU9uOBpCVLSFlrb28RUYwE6sBucePAY9RmlxhcRxqdwtF7rs5ak/L6e/8AVzhna/8A4n6S9JfCO1OMNGO5/wAvnHEUp2sZGKsSSKAo+JM1adKkJNT5aNelfJ6j8hTdeEchjeIRzSyxd8kRRlkoS9cK9bMVtzQrYNzfgNscEr9tAYHHSp4re6upzcSnyfYPFDghIMZBq62hq+KFSdseNsFv0qOvmV6iG1bfJMuWH9rcBanOWoZr6WT/AE4e+/vzi3/S2ZkVvtqC0b+YOvAcMe7FL42EyF5JayPT3Q5dITIlDwa8Uw9inFQXJNTxxXS3MLrJnl103I+5i3Q0q4Gc1McSUg6n3H3Z45oP0Pstk3vPUynHTdnCjLkgb5D9tBtpB164mbDv+Ro/sfSyyMdJO+S9/D9KE/cYgOi4d6t/y4D3Dy2BVlHvnhXfBp0QRbXDNKdxhOIfkdDRodQw9idBbTqJU77e4tEjZ49hZStcw1zOpfoxZTmiMUvQe4+/HDb0FHgK+YQOTIMuRvuVI5gzIXOxSNgOFANL0Zvzc7mb8qP8X6bXGnaHu9HeDcP0kbDeZEbKGoux3HX3ocUR2xw8nRmOzTpG2WH7VmaWvnzQo+fBphw+KxuFrdlCZUuEeIRoY2xisUop858n5/QHvVdzStvHAL0QdzL2RjKKczo3bbpuYV+UgG+Z23Sn8vlv5NHzWelrA9nbaYuywuz3fpDyO1vxpD3Hw/UUfa2MjpVnFz5NcVRDuEsmp90l04aev7Z611FA5ryB4PUEdOCsVOO1ZNxa49QJtu1gGMS5qZArDrQ6UlH9D5924gZ7KFRgBQmHk60vbE3mOIcqHomcV/X8ai61/wDRz2ocsOtHzVknNu9ZbZbQALBdfn+nu7VPbGNz57OB8D2K+FEfb9OWiyvqMpea2jLVI3+wKPD4K0c10Nfjx/sR0PXgDSbMhth5mGPSkwVk6uMg0PH6yKXc90r43AVHGMuuVfrI5wrda/8Aq3ZDF1jI647m6sBgDzcP0gPdFx0Fd2sa8CbceLn979RDQOHby1f1oeW4qBt2F5ZBFZ1dqEqTNuJ2+zw+D+NGvnrWAeB6geHGDwh8Sdz5qCQPWx1ij61PEY1UfpfHtyUXO3hbD7sZ3TMd0q1/YDFRLk3B2xBemO80PLVkU53Vb/ueLah5+mE3azqxPMq4/kfpa3b8jUfiMgE9snngOJ420JkTQ4AdQ1KVpbu2Xm3txl55H5knE+ODDhjuavFDoD1FMKFQum68haKSrS42SXKYMTjfLBg/pfHA0KHThCuY4Rkw9Am5iRhIx95j0Tzc+CcKn4/3o+bhu542RbdcGU/ZoV9Hpu1DUv5tT/zP0tatuc1zEYJqxk1n2CjVsqtMsjeh0qPKyyK+q6eNsNqvcPHE+OJr4+PFDx8/2rGOCvtBArxVpdtGEiSYJJLGu1ZyylW/Uxy42OaRcmP9uDtjfIggG+OXAQKMHJpKkGXkP3D4GOGe5YhzGA3RZJfxw+jV77juepcer/Sk/wDY6xaFYTihmvj2J5q2/I27mJrlLeOVTzZGIsx2Sfo+Cp6HgfB8cCKB4N3Vio5CjQyc1GiwqndFJGVHvPAxlKiSOppDI6LuaBBlWxBEo2TsWkg/abq85xFF2qDhZT9yFe4HfTUW7c/cH5HMsgfubguM/Sg2WwJ9JUi5vf0hJuv9Ttt01ypVlOCfPyeI4WX7FvsisJ27Tnd5qDPJ9mfaPPg0/Dxx8cRkEqyhvKkg2161MYmYq6Vt3H24oKNvN21tOXkJFQwlqxtqPFRrsr82UYC/vSminb8yjdIeyOJdtHzIQggyXQ5MmeWybKbggy2lnk6VImEp/wCb+lJHs1nUYOfaahGZZqA4Ftxo8YZOULBCJGnMkEn8eZttsoxacB7/AO3z4o+eBrNEcVhUx4VWkUowAwwKPHdbaj2NI1tzlkt2kM0Lwmhk1sC1zscFXtL8EXsRmav2l5eIl8HHMPiD8SRzdw3q26ogHl25evmc75Y0CLFUv7crZg+B5tU5tzZn/wAbc/y6f+d+lqh5ZkcSpr0XJusYLdrCgaPnj1ZjuXSQ49HcMCrnc74W0o/oeaPg/l4rz7PHA9KDEUG672EYbaWIPBWIqC5YSGdC79kSWWTJGWAgkkYWT06okrvk0OpdgII3OzcAWLZlAVRLmnkNRfhBkugpjgRLtj4NUcfSk6SORun/AGmBCirJgl1YjFqzrLf0/wDO/S1bttrZlt3+pLXdp7fkR1AoePYgwtsd+nwAK96my2z1l3Ee09OLeKanrHU9KNCjQo0KIrFE7qAzww4V0XHiua7qg6pNK1b/AFZaSOCmuN3FsYWhlnjGI124/wDo4DBeise78Y4v2PFDur+3DPXI3LX/ANnxunHdMcmoxmr2Ta9rDyrypP536WrPzbErsuPqje1lMpSQ0PZjs+UGQsZisYd0j3cwcqOly26b2t4z0p/xPHwT5bpwzwPjjio9uIitJOkhubT09GOnikjO7FZycJt4YyOAYtThcdAiocKFpQah6o47bg4iApq/EDi/44oN9yT9yTdvuTiST8qt1+zZqW1GLrqdSZ9Z+lyAI0zc6NcP6q4u441h+F8zDv8AjjaQ820uZyYwXp0MYhGZZW3Se4eKkpaTxXyKPWjQOeH9jwxXUcVpcA7uXVzeS3CLDI64pexpZN5AzUiFD8KO0quGyZPnFH8UzwerjrQ/MZLHzxYZWn8TeDjNwMl+EDf6OkfcurX+bU38r9PTy0enDMc9yj7KkXZUvcp4gCtPl21EMzSftzkcuzH3fefy8iTqB5Xon9T+Q8fPmvBJpfApItwyFreKbqe0l1wyoz1bmPcSI5JJEaNgorackZNt0pmzIq7mEBw21aj27QVzu20HBrcDQpvzf95f206KPYfxK5rAFfHbtlffR4WqhdN0f+LYEmapv5X6edp1GBUGrpuZanXMavheGDi1H3cbLqTO+4dFhU4ubfpB7vlvCnufgD0PAGs9RR60axwBrmNTNupQC8igBc4AOG+4FO2h3EKUdX5aMQ5mnAR23LEnRkcUxyxVQgUqMtW7FY3cP/o37nge0/j4VHDM3QzjDrQX7lM4XTNGbMGk9TUv8j9JbhSsaf8AlvqMO9nG6XEXzcH7JPDFJtzo8uzUZd41CxKuUJaGSLMrdie08CcV4LcB5biD356fA444GgpoDmoe2gcNCrGvCvGQFQY29IVrK7l2F9vQMwcd5VsvvFdxoDHEDuTq+Pee6kXDyDpcdaTqzDuoMTDYztb2ehsWiqT+b+lBq0tw8GqS29/JNJdSwBkgwC2aPCMYt1QheyM3PfWnp/uXRRLjO+e76J7/AIoeG8ijQ8jz80xpB7fm3PUZjOxmaWIbo3Ksihgx2HbtJxtcjYNscYRdihkpkc0eZHUezapHtjPWNdrHz7Mdf7BO+XtBG5W7o2/PO9qh6zXjFRoX8aup1D9ICor2eIteEtCw3qcMeAru9Hpqh4JEVLpnMkcZ+3c9i2PfJeRf6y+75PSn8p5k818L54fFfHGOMvRiYVnFRd1THbRIdWAwu4NFmijAuoY9aH5C4IqOUESDMajrjHujqPrQ88D44rU2Mr+K+U6SjpXxbELPM2b7Sht4Rj/a/S//xAA4EQACAQIEBAMECQUBAQEAAAABAgADERASITEEEyBBIlFxMDJh8AUUIzNCgaGx0UCRweHxUiQ0/9oACAEDAQE/AXPYThLcyzd9IdaQsNfn/nrKYz7SksyEzLAIbDWMReFr4HC0EtLS0tLYWi63FtDGU02BGvl8PKK4qC3cftLQgZ+W238/8/WDQW6rXjLeFYRaDQH4Thtai2+TKrArY95V1Atubf2lEHIxXTtBppDGeEZlt3im1jFXV1/8m4/P/sRuXzPS4/OUFAUCVCOW/of2lOsAgh4g/hhJbfG0MAlpaWxtAJaNoIbMsIzLZ4i7GpuJmEdwjh+0zewItrKiW1E0yken63lJTzFjP4rW0gfwc/t2/KUFy8OoPeExmxChTpHA5q3PvracQhPDirse/wCXaLxIWiHTUnaVMxBYnsw/SUvcHTaWlpaWxt5zIV1BhaoIHLaXtBLiXmaZ7TMDLjAEdoOp10gZdT6fpKfirZSLRW8LMPT+f0nEDlUVVfw2/XX+I32YCDsLRr940OCrfwx1qZFYDUf4lcMc1IbfzKNQBxrpKS51YH50MoNnW8tjaWlpaWtM0zTNLnC8vMyzMJeZpcQG0LkzO8DW26zEULWdbThbtVLfGZ7oMw98/p/yDXQ+sLjeFr4X11i2baMWzctPzgoIKqX1sTf+04ZlVSTq1/0v/wAgoJexO0oLam1j2lFBSGQnXC0tLQCWm0LwnHQQmGoIzpexgyHtM1ITPT3nOTtOasFYbQVb7RagMDWgaxvA19prDA2mszCX7wC5qW+Ep6nT51EratpNpmw942Et5yopzX+TKZX73z0/OcTVDI1KludD+U4dOQyZt209fL9J4i2Vt/4MR21zGUkYcQ2aWlhLS0tDpGfywvGfLGqXmYmC7TlTlCCiJyFgoKJylnJWcoQIRG01iPAYCRtEfTWNVvpEYAS4MGUSh7r1DOEpjl5jvv8AtHsNoRNsLE0sw3vEZKyGsO0cGoBrqNpkOQsBroSPTvOENSst1965/eNw/KqBr7a795yqafag63mqhiBewlYsKyqN7X/mAy2OaM2BMLeUNp3iJf3pb2Zore4ii2ANpcwmZ5UqELMnKphR6/nKDhKWQ+X7/wDMSIHBuPKXCqB2A/eWfMAdO5gZPOaNkyg3On5TPUp1GWnpOGRTSzX/AOyxXWAeC4b0jEqykTQatpBtfAtM2Bjv+GMx92BYq9z/AEJ0hMtcRha15XufDL+BQewGBMVid4o5mcDc6fzK7BqgpLsfn+JRpBQT2iBmIF4n33Md/Cum+5io1biTVY2Cn8zOXlYotx+crcQPrJoU9Y6AZKfdr/oIgzqPWU6ukZRvGVv/AFDgWtGqmAmJTy77xVt/Q2hhE0hQNvDpqYNdYZaNZfFEXlnON7fJnDKXb129IWHuJsJwwseYdhKTtVIXZR2vqZWVPrANs2nz3nLqGncKARrpeZcvGNlGmXMfS0pZXZa/wnD0TU4VBEVclraRKuRuWTeM18DHbMZYuYq+UAt/QqhIvLde8XVwsYcw2lU5iyrta0FlpW84fD7piIH8LbSiiUWDATheEZU+13gvSa42ldRTqVCNmWw+E4bRQsC2N4SEObtCg7CHBzG1OWUkvLW/okFqV4RD1EibOIVAFhKCI35nf0lZgzeHaHWUjg7BBdpepV2FlnFqFqqg8p48oOb9oKt7BNZVrkWVtLxU8NsaptKYLRBYf0VIXMr0stG/lgwsbdLazTNllO5XmHdzYSsQLr3FhAMoCjtim8vacpyczt/iCkt7z6SF2bLudPn+8RPCJkYHwzPbQx/dtiWzteUl/o+B4bmtrsJx3ECo5VdsG1EsCOi1o/iq27W8XpLgLTO3l/n+Jc3JPQDDVvFN5tOWTWaqcXUNoYfDgYq2lP8AoqFLmNaV/wD41OXvAIYmotLWHSi5gV7E6yq+dr9N4Il+8PQZV3wIuIws1ohvf+hAnDWo0izd5Wqms+Y4ottZuYT7FRDFggxODG5wZbR1uIqkRTcf0HDUc2s4quKhypsIBiY/l7JRAYsWDExtBgBE96zSrRK6xqc21EGvtqdPM1pxlVUQUUxEEY2ha49knnFijWAQ1kBtePVyLnfQSiXY5279oY8tpFTwj4x7FjOGqrVHLqStQYaiFNLwoV8XRb2NNbmfcgMdzHuWN4BgNoITcxRoegC+0ygbwm+IibRQJ2sI+fKNe8yEe6NfOMM2tWWZV0N4uctc7RjvG2lI7HyGGqm4nD8WNmlbhRbmUdoaYO39oUymIgO85Okemd/YBSZwtABbnbv6TiK5qPmi6nHt02gQd4zgCE9AixVvtGXIbNDlayH3ZWu9UFvdGg9e5jMzDIDaJlXRZ9YCi5jsDthw4+ydj2EGFpw/FtTaxlSnTri/eVaJXw1f7xkal4W2hfS0NjeMLHr4Kjm1M42tb7JPzwToaWg7wU/OW8oY3SmHFDkUyfxSm7Ooz6GVTTqHT8O3xjuxGca/O8UbawvbYX9ICL2jAZrid4oP1Vj8YMSJTrtT0lDiEqjJU2lbh2oC66rKnwgjgnXqRL7TMKNIBY7ZjBFEONpaAWwZgIXPUmHJYup89pVLLa42jK2awOvnC2W118Mp1Fq+6bwsoqEUu39v9+kpMNRNTG0h04AesHRaKSs4fjsvgO37R+BWuvMpyrTKGXuuWEW6Uo5aXi7yvU5jaYCCHG2DN2hJ9guCNkpkNqBF8SZO5gy/dj3P4+fzi5uacsqvkS1Lc/rKdEKoEaku8pnKwM4geK/nDUH1TJ8f8dZE+jOMZfC20+kKanUQi3Slrx/tFKxrX0xOAxJh3h9guAvtHUfdod94oyHL8/CZclM6/wC5RoEnO+h+fhFUg6mPtCJWN0Ev4bYDqp1TSbSVAKtAONZUXKekaynYrc/PaHQ4biWx2hN8Kwtb2AgwQZVz/PrL5TmOn+B2/n1i+Il2nvWvF2wtGEdja0bbAdRE+iq170mnG08jWh6BpOGe9hfylT7wy0taE4CNjVN5RTNUAMqDKxHUsGHE1PEETb51j6+D5+fONr4cF2xMraGDAddGpynDCcWOYMy7GHoBnDVOWSbRzdzNoTisY64GGcOuqtK/vX6lGKeEZj8/PeJfc74jbornNvEtfxexOs4Wv4chnGUOTUt2hFjbEECLvpDodZfC2A2jbwTvAbmcCAtN83lOI/Cfh0iDHl5iW6MwEXXXGqO87+xtL2NxKw+t8LzO4hxEpg3liDrgNY2LQxpT3igclAvefSSZHFtugS0GNKm77RzmYnEmLi+K9bYfR3Ect8j7GcTQ5TlcRKT5GvNzhsIYMDFXMZuYg1uZw9s4Tyn0xR+zVx26ANIYMeGqCnTOYaRhY4jeKcahg9iYBNtZ/wDppfGZMRpi0MGDaQg0xbuYs5QFG53lAZUD+k4zxJk85VtnNsB1NmWkyjvPe0O+Kby14BhUxWDpPRw9TIcsrjI+mKmKL9A3hh10jEsbmASivNqAGDKUKJ5xdal9zK9BEF1wUdQIfhid94KmlmjLpmGFPeDAxzrhfAnv7EKXawnFWZQPKEWNsF2g0hOI3hjgKt+5m5lNFZvFKAyjTeVG5RzD4RU5a285xrfZKognx6g2VCB36Ke8GDG2JwHsDOGTKuY7mGoWfSEWNooBgMEyE+7NtDgJvKkp7ynsfOItkLSl41yHznFuVq51nE9hFFr9fFU8tyNj/roU641DiT4rQHBbHSFCJfpRM5ldrLlEY64gW0ma5gcg3EFQN78+rq/umxn1WpzOWZVspyiP5RNROEpcw+LaZSw0iavecWeY15xN895+HrbWmw7xhY2HQjS8JvgDvMv4ouKVB+MTlA60zeG4NpfAymgUSoxZix7SrbNphe0vgIE5n3cWoBo0+vNSFlML31OCC04OkVWMbEW+e0Bt4e84in9rkE43wVMvlB18M2Zde1xK6gbRksubozYMZuYmogwEOkpVMpvM9KqBm+fn4StwrLquonLaUaBN2Mr/AGYt3hfTLgN4T0A2N4p5x8RldOWxXCiu7HtKKeIKZS928DZ6thErZafNA17Siv2yZu15xNTmVC0HXSYWLiV6WVATH+7X8+p2g3g6WXuIrdjKbtTjcUr7wcQKYsu0di2vXfBWIOkOApZaAHnCoR7/ABt/bSfermPuj9YmmbtGAOSce3KXKPn5vgOuk5taVmvlUw+5l6XOoWPuBF62QGLUYaGU15psJVQ0zkh9iJRpcw2lKl4DmlU5VT59Jw/DkupqbbxyNBBTJtTG5NzGsoLfOk+kG5lm8yf8YDrvaBh4SYT0r4mvCMxv7Ei8So1JrqbGc25139lTTOwWUcgpn1tCCv5w0iWAjaVrDsIEGrGJT5d37z6Q4jJTyL3i+Kmp8r/4wHWRA2loeiq1lMBskHsiL6T3dDL236yYBfSCkL0/QykhdlpL6xqH2lh2nD+N/n1jVcju/nYQAmyeUq7WlT6Parmq1fP+wla1OiAve/8AjAbdZ1neHoY3NoYPaFSNoD1Ad5wSjNqJRU1St9gJ9GXqV3qmGp9m7ecoowFtpSF6zVW2WUw3JzPuf5nFcUwrLTG8r0udSvfwi5t5zimfQVN8B1/CWh0h1OO5vE1i+zO2BQTxLtBV08UD3gZe2FMLrmnDMqJoZnWndkG0WpTVWYHecwlKdMTxWzsdPn/E4XhwKYDesqmyThKHjNepu0zZaGU/ETjiS49MANOs7xt4d+i28p6LrB7crfeZIBbCgDaUwdABtBRuMp7zkF6Ie+kI+1yjsP3mjNbsIg7ziELLeFshGaO+UN6z6QNqjAYVDlQUx1mNEUkFvKVhZ8G2h0l/D7NENQ2WctRu0tgU0uJyTvMusK62nD0GY3AvPq/iyAxMq6sY6rUYMGlT7uL98zfOg/3KK+EfHB7ZSIxZtLSvUCkt52nH1FqOWXv/AKiWvrG306zDOHtyql/h+8zG1jgY4ufSb+zBttOc5FiZQp81SoGsWynUQUy3j2nLy+9vGLIvrKNLMLXhRaQCsP7SiAL5vxbSyjSmYlEn341zYCcOL5mlMd4Y3iBEpcQ3MAUaT6Sp3RhPwKYvnB15peA2GDNlF58YR4oCA1vaDhqpTmBdJwDcwCn3Eq0aRvTPvSlV5RysLiNQNUZ+04hyd5T4qjU0qaT6rTqU/C1wJR4JwcxOnxiLYYfjWU1AQKveWjHzjLppDR5VElZxC5wvxj+HBev/xAA5EQACAQMDAgUBBgQFBQEAAAAAAQIDESEQEjEEQRMgIjJRYTBCgZGx8AUjcaEUM0DB0SRDUuHxcv/aAAgBAgEBPwGPx8FeN4EKk6ihu5fP7/AkrYOl6dxirlSSSyWEiSP8NnJm1vKxsuNl/kb0m8D3RyzaqlPav3/Qpt05bZaVcR32uKy4Lly43pexzpc+9YrO2H3ZC9xVMXfKMTq3nyuxtXbX2vcSXbsOXhQU3912IeuDXdftEfSlE/iEl4VjxIpDrDlfS5cQ2XLlxyHMuXLjd8IT+SLUXjgdli90XJPdTko8ly/kuMvYvci8izNW+Dqn/LVvn9CO62CnBTlsfYhJznKo++ltb/dKPqc4Ndriq+DWjGXEv2ytOpKSjDudTC14XuT58t9Gy45DmORf5NxhjVi43fS+ik1wX8rG9Ycj9P5FVWUYvuyzjWT7RV/xOkm4U3J88/v+xTjtjotXflclPbTrKfaxUpx8Xd/4P9Tpavq9R18sqSPuqXyX1bLm4uTkOZuL6XL6WZZm02lnordxbGPyfQstI4Z1LlKKklydXHMYLnBvzL4/f+w0triu+iWlh3XJSh4kvoQlSjPw7c/rkqJ/4enOCtfn/Yh1PhpKfY6+unFfRohNShG3YuXNxuGy45DmX0volcVNipy5RtkhU6jNlQ8KZ4THRY6NuSVNoaLaXRe5Y2kSS9Sv8f8Aw6pcvv2KfpjY9xbS6vYRCyWeP0KMnRk18lanKtJJK0bnUPepUqXdfoUbTpqcXm2f9zq4KVO8rs6ZpUWi5dm4cjcNjlra5GAqZt2mS7NzN7PEbN7PEbN43ci74ZOBJW0ksiRYZm5VlurRpx+h1FTdNxFdlzkjln+a2vyE5bnTa4F6Jbl+K+Sc/Cs6b9N/yZ4XpvfDuKpRoz2ikqSjSisPudRK8Xtf0Oly3bsbk8DkXL3Nw3rYjAjHA3bj7C3kVV2JvXAlc2FKHqu+x0r31PF7v9CpTbq7uxbRMStK5TSgldkowa//AF+hG79qK/TylxHnk6d76Pq9pOlT2KMUSTWHwdQo3W9X/fJ07u7cEm7W5N3wXL+SMLkaffR/Yvy86xVxRL2Ny8N3OjSgrspxdraKNyVPGCd43b/oK9Kn4j5ZVl4lR04/iXUnkqVaVOMp2zwj+Gbemob6nL7Cr7oWlHj6nR7qqlN8Ik/Eq2XCTZH7svoX3EmnyLYne3kjG4kiTvgb+1er0iyLLM3NRsJbsIlZYQomXkp3fJN75wxf/n/g6qvsasyMPDW5InPYrnh7IRq1X+B0O6cHYlCNN7pSv84KElSo1E3hP/4VE6cZR+UVdsZRb+EVbydza5x3LyRRBHH2yHoxvVPT3ciwiwsFT0RuipUVGm/khLbZ97FO85uf5EY71ea/uQtuTZW6rfFxQqyhSjFfBKXjJrhlJudKfTLm6/I6h3lc7Ee0R1JWtfVFNYuSdi/+hY+fLF2EWN3wVZtwTRH1O9zqZzhdct8EKfhxSFgeBzyKTeEbIxXrZQqqpUqSb4RLZu2yz+Y4Nu/CIUnNkpXe4ekFc9qH9u9GyTIu8vKhLFy/pZl2j8lSok5v7sMfidNup7ZfCF86y4OSnONOOFkjO5/D07yXZtnUT3TbRux9BK+UIbvpTgTYv9FUntKULIeq4LEX2OSb2xil7nf8ih6qbj9f79ySzjVjPDzcykUcoptQpbe99b2L30REln/QMZN2I/zORaTkoLcyNXx6iUeFkXxohHVSfq2e/go0/Cionckdh6Mm49inK2LaPREONFhlN+m41b7Z6Sek/VKxCO1W0eD+JVt38mJH/p4bY8lOOxZ5EyPlmMkxEhyaSI1ZPCF9S5zpFWWiZTlZm9Mf27ZKVinG2WIbsrsqVr0lL5KVnPfI6am5S8aeiLi07Hck9JystJFSe/2spw2LVCd3qyMiFSwnfH2j0bGynG73PRHVy9OxdzrJr2fB0tHxJWLW0QvJxoyt8aVHaLOmgvexQlJXSwWztWX9CsoU1sXIiHzo2JYJq2URkRnYjUTx9mxsbPcLXqKn81S+CsdNT8OCQ9Li5K1aFJXmxdVOvigvzKVKUcyldj50ZVeR3KibauUnT8RR2jqXxfBH05pDu5WkrEtkU1yRXBEejVycCM+0jcKo3yOZ4iFNeV6NjZORGNkVpuEG0Ql6Nw2VJbqrfwJ3dyF0luGXHUilkrdbP20zp+lrVZ75FKmoLB3HyMkSdyc7FOtKsm4o6aNRz3z5RQjtTlJ+uX9vkVKC9U/7E1KplsVBz4IwcXkRLlaXOSdO4m4kZd4ilfK0TIu/kbGNlR2Kce706j2m/wBquN2hdna/ydHS3O/ZG5IrVVTV5FT+IXe2CN8pZk7fqUcfRHSyU43i8C0fIypwMoTnVns/Mn00aM9tN4On8WmnUvn4FBR9Lxck190WXaTt+/32Hci3tsdh+/VDRKBKLWURnu5FpET0ZfJIbLbpCG7WOrlZWRTnJyJztCzOSNTbBRieLCnnudRU8Rm58Mo9NUqP6FPoacLOWWLjRs7jKz0i1SvSSyUnG+65CapXx/7MSfNn9SpTcPcQ3Onun3/QnHH00R/3NVoxxJU75FUcXZidyDyX0YxjldkY20qL0nVWnG8fgpr0bic7jfA57VsibSh0rlloh08EJayGMZW0rPclfkqx2vLwheqPiS/D9/u5Z+HeaKdPe054iVq26WCFSXBPgp8FvXfVeRlancpMixSLjGMWGLSTUotIpSXhJfRkcIl8FiENzsih00YLVC0ejGV9JK/IlKT3yXoRKUqy/f5Epuo1GSK9dJbY/iOaa4KfIncp+ReWcbi9MrEWLguMa0es/wCRU3Lhjq2e1DHgpKVWVolChGksCEIQiWB6Pgk7IqO70rO7VNcs9vothfu3/JNKC2otsyuSXOlyDIcaPReatHuU3cpsQ3o5XxEqXXLNyS9zJ9Vt9rJ1pVCnC2lVn8PjaLlqhvAndERnbRlV4sS506KO+Try/D+huv8A0X7/APZzLcxkudYlPjVeeSuingTExiPDiuxXqRj6YLJV+ZDbmyEMfQYncq4wdH/lvR6MpcHA9OESfcqytq5X9KX77EljaP40fPkosf2U49ynLciDHpOFSo8uyKlqUfQiVOVR25ZDp1J7F+LKsk3tjwhyvcWGipG8zpV/K0elTlWKXcfA9JDZUedYScfxLj02NsmksLWi82+xenJH0TsLWpLaTUp4iT2014VP8STUY7IFR7YnSxxuZONpJD7HRtbbL+urHyzpspnbWcrG/JPVtIWFYfOiVkT51pci1XletaN1dEJXVxPtpUTeCvLw4WQ7Qhdcj9CIw8apZ8I6aO6SR1ENsI/ImdPC8VJ8jxrNYudNK0nEbOwypK8rEO49ZK7wXHzpPgmu+tDyLzMQ0exkXbSbtknbbeZdz9bKl+WdFStHPf8A2OlhtZ1ebsXB0U91Oz5RzopZHzYp4lcWIZLk3ZEebke/kh7kz6ktKvtZKe14G76dP5F50ixUiRyjsSe6Vvg6qWEvkqTUXZ/v6G6U3kUdkH9MFCNopnVxXhuxAh6Ntb89XhHe7HwKblzpXeDiPl4khx7o+mlf2k+dEUY2holovOtJshyLghG/JVl/Mc5dip6vUdPC1pP9/vBVi1TUUWsrHUK9NkFuwdJLdTRFbVYbG7kc4G7lNZGVnd2H5YrNxfGjK/tJc6U47nY+mkUPS5fyobsTd2WsiKK09kblWNkovlm3fOyKcf5jYpX06j/KkRe2VvqdArKUPhjHpLBFYsRGN3yPy0mSxp2KivEfOnTR76IivRckra3E/LORFEY6Tfq/oVJ74uoLp/CpelZwRhtjYt8CqOJKalFkKGHN/dZSp7ZyfyMky9udI4IksI7D8qL3Gta9JRdxQT7kI7VbTbwRf3SpEato0y/yJl9GNiXYpp2yMlT8bF+f0FTio7bY0eTjkseGmeCrSj86yeqeLlPKKvt+wiy98FtJRUiNNR40SErK48SJK4/kaFZk44LNEZm4nMjl3IQzfStdQduSnT2R8jQ8EXdX0Y2MfBtvKzJP0sitqsVfaPzqV2R5YpeWCufcOwj6DWkZ/I43yiSubLG2/IkRVlqy2liw9W86LDsPsfJRW53JclV+kfu8zER5uPyRKS5YxYwXHkauNaRnYcYy4JekjnJGPmelxjdhyyIcsYEjd94WSgrY0rPhHf7BadtVwQ9K0sOOnAo3GraJ2MSWSMMEF38/A2NkudLi4N3YlK9kdPT3PcyWJPSr7heanK680FdiXqF8+Rlri5JK40WItxdy+7gTvo9WPRl8Mk8bhPBLgjHdg4yRI11FKMRZk7iKnv8APTltfmSInbS+qwS+fLwRqJ8nbzSl2J8DditiCR3Q2PEFFcsnZSsilTWxyZTnskRS+7pL3C8zbxIjK607axQ8DwcltWPVoesZtCalybc4LWJXXJf40llizhjuzbls72KlR7sC5Ks8bI9i15XKXGkufOvbYoe3yrsP3YLa8MbwL4E9E9LDWvApW4PEY22IkMubrSsN40ZB2LX4Iq5S40kLzJ4KSsdxaR5I5yRWbeRkuCm9EcDyN7csbv5LlzsSkbtE7YF7h5iS50Rggr4KcdqsyRUF5o4uU36bkvch6JEHtX9SOH5e1haIZFFiUET9LHnVZZJ5Fkl9NLncm+wxCwOmtuWdPK0kS9zGiquWLzOkhQtqlc+hH2jV43F5E7MfOrYsaOpG+251Cs7ib5Hk3WwU4jpTjlHiSTyOongb0lwPm+iQmKe+STIOzOdK3t8//8QASxAAAQMCAgcEBwYDBwMDAwUAAQACEQMhEjEEECJBUWFxEyAygSMwQlKRobEzYsHR4fAUcoIFJEBDUFPxc5KiNGOyRJPCJVRkg9L/2gAIAQEABj8Cbc/em1iUyjEUqXszOIzknVGiKj/EVTxEwXYBHtD9lFgt7TQTkjUqHGyDHHFvaqmlM8Uw07pOZ/BG8pvCUTcxvWXmuHL8ETv+qFvjkFz4BRALeO5NmQfmFxHyKJAwmbceqtlv56x6mO4e5w7mYWynXtF/ipMzhiJ55oEGHAw4zkqbneJuR3ORpk4QYc2/hH4pl8TRs4p1XQT8ILph8fVMwOkTNt91PG/qbdzELP4rDWAg/ByiWnsjZ2RZwvwRFUQ2sbhmbHcQtvIOh8fJwTGVNqBsO3R7p5c0KVRxOhV/A7fTcnvxFtRrvSlvEe0Pku0EM0towuHvWy8xcJwqyHSSJtKnEe0ccThuU7944KmYxVL4WzbzTsJJ7Q4Mc3CPZS+tPZ2Nl2bbGwzRc4vLeIdBKG5oyas9RacnWTaES6MVU+6Anfw/2rhhbGVNn5qlTbiOZfG/9ynBmIPZ4eQ3J4IAMYTiyum4veFNschJQpE7eGWvO88F6RhDC5zajeD+KFEz6PNTdZXaICvnmV+CAG0ei/dlnf66jBjl+C/d19OSvqt6s97dq948kD4eWoapVzaFg9yfmnWNvmFlsncUWswjAQ7LMIgNd2NQeD3TxCwu8QV9VF33oPRBnuv8MZeviJCa+kMZaIwk5jghU2naO84HA+Kk5CnpDhHsV+HJywOhldthPsu/IqOx9FUOF9Lex/JCk6LWxb4RLPafDXR8jy4JtfaMEl1v3dCHTECR7SNYCX8OXEqm+mXHfijK6qMpNhtIOOMjNZYhE5XT3sGEjPfNkHOOY1AOvdOYd2XRGo7+kcSjT0gR2oxvb7dQ7hyCuMPvWVOgwujARxlx3n4JsezsvQO/EIWidowAw9xI6JtRo8ERZDSIt/nQMlTrUgSybu4jiqYxOEPTzzW0ZPFDceKohuKAfCqnVNienDVvnuX7l1Cy1W1W718+GrA3afwCDatycmM/FY60F25gWKqS1nuK2uNRMR5LtLbO+FhxAuACbUwg4DMckMcyPajMItJnhr+cLE0w/CCXYecLBVb2b/r/AIB72tJcRBaPaVnYmgWdx6phLoZGy73eXRFtT7SIP3x+aomPBcHDmqmh173dhL80528CXGL1E2RsuiBB2YRJER7SY1rcOijxAi7irtw4TGVv1TmgEwcLuaOQaGi3BAcNRjND+Gu8Wc4+BvVVNP0lxeG2YTv5hOrYtuZlc06uTlXYwf8AbH4rHaYi6rtqwRSBLSRuwwPqtEos9oYRCezaDwMZ6SjRrOPYuaZaU7Rs6T8ZpTu5LC72JkKdy2fnmr+HgqXGSY3J5A9o+pt6oa4bdyL6h2t/JRSOGnvPHouz0aB7z0WaLtv3vKx1Djqd7jyW5FnaMccoWFwPZZh4zYg2q4Obufx6oltUdMWS8fyW/wCCyKgUpHVVKZGFpacPXgmsqU44SE1jq2CciVNbSHnk1Xxu6uQa2By9Se4a9AYg77Wn73TmgRendpHBP7PZ0mkdsR4vvDmtzTEP4NPFOe0tNRtnwPFfNU+0hzw+KYyLuK7R5ho8WD2juhdppBDaDTsU/wB3VR7zgMWbHsrSHtgMxHCCP3zQY50xthCnGZBf8NRc8gAXk5K+Knox8nP/ACC/hKPhPiDfZHBBrpAGTNzemvSnSNitI5AEKoeDSi32g5tExeRmtGLoDKIxFQ55ZUuDf4DqmTm0kEH4KpQfeq2R4vKyL3gTAYPvc02TCjFBm5Ch1WH/ACTGYsiZ5KpE+LVz9RzQv6kkNxHgnRSiMzKBLGDgJupqljW8JUvqQ3ID3uiDnmBuBKc2i8ECx2rL0ocOfaqw0o/1LZGkH+pYYqt6kypNV7RzaVtaU5vVbWlVMtxQ/vla25EU6tXiWuyKGHGCNxdIWxS8plbFQDiyFtdt0Dbr0tKo9k2JsV/6VvUuWEUqbeBDroFrQKmez7Sc0ZjMRknseWg8Cuy0iq9o4hRV0p73H2WmSg9rTiHE6nsdxt09ZpUDFS8T2dd4VHS6BEizo9pq7Wn4TLjO8IVKoJkl1Np9v9EfbJ8bneGl0TMRGQg5lx5JmNrH1T/l7qaFOfRjZBn2lR0dsY7nPcjBjE/C6OCcbw0Q26xOdZuZKs3G3NlOd/F35I1azyKfujZafzXomB1Z13O3NGqLeaaJs3JaaBliqZJnB5aE0tt6SrVPTw2TnYsbTGZmQFQl8kPyPNYqVQjEcR4tQqNJaSMSa10APGQXZXEXDuKGAlxN/JZ7Spv3ncnifaK3eoy1X1x3fSPaERQBceMZINZTbbn8yi81GufxjJNhxqOOTYXbaZW9J9F2Wj9u8HO+aaK+kPFvC1y9CKnUodr2xH3nR8kSH9i3m5Yn6b/5qO2qVuTSSvRaO9vV/wCF1M0W9KX5qKzalUjg6B8kcFBpnc+6xANa07pWfwUY3W5ppfUe6OLliMn+YyposFsxgsizCHDdO5DGyHC7Sxds3Ax7d95QLtLoUntyhhv5oYtIk5AOdGLksFEBuPwuba6h9N4qN8VlBMdQm1KZE+H8v3zQI7nTVbusd77SEXUwTTfd1P6kLFTipTM4G80+tpL8VTeeHIfBNqYcOizAbvcqeEAPBifcEJ+B2KBOOR8EarrVSZDd8cVXl2c4XT4Uzd2TbjiU6pWfBcZg5nonUqLHCk+4A/Eo1a7sUZDD+5TJllKJbvIHFCho7MNFlzObjxKy1YsgbAqrG81D8ytC5DH8G/qqlXfTo4GjdiN0KV3VI2Rl+5VNwcWlu1hzKfUbi2XmeOE3Xow7EHXG5sp7A7DTALfMWQ2T2gi+7BxRLh0hXlUQDc1S3FwTre1bmEZU+osjPc5risDW34uXpNIgcGBYacDi910KdORR3nisNMMY3gMz5r0pik3Jjd6LhSL6p8oWN/lwCgOkb0C3s54BmSa6o5znNy4BAk1HO37Su19Q8zC2dFpf1SVstpt6NXiPl6rK6xVKFNzSIIDfmmupk0XjLCy68GFsYoLt/HpyTDpFVogguYNkHg5bLsFKo7a333FMFSGPPgq7if1RBljwYLHZgp3Z7DuIQcRs1Bi6O3j1dKpHheg7e0o4WuEtLp3wsVSiQym2BT94wiyTUqEBkt8NPkEcTsjJcd5w5JznCWl12pzhhMDCDG+clLp7Gq8meDuaqmrTvOR3t5IYmtc1/hJ4pj/aBsOKdT7WP9yrHs8By+qNGjIa7M7zrNSsNgZcz+SY1tsO9EnP0n1KY6PDopv1hOixqvwcoWKm7AwGAeDQhpEBo6ZFDGW9rWpDaOSMmzWnG2JU4I9JMRliEKoW3qz7viG9Y6Qw0X5cRyKBTAYcO3yidxVFonKUePqZ1DuuFGlTw7nFEV6luDXQsVQAj3caMU2t6K4nUN6tSo//AGgsLRPJrFDhBWSBDGdMKmIm9hq2GOPQK2j1fgp/h3wpNCp8Ft0Hjq1XBHkUHGswTxn8lg7WjB9pwX/qNGMffhQ00nfyvClzLK7I8tQW3iBi0Ju3MI0y3DisUdFe1pcMpv8ABDtLvpjPfG5RXeBsYoHtN4p4pPGB3pKZH74r5H1T+IuhwcFedoQ7fKPZejBxDFhTXPG3OJzY+6nU2Mws7SAI5Smx9oxrSTC2YwVPEE6jUMioPKsPwemtqnAwbdOtvz3/AIqKjXA+ENb72Yjkj/Elg0pxw4Y8A4lVW9pgJggE58yr6rqBs02/Eqm8xLzsgj5p53NFSfmnDeadOkDx3lUtrDuHJNfVfdt+zZu6pjWU6bZPtAuVMYWhpG4c05xP2h9HuwBPqMu17Q7HuCpVqNqVsJG5WsagkxxQn4qBhxCqMxkqFuR9bfNW1bFF7k5jCxoHiduCwNON3HUOaLqldpqbqbL/ADTZIAKxw2rUjJxJ+UJ2BlOkHZhgzVnEbrLFWZXqu4NsFhof2c1n82JxU9jU/wC0p/b6NWxezslX0Zoj3tHcZ+a4Dh/DEWRnSoj/APjlf+rd/wDYUHS6vD7EJrG6VXgWg0wr6RVA/kCl9esRulgT/TaRlcQF4dIcALRBhQ8Vy7dACgt0gO32TeydU6OshsPD/wCYQjgx8iVtT1ClpDgoF0HNlhB3bkx1Sn6Rti5m8dEH0HBxaZEGxauyLPRl1ifZlYjZvhP567K86qlJnipxPnqudRHEJuXBAtw+AkSFAsCJfnxlOfSjFJazqYQEThrDEL3ssTDha0+FohA6M0Pa6zmj8FY85G4rs6jS2u12FxGR59fqmUHtw6SCRTeRbp0XaaUe10knaY4ZdVWn/MY78/wTK8eKz/5kUcAubSi+o4ADPcmVqpc9tI7MN2VXZVgPAdYWsd6r1ftKMYdm/Z7rhMc6p9i3Ff5J73mBOIuCDu0DGt2RO5Uy5oa8yM+aApz6PMLsHwczE2yyU09qcNvd8k1weDQHtYt6wubDs4Bmyq03G2ILHPiqQByj9EY80IMetD8OIzACw4ezCwlxjh3IY0u6IYxCsJ6IDs60b8NMmFjfS04zv7IBDDT02+4OAlCaH9pBg/8AdhT2WldamkISGDk6s5OGluGIe7pBUdpX4eMqHfxIH89lgbR0gt+8+AjLRT53KvjK2e1lRtsdxcVfE7zWVSN8HJbNMnmU1rwxpnKIlfZMDvdesbKBa3eBkjUY0TGUKPEx52qbhdpRNI2Bu1w8Kyj3YMqCpkKJA5pjHOjBkRmuzr16vaZFkxiRa/G97My5xvzX2FP4L7Gn8FYEdHEJ9Uvq2ED0hzVd3bYYw4i4A4jH6rw06g64Vt0qjPKfos2YCcIveV93ins5yiCdlrM5Wx9oZZTk7uKDWnYxNxGfDCqNpEYQRhdOZj9UGMDhUiHbr/kUaVZvaUwLt32/JB7PSUKjcX8w4jmu2ogVDGF7csQ4deCeWux18Mxkao49Quzef70wRTP+4OB5pk2AN5+a0uiILG2J4Hcf3xQsL5SvSumbgN3pjKLQXkzxVIaVUBY3/Lack5tN4geGTOH9EXbdM++3eqzajc2SXM3Ry3rYcH0j7eX7KcwuOA7uCfTmQeJsqly1xtA3qlju0nCSLhUgHHA22f2l02tQeKb8iJt5oNqTTq3OJjuaDzhqES3FPNNu4tVplHEVEyfV4GbdThwWCl6fST/2sUNe2tpO9+bW9OfNXUccoThWr06TWWe6ziOQ5ovl1OhMNLz80W6JQNVwze/Zpt/Nen9NXz8OyEKdINFTdbw81AqOftXPFy8buJjNONekB907RXosNLoZJ8gg+ppFRp4YQtzv5mH80B2bWnqUTUqy3gNiV6N9Jh+JCjtWx/0kY0qr/wBsfgvtPNxP5IYX0fMOKh2ksbO5lMoD+McW/wDTQjSKbhvmmQhiqhv8m5fbPeeOHJeM9rljbk5TQqtLOD4H0RI2BwwyPio0lue9A4Q9sTlcJxa1mB3Df+RQxNxYfa3rZMgrC62/VIJBGSbUcRXYLHjCxOo1WsyxYZXo6rHeep1OJoUBePaeqbKvhqVJ6xmfwVk9w3BCm4DFhgOIuEH0azm8WP2hO/mqhq045svKdUp3jdKeKQxMdIa6coTqjdiQ0MAOarl2O75eOSpObLnA4ccbualkt3sg3YfyVQPaMH2hHuHiOXJMqaO6aD9j3sDvdPJdphEbxvY73p/FRUGZseKxR/eB4o9vn1VF7owaSzA/6fUKsdgB78P5p1LE6128xyRe2MI4WX5JtXQ3OgT2YtM8Cv4bTGdnpW7d8Ftv28UsdG7em1oc3FA2Nyx1A5t/E0W+CYPDSLYa5okKMq7fose0Cc2bieaZVoul1nYVUH/dI8Sl7S7RwfCfFSKfUouxscDcJ+F2EZIAiDzV1MLhqotG9ytqDTv1ybAI4ajaNL/cdv6LBogLaW9xzcjLjHDjqqPr7OCNl2ZKD4eWtEB3hYPNdrpFQfwguMFsaxPpmho2HwDxOHMprGsFO2Q9lG+IhF9RzQT4nH6dE6Ij3nbIUOe6qDaGhNL6TGAZYrx+Cm7zw8IChpaz+Vqu8q5v6qD3Nh7gOqioA9vDJNNMdk4FOeOzfSd4sPslMdDqdWM4sViayH76f5KxJbu5ctcIjR8D2eIsdmhU0jQXPb7zYfCP8K57GndiJt5qqGCXOs0n2eaiq92WFpI8I4IDRxjPE5BAdv7YkOtvX/qafxVVp0inhMObf4oRXYsQMNw2eL3VRlCq6RbDaMKwC4xt3+BPpY5GK4JjFCdSaWOxDwNyapOaN804HI+Nk+IcRwcE2pSq9m3OXRBbxPI7+a7GMW9k7/u9eCw3EZymtYMLwZ2VTqMdbIxkpY/C4DcnVq7AcVO7G7+ail6d+UjwhYnOaKbWkEEZ8kNN0GcQ5XTaOmObj9moE+mNqCDiA8SZNm8IRE4RHiI2SjgbhpCZMSR+ia0tv4rZeSpRyD532R7Zs8CBdYmFrhkTFo4FCpRBNF8iN4XocLHDdGSdUggzDwcuoQnPuNtkiSu05SYTAfEXSU9ozbmhTcCXFs2WPSzs7qQXa1cLaTbNA38leI4DLV2z2Bzx7+7yR0zTmYmTIaRDep5LsKbqlUWinPi//wAhN/iYqPa2cLfCwbmt5nioqPGN1yeaeadShTpMzcTi/RRTD6gHh9kHiVjr1LbmjcuHXaf+icKd39Z+al59ffXbXsOLeiDKzQ9nLcgaboqbpsVtXDgodv1yETTeQ4rtTBdUtluUP0drXYpdu8lLW4QuHNHBVMl03E+a8YHRoCa7GMTRE4QsBLRO8MCGM3cMMeSb2mFlSqPdyaqmGxa8F1s7gKs2WeP3I1Za8QwuaNzsl2WJzWn7N3tDl1Ce8ADTGeIbqg4hYHQ3cQ4J9B5loEPHAxuWKsMQ3YtkSgO2qCsYdjY20DILGKTBibtEDNVBeXwOUIQ9oYAZBFinVtDFj46e9q7CscVUbwhMBuK3T9yhiOx8oQwwBfNEPHopvvwpvu+y5XgVWxiduT7gOHs5ErSKcYXxOVlXEAAwAeNk9jodTEQ0oNJvCcQ1/Q62mM3/AAsnN9kC8b1h9lr3fVOMRhcW2VfBGJzpxHIBOq/a6TUOzO4bk51Z2N+Vt/IcuaxOjhYWGpukV6j3PcJYxov1TdJ0trzSxSylx5lDRdCc13vPHgaOAVTOwxVKhzctmcb3bhO115C3xR7Z7aOjj2Zu9NpUWefJS50O3xuU+9lxXZ0Ts8R/isVix+bVhtnOv8FdS04eCk5lGUMLABx/VDaklfaty4FQ0Fx5BYyDmAAgHWDBJ6Jzg4cuiLaxDWuBgjjjlVXy2HOlZq6trce1qDn7qafs9Kp+f7BWL+Ha58bU2UMEQ434BMcHYKftkJjKTcOjmN27nzRoxt5zuhQ32rlP5qg9lrTBX8Q4T2YEvb4hyKwPhwKcapljTLU0Uxha5NDsQw+F05deIUbEv9mdg9DuK2XbAz4j+ZM7QYwPCJuxdowziti4qIEHG6++ybtBtU5g5La3/NDfG4lWyzM5qVo88yUHOjbdKNWp7Ty6OK0moXYaReThHFNoUxBqbM8t67Oh/wB2r0bSead4ndm3bnws4lx/BOr1tnRKe1jqDxcP+FWLQdH0Rt3n2qnL9Fh0NnbVXDbqZMbyXZOca9TPC3wBOfUqjFEAMsGjki5vg4++vRDHVeNt3BYiaeLPbyHkoBJ4uOZ/xcOMTv4KNcKyCks8QssNOoILRJUux4t+G7XL0UX4hbMZRaAj2jqhfv8A+VLdpwhob53XZUSXEm95KGFuHbm+Up7ZyIssoUNzKtDjuAXRQBmnYROHxIO8QIgjkqb6dR2CkJO6R+9ydWberENaMnBPHje8+kvksBl/sieC23TUgTyTqvvWBnxQqjy9gOHDe8XQbjnCTEMTQGOc3LbNkyQMO8cQmuozdu9PoaSMIYYkHZJTmvy9l2ojNpzByKxCoW1dwJy896fTOw4/es7oUGE4mmXBOZxEStubFsHjaFAMDgbhe0Bxz/VSYvwMp+Ikh1sQzCYWGbxI5hNoUTLt53BUmC9SMTieac2TIedncE4tzjD5anuya3eVUJ2KI9tpuQOCbQALdHB2aDPbKxVQ1+kgz2YOxR5k8VTfWbNLNrDl1J9oqKz8vCwWHwXakG/ktt2Gly3oOi/sN39SjhIaxvtDIdOJUCzOHHr/AI3mO9xcT4uCddzbWsptjG/xNctlraXRDtMQHILBSoy/3okoOrlzWl4jieAVU0yQC7MI5Ep7jDAbwtsx5qG7S2jtcOCLQzG/kmPO93hG8IhtPYGbGjPqtw5Kq9rhTc47PBY4dieTdpGfRN7JoFMuiZ8f6oQPIK5hv2jnAo7TRTyAKw4yGk8E2KhhriRsJo9Lia7fCJgxaACLKkBcOGTigW+F25tk2mTi5kiUIm33s00hr/wCEX5os0luOl8wqTZc+mfC8bk22NhMWV2uezMtbmgWnFTPtajhs4e0mAGc3Hcmj0wcLiIKAZBqtsSGQmztPNyUW851Nzj2kyu5pGjNqYWUQIxgCSSjRB7R7zctv8EQHAVCbD2mjK53dEKDcIZTdM73FNa0ucesfRAm7gY5D/j6q/wXZUziPtP3DooJIaf+6p+i4AZDh/j8o7gByCIm4MrihOC3EImFGEEc0X03wZgMCYTDi2dmPCVL3Q3cFARdZrRm5yDaIPN53oFXmOSwFrCACB571tgtJGzB+ahkRzWJ+G3kqQDgzCwlzvdm5QZQEkCHNU1CHOdsge7/ADc00U5FJrZNvFwQpMls2PGU4OFrCQh1TncGzdB/tHK2SD62Fo8R3KWRiwporAtHMI/wzhRcPFTLJlf3pjKfuva36pocQbzyTqdNsUhvQYC0A5EoNoPwt3si5Wy1xtfCN3RD+GqYarmiQ4Wf0QGHs6jgPRubYq4cW9PDy1PpicsJIQHgYGluHfCeKWw11SJG/cjgaGMaMDdQC7auxpLjgYwuiPvFClo3OXu380KOjtDtKqNlzju68AhSouu65qm/msPhe4eHMgc0MBmo/KT81LG52Z0Rp0zI9orDEnhx5n8licZP+hH3u5a2oRZDfPBAMBxjcE3C6TF+Sui5zw1oQaH4sOQaLBYVcrtHDYaYjinPf4ps0KwUpvuyDKPZsmo8yG4eajRxOk1Ddx9jkgy73kkvMbl4rnawAX6IVQ5tOjAddtxvyF0e0GzEEEX+CjenjEBO87kKTYGHafyTWPpYqZALWub81hBIdgaS3gE/snA0haAfwU2c8zAiy+zGA+JhE35KW0y05QU5tRuB2LJS67RuTXksx4rb7Iup2LReU1lQNbhux2H6rFVIfwMW8isNTapx5j9Ff7M3a78F2js4xFYKeQZtEfNCXSGCQOMnVCxWws2jKpVtMvivQoAeM8XckIh+m6Q6b+7zREvgbT6mZeeC7SphvcjmMh0CjN28ldpNiN+5n6qGbFHe7ippAQLNP4qXZ/6QNVlha4gHPuc1C+vJZQcms93rqJ5x1REjyGaaHx2bBd3NN3TvMjErNNOmZMvzcVYXAXavqN0ShIOLKeXNdnQfiI9hou7zKE0opVNnG1xs6clFM7KAxNiDPROFIAlx8Q3pzC5lxth7skaoIc3CGWKIDBiJuXFTUqOPIWCABIYbAYt6fTqlxc0jfkvSO2Q6eCqBwjCUXGzcyRmFWziAFjbb3uXNSx3WEJ2HcRkiKwa6lcGXWd+qFNznCjExF/NObSEM5Jrr4ihfPUatR0CDhVE1B/eq1qTAfs6a7Klmxgbi+8UKbdllIQ481LopsbZPosdbOq7lwTn1TgpDIcV2bNmlw4/6IIm2oHjrE5DuwiBqKk5I22jv4KSs0BLNol3NDC0u2oAjetoTVi4ByRqVC2k3CZczxE9UGgDfcmPih2M4syWCYRqaU41MjGLESOg/NeiZ/D8akyeA+a7LSmtbpDrcGV457nKW/NNZiwy0mR1W1UqEcz9VLDyVIYiH2JaDKeT4XZycvyW1lMC90Rv4oVAXTAa6DmQnv5RcqrJ9rPUXNvK5rE3EfuzuUtMhNx+BoL3I6TVxNY7ZawZu6fmg52GT4Wty8kwu9obI4anvJEC0cVQpDCakiGn4p5vVc04sZ4p9Q3q1apDeJ3SsOPO3NzkX1QAG5H8VLp2rxvjcsTstw/0Syz9RfVzRULkoGsigyecZeaZ/EOmGjZFgjT0YCG5tbuTXYWM2QWlzt85En8E9+m1cdQ7QYw5QiWQ0VJl+KcICqUalXDTdZt7A7kdFex3aMnBy4hY6XgdP6hBtZszuPHVowqf/ALcn/wAkLCePFCWeXJU3g2bn+S/NbJjoLhTfAPmqkZOGIcin4qOw54227+qqPpvBn/LdmtpuGTrgyseEhm8cOar1p9G3YaPeKDtIbjruEU6XAfkhtYn523ICHNwt3m6MLD5oVB420fmVV0lzLuaX/oEysT6NrcNLfbeUx8YiLNaN5QbWdc7T+TVicen+inop5rrqB70q2eqN+rDSY55+6JU6XVpUORMu+C7So1z5yNS0nk1CjQpYZsJsE4l4eTPTomMpu7PFYuH5lGuKbJdAPaPE9UDVq7BzNMZyclWbTaG1rt8lNvJU9KZetRtU+83j+Cx4sLXDEeXB/wCBQpV2YJF/L2vwT2OMlphaLhiey803l8YQkNv8FG/5rIYYRwiTy3IHxVd1kL4akEEDIoNc1tRmXRONGGuPz5IDDUNO4LXxmt9I+64SsNuV1Ba+f5U1rDt/cEnpK9Fnd4nJVAxwfWdepVP0Cbh2gKkmOX7Ke47zqpg8VpGCIqPbTAy5fSUzRKUbcN6NUc5wJ1R7tqM/dC51do3yG4arf6GfgFU4hAORjd6mynXh0fExs7TmWnzRBqgvFyaYx/PJegptuIx17z04oO0gvc4XGP2f6VgptAa10dbXQdpRimI7Onki+o8E/dyXZjC2m32WoucZcd+qcwbEcU1lMAkEln3+LSu3okmpQ22znG8FGo7N1ymt2dhpbEbkzwzKzEcYXs9FiqnY6XQ8NJu7jCIaRO+6dUthGRQDwMwce4KpiIdozvZPVTOIxZwE4eqDA75Ri6INODBuBkok7MiD7Tfgi2ixm1Y2+ac1m4ls8Gp5bI/NMq4tpwcY4bvxVphHJMcfDSBqHyXbVHOLKAdUPU7I/FaMaw9NVf2j/uwLBGJIhCn7Uyev5BOdu3Ln/ojQclmfzTYu85BGBecEn5ag7j6mVFr8dyBr1CKQ/wAmmbuW0xujaNubEnyCwjCKr7E5v/TyRNQw4tOe8rtqt9k3/wDkqpeRZpyRdswLwjl5dw0faN2fzcPNU8GFzawu3dPBaSyntU3eA+amTb8imGSsDW4t2e/gtq9R15bmUDG723E2RGKJzshL32ygwjjMVMQBlMqieDYO9YsnyiQSG3vP0QDhDvcJgH8igXNnj91DDlz3oR4i7JNY4/eeVTpjxPMgHmm0h7LA0qZ1PggY2GnwsmuN2tOIzfEd3wTYwk4IwnmqtQ7LNyqvMz4W+aj/AEXkgNyJqkU6dFuI8gqhdSwtc0DpYGUDvaYKjhfVdHvQi1zMU8M1hoUww73Ey5S/acTMyjpB8NnC6ZSAj2to7lVa2MGICcSrutEAfNPYcOLf3g+jHaufkNz/ANfqsVNkCBiG6VozN92n8PqhItvWhuES+pil3Egouw7UecLdPyXlqcch2sgzndQKRFSMUByA379WfnwWFxkC2ea9FDHn2VQxtMCeinIE/JUw7JrHVePRVDM31OPBU6dMyXBvxKFFrbAHzVYgSJDYCdaw8J4ocAp/0TmgE8N4XPBaWxoAY1uM75tYfiqjjJwuiP6QqlKDcZ/MIHUeaJ56hqwlX7mDjaeCpUGAl7hBAdk1PIMuq+Ik3HIIeGSS7mjhJHTuTq5qXT2Zs4BObSyk24AFBsw7NhnfuVSoyQ4MJLeEhaOKL3Yz4MN8rKPNZuG6d+qEzFudv3Iv3u7tlWYSDRaQMJ+a7KCQ7Y/lG9f2g8eIjsWfjqi91UAjbICpGci0oxuWI+26/mm0mXLMDE5u5tv9EG+UJzJVsynUmj7S+LkERTb6Ysk87I4s3y6EHNyLRhJ3XTk08VAuVR0S3a1T2lTVGo6ratynBtvviHshPrSWDjw5KrGEtyHId/rrpNe2H1tGeXGd5lbQAJ4LAHnZm33d6ot92fLaQt3IcwK2Xdc+Mk5zruuVU0zGwdns33x+qdb0tZ2Jx+7/AM6h2f2bGhjOg1OwZU9HDvObpoyc6m2I5oX9CNn9/BGvuxeDK91TcOEHr/ogcfJNlbV25LtMiX4YGTWNvH01RuzCqHDLqTpH8u9X/YRpTha3axQu1HgpCATvdvKfV9nJvT1L3vIYAQDz5eaNGkI3E8UTAE8NR1nuGwNt60fSp+y2MMZyY/FNbYf5XnuVPF9rGfEfmE1nvGFT8Ph3ZLy9S1sWG2fJUh7YGMgb/wBkhPoZh0YJ4703kIGslVQZjs8Mclo4JOyza8kWgS0X6jcq5mXtsRzT28Nr/QspWXkE0LCPNU8AJ4WusgMIw+eZ/fLVbxDJHEdl4ghBzch8UMY9JU2isNZxays7smhuZVZgd6KlMuiei/hAGu0qoJrOzw8h/g6eHxuj4n9E9trjesNZsdo0iTutNlpBqD0hAgcDN/xVLZaC6oLZb09tthxHlmFumPU1PvltMdECMi638rf1TGyLAuP0UcNYyujG5VgTcnZKDRHpDPQKr/tnDELC/jhKIO7/AEEN3m5X4pxb0CdJBwjE5aTWbeo0Q0cyjTG7567ZEFBz47M7Uc9/4K5gLSNJYwuZQpllFo3TYJ7pD+zO19+pw6BOe8y5xkn/AATaYzcYQuA2kHVHX8vy1UnhtqbiD5tCr2wiXRhHJaPvPaD6qqYs9gOSy9Q5x3CVQY3xxPmU6DLafo24hwTqQtTEDCOMfqp1i2QW1kUQct4TX1TGAYWypA2SIubI1aZmDBKmc7/6BzU5koj2nBNxy3EMRd7rN5VRgAYJEjhwanPyDvCOPMp3ONbozK5J+c/Zjzz+S9KAKjzjPLgg2j9gzwxvPHvx6g9yvVHsM+Zsn0xIabv5Mb+wgQqpj2t/km1gS1zmuqQebo+i0affCY0eFrMLj943/BDaEdFnbvtp++4NT3tEhghv837KaM4t1KNVxnG4me454TXfFSbjmncYlejPpci3c9drR8OT2HcmVGfZEf4/koUk8oQtiHu8VVpgyRGIg8OHn9EO1ZIxRB+ZQa0Q3KEBy1xy1UKlYyyjcDi5fw1H2vGeHLvD1IXXuFxma1S3Rv6p9WNqsQzy1aUCMOy7CQc7rsSDhoUL+TZTXTHA8wqjngisXds+Radw+CaWk9fUU72Y0uKZWtgLS7zlV63s02kN5nKVTotM9m0MnnmUQLay2dlETCvmrKDYOvbiicQbVAvwcsPsxBH4rE3wfT/HQp+Cwt81Vc3xgRPuyn6Rg9GxuMddy2jLzc6nO1lSnOHj9nqnl7pc65nj/gwqOjj/AOlo35uP/K0TR+Fz5DV//b/+S/tar90tHxhU6bM3nD+aD6BDKoZguLEcwqdPc1ob6jSnDP7P9/FAbhZaPRl+Fz74nkw1tyqlV+bsTkwnNzcR1jmiChi1Q5S3MZIVKVuXArZG3vZucg5hlh/cf4wcdUDM5IgNl5yJ+qp6JQ+xpy+o/id5Wj0TvPbvHADwj6fD1FTDONm01VIF7VBHz9eO5Te8bLbrtKp26lX6XP4J1yAxoEjcTq0enEzpW/pK0qmAYc8D4FD+EILvCCeELK8dy5E8EH+ycibIy5mLlKDi0t5aqE5vcXnVprmjF2FHswOZzWFPIyyHRFdLJrWOwljZmfNF7BBZ9oJ+ih3hKtnu5qMjqsuYRIEv9oe8pzad/wDirqVfIBYWCalS3QKo0HFiYC985N4JtJzNp8Vap4e61aTV+92Y8v1745ocCsyG9q6mQOH7KHqhgpFrT7T7Bf36ualX/bppxos7Nm5syh3Lqs90RSHz/coO91knq5VqkeN51UpkuHpAziYgLET43kxz/ZQdVILi5zXbzvVkZNxuTrNa4ZNeblO8V+Jj4ITVMnIMzci9wBkT2Ydl1QqVsvZad2qo7kgNzKYRcchdVKxnHpDsXx/RVnb3bOrzRnIAvKEw6xCbVht6pZMThRa9uF4z4IH/ACz/AOJUOtzRxeIKMnK9l+KLKph248eqLXiFbuz/AIMncpKEpzKTJrVMzwHBaKKsuYXdvU4v/Zsjidie44nHiVhYIGffYeBXRaQ5tzhZV/8AxP4Jo59+AprehZ97P4JzWYMbRMm7vyCwUiaNPKAZJ80Z1zrBO5VBnjeGee9aXX52nkFTbkcKN2zwnNGu99CpNMhga8Knj0Z1Ro3AyFTMVRUByeMMG/5o4X0za57UIYWVdr/bcL80Q5xJ4uIsiS14aOLrOWxTHAy8HCr03MAOLHOa3OPugiUbSPgowGzhN1VeGmDEnhyTmNO3VIpjzWjaOPCL+QTHOs18uF9XmtJdwZHzVKDBOR6rRGHNznOcOod+5T2uwmoPs3H2vu/veouOIK4jhwUHPVhf8V+Ors9I/pfwX04HVYTqCjd/ghG9NpNyGaw/FNfUGxOXFekvvJ4N4earOI2KRHxGX1J+HcnuTqHAs/FUnu3tqUj5tt9EyDmJ7sASdwCadLcNHYcgfEfJTTZf3zcrDQd/DD2qj+COi6CT2Z+0qnOofUOJBOVgmveBbFWPmqFM51iPmdXYF0lwmq7LY4eaqlwj0QFHnfNSx79lpNiVROlaZAJIf7Tst6DKIc5nHstn4rG6mzF4sQbzRe1pbnLbEFA1C119mKeVuqG3EZkt8RTSGMeM4bYjyRgbcb25LswPR39lU2VHF0DHE5bkSPacT81o1P2aLTVd13LSXx9mOzC0ZhsOyt8U5FO5lGtPhqNb8itGaCR2bXbTd25HtTMtw2t59V2ekYsXsvG/n1WF0cWubk4LEzx72j6qHKyjNvBANOE80Q4XGq62VlYq/iTgYTf8ByGaxfBF3tFbU8XJsyGgYsvCPzVxtHP1RHJUXzujqnn3XNcsQESbIMY0ucdwU6bXp6N903f8AnOLaxrPHosZgnnHBdtpz/4ahnfxHyX/AOmUm0aO/SqwueidVmXHPSKxz6fou2fNChuLht1OgWG7KO5k/X1J5gwPknuLJc4NYB+/JUKYGzTaXfgNTmwHVKjsVQ7iNzU6tVqsL+E3Vap2NSoGtzaYA6ql2fZ0ZqvHoxLhbinubic8jxvMpjCBhNiL5oMdamJud6Lt1M5AeIphFEuygQppjHUOQDbIl2AtucMb1geyP5RZaRU4CBPRU/5VWrDxPu49EbnHWeSfj+ipYgdimGSeSKe7mGoKXh0OrtGSqXcez9GZ4ySfw1YKg5g8Cho2nC7bgi0/eH5IOaSabvBUH7zXAqCrKRkiypdhQcPCVcSFsny4arLyQR9dPwQaPPmVfILluQ0qvTxt/wAmnF3u3Kazg57nY3Rvdr6HUe/wwO/FPaJLnODQB1QOn1Ozj/KZd5/Jfw39m0exadzPE7q5dtUqMNQf5r/Aw8veKx0GHtHeLStIG15Bdtpb8Ub6p3qKFIU6P+5WGfRv5oNFOpp2n57RJjrwC7f+1NJpUP5inAHEAYnjrHeayLmGhaPHh7WfIf8AAVd54hg1DBs1GlYKbSKmLFULruw2Cq0qcUyQW3tJhUprU7VS/Dcm7eiaH2vYotNUMgEzByRdSq0+zGWKRBW1WptfMtwlEUWjHbFtoYzusXG6xirBjISo7V5acxg/FOBq4cZOaw0XYnCxtZP2ttwwrs8+zaPwVa8bIzR6LB96UwJjTN8bpnoPxWkU8RdFQmTv1w6QRdrhm0qpomnQ9rzLZyKkXoOOyfwUZc1ez/rqlnwUEW90rFTvGvpqb6+2ZU/BYG570X1fsadzzRrR6BmzS673awjqPfqtftB24Ki2icBL2TGdyjU0wbbhZvDmhRpNAnjm5N7TBh9kRclYNFZf/cd4W/mu1qudXr+/U3dBuW3VFNvK7iv7uwaFScb1ap23I19I00mrFsQ8XRT6mpU3saSOpt+KpEtgMol3x/4TCc3bR89WHSGdjUf7TePvjlxCqGQamU+y8fuFXwwXBhO1ustDbjcMTOuOyploBEXtZYRWe1tzxMpjHAvIsOaAZoxgZuO7oh6GWYrOvkjjwA8wjhqbPEFVCXHLiqDMRxEtkyt/xVCkHOOM7QJmyYB4XVR8Aq8AYcUx5o6hwTTuFP6u/RNcL4pdMRme5hf8tyNCrD2Os0H2unNCswEtjbG9qh1wtu/3lxCn5qZt7yvsv47irCFYQp4LIoWy3q1/VyuZUlF25uSdPiNymaFSG0T6d0WxH2fLeqdJlgBA1jWe/hAsm9ptPLhhniuBRFCGud46ztpxRdLqlU51H3Oq4DW73OKIcS6qb7IuvQU20o9rNyx1HF7uJ1hefeqADac7P99VpUNuSKNvggBkNQb2ZNIZ23oU6bMLFXNRzMZBb4uS0Z1N7QKLcj0hFjKhk5wnF9byyCcwFzzmvQjDOQLs1ssqBzgJ3hqh3aRxxIGzj7pAKwA+J0TkqGN1qbSZO8oOGRVR3+1Tj9/FNrhuKJaBzj9Qq0QWtOD4f8I9FA3po4BOccWyzf0lUhwYPp3S14lp3IB+KpR97Mt6/mjpGhttm5g+oXJbJhc11UNGe5YHbtx3IQOvcsVf1V8gpKAavuM+adUeAdIqw648A3LtAfQRDZ8TuJ5SVAFuGsIao7+zmuJV1awQ7KoA3eQJUVquJ49kXcposDODnbR/IIueSXG8nWdXRDuvMiwKpuAJhxfHJon6wtEo9Xu8h+Z12GLknH+GbDRv2pWENw2kHCBCgODPeeQm3dUm04ViqdpI4gXTjhBc6Sabbz1UnFgGRw7uAWJrRfeLIDKFhDyKmfaNH1C7SYp0zvGZT31fCHbIP4oudlbJaTU94laOW2c5mJ58/wDhdpO09uL/AMiNfkqmETYN+QHqMVO7P9vh0/JHSdEjPaasQyHi+71V2qR4N6BbkjiMVNx4q+vkrX9QNcLDvVvEqeORi2hAmw5dbISYE4Gsn2vaPMgIBtgLAd4In1ODQaXbu3vyY3zX97rnS6n+3StTH5rDTijTyhn5+oKHLu4d0SeguUKUHwsYeWI4j8gnvO5gHxvra405YDtQmt7Bhc+YMIBoYKl5BBxIbNNzHRYOuFUdWG1lsEpxNCq2iPe6ohzTivBDSj/BsruAzxZJjXteHG3hhHjuU6VLnPzACY6AajWuIbHhTWt/q3X6qtRxS5rMXkmtb0J6plGYaxgBRa3w03FvUTq8kVQLRPaVBn1/T1ONhw1PkeqdVpDs9IYMokOHDmE6poYwV2/aUJ+iwPFxYgppzC5KO5IVu6e607k9zsosiXXKLxaq/Zxj/Lpi0DmU7C2GUB2bfPP8O6dQ7vPXdCpX2hNmcSuztTobqbUPX1zkLMnqVUe27iXlvXwifmUTM4nG+sYh6Nw2YyCe1ru0bntfgm7BDy0v2amVk1zBSa4xdxQMPNN2Tb3KFKkMFY2H3QnFlXiDUfUgA8lgr6cx5iGtYXG/FbVU16sibfRMqOa5x3BxlOe6mxj9wOcIBriKcnEBvQJm2V057faaZPPh9VTM7JfeM7LTNI9p7iGBHsxsEAxwOodEOoX9n0w42p4zzt+vqocEzSAS0tN3tG77w/FB+AGo0WdTd4hwWCoOYV1Lcl1Vt2u3qmtHFN+idSb46sD9/veopshtMZDemtf4s3de/f1GMHHLs1gE3fPW3qZ7nTXbddMk7PjhHSntImGMB4bz9VSDMsOs04eWH72fNdoMZcGy0Tn/AMLOs6n7RaYzTWMpl7ydk7lAM6Q7xfog2Zk7Tk89r2bcmYon4JjcdVxcT7UINxOqVTGGH2QY44qkS++y1NaTJ1398QqTwP8A3B+ITtGqDC4LSW7jcW1N6o3i+a3bFFgnr/x6yaJw8W7j+Sk0nSycTTvbvH4+Sc1jsbRtNPELcJC6LF8Ue+e63mnk5yhVrZNLY+Kp0/Zb6R34fvl3ufqXmdyaDeIRaPC35epKnudNTuKLyMAYA0fvyVJhc4UKhFJjOPEptNlmtEDuNNOQQm0yHvY44oFgml+EP9ra+SxdpRxuEg40XOi9rO3b1BcxlIc8lNJrH1d7nmAoqaRTFR3s7mrAAwjPEXZok0/JrgVMEcjqpN4uVAFm1RZB6SqGlj2dlwHJU3ky51G+oanVB7WD/wCI9bhqNDhzTT7dA9mebPZP4K2e5eGLXR+CwkXFvWMjcEeELRRFnVTj+KD6jtuu4kT8h8O7AVvU0qfvORlV3zOOofWddR1CM1ToYyaZdc8lRewAUGtIpD7g3+Z7sAE9EzSDjJyHAplOo9+z4iy0/wDCxUcLaWzGKmXQtvTKx4dnSAWChQqOxHN7pJXa1g2/h6qnVrsGJwnKFEW4KYE66Dd0EpzCDD6Ajqq2iATj22cuP75J2MS6lTwA+du4zHnf1xqU42RDxxane8Mla4zCvkVPkfWOtkAE1o9oKjSOXaiAtAPBhfHM9zl3x3OTGqu/gxAHc2fUxqGvrqCDXWZgl889yrkWFNjWDucSmbLg690XthoGQjMxmgalm28uA/FEtEPjA2B8SrYjwQfD8SIwhrMBt5LR/wDpt+ndFSpcBuHCm1CYFM4j03o1qY26Z7QDjxRcz7Oq3E2E08kDqdJxbfri1+RsQiwDwb/ebuP4IAZrJPb5j1ZAX2Lmg737KZ2mk0AQMg7F9Ex50qoXMdaKXNEUnVHYJbtcj+vqx3HO3ucsH+44BO+GsN1nudUO7U99whjYkuVXtB4M5Veoc3vme5Bxf0qMpG3xA4IPrEdmzw/fKl2Zv+ZQwiBEATuTTdud9yETG7ohPuu/+JWi/wDTHeIOREKm8nEaXo389ydQJLmMuzodR1Opnwv2m+v7XDJpja5t/d9YO8L5+p7XS6nY0TlaXO6BRoNIUPvnaefNHGX1HcTdBwoviMyIU1KtBt4gun6LFjLyfawxPq/LW93AJreAVJjfYElMGqV5K3dKHeY3I073tAF05jqjWvNEYozxOupZ4CbHiO4177MYMTyTCcMQvJVpDJs2VhGb4/7dyFjc+yuzabuuRw1OcM2MLgtF/wCmFhb5qB3SwjZrCfMfp9Exp8dNppnmNyg66wF3saKjfI3+qDm5G49e9gBgXB+7uXVDmiOHeOoodpS0eoYiXU7o4aOjN6Ugo7d7QPdt9FS2nvLhxlOxmmztHbMtv+qAdiJ5+rKGpjPfcBqe873H4C2sBOHIpkDd6kKUBIG+StJNMlpqtgW45oNDI0bxunN8fgmcY7ga7PNzTl/wEaLGm5kjeV2lWYiXfe/5TfaKFU4tn5lXzznVYTsOaY6LRoz7MKB3g/8A2jj/AD+SouBEOaLq+qyY45GxT6XuG3Td6/tovSz/AJd6NPeg8Z/ii7fqA9S2pWd2NA+27f0G9NZS9DbxPu+PwCd/Cu7Ogz7XSneJ3IcEDQvTkger89dNvAFyqVPuoXnCI1k8E/8AlTD3ijrhVtL0gYjTGwDvcUWGRSnaWkOFmud2TI7riXnAfDbf+Sxvl0k9eZQZ7c4j++SlxPkg0SGjdrc7kR/4lUg0Wwj1FXtDLaeENveE9rs6bi3U7iE13AqlO4dmTxGbT69zTk4QtqJoHs3HluRHsq2/UbXQ70UKZdz3LtNNqMdW4Zx0G9YdCGC16zztNHHkEaVEu/hmH0lY51P3wTW1G4NFZ4KPvc3KKcQLbKGLeYHqR3KtRoBdhDG9UWbLu0OEX/fJRqY4ZqOKceAhN6+olF0S1gxOXaVeM2U1AMTQABwTq95LDUd+C0ankQ3tXd3AA4U/C3812n/bHFSZnn3Tffkm9B6hriPH6Nx+i0gO8Tg2p56uurY+1o26jMKnU94T6/8AiPYwdnVbHib+iLH3G4+8OKb7u4rHvGeoRu+nebRZVwMaI2RCAEuqPMdSsFV2DRh9o5viruG4ckKmkOFMEbFFvsj8TzU1C7R9E9xvieOqZRptythb7Kpud7FwOfdGqNQ7jnZ4nOOfkE7aEUDgEe8f+Fz1XyVs4lAN9pHr6iAuzyYTiMZmE57xBMQOC013+YcAb5hNo76tQU/IKo7d4R5d1r3Ocw3BJ3dFOTZtfvEBrfGNrehhy1O7NvaPiYCZ20drG1HHu1GVPC5sFYcG24NZE+F2X4fPuRMYvruT6H+W/bp+e7/AOo4fSaPemfeZwQa/JYKgvqHfZ2GLtZ2cOcou/wDVf2jG0XXZQ/VfxOk1v4l5Mz7P6o0NCMv31OHRU67nkh1MfFS247oQ7xPBEtaXPsz+rP8AFFmLEQ6/XefjrMK2ULDwlP537sa5iV2lTxm4RadzcfwCGxFPsm1Segj6qlj/AMq/xumzmb90ztNHFDv7eTEakT7jPzRBFqb8Tj7z/wBO/o72n7SLHKQVUwiBi1yM1RqtMXgH3Z/VAnxCxHP14qU2h1SncWz5KaRmjUHaM6Js+JtvLcg4KFbvdoarjpbxfALt5Dh1Xbad/dP7OblSbbH+aFDRW9lo0RA3oPf9g3xc+SNLRxBMMtbCN/yQa3dYd1vxQPdKdGeScGmW0nFxk78ly3a8Pnqj4p1unqAD4d6tmRi6BOrRtVNnyRZ/7jaWfAyVSteu5zvLvRKaHD4KW2Vu4bbQIVbshDTYudvnguxE42zUdbOFL86j5+Pef4g8U2kOG65VNlYWY2Ms5TjgDcIAI+XcqaOTE+H99VT0sTBEVG/irevL6f2ZM5+F35HUW6pG+/dC/j9P+z/y6fvlYqp2fZaMgsAtFy7gOKotZTcS6zKe93NDG0DD4mg2aeHX6d75Id0phPhBxHyVQ/5tcwem/ucsk8fBFxRUdydT6r8x4eaNSoNkf+XJaQ90ds9suP4Ki37spxZI23kdSg3/AGaWH4992yMLe+KWGHeIrSjHsho6lwVEfeJ+Xep/fY5vwv8Amg/28455x9E5/wDubcdb9xtQbingiWu2/jmjo78s6fTh69zHiWusQnBxkPu13EIBHiunea0kkNyCAAOLJOpVX08bRjrcuHkjpLn4WxatvjhTH4rswwMj2Ru/XudFKYgNQ7jKYdFr+at4RfuAblI3hYeF9U8brmr9wN4BB/8Al0rM5u3lOZve4N+acGCSG2Cp0hBJwuOLiq2e4E8T3sRX82/vuBvhE55IUqjSO0rMOM2GzzTP6u8x8kYXi43A2/FUpEFr5f8AFRTJdh2Z4jcr64VJjrNaYnkVNP7Vu0woO35OHA+vcy2MXYeah1t3RA+00qRk5DvfxlSO2f8AYMP/AMlXawU3Oqw5zqg+aZUqkudm0kf+X5BQ3dqnUSmj1FV7bgGG9AnDjqKgI8BZA8EeYXVSeKFrrn3GtHiN/jkmU25NC0OnEzVn4anuY3EWiIlRmcye8FnI75HFaJRqNDmTUeQRyhbANSg0uGH2m9OKD6bg5p3ju9i0wXclRqbJBZEfVONMQybDu4hkbFU69HbpkbVMbv5fyQq0yDo9XOOPH190K7Bs1M/5lCjeVdFvHuE1jhoUxjqO5Jjg27jgYwbhuCqOfHZM+0d75G7oE3B9vV+za7d16JrATYZlQDJGajUAug1OOsanuB9I7ZZ1TeLrok6uqxHqm8zKw75TOGSxuW1kESc+4AqTntnG4HPcEXvyCoAZMZj1aRUmd3z747PMJuFYT5K/eqVKj8IbTi/VE0aTnbTvFsoVKAo6PU9otcTPURdDt9GLgfbonEPhn3HPaCcUz0ATcgZMdM9VQlsw3PgjOY1g7l2bj6E58jxRLW42vzZMTzHNdmXS5nzHr30qmR+SLXjaaYIWMZH6rFxurdUTrpaG2O1Ppa3XcFTpsB/i6vxYDu6lMoHB2GjDbcMnO4eSdpL52rUwfZb+uaAJzsE+J2nYj3Dz1YUdQWN5hoWjsds08BJcpYIZuB1wE6OgQ56iTuK+TRxQm7+CLR8UbzA1jhPyVC0EsNX45IM3EElaS/c0CmNRDSTidik9+Raya6c9Wd+9Uc6zpAa4bk5rr3O1x1DW5wEkDJEbM9ngH8xWEZNGFXTpzKhRqITSfDkUKDvsRdjuCGk6P423c33gm1GGWu9e7Sabfs7H7ywTAUR07j9J0j/0+jjEeZ3BVP7Q0loON+ww+278gsLr6bUzvdk/iVS0c/1805wd6PwtHE8UJ9nJDUSjy7h1mqTPZ5N4v3JmiOdOkikKlNxOfEKMj3M75lSomyIyaE211ExxWBlm7yuHLXTpN9ogKvB2GYWAcFpLnWa1rWD4rG6zqji8+pqFDko3cECxDjv7jQclVw+IVJTief1R7jGxOJ0HogBuieqCsnObYCIB1HXKFCsRib9mXe190prb9mfCT9DzRwGWVcmkoOYZad+q/q+ypnaOZ4BPxDYDclhiCp37u5o1KoYY8dq9rTtVDwX8XVgViIoUt1McV275Lae1PFy/g6MyWzUqD2B+akfZU/R0+Zy1dVU5PLEB6jR6fsRI6rRnUdlzaTDI4rtqLS0uG2Pva8O9O+CjJSNxWGc7omb7zwUbl8yidVuioCDDXSU+oY2nuKaXWNaqHX6+qLHI6xuPcY3iYWkMNpioOid+96A7kXhrPr/wo3l5J+g1O9kATrt7VwraoK5b12GmHEx/tDOeK7ImT4qb27+YQrtaY/zG7x0WIGQd49WXIl32jruQpB0Bu0/8EXk6gN6srp2kNmu8xgYRha3rxTqlV2J5KximZLj/AFncsDXemqGalX9/JUaOjx2p2aY4c1o9BvtW+AkrDJxNui4mGASVPFc+8zC2bweSpVo8JITJbhPZstP3dYlOdvKkrF7O4cVHHNNfdAnIXU/uUB8eZ1iYgXMqppzjtMLsPwTWtzcA0ea0WnwdbyHqgiDx78zEZKlUuP7sARx3p/VDuaVXO4n5WTn8TKhoJKqN96NVhncLEMsOH80QDMK+oOiRvHEJzc6R4oMquxNHhKwvMY/rxRP/ANO7P7h/LXHqBU/y2eHmeKfUO5OvOIysKyui72nK+unSZ4nmAhb0dBk/BHS9JcGUrw3knaRU8T27I9xm74p9V3hoM+tz8lp+kVXktnF+Kp9q7DUqjtMLzkOE/msVN+Hdh9n99EAczkO9TdTMHHtdJuqvIg/NEfcZ/wDEaoRPBTxstrwo7k6YhuSaDlM6ugsh0V9UTYmV9+o3EfNaHS4HF8AmfdYT8fVYViv19Q8PEPp08BX9SOuU2kbVKtvxOqRmgIuoRrDcAOq34CFO/FHd4LEyMPI+Ars9ILcfhncUKdzRPhPu8vU9i3M+LkEAMghRblT+qLju+qLtwUxZc0Y1v0l3hptwgn5r+CoQ2hivU4gb0yhlo7GY6n8u5vmm9qPSVTjqcuAWn0WwcFOXEe8Sj/FODG1KhcW73gcE6viguyjLog1vkCsNUlrhtbbol3VN8cccwfNeGRyVkKYBJzPJHgq5pGHBjiE8kTipE33qrtYoMTHDVKHNCTYK3gamjcoPVSgMk69gFz102cYCpUmxGJlNRuZS+pWkG2zDfVMeLcUOuu/d0j/3GMf+B+ib5qdeEEgvIaCE4AjBo7N/HUJ3iU4ssJVN05z5IANBwTPNGjMj2E4cO7xCxUc8o4rtqGyR46U/REVx2lIDatJZ+iAxiox32bxv5d8vdkFLzL3XTqntZN6oufck3Ue0UGjfuQA7tDRmPds05ffe66DnyO0GN54UxkPMrs3xDSK1b+f2W+ScwAurlluAX9ouuaj8DepJTNHYdig0M89+q+75IkwZ35qaFYsHA3agNMYab/ebkqvYVw1rcnOsVQoueHDtoMHPqfNaW9rp4cohaS2g8H0GOy0hpzpSeoTqjvE4ydUq+QRKhgTZu5czqEZlfvNYRroNOXaBaLGTqgIWku3jC1VXW2qjvVYU0+oFMnZLSPxQQ1tfU8LJf+X1T6j7vqHEmtBiSnMp3a208UWjIAuKDSMWGc18d6fgEyZQqkeE4XDkj3IyHBYmbljOzVHtDegSTTqjw1G/ijcU3HOPA48eR5oB+zWHib+PRX7sexS+Z1Ds/sxZnPmhwTnFc0OKjfrosPhmT0F05z/C9xe+NwRfUG2TZkWLtw6NTalV0ueDXqE/JVax9o/JaT22dnMHEhPJO0651cCiuC2rLHQeWuG9tkQ/I5rSyNxI+irUHm/Zuw2+K0hr5h9Ittx1hOPwQG9dPqieS6ai/c2wU9AnO8lCYOJVN+YaT9ForYttFV3nfVKYYjFf1XRRuOoqe6CRK7J9RvaNyk+Idyo+4J9HT6Zk/TVW0l7QTTbsT7yqOOaNbN5JY1vIj/hXzkLzLUxo+zxz1Tt7X7JCI4K+u25YsqnEb1isSiFs2KAu1zbtgxHRAaYZb/ut+hQcwhzTv1hrPG6wWcNGZKbTZLTUyabfFON+DTy3qTvUcPqie7pek7yOxZ1OfyX8TpJaCdqDnh3fNGo/LJreAVWgww2pGLuXV8tWzf7pVs/dKgjycuar0S4doX+H4Kg5xgEwnAXvrny1SgE5BFBnK6agN5RTXcDKhsy/GCR/SqJduoSUHu3guuqX8o9U6OGoc9RHea6j9qL4Dk/iPNMdRaW08wGEtg+Sbh0nSQBuxzPxVQVNKrmgz7W//iICcRjwzbG6TqbTB3lxQAzPBUXe2Sc99/38U/e7dCqk3PiX8kOCrt3Epj2wbbXVOw5i/Ua7as4Kh4upYr5Kylruzdclvsv/ACKa3wVT7LjhROCRxa4FGo6cfhY2NyNaq9jgLhrTICqPJ9JUt0C5JpPjdePosPBNbv3oQIjuaFoLc4x1PP8AIJzqdqQ2WD7o78HJZ35LmF6QTzXvhX7sKUB7t9UofeuifdUi6PABAb0BOvSKv+2zCPiVXicTKDWpwHs0/wAEzoPVQeELoiN4y1de819Mw5pkQjpXZ0306n2jWn2uPJN7FtBjngxiq3bzyTWBvZNGTQ6/MnnqCn+kLGTtGY+CMyWjJUBaXDJPIybDf38EY2h+Cc45kyuq2dZ5It9tt/JWz4LbE9VNN1/cKIHi4Fe6VtC/FZlNZVa0symLwj2Rq07dZ+KxURDcpLQJ+CNpLk0O+zm8cFWr5CbLEUT3KNLcXX6KtpX+bpZIYPdZx9TKgja4ripBy7pKMqkxE8TqMZAIxwgJ4HRXTnuHNOK89ekwJl4b+/iqrMw6sxvkFV9W6EY6qm74o8E3fBR721MLBJw8FJMnUE1u7NQz2WbuaYalqcz8Ea0QMSqx7WA641zqD22IWWEOGU+Ers64LanNWM8FD7894W1tt+aOG/1VrhWz4K66KPaKdve6zUKQ8Lfqo7pfXnDgcNlY3W3ADcOHevl3LIMNuK2I7uFdUXnqhwjVgZvUuJKLtya3dksPKV5A65VV/vVmhMj36lT8F1e0fP1fknclHC6Kf01n1F8slHBF7fFUdAwjp+ikC/g/P8F2fAX6o4vZb8AjrnvN2ttngJ+hXahvZvH2oH1Tm1BdvtgblDgHBSw/moN+a2tocUSpiWrEc3WaFnijVKj1ka4V/j3eindkqQ5JzR/KrrlxQAybdQN9kQo4KoTmnAb2xrF3Z5blPaO7IVBDJtMKq/gI+ap/9Rvq2lGOhXJyd19XEJmLwYr9FpukluVhylUnvIsO0y3ZD8Vif4KcuRccynQ4CREce7G9de5ibEj2SoksB38E2KeJzLPb9xeMmm67XqHfFcRxW1eN6FvNQ0KfDqz/AMDO7vdbpjea5NRPMr7v1VvJcTxQLkTvKKa1Sjq0ds5ucemSYf8A3Xn/AMUXO3usqOX2jfVgq3tDJcwngcdVxnf1GU2QKqvdAc8COOaZS9qq7HnuyT3C2PYb0y/NRvqn5D1HXuyBlmm4nGW5FNpB9MNdkPdPBPbIkfuVib4fpquvyWEnJWUH/AQoZamzXKCDt5TG+ZRO5qcfvLayz1dEeAQavomBNHJDWOSh/BzhH8gVAfdlaP8A9UesBR4GydOaKZfd39nLU2kM3H5KjRoPOHxOBsoOVmtVGjTFkcPhZsjV1V1uPqZCkZJuK0WkIWHbMGyGjxIVKR8Qkz7R4HmvRgkKXT2allhmueqf8AQN6jXLvgoNt635QFb2lA9pbScUAjGaKLuaPJT5oHiCdR1UaYE4ngJ0W2HBUxuDQtG/6n4esjU4Dgih33/eEJpJEFVH1Nnc28KpJxAEj8PzQfulaRWP+WMI662oK2vlrhSues4hbjwQBNpkObmjjdjYTi681iZOEZn81ER0R3AoEf4ENaobktnLUWu3b00HOYCaI2lbeVkbWAR34QjHBCd91zNlyVt+ozvzWGY4qJ3InXoo+/Kpgb3QgtGj/c/D10jWe8SZncqNJt8mhaSweyAxjefFU6bc4k+f7CbTtYfXNMZvdtu78FX1zq5a+l4VgL8FByTWEQciQfEnOZJpzcb2qX7TOSnNpyP+B5u+iI36r7kTuKbG6y95xTGsu5Ac5WLidQHJDgO49xV951E/e10T7oJ+SoNEjMzq0b+Y/T1dcMHo8Vvrq2siuIXP1DyLtYJPK8I1qhGGg3F5p7mg4nQQ3fyQnqVHtOKLvU21cu96ZszvGYVy1wOTm5HVLiZ4rG1vZuzjcUA/7LeOCLmXZ/gJOp53ohOduWyjg3DNGNzU8/0hAe6EBzWfchFu5AlNneTZADKTrqP92mgYnCGt+OrRf6j8vV6VDDIYyoDxzB+SLD8eI1W9QztPBMu6LSMHo2VHThjnZVaVXZaCHO52yVWtOwGmD0Cr1Scgg85nF8h6p2vnr5a4zYcwvpqwO26fun8EX0HBrydlkolo2QbjgtmGOOQ3FEOEH1skXcrZaqgGQT3Hom8ChuA+eqeOaa1vUolUxzlAG+qdXIKVjfuyU+ziUaoWku5AJzsMzpIb8NVCReHR6sNjxUD8nLHh+wd2cxm03b+SsreomJw3TBm58YQM8Xi/JOGjPxPcSOYED8U2mPCdnyGaAYI7R0809rf8ukR+fqjr56+S5dyZ+OoEZhTI7Vo2T+HNYmifep+9zCmptU/eHiYp8TDk4eqGPZlGrcU2ccyi4/DggOK5Zp85kqXfBXGSCaEfgnOQAzQ4wi49E5ABSmjcivutTQPCBrugdzg53zWhvFi+vPxOqidwa71eiOMAupPEb5sr+Cs3sj1zafj9VfM5jgfU6Tb2JVJ7x/edFqxE5z+wpc0Cq+o6qTyCpSYDIZPzKxnKk2f6itIdy+p9UUeGvqrarqDrsg7dqstpuI8vyWOn6GrvbucvR+B3C4KOBp6d62alxgcN5XohhtHNc0G+yNTbxJhEU73t0RnNXXMoBOJ6BC1hdNaSgFbxcEAEUOqPJTwuUSjhQMzIR1RbzKpnFf8Ah3O/8l/ZrODx9NVL+R34er0Y+w/GehhVGzhdEtdwKNdoGGszteh3j49y/dov3tOXEIVKn+YHR1Veq7c3APN0lUxHHEeZVNgzdtu/BPPFwHr57kasU9eX6KMUsPBXBhSLc1BsQoIDm+7uXo6b6zPaEXap0dzq7B7viaicTT96PqtttuO7Va62z5BRSGAcs9WJ3lrLoyRd5BWune9mrphAVyj1V1O4LIgcU53BSdQUDosKIT1TceiOqmwe04BaIBvplk/1LQwPeP01Uv5Her0R7RLhWt8CqTaZtVv/AEqI2XOxs/qzHx+qvrHdEBUXOG1MtVJhPiqYnAcAq/O4+mqlzcTqj1A1DUV17+502IKdTMxwQhcNQvCLw5zT9wwp0jFij7RtlAq4mu+fkhBwuzwm9lDcLTvaWo4aE7WbMltiPMKA7tGjgjFhwGtrG/8AKaAJwoD4zmm3gFTcnihAJQxNgFWBPyRNh0RdvKPIIcdYRcczqeFh32UfeXnqpudkCv7OY62GoQ6dy0V7CHMwuMjVS/kd+Hq2VLDs6rHT5qs3A7EPs28Wngu2efSNeL8AdyKM9/FedxTi50ig0tando3wNjPeqbfa3oqmHDDDVbujudD3CuvqL65LThUsy56oJcWjdOSxCqGuGUrDTqZXgwPgvTaSGGIuiKdbF/LkUZYz4a4GowjtHoFOz5puGTGcWXDzXtfRS1o2V0CtmUAr9wndkoULyQ4ofzKOepxG4ShowMuFQknqAqLBlTpX89VH+V3q6wabAGPvEfgqGkOcSX7FsoOSFJh8UuPRolOBIJ4jUe5M3nVJy8Mp+3Zz+zcPNEZmo6R5J2Ee7bU60bo741nU31mEwCT4pyWEwL+PeFTFcSAb53/VAtqU6lM72mY6psTLsrKKjHNPMQrK68RxdNZjVKa15spDiScgvDdbm/VWEogEN6LauZ3p0b0VTajGeXfIiyYmYQm/HXXdwatGa/2nCq5VOTQI8tVDhDvVuBuXNIlUy3x9mHN6j/hMdlTNJ0fAfmtFdTzcza6yUUESPLu17bQjD1RY3J5a/wCSYGWdTaUJtjbKZxmyc45kz6keo5q6z9Qcc9F4SE1lRxLWZSnOaxxa3Mxlq9k9VcCN0CFvlBpEHVB8LVM3O5bOYyhNbhw71e+q3vam9UwcXI/BdO6dU8EDwTXTuTf5Shqq0xm9zUagF2U6Yv5KueLvwGrR/wCr6esLPaa97B/3FOvApUqj2t5Z/VU6V9hmP8/nqpkb2puHr3GxJO8KrTybUgEzldU2Hwzmi4N9pzBa0ZKm322AzzWL3Wl3eOrrqGs92/cxGw5LwT1TthqyhbwrKy9PJbyRdTbLJtiusNDEzF4gTmhPi3oA71DJ81ipEt3SsQDWwibu6LP+lA4cKlxzRMzuW8jot/wXi1MHVM5SVbM37xWZhQmz0Tce4JpA3HXXqH/cYFXN5wqtl4nfhq0a29309Zpwkw2rA6uAWilwnE7snDk7/haRWky17qUeeqn/ACp3MRrFkZnI/HgqoAw4TOE8tyqPg4sUwtGIEAvBgLSWuGElpA3wqx5YfVH1GWvgrLOeq8IHRCcuSbhlQ12e5Gc27li+fFcQdyg2W7zTxEVXZnkgBAauzpwR0yQnNZhWeUGnLmpA+CsfisgfNTBC4N1eSf0A1R3Sm4nuWyD1R+KKqfyog7p1UGXlxNQ9BK0lzLbWSe45ku+uqh5/T1bsw8ZsOafTzsyq7rcJrabodix/C6qB0BztNg25bvhqpdxkyeKa7DiLpAvx5p7qr9rEQ53FaSHmA5iEmey+V0x0+lIxkK3hc76f8+pPrs9Vgjs34yrhSpgEcFDwEMdxxCPaPIA+CE/HcsRALptT4q7LK9gFslRfobIu8ghOQVr9FwXPW5H+adU96I2k3Dv1DhCcOifG7URwEfNaeRmGNjqg52ZnVQHJx9W1tanjw5Q6HTyTqmk0jiezBtbO/eqc1dFpbDonEc/gqTKdV81Iq2tFnAlHD5K+4QNby4eLwoub0WJk/dJTqhdd1xzuqc2a6YK0unuc4QmOBMNDm/VNpj2doHr6iNZ7pU98KNyPDcpfC3gIgRi4oly9HtDggSLZxuVvgmgNh2U8VmChe5RwslTaM4UbULwn6oBvdf1Tu9KCB3FWgI810CwtTuBvqpg5SFUpsFqjQfIEpn9WqJsKf4+rsgZxiIh+0FLWikMMFrLAoFtSA0GxMSO664DGm/MqqMYIawADgXZqqyIphxA5cEGxZuXmtDMCxI+a0dx8dyZTwf5lQqHMANP+Ajv2WStmsTrv+iBW2YbwRi7ePBceq3TvlS057oRIsApcJXIXUOGo8Vidnu77uqJ4lE67dwIcUE8ISOI1dExxMCUygW+NraU8NpFvuvqD/wAtVV07g31f/8QAKRABAAICAQMEAgIDAQEAAAAAAQARITFBUWFxEIGRobHB0fAg4fEwQP/aAAgBAQABPyE4eG6KY3u3rgm1zY1YnsOe8NbpC5jpbVXy3Xt+BK4tBtZx9wblhvB1/mLmBGwNTfQad7ncRut94t6/oxuFUyuWcf7/ABKMBF74+GVDSNU32R3k/LyzDfqcfRM8wDQPMqffBOjbf7o1EkcH9KgVuq81s6P5lKm1pVOmXxa2l48sweeS8ExJM7Z8PEoGZtVRu3mAbN44lOE5VLX1Ja7qPcQZBl7tWcalaqvEslSpVu89Ja5XscRou6QA4r7lnjJFYzU5mLvLtaoXPeDRqFeyVgueMXefsrmDY0Rp8ulZjKlMLuHoyt0ABf8AkhReNg3evJuMucTN71jrgjx2BCALWsUVGVxNq3dYlr55YPeabg7yRHiZlpUG7xM4xBiVu5QwxKO0CIQMLxc4wNcVnMEMpmmlfvLGXmcRRxA6Dhj+t0Pm/wDEwBZtFqRnujX8GZEtLzPpH+ZgYUW0zBc6T27kzniLAtk+4eZWI1U8uO2/eKQ0ROuNQCmrSbXRlmVOg4Z/SbygU2chH2SEMK/7mBbXYd5F4x7Ea0wULgJ39vmXgMag0f7l4uG4WB9oH5Rb1RqK8vl4l5QqXtflt8y4nCmMKM9cKemeY7bhVwwlU8/fMvX9DdpxnNxhZkMVFYHp09olHaijA8pq3+hwfrF2jvFP9t+Wbdw0b8ROIqAueq15xFX3H8dorba5La8HMyzFaU+3aZFtHBOSsuSb767RR3XdoPIzcYOeGuyF1wPXOPd2jZ7cnDBccxbgS0wQHQdzPX4jQMxlZ1L/AB1jmpaw9RZAXtLarUMQdC4O67xHCIDjmHB+IirC2U6dMTTUZLWu0ygI8fygwDYu3EOimYjj8xV0Z7zLwrrCIswJW+YaZnNjdsC+IvTlNHaf1HN8joRYisGi+bt+4JTYuA3fB27SrQ1ZrT4hpIjwyjCnsxiKr3i2S69VY0Xk/eoOrcSVmBDJA94Zr13AmVYnPWJxAP5hnmF7xIgmyGLQ572up5hR4plrHiEtNaPcP7iKSOoPTT3juvWAY6dafPRZnpFQuw1pDQ9y8X3OkF+AR1i9qdT8sQ9YUBKvXsaO+IOmrCqgXf8Ae0sZgF0Bt/wiJYDhdy71NNIos3b2PzLBM5aglOOhKWeVUWlA9u2pm0wGtfrxENTdQaQdctm2lp5jI7x8MTj4n2P+JujvBVs0A6uSjVaitUHvN9/YYNhATh3rP4fdhY/ZHGbt7YYiSDXI7Pfe4icZhsNwOvYGpi77mI3j0Ip4v0gygVsKB7fiZE50z3llTdk6895gH7kVIWCo0dL5Y0FLCr3mHAfY93mFCDZ4gVstl7yu+pWZWe0LZsxrpMLWyWZNwPRF1MqrrIxiCZYuAVgPiBfhEw8oM7xxAB6Q3ohdQy/E1i1gG2FvEoQvri89Jyksr8oEILtDwfuVKjkGL8wQoUBRArfMDsMyt2c8Rqc098zIFqrw+ZuWBtWacRu4xPYzUDJlpF3FwkLRdLkr+JgELnWc9YhrtE5IQMCiWGjnxiI3Uswawfccv4R14Q7pb2hQgWGPiEZagTWJqFMwgTiV19MH8zTK/qP5PuWXBN/HCdD1gqyHno6T/RNmiwZpM+3Z7kxFNi9Uoa3rnjxB4jQrs8fuVBsIxAov3cvaoxX8BKt51v3wQI8kyMVz73csS7mX99ekqy2iOTNpfLXaDB6AOjr01KvGkVlm/uW3mga9FDuMeYtWd+b1c+CUTvwvbcXolpF8Ph7eIpFVXXmAZiAug/ZBFO3S1Z5e3HvMqHJKyHe2SvghoaoTPX6gDMMBxTiuuWZWC3QxTx5fiVyQKU67/B9oRvsqi/jvKpranGNbfaW3x6XNQcO9q9e8QI3QcLW4JTn6orWi+YQEzAKgBepZlxEvtOnSIXjEShLf5mxiFOph5s8TJMV7R7We80qBxANY7wXvKCLfMNd5XmFiV17TAtraeE2AGUzItq6hkP5ZrbCAOoF0PaEHUYlQK8S+WoloqKS3eW8/DUzi1Savt3jJYZXzXzXc94STmuq/R50w/eyuDwgOXfZsqWXWeF/Mase8kfBdzf6jI0m23D6mJ03pfmJrrtEzZ7pSiILY5uqavBgupU51OrDMLxfMr4hKvUzc3UHFM9e0V30nt9pSupCZ+wfX+tz3TgBdWfTUTTrTo46HVFG3ibCLw+fe4QdkK0OH7Ca1KSFeOTbtbNH1dlugDjmoyMBsct3b1Z126S+JAS+2q6sojticgXDocKG9Xn3iW2PRmBiLRnfMA71kwIKK0gWPv/RmIqR/eMw4wtaOnTxy+gdI7Ssd7A/MqMv9BgH4JMlQnzGz609rjzgxB6nUub+liIbXgA5EVyooarXJxAT1VOKdXjiEoQc7yH7lfUOZz2iGa6P5yxLTi6O6LAmWJgOHmnEyYjPO43uZrO5cIa3iLG2+WOF28agIHTpGlITjrLe0rvA7TFLq4UuHOsxuRaDuGBsZNZ1JhWX+4EKc6A8y5xsLD4Ok5HtUVHBHYUt2eZaeKC4Y+FsfiFqL9C/4h6HdFfhASl+oWLfgElfTNxmjV+EJUuzGGviVtlpI+1xEuqZT+OSAuu8OK+CN3Qq0dniEzKGcVPbjiukOY20g/DmWYGyqPXEEIEsHTmoGam0B+cFIy2gHuVFJ8FJdH8TEKAfQC5xI0ozXEZtDjq6D/MqJ3meWZ64hiXGqYbLuyP3NVG9kIjOqDLaH/Y5jlb26dR9iUoY7zgePM1cKIujfkn6iIlAtVQLXde46m0Gk4dZqKO7hHbzeckVauovF7YSFUtww1fuQoqrtEn1Bv0JFK+8vg0cAK6y6GbZpY+I6e6KANFCjgOfxlo0UbRoD+ZijdrlYhBF8qiXVWTDHv3hyZaXRf4jq717hRhCHkWg091MG177UPuK85J4LfuEmQLfu982RS7o/b+cT3dQCVrtFtNnAz3D4+4JQGpdIv3/EtN5tvQ7Rhg4i5msXOHWx6VFYRo68R0q5dwv0rMBOdRVaEtkP5R2XHkVYfMsZD5gQ33joqWy+0s/kWAZDZwPWEFnNuwP5IMGluSnl1CF6wVL7HMvXFvJXYS+PIKP8CX2vRA7ETkj1bZc3zA/KdeG3XX1BFYHNB+YdQXP+hRnMGn+JG1pdD9pROXgt7CKZvyIa87JfT1gFHjNxHEfKioSGnR4gKTqJHBWveCQe8Iyix0S4DCcEF9t8k+WyQwawWLbPgY76K/gFxLaYLsBvACg/M7rlLV4Xr2dyuEWJYvr8zZ34p19C3F9XviCzoSybEFkDg2QctxWGc6QxGmEXNTNSWocpki3Ep1n8jqczILyZztz0/wCR46C8OGmNvrJ1ahrneYhdaJmNnsS9kBcDlvLlW895XoyYDIqvb9RCuQjww1K5rKvNVDC0BvgQ6u3EXXUxXi5mteG1p25ecQHJ0FZHgcst1GyvchuUp6uZZUL4VoZveP5gYL5q47NoRcByuvs7N/K+IiDgDavvlHykZgL4OdZhAA12KfylmRAIAsVWO1/HMojCuMrZ+yGvE1VOXlMFMYS54r2gC22cXMDNABgzQW21OMlfmOaM67TIBxAjMoxNXqVHCcrKLnEYWW4aYGxXYhKm+Zo0WrKacanQIwM0oQWi04Ahkdxp9zwROo8d4cIbfI+qwEO+dYurm5D/ALyzGAS7oehMZ1vBz4SCLB1JfnrFBt2M+TMp3A0P2P3BrbNml+OSU7yzFb9sur18pPzMGj6C/m5aXm8PxLZxuD1j2zMwGUjuOPSmNfO5UZUr8O8bnsGgeQwkUFcfQ8BVw9jNRydeJ3saAD8C9xAU7L5/YYfZhQJXTA0dfMe8kaxZ6xxXD61fu+YGMQPSOjGAMDcDXMuWHoWnjpOgTPZxEMwsY6aY8U0FpyrgWWwy5Kt1PaUGEBr+HOZlSCgDEK7uIlS2QMU/tnYSQSw9+PqEVOsFEML2UiHB4BWPfVKTgKg12XqDS3Ss058HMvCFmygbIcaeUU6orNhoPYiqr0PyjtrvdnPsTWOk4H+2K9tWVmqKzDakCpeuM44cq9qvtKxVYi6FD8BBzwPbbPsfeCodiChjB9bnNMZox03bL7vdp43nPFkxBI91GF3jUzCuUSl5D8QJzgfc7wgkgvKRsx3hdgLAgBKtl8LmJZbFyhYYA5hrEx8Qo7SjYMSijfmBvl95XgFTITrlyqvFzfG46geyKwWlGQ/iRD0Pdm+3mVJ7o4S4D0DqKb1ntM01Th1CtcXKmiOWOtYo9iP3Bwxhdh8wbcfGj4gvitFBCw6me8usKzSuslF/cYiEINxyZ9eM6vz/ABSgptVOMUvUlAPerjZ01TX8UyBO6l4AsXuVDTxZtDcthSUTLrvPXFWPaWalKQGRa+P3MZ9FkThy3EzkiMeTvLgoW/eP4mkQ8F1x0p9wTpsaK0zB5xFOZV+IJ1FSt8w3XwTAeGBgmUslLmCnkzEg9R7wj2VeiNNccS4qoVyUAvgfuXhBzROF+5BAFacy6CILR2ty5rNBb8RIC0omcttd9TOukrHB8HWGeplXvA68GAhlcg3ruVsZhmlCor8m8HXMEiho6l+zaleYiGCR3BC6F0IXnxKNmPv5Iog4JVyvGMS2bzjVM0CuICUpg1FhHZsuvMz00jGt4VCbiBYLnq9695hsA9U+mpk/WwXRx88SmxbacpvnUcuwpELmG/LGogTjg4/cuRYrQzE8hg99ycTQUQR70MGIjpiBtlZgxhlPdNqYdTzLvMro+0Dv7lJnwxhkgdYhKbF4CI4tg0+Z3javMs4g7HOhO/zxX30PuM6xTmvMIjRjI96D7YsDPMH/AB2jXEbKsnvSgu7uWWQZaEQvCDctYRdq7s32lgdr/YIqV5jHvlZnA6szPvmEzAd0T8svBitKU75zFYXOA+MxdqPRn5lMGuzr7XKHR2GX2XUtpoJwn8VKJHyKWMfqXguFKbgw/IY7PXcyCnzTRQBPsPhIGzHxq+JU8M4fiMsDSqafzHruEtf2lFBLS+vlnG/+xAhrKxsTj/cPYV5A4++PiNaWYXAdP0+JigmbwdJaw4Ycm2WYA7wAK4mVe2+PCNecegIbmishFttB+MCht7kZjkGzUy7H774gDmQaaxF8f6i22WLqMe1/U1vvIR0c5zk9qmNAIoLw9OUs79ElkGxrv6h/EeKc4RKO1FHZ4xZ2LOfH+jcs4OjZPyx8RS79mWFYQKsMXJ/kp+YXE+043FuzkjVY1NKXBD4qhZ0tBWPeYP8Az8aafOIEFxFm8DqDAx1UsIMC6fcUx/or9RxcoVVft5xmN16ix3eJZGKBNtp/P5lstrY0bCZqyp4imv63U0N6tmcK1Eck7q5gRN7wadxBYp7ehAp581SVoDy5iY4x1g4DUq6xjrKziGTEBeOJXaJFE2jh6yruZovQfzE9ClOG2M8nujR8ReOJXoIWbsuBp76GG3nQdoal6uYXqCHO24+YIS1d8G8VEEkoKhPg6x3Svp4jYQpCHQOouX7XcwJr2tzKE8rl+dy+BAXCHWp8iB8Bf7ma9OQqIk9i3GzxNBvwG4SBfr/pB6XMQzEpOXP1llhh6LB5jSjsOy+mWoWdFQaey648xg0t5yVrMtTrCj3EsoWrKnjp3IjTuXTD+6l6hxw7lseyqvMeKnNI/cp1MQ4F6/cKJbgkdqMzQgexs8v7U2c0DSi8Ulxlev7qH94S6+FX/agSpqPEst4dwZoPVJPzZMBZ50/NpijLqwDl7PH+4QLjejuXtOLh6N8e0oVjxFMrqDeZbQoZhUTW6kWzzUqgH2Vd310x2hMExZoqLPZ/twzN1goch67YlMOEXRzdIcxOsdVebdBtfzDUwoWh0oxzHMA9uH5Lo466gLCGHatftDrl2HSuLvVXFEdAdX1gcXENRYvZ/PEe9/Bt/r5mMNJeZu2NQG3XfsjUo5Efd79IgO0EpsFePV8w+lGO3TGzA7So01t8XvEuGVYbdPuEGXJMY1WXGagcy5SnGDt7wNxlryYH2RPco8JV0ddc8wt8pDl6L434joQUIt2LOsFrELW6ZRUbHLuItFVipoqvXcMG6jqSusCuxB4duWbCwDiXdMjBLU6SltnDXl0hPoJMd/p7se3VZvg9UHKQ3zcpc7wAu3gmnh14B57iJ2Nkdd6BbyteIji+ct8bXl9pXR5c7QOHPWFNA4wHXVf71MGFkt2ObrvMVoP6de0TmxsUXyaPmIIbnT/UCCoENiwee/iPu3hxr+YZu2wIexzKl6KG/NNkZ0feDAtccZPO97ivULpH4RttrxbfUfFJkpdA8FJPeIUrMv8ACXvSbfiIAXOKD+uozQNfsbldZiqFD3HBGNLH+MgrCvivDiJUWMaD3K3D9A5brldI6KZqWPB/6QLXztancghTxlyeYlS40OsN5iSlhrKbZzfm5mWZYEb6YhVs9DI9pahiWPOAWwoD3/DC+oio9C3sADuzC4YmLpQM8uD7SUFXbgFWMSXOjWMDozfMSWBW42eOYRMKulXGMnvLZzKUxZa4vP1L7kQJem/zEAGhOyma74+pkfG27c9iaIAva2nn8v565G3izmmOU+evo8Sz1Fr7jDt7Ezz2RLC9+1wPD0dnrEvSzr/aWhXjdeX2c/PWYUgJ35+wPvBo6H99fr7lQirMAFVlOcQWiEAtn35lcWA5rSXrO92NPT+9I6ds1s90rVToWjk9lupnSHQQPbGjEoELVn/jrFRkAVl49q/MI6jYCI0nX9kLsy+CsZ/07S/7iJVYWmWK3WFVtidILQozXY2PTozpOkgVeThJYKF15asx5l9C7BKq7HaErmZaqCivJ8RDCZHwEDWEo0pvd9e0wwunSc3MNxUd8OCYcjaU+HbF7zegh1ZjcW7Qt3RKE6KWCtAeMzGIknyGg+VlAQbci5W87KPqK7gK8G6d7rxBIU41dkBh0aLyvB5YkwBurjh2f3c3UblCvbmGVRTEa7cy2p9PxsWlRThB+nuWgB6FnvuJi1u7vMVLK65uexMdJRKxtldJxzL63MP/AGV0lNBB22RodSWLPvFl66YQYIdaD447TbdAqzs+33DEYqz5B4mHwxVsGntL4ItNpvmTCl4t/YlNCHa+8pGuZUkGZSe1QrTROIp/lDhGGipj6FanuMfMiwTbflWI8gBxW505V+otfNXefsWFcBSRQAbydoYAObqc9ALrcD6v3hZHnrMP9pRZ7+0uSWADNMr3xuW4Nbo0oy/O5XatDOI5dFw2oyJdnD/EV2KusJeCqhoOrQ/1AZaxxgK+4BroLxwzEdaMrFdp6OX+49RVVFPudZdPaoxoF8ND58kHQ6G5667blU1QbXM/wMbHXb/rmHmtOsO+LfqZBSQgsbV1WJlljVh57959jOBjPR785hsoN0VaiqAjjDziUFmtQSqvqa+IgaYOu3kOXC052rqm+yEQ4pKNH1RMFXVcS9pz4+5gZMyLXDs/rFNqbVDOTnpcPDG3wLmChB+RMN0jZdyGBRfMqDvPeB9pcNK5fMrQgFgxFXQHPT5lMP6n4nHBmEp4A0u80HvFWGXW29+rOSF2T6X8vxNBBoqB0hgO2H+JSwuKGfxD2OqYP9lczWFrCrnVY6C8Z6SkAyho2LHJy4GENtZ32duPiYeTZretfS4Q4YVpfVdnGOPMRaPXsXTO32jnDx/majeqwpYeYtBehoPacS4xO88ej/il7jjTHDn0B7WzhxPgg4uaihvt23PZKkjxphbh0Gri9X0luVtBHnlemSBrKP7uC30uHSYbVycfEUqMvkfN7iGgSvg+9SwAATgOhwVKgA0GaOCCw09jiP1IM2DWXMOrznPxLsuhyqeuM6mGW6ZWsGOrUdbtQrPKvP5iKWnT0Pn+IPupn+FSdf6aJD8TK1v0x3S6ZejMcR030sTOtX1lDeZ6d3+4zECmsccLpfziKHG3Dh7kx1gZRzOrd+0woxdfwt0dX4hRlEdirXmWWSm7Xzx3iV24Jhy92j7nCsoQ8NZhNOQfLXUv3gXANHIdfMpcCnVpUPvTtWlteZrSGViit+IaVy1yVYR/twbzFUiYo/uSdm2Fdt9B68cw/uTgIL3XJ+ZyZiShdXWxj2coXoZWEiHiq+RluEcr/Tz+YxorGX8MG3MCWNbdT2Ta9xg8p0fdwgFFh+dEy0by7/xKUhfBBvvKioZ7JbpG2k2Vh/WOfZOMAAVB0Ii1zFlxp6dXswdI+UVec+vx35qL83eTsDfd9pzU55PP6JZNGfRozSweRyqJmh+qbtLrpMtNKeXVV9X9xVTO2DgHodfzBlGR1COoP24JgSWMh9D07wl95iXn09mcantMzMz/AEnvPmIO/R32iTmMGV7eidITocQOob2rMfP8zb30Jmo1TpMVZshqOGGwMFlkcHUZuu5XbOA0XKBLkJx3hYrxCYFntuz0mTzoEYRpi13fP96xkqPBZZXfuR2IoY4bcdJkFex2B+mV4KGHLfiYagJAYrPEtyRb7Q01yckeDHpyaGnvi/Hcslm72AOW/Jf3ENsFF7SnkP64iFgpgaAp7ylL0mQqtl8/6hThIsPk5R8TUSgiKOFH1UwdXCu6LP2y3VgM+ZWTdWKteLle7UirMJcwKFAi/kiGO8N2843Bv3cZsjDGFBkOg+iNQS8La4d/USsVWLLWTQOH4hvPCZ79X4+ZhRsBrHiNnLDdD9pjmAOqmyn+YMGtaXw63zA3qnSpjtLlTQQ0fz7RBDjXSYp57GxY1LgLjF3+CJvSUN5cSjcgGVceIIYVfLl2/wBRMlunl0/50uMt9vbpHVgcDUIy4LjOFgb8cxaXWbtSe2DjHyRGRWLNJ4/SCzYHy6xfkOhM9Ru1J0b+fbWZTra91U/Z7Sp8NVSnoy6M+8tNsBrt7Es1QyVd3+TLTbeg7PjtPcsrpKOP/Tz6eYvo/cM6ww6TeGefRuCrAKFygsWrzCsBzNpXcZux6TiaEpIVzWdVC1y2dp1rpMzFYayZGZ2MVI/CqWWJu4Vmb9vmU6rMDqZauNsc1lR/KYGZAIt5P48S1PZVk6F81+5m4DRhDAh7jxe+Nwka9hCgHBUJMi1tvfxGm1cHcHXE4wNo0e8SgMo0tcXw8y5ICDluA76v4bnEj3JrfN13IAIZ3z+O3TzLQ3571jt7Z0Ri0YHdr6Yj+VLEorw4/vMJFLlbr5q84munEVfLKeTrgB44ghox6WqjPiYgFhzaauFzYVK3+Y4GZk0+e8B8dZSiLvP8k1QIM/1Oz0mIcy7pn9h+uI0PkkyGP5mIsLk1ZUymy2aFFTBKpN0fBMdL0nn+H3LrGb+d2l0L3UtfzBHAUpXBk4hEaNWcFfuZCpeQAduvxH+oFtN8sckFlM12RUi1xu0ro/vSZsvF7HV4tXfxAliG1wj1VyrDpCBjPssNfUDq41dtciiXZ44ePpTfSNZLjwPnjR7RiJBVg2/fiW28b3/jHvqVJMyGbp+RHx26xNq6rlgfP/hf/jeagn5jkYZnNMScwJO5LjwP8hK+opk7l4ipGW2uhjrIgeE4T7hekOoV73DsRxx8gdRaDF0lGEli+g/HSIGxLes7EqpOMCiFHyxDbx5Oma6d5QTcObUmBwac2+Ys/WFd2bRyoevtBojo2t7H+IGzDDw64gQb3Po39x6BdwS7ukzcRcaHiXAqGXVbXiWQvPNFOF+XpB1iW3UnK66p0hUX6AlkK7KROT4x8xGFRzyFmK4dfE3wuNX/AHEVoC1+3tzLpMEtBk5+4ruikxrXWD3RBwpVA3VVyysQ+LvDq1b8zbI314eIXluLQfJB7TmlN9JRoGV3utzEq4AzzL7ahU0PqBWWAn/Q4QegJ3dHozF6PeFZDAphJvENB41abzDZYXmrHDjEB3lDLytGBxBf1C8aD6juwSL0RJYyZde3iOo9tDMBo/mXShM623VPYxwSxx2ys1JadmXrHfxZLTtelFNeCJupJor8lihWjXZ27fkzL4D8PmXNtGjTydB1ZZ5ZKY8PTvm04Q68Iem//gF+3rubMzzNd4OnoZ8x3j0QGzmYjcSlm8ziXgC1K0AuJfJbruMkOhWxT4AKJS8IzlYTKulvp0IDazOI0b5lMF6j/ExuV+YYHGDBHXA9mn2cECLdXji4TXcsOqGoldc7eUpx6ORfdL39ozj+VVU/3EuegLtkear5gmUVZev43zeJwX402rKPkykkaZ/o6yxZ4bXJg6vX6h+E4DXIf75zHELQIQEaLOQtiu0Va8ndhVkljti8OuPaFLmMK2+GCDy4WjrqIx21R8ZR8phg1w0+0qdaVdRj7iNlehbcsaMQOe0VK+C5FeHUYr2QBTTK3riNsGIkAYtq+33LcbtkPN/XiLQQc3svCefMCgNHaO4Shtoch3uUsJxfIYc8ZleikcQDD7mLY52P3LzC/eSoxfPGsp7/ADxLgmsNVcaOjGD5nJOoITbPYDbLCtGHT1fY470TKTlT5E62qvV7RBjTpA6uxMHrNF113+7ZmQMdXsdu/MKnddsfxenyi9S7WBs+3+G/f/Hf/iYjiP16PWDqo8TX8R7Tfq79Mp4gs7o2eIy9YlLeI8gqIUazuUrHIM5lBAZKXeoBlB0K/mYwNYBt0lqasF9aPlhTOqg/mYojy1z5m6st+iDXVhNX6eOsytbwFHnxBZkesrhah0AAznvULDOcTwa+/wDkeiuUrpgB+bhDWd9qZTzr5hEWYGFxgnHmUTJ124oZmu0x3PObeRo8xoVZ1jEBwFDyHfWaB4lVkH+sQ2H5gh84ll4YauxUBLolalc5QIt1Dh3RnQjjba+ytZlvk0894BVOzMFg7Ru7vcwNUhyDgsrAts1MvQcsmnkB0l0c7cH9NfUEU7s7PJ5hMZb7F+5lkAXeZmcq8aXm8uCXMdN3E7FXEgtKeJXWC+XBGs1ybAo4z+INGuQv/STYqBWAtqOmNczKVlj2R3frRKGZQrYYP6tuY/SoUDy3ASwxnAJ/r3liWTXTXjwdPmbgiDl/rfxUQta2wz/83E/M5ekYxh0jOJg+lq16xPol7cMEo1niX8Llu1XeJOHh3AVgb/Mr39omcjCxtu5ssLt0SoMEscOvdNdzAWgHu7QNBr1BVSoqul4L8a+YOtLUwB0DPGpnsGvZ23UNbszDqiLbGCpnjLP4RYenl3HWjWNHm5ucCpAWZimEQW5b6tfqYFZONW5Y0Q6ImRLqFAFh7wsCD3Pf+OYbKZR0ZxL40czLKSVpin1LETK4GuGU2ihRyf7UN0qCukEWFtDJ18TCo2CGXLpZeGhMtDuY/wBkT2cv8Dj2gA29Sla6f0R1L8Lg47oWFaHMx35ZkqmvWKlAqLlEoQt8anVuj5z99IuNUYgBQ9rqNMzh85F81QE4q0HPadzR3t4jqQJR3fbt+YAYrwUHCKrPm3wv+P8AsTDeiwjv/EyzVcVxNvb/AOK/8teJu+8M93oz9xNQc1Mrh3KxmymDrEpQvd2gzcWAuhNMymWVjMFym+rmAvsSzhvqw5OO8z5McNmOXh3hd8jM8gVnMcBYoc+CukZGGq6PPgz8SvUZyArw24i9NBV3tO3xUpqvBu7d6jWayWVVl6dNzNQABtGdBdL7piTy4yOTxYvzuVxVRGhpXD4YKjReCD2rfTdlb7xLIGc2VfTo0/3VMTOC/mV460IKxZ9ywChl1Wo2ILhSgOv8ytUEY6HhlLLqAHPzHa2lXKWzH3F+30VZFll12rp/MNU0YNLe50PBSh2+T71BJG0nMLUuI3g1ERPx6/R3gDQdNdx/1zDj3cdNdH7gYG0WyZhDROyOvEfoxadGV9qVZfzp+vBcYxwPaGbsgJ0mXiOi4upUM0mAxj79oKCmO/gX52xzhGjj+9Z1O45a457/APxvoR9XU1R6Tj0dzi5e2dZgCDjZp+iZ0RVUd8WRLy3cC2JT6Oj8zzOIZZQ7bvUYY5jg3ncOHh3E1NdzGODiA7d+iCS4dXdGGyM+Te/MQi4bhUVWRBd2/wCCQ9XSoDlmHVbGt3u0R0p6fVDpe5ekw2c+XoPXhrhYZ44bx1fF/iEaIztDvxnMFg7GoVo4fJwjHaDR1O/SCwhd2eHPvKpa3z6QAVT20YeeIghR0mRsHL235IIOiBvB/wB+Jw+neYdRxn8xnLlgB36RJsDVVNyucVeHx0glzDNEuEJwG34dTiATVBb/ALZYDwil+Tp+UyCFLcEugmoKAXe/pBYmi2IYcXsZllbuVy679l+IWgHFdX9GpdGtk7LZ5fogKC3tetfjnvGbW7phwfj5iu9xwo/U29iPQ+f/AD3Pv/F9WV/iwZJrxCGY6jgqcTFxMEjB7JR3xqK2aM8Si+8R3BmbTO0DC+jxHb8JavkqVFzcww22wNDxcyqmv9CB7cln+JNewxzZoP3LsWKqH3xctySl4F6X1OhQkLatfJGGjQg1imcHYgF7LBQ4PLEHuKP2POdcTLANBWmoTRML7Qvy9mMKCMOb48A3BN9my3fDwrLwMsnKnr3jR3489m7+MSoU3TPDu8wykFrk8BMW0wHP2fEWVugriv5h14XDwfrqVydMxAo4Tw4Q45ltYzraXBUvYM4EHRf8yv4cqfp+5dsb/BeLGNEN8F+LiNyytvzKQQtfmnAgVIHD0OlHnmZDeP8Ad0/Mr0WyNmBXlIRZvrcRe0PSK3crYSmWl2hOECqbzrmeUH5189IGy0oo0BqWBMtvohCLWNNHZ+Yum+JrG3X/ANfv1f8Az58ejljDUWd4whm7cEOWFwwrbb7wsPI5QXZOEYTjvCYhi5d6gTPGX8uIKz2zQ0NbvUrk2yCl4/ksBlpfK8i/whTFs3PPQM+3ERpdYo8Boe7xOTUE82uaMecSrnRsHOT+6gMcUVsEprW9Jam3UGFxUesZHQHZGcDiVRo6i8Y6xizRfA6pMX195UFxHWZrqXLk1fvwTINDHfs/3+eCFHDLupMM51rpOKYVEC7BCbrPX2meIF0/4Mwkzdsn35hAiniOev5l/FprLs8PzEsIXpa64nKarpjozZr9R5wG7SjDS5j2GqvT8xCi9Q5PdBla1CMrw/UthGIH9czXVDVZX8BLRT28FF+0sGi/O4M94Ypn4UZm/wA1DW+oGXE92j5TGq4hwPgAfzLUFgv8RMG0dHp/pxMlqnLsTmzbUFH/AKv/ALDz6F16OItxYZYlYo3ftKKrFz0ilRbrqy0StRip37nJBYrHJMxaN+/M1NrmpebeY8dYrDzCyqupDgfiaHRFodD9kqZwWNFZ4IXzouw7F80TKamx2hdcMQRC8cqvuBbDs4pyrvf6iZo4trGK+YO2fTehMRl449o5Yj/hOa1Uxhp79Yfox5qOGAOvmcuv58RdDivQJvtiW1cDC3fJXPGKZqRaz26+f7zmmetapRLy5KM5nUZNrJnHTUa58x2jiue0OrC9zPPTP9/IArCqB12gXSXe6NBMIB3loVXxoj1twMtBc5pCtE/rjXSU+I2IVX9OIhogl85dK/c2iidawxDhVt/eJkth/d5lSEH7AL77irYRB21KLbLqo/i5uwewBH8TPOtqUTZ7PtgUJMhyt/EwHuBVl7/xHE7DxO31K1wP1A+X/wBn/wAL/wAdIa9BDcWJoIy5h1GtTHrKCwDMW/DnIdHqt5gykoW1UA9b35g1Nhut5H8wtOpT0InQvMqRoYd5UEEwfaB1x0n+hF0QXQOVUM/6lgvOUb30exHUWz7GOQ1uWvJm44M8h0GtvGWYl0BLGMgdwJa04rxhr4m8rN7b4DwMczM8wjjvLBWHqQokAp5HN+K3jhUIu0xhyrtL4ap3m9vcRJVDPb2epuN1Ycq1fG6h7sNYeXMZQHfPd0m71w5nGM9otWlHOTR+JnGHQ5c5/upe9cvKUIyj2s1y8P41LuCgvHu7QTLkmmMcOc7x6Mu9tq6w59iXKui4Bx+jNUggfeZ3mq+4p4u72IZy8+LJ9y+AJja5feOOUXkA19yngol2xzXTYRAnGb5hvLmfv/5H/N9HM5mzNvYi+gpDtOpPMxFBZNA5f7zEmcnvKbXQbix/+GGvz8zQcER7nwy8M9e8ydI6q5pUda2UX2gTkdYFzidhKrGnozJuG3EpOXIrz7+Jw1gEOXvipd7SYAvIdDPzEgyxmxmg+CGJFKXkMb67WOyXTfSK7jDHBbXpAyPOtNcJ3GkmhcdM4C2DYnogJg9lqZrbDKtn3LyTpVpXB75/MwG+jC8XFFuVor4R6744mxDEnypsppz9yw223rBr0vMq5ULGUA+lG78tyuExWbSbHc0XB8EhHFGXY/1LWdssMHLonETeodaM/mbWznbNzXNNvh/tyzKup6v0QrZSMYvL+41pujfgMem5v/1f8dx/zOPmJOSckfzHUqAFsfA48xDkUCY2lVZm8TlGbyJ2LL9o4QTSZXD+8wpcKXFtm+1SmbiBbRvyp7wQDfRCp2yM+SGxUaA5n62paP17QxaNrymrtEEp4XiEF7eSbnR1l1nxKqHaHCfmoHqKsDE/hXwyrLAyW2X9ze5ygplZhKmIZ8EzYGOE2U+lHZr2aF+yEbmJ4a37zO2svjqA+2mZUWOVWbfiWfTv4BlF1V9e/VIYHSb4jNUUXFahAMAYIkLmpvMy2U488TXacnLr8zNSjIOOz7/pKDV1PQ4D+tTQ6sz0zFuj8uX3l4EBzdRW8yrtt+Itgg7vGpW30LVgZYaz0+BBftX3MbLV4D/v03/l9f8Au+r62vTpHn1DbOQGNB4zHItyDdXx3lAwAGLSfW/6zLTz6C6Q8YtaR2O0++qAdktkrt7x3cHZ478YRjd/gaiQWMzXibXN9h6XJ0YaxOZFY1M07r4hdZZ+nb2xPA5aemimhBCtUxX1HbjRj0N6qno1OpMI2oX0gsRvwyPtMJ8OHhp7gkYbYfNizDShay6sTCzOhejoMDeCcxzw1EVKV1h2TxC7h05Bv6afdR4D3FOKkr8qV2D+ixxpgU8TJgWxaW3dHEu5JibR3+4+w8uhgRhVfBe1w91r2iquEGe5+IspuH8P+PP/AMHn1Zcc9odouSZZ9OEWKnRCJugykaEDuAvEOxxGtPLoQLQt0LUMuuZn6oVOF+9CLxFHeKHlah64qJ5FgjpnP3+Yq0efDg/vWHZ2oorz87ewdYiSXeiNAOq1BB9JO6dKDvDdamGuCcr6+jse8/OZrt6Pps8x0fEVOaxOKNyypVYlKTddrai17A+YJRlVsX3g695sXcdZrjReyw0BgCKGGIjgC/XP6GYWjYqtviKzHzLdZljo4jgEuukNFO5fTE7xQ6z77Z/cBPm4G/0r+pYPBK85x/L8TF6dQS/W5RBjcuMxOqs48MXBhIY5aubgGotUa/mWXe026P5lCVB7Bx+4m3Kmef8AH7/8X/A/yDEOYt3U6S4qZfMsUVH+FR0l5WayU13+JSY5aXbFoRdjiul/3TMf2Jexl8XC5gM9Tlfdl/0y8S7gF57MRoWNcpxbs/hGqXrDNVsQk/n2xb52uKcB/o30ip7wdYwzG1dZsnphHZ6uyOpqhsiug9OID3mTKVeUge5OTOaHbB8pQyzy4eVqMAa2WXZOjzuHcK71do6d2J2sUpPFTSLDvp73MojdQqrMNS82krNrHSqmoGpNBu5uPxD7WvtBdZvdTrvj2lkB/EUssuxcx9KoDgMpDU2cTcqKfnt/uYQloOdtyhqI70rOPHZgnhYHTi/x8RWqmovNS/T+1O3p9+n36M+v/F/w33qfc0M4J7QYt4eiCFMP5Q+7Bx+Jf5m+I9AX7zxMRIq4x+g37zQB3Rkmv1HTzMuQC8Q+phEdQKHpBaxg4gGEoKeXJf1zLDnQ8OD7X8w6UX0FXbpOJZGxMM+Jp8S5u6QyEOkd+hTOicPzBFOjURZFv0WhDfV+B+YGMHy9BfdB8zP6k0n1UuDU3arqkyTU8l9CEFpXNLho/wBqjviNeKC9nibNaGSs35/v8KCLm+lSq1AagdZibiLKucrG36I2oq3GFB9obDeg7/8ALGFs5c9WVW4FpOcamEmtPvKqBNC+Y84WK5neCkeSj9wuKFj3ioyj/wAmep3lbVCDydmaw6hjHp2m5v8A+F13honOYsfTAjibDpuXKfME4FHghvcnAc9sMgrKa8LFwaHYSxHMBrSnggECKDgirpa/DKfaaIh1P2n0/qYt48FHadsRu2cDdP5Sspx6dIqhu+fRfhMfKaTDPobXOmPbvAGuyogfWKy9FzKJRXB0N/IiuoI+hOYiClCzFKvvr5hJyoQpLvyYZ+9Qy0WY81BTZggMH6HzHOOwTl5l44lZjfE4v1rmowj9isH7jGtdjlqvqPb0H6t/ko95yKmXX+wsM8BirggMNyhuBS9wXcT+kCBUhLEnE2s2CddQQpezZepX2Q3LWwyeB+SE0eGLz0e3RnbpOz67/wDgYZfENI+hO8cvoqIJ0D5S524qYmZ/0v8AvEDNlMSx1t/cstL/AGouX7jHGaTESZg6sy90OfhMI1CF01a/EQo5ZZYzTqVh9EhqU4mV930NpBfvCcvmPXpMA5I4Y5i4BMK6wXLl6xhZQfNV8iFBYNX9OWG0qhb4rjas8VDJhEeSzFtxYdQT9LjVMrXdH2OGGEUY3wG/Rxue8LXFZiHoNg5Bs/vMGbogY5pUBaOmoNEyd6tuWYs2TV/6qXlYKy9uZYp2/iAm2X4nRQwPTtA98ytgx5zBfdF2F93+LtMefFNHNfmvicYaPI9Xf0O+/wD4H0VEqo0EdRnEdY9HuDiCi5Sfph1mZNkjQG1fBvviZkftcU7GDz3lIqX8WfL9kQuIwc+g1az8s+hHVVQbTP6qXIlnZLoff1A0H04jzOOaCfh6c31nX4hhgxHNJp6SgDj0/CZlhStBzX8695mcGuLEsUKg3W1i89p75kRUXai37QpVRboTH4+JkOdJZpXPFTEv3Ga8x7y5cfrzjPxMKrgRnb3mD1LAIC6yxjA8prMofwJxlP16IFFaas7p7Ts91b08zqg+wKPontBcuPuBEm0FaJeHzM4BFvJWnqPxDcn0RcO8uITjwRMHXSIt5JzFazWpI1I4/FetdYYHoqc9E4YkH/H9zfv/AJvo+jlJwzeYzliqOZceEsz3VENff+8TLPr+D+8TmBJVn5LqXOzQa3zflILQ4J2Ofs/EqI6x+GLA19DgO5Vutwy5EDDudOPJCCp29ThHSxRhfX0esMETf9Gjb7QTzTR/v3ajxeWx+80bztgtJwHWYYIzQUvRGYgzqf1UMx6fBpj9ECoVldQx+pQNfUHMsAbCR3UY7tRzqFZhkC4GQLZ8kvtQLznmbUbIfGItT7BMBhya410fthiEDAPPyx1UL1HDylkmFrt8oTsY686nM6bfK/6mlkt4IM+2d92PpFl3JvAWfxLG3uUlrQj0H15/upoS1r4DiYVl5yAq06NInYZaGGH0rqTM35OhCTkPCVhfgessaatXEALTbtfhEyMeVd11SwQJvMK44r0C3j3hh0XU37/4/Uf8GE6IznxFomWJconRRxfWYegzGlFnTrMR2z56vh17Y6xiu/O2Kq/KAeZnTevVn6MHtNpQ+5bfz6kWrxAszQjpmscUQmTZa5aAoE7Fr9yTzBPrwjufadXWBALVwHMpi8bPxCJhabHyt/hgcwMmLu4sitcqyjNcsFZvLFlhivRbYL9iuus05+5c0/HvHcFGKWz/AHTDwAUOrmO4WiirhzqUSRIJekuubiqL1SWPh8Rtszuo5VXLPiMwpzC/YlYyLDbp1O4fcWUb9JzCus8UrqkS4DvnjxA6gIWFl6agjVS+4N1/uJaufOx2zO69gyGX8TqzEYQfKPQHu2z9XKX8jwVCyAMNshklbUUTobX+IhOsB+H8QKkLZrKMD0VciL8ZhWawJ5aXZCzoGGh0YXOkhuGDPV4S6pwGN9ejCwaeOiUzm9cIlwcaliEruf8AMWjGco+Qhb2T4gioDHiZVMgBxtisbbXLznbH1+p9Rl+lTbXTMGdL9OZk8eiBHZHcOVdWXp0H/EtZYDS/Q+oZyaDzGynlWehARVxvRh03A6O1wFa9MCOkG2MYWpkJuxlqm7LvGB/MKEV87PtGUzN7NpX16MqWcsIu0AtYaoBseOFQ67D+vtLZQt1r8Q15xEqF+zvETN946ucky3/yDp3lGekutTDn0PJb9DBcAZO1UNccQFhkObyfiUGAjgLgOA8eOHssoFQpOfDxi6vsyqxiug7amj7w9QOGC4zAUIVC/gS7jVwVRi9Vny2agX6WVL0Co7jBpOK4OgDChJCs5bs9IyrltYKD3s94dca3sDzzABAYeHCz2wWIwJCg+8T3YKVxZlkVtWIymrZi/wDYmJVUD7HfbNBJ2yhDvZvDCHdtMv02j42TtfQc6Y510YORWXV9QSmKcniUQZKmpTk31lugTlLxtz+0pqc2xhgF08dI5xdVco5Mc5qWWg5S9xa8y1QzFv3LI7bs6R3/AON7nSJxLxGWCuowWnYukVXWlK7CYN6ME5DYcHMUmXYZLg8L9ymxfG6E3dmaMYScvaJmd5wCbnRLz7R6SksXFXSJZ+VfxOcShrdNP5j1EqOhG51QdrEIL6v9rvU/Bz8t68tzCkDI34OHvAGN84fUPEf9jlW07YRPdWF9Z3ZQCPRt36mXf3jlCY0jih0ZYaFdsNdianaO4ib4R1/0uAnoC8V/XWVD1AOIEwQj0b+DqfzLMSDevFYo6Tay2b6ttzxiWgK1wtKW2BqXADFjTp2zBN0xrI37TGVeha8Fnt5gMKQPCZYD1DLF/j3lJFEsKX0+cy2EVl1XhawymgcQSXgIUtWa+YaN3RYMSUKeiI5TwtBqACcl5WxXFuUJf+x/UqfVD9y7xidgDb+Jf7ALP9g+yMyQA0N9YlT3KtBnJXfO11Ol6oX2enUQmXAyy656Q5T5D8xe610mouM8PU6Som9HWP5AGJN1ZeUKFK9KmXoOcxWuoYVZy9esIb/ydTKiLmHpSbVCZprTrLvISW+YYuLB0igwOXJYt2v+eIU3sXI37HHp+VxXAMHZg3dZkn3hz4i3MEzS+sZXg0B+INLDUtXs9puv5iyr1r3xmxbtLLr0vgirIq6+0f6vMq+vsK9ePsTCBVly+quX8cQBwZqIg4BAeQAx2I6s+qFOwcEFvSDodZ+kNu2Iih43KtnlzLJfEy9Gbla/DbefzCKg6znafUuAh4AM/bCN/BHbfSoooji0FA6bV+JWyhR7wgTOcoLkY7Gf4iYIrg32+5apMChSWeZs69Mpxf8AdTHcYAPtK8GomF8L/EMTqlBl5lR1AEBfaGssQac/hDDhljVnENOoppxi5WZQci73hhDQigd0w+b+ZkCwk2LynzDz6oYKZs32r+YsnvMMxGFpSAPtHERSp4OPIxJUCMhcV1AwwGAHFzXTPxfiZeNdvu7wzJtxDkEHxxKlKVfEswT6MVbnKB3NsKdnaDPIk2X1GNuYbVsxU4rJzMh21Mp9/wCDGDtN44i7l8wFcQbvQHjlgPjD9zZS8uCF13S4P2zlwumnT9B2v0Zsu80us/WYwX78Q+VjqKwI6CGTE30D4+svw7EgYv5jCxhc7u1czbr7a6+Xr+JsQDaW7T/WZywmf7j7HzBdSVdf4EUvj7xw/wCxNQw8A0bvtuLzaRubrK53TRfNzVrKzHtEDWOIrw1ArfmcRVxFtr7ZGB929pkYA14X9vmOCt13dcNdo8Jw3SHS/wAg3A0MWCaN5+UZhYro/LpFcMNW8g+uDZ8Skl3SEOc3y3MgATNluss/d+w/3EtSTuAacN9JSltUCl+G7ib2G1nDrn3lCbbT69SIaabtHa2E7aLZSmbHNpbOJoHXhlgj3ynuofTzb0UIZV1UKll88CZBl9dn+L6QdH1SNr+5zGeY9srY4K6neFf7bDlx2fEyb03906krIdBHJ4lFWB0OfMZU5vuc2HA2Srs6B+5ZMOKAk2njiNWa2yC2NqJuYL9pnvcEB5U6Qs07j/guop0mkuWTonY/hnjOsMrqod5tQV704PdlwOwiaHLsz4VzA+wzXB1Zz6ZkMkHEa+hFHgmTjUoerCznXSWMFAYObMUOA1R2LgucPkJsdjJPY/nXSVIFmW9ux2JYS4AcigQKjWNJ1bN3GixeHiWB3a2x4lYR8l5hiNO8NUOJlGA3iDMqVBqqwD2X6xqalq2Dl9MPSgCXF0U7jPUdGB2sq7M44f5gBVOSCPJOn6lS4CrizbUsCAVjfWN9TgNPeocXGd396iQCpCM6uytu8RMuqG7EEJQF9S+r+GApwFGZ20fuIHwa28F8RgZRYHR+LZkD1wMkiiuqQneFsG23zNDFMfhTColZWxBAAahcyhuRVWw+eZb7aH6ejfEeJeDvPSuZkwMHxXWf9dZlIfF/6ainGVxCrkdzH/ZQiPcDECkD6MJ451PQjfsdOSAMNqhx7TkEUeaIO5u4sGzk6TnCYGc+jGLClfmaegLzmIues5lnJbJdLnQdcBfyG0cXutIe/EcmlhhMlvf7FBKTAaGvR9Aho95m+yOCpuYy9ptfaHVvp6NpMEb/AJlHvrd5bFqejUpIA4IlCC7J2HX5iXyEH6+onHHSPcNntMplSWsMPvBlOZ+hKgVD72PTgndzcVP4nRqGLQwevB+Zlw6rd21dbQl+KRoc0fsmpzEd/AGGZEIArZw5ZemTReBM78zCxIRpTtCNvDe6P54g9TaKYV4KjbooVURJuElK7J3mGIjRZ8x7dmnXtLRGKUT8DNtPQ4DZ1ehKkribN8q5ZeRR7m4Tde/D+kx9cIO8j7BLkCG/uPzED4lXTRZNToIZMlRu/wDe+pq69OIxI2KgJLpGvP8AT/XEDQWnXTz47keAuAVldnEAgV6JeoXrcQTIFF0yyDnfosxYz+YOCmW8XK69twhmo5EnaPo6jg9T9CXj0xa4vMGbwthGlnd1HSnaNt3pyWg94yddOD5fetXg1DKBUOCPosy981945iMjiVbmXOviFA6zWWOZUwfzGqwaVtd+ftGqL727/wArmFWKHTXT/SNZy27n7TAElUxMcw4E5jipnLuIOwlMnM1DtXqe4LG7wP6pZXDBXKWG5GZ7pX69CNG2LB3e/iKTVHKP3x0jT3a9McfUQ8KWPg4gCs7LBPN7v3hc+1pKeqoINoA2s75jw7FAKx37dJXq/os37xyM04Xa6mI+5UbHXYlt6EUHHv35i6kb1LYXtLCNqN2x+ImqrvyNfqVdq81m/wDctNtJzpJjSqxMXZvCYjwRzGgu2ufxBOI+juLKbgVAsZqtq/C587jG14PqDo/DABYC2930i1JZgGNe2lJ0gCqXEOlw4jmtswEdD0gm4j6iwXZX+G2ptU1TpOI8QLoNzYds/EN0VMzwS2jgC1+JQpQpXUp/Q5hgpPQsXT2pfmcS7l+huJiTN4s0eg7YYF5Y6XBat9CFoDvLURxL0OK/nEVoW+D8vP4gx4eg1jpMoDY6IwaPNQ1Y6JjRG3uqP6Y9TRuGQHWdFgaXVZ+BgknorvxOAJEQ7oTsMX6lFakzgXvvA0KcuXOFvFe0yEELlJSlpzv4mVeBa32DbFJgAKzdl7eYVwhEWlc4682zevKOQb6el8yvBTjiMpCUW3nXvQGYqIukdY7NGjZ7ok56Pl+PabDGxatVqXH4Wiv5B+EqGxqi8F37Zi5Kuhijt7SqId9gyfN+m6LixN04bMUNCB0BPz9Yaj6pnEfQcziZTjZwjwnR7zY85t1yfq+5zEQFHMeZ9NyxLJZVWfqUMM9OveHntQ8Ux+0vVYtWZW4mVWQzbxl1UfS2rnDOExPMSoYcmY0o5lKJtuh0grGCreXXiKmLHrP5WJpe51eX7lzTGbkfzml41LJd4+isTXmVtFqZtStCu0pgNYgmRRVuKH+Zi2R2mHWbTV5ycwzbK/FTFOBHPYTh7Tq4vU5kJR7GJu9LiLDqdoLgRzYwLkiHEYDR+xfhKRmpKb3n1vCktqluzIMSSYite6K+zMTpqwflbr5h6SpW3W/PdiChQq3vQO/93LguqJ55peD7qUf7TJxgwyvPS46tG8hR+Mv3FyZtNbGv7uZWuhm/EUmRleX1aXYVf3tcdygaepk/J8yrWrrzk/ZAzd1XAz+47lxxROBBYFmgl60WJm2y+2EqVGa9HEdS6mPeYj2JUJ1fzd3f6js4fJ46uuME54SgSgHnLH4Z4IrTA9/5lLzazKBSH6I5gbpuFmsQDV4fTSOXUdQMzn0Fk9AlpdXoDbmJYucYABLZ2ch2B+Zge8z41+cx+Z7zmOojoZlFTPJ6Ss3HpHcC3MZrzFmrlGWUZThU4MIbie4brwCDMzV4hLR2x16c3nrBw6x8/M3luY1fGYKD1Ydmk0qLayKIYqtlWuj32YEOknFM0dsq9aIatEXY9VsbqZxBFw2dKcTcitaunATMV5NbC8eDi+upfnRuozTT217yh+RQbV8h6tVAdlKuynsE34A2sfjUYWgAGBqsBmKdS18uJhEeEtStz/DSeldXe/B/uIs0XdtvcqIHx2R/xTNkPU1tf3MHMgm0oXuZ1qC7vX8zD/JUqYS5Xuj77jd96BrxOCqoNlv5/ZDxrFPdfEzMP5P6Q6emUqITP78jFi5rUyLov0vmVROU5QOm4m986l4mgVU5jMDYsqrm8clD40fc7jmBRdPgeo5hbX/J/sQZGam4KjrGEWiLMWO2mK1Wo3XQzHb6hbGzRmdS7mpXp1PQwXDCviVQMuizid4ZFi5BtVHV9Jpfc2VEH5CoHZXyxavxfzCPavjB9j2Cb9agl63RsxbXXVNV27XHD8qQ0Gc9NI6oOhQV92r5+5dy7s25fV4v5lWCTcHag+IuonVxj51dkoa3lZOj8Z94IEY10QOsKVdZr1uYCITrAldR/SauFZjC9vFkDN+M3kW+IKVzbEQ1UapVcarBgh6Po/4tzGG4xxHM5zxjkH6QZz9+2esOgj+iQW+A0zBY390o/Bi2PtE4hhfzL03UY8xq/eVj0uT0ivYIldoObDglXXt1ymAQ0c+oX/foyvZHVai+DBDjzOJ59KqHJGCd4k9hiZ8Uru/6g9WI/wD3j6GWVdvid01NY5Q95sm++K7xqJ7rc2PBBqkWKilyiaXb1qUcdkbP2H1cIqCs0cwj6WpycEUd5mtRCyesPQ+BM5c5aVPJ5/SP0AhiP3bPmOsHQ5roS5cxp0D1JVldldVn+Ixpv/Qh/giX/cIrAOjnQfD9S9Ed/C8Pw+Fntk4I/wANzohhGAOtMa8biEtDz5CHqUNxR6xWCTDcdy4NRzWILoQWLCxyTlg13n3bXgirbWTsyrXulpO4a31xNNw4YlamrVXM2RNzanf0u5rsOMRF3ADAz3YlL4tLzhCAJdJS3LLVJwQVo9ot6TLeCdCJ1ZXSVj1eJ8Aejv3wy75moMvYXxomPDfspl/EzHVB4m04nQbnxAC1q4srN1DabJx7TMd0ARF4czhd0Qxn0TEU4cw1Z01B2sTz1o+cQJMaU7Nk4x6XDIEIpyY9FsibyNe7P2xmncXGqfxjXQDmWW7Z4vHyzU7pkvQTE02Y/aCulvJhB1FeLbhbgDh9vQb1x/gY9sXhgsuqOgy+Sbbhme9/eZxxRBi73OYhpg81ZPqDfos2RmlYh0R3HDKx6duZVN2soOyADKb+NPETAtVORwmTpGKHDNE4cJ+EekM33bhqGNxbm3vHaUZ8z/kbvqJPfX3Fr2lHOA5HOwhxfLHeRXdW33dPqWJ5LWZXF5YC+IuO0voTuh9dQzZmnxG4wm/supvppufyUx/0SnV1b7zZhwttECJGrRK0dEvHp0czRrVzh59FWUdv4j01MK9WHB2m0xO8+5r7v3nPKSEimt6ZYKODcAA/XqwlFwAavFPdiwGqt0VyvTFFcHmXHdQ2n9XtGDBcbc9zpe/iAZp0fpGrdFpyOPfr5lxivEDwWF7r/rM98E5Tl0gGGD/EZsnscT+EIP8Amky+EgB5iWjEtXER2KDuU+FFUs7O0YxTqX6DnM7ComI4jzKtww4My9VqcwjSWPHWWyM65X6aiIHGkRLZjiM7vI8MFuZ/Gb+ZyzrEz6HAjyZFeoO8rCI35/eOVoVVTDO04KtDsW8Wb15XQ1EegAWufjEtmYAO7OcblcEW46j0jpjpj+pAoek1Nw/7SW05q6nTVgvWB+GZNOcSnECDKEIVcIFbgZ8SqTKm6x3ma1tZv6EG7PmA/uYdqNSMY3KSgouUhUKCxnsN+0+LUZ8+TrmXCVSp09L9Fr5vw+X9LWokcs1u3X81/EK3qebe8Hw+DpK08AUX0IVSC2a4A/cVtWlXJX0Zl7ADhWf70gjmwU4rE/sxh636Wlafgmn2mXEKnfDBgvjzOZtdFTgZPiY7Fv5jz/XaXMx7yu8ofEojZ6fzPMKTuTSUud6zClGTXNv6YiCw8clWP7jmtdnA/pFkZ2feJVeIjZxjUGkHiLzOY8+jrL+BguanCEkcrpugsMrI381Neb4luhOT3hhm0U6c099+ZXWFvYhnBKBicem423N0dIPuA3gjKrP6iD0pJer6fNS4sYX++8cB1gXLlapExLvCXVPUrxNLYk0rrOPacO2Zi3ac3aXS3Fc8BTQ11uDDKP7hgjM5WmMZa/1BuOpCqL4lV6BO0WG65uNey77xGpQF5X/w95kdmJrBigILJN3cIpwn7fcXT6CCy0tYzyQNwavi/wDDiV6V2jUcIjBxU6V+IM7d8dPS3co+03RgY7btyTefwI+h6ep3jnUHWOfTBhubRYG7B+5HNFQG+q/Z7Rae0ijmu8apA6eSMl8dZQDqktkwZwk59D+p37vQe8GLZYzL/Vmib2qMUdp14o1Qk3r+v8fKXj1qWn8nxMkPoFHaZ+qrvLPgQ/E24iiq3pfvNkfQ5rAvUroHlD/uM2lUmS1c1dHWK/DEbQyz9yw8GH3BubxHAzik5nJP3hx7RYYqJo92au6xH8elrBx7tHvAtBzR1HEauKo6Vhe8dtLM81T2lxZYDq/9hr11OQ0LbXPyyxZvABFdv8sRO4XzfMbx/hthVV+jBvKdXTH/AIVzhXk8/l+YqamWObVf5gRLlu1YESGmnZNYv9odM/EAjhXnmPqw5lvRthvPoppNM7gQdytDtZpO+3tLWzzo6I7MFhlfFK+nBAuHia2OHVWfpua1O85m0/SGGdAa+ZTMgW2oxUzdXYF49dcwTX6ldArfUjPaqEruuBCyzABgZz/cy0Km8CxV/n5nao+56ChwSq9JkMqHFcyPiHZiNPx1gvlgkraHtLa7BT2lFeWD05zogb1F7pbxir/MA3rjEhOVeJxd4UzqxELiZQ5jMaAiK2pXxBcp+rj6sH1Gai17KH/Gc+fOgLncIeL/AGZX+CRRWsC8+Tr5i4As42rtNxUZvEUnX0wEi9cm6PzERCjCeljJMJjpnteO7gnY9pqcv8bqrlGzvK0JnJ9zUNhqmoZ1MsxjproXoz8nHvAYvbvufQ+vMNxLJ0InoSr161iOu4pTLrJl11KUnt3huq76f3cuKCMkZR4h1miH+5xXqZwmdxC7OhUQXWcB3XH6TvJA2et/8SvjXuO3qe8W8aXttbfOz3uAUE0k9xAuz7RzbDk6E+5OX0GvxNz3mLPQnZZcC3amnbCvf6wjLIfCMe5b4igIQLxDcJtwD+YqNFj2mbPGAhla1DL9/EdFvMeVY9CSFOGCFfBdL5ZnoiJ8lfaSjLFO6n2iha5TpRf4I9uoXvq5/wACKTcKlYeJ5S34nZKyTsc+q0dUjQCIkzKVoNOd9v5lztpJV2vheOLIa9eITsq+8XEVj2AfubChvff7iyVfoQkoNksy3qN2Pg17ygNN2UL68RYZPRQ9HNPUk2Amyefd+QiIV0nVx7ZJYPCX6/0r4ntyZd1OPMSHu8dvRjCO46JgtBq3UcQvoMH2jfNvv7mZtwFI/RjUS82W+romLtTkEEeLQpQAB0CEvcU2J+wivwXMLnKbR2zkOkSnF4eViwR+Y0wfbKeCUnhOHQmzv6JkYu0qryLLNmRz+TDbRQRxMIwCPCVtz6cwTVGfAiWFM7T5f1AXnZdvHzBfDSXsSCvctdrgfQwOmv8AEm0DFsrByifAl1jtyX6eJbblQ3xzHAFBWegPF5YBophqoaz7y8DoHXL8V/iy7rHzuq/fWHXqVNhcnbUtWEsbyZffo5216ZB4e7P8AfmXTTHLzr4MQKrEsfSvS4uGYu41cd49TxBnMZW7CBgPv+mGusGq4i3ASeaMSxFRgA+SYu8a9I1OECwOMzG9PmDt0jCqL4j0/wBzC/YtcymCYC1dX595jIbm7r7qpf7MPMod5h5Rwb8VFb3KR0ScIs+fQmLIPNOtx/QCz2LJrZe617egHaJULmFT8D9J2Nfy9I0TzZDTa7vMcY6zCGKVhati+PQstAa2/wBSwFqU5XA8syqyLQ8DsQulhPnMFhIN1xfhJRytGmL/AOPv/AJlNRTu+sZsBVQHWJVFTthfE5gyzM6scaoTrtjgJcaXhvwMJBx8Sn+PETqU3l9R+0XeK6PYvyYgCkyGOK0/MYehJyoaEF66Hz+Yq7LO8/wRPTKONwEiNR9D0VRStd/QzJu4Jl6LrL99YSHhmCGRZHAxC44ZdRNfEdS2pZJCxwRko9Dl4ldhb32HspiGxqIVk82+szeIOXTOUvwvPJe8cYIPjiyhkY6pQ4yp7zsAam0NxzmiTI/Mrj8Q9F/qC9CWeBHcOK3uZ3Y+5RQXy7zhIQlzhVbw5g5lrBsOVAhezA3f/I16CEQG2BR9fmKiLVccEVfEH7wyhcLa1iDMMHsW/iEnJOgbF+/VzKhCOx3jusEX5MyKPE5JvianX0AACstPZ8yt05obKd11jvERd0/Gf8gOUw78nDglwXs5fEdlLBNgOR7VKW+o5dX5mBaKv8vazcEOHuD/AHADj9gH+BGDUfUixmLPogIpT2R/gwLHYbXyhdm6E42+h6ShDnE0Y7nBmkdxFNXhMdF+OIWN7AANrtzKqjaXXecPHAd1lLMJPfmPZ1mChT5GJoeWfgll+hLC8ZnTzNveUT8sR94f6kYB6ItzM3TqBeuxMP3RfeKr9RUQgfghhDI2YeJm3KXXSVDOYwy1NmYBxbvfE1yA+vCOFsee86FJ+PRmRP4hfjLMmbfKfVI3K6wQjm6xBJn47kQpyOnqR4jtjqPoU7VDq63o4C5mFEEsL30O25rZslkMrXH+C89V2ex9v1Ho3oOKP2uvEtFy7RxDZOrDS+l04jj+gGKsMVMowv8ATtNPGdPj/iyYmq4m3MQojD1efRixYdEGvf73xGUGrKqXG+Q7Mx5uO8oBMrEfiXjE4zwb/HQd3Ufv9BAIAxHW0yq/2XxCEKWt7u8GX4jAhVsV5XywClRXa9JiIU1DjcCgupu7difSSbIQ5vMWYcAQ5V/BmU3mV4l+4Iqbg15IoZqLR+uRwY0rKyqdBVOKA1F72xD8R9sYrpF15l6TiJg97jBjMvQ/5/Edb903Hd8vSyQLyPJ/j/E+4TIGwtJq48nSELfLoxmNoBy5iRVk16Jco18Zs18Q0ZcW/fP1H7zSntRyiIWM+AZYf4Fz5Dqte8Nda6cmi/mLmdpDGNyn9TgLoaW/WrlUwd6n4nZjB1AKj+z5jHiZ08Dnnr/hgR5uB4j6bwE4nMuZLMHFQkseHq4Y+ctKdR5/EMH/ALo2qq4R/DJ1QNMNTgOV5/gk4oFR2Ls/F5hZ8p3t8jZeWKA4S/ph9IOgVR1ZfMzIt5ZsZkSau7F5L6n4T8S4A53/AIAn4CZXiYxVL0ts9v3L4OaWhHB59KDJcYWz9UuCXengiGrwXUvYUA63F0Y/2Ec0Wa6IrI25gxYth1lA3l1CWhsRIJLdLwq+kSqX4DD+WM4PjU9LbwLZbOf8q9UZS7AfaVFpQzgdOO8zidSbESfaZW8xTy4ltfStu8dJ6TkdPVGpBByx6AL95tD+Zi6WPadRq+IBcQxe62RBwfEyBzz2eno3QzNi1i7MH2yyPZfbNecQOuMe97/mU2hZLly8xDiyVfLP2gCqbm8IvqxR6CxzG0ZHDI6+0yiy37ylTZvy5g4qOaH7gQ3mPkhe4sfxz5vYlxsfaMHh/aiZSir7u0/UfG3U1b/T2YCwNva8soII9fMVctwR5HhESPBAv7E5JiQMGKIeaynNh+GWZPn63TZ1/vEtnEFseJkL0gNXMM5iDYGzXSWJ8eCWDzZ0gM95XktCgijIdz8S0Dj8hGWwYAU4lA1tnH6XBT+ptmuqBugjtq3Xds/qOA+Xjj049H0qeCBFbHFbl4vhiM1ZW1AtS9TkjSwuT/tLFHiG8cRd94auk5ehLEloPYJYtVw+pNHrdqrHBrJ/Ux7buuzJD9y+23LAVFgW9pk9SdJUFud1Bfn0dNwaBhll+zhl3+qFvhp1tm+w/HvORlYS+a6PSGH1BDcQeCI4VZefQKhLOI6Rj6E6AXKSAvCuTpG6WFDzCR/oMWxxeZ3xy30hBxhtjIehq3ipTDUN4Nehx1cx1vnI+D+ZUE9ZH07uPmIhgwZ5Vfj2ZjdyyixswlZBQR3qYdncyb5Y7XrNppMrms9oARcuozVZA8qf1HsPDIlFX1zHVXaE0e8VQZF/uUlM6B1YBdX4mQ0I62dYXbnDLr0lwYrOLwmgFDlDb/2adRb/AATo/eIy3kwGkHTxXWFThYnINfqCB2+Z7sHwR6GpXX10gf4cNHT1h4VXqDk8SjI0kAhpMdmMGnHEGsYuoMoDmui8RDeQPVWY+Jm7u38pv1H/AAtLBY7KotSlPHQr8bFeIAYxDSWp1Z4PePPPvLvmaBbyO0IPi5PQo+CPKr/bcYcS5xwsc/fMVq1fHV6Hwn6jEhY3oc+HJzDAgWaElkydJRXUq5zniKrqeE1jDYLrQcsbI8p+odDG78PMZCY6zZnH76xG7tRxK1sTV9ZXGSXmK4TGsAOqla1NtUli0ZjyVT8fMLmXdI8p+IVTGfadZfgv5mziq+ET+9YjFDhTX8MAAuhhd2s4qJkJm4O30Kpgl0Ktx8At9ap1+amVBsK6mInBBiW4RzNnvDR05lby7WEJibH3m5Cj3Ed45GUaYi7f4hYkWH7g7xW/n/SatZvuOIT8kUviDnYGf1F1NYMBdm/mdLunFr/3CB6w7f8AlFqMGI7cAPqKqOjLnXxDNA7i1BSzGbFYVHWbATgFnKM2GfvFYdBZcuXiN8q2+h/a5xiJTocS+A8EYT4ukc5QXkJU6MxIYNTtQL7uBXdVcRUKYrblmDU+uQgs3a51x4YWuy6THRe51+bILrDmyumvZl01fvzc+f0ymhC3Mq8mZrDUc+Jfpis+pyl4BBx18HVj4vcdWVu6+2Gt5X4gi51PPmBnhKNMF8kAfC/khaNA64fl/c4Zg1B1vXX5idOi/wDQ7McE289X9AfMZxyjZpX1RHLi7L9YKO0Wb4Cbleq4vvtEGqus5r1omDOPmCwpewgRTdl85w/cABWD4l2mjheIjhsPeKNGT7JYFUcrKt2CqIqpYodCZiAwdYephvESk3R0r1iF61r3ij0Jc1CVXrWD8sNkxbvgfVQWjj+q94TIFrPIP1/iw/wS6UxFCLLs9tSlujDJPyQbc+YlnsX6glsqdlr6SWje1MuzR6rZ0ZjALAwdP9PmKsdsy1qUSxrZUUrbW3rBUo2zDgbHldfqEF3s5OeT9QatYpvfmb36ERzhiAuRnEGUdyyzoPb8cSoJbIY+vvEZoPrv9PtHGGbXHPebaxKnE74xQWhtXEQ6CghKBzJwzc37+YyVcd95yYMS4F6CVTXiVWOZ4mBPSAHa+PzFQLvkvKfDn4g+KbDTT7lGWzJj+kwezG5y8zxvAUe0dOiREx7qmaS9AHEJwueUdcHmIntjtH91RBqMoVSIhm2Vt39S0OyYRHaaPF+ZtNYYlhbS6OWLTaVcvC7x3luVvwNA0eJuWb8a8yxb3TC4D4gCLWVXVl3DbOsy9KeyZq4goDkxs1Tpu6N9WFhncJrLmNI9xYZZEBXFh+o9wz3/ANEVOrh8YtPv/wAr9ZVaEHa5y7y2MV5egVMrphCGoGklMFZeDzGp5V9w4epuV6PLdQi1/i4BY7sH25cgRgS8AeGBZTY7EcErqvg8/mXN5Q/rcrq+WgquZZJSqq7hpl0IZPQNOTMqKP6JoWx5Kclc+JlVY3Evl9POI7enOC79V1/5C2tvC9Xc+/aaYKGtx+piJjHoa2CO4LNa7RPOlHWGyHeGYCHm9iZF1kwugsr3lsDXED4QXNd4nUQyg5h8UQe0A1j5C+CA6GkOVy9lfEvdO+rf2zdj8HUfmA0v9bd4a0+YCFq0TcEKgxUUfPR7kb8xb/xNp/57d8ZnsgeFPXdYP7iZ28B5dQ47ufEfETg7CLLCxfujM3xoLeC6r2SPbavM5larxmpV2malQvhnsm8R5AdSz3hhBXtTVerEByxEP2K82g4TBvrMBMvrGVrZq8H/ACWkumPCyojJb4L/AHADtwu2P1/4+8o0bEmJnaniChzLZR45jntj66m2fTAqCa5/a5pxKuUBzXpzKPFa45Cgd7jO6qb1HAEBbogldB2DcsG9gDcuDIG+Sm/aoqKGaWOzklqpauacfnJNZhfXf3xBg336+itzFayCyLMgNMNbvs2RSV7Be5lQ4f8ATfx8MMN+tcpjytD3IBgbL+HVdZQ9Ee2pV8x0PEzl3bNnp/pigKoBBu6uvfmNLkZ81/LHY4C3+Jkdv8yncMSvSGYkcv5H0SxI9wi/weSF0L2oj4iveeQCDsW9rZ1c0OnA+JmUvGXmUfKMurI2crL5HE2M9BigcfiODb+0VAncc+Z1y6WHZNC1brX3nzNJYqFHb8tYmH4fmBmqn67+5U61DVPmDBZeUooz35lnbs9YFoOEciGuPMxA5Nzose5AUTaoSmz4P7jXJMMrSUc5lsFgqtZo/KRUPOvSiv3GCOL4MRY/kqd1lw/8FqZyWEdWy8dYE01xKsHRYLKR7xE945hKUD0eZUgSkQ9Tz1gWYyRxLBagGVXUVouHe90cXfsYrczF0B6X1+4mzRt6szWGXagXxb8JQF7F/MeFlVG/e/hlw1TFnVLIVe6rP55mybVZiODJGZZZ06sSwWSx+5K+xOCmUELvqalXJ5NMJyq7d/l0g8KyhtOzwwwAWDmWJmw6kyNPT+5SUZKPtie+kFdek7fMUIjADHc9/wARFeTKuhxA6DN7wgt3ogbYwuoblVGC6QJ1tsG1FekHU7i+9Ex/HsP5IDnhmUOL6RIYJzKbMdSV2KtJzLR6hwxdEO4BbGm9vsx/Ro16jXhJMUFrnWV/UEoVd9xgEgBgnOfQKM8zG3sQQtucXwS6WAo6m5Tfi4KB2tpBacLNmxsh1NG5eYWXOSVuU6WlGOQKGkDa/Z+YLW5rvKn8RRVtfzthFKo1ePQ/8AdAtBkrPEa2vS6g7M1AUOGPXaX5enHoforTKgOHs14e0XY1QPINjNkvY+vGPKiwLtZaS/Ae/wAcy1yuzCO6zp0na/EyzFM/17wd2NfQ+C4bbnO9y5dyghpxTv8AJBtDe04e3xEeb0Trf/Ygq00dPKZXaKHPJ7npRNX26xLVVQIyeGUin7k289ZufhTknUEZRsWmBStteP8Ah4hqCQ5TwsfI53Ruu4jZ7m7ukx5lczjPL3iWAm3v/OvE0W3ylQGuqKo4fuGqvJ6sADARrbd2Go4n4StdHaDA53EAqJ0wUfzOsXmLqJ09Kp7TliBZLbQ25fYjpt9G5zAHLsj9aoKoETfj0FtTZ7pC4MMsqn4gpzAt5Z7Az7w2qHJ5K8SmbilwGSA0EuzoY7y6NNxWbIq4rXvG0gyOEe6foipxQGayjM1NMCk8fi/8gtkTLPD1e0yPZcCF81mqjdu3KPM0ZiWGPo2UxFkTmG8zq+i5zfhiUuGmHIg5gkcR9hW5fS7pLigVX7GVYGgbqupfeLcAoDq6/vaYeMd+7mNh6OfMXCmiuqhBGoOsNPbKUiKR2Q5HPpirnKu0qm00Z+v91c4X+7xFV4XGDKzm3f8AZmCA7nStPm1A39kYRDFO2n/W3WGurByYDWxCdO2rDpYAsAmosehDCB0oYOAPYj6saIdcvlnO/XgAVuzL9Et4Dcrhfdr5l06g59aqFqVg81fUmTiu0FCZWfogWcLpGytGx0mp3l1NO9y8TVZ6Q3ljLOlgF/liwume0DCbi9VfmGnZfzTl6nDriVrhWXzOmVTv0mbtuJUeUY8B5T8yt6pU6wWKHTsCxWRyVjyQx7eg+p/heZhMabl2XwxSCF1w5IRDRw9od6dB2gCnVyrx8yya9bXiFgLRBqW03FOCKlJyuYL5Jbk7ZgpMsIXZXbhacn6xKqtm+9YmKs1fDuciYddyJRH/AEhG5QynPEbG5UV52Qaje27GP3gw5vjX8kR5kvL2enmUsS7GL9pfjQatUH4OTEVkgprhF5U6TuXsYVysQ5q43hho1X2Z32MIMHwdqur3macltaeqNkBRdwOeYzxC3dbytKxEpGBri0JogJUyRzjUxHkqNbJ8JddIFdHFxH30SpMFZqM13Qm5MU+V6swV3aoeqA/SFXDDbvMc9QzFl5ekW+pbDhv84LxlwhijwS6ApuXKbxHEIA3Q7iprt/PBn9zhADA50ZTXeArwnX/yUDy3mK2iIRvCfmGrnWJcgq5d5xHqJZSNDPMr/ALQuppdkTkLh0Gi2+xLaBQKLqkAnIgfz+iXssk52RfhaqRqi2JjLO4r7yY0xzBqWqdckOZXpY6xvCPn3/o7y5VIB0cHqRf9heErT3h4GUc+zHYK+IoNLQwwG4AwDCQDlj3QLS3zFYt4BMTqVjQ9Paedyy5msajH10lY3My5idMy9OGdzFlyj/c0s2dKi4UeLbI7t79fUJ0ysmZeWhLB9kALWWD9wF2HMBsgOGcx2Jst1aiCrvDCp8V+I4lVJx/fiUN7KIumBGbPb0JpKFr4JcVDdQFa9ifVg6pZZE5565/w4h/kaxdJn+6ntCfxCN0V10xOnkBmKnV5OPRHcXoxlla9NV6iyBZixl7F1fuhmFUDuxkC9di/sV7EZyak+b/MXdxX3lhQvo0/tww0nycTWsQFJwzxTU5DUfmbYlOYaGW8Nn7JsAFd3jxLBUTW5dO23tFNgvA8fE6M8Gc4JoaYVmwY5Eo2Aeic6V9zZnCCz3llKNdOsH75z6P+GkMk49eId5SHeWt8kzcxZx6C2VVGCHXI9CPYWP2mXvTuGsG65VPPl3/AgYWdCYqrDPcsxCc48RKquqh68Sqeh8sNdWRbWLamxOYTrcX3D9SqXAPPSkuzN/sJSODZ/wDOmtksY8xwzcVHfk2CNBrOpu0aq9eJxDHqFlGQz3nfDn2l3ijtR7HNwYWdV/EPJlQNUw/C950Ff0XlmjDstKYjiU+YtXi9XFddT0HA+zEuw1kTk6ysd4t0lxWhjT8yvAl83jxOP2E5N+O0+IylK03jo6nU9yCT2XKaXeNrdJqtS93p1mzauox2PAYkFINRNZgUejr0v15HSbx6c+nPowBDv07scSQYO7t8s5m4t1oiur3hqMKuehKkcVG/dSkRa0ozcp6WSnvOTxolZODg7yzezGE4KhyrYUO8SuBzHfAHmb90eXpmGcMZmEDllgKP0xlt0+WYQaPk7MGX6X6X6X6XEAvUosqXhqUIXd3slhYZTfNKfMVoyDxNOcxZxqDj0YS7ClOYrDGV4YvQZZdaMgUDWPZjaiUNWjB+Jl4XwfR+4QKyPGR0xMKdJYLjeoZagqYKudh4mzHmZUd3OL5JsnDKvzNyzlRfK5dpUWoU3BEwW9hOtP4ithwN66B0ZlJKmR4eZbAQaxHmAIK72pmyGCDK9sWa9GfiPqy6y6QxccRgxn35gyKMXuRrhrNudxfTTTBmxGCmFEtIB8m4DrKBDXRMV3YhPE4nhFV8QCdzBqv1fxDKplDXWHI0qoZbgEA8p7JZu/0Uu2i2LMYJdsW0FF1zMoAfpEE+gPiVbrwXHlD14/zSpevEbJYjNzkJkRwkyoxcdxEze4GkF0dY4w+tUq3IeM/6iIQifHMb1QD8j+dS4mwHTWGu1veINeWvY/5NldR6ZpbzmaMd+U3rcwd7T5ZywsauFLsqmG+i/mGEtMwx7ygvUMQ/EqBrFAc901pOBPEsTQQwKHQp4AKq+PKKoymTw2fxAiDidKJiQIbI55yzUe05+vV/x5KzOY+uK1DStYSlptFzM4MHfvEUDmV5C1toGwh1KgqMH4luq3A+COwUI9xiJfZA/UxGxHe1lDbdCCmmOXzCjXIw3qAYaIMW1GNVkL7OhEO6hMVNF/hj6f2goWdQUeIKI6ESCt5fL/N9GE/HpRWqiutMsIuCk8YhBzqaoK9e2gB1lrLNDuv8rDk1bLVvGXusrW8tlX/Q+UObN9bvKFMi+52rr69HTKjHCfuC/wDUrydVBHhyRJihltU8Tgc8whhMobTmOTvLXpyu55IcgHJNF7dIf2MQ7AuCI79408dGKTuQBodCqq/iUe8d/HmczzHEqjj29GP+HaO9cR4i3iV1jr0MA0WUfhLJjpe0pZjNKCwF82OZkG3B5hAusn2mnuS+DmGzXK+Ea1rGeJaZ2k9qh8RSpDEo2wZvGiaAcsQQlY9yW22YWSrw/iUck0j6GILs+2X8xjgF4zWicxUdP+3/AJDPPo+mNj4VhT7jm3MxteJhELglq6qltly2vTvMvErc2wqjyKaPzM7ZKa4H7ZcwiHVgfa+0u5sHr6zLpVZvOra/BG+N9Ex6b/UHfEGvJuNE0G6hzaU9ImCZh0GzrBccww5mT+5j5Gqg1aOzTqRC5XVfdgpLS9lVfz1lOlTRg6kpJfkQl1AFzdD+TvHZ6MY+rcL5JecZl4G2fmNzSBfPbiIKAqUZ13m2HTWDE4Ys+uZV8wiTQFV+ZRNcnXM6AqryzBOAkSuY+1nHDZIebbUwJ8zdffx6ZnsjVKpVysYt1zHcigdULlTfc5nJmNhGz0VP9xW8nINbXKlUVpuQ9ePTmHPowhDobd0qEZV9INIWJ5Jz2gqM49Ypcw3frsTo6YglaoU4O/qHFHOxxbL2qODpsNp0X5m4jtHD+bgaMT33/E17YhvPV+X6grD/AA2eIaPUVk2Y9pd9YbqIOWmJrxM3TpDA4eke3PSOD+qin2gxlXXP9w94krVtq79o5UwAVnN+XDHltF2K5/tQkmeO+/sfUHVdrP436jZDwj6Pr0jwTzFlb9LvUq/EHWuC/wC6/c0PQ4Vzx+IjwRKLVfZMtyaxBo6FNQy81od9/dBkuX6JdTtxYBTZ1IaqYOkFinFRlmpjZLPfswF3GAjp6yPd8ywF1ZzDSOaJVkW/YljV15wr0tCwoumC/wDJYM16XG4lsHejH3GoddHcp7W/CEPImbqjnaG49/TzEWswj7R3LC0l/Bs99SsCYUbUwr3+8MlcoZGfzkVHP1Rf2H4sWG0C0+h+JRLhl3n/AGf/ABdnSZVvOYFfiETM2NaxY37QOmTiDy5UGsOZq8ShzNOrO84FuOqC6Rs00JslRwI4Wj2eEUrZ2a/p41AqksW/J1IGKdgH/cefRl1ua8zzqdGfpHMqPX9w61K93vA/mY+OAaHBGP5TChdtuhqdagHeMei8RUqAahru5m79WYTtwgvt/wATdoFRwBo4V3Yzt4KvjU1RVtSj++ZcH1295o+JZiVDTRafhiy3xOZ4uIheyHSv6mIV19z0QN2h8f4X68x9cw89cCtPpgCOlXOvwWMYCrNVXWK8yrZQr3icIEad942MebmxOZrUvb2Gn8xEhc8j/sPpECYJcW8cZIbtSW10v8kG6l7n2D8fEyHabfB62XXPBFP9Qsf4ObmV26nlco5z4gzZtgj4jPUOkKtrEqsYTPQMqt66xxhigYyKNjBXdtxVSwcMwZVBysvd5eYyZUbtXNcRqzfCvhf1i8gD3pKfj03DPiVe9Sy0G2iWhwT8yNLu5Lte8VV7Z3Li9E4m+JpikHz/AKlHTtk7OZmHUO9ysXtM+IXZtIHTCpnqgIb1izL6mVjkvxthoYDMDq+I3n0uZxbtx4n9rtFDlWHdg2UgFaaZwIa2zRgXjtNn6VNMtYCUoMMe7+Zd9P4LfQW9uOTv6q9De8QfUniMYKOfVOw81fzKPqdgsj8kE0ZXufMW+ZtjN15hhxGs2i2zIcQU16GyKtwxsL97mRPMdNyZKCoS7/UQoelXY1/oJoFser/Cao/Bi/x6LmiLnhgXs/x3Gg9yXRvpKQdJli+amnzLutIcYw9YYZlup3GIdGEi2jEN+Hy68SgaAN8WUkmFWVZGWcMHD3/tRIF7MRWxtbd66yoaDY++hA6N/kv4mAlNqJ2P7gQS2jle8M3xCoZOAijVjbbfR6SwcCpta951JXnhw6xsgBm75iNC6YroFHsFuSqDxLFpaoZzKyZavaZYO4R0JcTiC6JkhVOFTG1ooz8/xG5uFe7KbmMC5nEV48xuM0YPR+2MGcPlOqSZlBLZUzA6ShFbhy/eZZRf9mSFaolDxl+KFrx6U6Ws3TZ6v+A9f8Hq5wdbvPeWYCPzP6IHMfBgpXxBjROmkhUB95T0hpVqPoSxrMUB2mkta6gv6Y2/i7SmOGhj3/XWZKqzcPDXdntFvGvzMnn26QOef8l3Gk9k1dRqCHUacxKQYadflHTiaezK4fEx7czNmG4fvUzEEP8AAy4NqNnAnaXAghTzcs0PDiIkUokaRlbg1ZV9tM3+6cT2jHtPFInlwnS8VAvJOv4l8+F2/NSwQFFK7gdQtXXa6XtFgMq8LmDDi0SndYnKwQk0UtWv+JYFkdanEYN8x4iiesRTS5sQ84JxKAttWs0n0TcGBn7TBTku+3E7Us95RHufPrQs9Zgc3h0heMbyz4IwWLL9phSZMA94qEqMG4Jl5MYjbTuFLKGQ2YeIsbsa/d6B9D0Jv/B3KD64Kj9M1F8tGwoe6/GIWQMe0U7Szsy8soB5MS5g4dZbU4nEITulip11mO4hXlv7IP2CmsOf6jXFlvPjH7ZSxcGIKALA5y3cu2vcwAKJv1zLpj05mLmiBoxW5gkphB4IM41p5jvzDZFfkhGLd88wPbrLD4jq3mtxBjiZMmJQWDF1hri5mJwGmX7dZnMa95QgTFiRnrbIpfvHso5gH9oZRKzAx7cQBzpr8l6nWoVRQJd8ysyge5mCkZfiZzbjEJiS6hXqW7dvxMPJCBSVErPmzLiVQ9sS6qLst+WZy7/TMG9AfglFHiDKmLuZR0PVsHShfmDPdC2YX0NRwO8qq7vSc2lmXmWFvzO0VIzqMZKPrn9rMT9vr0WBzXt8elR9K9b9TzXWF7F+Fbm4NfCF/Y33io1YN7TSXtlssZmLd6h5brEOTmP36IpuUqGlxTryD0f0jCnO9GSl34jzuyt5TMZGBhra/css7WbkBQRWiswKj/hs7QrzRfifmnKaS4ZHxFcHzF7m4rvDTs/UF3zNNReZ90qqIia+J4/5G1yxgEprCDzu8F+HNVObtxAaq8aBzzzEwUUB1g6IyVPQ5eJ2kc0CoqnrcVe5mrR0GHz6VC4tjPtMlNVAaUd7lOGXPxF3BYOkbBwUF8ymFGuP2gmmfV1GYgxjBm61tMVthMBxeJUdHLG/AeYHswUd+fTPEIq5QVDLuM4iuF5YkfyRkC3t8TVrMfCK03vMqW8cj5Y06rx22Y/veMeOf6B5i4iw2qadcH+Awz/hdwljrxZwmux2lf6XGdL7ineQjFP7KS9q3XtL+JWrtC6DGYRgRbjOXrzAzjWrqzm/YZetx3nF+4fIS2Oazf7hammS931iBAWQe8R/aEn+K5rmbKjy6mZWa4dTGF11OSPL0amK+JoLMwPmY695Q9ANTDiJEs5m4/KIlkI/EyQlW5KQ0pHMDHrz/e0u19zOerzqEWawwE6C7gWcwdxEtGChTPiYAC7ZRDN9feJgYV+Y7b62cB7Q9B3dpKjXQ1mWq5bzcqt/JN3iVnLL4gBOIdmYuiSq5xUZl0PuaPXmVLtOZgOpcPyEsRQtzCoZynxFYq3Dcwft2uC/2kpgpwq0h/EIWrU+glzYxwuD1J+P8DEPR0Y9usnxLng4cqh8fpBoENk6uv2S4PnCVALwp6StFTj0+Ga78TFnK2mlGdPKeCxVn1xhYYS9AzjkUV9Sq/L9F6fUfiX/AMhKt6oNkwHSDXti7rmao8nSGPIM5Yb82GvciFridYMpMNwD0sogywsDGFsu1738YsUynTUVCDDiW6+xUBC6HaIqM1eXfiCIel2IQBfARAdrifZqCjwTR2jjAdBhiVebbgu7hpvXB++JSLFrZL+xc4XKVvXK/EGCUctQsFXK1j1ZHhOt31sQ6zDylCqC64mlT7R9QXfwgFbzPlDknVyzR6dZZuONS/q6CBO45Y57z+EW+VsKvkZYpKCj4jcHSc6hCuS46Wv6jovVez/qKiZN9wSu48hx6D/Dj/AjBWAnyg19/M2nHcipvxDvUxebAOOm5s+J4j+k1UZOZeKmYtS0TBUJUBumPc4i3K/fra4CUAsrof6QRoifzjzMAS76PiX1dC/l/g9X+nry950Q3OadfUoQHeY4R1F5p1KgxzDouot4Y9BSla8TArCSw2QxsnhhTTR2XD+2wmao8Q9GyXFWA0dJeMEg00L+Xl/M5Z1yWNaykGbzkMNHXIa7Z1GnacbYepOuHcd+sYY0oOn8yqtXZuxmc9liEwcrVcQoM4OqUDDwCU78SFsp7yRpBOw7ZcvI6fvMnN0ff0KwfKEZeQrfpnxNTDPbSuKOqOmuMGMKsXfz/wAjq3T9pbjqado1ipQPZnCgnc7DMg3X5j1BDesIz7b/AMB/kTD2HDReP+ky/bpVD+CMaLMXxf8Ab2hoZF3pdP5IBUq8/M0266zUcehYvicftkx8SlsE6GRR2eYSxiA6G33lvIsvkqPj0iDFLE4E90hV6P8AD/I46uDSzDE8DMNl+jwmSTt2n8yz2RoOrErufuDPjBK9E9Ke0p6oXGo1vRm71LZiVKAhVzDnkmkX2WKo3FmG3eAdkRf6TcQTVsL7JXBvu4eYdNTLTo34ifvHdgHbkXyxtuBrmWwp6OR2hw7vBuoJ6HR0sbay+6Ooo/LBV5ep36DmXP4IPfPhiZId4c9Wv8LLrmdoVnAx38y6+QJZZ0XcyrlIsOafcrfDsnMsL3j1tiUqY/Wkhc1835kzHs6rddet/wCRqEtUczUd3f3Bu7C+KYOHtiX2e44Q7pqMEV2BZYHpWWANNWqekGiPiKit9AuDA8hL+px0CqLvrXgjs4G+RT/EBq5qw+H3NnOgJznPiVKrGMliWD7s59Mc8z6iQWE9YUSGc3uZ8+l9fTYwySiyjh9qY7PaCpDMWn0sadI7CHH91Nj0wSjfP+Go/umcjKG4Ael3c3ArdmCCfAvsToKJwZsQ5HiLU1faeImxNn649njPA8QD1izf6JmaYYJjnUUWXA030h7c0tZiAtaYrrLrLdV2Za0unT0fQll3Ffqddd/OZl9fS+3pzcp3I/MVM7z0ImvMZQuipYXFj/EBZbq89YdxFxubQsTXmPrVb/Q4+ItnFPGSEUFnDrFv+kH/AMSWmRfRjuJIngasp8EtfmUewzUTSPlvRaX3yTUdydRdanM90CuApQzdi/uFips4R9T8yxF0dedviAOzOBq1ylm7ru+h6bmCk8gtu/uMzTdvZP3Gtvgjicjo1/jU12MW05DUWR6Nzo7TZDdwLvul6bsxHNfELprHq4R3LPCjrOvjqZmWB9iNxjrnVS49isqxyaaUpS+GMRIndBtsbiQN7/kjCuScRtWQLu5oDsJxgiZNdKiWsqOrAtOhKYAEG9N/4Eo4ZzmIuWZ95UfS1tGLVXOaiYgs7FmQS1i+kdv2hyP7bDZqPkYmxeNSlbxFbo36QdsRtkGz+8zGsFB7PQm0U8Ln9/8AkM//2gAMAwEAAgADAAAAEKs/kTmuLQa5jJtgGiKVe/UFN9PObFugA3Mg07s1CsQCbKEGrEgP645L/wCtH4Ph9A3gj/5MxNZS4ZvXUnnSBYmwYLc7Ux8/FBE/1FkhnQ5MvOOJWPoKL1OajcUsSqVRQXavJo7GxH0tKPW3APJNrvrKPOIbO8toEGRM9PBh/WtK/wBSDgW/+aIptSOy1dPEILVZPEsitNmMXVdo4ooelaJJJXo8nHOuBdZ+QKaChV5E4vN7pkMtiXW2z6DPrhGV0eb+IjUf4dQsp9GbuVfXapprvxWp7HVyxlAOhm/rfHDvnbr4UU85EJzo9ceOXsfBYpv2KZo7Ck77frxN17elXDPn4dFeKHfrrAIMm9AJf7MVwXIuu4QKBEXCUMpXeOOXJlYN2iiTp0ZxxTyQ2QQEfAWPG308cssz3CSdfzk1CAcwQ5s5fngASGeSVbfitHXup2k6yrPgOwAwcYpn1j23tLil1uCJySLwqRC39mfVzWwBm7aRg5MiQNOmZZewTW2jee2tgdxMNWUrpmaKCSpomN7X5ag/G+7bgM4vPaJcbtr86WiFtpqYXd90bJSSCCSS5wwVM5jGlJmUFg5Wjn25dZ/p3XDFRwTkuS3qUOZSyTCiDCDQdpb2Rys8JxMO7ypxFcbcxHnG3H1h01qczJk/uLKHCHGXxgMgj3feSsCrOpfxMgTeeFTJBV3tYpCcxy61hPSuGDDh3ch/I2m5JqvHq5TV5jy+kmazJN8+F9EiUmY7tDxMD5dQCzW85y0d5PGSOqozLsJ5Gmn8PH/pF47xtXDX4TrabR/ECHIKBxUUt+lfq84q3cNhIBwMnjmvrxk8qdIIbdr73NuEEfsMIULKQ4yE70zqypQcn04tXqpVA0O0ahKy2mQp5N0yshHiApmOGJMhIpurgeHY14JgbkBdzVO9pEln6+QzeKpCiO2BLbYobW8R51OqEYEZMfCxwSdUFNOYQkn+UtX6mcQb+00+x9ZboYUX4WMp3W0g6hyF06xiPrL4isjinTiihbb90NSUvQv8NRQP0nklMFmSwb6QALrpMj5ZjUTiIWZNye2b8QeuKBePm6ji8s0yT6kq3WCmSAUWUXJmGvCKZKoz7ch48GF9z8N3fsBRBuFm9r+WOOTsIzGbbnGEq+Rya2+KlR+aEvKnWXdoU5WjUbIv/wB2lRk/1LYP3cRd5wZFsWE7BahVwzQvivLRiS7RCSkaYgbiqE/hDCEo9upVc7fxZJncmTuenY9Nz3sq1EG0CZ/z81P27uh9hg2qqk2oIr+o3h6pdtTH6od2qx9703IaeB4Jndu+UaavhpP89OJ3JIJvQMK+zvJn5khEDbxKjV0OzVaoQLNL4sT6p4c1t6+TChKmevfR7NeVEWzu+z41LjvM+5tywnWc+tvxSi0QqXyYN+MtGWNhm3IpPiXDrIW7G2qtDcDy29Evayw7wxJ9lmk/QOgOv4ujhDouW0voyNfhIIKoNPfWkmjJ5IJ9eXGVJ8ItswS4m5ihvC+imDvrsw7AGlX20ihwZXRSgm/U/CHi8rEKWOiqsXUXcOWB0cSKb5SGmFS4urNHHcTBMrdRiBqYS5NMAm1zD5/j9ut1322EJ0qDtdUEHn4vB+Im7cnL6c80FROGSiuuATxVdGhdu5PAJyCE6aGVBmnxkJ4Zc88L/EcdxmvENRO1mD9/gI1zko/yOuggdm9cL7kCRtKC3KypM+QmYn98Ojkwrh9MCOJutRj4IgKfw67aOc/CSn9Y1GfiGSN8/wDBRw7ho9shQCA+67dmlYGdAllsVkvFnKDQTP5gxIFQnuK/U1HK445/3FJhBj9nz0kXOqMMEG39Q3IDgz9gFgcXZD3GRoQ2w/oYHITKKc3lUGD3AadfVvFuvxREbT+Q2WIjmI0oGETK7xXUIbDG1OwDHJOPKaOHleySc9ALGgxeXF7F4au1g1KvR1HyNtS5uG+P8uDhVic+OhfMmL3gIPhBiaEZU6q86AjPZ5HAul2UPSaLQyF0CWtQg6C702O/IG0Ir4w/CKDHBlVGSTzG2lwGetVUTuXg9xqDWHIVBY7elP5r3iRXn+m3P0uVikTXmONCV8NPRxiX5kgxPJCYHBPSDuXTkTFVimkq2Qc+EWoYMfGBQhT/xAAoEQEAAgECBAYDAQEAAAAAAAABABEhMUEQUWFxgZGhscHwINHh8TD/2gAIAQMBAT8QIQcVZ8nhqdEIECsyHfEom22HmVXni3Qc2ULzvPhrLarN/SAFDTP37mOh2m4xjaASZia5VsCMLYRhcOSX1hbDEBRBOspuWduUyhVUDezB559IDNFKKWtaLs2lNmYsaGatFWRp5XTWD0L3cVeyXHQc+j5oFHJKlVAgcGFaIDvPBMSqs0RjqIKvDzcuWDlLMNcna/Lr5TKoAwy3QepSHqx+6rO7eWvHrrCEEVFxHJHqaMnfc8T4h0ct3HzAW8s12bcs5Itbs/QV4LW0Brt/Pu22sWV0nvoWrbX3n7xphUyTgVKuA2giVHGEFIEohd4NYLGoKQ4dH5It/mspjPxFcB0E8fXOY8yOPQ09BrPmEqKQXlCmVwrjnCByGspJO7uX6mNuovRdTTPSFYZL2UO+u3rB1tdAvQW9s47vaI0tsrzd/W4Bg1hjluvK4ttstEqAdI+jufJ5bRf7AFmvl5Q95EwrLTyOLOZDhMG21GV7fcwXabmg7jblf0mAdONTaGcKQtDkhCZxGjDE/pHSHvmZWhPKL28hPvjEBWpEiiouA3hZQYiPLBNWD0xKlwtuFQ42s+kUBVauY2v4mXgMbOc9wvGkIRpaHIsteFNOY7w8pBhzcnPOB/YRNdXiDPrcw5ZdpqoiAtmqzN5tOjs/vpcxkXunMXy2XvpKAFCy3e69dSvGYJY4011UwapXcdqiaIt9Q+Y1gqlPJlLgRIPjl4oR6IqCG5vMtW1uWu2OFOkAxZ5zqkTzlDWCaMVWQ+jESrTr1/UNXogiifhrwGpDQm6vWi7vzNYBy50Y0spycu8Cgi15ZN9sg2mgqg0z1vXGnrKSN46veOIhvDRV54mV6oyNVrS9gzGhUsbuqWtu4VvKXLDo3YJ2K8lwVECUHGtNbGteUBBPMIm3LvMgua9BWvOmBi4QbSHGNFsDaWN8EvWGgQTLF4UPH+xWo9Ycx6COD8H6hoseB+oK1bygmixGhlfDSaDEFEehNbunZEhaesZsJRrEuH3/ACAHFs+d5voN+HOBCyI11LEH26ZlGdBjyxDPpDDEXdgaFff27xK555QLBbWTkNzqbn+yoLRlQ5NPTz8IYOazloa5oYvobx9VJ61uxtbcvHSFWml4ooUS+4nW4u5lDis3fPlT6G0RMLCvC/7cMoIYhANeBAtjuIVdYiHoiu7ijSHBUL6/fSXQe76TrPp+poXx+ot/h+pms+P1Gij1Lmyj6QtSV3hLiyXFxW1U3y+/8hdKW5czmiALGo0yQI+JdeteAzqce5tnlAlcAN6jpAZaSTwwfPnMBjqOu72+6SoKZl8PTbnAsXvUEIO+RTUY5MAK1aXZrXOuUiKXvQ1c19T2xG8pSvOgthXRfbpKBi1Bwjz8azzuCPayX2p1xZqVMFnj/SAhi2CYI6Am1FjjRHeiK1OV9I8hVRTejlABRxPzQcMVoHpEw2h1iKyEKJYN4xpy484rHird199LvvNBahOpTeLvSd4bmX3stouvj1lylAt65B0Xvj3E0hkKrtjpR4Y1L6r2F+KmiBrMFjKauNrdHpC/aAXQsuqFHOM1nziDJa2erno4mgacufSvvxBXoNF7bnhiue+SbQTrrrjX+jLSmxvr/Tf9zDNZzPvtFxZLHtHDEWOjrNsZmgQtKlfAv8z8dG5UqNFxsVE5vWGgqzvv+t4q23QHjRbCmoge4TtKdpYbIoDaB10Mr239oeSoq9n/ABrgxHDm/PX/AF9CFXXWx+oEvNFyOUDPT1mjaysgmxr4rRm5QRkut171zddGLwICmuqZd1xVadJUCWJzitTvs1XWKEzaz0uzLiqHTbtAqrY2X1MPhekByPMwxwNsN6H+zBjiFqhhYzMajqbTUOsuX/wPyKqooBguWRFhiaSwry+SKjMoNErtMxgWrcuhurorjtjDK06WtuaLdaXKfuEdDxq+/wA5qS4RVfDEwOZdhlbVMordVnnLByE3M3zpjrlltgKFZrKZ6aYvlrALKgS3NiVzXBbGJ1EF8k2NLvziIWw00U3P14mjKw/Tpt9xDyJob8sPh/cy5wVS8Nt4ZDSPg/x/YeXCpXA/A/4OjoRwen4AGnFFWxdSfSrfQh4LS1jbm3ZoYOqO03MB00OazrR9xFt7QOYHLblEEv7VVeOrE6bwx4wiJXIlBGd76C3XZW69d5RZNnTo/wB9ZpwPlDKi3sNabSzwFBg2v+VtvAoYv+fBGFstejzOnPk53gWwN/74+sdtHC0mgeMTB0gBRwrhcJX4HA/Eq8x6pqt+H+kISCmjjXBagEFy7SjPylnZw78u8a1ZtLawYzk3y1BUClLDhMdBqr16HNiDYwfefOYOpKnPSDZcs3R2VewawUblrq3z5HTxubWDU8LrUzbvB2A1YWTpo89/TSOEvNZ76N+E0AMdFd7zpXh4wBbS67beNbywKI6TEjjmUPG+GOB+VfiNj9uKeAjnd2++neWNP40dYbHRP8/u2su5O1joBvry/UVM9AAvk15POVFkLPVDxM8/KDprR45fXgm5FRheNffvpL9avLA6UbHf9ykWe6vvAZfNgZBoexYt6QANEK/3UfGFVgnk9On2naF1VPX4/wB5S+CBWIy52bQgTRjxxHgf9A70fgm+m9sESogE2x99vCFDvr+BcpvE5WK6LZ82ujhiOHQ5Gq7tHZDWq2z2/vFmSOKlAuJaKZw6HI19VdK25cKmAbJhq13zscGGsqW85hl+v4VxCH4n4tUP5EKVJrrpdvmzegslE3frP7JnrrNeNXiWxp8uQDply0PbrMcwGA5H4iMxLrNKGLiVCMyZjUiQqIysxPcDynaVwvhU0h/xRjSNfkH7jjwOhAo4Alx1nSWOPwCvxs4NsRkIuFRUQpVdCXDK3lUOctljPUhEkv8AAmv/ABBWiW7mPb6fdYcCsR16s3mGYlNRppGmnr/wOF6HjLnMs4g2SDi4XDHJcu0jNzX2o1YwxAswkS/mRaiJL4XD8jiwveaoG/6+7QLYFYhzcFtyhKu9TH6+f+JDhgWy4EdcEpGzyM+unmxjLKa5XOwfuMmopXIft35ddZqjvEQX3jUmq+/ekaRpbPKE/wB+du0vS0af6fbjmOAAbPaWJZKgXFGv4nA4LinPGhfhr0lweblPARz8NBFdvk4sXCHJkMAr8BoE31y3NL51nzz7QF9JRzrhq9rvt3isw+FnkAtvW98XLKCVzL03U01e0yd/Y3T7zu+kJsA2xfjt5S5XhC0qCh7j5H7hmCDGwGPXCczp97comxe4+GKLj1a+HOXASp+uksY7l5x4C84cvt6Vt+JxQoImetS6Nju+kRsrkcuUGpHXhoCJipi8QFuuUqCZrIoxEWXDgbZgS1WqDvUGhdS8tjxtx1iEkwmbt3LQ1K3oIzpLyuqOxr4p67WKqc6Z87+9otAtevwefOB5zKhAeTHmzZwcrnzBlPtc3XqbPMfCYarlq/06am0PDtaJv2fhmlOkRBcQEBv8A4BbOgKt+/djnKV2Ne7Y8PeLc1StYGamrFiplAoDl8kwXFDAv2j8WFHMYw4C2GkIFulh7X16dYGizXWj45Sp4FH5PeV0Qr0LdcPV/wAjikZ3TF+D5PnGNnZrL+bb5jFuINBl18Ibu8ATSnnmvSDjzI9ljz8/t8o4K1z+Of3O8S5/Udvk7694TR45O336Ri5iFm8cTipHf9WLu1zfXXyNf9mmff8AdYL4Ax4QJpGzbLM1kQOCq0j+AcBFZTGw0acrqttXTQg6o1aY057nTeOYKFugL1rIaYNa13g1NSsjeubdMF4q+vQztJiyMd8t0PIAoyvKDQy82sv2oCUauILVPHvjNH4NoriUTKv9dzpF1dv3t4xOJUDa54+ZYp4DwC8RyXTQ6BV/esvHRsdOvV3lQwVFmBKhbLwyUhmuLDgQjlxzNzFmVcF8nS+lxrBrWpbT2D0OukabsMuNXU7Y5rlYMYArSLlNKusbBRqbbzOWerPMh0za6s5OOh+oCyZqOBqTJOlvv3rGG2Qvmv7BqDf4IMuzHXJ9Z8OUtGw5Ho/pr1jtHUjwOG4jxVID2Av1NItDiBDCXNcczDMJe8tl6MVq/gcCEd8FkN/WbWoVYsDXPiBrntBua0cig0Vjledc848k7u6dfF18OkaI6BSVVYq8N/GJWw2x99pqxAmAmn7Z625cf5HlV9++UxVDX75ecdTbU7cKhwyUEKGw5+B6ECw7cDS3I4XwCOFxI2mybV+/V4v4EFtQ0cGzadB5c/AadUIJgyz2NDzdxzZ0yqHS550ffNl6XS68f8isMIh1ljFcn+xYETEP5XFy1lDp9++kux9HPviCMDhvMY1aG3TPXtM6MwvrAxdxu64NVmOi/t5+YAXCk7qR/AmDc0cBKRGC901XQaxi2rwMSsOru9M83XmxylAcuXvseGveuUNZp8Ti4U+oQDrpBx/wLMELWFnz5MFWcDhXlg5k4TwYjkpV94AJRwSZSmkG48RLjeKWKy32rHtLt24PofiGZdxIulsOtXg62+h2lG+svf7tADSGsxHFzEQ7MeWkqrohhzD8nGZSGpo35c/P46zJMrI9H76R2UOGgZY2u+vv3aNWFmWHNhSo5GKoFyEYU5S6oy+kQM9R8V4vtLNm49MfH4EEOOKsjWxpgwPX7XEaYkzGpXEKhbsx1g3+BwSYMFIAAfr38nMtqw4C2MoNf3EWXZNW2G0Wam00EgyM5JQaOUrceTFa4M+NY8z0hhNUx5v7/AXDD8CuWqBfLX0qKjqsISxxymiXLmlrnHXgvwODBvBvELo0+MtbTb72+OKKecwPr6zNDpDMHNvwK2MWaiVm0VRlI0o7DRNdXU+fCA7mp7OnqcSUWmzgI5jBgGpzftRVErjmIOjxquZOIlNQQCD+LEOJYwVh2gmUx07n7MeTNVPALYMxzo+Z/ZpggFURWxXFmOsFrhS2C/Bv4ZS7Zzh5O2nu+kpJ0bedPoylbLoPl9XtGy0nA2x0qIY4rFjA1cqKyfMpAWGnU5frpjlxFmFdsQ1YtEUcE3iNIrh+GibwJW0dlvp3+4Yb2w58d/35RbbYURW15HoRMpQS7YxFTgcVmZZQlwq0Af1/UWogiuta9jDAplgPt4vlsGa5ts2dduxzDm67c4lMoZqxly5cq1YFq4VX9S7VG3M7fqXbHTj6eGmWTriPJBdSWNN4IkOLN+JrX+CVcZAY32mQR1g0ms2mXaQ1uLMTFWYcD8BMyMXos8qz8Sz3vbNr982IKZya2vD6JHFOc/D7512Jy31erWPnxuC2mGVglwal8HLPN4eHU/CuqaeFC5q3METoRKoG4kbmHJiDs/hrwVEvy2Dsa/enWUF9v335S45IA3NZIucptbr7vFVRTBgLGVCyPOMqOkYBWWnjq+UAPZA63jyM12la3Nh8G89jEuBVleWfT4gR8X2PiZt2/cvnxvjbBgvs6vwqgcS5sy4ucTN6MS4lzWtYJnFlnJ7Msawznga8GwNBK7QcHOv790jAR4BiAiL9GAIHgb6/uYWQxnT75QIhWdTJE97bc7VNltIMEC3St88BKgNZoxpWV8z3hFGn233hqs3ddjfxZgLTbtt7QbTerwD8aa5VfCy/Oo6/S50eKpUWGkuXKmomo5o8FEG+GjsIjoDlvBhq6QLMRbSo39++86QX49P7KaOzGYM3eUtd8GjcBc3K9PHeYmp9PmvUgrrtk9f1XlHdUBWiLbp9+YIvV+P0vpEoM5r2e8Ow6DsYXzvSCg969QPb3gFOcDyP3c18B/FHNYT74R+9vsgkUG68RTSKSuFFE1CaFmGIRBqS2jSAMbYPP9mp3w6GkQEs3M+0ORGNh9rvsRU/S9A7a+UROzhWlyxxxCiKAaYgammTtWflgCo1izTwjAdkPXb9yzfqXtr8RXt3j5XzuOzWA2mh0Oxy3iDoSHxK8M+ktXqHm5zAP3Zr/MLdWonc1i6oyeWj5Mq16/x+K0XDBeX6uHTsQUv4rcMsMkGN/wCwc+H31vvtEoX7NvGtuuYovePA/ARpwyxFmU6wQDOXi4CINI0LyFvX2gGgn8PvtziSXXr0HFeBy3j4MBfldnsRSbN17r7CbTXNvyzDSx+Ip7H74TN3wZPOn8bid5W7u2+ELVu+eJD8NHH06/dZVa33L0iB69NH6+0xf+DMJryus0Fk/wB9KYnPFNdtHz4zZlYebmLEcCqdQuowjLToOnTaDkdfJZ9q7TGNEHZKR1hjp+QtEUZJee0ZHpj8FqKx7xOWceEOF8bqEYAzCtY377PeORgot6/8Os6ytTCi7o5pfwadYApr580HdR/caGVfYx7kLT3SV3f0RSagfP8A18cQQ+r76vpUz1m/lb7/AC9IXmB+VuBxHjXCowxk1unHOIb/AAVhMFvR6yt0bffjgazfiw4mVRsPmwXQhmH40R0CFBwWL2v/ACaiQdFq3rtRv+46NiLyNdPR5tRotYK+cOzRGqM0PK/mE6eFxFHukYZS0M4ByvsHOUexRfPXfp+VfE0UgbsQ54sGyaSmOn39Q0sqB+B+KXhmdzJn5d4N8bCW9pktF2zGdNdMecWjkHbOr5uOkGajS+7+iE3aUh2KLgYmAHW1t+ImStZyXQ8faMoVrdv4mQaxddHN968i95UJKIORaImhVnHIQqulcNH43LhQsNaYLVuR5HjheuvL+QUt53Mres0/4lbxuFHfgjSO4v3gloE3dEZzQLyxDk0arntcFGasPJeXy8jwg2nDSLV79bc6y/BqwIXQZ282AB1y+BbyPWFdYW1Wv6/SDZlb93n2+IDLtXuRq3kdBaro6eEo7Bb7ksTNC+4A+0xUTKsSuNx4KrHAA04ukKXHF/fmWs7poPwD87QqWRKaIgwJBcXjlA0Srj07Gda/u/KXwmn3L/JZUdJnbZa5ZzA6pS63KMdm65y4chO6r4gWH0wHov8AsYLauZUDQW98YiLWVQo2dPYzKnV0dr1rTrmdW2ff9Qh6DFV5unwx4XxYMxXBRpS/FhojY5xp4cGliVAS9lhg4EIR/Gu1sQUQ8qf1Kq0wNt5Zqa8yCGWO/wB8o6QZgtCY5c5/nO+fCGkC6XbTvm7e1wlQRemhpYY8a8pSGo2r77yqCqtDzQicC6fY+fRMU65M0mYl2MGag2V32o/dTC2gstFiazRI5NHH9TaLwni6RDyPyWLSDKRkeT2IqGwaRYs1KO8ft/ZgUdPSP5s3jEVqNhk6594ucOTC3zirUO/784Cb29Ya/fj1i7oQZ1p+8qjwTPm6fd5U052ca6rFpU6K/sSwtqSbXr5W/MpWGuWfeyWQsO33boQ9TewxiO6+qvyQQp9NoVMMqA9IEHVB1XY3vxqperpSdrfvhAzCw/qyha2juOD8hRDNN+8uFxAWgjNnfHlmA391fxriyuN0Dz1cU+x2nanU5vaOZgzbv1Xbrvy6OfRW2ffuXZ1hnNDYAUdhy5rEQsYHbcMPnHQwhQUvK27OUbFwKBVHZOfLMBXNoLo27duUbWs6afPvKzC2h3faaZiXwyzRRBOmEvfd+MLF1RvvQ9dYdjanpZ8xVt3XHgV7sVJqv8ln/8QAKBEBAAICAQIFBQEBAQAAAAAAAQARITFBUWEQcYGh8JGxwdHhIPEw/9oACAECAQE/EEuf/H8/MRA2ZH8xCp9xm3PXLzE5ip6JUzDl9NfXPpCSuSWeZTUwIsXd5MKDiS6IUkutRZlOp4Q3KGVUA1LKzOCwEbc2cU6fnUmOA6jxfPRTxrP0Wk5yWV5no/eKJEdkWPOaTnivrAFCiUIliPA7+FcCQtC012XBBjbPQ17/AGjFA4fLTVylV6A4Te++LO8zVsPqacv4uJFioVzA4i4HG/Lmb+b8/iMEuxFcOemxFP7BeNq33KdK1x21K9MA9pebSi8j7RHBiPsxbhwjhFAuGUYbzgInEbamEXGzMsobOOkqeXdyO/aME2Ml8PNdO/WAOYmlC/39j6RlTLZcsZ2SwxhkjIILgx+T85mk50vn4xAw6a9dAY95ZGzfzAXNdz1ZuXX4D8RhD0lCUwSXNa7l/iVszR6Otd30m7AD9Mg8ks/5PmAz21y/SbtwXNVZ0xjF/Sdjg+3istvUXLs8TVLnDOBjTMATJAahg98tcRWxXwFVYxG1TFLL8LqD1ihaCZlxORv55wNK3w9WVnLDWQfz6HfvCgNx3WvofvpELtC/XPTya4hifPxGrmkPAdi1+oQuWr8ubx2d/wDXJK2V68cep5/UyvRj1pT9epxKOca+tnTvFV3AZaXLg6qJ8DWYcTsRd4lty+sVLQtinE7UExUSlShwgsM9u0FRalrKHco2iG4BeJSypQMB57aMejGbksLs3eXXqa6wzzNqDrdH2V2uAM4X6aPtK7VME3DCIK9uT6xW3Tfv2iyjBpb4cn64+mYmxOkXRtrFUK8whipRxd1kxWzylXNqErVvk/Pce3Gd/OY2jSNvEskF3M2HEbSyCirFwIPi/T+RhB3n7xK6imEH1ZUW1KdhEZxFWW/BbI4Qo3BMQsq51SyXAiiQXgA8rv8Aa/IYGEw2d9C/Vv8A5DQfjHDvHrlcEqCaYa0YgarzdX6fZv1qLfE67x9OnqTdljfUu8VmyhPvmwsdUdcjAFYEyOk7wqR94NcM5fLFRanBWzyzpL494NNifZjhHkm1SjcR4N03KhK81KMzNcvh8953JdxO3HAYjqAqdSxvUHm/iGFI9ZqWqgDip0VQRvwLFQUcQAGat2D5RnrLpLFu+wlHxiyMISkFAQDob7OPWvr3ZigRl46+0LU2PkDPvKuN4PObZV06gakiPXVv6h1jg5e+0bz0x008dzdt21U3Ya5MXfpCwEW3CLp1nz5MQoUVW+9hf3xB+WTrOKLpY80YtlO4EOqPVwzKGq28GOIwfCritm5ki9I2ZIWjkgNMavEUqo4Yh7TN/wCQTjZfSdyN+hwcb3CoLQv1SNNyukrjlXFL9M/Kj0w1bXB6g21jF8nEu9W2vrlzrH8ifIzDGAoKZM2hlsP1LVWK3TaF1eeePOCEAZHz5t36wx2Pv17efrFZE4eibNKxWfqR0DkPn27f8gcHo39M+3tH+bh9/wA/Wa+FYFzsxsoYWm86I7wSglf7WMRySpcYgGOoMFVNxCzEL02c10r+UecFDV59sfqFPKd2KtwC2UqktABdWuXPbmWuWnHtXl+N1AYXdHCjDRjn7elctfX+RlJohbbd3VdsdouaSUu7VQ57Ra0CcWUe4fthL6RDOKveb9Kh1+0ZrH7vyx1l7PF2fPfpjtBoE2Wd/wC/O0wgshseFGf3b4EC5aqXgJpNS7BK/wDF3fhU08HGYsy5QyjMNhF46d9MxlTDGZcQAtUGJYM19oJGzNBzYH0buVG/gEw8Xy/lZYWVy6tfmAP7Bb41K3kgpytu3GsYL++0WKXIpi16NOCEiDgE65u+PKGWOMJ3plw3uMjpdaHPvzAOaL236W+kPEJriFMZN+JKS5SZihtlvMPC/wDJ4scTogiYmsAa8CKReYXBGDcFXnACiXHeoRgcrFd3n0+7vEPQpSvdeDpx6FETbNY0xgury51xiViB7r8Y9oiDYMWwik2Div1br7QLX8ntV/KmnRkvdseaGPTpAftPtLqjmJBfT9fr6dIi3CBi/AS5IgYEbNsD/Vw8HwY6l1iLcWoorrC4ZnMGbUBhY8p1BSHli8d1xuUe4to5Xj3bz/2dklTiqL6bzfY6ztOTJ2j2Ilb+ZJyAsyV3Y/Kfj6kq9BF+rruX+4BRU03o49Mn/JfX1D/srF3zjH1Y58pll8LFTAdY8wK/0w8G4y5cdx0zWZZMExnX8SoN5nMqUq3crg0q+f8AeCNpXXDu9ax7ziqepF4+3qyxZQVHAufVZxXf3i2y63BaiLq8/O8aly2ufpnAfCVkA+h/2DZsLvsY95f2xfn8hscjY78z5fW4A4T6ytly5bCVBc0vEF5/2+L/AIN3HLFxFlTHMql3BCcw2oW3Eiitnwh4fQPoV+gzF8lbeuy8jR5QEixj2jRiDW5g5gxCubUVGfn0gVuIjsn0ax7S4OYPMYdMvnv4C4wCpwR/2+F+LHVwOIIoJuZjohiYjhaDcLqid3g9NxOYGwIBlxpiR8QegO0v5rrDF4gQqJjJ3FbcqYFxAn4dIoooImYJdRNTO3hcGAkOdTCv/wAGVAjGbxFiD4CywDiUghEC2WzPeX9fuFHdr6/PfPWPlWm17/rp4WkYtzqwKfpMmb1KfA6GMnKH2O/aLlMSGUZIWijmUB4XN9JSB9JRvrCj/wCOmPWLDvFuLWZ1JqRTyM6obaCM4U6fc/sTdF358+/PnGW50fn9f2ExhW5lO0Y5M4J3lw+hEqIBWALzLrpCEu3mbI4j5ZiYYxFlgxATDklqnTDFmOMQZcuX/jzixzFjw4pWXESFQVEAmXX7jinYfn9SkWjfzvAYHgMwZqdJzccEUsyookTpi4uWB6TPwHH0PKXjd2A96v0gEtfoH3WiCc263eek0ZhAqyhb4iIiuQuGOqncUviXiYgjr/KwaLmkoJVNkNE1xAl0WwDiBrzcH39oqUG3UDlOZYTwKZju0p8CKNQNvAdY+d4jab6egYJZoxilr9I6Y+e8VNTgd7xX9llIvRXPDvGfbyj2FRxtd3uqiAqW9Gvu7v27xr7lj3c/qAhlw6K/cqp6xXlh2dWEpRdkW+SCKv6wwNiU6glWwhR4r4lo8K3MVaN8ecKom9GmKLdq5eB1jOa+7f5YxgtuVras+cWogaZalX58oQ0P1f0e72lrbeVzXbu+xzFx9Ty9XwLKYxULGV9ZsupR8pr27x2lhZk3VFB395Vhoro7L+vS8RAK+yx2Xt6557BOMdSqryihff0iD5xKEWLqzUISAEfp1AfsQMzMN3F4lLxWWJHipilKpZ1vBUl6P2iLHY/GvvDVsV/32loluy+sQWfkf5fv2iqlgh6PeBcq69YlxvQ283g7Y8obFHq5fN2+RM9AxQIFdL8BbawX4DpzeEqaxbRvWbtrUa3MstbrRrrARssHZnN97lVyCK9cr6/SCsw6F0p9KO3U6Qt481fu4NLGy9zNHEIRQ8DwWGYLsjvJAdYMXWDRHWiM7PBzRHklO5ZFgol4dWo48l/j9whfC+4/uKvM36YlO/MRtbXodV+ZgbO1q/u/jpxFLK/b6fuD2nn/AGYUV1ahAvM/UIVCVxKDM1aKYK8EEEHn1au97w5zLdY92s54a6Y/MHaqLNl2y113xrtNhvVRgBx59ulRuzV89Ybc8C8p1HS+rgIiKwMB833eYIYY7Lhn0x1K8AwXLNy9Tf38FZiMWgEsjM5isVzQ8Sp4NdNmfpBtRkfUj+ofn9S6DoxHWmN/SfHvr+oJb2zjB3+W+0RtLfb0NToRGodCLLFMV8Cxb4I7W7LPJ3vq+sQSzbelLu19vrAMfr6HNcGcZvluhBActt5urcvTng7RyHJTydXodDbFV00b1MAuJe6RWYM8qLx4iJGDmELNxzDMmIRuOF+FtvgFTLVmER28J6wGxQe5XtUugnMutOY0ccTHGXX9gAd+/r+vrca1CaQdYDHZXWOiVq5lAm3L9vADjiJrA2d0Wzo8euIpaMVdXvj0XrW1gaVvAa53r1vpb2rONuxizpTqHyo9S/s394sYCqBLGVm4wmXgsYXA2l1WJZFdiBSGpkjiYIEGy4RLp1+z8+anxv2+kVxi8pSaYPy7fnHSdUd3BNLgxc6MyfKXmOARlJ4f8AmZdNH1b4HWt8Lq4Q59+fQ+bisjTP6jzO8II1KIAswgxAg8XwTmYgylcyVAOYSZh1mk39vr+oLEDev7KVfQr9R8EfOvxLIux+nz7ypbFjA43+LnV5/sqsTRDKnUqamgR5i0mCtsxaiKPMdrw1tHHYOfXjtUbLr9nzLriOTUa85amYPzi0zcWaY7MZxBArxfC5fESqZQ2TFMyLEcQijsZaJcB+6dOh/OehuVh105f15RWxgRViOlY1eSCvU+39hmLFQiGyAa9IUItxVo9ZcKRgxRuPhUKQVj7P3/ACEUZ6913MMOIlx2nxuIrNMeBD/CRljDukyPMt8BqPAuzt9cV5EdHM4O8BF7Jo/vX3l7bDyPI8CheXb7wVHylF3r7wMjlf1+IbjlVFfcTUHWDKaRctRcExSxL4i05U29ukbExZVwaogJK5cq7kNQ8D/ImogKibumOmOS5xGFha/Mwe6nl6dr/UQHpdunz5uaVHPV8/1D7zKWe/n8locQKqGab+5z+/XwM5gxCl0Vp3f4jFrFzNCOYOJx/wACEeE4ozeYzFd5cuo7L2mh4q/8i44gzqkSii8ilKgoGjmDR54/fzbOaHzuv2n3+kaDtuefA+R+3ERAwK/d/EJCZZfVuUhfX8XKwUSvT+RQFRbwRFDtFQ5zLiiO9zSpTiZWjz4EUzb9TQmxjMXcfTUvwNh6wKK8OZt4MJcYILZaTo6lqPeAVStna8euAnQIaPKK5gAsPPXtMns/b+oQh093+VAXeMe0d4fOPzKbcI+6SxrHUovxKKXeJq8Swco4VL9llKKhTfhuU6wmsNSlXEiC6JQIOhUMtQFKQ3HUfAeF1Bj/AImW4oDBjbH3cH5+kvJyx+U+x9YG1Br7ftDkd58/lNS6HD6tvukdg3f4r2hE6r+sZd+f4hABhK8l4fT7QrwtBsHJB6IMELK6TFMFqvCpVQ0samB2feXy3HBLXim5vcKZjMucxOGKoN+CQxNys+BhGWXEx3DDBLy3349NX0xA0pgTeNt15HP0976Trqg+ho9vqmepUv7vvAkOJXXpL1PjmUV0We9faCZ0RAxLkFbfOYK8pkrFUwbjEzJUqa8ASuJZIXhgqX0mT8KAcsaAHE3OaHN+AiFvBgy78FC5jIbkoBiN8XxHI5LeaP2xadEPIUPtj1vmEp0UHp/ftD0jKidn7Qh5Ps1Lo5Px4diVkGFVnSHLmxXUuPmg0f4qG4d4gViLYjFubaPLw5c4uCYw6y1248G4dPgufAYM4pc2y4uUVA20bfXB7XEY04Pn271zBvsdn0T2lQ+IsjZZJ36JyY/ojFGEJ9JgyoxKKHJLjE1iseh4FmHjuFEeLgQL5TFccYJxU2RmMY9jCES4aJRelfPxMlxlCM0y40a8AgIqzGWEAOYKopgjXuBW+TAetLBhFKx5ROkFIsFuTMW2kBI879SoYIty5gFNw1cOGz1ipMY7/wAYi011RiO+ZVPRHwAUkWseF2YHVTdOZscwhXCVOGUc7iNJn1AcO4Emg6w4kKBqXs3TEUL2/A9JrEWUbgJBqHjDWusxKTaEAxzLG36TAHNSkg2oKQjL8cRNHSYk1+41u7TgZUrwMx0BzEwgWLlkqVTFTXhgqKURVMHpLqC1Kk6ziLNJSrnnEOIwSqYECW+WDZUWBthvq6QUy5+fmZ9r5+pslC/0aghq0irwjGEGFmL0D1lchxMNoUyzkJViEqozlqwc114K6u8N/wCO3gGINx3l8FQKgFZUjyxjPLEAowFEsghXXAfmLeZT3Jd+O5cvwpzU4RqoG0YEFUJqu/hHUdoFKQc3pjlmBcjKmVmKrJWOs+ag2TUpgI/4e0uOBmJYH6IN74lQYhu9YsoN2SyOpacH3iO4CHSPE6Eyb8b8LzDO+kSE4mdRlKQ0efsQKW58ExDUFNkKkI6w3MR5lTcbEpCBo78kDE34Lw5iYggXliqC9UlaXWofqgDbf/IILazFLdeoLV6TJP17vSNsMhqd0zXaEP8ACypHp9o6hHr4sFkKCHOPn0YaSwlNeDEq+JlhNkyZIlNkSCqyUJiwXul3FhHOo0azLCksWhWDlgOZZVF0h73H/wAARWXB+o7SU/Xj53lxRloHpA2qzH5nEzT3/wALlQIg+WIRpDMqsIt+CAHzMFkOlfiMoTLgDwcTC5hiGHtEziXwJiDfMIpmZbCLaZxbozBmxjxhspJdrgattlgHiIEsxgO0QraxCsFRse5hgOKYi3r4V90HMvwrxOzvFZhHjwJx/Plx3T5qZLKDXgNlwrTIgFVmheISVGqpmmZTqZhkgsLsiWees2sXEoIRXaswROI2uUqv3+0tC+WLiCtZhQ01LB5QWFizHPabf4YRm3RJoGv+y6B1jxnjwF0hbfGM/qaD58fBizizfMmYamlPMbd8RCCGLMRtD7Rvkmbg9WINS1doYs8ysq5mCxV1KyjcwgUEVQGIlRgAu7fKKjLkxE5Aix9JYXwErxIUWjAUDaQF2eFWZe18D+pax7+/98Fi8xSm4WvojpjhYnEyKuX2zSptBUoV6lxLrEG0qVI6RHSWSjMgeEF5iOJQWgFQ81EXmWpG3zJ6e0sUWOXUSiGT4GZqbhuCMGGMa4nPheCLQqKqHH5oiMZkTXg1WZiWGnBtIOKlRRDSpdTNgMFNh3LIdQ7RmoxzCNveYk0wehntLGGqmyPJTTbGdRhzHyjiIgcMC8dTIEqoeB4E/8QAJxABAAICAgEEAwEBAQEBAAAAAREhADFBUWFxgZHwobHB0fHhECD/2gAIAQEAAT8QGEUSJGki2tPgnc4mwJhQrBYqSOVOlk8YBpDUmpouJo6wzhocmU5yUOoq3jYCpI019754rwPrlJAIKBAEeAtvG632sCo1JTbMnFJ3g+a23bnqrDsWt6R85CjsjudUhdSeqZzjpT5eTuPbFyxUz2T4Wzme+cmQAIFGB7oPFd87GgaNglTe02OeX3G3wRU6kEDv098ALUAIg8SmXVnBkYlIQQetEttzGACcpuewTNdPHqENJgSO6gfP/ub/AOtQfEYPwbyF1wB1NAdHWJSDuC3IXHABohYnnGSsgzD085RInyTJ5x0QiIUmA8ThyRKLSvnFDG7DdXkAVSdRicooowAqATF4A4BTZnFEvP8AMdzhRHXWIVRrZRP/ALkUBad+/jHIHOzl8OJhIxbGzzjECAETTACpfi47xUktCKHrOMYAPEcX59MeB2zA0mKyoiNj8ZySFDaOcKwKrSVgC/XNTM+PeEtpv2jWRtj4N604KE6nFTUy+JU2ST5myScl8Aj2MjwkiFoUVkeYU5KrkrQn0N5PmFwjIBqKxXFXLyYbPnEJ5kQPABxiaghxWiB5iF7msTEegtK3YBYXrCTQWQRalruXIYBDrCYNDKa3kJphbwbciCEcVeMGKiZbiP8AcU0i8CqBH5ypIncVfnCxdOJwUmAnq8nMyRqMjPBikh09mIeyqIT54fD7LkBzzOskK0IGgQpDNcxWlzCtg8FWk8G/SDNVCYXZaaORw/OrfGKIWA1xAsMRK2QJAGFNOTwoClyPYyIGDOwFjPtx00QCanTRLJ4HFRHFBmUMdnSFX0ydEoRAq0JBoL4nH0xInyfQxvuJSAV6zwoeeJ5da0KFNQE86CHKA6IhRJMSjJ4JVNs1fFbCAxJiCdyzFE4uBCZAskIANwiOCYym4uqZlOfLAE0E2r/uDCMLCu/jrGAKCTIBJ/OJ9ZbVkvELB2L3h2RT5lVIrXyCJsx2OB8zqYSXmoRSsGMXLBRMA1o74PLDBsIosNkQkCEZrJvBGEriE2YUq96wRsC+oMLEJDqC43jsgwKAiHlQxMEuDEbFrIZhAdWTtWYnERi0AVkwHZSarjvKI4oTfYleQGRRmUApdre2jVYtMigyejoBw84NiSGWYjmKmdEUGSgEpfBwpm13E+03iYT0OXyEqHo4nzg9BBklD4Is8E85PtMQk4Kmt65yA4BIC7w22JqbcUYk09S2OZsvHus/HXpMV6awkFjF/Yxs3RksZsyF5wAGQXdz64ORHSNY2jH6PGEdEMKw+5DkywCBOfXF4YYEayaSJsdx3kaIqbOcOJBNnr3mtTBtfYyFiJAC3H+YwIAOUYQCDpuRnJbINL3vAoQHkZB6xhSTAqzE+M22I7pfODSxTae+hg14Ed+DkTMBKYn4xISAbk4YpBEzAtxQk7B7fTLPRjAuUs65nWTw+FSJIQkJV6Yc81yGYufcNvzWMJOlgFmPzgCBmZGgVmxJcYFm5L1VphT3IlF7gHJaEjNK58m8Qh09z+4SEVSmjFMAnSUku3UPtimX6iRadw4OryQ2JyS2vTIqYJ8n5yiePTBpZO+8kN9FayMNNEuiODLGE97ySBSar+8YjGJE2vWIkI+cmMbO2usDVEDFYwlsMXglhhSSMepSqbaZE2GidSY0dlCGTuwMFzJVyYAFSpx0DQ10G+zNw0CAyNIRs0BKguXBGpTHGkgNgiYw7dHzNSWOYEm2HEUDMJ0Jlm5alwpgmIFAQU9a4qqYFwT6Ad6GG4izhUTgYxq2AbRgWFvrQyTiKIgoGkc9SsxlbFAt5C7A5diYKw6UIyNkDaa2rPBiSRkOmluVSJS1t5O8yRgBWAgIXWlYSSJOr/8Acbc5IE7GBPXIk2JqZmpnrXxkW9YFr0Jv40TjLBlnRCRukjsGwYQiNDD2DgAbUZRXA5YL1llRkJfRFAZFH+jAR6te6YHdCAiJkqFoGXcfkQImQ1wkMU1OmbmMNUSdhWLHrDHjFOpTHIwDwVkW2ojFzg58EWoRt2YKKHKVgG26lRo3liJ3lG1HXDhIBGbRiq6HWKYwAq4+HieuMGc5Q1FOVFkdYysgUkQ0nTu8eEunXMO1kssL4IWEcOsEBmnkeU81lYBRKtffvtYLKbe3C9JOld4JCLYjxghteDAAKSa/ONAisXzgCtmCJyYRJxgnBChoOAJiskRHrgJBeGjKnZTW8AixogZLVTKJeboKaxiSissc5IW3w6xELoaFYGKJhZXoP7kyUt45wEXE4by0PXDfJyCg76cGWNWOo5HtYPDOvI8T3h4BBGgOIwIOEDGMXiNl5NFKsBuMZEgJEIgl0b5MmmZEyLyyud3zgZBjQkcgDexipjAxjNMMMUmhR9GTNCo8zAeeT0wYBwZXNtjM8N3rN4oS5bM+5W+ZzUD0aHFsONd5I62RnRbSlvOQ4khIXcgU8zkxVwmW8sSAbdxm1Agp5yOnjx/cNAEjeBG2DmsQgUc1kkvtrB4FHvJIDYeKwE8LVZYrCfd4XICfNYOCGRKVCETggSxw7UcPNkb4pj0DwjQI7VognhkDU4gicxomelLMMTI2EZBhr8qQcMPnnQhlSWqqEUUhBDal4MSuMgHLAYWZBzwzEqTEC0PALsE5qIwSAzFFCxpFAACpCZch74NlJE2rYI4SDeMOmKduyx2IGm7caAI8JJCTqlOiVJST3Ky04AiSgpbKGOo2OhZx3KCwpTnJSipIaDKtQI6MEAsNKhZPvkPIIiaqcoSfkTFYTEhAw6ZUCaJWVwmb00ZZ8woD4xlwSqlS8uBTDGiWLVsQExFU3gMHEhBCATcmVTFMkPDEoMKpKt41eChAD0vWkBhNo4XBGGaNKEzNkj54yB0BdgjNrE/xlkkxJpDZKIeJHOXstCWka75cfOFsQRCTSXgZfOIisQVQ+JFS5YQW4zHby7xxIohoKesa8bwGwQVMyKjw85IgkICpP+feBoU7rnGKY5jVGCLQfN5DCjoIYCUmGg57wXa5axF0PJNYYAEwx/WUUFFriDS3d5ZRiNSxW0Dlk45YjcKTAoB6hhLYbjXOKdKSrnLgKAiYMEgKWBvIDQOExkQWyXIgITDdT5eDeRFYk66jgMHorUhzDg843XdFydpL564wyXnYJm1Xf6xsUU2+8MZ4nj1x1FK9YIQI+LxZqAmvPthY2C//ADIzAkiUDE+ftYstiVE6cEuB0AFDYYNaJU4pbJdfovgkqhF5CQWWOoBSqh7DWU9SENk04nFJW0/ybynpMi3wsXgKRhdSeqnGVPuR+BjfsoiBae7PTeLUkldY3bfnItuhADoWK6685IDshhGyf8M66genrFWEAKg485ttnAlBLHMyCahnWQ0BCMIUVmGvM4OY9sEF56O8c0gKsrCUYhiDgxJ0krWTUUBGsBlLOTTlQhgiBIiaAV0KbxlSth4Iuk2NXiIYPBRMGiWohEscuA71mMgDg3IPBrG0zclMgPGwTwwIaGLB7rgRKcScYXREo/epADIa3eIUPiwRMEnCVMoVKY+1jpCv8L31RgWD0goAnbJPSMi0E6ZMrLlUvUecANUAWYy3BC08Q3hNMheKQBdC5XEnYS/yA+wLHRldCoiC6MoLCdoS7cXzFoCgCNqSLW9GGkVHHvb0xwgCAGankg2u8GKyAOWgDmWMki3UVeOxDLdXg9TiEt6EbAHKeMLGiQJiAstJWbs4tDOjITXQ2iNTrD1W1B2WMRZThqXGOASnOQGFNwbBwTQvEqyBjZLn8XgeMyAKISi38FbycBiBNpJVWzqQb3V5pLFqQCDwvPUGRJgCTMNYwRKwBC2CGQjUsTjBZxu+uQRZgiP7nSnSZ4zdtnn0xMib9YwSIhtOTJOAs/GEOFobJkgAhSrzWQvUkWI7ykJCOM3XEI8mAQhAM1zjARBcgRrSljfLjUNrO8ZUORauaS9AI9XDj4g2PjifGTj6B5jtiZVyuEUi8I4jz75d+XtKA+WsgwVlheQ89tuSaDigkpBHSSccSDB+BEThJd7rPWmFH+MlQppAw4LF7G72LYrV4hdkAswcUvOJJEw6i1AX5xar7P8AUFH1/GCPUA8A0R6Mm5bPJ22FLyfGCkeEF41QSfOTybvHLZLH0rcmOeI2bM6VU+PTI3ExwSdg8eRrAila2PeXE0zNJYmsHu8ABL5EIbH2rGxSkBJoI94wfIhMm4iPXIapqNPVCXlXX3A8A72nOSQbEGoXt6njnJrWkelrazmMDQmpylXuyIETVhd7Si/Dw4GC4TkxiwPU8eMgMhIymW1JLxkxJMmFw14OMANgc7wVCWIgdGWAzBlAEGNCpvnjOQlZZh8onhWWE3h8VG3yIaNsxvB27QCwM1UKsMgxxOWvAZKEO487a2tx4seUIh+YAQH4YYsy4KeqFLAo7nLPw1kJHZkE5AcnBkyKyV3Aa6gOcPZopCDotbKY9859fzR0MUgFiN4/0W0UlZbkrtnI2zh8DknxE47BqIGbNDEpUW0YsQAWWaXrKJTbi0GMHVYOtlwZaKnJoR8y2VxB6ogBzKvpjcJQkss6EqeW9GTJT0Vh0At0fLJgPclVbYPED6YjAlG1wiNk5ssjabzQjeDUJoM3usAEF6EWHkkrr3wreEOyKQAIQk2RDvI0Um7RgIeW0eXeQthFAsM6pCNc4ES8gnHAIaHRzcuIMaeWSXDoGMoUSdl7BwHWNHGBVD6awemKww1Erw85IA5hfuxbqW04MnYiSRreINVORMy6MEK28ASE8klYrAlJeqfGVy1JqIxCA6qtn+YFSbIrn5wCYXj0MQ4SV/rAhJIrsb0+cmISPGCYWDSs4KEEJkjCIS6lZ4nBak3ST0YSnmZPWOarCRx5YaN9C8drWVPANHpCcLVMJGdCWvLWcy5NTcjuPFYhNUDRKgC3aux4xJGjjA0E61xOOvvNg2MBL8mGXjzSaaBKvjErSk1OBFkCsmsQIHjhlL6YskXYHF0flj4OIfsk/Y3gkQtLiRVpeOM1S3s1LQ+JcSgqTEtEDZscMpXA3yhRK1hpkcSIyWwUVMWZ8Jl1ucepg8B6Rk9sk0OYuRxFSnDJkynIe6lDgSJSIjxOHD+RaTXq4m8VGTwBGvniCE5MiO1JDNKSC4t1XWB9iiwvQlUiQPFYs78OmGFUG9rRhFG6mIojQbkNQYwRA+iFIhkIJHCQ5IyWgRruLNknzgFYdkKbMxYWcWjxYPLH28CAWvXHrhzsNyVhst2VigSEE8iOsFVhiZv94BBQtBgFy+VvKABPrj2NJ7mAcnKYJc0BAkR9lyCegUwoaRREezvaCidjKBl6aynKvZweh/SIDpRQg3QaMAODXyiA8NmhfC5BkmARWD2gD6RkdzMwsAFlJXQwJ6SC5AaNkdaelC41YhFtbQMc+TwiYlE8Fh0TjdjENAgLdJZjk5hECheUcbItiMniEVJZZGqXdBcG8AYRlABcEwQaI5gXGsOyDSUHwCYJYxjYMIlsuZ/mARC5t/mVkLEJwsGIovgPnNx06RCgNe2ABBo4w40upHpvJPM2xGQFEBI65SGKF0noiWVeB8EILxpHlAbA1X8CHCS4DgQWZQS9UJdJOEZgcgSVMsolbJQFOg0gpyF1K8THWIGFbwCRCklCt2ecM0JwKGGoqJD6tYExGyCBpkd1juxBNGE28Asa7wKpm7yiTRBqtYjIBGkeVFY67U9cYLZIFSmsnCQPLxhEKI1Jl2iT8+uEqcAneSEylFO/GIoOxhHXWBJaURw+hvGnmCqv4YhAHQbcgJy0s094FOZ4TvAlY4ULIOaJZw0J64YCd5d7EuGEk4C93JyTm1NT1nsYyC/IoH5GifV/WRyXGd22sHxOBltVVvLPPckcYPYIeJ3hU7dvpjggpMg4EpiOd84jWRERJlXTZ7yHQ5WI6k2WjXzlvHMlDCJCxHbB0QI/0kEBvd6wXSQD3ExJFNJzkUdtDTEVSCbjKwyQBD3myvOEIox1EMsWVXeDDlTMRHGA8ss0RoYxoDiFiKJ3hwR69sCunw5K7fnLkwMtgkzMOvbI5aGSqQaETMU842I1a19QYhvK8uLGXEShC85loxuJS1jKCWMSBCDNOkLKRAkgSKIlWTlljAxoL9ANudluHaCIAF6nJynNZTHIMwjSCTZhaUnsLY4FgeclYRF9TkllPvoxggZ5ZxDTCEw1kgcQmnCS5N7ctDEkfOJhkjW7x0glR04iYiV/6yTAqSlgqT5MjVMqpi1HNK+2JsULx2ktQlmXIJ7QUKYltmCyILMRglClSIwywtjdWODHOB+gOWgqdE0TeDD4dQgkjmoDVxjkNSxpynBNpEAdYRghLcIF33Ux0JhStI2AzMDZu4mzBt6I9CQQ4BARx1lk800pVeAstAL1kp9JSSiqxgS24anKmq3QlsWAeBWAxATWWuAoIs0BuB5J9hvGYQrSqGa07Geg4wejaDLy8ZfmQkBtQ2saOpnviMZoMb9AJNAjlwZmM60yXb7p9sj9GKkx5Tkj9hWReEwGEmh2vJPZgVesA0HhojnCCQUOXUt674KnnFkJ7JgBKCCjSwKZJth95MaRmnGMojSR+1sxuQQ+8gUiLwx7JBVi7vbHkwxGDg3HnAsXLr17cJRQjnn71gBB7kRhTYLqIvIsnY8N5EkmYcmSZBK1bHCYWkGsUA6uk5YWSsO0/vJlcgRvGRDM7WsJonIiaxgME6MmlDDChNdj3C0+2QeCAqbudkYddFpPUgtIrgxNHoMp5i2vq/OQukWkl2xv8Yw4DukI9OsUKkCjKjhOsc5klGPKojCsWkQoOio7c2bOOEnxhvhMH/cAsCABTJtTOue3vE5cYCKWUCgp11jJmhNsL6ZBmXSD7ViVF8qnvGKQYJUQPW6x07BKKTqTcecMEY1sR1JjcAsJjS8UsbnAQWkiWE1w4XFYk88v1Y4MsRKe5UT62YKpU8D6zGFG1AINxwuDNNtBI7dLhhCCwzJrEiRXSvz4w2eSQHqZ2I8OSIkjN5lmnrWTrfXetICn5Rjk4JjkQeRkGnxGSOmEkAkVsg9DEjMEFqrk1TMMwQie7AGneusIgU0eZjNCeKEOy+OnkRxCXPlxgCDI3ZiALJD0wBlSktYizI0rRh2LSIVHpkVyRkcOYkHWahJ5rGd3U4tB+sdKTKLIFxg01H8s07KBMU846TZ2RgEZ0zyOsleWKJEAlDRvsYIosNYAS6tDiIjCPFwuKxsUxqU1mpqgGFURBCQbWc6m1EGwkdHkxNosB9C7gCIoLRAFxEQQky4SRfiahKObCi2FIRSNoEgWTNASc6AnlEGkBk1eFfKRGoTZnve2BSQSLy7KQNHjF4AZIYbe0TKry+2RfiuKiyqBTAzPPBhYvPaSkl3vivXBSkuoMEFQD5jTiheQBQbsMpGKhvBEbAAKCw3TCS5vZOUuEwLPBu+sc0LpjImJJMwqH2yfCCyI1rTKJUjcYILdtYtKMBDqyJNmM+h+pacBgu+8jsvhk7AyI36sAIoSLCNxkECWBZIHIm0mrjCMC89hTL4BLyoj6S8uEEUjELU5qSsOCVnWKv5IwJlsxveRkFelGHGInAN5OmYNMGzCMLFIw374hICmoXhDdtVkCKSyGkwklHb3glOj85IunI/MrMYsPW10VzfpjWIsvAJbLkxZYBPMVjYxGMxcsHp75Gg0DT7RRHMK1HYTtrLUlULPTnAOUDsZlAYCIJSc4wlAUWGFVbBGhFBiS/KnuTDETfeAKCZSFtEKD6DOHz0EagiVCeaPbDK66hBMxx4fjGYUcFUCgFp7mUMKb0wlkgLzBKaPVwsjIpQ4EH8xVyZEbDbBOkxKqfOW6UQ5CaGCNet5JGCxcNEL3RjkAIHj05MdS1WQC2AheBeDrJEEAVK9ikz1z4whbK6i2MhWpL8YQeYEbTCQ1DhPxaUlKEEXghYhIw8ecSVsAwV2Me3NYWnmEigwBQNXxFuQhbBHkYsSZeRSOMDCIFIk5CsM6vXGSOUjEYvEov0cufiRUJ5d+5J5w1FwGgvChrkyizXq84jMoxIlTU2MSFjBid+ljYbbG4quUTilgKTGBQmkX78sIJgQKZtdzMel0jNtooS00uAJeJeO8sosxBc5NHjdPxhxSRbXvhWWgIKFBbki/XHAAksrty0pHT/zBoJkALx2ZGgksydgooKFI4Ms2khQCU3TMZzRNC4I8EqBrZgNhkLOTeISE1BC8J+7ihqNuE4H1Y48Jk1Q2UAySwlEVg2pTqdeJhQmEQuYdz2VJUVi1NJI0g5KkSESwagEJjrQ4WEMjiWYEE9XWkpllZUodyItAA5STI5HXDMPkBcCYPAYPiUkINvi7e3lgQEQqG3zLreT2RulD5OB5iHiYpuNEWMAhtncdGNcIEEZigBhQlZugc1GgeTMapR1Eskzs2Nc0KTPKBlIlLctGcwQBnQLJ6B7nG6VIyXs5LPausmakldLTUos6TIuYsjqONSmZjlMk8ZFA4p4AaiGmLxxE6RdJaVmRvrKWAgmGFw+5R0ZL2Z2EQQ3MsArWnyDEYKFBtmHReWMErcBsspudKZI62qBkztb1dXkKRZCCgm4n+YFADkM+F/vDkMlSI9YxDFgEJNe+SUgeLf5wM/647wKovpeMTIbRhtsmp7yyWoi3EVyvl1goBIG8rAsTtoMn0nriPONAXMILzIGIPnHNEQQDwr44wGjuQ8isVLSFjJPNYREWMFdvGOQ1SFt1+MOC3SCncbjzh8VjkatR4Jx+Lpq7ASQZEdlXgDUAxHWQWxTSDgUyU9RYEwCFIUn3xcdQqXhg5QZCYtkM5gCAZ6jbJkOEo+SyzSPmJwXoCoJWRoQI7yZlCh4OWCo1fDvJkO6ktSAQ+wcGhQGkIKJg88YrEkmTZnQI1aq3GbE6mfKst07zWFSgQ4lqNnfecE0S4lQIg7ufHOTXjaYvsDDsU0NDaIqanresUlzWzEsdjqpHvWMgQwRPG5LW45aaJ3bv2yLbHDJJesYw7KaGElAuBJLZi7ULYUXgBiR7lm8GwqxNE303Z16Y/l0TJJlQqznrzkpAwCVtUWCPLfrmwVWaD2b5yKRRJUfMdZeqTBROyBMcdXnCyXVhgiSCQnnnCpvba8AQgSSoz3ONy0MUaIEYSmi0Rk7Ygis1lu5yWhiJ/ixsPRKT2jArLYtNAm1gU4ObSwFWdQEEM3MXibePJfYA9n4x7B5kfGTfp8ZearuiAZ2iIKgldJlGjwrrcem8TldwFppDVvXAwUBcQE1wd8awiQgbhwzEVDsYmpcAMzGiUJ4FiCJm8P2SaZWLbsFiY1qVCWR5FOpBpJK1QigpLckiLRCJEwTpiPhXAhQexYhq140SIQ0pIzmhiWRYDdEuQCh3RcA9pgIRHMAhvKVxJv1gkSgSOoRxlMJfDdQyCThRbD57JhMZlPAQytVj2I00ALIPjotawgR8CLoH3FdJjp+gUYMrMQCu1VveTY5YBqJqUGUg11haJBQTZSvabaawYQ3JEEI0EoR2vACrLQlDJ3tCK4UyeQPYc6PDccGLfZCKAQteiTrjeKGV8cYODIMUT4yLcsc4EhtYxY3eFnnqshACwkmphaGMZk06qMOjpXgLrIbqa6tEwkQIIhVuLv7eiKF+1nbhEsuibEcQBPjzWHelQC0/jKoGwWPOuDvDed04G7nGJIpqtYrHH4e822Za7TIDIpIQ/B646LkE3nAkpRu2P8AzJRJK3LRmyOByYGzb+cJiLG8ft2H4Nvhi1WlEHkToe15cmmtIq8rXdCDi8apEqGyr3jxEuwn0Em1Dxm2oLUt2LiNB3iyoMZjZFEAIJtLh4q4k2ptXWydMcKBLLWQgIw7ShqMbigCO7ECigNo7OLDrWiJo3K8hCaMhTNDiBMhyEKROsT/AGhRBCVEhStXrBNAwoISCRt1+cc3ssMyKSPhw0dsmLlIBSx9DU5MAgy1JKLcG5ITESogMk2SpkJNmQZWYY5O1CtRIwzkqEtgdelBy2PG8KQlkGByEj9MgGPqVueWCeMoiUtAAm2AvWsYwRgIREJmybk1iM7sxHgZWPc+2RTqpPJGBt1s7ucBZrb97tjQi1ufA+GYDx9UQ5MIepGOncmJbByHaRPiTCTSTsvJdDXRrpwWAKiGhkJvNEIWQjEaXJIXhKQYRHVM6xPQgTlnfWntsTkyXucaLO7NRUoq3WDwiuCDmsPJpcUTMaUsyKKZ+cLTgMZA6ROGN+MkCFeecQNwW9bLE2YWlKVAWhjIGxZhWYnBqGqZ9q6PqY16GeyNr34xhwLhZ/mB+CJVrzh7IfWB6BrCxN4G6leMoQuyDAHjAbIkQChMCXJhAEBCREGnG5NDACMqUdPZkm2o9ugA7MyVq8ej4AaZNCZGUJNxdYMpmcaHCUmE6WU5BZ9gYDESpY6ickKJ8gkh7SuPCsJknzI6lSySYFKhjGSLpQgQqI6mtIEDEszjluCYUEjuSkwlpeRRhK2EzmiFLnA1HJgcejRntBSTf3tW/t1pI5AqFsTCvgBQiSl4B0sAqro9A4ky5dsUqxAWQP8AGPIzRltsUaNzD3jCVpVgEQsktsTG8STS9Hh6++QeCgUHYDtW6s5wpIC+i1IU+Ga5cZxtFBGa4CHiclkiCXCV1Y1PFUuPIg4z4MyJSw6WYNKX9E4ogkCyoxLvLvIyqYW8iZInk1QkjmjCStYVFG1mAnWAhJYoi4gbuDLrGKoEhxEo1xMmHBYonaL24WSymExxghQIQGG9NXM01iinFVUyeokD15wEPLcaUs7yYYjRS46jzgyhBniHr1yAIEKkV3PWIWW3yyeBKo8yflTJWNdbPnCWMCVLfU4X1CASF0PAsVgBQdPOElICtTjOgpXAO8F+qvFpF9CQ+MBWnaIVEn0zQcYFLmSe/fEiM6Dj/cEaFL8igxbMARLZmjMXWRDAEpZnSI3hIYpiLVJOAQEySxhgqGWyEsIUYYZNkgvYHtxBCncJJzzAoUJnEI6kH5nWWIGZBCl0AoL5bU4CM5QJFCLcB2cm7zixUcOBEO1U+MKMIWGMaKHiskRjXGSsp8RFMyvEtu2Ys5EHpMelzMRg8OAlbudv9x4vSqUu15f3iBwMREb/AN/usR2F9D79rKkiOwYjAiA3y0R99sGPhu0+/wAxGBWCIHXOGinBzxzr73ghSo/X3nGbDhOyRHIKRdMb9H7OIvQryefP0yInwP37xkkt1ox584aBCQojqNf5hcTb7GxNpQ2j9YmudUKbB8qtpvWSlVJgboXYXi+MNACHCwlSZUxDeIzDuk4EvhRh/GGLPPYUqqbUzX7yZHEy4YkUQHTmx32h/k/GMtNENhKkMwTVV6SfQtOpsCGnSEY0+4hKJCxDdCfwZ0AelCGxdTMksbc5dhMKNCq7OqTg/wBdMzuIKHiDzrJfOceBcHlG8UxSVn51iJFYgZpJqxbtjJSRJiNsoxOvziyJoWSlsbQh6bnHIlKkUlRBNmanvGHR+zoxgBX2VRrCycucSBiBpBbNUZGB8XpSlyXIH8Y5ssqnKCIFDZNXxHEY8IQ5Eqk5CIVXYyw8im2WIDKDywaztdhgJPCBLBKEMwEORJExXhBTG4wbxxEhCJiFITIEugMKKWiSFDMtaWpZDh0aI/qHi7zUUJyNB4Lcb4QrCygM4Mj1UG61zrJ35HpyATMATUS0Y0FCjREsHh8izjGBiEGIoSeSYoQGRaAdWJlNIz3A8zjPPPyAp3/k5FtaSAQFigpM2ZOA3UAYMyrRMkyjDGWUKkQEB9iVjTJBGb+YcIB7iR4QyOQoOTx4F3fXAyGKyRwCeQRp0kHFMeooSJLkI2TBA4BkSG3Cks+Y84xLQBlPTFCDGsfACNvGsIJhMmIwDEhSi1fSdYhW/VjbsQK4mX6DHkS15AnCrKg06om5sZInHi2ML8UMSFE0QKSR3jNKHISAndvYcQNDElxH8VHOI8RDPQAmK6dltBUvBFFoHR5cKk6qA/8ADAZMhDTPJWphZFyGFGxg4ElIIApMC6AX0BuMxSQR4QTLZcyJCQTA1oUMzQgxzZEOCbZaNDQBiBwS8dRgHuV7jImSOQAiFyohHKcHIu3uMKVVENjiDNGZhxk5S/IV5vKGSZoDtLbRCYq8Q2Si0daH1yY2gaf3/n7wtVdu/v1xM1U1dyf3+5ZCvQ+3/caiHpzOTPjxlFNdmT/6a+/zLmN8e334xuBsKjrEmOePv3zgKk+2sShljiZWeMbrQ3YfvCFtHJbHeJiYnSQZCYDDdRGNHZzU5IA1w5tQw7rFxQgKB8mn0cnJiBB0nA8MYXF1lohFkJNhyVV3ahpAmFNI+uScC29zB8sVkPb47xL7pxigy5ZMcrmPGDdESiAlkMoIHYVMYNp4tsKo1C293c5ffPBEVuZDtW8RrpHbEou41LbzgiAoCVXZDvjFXCPlKxLI1g9PIlIgi0k3camMQcx3OhnsUtvfbh0hEiPtAQS3eusbbfV0jAcwL8PeKfUBm2mCVXM6OGRpKxQYTMwqBpKjBsdAEpEIk0Nkyt3jRWng3ksJDu0IMiCC+kn4wTDXeGX4qiUFOgQwlwQC2wVkgRXaN8syg5waSOjeY2Qh4AqKWQOPDAisluOOMMJpyglAIoOwxqchXUsJDCykUzDEgKcq5SZKQJUc01PWx3chQluShJpU3OANGGTLVDMCBMaLXkLBjKkKAlLp2eDEilGUlJAd8EClR0IkhVVhpLEUBmLjCGSO2GQPDtO28OrkPKicXcH4vFkpdMLioIWARtdeJ/6uVAsBFyEaBwwjEWS6vQhwnJZEOHY2QQqpwEBibKhF4VHjCrBECz1PdgSlGc6HZXIMJoMjE0eqGDk3fcnGNctKiuCJId351gFAJNeQjXQWGPBxmhJkEvdCLu+MMrI1SGvHnAZCoYcEBEdRif3hOjNsKJdgEntglFmZKoo4mfjARoFIyiBvVCcVZuXEOeyC4851lLaWJcm2Ds1kS+omMywiiIt6d4lUwmE6A0GKINoTAvE8ApotbMjHMRhNltluNDiMvgAX+gxwmwhMrsmESmL4KQtAoVyxVRJ3il4QFZmCw4hwhOWc4IC24cxSREASBM4M4hgQykXI6ojkxGVkEABtLcDA0LollhIkIBcpJwpyLOGxSB4lN0ukwOTW5RIExS0Hg/H9xATDx191/cnsTu7+/eMRS5a0/fvWPo+fP388YrFaKHr788ZLKFPE4VMoPUt+/ZyZWR3d4oqDzkMITyHD7OQoE/bj7eRIEp4+/fjFBE+t5ByZSTa27v8A9woLROuMZJFP3WI2JJIMfzJCGGeYrAiJsbwDmk3eVyGctIWNxkXIyYJ4wwKoZDCVFkIZwk3jScqEk8jT7YAjKIPTAhcE7/OLgLNPA8xjZmNDGj65O5pBqeHeIyaZxTlxFSoA3d+CzfWAhgiOT4vFxr3xO3ZP+zm2i7VpwN234yZy3uGh6TH/AFkGbkjoSHhE1huljOoEFbh3jk5FzYUShCCiPS8O+GQIRKJil4ffIoxxWxYoTevmcnY10xMj1joVoKTvGFg2OJxglJ24cKsz4VrosXeIsImt4nEyAFiQSGB0uu2QcKcn4SEOSJ0yAcSZSFhWRSnAjcAnQIFoGQiW7bx3jEgGc8u3CGzMYat99kgYJiI3FViRxKin0LCPcUFJOxDIUgaKWxokBV/mMGiTdLP6PjKWEEmSrjKRMPC4slg5qhJBuRqSVwMFSuTmQsYszhVgCQLEJaWGLjJoDU0VgAdQXK9PpNyXFjRwHVVykKQ1iD+XjxBGG2lC36YQDlYUjcTASSvDiyeUeOMYClImpQeS9URzMFhyoT5P0mredRJQweS+hO8SGlf3SKQegnJGRxCJ41YBoHx3iIvoqLaUKHyVERkxQ5ohdgSALXSqONwwVbQEv6xGIqt2UfzlqFGjJRT6cnWGyOGM7AE+MoTRRDxLgSUbwzGRgWSjwUVehwYQawDAjbVVLDsZdFCDBCCAHA4MSyEmhOiXRPz1jTCSwBSpUrEKImLwy8AlESS2TCoISwuAqwm2wMzISAUuKwJ6lYDQUbG21W2Mo1UaaQa0VOUJNMRRZFmwobBjULycNOUeIpXSwC3bWCERVGKKCkcsOwm1MgTB6/NxhMimyeLydrcj9WJQNR7m4AMyqNWx6fr+5BmG4jr79csoenE/f/cjzHZ99v8AmfLG5+/fTKeZj8ff+Z6X68ffHtidY89d+fv2cblfnziR7Ya/z795yKL4msiAzooffv6zw13i0y9csCb68ffs5sLv9YBRq0RxGCYrhR+6xMyKeHJFJrl3k8y6nBFyXdYQRIlpyVzxfoL4mB8OIwSgdJWQSLEKumd46aYbNmBE6dZ7cWNfGLShGApESj5ZyQZAgZNPJvnbvKIlHPZjMhprCVoy0VkDqUfTWO2Oo5TzEq1F5LSpLiNEjwhix65FccuWsIm5d/rAWAA8WJZMJcB2AMWgUmL2YkOR8OaNKUlAmSrgSBjhCm6Q0Bu+4qYwThWo6SRsJSxEzkFE8E/nJ6XUB6S/usGGiSWP0R6pMEiNUAaXVemEMNAm8LsXXrhc+ewU+DDh4Qhaseg0eEHGLirIgBcWnsO+RiICREApJJBVlFLLx99E1plAbgil1JlyIz1JBoknAMjB0uQwzkkz9w3ouOslfvXVh5DRC6JeGRqzxRdwIUJImp1kQRRGpuF4ZnpjJcMKMHCGzm+O8EaajfwEltmdq+pkcAAsSCzWn38ZMf0yUAh0LRn941BQMt3A4VHFHF4TCLSynzB/7/xWCQU3wT8kOBDAGDsUibuwAHMvExynA6lTrhGi4PSHQAQJOl2OMh4pmiSL1SZ98fkVAFfMsyWTvjeSSwhSFtnXuQ1vCLHCiBfMgD0RHnIO4KoAFoJ3NhE4OTEyCApo2UwkrOclynSCSGj6ecUFEIAHCeXatRhllnwsQUwJHlwQoBMoRBI/8AxcQQkqhl5iF5F7xgsqtuP8DzQlA+VlehLrHi75YECkxKpSVfY4Mp4U2d3BQXzGFiMHYsTbxgHVAgxZDSyqiTCJVdMmrMTzRIEYgBS7ozboxHdp5ZaClIExZQvNNwEO2J3bQCecHVJr0drMhMaFm1wRik+wdbfn63W8VRX7okZ0GoyBtlfrr767zoLXR9+95vVzrn7/AHnG/fRgTezDzs/Gfy51H38cZok/yI++3GO0fPWN79MNTPrjuXr5zQfM5wfONO4nOuM1PGIspDTkhbHphaij6MIDnj1ySh3NPeDYTe3TkhdneCCFhneEkM8Q5xJZXrgE6mvfBCEMJ+mv16YVRp/LLg4++OmsYSGGYSTCWcQoWzycXz+MCkospKO4tUcJ0uZKIGAKhX9YFT6TlBpOuqTzkrClMCvX+eccIxZZY8kF695SNYhZXAQIc43s+bo0KRZeB5yQKQsKUAaUK7YsAiMkB4U9985OACBMSKRPl0ZbAiQSjlEYDwS4BbKeddJtDgO0RmDQXGuXrkliCnNbUi2BIxAEchEEhGG4JxxWRgiNJ2aZUTZqSNE4Fhc1zTVte+Bnh05AIaMoklq4ycbACBA4wS6LsJGLuINtiNIWBgg1JGasg0zcBwLAHSOLpgyGlTSV0PZSJMN2iQEjAVElY4cRhFhjfKK7A2159Ml5hYCfliFhitY1zSRsEcxqGtNQUjNMRbJIA2C7rKyC4Sq6oo45yK0m4JIhZJY3OzCthx6AQgliYTPnRDp1Jgh3Kqp9NdZFXKdbFtV673jhgACG6ip41erOcD2XLJKdIW8Q+/WMUfMbJA7BTXrWBNGxkJ03BMcmt5Xb4Is87sWYE1XOTNwdYS4y/EhPHWDOUhvQinBVNASpOHn01imUQEiGghS2nqxjrLosQCXHsWcRWclEzKV6DcKR1WMEiVpXYSXAGfMYc4WZO4jGy6FmDJzUEqkJsRpHO8OjVVENUJEo8M4BXeAFSaCjRFSEIlAyaKx5OxGo2xEIUU8eUUKNqT6x5Vwq+sdMqgnanpY7NOMULEp3AtFsiqmZJ47HhfBBx7GVmARA3YYjOSSrnFaqikdpGLhb6XTpEBDoHQ47eZtnBaxf86++uePx9+854O9G3/3+7zfo8bfv7xsOmo9fvvrJ7+/f/Mb3x7ff5rGvUvqP8/mMtTBsgiPv4x9vEGs/59++cfeddjkd3xO5+/nI+e+/v5z0T3+/dYPTE/fvxhA8B0+PvtkwdR2ff/MGFXY4cLAePH37eRKQWeLxgR3UH3/uB2CuMaYud4yDY8Z7jFYjo11kCI4JGn+YpUMXN9ziyCDTSzszYDyMGkEAeR05MCxxRkIpBZLeOGgwBDInrpk85BJYxRtH8xuiEiVN2RbkBiTKHZdcVONAQAlWRVPBghl7kd3bB6hHhigKZkSWmJJPg5W06ecIXgyu19r+jG6K3k/FjfRbOHDEskB31/JhRsSdr3mIYwY5CyLXjWU+ItKDZwghwxCYU6LZ2TAROyDFznlfhmceKroGzi7X5rxgaAD2IAwwCBCR7VivyOIVuN7QrgkdxUQ5KAAFFfUpchWCZKBhO2WUIaO8YUe+hqbCTgSERLG26pQKSqLfkLTIJrglmUR17YcdFCwiYCtv+454iARgJglop9ucIfsKmggsFoZE4ot8KkrBAWRfbOsijYhwwhe1afy4tgidjT4cTF6cqMH84BAsdvHJzOHShEncWrWsNyyDBldM2s8UE7w497tdBIFnW/XEWSwQW0FtKcuA0CHMJNcSuDxMxiZOQEDBl5RVi4TEmOhMA1CWkBhN4VnIW92KB1oxd5IxWekkYzULIWUByQT4caU/4lwHyL9MNe2a0L2YJL5yIWcGJGJXsyuTUtqzOA4CUGYDy3xWSVpIQxmqIgMbMLinZJqJJTQdrFqS0BVzLNsuAWFSUHKGR6mghEegmDMMEgXHFIh2FlGwkibe2GTe0NrF3LJLe5DBWYdq5JNAquKCJxMIpEIvy+PlDggwUlMM2fAV8kejPL5V1qOo4NGQphShqD/f1j8xy/fu8j7/AOfe83vnx9/9x7e7f3+5sXuu/v8A5mpuPT791vF9D79/WOuD0r7/ADnIV1XHH38c4/E8HGHp4j7951gRv07Mmu/G/v8AcWOZ5vDXeb6yYsMXhXecntOeV8sJ0x4eXJUIe63lA8DU1kpS+O5yFVMYsIq6yttDj44aTeDLKF3OSDCTNf7jC3UFYS10MWoBJxwf5kqwgqFbO8aNYIhJOTqwkjDihEXBsTt99YhQ1A4atkK9IccYgy2yias94neQrckIgJU55TxgaHCCJH3caxu0aJ3jZmBUFUwTEFbxlwJeaWWW5HZ6YBoXSteX84y0IVFuECT5ADCmleh3eV3hAPKjgUAb9BwyB+164PIOT4/v+48LRlgQB073rQ4hQ9wqYdCDXUo2QxU6AkQrlQWJJ4GLDNm9mWtJhkhbmBwuLidCwDBpgk8IBiZDGR/m6FhFKIy2ahw+IIqmQhIYAQU2MTkxXTkBSqaON4HEQZRshG1QHZgkOGEpCCwIEQWWDjEMEuIVZa5SHSQfI0f0JJCl0yJLvqMHYLLkE/M9TLk4sjg7zEzE36ZObZIFLWEBoHXrnJ6SENA1XxERxiA0QU4UDpwffqOwGMbZ2c+2WcyJCRIIpY871jmAZUhCYOmYY9rwo3ITnNCRke1suEKPWtZAXHMn1wYVYMx8kObkJOo1HZwQg2iOYJPjDcaoESihPuGGEFwoNTPZSXnCg4QkUFAoyl21qcd5gsHXGuMBB6IWDyvGGm70EDaKsBBnrB8j0C63hKEQLZAQORZXG0UEoqA9gg0UqZuABF2IBoJ4Ge8jjJQYodbXgYmlVunYdxuOAKyanUUuRm4U9aAYixKVibQOIuUESp1Js8Kq5MM3HOosXG0tlK+/zE2iuDXv998Hfiuvv2cmZ0/fv/Mb366+/fGbfXn796xZvU8/8+9ZM2819++l5Zvjx9++clPEffv5vNVqPv384nt9+/3Px9+/8xYGPSPv32zlj4+/esmOnx9+9Yvvz9++mOjmsXRP379nJ53xko1DHjJueDE865+/fbE0aO+vv2sGZ0DdZMfExaZufXNusns3G8CHBOcaDx3hoFJzlQIrjG2QiMg0cxOSuphxM6i5yd1VSxrLYaV+THZLJ6+Ml0ESkb9sgwj+2MCVULRSe+GYCNj1u8pRTz4xygk0gq8gzXSM/H384Jkgl9YCzt6ecYe4hnuf8O6yF7CUsM9E5lO2XgyxGCFRo/37xiROlUouhZArriMQnatETSBBG+vTBHwBL0kLmSK4yNRYyKaLNCiuWXy9hWhLo3qRkIDmVwpSK+WIJ4kmup7trliQtswgqZTasY7MgF0L6YDgC4JyMQyNqwwMtqdtmGNSQUexJOjT/cSYOoPIEG3hYg5y3aEummAq4VSAcYSYCmwC0K2JKtuWzS9Gd5Jjgymp3kuABaDbARDBDbMk4wW7Wx6C0e2OPdE5ps8GX4nrHJJJKEQlosR85YyEzaZq7YeZTIaRSacLe2J98YBBCNvTmUw02YRTYCFSBS9v5iclTyTmClqjZUizrBNiwWEjMw0mySxx9AlE/oWUvzTxh9cLvomMgM0waos40YLKIloi3BAMAK6nEG1MUaIuhuvRNHOWTMZoDAy7VH0jJNkCC0uL/eLQRbs2YLtsJY2upAPRaWEmIsiIyZQUKykrbOQJplZspncEUBwFkkxmDZGyzSzzm5seruiUAbIJAYVaolVSAyEksXLJL0xnIYSIG4phJgWypF4CBqtYshGvQUbtvGgAAAYAaD2/3eXd6I58/ffPzPX37zmj8H375yeJ+K+/eM+Pv36Z4Ul34+/8z1Yefv3xh7Tz9++M971f3764XR/v37zjuvH2/veLPUJ9+/OL6WX9+/GLzX379MWm9d4QXuPz9/5j1uL+/fTGg0+n3764qeL+/f8AcO6eMC6/H37ziczLx1nNR9+/THj84tZQX4zylJv3xNkAIZx4/ucOTnGwqXhjDNkmfOQRJDpxCXoGIi6xH0oDqJCHxc4KZE6nJgChgcj7ORSd04spW8SLZDYSy5aXCZK9BqcVBVsQcvn0x0vHM4tt7CwMqqErRmLXIqYwnq8/f3koZQ07Ty4OBPpkChFZfAj3QrXWnAmkyO53593+1hKDCEMLGqOdf+ZCoIZQIRdLn1weIEjaiiAEZUSdsf2w4ElwZPCkdpvJWyfuRU6EchMERiugLaRC5JStTtyamxuGaFKjEcaYclPLmiFGA5COMusFd7giInUAMCYm0xZPHVET5hwjNIjGXn03EOJ8xgK8kiIkHZKuAiZVckROGEirFwkkTTq3E1NjLohMyfJHs0RBEBFBVHqCPJXGOo3r4IQKLShKiB7xqHNqmKlpCUkiJhwJudRJXR9vzZwqBgPf1i60dYsANa2EPVZ27jEVQKUmiyPpNcYAs0pzGI62qyISCRtrkU6rDkEkJqknufG8vGm6gVQRdiHAxOvqVIBisNUlxIENG7cYgii1Df4BNqwxISqIZFUzG5dozfXoaZkck0nfePEZzWEO5KZvWQJxPhQfglPJi1AwkvASgIHdhc4jg6iorgABAAMCcG9ZlB0AMCRiMl6m4nYB2o17K1OI0FESZFpsE+AryZZ+QIRr5FlSeaaMUAbMuP8Ab3t+gIQgrY76++uCbh2j4GRHj06+/OcbieuT+/3PeH9/fzmvHR9+8YnE+337xkXs8mo+36Z6+5qPt+mRO+Nn36bzxtND99/zvC6L65+/XN+T5v784l99u9/ffG5ue1vCYmff794wJsfRc1p9HTjXMf79jEodemDXHpnRRJ6ziuF+/fnBPnrInk7jObjDK7e+MC+qhOgwaaKhnrJ1i7BkJ2dYyJB4yRlrjxjBcrBi4CKsXRL+sY8MMlwV8FGKEUpGSITI4aJvxlZEI84EwczGIQgkb7YXt75NWusrEJEC/jGiMQwP6wtCRudr9+MMo6TYxNaPGHCREjC08YDmhIRy9GKIUi05f87yVNL2+Hr7eHe3s++v6yHPk5FMtUEJHLcAmBFdPRhVncWUKTGRFNXwmMLyqFSrOW7SlXKrKQFSMxQYWbGWJmO90FeHEAyaQqg0sAoh7w7FQdUmtTCdRmazd8QFFLE24TirQSDgwtHEOgZY6Yllmdc0hFGVBCIwmOjlCnxX8y0wIjArR3zPd4gOKYxBLCZhHe8XDUmySwHSQK6cl5vpLa3BqNrPOsAHKEIeRFpD75CT0ylLhI0qMaY43kshvJiImk4Gpg1ZFtMTmJFhjb4YYjWTCMtigBIDYZyUqUWNQirOSIlN94puuABNTxMRORJkMHoERgBQ8usSyMsYhmVEsiJmOavJCCgoWpjCwuyyvo3aIAF6U8QPteWuLkwkyZ715g6MDaW1qR40zB3msfDrTcKElBoTnG0wQAzARLeabOoBKQXuIxqt7EiYg6IEcNtGRPGjmxC4AbbeMQvxXWGtSTEDs5yTlaYWggFBEpUg3gOAuO9QdDQ7wkRBBED0B8npXvOUp6dSn+V6YplEOYe/3reQFEBqfv3nNW1O3c/fzvOJanfMz+/7hXidHc/ffNSa/vH34xA3B4++5+Mo3UbNR/nPpj542aj/ADn0xOHZs++/pvEmvg+/ecry8b+9/nG6seb+/wBxubnt39/uLvk5cnkb7+/eMOxDp+/TKNV0/fb0wYejvX3j0wouvv8AzN+pzT1+/e856n8/fznNO7OZx3Wuvx9+M9fj794yyHEy8RkhOwawpseC8ZSn2/zBJa3lJbxIyJ1XGQTuOMbIoe+seUlh6LCT8ZMRJaxAwjqBEDKRv5nJsgQI+MiaBpeSv8yJZjz1iEFC5whik/uC/TjGLUb1kpSZ+hyYZqFgoMERCoduJmw8hqN/ffOknqX9+d5IXwxGrr8H1w56QIDuVkgtu6yFtsSkG2BmCcXHOOIZjpUI7IJgCoveM2ZAzwEqa01y1eI7ISjngJZRtPSMgrBiFBmnQorB5yr6fdhOhC2YiBye4Gk3YPIFBpBdGOjQwLQCYwplNen4zgRGWXIuQNQyHlWBnl2GMKIGiVC8ZwOkFOUBH9Jj2u933i+1Yo5Ui0oghzeXZBOEcR7SD2TOBbLIDyBIlyZACoirNLphJhYcIjuoThL54ydEQqEyDl1potf2I6SMQOoqsFlsKVkOOTlB9A4bjVcxtErB2AbaFAoFmrV4ck5ovbNkLhw5xQzm0M7RqeGSl5wEMVIc3xxWSCoKKaTNExFgsYZPDCIJYFUEbvLJfYRiToMSo1zvA9JWwqDUtrVAPjJaBTkqhH+KagMEkCjks/aVfTEZEwug4yU0PTHfJ84AO3v0wOJ4InOBISiCODDUDrEhPwc7csLKKoWtmxGgo8e7FDS0SxTtanmwwgoCeSo99K1ajrEC5Ol1/wA/HOGkP4DzkQ1X37+9ZzPy/fvOs+ual+Zufv54w8V6/f8AuVHXr9+63ix4/wB+/wCbyILoNmvvPpzhRcVs1959Ocl08bDcfZzgN9H33/esetnHP37xjDv+r+/PGN7h87+/3jC93m1es+Pv2cm5+HWMbPZ1nNenvjXIY08dffvnJfSox1P7wdRziTo9ucddeMiRqmucSe0MGTQgjeAhFknO4yJ8F4CqoiMs4h9IBtW34wQ9VHgD/wA/WCWiaQrl6c4zHTU6NDH3eIAJXXri0TIyVzglDtyCZ2yzAXkWCZ47wMCXpIy0iSFzoxUmkS9+cMiF+/M4sbmVq/usMMCpChdi+f8AmI0eREZnIohkATHhtRkAZ0+pSBilcp+ChNIggMwEvMzmw0O0FJTuJcwrUlVQk6MnDg0yux2xs5MkAEjNaRTw1EjiHbBCBLQC+89ziEPGRk2RgZPGrjteMiVtY3kCnHXp3gFgkVgEJG6/IdZDw+Q2T0JCFQTeLbAOEWQiAAFwBzP5VqeCvSpPvhBRUZOjoU02UamnkEm4sWDkg4vbesUJPAzvrS4QfPvktbUBZAChGUU/WFtwaa9AkcAOZvlMASpAcRBY07ZXZlSKpcJtWgPnrK5LsCoiX9PeNhEbXLAM0UTKbDeXMEpJJJs2JkEuZTABBpWCiQi7Rr2TpvJcYyvyH0HnIthEuoJJIBU6iNuL/AOhjU2G3T1OTRQBbGUgqY/R7jQGe5ABHcQX8c5F+B1Db+QfLgkyYfmFavviDZKEDDieJwRMkADcjZxXnIzWH1AfMGQjuD0zjo0zc5whd8VRoroUjSq24BTGplECj+jxhLVOBeVHsL8tt5qMBL4h99+/eXMOE8B3+v7kCTK8pt+x/az238ffus2zBGk4+/dZ7es/fvGNTXz/AOfesH/x6+/8vPt8fft5zx8ffvnGnWqfr97zXtv6+j/ciNn36P8AayOIPv36ZNffv3rLb9Pv30xu3jfn7/zNzJ4+/fzjuPx9+++RZFzgdbdffvnFuivv395NePj794ySNTHt9+8Y+ON5MvF5E+/4znRGvv384oE8G3vGbHhy5e4ciUBnMcTklMUZwIjIiAwodzkAsWPAf7iydblJM36YNXIgrNggNpqHvEfEQCjRCIA8yAkuSacgb71hBJFp7B8/vBl6YslDmMNH3xmxHat5NZNrnEEpcunGQJOh4y4xLUODBobTXXP3+YxB7VJ214Av1jkwvWygwkshm5m2WnAUsuZWZYeJyd8VT2Yw4s6wR6HeUk1e4FT1oc0YeChDRIou0UGLASZF0mxgsF77e85DKuytwAzlVafM40KJDQFiWmjJHwSo/WSCt15Z0Mhya84mKOlABYStGx064CY5giUSwiqVqmHSVRJDsY2WP40GoBWTGT8BkQsAHMPJE0obvm3A09Qyp00AEnIvrkPc8OUS8pgTRsjeNkBZp4EVlXbiIbpmtKFjAlIeRrjZhZ+AIJhcOvL3hv5N8hJPno3OSuybouwjQDtYcGR2vwVANa67NZT0yUyCocbmg4DjTNJfKqzslRZUCK6mLonkgWRKWwZHamBpoIIBeHq93PWEOR3ZMS/NL4zaGbZWLBev4e8hl85IlMHSCnB5cIXSmjFAOidx+c1Rrc9byCBmhTCxlScC3xol8+cIOTiCFCF7INYc4t3m8ugCq9HeEkgWrzoeX+tON4PRVsMHwXnk7xAbGwvwPfIBoIKODr8/7m+N8ffveLPXUffvtizdeh9++ma6U9o+/wDMmDiruo+/8zuI9evv/M9qfx9+3j3XX37+cm5if79j/c80+e/sf7nmo7efsf7k1xfP377ZMERH37/zNJSPv3+ZrcEV9++mLG4I39+/OdkX19+++E8WvGLOjej797zdgJo+/fOKteI+/fxj4TBkzqNZ5r/MW/7hPGs1FXzOUPpvvFCK6nzOCS4nHM2iMiTXUY0qnebR1jowQmY/GF2y79WQOvkcE18698DUV8SanAcEYLOMMlnjkDqqwWBcjkJAEBQHyj8DHtcQRd7/AEOLDrA1SiQaJwJZIBx1QZ1k0glmY4yUtLUd4xDORKjHQRA7XHkwBoXZ19+1gJzaOBbRjTjTi9eGiSKXa2DdOAc+pzGxV+Hc6cUUCXGpCWwEhneGwhYQYMUuEglow5KzKtjzQhwRDktAyDroPpb/AJjCAM6KD8gU2vWN0AJNFRnYB0esezUVBjaoGyuChJolCIyJ5xCwFwHVOhZ7I3hdtJKWJskSSSzKnGMKtGkLVw0H0Gp4xjSR5BiT0AK+OnC6E5sWwGUEEsUPnDkioEXVHseOsIR2KMvFxB7XgxAlS0ipZ5Lfk8zDBG8w5xqiTGZSB1t6xPGCDyH072sK8c+GIPpnOU36xrII3jkFIOyac9hzKZcZDBwUEeMp5GSdZK5O1iTahv1P9xn5I7uPBKsRTWsQG1cBdlNAx5Z4zacRRa2lEHqLvH34UGSXP4yiqCbH0YUOAgVJCvyHvg0dmsgBoqmHtgLYVMcpNCn2nxiPKqd34E2eCesF5R3I18RRF6wjQCS7dmHmIPacJsBKYiXx998Ca/03+/7m/R92/wB/3NtXNVvr73rP0dffb8Y1uIOq+/zP5fX/AD+ZH3UR99t4b/Fffu8bjnitff8AuPPMdWP+698T0Xxc/Y98PU7nY/fzrO423P37xkVweX791jQ0HrUR+v5mvEVdf8/mMiePv35zsr0fvv8AnImeZ4+/XG6dPv8Af7lp5H+/ffOrPb791jo/mJ0lGc2cdayPS/xkc/fv/cmgIgIny/8AmLZp/uLJaS8KXzeGCk98UncFbrIUIyGMQJ1H+4dRzfcE4cKlVREpqpPceMZQXpk+tYKtDrCPGWKAqDpbR27wktA4zDsEksJ2euRBQUJ06+MY0RMQ8YJECB4ZkcMWpIMkMCemTEmOZrBchpfjBIQA3yplxBBpP5ip2PSEx6YBFHUBdx2Prk7YXumnNiPIfH32xRCViIpJw22eSd4Z05OFdXoPKYYSrHAIDkB58MmdzKEsIccvdONHgrFSRNRXX6MdDMyVWfn65bmiWeOvvxjISUygljoxJHMHcHPvlKIKY9MpJpuCnhRpXJkys+RoGSUlHddbxthZmRj4AD7YMiCLSYDyMg7h5IF6EDIUSrUosXpgoKFkDyjwH7M1PLih2zorkLG8GxCJAKpu8kIFRG4STvj1yZ93tgmJbVRcrbGTlt6EqjHFX74HeCgBA7cVLQeuQJEiUm+Mh6ySHyf3IzLIxBYdjBuowDpXAAIecZhPGR5P5IzuDQp7wMUaqKq8rziQJxStLpzDOTGGSzFdfCCfTLaB5HggjVXHC5MdbJYhG/whwmOSgQgg/gesVe7iCY6x5kz5w80ZNpAAfS8ien18/f7kQ3T7t/v+52792/vvjq/Tv79Madkn3/z8YEdVdff+ayI8RfX3+Z41z19/mHt9v785+eK+fvziQ9/kfse+J6P5H/f7gS8KXdz/AL/cjqH39vvxidx719+mU+x/z+Ywaij0+/zGuq9sjj3/AL9+cSlYu/v28iD5+/e87d/fveJEa9mcmLdhw5DqiPb/AJml0P6w+P5hRJ74UE0swckqScSYIxPeydBTy6wbTS1/uPowluJEu2HB6Q6n78YhzIA5VD+sswSQBKtaASWxOjCzsF1h5SHHlk8Io1kuKWHYcK4DtkFBMilIHUIaMI8RWIJPXFP4yc1p/A/UPvhnDHqpaAN4I2QWJeg9D+R5xQKKdYBJEsTwY4KoUYgNoZqpCRHPGQrXyL+sJq0gxN9NYIYkKerHfjj3xM4lhj0MXYg5wBjhEooZekA9peOpBQIBAJb5O9mSxFLEbnFEqgB+94fCpXrWbfAe+TBbbfU1kkToNfzLQJoOFZFiGC3t8YEjZJg2L2g1eqimOCGDBTAEiUhhFRKZ8uR+DE4Om2mZEhNkKjOlW0g83zQPc6yQMBBIbe3B7j1yYImOt9qE8X+cmggQI7I7PXrEEaeTnEHwBIuip1hHkF4NGXT7YkCVNOFJ8TeEzQnhyIEFBt0EeqYrARmkdD3Ee+EnfMBgjPLMXuMQQluE9gpSvcOsRnTKx0hX7yOQPDCiCnZJ5WJQBAzMW+/WSJ/qURDaIK46ODE8IJIDsqDX+4ZgEiixMmwGB73GDuC1FkQIs27xABKYbtPqgfzrNzzkeqbefv8AeM3bF7W/+/3jHt5qd/fvOO9tc9/f/N5o4I6wpqov79rnK1+Fff5n44+/fOs549Pv32z8xxuftevGRGmejc/f+ZHvF/ft5E+efT7/AObzfr8R9+3juo16R9/HOe4xrj7/ADNc6ox9o7/n31xtkfVcIZVp539/uNXp+fv9ynp4vGuQ85HoZ8PxgRrn8YNDbQGKSiGKDNRcvpvGF8MImhHnFoYt/Biyy6yYQmp3lJwoD13ksQsxfEGWqCvO8stIqeJcFZhFgCFFCZXze2KjBcTPeOckKyMy7T5vDSEQZJLT1nJW8A6YoeET6Y/m+u0g8lR7DgKzpON2KHcUPpk18kSRFQ/b75WShFRkULQnzhhnlXeXmdqPvgVRcqzzgzLgiiDECY1hKKC1PWaFzDE+ZRvQF4jBrTCiEjp5gvFzeT4BTGwo1t4wgUfTvALImQ3iJDlW8kk7b9ctAlEMtdtHu5wVrHbifGMKpWbUhhQIV+U4OWMY1xEUnB4IJiL9sCg1AJi4glkAYKHCeAIDBfB4TXkjktm4LPSBz65zXjMYIhp4Sf8AmHEUe44ORNZCwk8c+P5kbxPDlYoSuTZkCzEG3jBIyCZ7wQFEbMR4Fd5JFKPfOk2PByH1/Fh4YGUEoAuJoeHeNJyyg6kkTRbU3E5PEbhFSn8rfjJBeqxIJJdecFBBQVDb4isRCkQxEsloLXMUcZeNQnkkMSLB5gIxHCn6Ra1HIaWDUSpFnW8yYOocZAERjf8A5o+3WNzO/v39Vibn38P3/wAx8876++ntm975+/fnPCJ/H37vDx6nP37N4ePWfP3/ANwh9Ofv3zWbvvc/fvpnC6+/f+ZF1fXn7X8yI9D5+6/mfnr78fy89dffv/uPt7ffvrjXrqvv3nHwz1H37zjT+a+/fTNvHf37+ML365y8nc6+/TPLE6fv3xnwPn799cUNGU0ERz9+85bAoN94C+DsyYp1eJUiuO4xYROOMQwDv5zU9W4oAFm8U2VB5Dzx65JVE0xLOjxcYJcAWk0NZHFRKWeTFVtVOkkSZyA8KdY0MRIkh8PH/hsVQEfDjMASYcnHvZkCkepUX8nHRnx5hXCoArqPBMnN4FIUX+hfqsDl3eKMVkBCnQtxD/05ISQEiAf5hZEQQHqDyXF8kVBXgxsSo1iEHYTzib7MmOKzZ9+/e8SCbKJ6Y0GZB+cUQGFcCw9VjuNy242YAJ385Fy87yC3cr6nBACXScbUgK7nERLe3GYFpL9+MeBfeMkizeIAjCaCzeLPJgMS0UVARQY04H+Z4riOUIVUmIcNixIWIIHBtHmZwgShLTQDR6ZQ4ubbAvLCXbGT4lBCc3WxHXnAaYoQQmO75wQvlQ4gelJORTDa+cDYIgIF5BKvPCSkFNCVgQsG426xgrsuRKs6n8M1GZ2TiZ+R6B3hoTugh7K4qMyA41O2PfBylxHgv/zEFASkMaTHsKrQ0wz4X9ZMGYkPsT6mzrAeiWgSnQu4qYcGtFE/YYVhsuNYCGOUcobm5Dex6ydNgZ7H7RL/AMwS4fxWKP8Ac0II74j7fpxnhL5Ovt/zPH4+/ffNur6+/ed5To9Pv3zeTMhtrn79nCHz3N5xO/L9++mTycfMfY/5k9Gtffj+Z6ez99v5ixrXHrnHh+/fneb431t+/by3X+/fzzjHHoefv/c346zjKTJ6jxj5434y5h2b8ZuAM2d+uNcSee8QE32+cMiS1Zcsvc+OP5jSA9zDSeMEGKJ+cYyoVxysPbGFuXJSI8OzlfUyfOhsAc+wLhzImKUWpwxlQzRPUs9bejD2L1i/YECBe+4jH6UmTVNJ8ovvi++rGmNETUzeMoNEaIfyxgROaIFISLAT5fc4EcAV+CLxBjLwEA7QolseDFbUCtQN8yyvbBqxd4pvECgDe8qXGWWw5fSccRg8GCrHfGOTUl5GGillZtrnWMW7NuWohWUe8SJCcBABaRkEwlBfTKApZ9YxXfW+3GRiUF+Y1gNBHePqAhUQbWfQcLYQAVsohTq3OPFyVWxiCMVPDuwAvBMLwZW3oGe9b3OJXjEu4IZSCb5pyqzeUy81AtUBoxQsTA0bk9P/AHrCVMpkiPHjn89UqA2ljj791gNpidzbkpQOAXBkoka6yyEO7zQho3cGN8tctYJxNAGMjFwOWQyX9hpUsJsJZlXWBbrRBQodSN3XjGQSpXOlYWMGIjqKBiW2fyfGTDtG5XD8hm76CMR1IFGdcFyUuRTLuoNg3Md95FtYc55PIPC6nUydOplSyG6uVyeqJIS+GxCR8zPprIFNdmoj6+mWUkJs1Efr+bzTEQnw+/8AuNsAXgPn785E6JnRv7/d5sot7/8AZ/ObJ32zP3+6wv8Arrj78YvJxz19r9ZySunUR+v5j49Dr7x6Zq4jp+/TeamSPP5+/OT2b/P387x3qH5k/s/nKeAqTmZ+++a1U6Nz9/Oseap4n79rBhv3PP34xOk1s1H38Z6k9nj78Ys6t6+/ecFU0/fv7whMEF639n1wuJ4W/friytssc4EBxO/GbJoxvA9hp7yuEhLOMTQJ04CcoeEf9wmyei26x9BfxhsIRlsJke7HxlagJJToDcAnq8mSycAFMKG6JbE7OX9HRBiUbJskpKy4a2UUlpRcZsG9CXnFpfvmxxdRG/mMEwRQ+dW+OsGWIiIcJ7CHhyRjnKIkSNJI9SxulqRRL9lkPF8uT05ygJczPthkipd4JaGiYuoBJTISSIvH5yWJw/fGNpSoMZ1WTR9+uOYEPL0ff/Mb00fGURA3d6jDDZEAvFYKYyXC4MABg9nOJskjf7zg0dYEJ5aIwaIOgwaatzQ8zw4twyhB8iiD1ywYjMsJNylYjIj1iTkQEB3B6IPWIcQXwWsC+I+z3lav4szAPvGJfUGAhZTdlENsTeGUgAnB1ZEPxrZwsIcD2TFKI/GsC12B9Pn8GggIPhc4Vnt5wmJS+KwhIN4x2vjHqFEEjKjAAzwllDjUizehwig0qpH9VfV6wmG6REdHArHtjAAtuMESlsemMFG2KHCZQqKE/GTNOK5RE+kiX3jTqCZKNAuYOfBksCHMAhG/EC2Wek4RbVYnsu7HAClXiYJBf2p7Gw4Nbw3IdkKL7nA+Iw2CB7a/z8ZJTqO61+v5kcfjVff9zdrej793nhc6N/f7vPK/z/2fznc33z9/us/L2ffus89XM8ff8zb54ig/zj0zTJXXEffxnoe+vv8AN49lHL3z9+cCN8l/fveIJ693M/ffHxzqbn7+cOuHzvOE46/H34zU+CEwZ3KBZr7/ADITxHH36YohI42AErWAVS447xSH/oxElvaemJkm6ydFy49XNGIoELvJDGBOKASdxvzGMIGPotv9TOM80IBDQ5vxcauMhrDUhNOysQBdLJQmt+KldKG7lDBoDpQiAA8Y03KqV7TFmC5ccGMgCQIrASQkVOJZGRufUwxi6Ze0PQgRtmOIyhbbQkIekWvVcuLSCN/fWRPRhUmzEEjEMmT9VJjCbgj84M6UFcDIlqWf1+s4SG0jEIVGnAGVlW8lQYIy7yY9rYwrIlUekZIMhJeiNYhMq34JyaVAXkVq3GehwZGSN6JS+UQvbJDXAWSQYdEvy4tHAnHFzF7yTxxtpN1KVU6hDljhEIhcvFerjBIE4cpRu4Or8OQa54MjXNmESJDsyMe9RFrFESA7MRiZEE6Z36Mn4OiNEFRkkEiHbEYKSSeDLUag3JeHkyEos7cAIGilKGfbEtAhzRsbpzPtk8CJLsgefyZcmMAlxIGsJuAXtiATAExV23vHiNRhUjYD05VTJcEpg9e/zjBYUsoXk9ecNaFEtSGnHnZBXtlJBsPDiBEWWDHJoxolqQSHfMYNCMTGOTpFeqYnssC9IrK6JNNlarYe0EpsbusdSken37zgo8p+vv2MhKd+Pv30x+8/fvGJbSeL+/Yzv7ePbx0/fvnOtzv79/OI8cxHj7+OcS6rrx9/7hZP/n3f0xJFiY35+/ay/v376Y/+317fesSH1u/v3jGfnG/T8/fu8iTiu3EiYNYVv79/7kJPOo++uDlYoeuRW8cYpUmy3ImJ0cemSZXCfDzjZXXGRLE3zgEd2ixgqMPA7cuKgTa3i5fS8jB3psyTWowhuRDkPumZQl5K7FJ7ABqEXpJ0mdrJvwYibHIUE3mS2YBxvCObszUNIFOAMmlgtDoxwLVYSIK0Hl6c5ICWJIlfcfxgBpghz5wSnGQxLkEjSMYUZqcZpbBwQ20+xhZ0ecqbsfnIEcYYhTu8mCWjthBXM+XjNnQnvWGc3O0bsxqJ4IMCGhlVwAJ5OKCEpLoGJyIbwgVt1aJp6o9FZ+QYSZHUNMT+cmHIZCa7S3Ij2E5a+oKg2jxIR6MamJBnMlmF4Z2x3XtDBREkcINWWON6rEJEaaWJjAIhMPzkRzIQsYvOxU9YSHQb5wCRSVGS6vjCylwgTLQiQCuyT4wB4GIqgjGuY2oQjQoJiSS8pyEAoJAxFXkKu2ZTUPGyOnJxgsT0wxWCk96x5SAqRsFUd2OPasE8jX+Y4VRIZYbXeQolcjQ+PERhRQRe4PH+YplvC0joaek5wVVUlY97TLZPaOsA4gNMmx1mOSG4axltZEpWPTvTvGyJjz9++2J1A2+/fxh8ffv8rHXXH3/z2xq3ivX7/wAvPx9+/wDc565+/fzm9VNh9+95uA50ffveFxHx9+91lRqav79+Mnvj2+/eMXjq+o+/8xWHmbPv3xnE9/j79vJLj0+/fzmir8zkjTrnv7/3Cj+9/f8AuSLqp+/fxhCNMTOTaqojtxQyqPlyAA8byHXbxkYFOXJ5xFCT+w/9ydu3b4xhkFBa8jJLKA0pREbXaGpMSc5ChesSk/Ygw6ok5wFFxCp3wY4krpwLZiBwlfnATqM2DUlek5FBrl8Gd06s0Z3IqXeBJQQm68WyxxLAtSBI5HLC8I07wCMJO8EpG2MbSCyn4jAVsvN84DH9zXFDc6j/ALhaqjlOWJY5gxIrUX3ms0rMc/YySiVr3jC4QuHAgVNFZyXhJlmdk7ycGeHXKQ76P4ycqzcPKT2DxGPbAQjQLyAHrICoiTSY1oOAkl1RFI0TimXGaYjW1r9mSiF6WypjArMzAOSRpMAy6Y5S3E85BAvITDHtgLIjIJsmaMYmjyfBeHx3xahq0a49YxyRoWqSFsxo56wgwy7f+fGKWaL9sNNTNAWPnJQ842ekg224SJpwIgqlMheUGgbwNSAQ0Lb4MiRUGlE8gH5xwgMA4Yj/ADGMThEELeYAd5q/jyeWKgSWqeIyabm+X03hyx7Af7glG0MrJuP8xJmntZA9tLtTz3k6FElRe/ZrGoIFI+1CEdhPKO8QdQiITk6x6d8VgKJTsZ++n4yaXSUjxhpfa61+v5mvU7Pv/mehB9+/nec+P39/9yJP+t/ffPw933+xjbPf373k/jp+/azw8dV9+mLHiOq+/wAxn09Kj7+Mfh+IxQefv384vunMbyB5wOrfWZ+/nKJ4Z7vGprI5wgQ1Ee3eGIPMYCKVcGClSI1641S83hoEm0nZiDJCMIljJKDgOTE/Mxg3xBmLL6Eha6D24gbSbYSRBJkOSHzi43k0QMLbT4DPGT7bct6WaiHXKwEhY+MCQUMED1L4MkQm0l9MMenD/cYQtQYYM2R4gn/MlsJWrnZ82YRM4soxFEsks4O8QwMsnxxjZeAR5xihbNZDqiGMmMCxb6awCLKIvPXGEKrifusKMwMXLGaasBUkiT7EHvBCBwbpqDTyDxiDzCspnK2tvv4zcW8F3kSBFYk5zeVU/mFb0Q4YGCTQvFOSFr5MguDmBI7jLAb3TDi9JFPrhFoiFrjPywaEJ/rErdiJ4Rz6AJcIMvNg1Z3uZdwue0+hRQ06xMaYASCURk6AhaS+nfn4y5XUIN6l/wA5xrohelaDKUaNz4xd/S1Atdj5W4yIsCFksIpZsqYjIQpv7LMqiuCKIzSduFPAkkxan5cjJRro9L0ypkP8IS/gcvtntlZPAGO4btJCyRuYkPHmcWdWXADTBYeF/wDMZgkoZoMfliA6ShTPra4mInnATebB6UJQm0QCFnFGJqwoWU+USHkxyErAjT2vFiPJ75u38aFdOHGARPQnS/rDk2eFevHq1iz+lrI8kupIvseHHCwhJ0AeTTxONTVKbDyePPtiQGJ4eI+/GDI6q3X38YmQ0MPH2PxvIbI139+7ySJFTKjz973mqGalu9/33xpevc/+/wB9smb79/v9wnr4+/dYwbTX377Y10en2v5kX08V/wA/mUb56rLlq9Qffu8aL4r79vFBq0+/e8VMEsTHf385VDxb5f8AmOQ2nf6xdcZNmJhX34xCnjGwXu4hgA7/ANxW6wXJzRgDwGgSKC35wY0WYb6GGIogIBDAm1LuQaMoAiSVIgcVeoW2lQtqYuC4AA6xuN8DMqRW1VOQre8swBKwTmg7Qf3IA6MGAltpgoe+TDBJjyJHzkCiBMmowt5qEIY9kU8ZxnN4HjJkCMWQnICl8+mCCpFzeWzqTXoXilIxaPv4xHEcCVdBy/8AMmRd3LB8Pqx74CGLhklIRnTaDeNQaWA9Y86jfOIwybBV75frhRFQVuDFU5uvtmqSiKxOenfnLKVvnIcqvxXHo47aKEFjJzyAS49WWybpFDfU4GSwOoWN+VzSge62k0AiXifSRBA9LAuVqLsm3CMkPlEF/CU5OjDVNRWayUAhDrAQqAMEsSmDU/aLJevpc2V7ND3kLC6sBUvHyT3lotzSNXtuiA8ViUnorDYQ2ikk61kvuMhmZArfPiLw3KIBUd1FkRpbhJx22mY8koL40xy4pGt4Iqmd6RE5YkwgTYnlCs8GJqiJtSIe35ZEkSlOjCY98QRRZZreDo3UuPmyweJrIjK6ZuCv7wWJJIsVGMUmvsp8xyIIhw7wvy8yU0SSqIaScJGIsRpyA2eSQQBknIEzRYAC2Nkjfc9YXVn+k5PGGzwOzJ/cRCM6Hkzfg02//OKhEWBlH+4jJLYd4afiJJLp5fryMikuUhoTr8mJdQrVinnIWdJD6/zeAqHx36ffXWAax2kt3/v7xhphrm3n94lhA9ye/XOS0tODDM8b+/H4wq9Rp+++UaYfF/fjGAhPI1f8/mfRkij0j795zmN+HD3br79cUAKlhxOSExM/f8ziC1Jxe7ddRim105xfAyJoN5LcXEuf/MqAr8wXGtAinfP11hLESJ04b3lF2BaZPIkRCbRzIdgwpIflQoEo2BRqJ14ZRy/hvDYJeIwriMlAYSY/WPHneWrzjmXWbx/3Eh6BrpM3ymVlyjUx098lVZFpEJ7qysWIPcPgH3yTgud5B0RhZ8ZIg3xiyhYEPAbXDWkKPA4H1vxhZhrNZ4QkPAMDggiTBmYq5k6YxyrUkG2zf19NwBbaHRjvBBSvH2chBM1N8LbkEKJX4YCfo/8AMkgCiWZiSME+GFSpSWr7iGx/mQ/UwIohVaIHF84dq5RN6X4h7YEBAUBwZzrmwaNhY0dK4yc+2vJUNIPgECzGRRRAiYUogoy0bemqjgcJNFWoIFFbrKYKM9RoASWR+cHFZJVJEAdzd7Bd4CDkaqhcgmm+ZxBuTFjEgO+sjhmIQJYwKF80oQ5FWxPWafJtuonAKJVlSRIH5hicapB3kpaCzPSZjjJgF+poXnS1HCOVg4yC0EewZUxxmSgvTQn6ylgsMSpl5lr3cYyMoSya3cMsTXWIaBhDjIQlfkAwxqzd6IA/OAkqwuErcINdYTiSaIBUNEGQYuYHCGXk4BkG4FhDBNGK8bQGQOAMBTQ0ZCrodMR+ppGxpyfUKDZEiJqEGQ1HphT4jKrLwnVYQUcoc+TBaJHR6+HDo0CWJ66XF6wGSkQnkCU+piEUey/RjSVCZ66c74Mh4Dvz/mPYkOhmEepnCBMIHBcQ+jP/ADHHkSXMLiD6ZKUqc3q++mKV3z9++Ly7Xf37/wC4bIry/fvrmtV9+/3Fdan79/OROps1np9+/axOIrjGAma+/f1iIhMxP38YlgmCH1cFWryF71lQYtJxIQAk85PnCAaZ0Ymb/wBsbbhh5ePbLaRYKjYWqO61OLTd2SkqiQyDm2V6EJGYhEvg/OJIk4CNHOBBFT9K1lfBhEAzIr1yLAphjxx/uTNGuMCB0S4JT1LGrzg/LzisrAPtnGQ9qQR8Os8uKczwdCRdas4DMnZkRUD0syWTpLugMQQZVcRyTJPliFiIjIY24ti51CLxyBoQitG2UIPLhw4XCVtGFijwHphp1PY7PUII8nIihkitoGpvI+DeSbHEtEmF/wDA/OUhRBfZm4X1998YZIJj2yAhbj+fP6yoKwvib/zAyGQJ+cEggQC9rvNGWp80Qok87P2xHw8QWgF6QofzjxdYKYAB6TgarGFPVoxIiyNScJKLNRocAmgEBBYjQVgNxYKcpIaQgbjyYbWFwNYMAQeZ3gzcCbIloQKDcbwn11HBOvbxci1gqYAyIEuiNopPdWBOUEs4pMBRDwRj1hudDEqPDpHLrH79d5OpaybWCZi8tU4RazMDe+f1m7khiKQ6nfJrrKnrQkaI7J4c4piNEiFJZPfJRg8okYBwBORqIutiftXSYKRDp2J0qfGJYSp1iRQwDyifj8sSEhYnd2/mGULg3Qul7gzBERM4DiBFYhgPEwOqHGUbyUqQSIkDdk+iU4JGRGwJTCmkTAodrRWUzHclwWL53iObLTUvJ0eMhKIkAT5HfkwW0l/qPGcBGX+sSJYmCWKBOVvi+ceYLDUhRMhxdPOIwU8dP9xVNCoIKfhwOAiUpn7dd5Or13lz84DgMRQkOLWgy2o9Vk7uAfb7/wCYbRx+Pv28PH379vPX79/7iX4ifv31yw57c4rZd/fvpiSUehziQBTd9fYwPS6jfj9GBAE+OXJMenGVACy/jAvP3kS0oE5efHORAgml9r0MeWIap43gxCGOg7w2dbX9sJBphVYcTSdYVlQm4HFvOUQcZFYGovzipWQC/DWEIqZHJuEo/wB/GAcLCB+skK6EuSF9VhF3mcNnyr0ywQYioLq0EcnuKe+OV6YQDELSEsGSwDkVWCZQQ7c+MIWiVzSrgbiG8iYEpScPY3CxOIkZKFVu7BI67DW4wlHAFqRCb9UwoBizREi07rWwhgUMXjaidK4gOYEJri8j2EgKSwFAL0s83ikWDpKYA2CEw++ELiYoV1ncZGJlUlEa8ZL1B/j2MniSLUIiXJSYkm4wKNIAVjRVmQyssVFBI45dxhAoC1CYYYgFrnzOAHvHuV9HGcBrAqkmHkEkJM1r1wfXbUr98XNCCY1iHk6XRDLHRcXhxOrP0QUWuWCF3iVKrNrCK5JgWePOWPPRtWTMAJDsHtjDEGkRCRjmz0Qq5GNMNyptRb7Ox3l4nW+XQl5gA83BlEYAFksAWJdK+cTDMDYqSE35ieNYOrRRrsFYGbI8ZF0NcZUw1RBD1O8MSRMh2K6Ymq2N4FFgkRoEWA3E4YKVyZCT4hXyxzqS08oMsVgjvDOdIK51hpWeQCIPrnI3HKHNEYDwt1AwOXROC+hoiqdFH4yYL0OROSt4W4MGDXGeE0lOIqq6zwg1oWCZSNSUl6GyrfojnSX2ACuaUlB4n/TIGjI2t5HV4QHFC+O/X+4aErzfYMPNPHE9HApITKj9vfjnFkJXqD+eusugMkyqT7xie0gRFQ/rAqti6Xj+4zMSCC2nnC66NIgOMGm4uI19/wDciatffv5xJ8nz/wB/uE8337/ffHXfbvFOrjnx9/zJKRxz1xkW8qvQM2KQGmM3OpvqcmUdfOMFATFHjCYFW4jJITfpr7D5yuYnyl5xRlDuCNf7mu7g421eqfAecefyJAFpbhHxjWcmqZjFW8UTvqM8jBD2vBscywKrcsR2/wDmWNCtMonsc/K3kT0N+2UBFF5cLd5FYposszhUgqU6lMbC9SIW3awDG8YGKCZCSpbiEwG/DwkwdrLsE60krCwEEK0YS6gXR8gzfCBVe5g2KPAO8HNuwbTGonUEneKS0Tv/AIbHUwp6yPicQ7QGYA9CIi8RQgdbxNBPpAt4SSim7u28BQE0TNPGFQXvez/v+ZFjRIKdreSA6AfV3hrqmf8APx+8i8ot2fYyWVb3gFkLI3gWwurEFDwWQ5xp2UUCrnYx62JnbjeU/RMRaZxAIceTpq5QQyVcJwQIlQzaNIWpKi7iYmzoWCIlCFli27FU0y6hNazwrNrs0L4AojQajjCyizFKVrYXBsCMlN0CQhcQROj1LzgJlAEGEEClCkH6xhw5IIGZgqWjmHUZUlgaqWEd1tH6wb2ECC2DQTJ7RgWFMINVU94ilCSFZMzx+cjy1oCdevO8Sw1nboMTdnRkT0FsLAW9yZKqKgAYSKrcis8uOSAlcESdPoof3IMGnsjGIiKJIE7Om5G9/DHxZRIkOTclPbIhf7kpl06veMxYGLDCzlZ4H0/A+HSJWS4DVASkE1Qy6YszAPnKaJng4d9c1eFqRYBe1ho8VEj4f05wCWwPI8+Tsw/wZ+jcRplRZH0fsyZtYgH198bAtGMryeMdARtknmMVUwJOh5yzJizRwjkwjYfC+2BBLgXHvhsCDh+3kvt/f7jdsvne/vvjHn943Lyea+/8xpBt0xrIBPJBidqGb8mC65T33jQZlr+Yy4sIhePH1/Xrit5EB4al/mTtpOC8D+4lQRcsCAxygB6Y4uQ0ZVREDs4b4dFC9oDwED6xK1hEqox5xTekn8YIN0s1gpOkT8ZVPLOBZ0T7uTe2sKh7cm8KMY1O5k4DFAfoUYKOaLXLP8wAl0VWEkQMiYgvWIkjoD2rFDx+saR2PttUgE1KIQLeJXRhhWjqaaAxCWagDIRSJAnAbn1g9cAA2TK6f47VjjWKwiJAqWoRXkJ84gRN+3u5U0UtcNo0T6uJZSSnPORlwMZfH1ycAkV+7RgQTQH15xlEkgPY3ggeJ0euKAFcjgEdeQDkP/jJSZQGop0StVzk15aXAQYJ9uJwiGuAHbVFM1PnD+y2HiRC2LstYZbS/wDk7COtMnDEGKthJB55fFYTZctsQIiCvWJhHBtWGPEkqfLUr3c4jXSEI2ouAEe3piV6RdI2BQLcXjzFCJYTCMw7W3rJdOlSqhUJvZc1lkbWLcqpgmxA94y+i9hKAVIBpyWGu4gBUI4eheK3ClQknDeIEnJ2RZ8Q/hhCQ5LeS8RPZyjX9DVkB27i+d5xK4fkwyhEHq5/mImwQH1cF6yMxhyLXBba4MdESWIlMG8A0nJAnbgWtZHFh8g+8lnGDiBoOiABLzFFO+CVwEkikomx2j1KrL2KC9np0+TFypwJIq34D7PjWAJkS4Nbjk/WdmEqcxoGcKsSV5MOKiQFnMLz2OKKHqdGr2ETT+qCWQTiecOOAlckfnJiU0oL9P3jMk5ojw9cQQm6gn9YERKjj7/3GHf4v7/cp37c4rss85YY0VGbMrqMAirJR64z34tBxjplF6vQerkkMQnRfHxGAMuXgV0/esUWFTi+v4MPgTJ2WRO0GD9+1JeokiBa2Gw2hwgXOvXOUGdc4BYnCJOB/uWTx/cbPND4yXNQ/eIAdYEo53lHtfoIwaEzCrgZrEb/AMh3kkQIBtyKhACJh4e3piDGWqglW3x7YbMbBk+5ZhQwaYjII1GtFSaPdL0xLBAhRIhUGJEV5d4wO40TUqxTIkecZ70tTyq2uQVJGQmx0jFKUoQiyecUPcx+8sNGl9YyRSWesziKFqT1RnNtJS+mTSJkdu8ASmEhPWIVB0gRqIpUJ6YSRisiBAaeoDGyouoHIkbOK6iMYtG9GHIacQpUkRK41ieFC3SkAhKqVcpOMIMWhRtWC+pwG0jWkRYBt3qA98v2wacyEXMRoYdjV7jjKwOGnZmtuEN6lpjRBDrCYAyN2ZB2SO0KE7wAdCYQCAhEwd5IgETSBM0q32OM5YAwTIIgGq9aax7OfbVCDkVJu18i2rgRAjYArXEpHGQnzFFFAL4xo5Coksa6rBC1Ah4/eqLisJlBMhktJnXvnnGHenOG7ZOg4/uMifEvu8mVgSDnQBxIi8RIWBQ9MNYxKdZCDxrzgK5Yj3xWJjpH+4cb5gTClkRREqVkVTRQQEhtHSNAjxbEdiJInxGy2nTPdY9DBRYifO/8fjFmGhBtzDXMd+crU4rIXsx2A2H/AGXpfTrGLD2JWEFUDqMiZKY1BuMcbxkAGCpPv2MKtX37/wAz0Rx9++mOmoghO/v/ADKQSIyMieQPv31wRJcp/N44Bx1lFm2EOMku3vn0x6i8nt+Si1aPj+5GrDABRHHiv3hPWy6PP8wZ0wuVVfE02aMfASYZFIhhUe6IWK/YGAiADgDGFc471Dl0zGRQ6/w5f04syIicThAB5xsepzYD1jFsHEPdwKJL0dYwFAnby4mEV0decIEG+XABVKJVwd4giEUzbojyfLCv+wVpELpH8MVpWMNfIFFQMTjaKVl9ecQoTJT3xR+IqPXIVpWo6vIKcLEl/P8AMkecPB3xjhAN36bf1ghJC174A3EsdaMniStnxHP7wKsRh6OcQm7uDOfOEARlCL4N8W7rLEYeos4EkRS6oxKdKRAwkcUjGR79sMkIYMxJmCgjCwBuhnrFQwLIwhEyl2mSwXl1CX5xUoqcuBjHFCyXYkmjLVwlzVYgCJ1DsFAMiJg+uTGAJ00QFVtgluZgci3umISEQBXDcMVeQ+k1TZAylCHSo3kDpRIMuHQ3u8kggAlbQOG9w/vLNnIYOCbo6uZnAKCSUYUJ05SKaMvzEKIgoQNrKHgGJwIEwYCQwXaEHnTzg9oYibIT7LLcELKNiwOqp1lPEdoEHPJK/jIAFACe2AZsVe5OAlEEmiYrIRNMNqF6Zt8MWhjorGwxml2YwhOeliGjJArWBI765yHthKAaJSUEGjh4yFOms6CRaHUTGEhIUVqLAlLm26JTie4BeiQYiE7MiHQKxB2Rx3iupABOfo4dpg1x/wCYbsBPgHHQjqZjIQC05B1IqFD0/wAxhMwVSIefv8waI/P37xlFxCd/fvGPg1jGxROMS1WelZaDIoaBjUKaI9cRgVVhGoIp2on94hESdhci8Wx2pC4AP7uIyFMhqmQSokDZuUCPYBTWPIlSRK58smUm8LjkxSFInBpmLnFSThy7PF/nOh+vrkBg7cmJ5D8uRS8GN52oxgVoRGdgemsACs8qIUHzkHaiYZggqyb1Ew4NAuBQDqh9FeGQU2n23gWTeOPWualwxJqaMBa0mDgTLL4jEQerPW/8zWKiLv2/uJog1rf2PzhjEkwp1GTEFgROpv8AGTIFZp6av1vJFkwi26F/zAAzCJ9Gf/MEQmYGCGqFNjI7dU2TgEAjunSR41B3GE85dlkPdC++JE1m2sLVBDAqo0kCVlJqsFAJok0oGgKoxAgnBAziF9pSUiNTwyACAngUBAbNJEgus1FGtEFdBS1tlzOBQAVbyVTiUjt1GKlqsgEk6Q0EjVZAtiSY0FU7RapyNqSbYCGDFRHiVyPgE6MrCCBhjzrWNUgtdklQ7gJ1k7cAJqkIBG2x+casMSRkkKmZl+DAdrLEIrpAwY0RgFgTHcSSHT1iwXMMQAUdsN8uGQlh3lfUJPGT5K8rzi2UkTUO8qULBSiobi+MgMA7UAvgX/xkYeKxAEzdZKzVzhCzsjKjDIlrGXQ94WnGMcPTvJaJRBQtosNgsxySRYPABubprYUJFfnINUhGlF7zi0JFsixCnKWE7EwQNC+EL9DR649AAk7HrDAAsSlUf7isM2jaNn4xtyDrAJ9mqzYp4PjDgAPfH38ZSuvv3rF/Hf3/AJllELf39/nEqFSN+2ODsjOSHuXrkAztr0x7ICGHzpxBSEqYCo/b+MfwI5FLX2PjHRJRVkMngwHlQzUSClrSZd8wCXlytnslZKpPEkPAYwYi/GJo7wDIVzjRA5vITEUT8T/MQA3sYidG0REZUYiXKQGAmxxzhQ5TkRK1whbGFUKBL49cGlAYmcgLzFD24/gtkkQnQVju8TcDrHvXRL6f+ZMgYFOlmYTcYlCHiPOQxMqIZ7w2DdM9cYyUudj2f+GCgOgHW5+OMkIMQL4f5jYuk9ES5DG5YVc0E/E5AABBVchH7yNcEENxX+5CWLIncfZxHOis6BziOmVpKQhtg9SUzvj3w8BrbOgGQGFwAwkybtc31OERWsGBhPOOpQC9VHzl8cIZ4KwqF3HDhLb8mlMkUTfB3WRrGGeNIIvejl1glk4IZSJYJt5I5o64oIEnUSBjLyBoDDyoWAQASIAVP6MIV1M6IIQo2dMyoxqhlTLV1Cb878RksJbYwsICEhgqWCVywhTTJb7ToyPdyI/vjDGklbklf0e+BAeQfZPZiOCyBT2vE8nGGWIHwAlIurOtnrhQSXkikhJzCBjXNBsACV4DDXcADQXNOnAALj5f+ZKDqrneJDRO0nJkMwd5Mz5xac85ql215wZHTeEiYkcAwwM5FaKslnZRF+FJ2uJs3Igw2tW6oFInOgRBhfGJ6ZwgV4iGFeJPHRusK2JWwxG9byJNYR6Ovz+cAC2rhDZ+MaA0CY4yTJUEqajFNAngwk3xrKAu9PRvLroWPnLoS23kzqwvzeJebpvEmFqpxRR3l5hP8xmYmoZgoeuDKhIuwGUPacK6NyicUMqKHo1kDFArUqPfn6fPJlr1XkSROO8ag7w7GRpNhKGueLwP9w3tlYZ90ubnc489D942EO4xgHhE5IxDuMiCUFny5olqQmVo9bcq8oKgUSWDGGO0llIgBJEf8zk95ATlWCp1cThUsaYBzehgJjzg0b7nCyfz19/8yWhkUdHX6yAmmKP6yMaqRHHX6y0VAbOsYoQDODTx/cQbEubrf8MjOBEHq/23G+IVwFCgEcyk/g/OBksouIUYhCjy95KHO0yS0knyC0Vh8RT4CD9YR3VXO854mNZLAeiafnGdHBsmRAo1IjOB0+gtqUUBbg0QY4gqwKSd1AoS0FTM30azRS6F0RapIcNo6wgiQQkKsAq3Biz6JnBEoJU8+u3Ccyg6HRbcEF1OoMkCu8PSeU4VXrnG5ZEYWrs3TzV1kiUqp8sann057wSQX5CiE9sj2ckkMyPUOJgggCSIDUyOZ2+uK4LDWEO7Zd+Na7kxiBB9JHjAgdjgFGJa9ePzlJCSTcPbGL322N8fR4jea44zPLP4xJCqOchE46r5ycMJ6Rg57nAjtMpHbxgUIpgsuQ6wSFJCkuU6fOCmOARvkKl3ZPUAEFVwBL/R74sldEEMNibn8jJAdkPDz8frEHAVCxMjySnpGIRcVHrkbWItOPOQitAUjR3m4TXCdff/AHEiqwKyFkvK+cd6cu/XKX3WSBK0j6Rgximnb1ySx6kwGVAghbjxnJzEup4PXLwmMqEFOkBNx7sCQlKbTJ5jxtz3x1O8gaRjFlDzOvLLD1s8n/DCNAnlwRkRKMG+/OJS7vBKrrNl6Kw6f+5NFmFCsAZaOB1742pZ3zGOcZAormz7GCgCICcI/wAxWIESmHsvr4xZS4KQwIjrGTbbccrzXpjkUtROSCGaGWgZN+B+mCInSSnJrAm9duqvJIiMu/OU54DgxIGtPb6YrBO338ZACUHmcJAg0iSZqs2SHZuxnWyXWDxFPAAjPKpbVc4IJIiMm/Gekx3hSGR/GBohC0ksVkShal0YI3mCCFvRiySeSKt2igJcqkrndALAgSECQS07SYTaSIzkKssF1ENU4mgPwSYgCIiDEPGTq2JtEsoqSomZjgjCgonGMp3kw2wPQIQQDqNYA0yQeCdxiBeRWsZhkXLKhr0MGwnwBBlO0BMajF4pAAml2LEyVnEKx4UEfrd7xudpjJMpUzWO3TPJ95nEPQVmEs9gwVX/AMEXGLIBziwYWocSOEZxqDeLKykecBJHBgpCVZbEnhy2WJj5yb0ruLIXdY9XJyRcjMNlq0Xe78Y0KAkNnK8jvG8ikXDw+zGQBBUHg6n2/WRWmlA/GTSmS8MTBiJk6wyMrh158mQRM2TG3EXN/wC4a5MzWGST6MBBKVAf7jVXnhpP5xY1422C/wBxQZBIF84xVRylwUJuFDRveFjhrajrNABC9R1/8UbMEpWBvr/uJILLJ24pgbNT+8kYsH6Z0iDr9ZCh8sTQawHnm8fr5ycnq93AWXUqTzjdC8sVMpsnDz+mI0qr5aPy4ygEn2mcUz3G83UkV5Yam03PgxJmya7vICHhyMBzL0PpkZm69o+/+3jQEjQ3WaWEAjpa/mQBY7Hp/wAxVCmCKtyKgqmnX2DLhIYE++XIn3wwQARG/Fur5ymr+G0oSEqJnbthSIpgZkBoCAjDtM6TGJWF5yAZch8Tk8UIVBw3a7wgZvFLNOk0twDzbeLNbqoO5U5UPgDoX+WMlzZW4UGEARZsjQExHAayRChikQTQiEy8ydWJW0UhKp7Ws0xHmYHwCshyF6c1qsV1BgyC/nJQyhEWs2yITtFBJAbJHxB4yY46JpEx0lfysWDQlVyXyoMIFGCQQsd+cAqpF2fVxilmk8k4Hnk+bcM9a9s8s2ZpjooJ/OAjW8EAAcBBF4jo9MSIRWEVig5HKl4wKzuO8ECW6rWSEfApSEfUcnpmquSq3p0D1MBKqF8lOtx+cdjt4ZqpP3iM1N20v9YxN4D7jBShHtioDZ6zOSRPlG+eMmQIOi6f8wQE06vIv5yYVjZesIPMBLwwBNNs7xIEr0Eyag/GSiWlEQAtMvFZMdIkPzkG83gAJjW0NduQQUSQMIQsiQeV9M9j4cE1kG1MKYgBr/mSMoeXAEbzU4CB8/5gVe9ubSGpyCluKV4GBJdhkQTrv0YpA2mcUBqs5ShbQKPgxqC6FP8A4Qyjup7r/wA/+DAiRdVh3huzptyAUNh4JxjUBowbmmC8YsSEQHjDJG2APXjCEAoR65VG5AnjRhAGpd5IoIJWevv7wZEI5ONY5CkpjC5OcGgI7kakmAxUJ4klxRStrSIeNPp7YyfMSBJ9CBPnJmjJIZwpqHrGt2ABA7So5yQuSuBUMQbqZAsxddhg2QJ6TtPJMFAJCVKLM1RYaODhCWxQFHczuCw5xgoSDIB4b3t3GGjkbZtApwsMnnEKdOF5BBO5wCVjh4h/JxYwKeRwvE5u5xrcXrPzGR9mPYQ/hyGt5pBKt2Kj5rxkzInfbB0M2aJduSQ6lf8AfzjvIBp4x5ecWbmkQRQXExN9MKx85xibN9YsE6LvHdEzxj4FVi6xjD4LOCTZq8FEycRkkQXlSjuMIScwN4hAAg+cidhcYOPmTqnlx6jvJa+TJ6SJHeAIgZLy5fn9mEMLL8nGTEnjdeMGYu11hLiD32OSIK5DPpjmw284oxo0eusp2nrFafJwxFNf7iTz2rb9WVTj1ZBaxDD1RQa0TLn+SbHbMELge+1gsUMBucE7TjMwMGCSS/LJkFVGBVhAltQlzaMDkwmzA4HEnF6YJRLfm8O0IjNF7cXg5qc2OCd8M5ZXxmldSfjNjSoF5GomLwBRLCEqxB+cA1IUtzEs++A+mew30ewfOEAkvPVJ+MZxN7xbVEhxRL/MtnAeY5xF4iw05MBZHuAe8KDoK+/vCSQUsekMWfHOJubeZ9owinCAb1+8m5EkDmcopJBF94WxcEO6x5LKDXGShBc1hM5BMATw2MOboxtNskjECSBMlBHGSaYCwe5ISxiWPxkCus4XWOupCRXwEAyzvGIwpKRMq0grRhtY49RVnRZoJBgiExvN6MGxFBESQidRoMCRapy+Rpx75yqU6SJLgpPKh3k2Al1piTRckBQmY3VHjHSUQkt6jHU0inR/3GgBQDlTWXojz4z9TV7xF98njJaAAFdypdHlkMa8ZJTJtFnqZJCx8CEPxHzhyHUYI7RlPGBAWF0RDqfXYdIkGlEji6MaAuuI5rJSQAsnFZkII3l0tt1iRJAsbxovJzlhdveJAdLvCcmMiLItu6yi18rc0YJq0cQCDErA0j44xGo1CaHTks/BpxwEWL+HzUnsZACSEEyxBXvk5JbBT3ej/cB2msJEkr8HKMCAyTuMJCjdkuRy15+/dYEhKBE86xSiTt/WawRQ7iygGRwRUYGQr0ByGsdKBLhFRAKj2wQpIp08rhFNS9ZIA4lFNrEmRQBsqCLN3grXWJCoOuvTASArGIDydYXCy5ykVBa5ArlyFVpmnl/cpOcxjfUj+5ehcYMlPJvm8KRp3hPRaDkGR+MsLGm1Gt/zElo2EqAVZKTzm2IUOUNfrLmbEsT1hFyMlF2W41oRD1UX8ONuI4OWZT73kMIoXPeHpux7wUQ8HP37vGE2QrpLGKtgXztxC1wPOTMiEw84hIGQl/MplUYt6jeaGC8cY8MACBSStGo98lO5mJQrx7HhU4aV2FKqkvbre5BWRvNAYE2leuA7n2wFDrzzlq8PWTroRBREXLFqa22A+aknUgEBAvQFWKT3gISDTYoEGqIwwIUJhiVo4Ne1VhVpCiRcS4qX0BzhyntQhcvtiIzkGy6Fjn2SPphVwbEEFPWC8IB5Xt3lv/cdU4++Qm2/1giczlOWhiZFo5lH1jAIPDRfuwzfUYI5YS1yIZ9xyaTM4aqzJXZDgoN7kiVz7E4k543PbPSFMMJj840PsYo0nyYyCIZEAV5euEjBh5ONORqvfGNzAMFnacqgj2MpBLMSgrMVOJaGjE8khQUcAk2MD0YjEsxxIvgEYhIGTCIFhAw5INEKPDksbFftNq9ZZ85oLbcXHGABC9BO+e4xrWyPbJI92MwSfXxghjOvnJMJwvrrES/WDBbYD84bzF4ivEgEPzBrRH6w2BcKBDQACV1U2xbAUiDSjQYXUQMsUKllCBSUbBZZTO5zaXgEA/rglx+MEsb15yhrc/nBi+TCU83ggdKz+rPm4kwbT4DFZK/44CFax5tLyUDB95cU0QRTKKACLhBe/OE6H2Zl/L6sLHgV5Yh1+cYICJLUox+sYpSaEbqjm/7gT6SPAP8AVYE9wnnIgGZW1xbpsE++MhBajXa5VZoMf1i7FRXlDAxPqHu1iC2ZD4yS3wXWQTNQOkQiPWZyP8TCKYY7Evie4x64ICggl6SQ9eMJOiHVn0efDgBBQEGNwn7ySW7wdB98ibcVuu9lyle5xNnGapoJ2VHmmsbBcayt2UKYqVwqykoRW9Yf44hIblKbW3x1h2MqM+t4vWOcUWdQCohl7udMZGmAkoCE7W1X3wS5POQRMZ+cL5E52xCIMFchIsbHIrnoSEgtBIcs3IcBGAAxqCy19/OKTLvAGv1iqfzGPZpkKkNnuSZQ2yIRH1tubSzibTWXeVxmiWzCbqBsyAY4Npyb2dZRc1+cBTmZxMnOJ0cpKpwg1WAWM+ahDXvjcfZm1UTsmNOg8YeRd4A4ebRrT4MjzKY8LZDkFFVoQxxhfALJ4Jk/vthPKA9zhyQLpzoSlYtI0mKr7/mSFHFKYv7C6MoMZRMkdinnIsCgGbLgcrB8DMYXSd6DKySXnqGZLkiFBiBcgyls+e4xQh+CSDhFERo1kuNiG2VAeafjFTXq5orwP7i0aGRL8BkjLeJZreTJnyyfs5ofBnHncfOcklMmAEoYhPZtjQk9Qvgwxk0EJJgkEVDJU+J3WbS4Zhqj0MISQWcEQMaAT/zLzxh1IWBuS/iI+cao6f4l/ZiqXf37/cb5oJXDBPAAj1vEQFI5X0uN5aH0C/y5BjtBfzgqPqf9wpklphU34wWAT5Ai3TKBnUiEwJkBQOK8YwMDokhByyWb2u8FtAnIsoGyZb3kF3QzaQfdvtlKTkKMYdc5TVMCK8AvCreUNGqqDCmN/shCfIc21DvHccLydrxc+mucKVLHxjaUglKOcLSdRcYU4d5K2l2+v+4gMASuUa9sIHznGrxsw5jBmQyMEsxrSIFgIp8QJJdQwSSYoAVWYsc7rUmRogSTJz46kiYj7KEyLikTuV9xEPRnFPidcHsjklnjIlmoMACDJB4x1IsxpSIfOeY1iSSwF4/ewgcpveOYTgo8msheIyTk0o2EDsUvywgUYQllPACTFzvCpWn9+44QwgiDjWAXZTenN4Gm5B6RQLZs6xQU3Enp/wBx32SINY/smBh4co75c4/o6OaOhM+duMPORQgW9rkGx9r0L1Koc02Yhgoto75RkW29Bj0ySqA2VppCK13hRlGAlEvEll2nziNKTnAF2gwx6HUY4A2oyPVzi5cmMKzjABdXnO6z0hEwUUWRkZUQGGi0ylzddmFhgKIIMydwxDrxlPIhJWdFiDRtibtkHjl/WLGAhQCSjFDJSdsoD4lw2Ao+4T7t4gTiIdTvDp7/ACYMLsQPvvkAJ2PBlaJiLnWg/uRRkuY1Ms+2dRAB8YwMwBg65xbMpX3zi+Q6QgfGJWOlm4Mr/tVH8gH4nChFSkBH1X1EYEZUEl+nZbGa3DC9F/kPbClacXoxY9cLhxOo0ER2rplcmsk4owkD6vAtEzgxMpHLkArcJ6ZsWQXAXtLxifGFIp2SgAk6glTvjDuY0RCq6PGKQswFrgEfrRIwVwojlAFmJ0ASkiJQ9GvbNbM5nnHzmzFOCJqJp5NnpkEutMTqBlE2g3AcARiRCZ5cmoCvEZEBVXcmHd8O0tF4g8LYmZQqIB8BnFqOXKemLQzkjus0uZwRLhyAvBdL1GQTHGbCeMgJgQKDrAELPziUiBHNWEEHCJGT10LmkjpF1EwEWU28XNsXAx7Htyu+/h2eERPUc5T8b2cOOO4zEDj34p6O8iUpnVY3C+j64GfjGIRvrCWJZGfXEAVGJgMwHOAwhCVRTrXUxau2tRgpGYKIjqAokMYyR5PC9Ia+AcS6IB0bKStkZl/BkysJEiTEjz65Eu8NwxQ/ufGYTPjHAT5WD+5wP+cAvkVhf4ZKQw7VhiIKJlvy1gGtoE8E5CXWwl4oaULvhSZIQOSIYB2re0YAvNsYhmSTzkWCBl5aD4MnCgQJSt/tGVqhHZb/AEyIqKYeXnIGdLr0+/Oc0tJOSSMFgHnAlwGft/5iWaST6+cBgQmjrBPOC4fBH1jDAFENCsBopmPTDioKilEucgaV9Ngs8KENNEY02bkEJc3sA98TFMotWX7xk1Zi73ky1vziZYYjJe+bQMvhLGsmGIkB3yfxg6QfLlWTu+DWRmMOLkks/jJvCBmCR7P/ALlHDFDISlz1lNJrMLAYslNVSDlJhwvFIvFQiLCi1iCnGTf/ALrJmLp15yFpziI9GMnZcKlA4/snOBIdYkFfGAV6klTpS3YX3wSiBsecq6gbMV4Ag6S8D9Ehoa7zMXjD7SbMhvezmec7L8Ze8YyQpt5nIAY1qXeO3vjrGEpyegnEgzljuOseQG8VLnCyLnIgi/nIFTXBRPqEpvgZEic0Q6rOFiHjG+RitlKvYn0gytyHwun2yL1bT9MSyK2l5F/LnLydAPn6Rg5abMG4eoreR26xhfWTcwBrrVSJEyW6wiOrlKZT+QkrQYm8sSsUBjyIdsrh4nhS6RuJLXg8pkcyIcFAaGgdwbw67w0KD8GCCLfXKeBvJa73hmTUz7GCuij0OvvjIjVD9y4buVy0b3kD34qG5byA5QgHnZWNTDHGGAVPrji2kCYA1BK07eMnAKotsixPO8QLVvgwqcQCDnTGhDEQAnR2v38YWvBRghf4B6ZPMX3mpX71iwlmrJ5ylNQTf37rGETaqTFw3iYhbRjut/nOUwCSp3ONuHU9sU9caQwSj7174uJF4CAl9bQyFBNNZFgHVl81hKyOZX96BvFaQvSXYXj5mEECBx1lH7x7jJBmd6Z3gHEEVE5Hs+CSLnf6yNpcRSqzPrh99BES81jFLU6xVCklP+4DuOcY4M8zhUAlymcgjUTHnWNesBHKF6IJsjRzhsQAFShKVkTQR6YmpDhCmwR1EHtiXWJ5j+5eHrgTdmNE5PCIQ2oaBwpxFoSaISasynbJGAOlxyOVXlEp55wk3OMKUtL16YYIpJCzJkR18jwTJEqGxeQZ8YW44DIkZEnXjGTrIQK986cSW8d4mgIMIIVkSnT1jtwnG7P+Z5a/eSiDWXzlMW3CipM1EYCbQAsZwlDUCA0jCKIsJPHJkyKD2dfnK9ISXqc4DTHgATo9HHYS3fzNa0d5UZhjLy41ktrQl4wWM2OzLR5SK4pWiFStku3Dt7Vv4x6U07kyOg45cFrBzsKAkWRUtDdEjmdpdCe5Q1iEHBzN+NZcBOgZTObOCKtkwZUeSD1wElQYc9pGPTKBXtfjKnhhoeWfYwKW+enJmJlAk+cEsS1w37D5MMC0pwWA8JIFQsU4ICgybBKXETOPZlgUsEqYamAjq0vxjbmDU9D4aw5UQgmmecocHZxdmOQBZT9+/nHBWUlFnmP1gndROuqMjGoEPBoyFcaXCkoVZeoB8pi8cxl5988eAXjIW1VEaBcGwZWSiOWx/ORkpEgMgz4+Rk2zPbGJTzAwausrBJz7YhonsyjdGI8VZWli1PpH5x9JNQqY/wC4NAUtHF4Mm8PNYoScFMHpkAK/OCmHIJx4NhQcu9poYSMJV65fAn4A4LkCRPUJPfEeMLJRwh7g8byDHY3F42y3aKkjWkneSPWlBMtIkVIenc4w+igImRykMmIkzTJtWnWC6NZWuO+GrGPE4rkZokCAOCEx1hNaUUHbLtfjNEusrA/95WbS4wxeSimGQjd4xiyYyt53lUA++ELASyuJGSg2EJ/76Yt4QJSEZ8NDu+TGqiWQ5HWVHgR8xsxIsG4cxp/3HLMBGOCrAYm03ODp7XiBFd7yKnRBFiYNExcdZGsUnKlA8sxiyQva23agRu3ZDZHr3DAGXKwyEoBkEHN2y7t7rECQEaNVkG9oPTvJUmisQdpJs5IPN4ojMoQfb/3KJof05dzTE/ORl6UwgPr+4hkqaPDkw4zC+6cMqBhAg2vHomhyIn1CgKDwrHvOXlPOCOfd4wFYLFeeBjG6B8hebJ3BdM17QY+wA7AH7/GCqXROKpswDzX31xZWCvGTJoSOvH7yZApI3UnfxjkRAK8cY1QLVwYKQJCvhyslbrBYBQCJJ3CodTjFHyoH8HC9SzSiD3jHY0LAKch1RDcYBGfpsiY4sHpGMPth53/8FRC+6bww4aLM1qyp/IxF2MWnyfrHXakh47MmgYGa3hZcP1gwEYcnZ3OHrGMxBTGddpdPFYS8huFmKs835E9Mm9okYkHrhzO85wGjIw64UBsO6CAzxGShMdw5iBqCk7Qx5NP7DNWYmIoIrJfAYjvFjWHmYxpa0kDka/uR4B8FgoDcAYa5rEbCBZK0T0KymfukI0hxeGMZUo4IYgDGyi+hkMkidecIHn/5NZYM2P8A4A5PJwfAFxZceND7PGK+cAWDDPokRj7ZAPHXtXtiDCNTrkwSvkjkT/yMaTFOsiQZJscCUXEROGYdA3hVAYFnpRGqTWgqWcsgOaIsKhMpqtcY/wBAfTiDXQfLnArhTDcylLyysvc5EA3s9GXKiIMML9XNGEVGfzlvIXobzg4CRngjPvrGijihwUfHEBHpmyoTrEi4vx4jDgDFTYLczC++CWQwruC/y3iMZvBJGCByzj17YY++uBo4e5ZgVwwFnnV0/KYp8NGK4e7GQlC4KbYP64lZOPsRx7zedEE5Dj8S+MchSRKPk0ez84pF0v3/ANvFMMiYk0+ck14aWnJ66xhCK4sqP4V98gShTi1Frys409A6cBM/nF28t4Qm5giIA54QPOKU/MCJ7X04PAYHPOWmJBG8hkOOHC9JuayPIpyFz/xwrkcKir4rDSA5L5DFYsJ6nI1dYiPDJkYycYgpJ8RP+uG9lgxthEbPWPGduqJH7CP5LrCOTM8dnqaRscQO1Mm643gkTk5QJ7il2wgTMS+AxhFnHipCSkLOa9Mmy45pdvMROX1oJfXOWUpj5cmE9MjjIADN0X8MPtgYF/8AUZCVU7Q07ziwRqkO9M2O84PGGJOt5z4wvKmGkZD1WaRHqYaQrsjWK71jtjJSesXgp4emTDeRh06cBReoyBOUY1DdcTB9RxHUJHnz6/vGJlXov+mAoFScyiIN/wByxm5CZTYZexk7PONiK1CaxoIaSNYl3soERNtYB5crjSdEkJ1NvauRH/VH1nnm8fAMKm4VCRKXUntbbmiONtlTtRXy5N6VCaC0abmMiFkqvbWU45I8udmUz23kGtr/AIMkHSk3n64IKIgxWPE42dy3gljTeGHSSRRye54RgUQhUWafMH59ckiu1PWRMBjOWhF0VHM++QJUz1xAvQOx1+AxZrgpHiTIrPBgHU/GErpKPX+uSWQFe1Wh5ecLO6AaBx99cSBYFxo3khSpdffbKpfpisUoavZz6BjETkJqGrGEI8T5xsxCsbSwB5nLTIyFMUP5iUU7uMZA72LYk+hiSPGTX+YREmTxd4if0y18GKDHWWMdY/zFV9qqjO75V1/k/wDuTGhbk0zm5IRKGDIWCcqeWMElzNXjEHeOScKqSgB1KC5lvhW+aMWPpbMRncbTZTQTZuWRx5Ig8LhMQPvGGpkR0nORePXPjAEhcIwKeMsTm1rEAUwgW6Hc4d1GBycJScbxA7LmZb3OJJwmJiD8qfxmh/ThHG8sgbEGvDjuIyh6gjwESdy5HpBEKy0Qw1ZSFkHBekhBkYQsDQbERwZxdWRxeO9w8mABlxRCcNkawRhR5Zc7MhNZyd4hNkeciEUOTFJJzcWQ7nEKo/rAnaHa94Nd8rHT5H5JOcSCcqJimPCWPkcFKNAFJNZTuJhCiVmQuAdPJx4xoiJs6XiARYlnWbwSkOvGOKogohl9SSSjqcInUg9YAbCk8jilYWNIoJdjoM6AHBYNC6g0gnlhPUOMlYHXWsHoC4BLO6T/ACNZJI3oxzKwb9DeSOJds9YwmmI9BklXL/Fkjks3tkolZjLi9iY5m4cl9ydQmP2hg3MgKIN1SAO1E7MWNlEA1fvkjZ9GBe8ZgpAerixSoPLpPzOLKwEErs9F/WIENtMytb78Y6JX9Qv0Lwyji9tf+MS0HPF5Lx6+xhmrUGiP5l6QSEEODxgjbgHZy/rIzbDq8vsBZoEH6nCn7W1tvYn2cnFgOTEY/B8YRs+DNDPvV5EPZ1lRgKSTVcGjCrbz0rICqwRadbwtOu+cFnUPWbnlInfj0w2UDcGnD5yBUFhinEdExka9PkyaXTucgTlMy5olS5JKanIIXtg8W1okkXmh9so7q8gGHwyBpo6wyoRhT6Yc7+cNYVD7ZQKD1YxH3sgRxekEsW9Y/CfIkET7svvgi4DyibjzgyQkTssPWD1HEClE071jXQhAPUXkzV46AgDfEcmQsUyuanC1HIChm55SHQ7GXypQQ9J1v8rBLnyyQ+RHSMidmXGMhMdc4EahN5ypYiHIoCpmHKjMwyjDN9lViYagusTMQPUZIMydZY9TvlyUMXoyCHcRJv06z14MidAKcBxEUxQ8aezxjMsDxLGBcUzXnxjMJhSnWFpVPQyB3ZKeA5wXgC0kk3yo8k5HI9jZJvK6kJRlopWIUbiRay+xfgRzgIYIwBCk8lQirOsfONJLUj4GPnJAEmGOKwZk8Lz2DL85DolT1ciQUBjvCAkIGeUIygvBxg9QZQ6gcg0eP7klJ1hGTdSFom72YiqeIuPogkXUOJ0cSkw2PpD8YLhEDfeToJOZ4wBsgLkcTlyM6OHqrOKhxYi6uP7hLwQBO4WMFawCSJcYEiaHQg1H7fbLiMO74l6cGsBbXbhDYf7zkh3TWNh9ctBmvxjJBKJeAJXE6bxRpi/eskGHCHJTXk+Mq8wW0B/pj3wkkMQCPQMmCchZc5Hn3xXC5I86wkfbyLNHU5JUvrgEkCz0dORxd0FS0+k4fAPof+PnI6Qtaf8AvqZPwIF1Eyfk4ZR0ySAXJjEWR2yCjo3uPxhrXA50j3wMWVMvLy81msSzCDd4QHgjI5zjHOstZACreqnqlOTKOeARbbmDtAzzkUmorTMq7x5EgdJCX3TAcLkJZajyGzsvDCFPTjHXS5i3C2PMTiYveM3WAT1POQSwANROU2L6mkQcTN6qjHNyTJyJtMESRElTSdCK6DKPCGt2ZgMU02WQjYkYLIkmJJWeOsqAigecsI0bG8HRAs+uBIl/zLiHziUE1wOWS5L8YJ4+MkMf/AqxGt5X1dGcIbgIJ6pmPfALiBmQEg8zYYYHRQli2HvkRfRfP5wS9CvSectr3YnOJBQVOuSUAS4kIXdikGtWRbkfkuZcnSsydqW/QwIJikSkBeNOk9MEBl7NgjkkC+XV5sBpk1POJU6E+HDa1gvSKeJXIktn5OEpABPYtzzmXNGt5M8uHEcEoyZMDwYAwhgtsbjFaXnxXPY9EveEXRnHLN/D74RJeoEIUXYB9ZxqJxuO8SAsC/WQbJUPGLBZI25L+J/WBsmifDlfOJFEFSTOEvGHDjZSqNveMhDihKFK8t5rZRyjp8rLhDuZiFg+MSGhUdBX8yVDxk4mgQ7FzaXfcDPoBjiJwn6HFqJTxgDXTIOh0xhlpOEcYU5YHHGBDWWgt4dd5Ac4xNYXhWgFNMJ04tqAFNEVfq5IvDLeIBQ1I4yBrJutgr06wAlLC5/3LcEgiN8YSV0R644QUIDZLPALi1SBICpRNExxJ6LNy2mW0o9dF4XeTMxlxiY2b4GE9g2POCJnqGtDzp/RHDAKTyxy+cu2SEghY8Sq8ScK15Y5salHtM/jDGUx2woz4p+MEwzQbg6xmZ7xlSt+rIlUkDEgOl78msUk6wFQFw4tNotcqIIQU+khiFOFMnRaWwlAwlMTZAkWWWNh7kqsRNkZDmYipwDazc/rJRSOYwBmadZIdjjBTReMgUkVhJEgRhpeOcSsrjztQpW0GNSM814HgKwJsNLR4TmSQam2hyCucMrlovvmffIWEDDLTp7HnBezS7LcevOFxWUaGEkMHAbTn33hyghANHNohHliPBkgLUEBQAABQRkWqOMS4KJMLFtQtZHgV5cHClJC0RLpGatHlA84dMlo5cfCvs8oHyxPrg5hqgMSN8ClTI8YvSk0BIh718ZAFtKgHkTZkEApa5JxwNt4PjhCFyRkeFR4lwRP5icYFM0Pozj6i/cCCH3H4ySTs3NoqlKJXF4mzyzkEzEwP7/MlY3HwN5WsQPE6xuiUroTPwGEsBspe6XxgqPbOGJg+TFTfUQ8Tbllt9sPFhD3O5duNM6pWU+vYfnJCFyraJP6cpDu4amb9sm9FyWCj1UVBzSIwi7zhMiItgBFbwpIFw0ZPWFjrIUyZTv0kxLreB84jL/8A7w0f/JDZ+MN4EsIhZ0uM5DgGfWeHCmTcRzvJKioUev+ZFQBb0jGSES7ekxAQkYzUvAGGCLiUeL5wyWH6MuU7kv58ZE0CCzMrX95YwEZ5ayGpyjHeOzENsiNCAeIL3e8JOvtwtC+3Dk54OVqX8C48stHCUorPE6sWJ0YkJTey8AEjBM1Eg1Y+SMPKRMqHp5AOlPvIsS8ZgjZXjKmDf7n84syMHfRG1S+E+N8Y1MoGq8hp4fmtHHsyJCacnAZJkKYwgIokcFYUTdPhMUlKskVvam+6dLEjNkXOLJAITfOUgjh0uSwlRusn5ynNrMIUolu3FoudTGJDGLFusGQpYVaHyDR74zIyrMdJ84yPFQiY3+WPXAAE3d9r7aMkWTIzQOI+MN1MiNJ3A+MQpQbkyiCDtZwy1BUOJinB0SwrwAvtki0pioLKe57rvJv/Rk21+QwF4KS5O9CbCrV6ii8HWQSz2oZAePd4muaGDSHcODR7XFRw0yIiSJHaJ1jGaDHNZA8hInKcAQVIsbR3Aj/APOckeMn1YkhPDJz/wCFjYPdD1ithDLoEJPCMXngHSWYqZyh5XikZwT8/TGxCCOR4fnJakHraLPafnIEG+QnBkEhSsaOQPK7wJgJRUG/XAABaeiy9f8AuNQmOG7DrI2EMOQs/hgZwG9zn1eMgCb3DeO0bcihLA5CbGNBNXbA9mPnL4GMgiISvUYEbDFiI/Czf/xc26ynWKTX/wAejf8A81bcTzJKOMUQjYCy86h9s1K7/eLxBCyJC4yUU7cXmlJGmEmXQ+cTrNy9S5CwEItBpSYL6M2/EGIiOmj3xL4jm9YaCYDV7yNCUsNTHF4N5T6xllVSWN4gAY0+WVI4KRIrPC+uJiYuXaII8Q/OJNxQEzvr0yO1lYJmhFwQewnKaUATFD3iZfzSWqWohEiN6jjvFVbxeIK3PmMBaN9d4wNBkeHIrqp0n06eTAw5W1uJ4QkTKujJkJuksIgQ6LU06njNzoPS0tZR/s4xIolqdxnNQJgjAjou15xZqEOXRlGFHzODIADJdGKUxMkvpeDJhhBkhjy6wkZgODC+JzFdnIHHeLNDYbSal8WvpjNaQUUqbfhcZanAXe4n9+2QJMj9En3vHKVbbar85+0vrGRTlUYW7upAZExBAnBjjLYSqNFUHMS3kSV4JIgSaOCdD3jjGHJIAimtb1OcEok9WiQztQYHsSCnMXMgKcTd4KDFCQYHjgCn1wUwC1uhA82raGEA00xoxB00sIhmsWioLIrCk35m6yfgQk6Bo5K3rrAB35Pz6YKl3JLLN54BK20E4wKgEzaxDPviksZWUk/bHWNPjJpEG0FknUQ3nBcSS0OgikHWbK7cBboqOtDBOLUT+4yoEKugb+94MoCobHk+6wd0khy4A9smO0EFKJmeed4ZFMK9/wDmLEBxXoHEISYDl4PziVIgHklvsV6uVaSJTrAPQbD76YiMMia2vyY5MESEanpimGRqcHfpgix01ovOdMjnDnFk3Bw4XunrN4Y01kyeMm/OSF0IZDiYy3pF80GuMIRFSYghyvnIIUOfOcjTziQc0jM2Qf5iMEyMf5gLDeoxcIwwpEBJY5JvfOAMIlZ4VZLtTy6isZQ83kM+5U6xGJlwgYxNaezGLqMKfZIshOSdDgg85ASfmQfjADoVw8AGAT2EU149Qnuxigcm8sg2ImB84N8x3JQk7B09R1iMvEQQFjycnhyw85pJIZxlcjskxpAOAbe4zxKHfqMToKmhdqoptbxHmGCixJkoosCJBUYyDJoNJgS3MlEhUJWHoBL5IJXCDimEcSsCyT0wEWF3p6xW+yTE2B4vFh54YC5/3EpBWG14Dy5ZmhgQ69IYAscjyarxvHjBVNkTHtIeuOpgVtu2+9exk+SQJ5iD35ydtBgb5f584xOhL3PplxSpX5zsWWZBaYROCMIM4UoOpQ9a3kfIZJUyHYwF+5hB1mXCmbAUG3B26RArZ3xw3PviDsgpFuJeVcd4OEYEAAl1yrfjVZAAiQdj6/7kztJ2viHeIeDSy29pOQfnG4PSVnpIbW6PXCVRLRgoLhN1ZxgI+aRAMmpqaZqYrAZ80GwVgWIgFyNAxprclqQk+pcRv3xIi7BdTCdCPJHDgsKDE+EcCKHc5OqfRtFflwb8KXaLyhGmB3ucRJRRjWsIUF7684/Rm4AUNQaX7zjUEDqsWj4lrC+DDfkNYanJDOwr+fnCjsxMbIwaQkJTyIn0I/GH0QoDttfO33xyOj5zXnkxIhydRxmNNYu1HWEJWCByGdto+cMECh6ov5w6cGjN+/E4NRMnc/8A3znnficOvlgTJ7G8YCKFVJJEJ/cF+kwwarJQ5nU9mskEIGvTw5Kh2seMCQUdusUuUpUnOQMQ7w+U9miQ3zTbvNxhrysv5yapgZ9cGTnNwnXMbwNlNslJebJxoWox/HSiCs/Kx6HnBeWXCRCVdBOHCpQSBSx7hffBxDUIIcwnmP3gPilIpJPSEPMT4xEBIWFYk0agrz6ZACGQAQrsLB3N4HQBmSIEh+Q6DpkIVEqLhw++NsHz3jspVbVnHkLNJWGnQ1BthzHjEs85Zww7jB/5CczUhFxI943BbFCtg+FF4ROAdMZMBaCyg0uAFw6TagvupsAkwKF6IxWkOcxllBHIER9RjAaonImzt3s/MPzhIgVVAA2rlaCae2bOIOeEwNTo2oSv5PYxJaZDqeAe8e2KnFl8RiElJCxvon8/GKB4X498NYlTic6VhoBZig2X3fnAK5Jg0E8xHkwGOhgQPNZZcNsLYo8WzKVSAT4zlbrUBXtAxQgYMC4HksKgesArDFuKp0yvzglIedwx5OTJ3MfAe/8AuODJqi3rgvbEiNDryY75e0CmoaOckPilhKQSPfBkGoowLmhTZJXalnEOTL9Tw+cF2MCBJfKBL+WP/R2FVtYgJtjJCcIPERgB3Ysdg1h5GcBwNz8fvDT4Sm5cv3jHeWb+Lo9A/OKYVJ6q/wADGMyM22jWCXZCF5jKbFqunv8AvLg1k5lZ+D84CEAYxE3fuc0ZJDMwanEJSQFpBBjy/wBOQiQ8QD1THSYEfxRg2SNizDg/TkYwz6hVkjZeJhnD/wClk/8AwrLyUXpDiU4xrk6HCmJCcpPCGf5lEGQUyQ3/ADLM9fXAiEjqesVJOx5x7d5xesAhjKdF4/8Ae8ETNDS0pdYQeiSOWSFJksxCCp1iwfqAA5ejEixpDCPdiJtg7cWZLxeN9oVr0NKEr8ReS2FxSL9/vE/YkcJuKDu0YDveJRe3p1iWhqYBDBf163jpRXBrBECQKAjGDenUI4dCAf8AuMHUsREdT1eKMEREhHNqwtQl2xjeUkSdiHftjBu5Pr4cvnEEoCQE81TgJZBLcj7GcW6BV8KfT0yzQAkllVoICqmCE0wsPtIWAOmFfFk5JtA0g8YqK07OMEZNGmwwkPQExa9DIDOY4C7T1yv4JW++ZAkUQS6QMIYBpde6TRHq3kQDoPRfGQXrh79Hsf3ABrMR4Vtn7vKZCCfVH/MAJYqod4XxxhQ9MmxWUtAhVQG55xX9KEzhyGRy9BjEXO82BO215cNk4UWYg7i5OfFy8vjmOMW4qd9Y3azlMFKjryd4mBtcQOxwk6BfR/cVirLgejx6mPAwtUH7Mm+YphLcjw/7j1PkcP5y7ENXqdEtPnEvRlQjS9b3mtCaQFZ4cbjF72hkWSIp5YZf1lANgciZfwZOCugq5fv5xnLbS65f0ZBdmpPQDAo9+cFvtrCSw4kduiMpSDc4WVf3gK/hbULf57Yh6m0dHp75GWCQDcOoxWQIBhkZ3xkXNSZ4eCgorExWNKKCedrwBFZAJKyPGQ/oiMFho98mXWQZvX/0w1X/AMWMrjGB8NXxM5BsVERMVjJ8tCLKT8fnGCQkoCNzGGYWAN3/AHIou8MISDrr0xax4ZMB6ZJ/4g4EREywuUKcTxkgoIkABI8g4KGO16kQlamLcJXgdqBPEJgySbKGLcB0tJDLAaqjAYSIncYA8YIqgoEvmAOfbDuzQWjUB3HwcGYFCilQlgEvI8Y0UVFYjJfT95sqfoJC86L84PrZwAIB7LKt1bkjViuYKT1L037YuYLMYSSnlIvuzDE6fyf2FExsF4x5ycCOUUOsNoakS3BQUNiNnZ4x3IEgiv8AHvhfTEICHk785LuokyY8scnpgQ9QRpy+UAkLIGSTw3iJjPvDsho5HYteBCYShLAiWd5BJ5R4CyIpMQecqmaRWkPBLtWA5yB5emiULd5AHAbx3y05WbHWg8HvK0haNSKb9X+ZMxlBTVElzFjiMvxdNku35rKQaINj09p/uRBmsGZAJ/Hy4U9m8opiNPf38YKZ8pi8l2QXAY1dwF5I7id6jeUJeVwb/Cu8I0P+4xtIc9+uBuwmusNwyRjBGXsYgI26Sl5hHNu0gJg5k/pjJ6EOx5wkAhjVPt7fOFKkoPhZ25fmiidORJF7cYAZKGNs4xglWgxlicIKXJjwJcdQMGIzZ5/8hwQqdDy/zCuk0ehimoCk1Kf8wJJhkjQ7/DOMAoSgny/n4ySctHqP/nzloRZQ6C491MmIngCAmVv2Me2spZ5yQOs4jeU1Uts+hY15JAExA9y/rKdJjO5IfN5zIE/DNkw4bo/+OFlxH/w/+TGKOPUCMdW24WmV/hwZuFEFMg16hhmhwUBsr94UJQQeZ85BUcEg5JS3AfzDCoafXFUdYyGR55KKUMKFZhgJAZY117iY0H2YWZTHRVsrQwmTkSEYspBSCExMFqrKGKNcGiI25IBIQrV+Rn95FghsJQPUK/DhJpRSeB4FhxIgDGRFYqm2TWsnjoABIEPuHBeBFuQJZP1owZxj0Sbjx9MIUYqMaesk9GliHk9coYSJBN+DzjSmOw4prnknphXjYlMBQco3TyQxi1C3J0o/L03gRyYMwBx3gGdS6Jb5g1cPrxNJqLrflwhMElpfuWemLSpREk/xyRQWIniEj4U98UoiANRFulLY5xVvgFW7JmCLjqshUOCC7sTF8ZPDXzNuxfFYewOwdkLy384CXhJeabY0TwOOECt5t7fB+csKyIbE7yaBCNn4Pv8AcVmqipxZWAc2comos/kwWwRQptLSQMmhZKFRFf3A1SzOKKe8Gk64cR6NnrmpQ6QmN8YJDEH6eMQqAN8oOsvxB1cT5zUoW0EcWf3CFJbeq+ZyASw1WdHLitKeZjCohWEklOWrMoYqUkXkXDAIxz2C4Allj1n9mSKEofgR/HEL3D3hS2Be3QYjQSQNH/GVAK22oGScAJI5b/OQIqwvcGPb9ZMfEEb3c5upLb4AD9OJlHDZSQABdMn0IXSYGPFsBeapMfqH85NhEyqGy59cgAnpkxknGSMPHDk3q+sU5F7v/wCSPpw4SRFmTINKLxNn5xDXYB1MTD8ZdNQ5HZ+KyANK8ktfzEwZZtMol/GaSyJ85qQiIHeIkRrveJU5MtRvWKAUK8ZdVDL7VXDQwxHGARxGUQmIHW35cZpFqV6rlCA9a4wIIRD0DeBCiSDZMEvBRR/uKXTSN93hTUcxkPkPtuSHNoT2vWQ/itWjH4n5cbqmYqCbI7J/OIy0sLPPOCBDE7eTj/ntiC0lPXEMyC/UfTGN7bnvECk9g5vGMaFNwmAISxENSZomg1FnQdWeukpvFcCiakxooKKrtSsSLP3vEIBZP2B59HCC18A6XzhfeR1/rkuTGYoHrhLbYFp47xGcstka6K7vAMb2o10S5A0kBqAtfScSqgKUltIpAnqmLK5gw4XCVCS9XG8BBRViOvGQAkFzxiTI7P30wQn2cQjQjVYpT7JXjoopPEzhyMAgPghwEXyy84ARl/H3eMjvV4bQpHeSmhnEAQg5yYG9A36fnElFqfr3jhuzc9YaoU4eOwLR7tfODOhL3KXE7jOEQPNxPnFC3bvJIKkzPWeTkwOtHlyRUghXzHgvJCgcIqSL/bgN4Wzqh+8unHDgrfvlBMCh67/WM2IkoCWZxSELVQPHsYzlJaC1Rfnr5wiiRUuZf4OQWSAHgIID6EZM0ya7n/zFmLBTq1coMhCGoadl+2MYzZQUpPNp9MICcyTQRPrNeMIAUksy5QTTn/4fGT1LPHWRx+cNZzkzvBmy9VOcbrvBCg2Lc7E+HIqDKD0kYlxuG6I/QxhaJcGY6wPUEiTz/wCZBBCXPWHyJ4/zJspRa3kE7CQxBplyOv8AmCrbN7byxisNQhYl0YWBoYId4KA7nBuDrGccYFgkV+MguxBogIcElPXWSUQLbJaHmfkvFkpsdJLYeQQ9sOwSyiCa3cF4rCJsH3ciNnkhk/n6zQyXxUv34nADE19z9VgULCkuf+Y4AteuWU54MSs4QEQjpwlNk0DtduYO24kyb8CYtyCJi+YG+0bxJBCVgomnfEsYznNmGh2evR9zDebZBoP0vpjo2OYHw8pgKjoS+k385yRGCNq8Rl/oFRRIeuEsomzjxgoAIUEhWJ3J3ymJBSBUB13ipCj2vBECE0mqwNOek9/vzlqN8HDi4GejDov/AHHixwyOe71mtlqbyJRU4zHc+c0iZnvFpLgII48YIP1ATXTgECeevbLE54/1kwwizQORyykAkcNgqKQbeuJUzeDNUTzGKpdLE4ozatOMkW4Er71+8NLiwOgv7x/lDbtn9MKtBmHPj8YHFqUgJuO01OjDCsu3lfJ+cmYFKsSRC/ODxQOlSuCgcsNsgs+f6ci0Q2CbVE+X8ZI1JuIof7lVaI7cYAgmawE8ECJABLthZqq7wQLIiLq1MBPnJJNRa348zWEEGEiKb736YM3qe8bzx1hXL2M8NYQEZQarAvky+MPx1iElw4MYjzAkwiJLYwJBKaWw5JhAx6oT84uzKYZYJBKukwMKSecEOTc3sx0XMayAV64CSE1aYSxtJDjuTIwUTb0YBMBCZIsz1MVWHGLIRBCNjxj4LoaSx+ADjBEM0REAliN2V3YJqFbkmBjtB59sk4XMeZ8+uTscnTMUdO0+I5wGwLtYPvH4yjChs1Zr0r4zkQ6Oof5/MZSBmiLj/c8Qs9sBSDgjh6wS1oYRYxiuUwIGVmDmf2HWGIgM00Jdp0LimHLB8y7FJsUKzaoZCIPEJjQXlJtSzcTjqxOEtR3G9cYkesr6HT4x1yIJjol5jzkdilyFvfpkwZBKlnl+soFIQH5jCAFNHzgtQQrYentjAJC3wZ+/GEkkCKfv3vKkIDw/fu80gDwb+/3GVjl4+/XJlnZ0XH+/3E1zgl81NY4l85FJpjC2U8GHQtOO0wn5wkQL5rFo2HrhIgwc5KWYcuf93xgBlBz6YSnXid5vbkKdtZIAWOHJmCRh2DBflMJqsh7RIeMV3CKdmf8AuHOSa5AIifzxlOPNQJ0dkeuCY9DUK0GNbTrUIZ/WIwCII0Ja8reFfJvQkU9sg60Yg1MLPav6xgmSR51LPy4/SQICaAqOqy5Kv1wY7YhYPEh0ers+vVxzE0AUAerhUlNl4g/M4oBL2WrXnCfziOzC28g/+BjMVmsjJjjHAWwzYyRr+YwPgSSCCSF6jI8sTiZH/wBPzgFmIEbAl/GstdTPq2v04wyIeILk6uE77xVCfnOGTaYnEhSnOsGmcvcggmERPqbMGMMC91KD+5BjkLJQaqpfIwZr8jSUJ0DUiJ4ny5rgcKERHSYUAkD0T/7fkwTPdMuPEgNpqHApESSENefbAACwOizrIfCJ39/85yFOIs1T17/GR0KMD3w++A+1PI8mMRGIT5xAYm/yd5CIsa9MENMYgqGYouJHEqHU+uDkU7fAX5fpcaapOTSM4bQoFpUHtmsEpgXsQC5jkxuVc06EtOQWSqgSev8AmIKSS0JFxQgEQ0RPn7Ob4SKET4dZAger5wgDsY5xYSpC+NZU88z9/wCYkPmOrxW5krFLreMjxgT1jpngmsWwJU4loevpjzrNWa1ky+m8UBJbjU8HeSMC5Sg5g4MByaR6BeJDjg8YyWrxkcIxFY8T56wkkKxwDFQZn6VfnCNJSuiaPnLBeACP/cIStEpg/Re/jCicfGlVD8ZZKINWoMIaRmUQWJ/fxiqqxCtO/wC5QMMlJlaX4N4kzQCdCEn4nCd0/KK/JjxqNweU/wCYlRYNTc6wK7laeMSHJFpWlJC1o4wK8qyYCkgi6MNtmwW7P9ZMAMcQ/wB/TLA5jKoWTWLvCAjMzhE1vAYMrJkFxXgwGyceC2sMZNIVlWDGNKqVpnw5GMQkhPCJ+n2xwke4EJ/3DlIqOELkRNGowrFFqcBgxHcZzATGKOMZOj3wNhoa3on8ziwAwsTkHg+NBUfx8Y37ODDprm1Z8ecA1MJEki+hfVwCIJHLBMXsY0PdNIQvuy93mo9ffvxeNHA/LB/n2cZ0RWA1kjKKITXn2yFLshv4cEyQSlVHX8xJiJVB4/7+sUjRqen/ANwDIE0Ozs++2AyOB8neErBGwd4wkj0y8JCIkiJCJqMYjQgru6PSt5HuQrckZnifVxw5qNkquoPKWvDDWEqlJxC5LSBU7QCGnuC0HBDeaIUu+5fHnJoZATJEwJkUKZjlXVZGZs3G3/cVAJIPGUJesch9/wBwU619+/OO/bf377Yu+2p+/eMHinv794w5gbrOuODFTMayDUun+fnJLsk4hXU45ID0ygoxoW34wikP0YWQksaGY7iT3xiKTJF6ZNVfy4SGQiWksrHRYZXGtxzOX3wTXY6PzjuAo6YfgOPniPxET+3AAQbKqP8AAMdyRkpUW6+J6yuEkHlB/riApi/G3FbZoaiSnxfvhKRPw8sroUH3xOAeTTdLP8xnvcdQIP1+8mRJyDVkPYM7kFSev8wEqRUDjEJJPWaVNuYJE+Jx2gfvsAMdGH70JkOCQIDEbc8t5Q3vs5xi80FdVPecQ3ODMhOSDBfpnPnFI8cYMg8/jKz4/OKJhZRZOCwhQkVP1MSGDSTDJDgUQH7SOMIBRvxWMWdlyUOtYjGCUYCQEj1i84IOryiJk6xBY+BhlHjtCEo6uDtHAAVsKaVJ8BHlx6CqYTZYpPoPfYFwhSlBVfE/LCIclLIlCqmpXEvIUp5+/wDM0up/X3+YGSpgaJ1qfvzjZQIUnqZIaVomPz984lDAiw0n+5CkQ4YpJyUGFcmz17wgRNfEf8yShBG+h/HIRsOGePXJA4dQ48mJpLLgpxCyAPUYigjJIbHGnjoAnEOTs+MmMi1EBtscww8nGJ/oTlk2NjWsQRV20hT0adAHOBDMm4M29ol3Jkkx5qFL4BDzreagqEhDvEigqr6ecKMGQER9+7wZTExSOfv5xiO/TIZbGpGcUFVPPWWysHnrJJlrjGGI/WRrj+4sqWDEurxNpLM8AvF5YOvTFVIo7wRa3XOTUHuNG19gXE1Oe0Gpf3iig3MRDheXAAFUB64wQakQSj5xKFUloNvubyb6xVsSURx5zV/YRKQSei40CCKkdjGjAhzQBEoQDxL+MnTIYxzrGck/Kn/MKqoR8bYxwCUjLta+Mb4JNYVi+acLaDitViU0EDgt3+MRYEjQ0Oj5wCIDAE2k/wDuA5HZ81fnBfS4J0ThPmh9R1kmbWEWgWfgxt8CifGJJBKsSDxg2Y+MiWPb1xmf5Oaa+ZxWUN4kWsrcseuWCpapaxCRw8ziRvbEB79MWyVg/wDcg6H6jOwj3gnGoMioT/cvI7gvFCJQWYImjd3k6ZkVvmcJanIZGr842WKtposvpi/U83y9aH2GTKEqAoGGwUPnEkEyOTSTDA6n5YyADkLRg+kMdTleiRUsb8xyI3jUxxr7x/MMBGhxCCiAhixjDJAqH7985v6+v9wjDMunb7+8okJ2cvP3rAXY+h/3GS4E1rAlW0ew4+MiYEHXABKI5ff+/wBzVPQcOO3DiJNc/OTxyQwCnM7jr8N4BXwcNhQcuvioyCblr/GDmlSK2YlSeO9dI9qyATQtZEzVT03hoAQonaW7bXi78lCU9RqVHA698SAEeHgv+GKC+I7n7+cAAyYjo/fzkJzPOaRU78ZY88+M174qvB/M6Ocbgbe+MIhCjllLvvyZMhePK3jI+WLMWPnvGR3IAtr1g9jy4j2IWS+3vxgmrwm2hniDDUVWIgNL+MHbJRUhmfSPzlWQq6gaZ45ZwgQQCyZXh6Rk+LMIKwiX8uFW0U6l/A+cJCBASbucddUS26C+65E3YRHMW/rHG19D+cYToeic4pSiIb42/rJ2TKtgUe7ky9Rd7/z8YwhER65EIABY8M5KYnDImycUphsPAp+R85ApVhBAU9zhIh3O8EJZaAIqx+ciIWc4qvXK3kPD794zPnxkBCZTeBh0Z4vvkTCGuM3cGUAJwnRU8e+AiQCn/chYGh6O/XElA5NpkWQmB6a/zFCoBB6YlEqXWJB58Zcyf9xKLOBgAsMZpKDW8KdFkkAGYkVlHNdYvgxHmVWNe5JhZRqEQFHSiOgYwkjEsC4+YMmepFaUY8R+THNEUQ4AAj0A9JxqYhhp1r9cemAopLJ19/m8it13z9/7kW+JN/fvODJLF7S5n9/3Hz+Ln/f7hCw5CM+/n+xGOrQog76fvpjXFYOtDgQ7J27j7WHJShrcYKC6YP2MkkQaizusFNwpTIGkdya8jFEUlI8jxgk4SrZzxC9jTsRvKA6VJ0Tl2jCTYZpGmsnwGALgiC6RFeMFzVAXjBqy0JDxkcRWwgVs3ExYz11k3r0BMka6itXcawyDF75r7HrgJUj1Fz/v9wf+Hf3/AMyMQsc019/5myT5hxbiPMdYe2rOvv4wAIhjfjGiUlvusAwomZTvjIIqHkocgGAVbcWFHm3vEBJYzyRiAcT7qZHpJGJMyX3jtnIODtX+YchKJPVK/GElpyHd0fq/GM0qta1PnId2Br047/RxkEEADXBhkjLCNvMe7g9qMvZ/g4hcmBdXhay0ktwwTCTtzMuNLhQjWnr/ADGjBsEVLGjm8YmJQG9RGPMsQGlbfvOXnQVaMrhVvkwUfjNIrBAkQY6gLFsMR7AypCzSVtXicovrrDBQAdxF/eXn94d46rDhrDbSPeJadZKenFYP46xT6Y9yemO5OCoRN5CeoY+BEHIOluEEwazfTN3EKehjZDI8vnAUtEGGAmLwWWg24yAOsCwbnGKABFjm95A4ICVAsOdsVOxy6EOAQs3OlMpAyoMTRoWR59HCJByllJwR0SdYXCYFk2YV5NfJGFYEtQN6rDBkS9fv3vGpi00n37zjTI60/fvdZFVHr9++2AVWJUvt9/5nOpiHn79jLBt88z9/5kQvmruT79nGBRyufr7OEhIWQsTiPScZgkLPv3vGUxXxyOAiIZUbPOSqCESacG9ENrlwAhbu99sEpDwnnBkmI8/rByGzpzqf0D86xSKKmw7VT+PBgVBEdOzJ+1ZhhW0/wcEBuZTlAinfszm0/aoAHaanbTOsJ/RVIiye7jbiMZpMHZ4ft8Y1Ifm/v3nGR9mfv2cfMdxjqH3w7e+XeDcHXWX/AAGFIDvrIAdc71PGNSEeXFJLveHJY4OXIBApyMN08OXkBw4CKhqXbyuIZuN/o/KZPWGhVv8AjIZhidexr9YhMpKrDyZOtZyk3Z6vF4QImo0Atr0MsQKG2rXpGLgVKhUOvwZEsaSOiD9OVxCB2BkNCwJ+jzjFJygJe/TIVhJHplmMlngWjalBhJ8hltlTf7xiXcuPPlckKLlIRH8MUOUv5wLnnDO1YHvhqQ1WoJfMuKAhYwIKUdEuLb6423KXQg/bB4zvG2DeIvGc1hEOQKLeNmDJuL9sJLkRIZIMmSZmI1jnJ8NqQDm0Fm41GLjo2+mKxMB1ijGERXFGXuwYlpaswJmdYqvbWWaQq7G8gs4yI4eSiaU8Q+WXDVYdEUxEzdFsWmWBYgqCAu18Y7YkdZ6B9U5xrkREyQbolPYGCwsQJMPDpudZ/OtR9j+3jut8Rr79c9Pb7981jEP7+/fbGPMcz9++mc3vnr79M7n8/fvGMv3j7P8ALxIkWpn76/8AcJNSB2iP3vEFsLffvnBxRfWXGNJIyG6/7gtEklGsqU7uxkA0S+x85FRk07jHi7ekxmLCRfPrjBoBdSj0cj0YQuBz3yHpkFZAbxVKq+E8OGNrzDbA0OpQ+uD3s3SG4iHdinpGFBrvuoL7M10jjvBi8/J4HI+2IOkefv3zneIxgmWrjeUGbVuOpqT7OSTEBwf3EzKbQ4JAad+fTHCUSG+42PAxOGkSCYSuA0LQGi11kSYY0h0HQZcAgYFtdToqRLwsvtktsIO1F+xkqbTxcWHLgsEcSnd3518ZV6t6pd47VAL8R+pxGCsCNyx+seHs0U9n7wKfkC4Xd+7k8sYXSA/U5V1qI65xSXcEVUuSuEgnu/zCbeiCd6R85H1lAmljPxDj9N/GBsTp4j/1yS7CVCk1+MZJtK/+aEgIum2KKxfREQCiQ7T61i3agLZ2WbDJFnjIsgdG2JhWTkqsb1lidGHI04c9ZqQYLk6wkZ/eAP8AmS7sypGUSB4NY1WeZCr1qH0Qx2FKvkqPwQNeTNgde2sCqILEnRlyFMCkojOJBKRWBCCxtyMbp3DGauSDiQjUEXFh71ruHjAZkuLQqS3KDrFriNOGrQ972wxyIxAKzqh++NvVU2eXeA44SsTlufK7D+5zHPAcn2P7m2iF0F/f7znNErC/v9wVLa0Pv3Ws4h8n377YTz7+Pv44xvtTZqPv/Mu/7x9+3kALhr0+/bwEvLFmDIhoaSk8mIKrJAl87yPTkmOTnCIQNXU5DJQZOUZJNE2MRD5MlVg1MV75YoRfYxDiEtDEzIhi8ELRmkwcIJtxJp/XXGKkMog2G4jCTIrRjXNYVAtnjESqh0h7c2x0HzjbTdeO8amBPtirkeGmajEb+XG0xBZEaPrkxA32l5PKALecgCgFx35c5RA0d3tyCYSAJV9MaG2h3Qg0QTbU0Yp4Mipc+E+Iqu8ACtyfcr6YXLjHou31e8B0kuIFlwMGyqzUCfcxhFLsiaBc3/cDg2anJVXtB85FiOidX4yViyfy5tOFLU5bh69O3+4ql6xaEU9UxSYsRohwG777wAICUBB0f3HqyAS6uEf5m+jBFvyuOe4TEHr/ANMcc+B2SH2vA04Sb+ergA0lO4hytU9NEHLjieeJCLf7hk1whO/usm2jLJGsAntVAxHC3A0tldYtzyoJFlD3zpN1WCpb400a5ybvPXHyxU8+MTCfUwJTrNPjHxlP8nWcGx3OsIAWRaNnZP8A2yJZFjFOfxAOEUySgoTdCnwMNBlKTBLGjtDWFonsHGXEHtlhS1XPUFYW3vIVfWCQAmZEhOh7xrkGIgEJfCwwemOBaGbdl4kRL2GC0KlgnkR4T8ZTIkFq4HtF95y8gCFSlAdX+2enNxuZ/f8Ad5LTu3kP9/uWIIqF2n9n+RkrQTQsvu/esIuqNnP3/mdjw2FRH32xe+ONR9/GLPHxx9/G8Wynxx9/9x+hf5/OGiMvdv8A7/cksi0Wpj0xQWFCtvj3xCAELnhwgPanJwjp01gQBA88P+YIpHMOSgyE12PjLTo8F4aqQtJLDnRDbZqUE0tywKI8jSePTI4aSTFJHqxnnAEyIrCYWOi6npjYIYDp9TIo7iYp5NSuSMnl5Uwhol1HbIbwsvVAaFiLxynVYanwLHjpXPEj3wYYJTcONHIyKwtf5hLMtKV4s7wGElIQ6ct/WXiMR2eX7hZPxAZNJo2cxxhURpDjt9D9od5uOJImEanrIUQiD3kaCKV1E6jnC56oDBQooCusnCBQbWOV9XBrxvbZmDGAQIDRLBO8c3YkQkrvxlQ04MRHnbkZkRZM6/s5x0FlVZIXMGAiyefAYiOG2S1XPeAcRItDp+v3gRgARiHnCgjWMPwY3TizCYBUnz+MiImQ+1rDdkJYh5/9xCq6+8YKBuCzNJ/MbsZM894Qjk3xhiS7AoRLdQEt9ZJrYVbI8yOCSQnhwofvJgJmYvIoWlcNOVy4eM0xJr895CT+sSmlxCxlKObYHXOEF/jHrnVwNB4EYaGzBsgkcSPqOAiK4ZucaiM+GW2CyKaYTOEBFtiZdLA/vAEpIP4ygGDTiUvnOOMhM5FGgBcD/wAVyeUgVJhEHre28L1L6pQnjQtd5GiVlLA06Nr3xQVkhqACD01+8lCE2gUIF88/vFaJlo5H8P3grANw14TzgjK1R49Pt4Aca+Z+/wCZJDOjjn7/AMzSk6uNR/n8zW+Oq1+v5kRM/Hp9/uFCdHR99fzgA2KTE7P/ADJMFyaczU5B1jc3NP8AmKr02GjRkIkYJnjbkwAiiUiB/cmyQYiXvnEHE277xfaHL+YqZdqDxgplGx5MhDkKkIV2JZ6YamIAKryuLhEwZHKToB4TCnvi2PIpvMj4YyZNQUZ9nWIWRmttViJ+/wDmL4ZJ48zBGin5MBQ1hYCaUkGo2ieuK3VVzsjCqYJKvWFFp5JEJKIluqTEVORCeIWFYESJVhSEN4eK2PEVKMPN4GERAKjtlMbZyTKEBJ4GYTp/GTVCtgBMx6ZIMnZ8uAEZBv0wAEpRJZSBoVu3xiHokRonT5bXIRm8sg0Thm8eqxERJXRKe7g2QDOOeJ1lDWOizEYFuaxzG2jIo4Vbdid7ucleO5E7TEvgLwFRVBX028ZJItqtrR+/nIHW59rf8xZzj0xDuBSPzjQJSiNpPmMUjORJqM1aFPZv/cQBWFWkgYRLldAlp5dYqKDPghxtKQyLgjDghvKf6oqEzOgi8H22aQxAfZyBiCOcSJupwuDEzgMQ5TN83iFg/wDlGTWUJ/8Anx5yp85D4BUptHmU9FxJgs1F78AZzQBNYWIvLSJ2FFG9xOeRCbEZuXGXIYPpr2wGuzR3/mKxQPJ6+mSRIB3isNbxNq+cFecpMXASnhzWO6pyEiUvZIEfGa3kDUYX5gZMeNU0AVLFHuOQUQLfNfJ/zE+hLRQ0hwsz6R64qhtno/37GQqgW+f+/YxlevL9+8ZxPE7+/ffGidRzz9+7x1vYm4+/+5+Iuvv3nFiLXk+/fTIJoqIn798YdzTA9OMKkiUnYOJgNw2dtYDFcABMzF4zJEgk6nr7+c0mNltDI4sySSiPTAY/kYgZ6GclJSe8KmvJeAEY6C08eTGS914HCkEnZ5cmBHpNvoZcSyPnFrUt/QXyEk8k4JCmB03iDXyR6YLEkk1Yxhl85HwJ+s10Dr9uIg8X+MYAgzgDCuUV43uMiTCUyymqD6mVdRkBIRK3bZIsWA7pyLwALEm6hW3eSUeXOCfDvEfOhVpe4/BjLE3IPrzkCK5qErQ6zp9CCbD8HjCKCQEsClhPM7y6D1BpKTD08mWC7ol/OQwZRog4lbcQ+xIAWrI4nvJlLmM8mJmuU1b/AJYGqANdGA1U2G3j8R847CLGtvH/AMiffFOI8RA1lnBDNIaOp9cEO79mz94tJZiR1DgtM4iTBfsZIYGWrGw/xx4cX5bZZMcN2jj4hwYERLnFV1FUWByyE+p3jDLHXCyqeZnIkZMYaamTTjPneF4csg7yEO/TKIjjMprFgyXMYOF4eEGSZZAdsnSTxkyHLkoSGwi9XXKXzqE4+RIMeDCjkSWQCI+jid3W8sZPCUvnk/mEskhETEJrNGeVY6O8l6w9GC/nHIKDU9GS/FUtIWTnyzvW5y5OHP3brJbyGUVP/JwkZLRAhZeIYX1gwcyAZYXx74wy6mACQ2a1vjCpt2v371lpnfj794yO6/n3/mPdTr79/ObJ6+/f9wzE7TO5+/8AckkNoYv3/GVEIq5mcUlqQMcv37WXbAw+jh3JsfL/AOYhRIB+WQqEtAfPfthQIRgD2P8AcVNLaHbvFIYEzE15MW7aqB+/d4Qx2bGpMcUegnM4FSUkeMN1jtnEpk73/wCMhLUPtjX85wKZEBkZL2RkaAzckkSASOzqIzkqTRgsZAHaBaLZnRGlEB2nemHqMbROe3Y0WbqN+M8zTZ8JiaQy7PvOb0HlNGAOKcqJ8pPjIWb9pyjcZEBt0FHJX4yQLqHvEzFaJ1364lKIV2CD9DDkLjZo6rowSYCkrJix1eFBOEGdOVrAAUQpy7Wsgymw5o7fXDUGQKysgMlST5QyRoSDDG3BIsO7o/1wZEKift9/GGBaD3XOSlWu8sbKyZf4wJjFO6pPxgaAlo3k/wBQ4RuPn8YCkBUvinHJlS6tq+MIK1fy/wCObsSs8zhZHJCUkUSTCemsR5u9Asnepw4eRiYADfTiQRU4cVTsSUyiezGRTBJwGxxQthwvZjHmMI4MIJ0OKZLkesgeMLpBA4ZoY4wsZoYs6o9nFhicKqSldOhvxiOB1OFMeoYJImDBnkSwjp5+MLKEKKhv8YwVLq/vjNOTxj0xxlsEsFKBBBCe3Ckh1IEYx5kjGahaqBq6QhwxnkSJZIDTi7xvwYYNNvXnAs14hZ48Zro/H3+Y8y/wPv4zXQ8+MKK3qOPv/d5JH7G5MSTbie5+++IHSoJv1/WQCK9oPXv/AOZUu5MlYWiemLq0fg++mGDWgL6cFa6cxw5CppNcXr8ZGFc03glMJbH99MIYUEHr/uSJAO7swJRBfInAIijI15rJ4RhNuhvUYx0Fa/mWC4R5ww6Vzg18qALvGMgDtGSTCHGzJx/iDnYZls0IoTtx1RIKOhK2wALcHrkouHmRErxvIwInBEQHhnIKWcAU+NLiOILwO42fVfXBK+aBOCCNVsLx09Mpk1xgkldZdnPZdTrCMmQFrNX6d5BglBC+UrAMdd4ao2RSgVrd99ZBLMuRR7ZMUmJHnECMZleYQuTMffOS1DK8hK4UOYEx1kziCMXHL+zOKlCeb/CsCikBbhI6mMJToMFnLURBxnBa7ZQCZgi2cjHtCfGn95LQBKfbjGjyS0FhifFCOxjAVSC6rrBKGsR0s6SJG/NDxhiZCwCnr1YVpAGiCCeVyzI2xzkoQi5NkjWVZXJu81rjOSbdk5N8Q5znI+MTqs4N+JxVTJ3OKSSTF4iQ7hrQHQKY4jJpjBEq0WShJboRGSHvetMI1QH/ACxChrqd4gMgnosM/vGYgJN1JHxP7xDmJZ1l8PfAnFUwFLSOQWSIuCJxCgaCpEEdIeN5JlJWwIBjxuI7xIXdRTAQudvhyASC/DXDdoToOMkDsEJocHy75iMKDj+8f+fjNbDl1/zn0ym/ZqP8/mOwkPOkffxvBEk319+85UHISvGRbs3Hn+/3I8sIef8AvHrkbUFPhP8Ah66ydM2ounWOhoXeSBLlDz916ZVKD+R/zAEqRPxhBSchff384leElEP73igJcA8/f3lAOE/3EiKZSb98SSks++EiEx3r7+MlQ1K4fT/dYTkjsRT8DAbhEIacXvAboMnJNsYQGKAbE8kuNDKyyqOcrIFQmG7Nvj4zTl+hOJXj0xk9kggOJgme4xCCVM1QAIA65hvGaGM6Rx6vTIVRkjU+msMnjoWOorFcpBQiqpmV2w4Zbm4Kgnc3W1duIM0DYdy/9ZxFnwsQjiXPN4kkXdBAVs3rEQe0DMz3uvxiJjEJNHUeXI1API/Gzzh+x5bvxgrzgCg+vOCDJYIl242FEW+0P7gEVO36GBBIhNWpMtSpMq+OckgmLLzREK4Imo9cLNpT5x0QrmXjGKYyJ4H1x4VZixU04wyXdXN4iaYhZAWYl5MaYFp+TFi2VPnJlNJ4wKVSyhEQSOT4ZFBoERiXReahGETR4BKQesVggRffvxjEr0RKfc5yFKyu5zcyeMdRMee8CYjXWFjBrWW3nHNc95H/AMxsVgtiGWgpwIGHqxTqE5liESoDfWAxScEBVoE5L3xgtkITf/uCs2iBqQP+4z4Iodl1+sWdcV4JnBAopApao+T5yBUckIlMcgCOZjIqIEpTIXKdXfebmWvHLK8Eo8zkMoGPEwHl+crI6mSAY98MkwUOOY/6fjNeOj794yYeuev+c+mIOIOlff5hzNXZ1k1H4+/ec0UaUen3+4Uths59fvOTQWln37OQs1x85dHcNvIf5g7jEuSgjQfYxIABBPpgs8B6bwQSpLXjEJqI4E7zenFZY3mrENvWRQEGk78uCMQrh79cDxB5EqfX5y19kPvPpg14YEPnHwqFgpv/ANwggkmXWLoFSoi8nY+MYr5I2b28yKT5jLm3CpTlPJWRhMkFs6HD+WK05UMj78PpkOwPVxx6xgSFqL1A5HtMBipvwvfRjuUtoy2cf3E1EhIRARyxxM5sgYMnIwRIBLYjKVVnvxkWHiKo0dVgkobQicizsmygsTjElCimFNEYQdGAOvcjJICBuKX0THc7BQR8kO8RFG34GOD84Jgy6JqfF/8AjAyBlXWFKoAIP0YQ40QHo/3LcYvF4TRJ/AwYZckUsfGqyHAkFFyk4URNteuTeBAEERqEn+Y5qUXX1KyBQxBfhgrkI9hTJLGeSNOJsRioGDys/GQtZ6IKIdT/AO8SzOiFlIfOHjOwjSOdP7gGzD2ydzinEucMi8jIwXioR0MhpAojwiPeben1bUY0S/hgCug0w5EckQlDtMZdoUV1UkYVXCtjkDtkEPLrHZVnMeAZXaEKpuMe8ZAMNsawBodYZkLSnoGaxH4bqZiSqMjEkijFZ9HiiAk4PvOEmVx6RvdqvjAyGqch+YH2rCuJtSKTOZuDWuMloyApE2D8Y1quvv35zvjv7985qtd3z9/9xrfG+/v1yaY+/ftZACRTF9OVHRnv1+/GMXuadP3/AMzUQWDmvX4x1Irti/T7/cCpyVb4F++2RtVYHt/zJIRuH39ZAoFMm8ZFCCT4jBEa6n794wqyaCeTktIpF55cAAGtQ/fvrhqErSfff+5JlGhaP364EVRw3GSQqUiq5Mc2ERKENTnTdZDuznedVdp6vmfjI5EUtR9YzpEKxfT/AHERMdmn4iK8msbqIoBR4O55yX3zlBQS7xN4MkOAhIPbx/cgo03AFQ2Sm+nTihKjWudjgJqDgO8VTC+R0HgIx4BEJURGoeTw4xmCYEDfT7zjJlFBQbppl4xwA0EQni9IcdziZ70D9isCod9/TrBihc8/+M1ZkklvHUnXpUv9wJKywm6IPy4hJJgwtsY1ksUej7eUXm3CFhQnAjeQvoZM+zXjIr6VjFd/Aj2xaFK5IEd84FZBBPCf7GUeYaHbMn4nIwETZ5E4aQngmxbEE3jI+M5iEQ0BANs3rO6uB0X1FfrCRBnqDXGtzkLeaRBSMtAM8RP5y2d4VRxhKJMNajBkwez/AODMVGKZZNmoyeC4yyQKIY6FvkrGQSDcOxiJ0aZrIov0lqII6G9reRu/dA9y6+KFqYcNJKISiYmOdYqaUvoZ/wC/GIlWqq8uMpiboVDyyfEkPOR6RazOdXqL1gUxmkltjgZU4+nzTIIy4QT7Yg7unB4BCCBMNVhBsGhKKLOTVZOFiC0gFEdDjFUtAhOjqiT2MmSBAJWvv28QTRw3hIsmudz9/POMNr7cJ7+/fsYhI13jlmnXv9/8ySmij/ccItyLIw00edfT/uQgINxl346xEXSzA5eHR9/mXFKyyRqBBXg7wtiXTPGCAmeR3ziGQSJGdYl7+/fs5632/fvebv5dz9v+5CJ6ue/v/cmiB5N0P3/mIHILeZ1f6wgUFFScUbdZAOogUboA24sBuED5a47DWItdAZPrr0cjTZxuQ4X/ACsECRVElyrrFIqDGFbSlUB/LhoO3rD0XvvGYebLLgNAHRvE9u5Ws9R67cK1KqXkIEV/5gIKLUt5iZ/GE9yXQOanSxxkyipBMiW704Z8VYHkMH+YG31rCQ6ciWTNhNf/AAOwxOMgewxQ1F9Vle2sEIbSKbJtfgxKAyjDKecmMBTJIkjjHRaRkxwGT+8YjkJCiImZ71koDqqLgr3jBZiHXuYAFo1yKv7kqZKZ8Cf2Zr0d0wDH5cMge6xaUt3SAxHMTm1X+7xmNEksPFEVCEEKzGwun1xESVfWOe4xsLrmML3eb4/+HX/4p9MXGRaoZDZvn2ZK4uIIyfCiaXcoL0D5vCSkAcbVFCRywYiKbA7sjIlKLZ0uLKwiK2ioyCnniU0KLQmbg6m24ECWiDbon0G8DkoVqEFeTbzjGQIuoJdbk9sWKgxAmFBLDyqEe8bJ63yI9aj9hxFxLeZVZIXpuEAPRaifhZ7mCCG9D5Pvvlu74fX784qrzwu/v9xXpZ9/v9wG1iH4+/8AMaS1zKx9+mEqRATOrPvtlTQN4YNSJ98jok3gLcIOStDUZtCgl+sV7VZVKKYcmpeyagj/ANyY1oHl49sFDo/KbwSk5Ka+x/uVNXx9++c9Y9dz9v1yUD0XdP7174q2bVUzP/Mn18h/6+xg9g4RxmjQUCvAOPXEMJOAJ9/5kZhU2Pd/mSQ3LuwlWdmF+kFKUmJv0jJeK2j4wR4NZq8bVY4Sv/uCXKy3lg1eAGhcKd7fL3k1kV8E4/BfVXm8UBTygjGvOBQYCgS7GA9MG5kEtdXq84biGWCMDpPxidfGRz/8fOCQrE1pqsQuGRTNDH8wAxZCvoYrvFm4yQEIUvGHcVYJjbkhI3uMZAMMiYDDftrTAR4EKwBa4QjPbvII8HmNCT+8Z9JZnRUvzjxIQqNPj8GNuUbdTjGAlL8sLhCuCMfasIjkV4ALCCDiD0rjF331h7VMYiA09dsCQkj0woZzr7OT4nxg+a7wawav/wCHy9TgOkjuc//Z" alt="Spider-Man" class="hero-img">
  <div class="hero-overlay"></div>
  <div class="hero-grid"></div>
  <div class="hero-scan"></div>
  <div class="hero-corner tl"></div>
  <div class="hero-corner tr"></div>
  <div class="hero-corner bl"></div>
  <div class="hero-corner br"></div>
  <div class="hero-crosshair"></div>
  <div class="hero-content">
    <div class="hero-eyebrow">Intelligence · Lookup · System</div>
    <div class="hero-title">AMIR<br><span class="r">TRACER</span></div>
    <div class="hero-quote">With <em>great power</em> comes great responsibility</div>
  </div>
</div>

<!-- ── MAIN ── -->
<div class="wrapper">

  <!-- Header -->
  <header>
    <div class="logo">AMIR TRACER</div>
    <div class="tagline">Number · IP · Email · Username · Vehicle Intelligence</div>
    <div class="sys-badge"><span class="sys-dot"></span>All Systems Operational</div>
  </header>

  <!-- Stats bar -->
  <div class="stats-bar">
    <div class="stat-item">
      <div class="stat-label">Mode</div>
      <div class="stat-val" id="statMode" style="color:var(--red)">PHONE</div>
    </div>
    <div class="stat-item">
      <div class="stat-label">Queries</div>
      <div class="stat-val" id="statCount" style="color:var(--cyan)">0</div>
    </div>
    <div class="stat-item">
      <div class="stat-label">Status</div>
      <div class="stat-val" id="statStatus" style="color:var(--green)">IDLE</div>
    </div>
    <div class="stat-item">
      <div class="stat-label">Last</div>
      <div class="stat-val" id="statLast" style="color:var(--yellow);font-size:0.9rem">--:--</div>
    </div>
  </div>

  <!-- Mode tabs -->
  <div class="mode-tabs">
    <button class="tab-btn active" data-mode="phone" onclick="setMode('phone')">
      <span class="tab-icon">📞</span>
      Phone
    </button>
    <button class="tab-btn" data-mode="ip" onclick="setMode('ip')">
      <span class="tab-icon">🌐</span>
      IP Lookup
    </button>
    <button class="tab-btn" data-mode="email" onclick="setMode('email')">
      <span class="tab-icon">📧</span>
      Email Info
    </button>
    <button class="tab-btn" data-mode="username" onclick="setMode('username')">
      <span class="tab-icon">👤</span>
      Username
    </button>
    <button class="tab-btn" data-mode="vehicle" onclick="setMode('vehicle')">
      <span class="tab-icon">🚗</span>
      Vehicle
    </button>
  </div>

  <!-- Search box -->
  <div class="search-box" id="searchBox">
    <div class="input-meta">
      <div class="input-label" id="inputLabel">Target Number</div>
      <div class="input-desc" id="inputDesc">India: without +91</div>
    </div>
    <div class="input-row">
      <input type="text" id="mainInput" placeholder="9876543210" maxlength="100" />
      <button class="trace-btn" id="traceBtn" onclick="doTrace()">TRACE</button>
    </div>
    <div class="hint-row" id="hintRow">Enter number without country code e.g. 9876543210</div>
  </div>

  <!-- Status -->
  <div class="status" id="status">
    <div class="spinner"></div>
    <span id="statusText">Tracing...</span>
  </div>

  <!-- Error -->
  <div class="error-msg" id="errorMsg"></div>

  <!-- Pretty results -->
  <div class="pretty-results" id="prettyResults">
    <div class="result-card visible" style="margin-bottom:0">
      <div class="result-header">
        <div class="result-header-left">
          <span class="live-dot"></span>
          <span id="resultLabel">result.json</span>
        </div>
        <div style="display:flex;gap:8px;align-items:center;">
          <button class="copy-btn" id="copyFmtBtn" onclick="copyFormatted()" style="display:none">📋 Copy Text</button>
          <button class="copy-btn" id="copyJsonBtn" onclick="copyResult()">⬇ Copy JSON</button>
        </div>
      </div>
      <div class="result-grid" id="resultGrid"></div>
      <div class="raw-toggle" onclick="toggleRaw()"> &nbsp;View Raw JSON</div>
      <div class="raw-section" id="rawSection">
        <pre id="resultPre"></pre>
      </div>
    </div>
  </div>

  <!-- History -->
  <div class="history-section" id="historySection" style="display:none">
    <div class="history-title">Recent Lookups</div>
    <div class="history-list" id="historyList"></div>
  </div>

  <!-- Divider + watermark -->
  <div class="divider" style="margin-top:40px"></div>
  <div class="watermark">
    powered by <a href="https://instagram.com/amirplsstop" target="_blank">@amirplsstop</a>
    &nbsp;·&nbsp;
    <a href="https://instagram.com/chatpataprani" target="_blank">@chatpataprani</a>
  </div>

</div>

<script>
// ── CONFIG ──
const INSTAGRAM_ID = "amirplsstop";

// ── BLOCKED NUMBERS ──
const BLOCKED_NUMBERS = ["7546085732"];

function isBlockedNumber(num) {
  return BLOCKED_NUMBERS.includes(String(num).trim());
}

// ── RESTRICTED FILTER ──
const RESTRICTED_WORDS = [
  "@gauravcyber_op","@gaurav_cyber_op","api sell by","sell by","darzz","rose-x",
  "buy now","order now","purchase now","limited offer","limited time","exclusive deal","special offer",
  "discount","promo","coupon","subscribe","join now","sign up","click here",
  "free trial","free access","100% free","earn money","make money","passive income",
  "sponsored","advertisement","ad:","paid promotion","reseller","resell","contact us","dm us","dm for",
  "whatsapp us","whatsapp:","visit our","visit us","check out our",
  "follow us","follow our","follow @","t.me/","telegram.me/","youtube.com/","youtu.be/","instagram.com/",
];
const WHITELISTED = ["@chatpataprani","@amirplsstop"];

function containsRestricted(obj) {
  if(typeof obj==="string"){
    const low=obj.toLowerCase();
    for(const w of RESTRICTED_WORDS){
      if(low.includes(w)) { if(WHITELISTED.some(x=>low.includes(x.toLowerCase()))) continue; return true; }
    }
    return false;
  }
  if(Array.isArray(obj)) return obj.some(containsRestricted);
  if(obj&&typeof obj==="object") return Object.values(obj).some(containsRestricted);
  return false;
}

// Keys to strip from JSON output (branding/attribution)
const STRIP_KEYS = ["developed","developer","dev","credit","credits","poweredby","powered_by","powered by","api_by","apiby","buy","buy_link","buylink","ad","ads","banner","promo_link"];
const STRIP_VALUES = ["@lakhanpro","lakhanpro","@ab_devs","ab_devs","api powered by","powered by @"];

function sanitize(obj) {
  if(typeof obj==="string"){
    let s=obj;
    for(const w of RESTRICTED_WORDS) s=s.replaceAll(w,"");
    return s.trim();
  }
  if(Array.isArray(obj)) return obj.map(sanitize);
  if(obj&&typeof obj==="object"){
    const out={};
    for(const [k,v] of Object.entries(obj)){
      // Skip branding keys
      if(STRIP_KEYS.some(sk => k.toLowerCase().replace(/[_\\s]/g,"").includes(sk.replace(/[_\\s]/g,"")))) continue;
      // Skip branding values
      const vStr = typeof v === "string" ? v.toLowerCase() : "";
      if(STRIP_VALUES.some(sv => vStr.includes(sv.toLowerCase()))) continue;
      out[k]=sanitize(v);
    }
    return out;
  }
  return obj;
}

// ── MODE STATE ──
const MODES = {
  phone:    { label:"Target Number", desc:"India: without +91", hint:"Enter number without country code e.g. 9876543210", placeholder:"9876543210", color:"#e63946", rgb:"230,57,70", statLabel:"PHONE" },
  ip:       { label:"IP Address",    desc:"IPv4 or IPv6",       hint:"Leave blank to lookup your own public IP",           placeholder:"8.8.8.8 (blank = my IP)", color:"#60a5fa", rgb:"96,165,250", statLabel:"IP" },
  email:    { label:"Email Address", desc:"Validate & check",   hint:"Check deliverability, format, and domain info",      placeholder:"example@gmail.com", color:"#fbbf24", rgb:"251,191,36", statLabel:"EMAIL" },
  username: { label:"GitHub Username", desc:"Profile + public repos", hint:"Lookup any GitHub user's public profile",      placeholder:"torvalds", color:"#a78bfa", rgb:"167,139,250", statLabel:"USERNAME" },
  vehicle:  { label:"RC Number",     desc:"India registration no.", hint:"Enter RC without spaces e.g. MH12AB1234",        placeholder:"MH12AB1234", color:"#fb923c", rgb:"251,146,60", statLabel:"VEHICLE" },
};

let currentMode = "phone";
let queryCount = 0;
let lastResult = "";
let lastFormattedResult = "";
let history = [];

function setMode(mode) {
  currentMode = mode;
  const cfg = MODES[mode];

  // update tabs
  document.querySelectorAll(".tab-btn").forEach(b => b.classList.toggle("active", b.dataset.mode===mode));

  // update colors via CSS variables
  const box = document.getElementById("searchBox");
  box.style.setProperty("--active-color", cfg.color);
  box.style.setProperty("--active-rgb", cfg.rgb);
  document.documentElement.style.setProperty("--active-color", cfg.color);
  document.documentElement.style.setProperty("--active-rgb", cfg.rgb);

  document.getElementById("inputLabel").textContent = cfg.label;
  document.getElementById("inputDesc").textContent  = cfg.desc;
  document.getElementById("hintRow").textContent    = cfg.hint;
  document.getElementById("mainInput").placeholder  = cfg.placeholder;
  document.getElementById("statMode").textContent   = cfg.statLabel;
  document.getElementById("statMode").style.color   = cfg.color;
  document.querySelector(".spinner").style.borderTopColor = cfg.color;

  clearResults();
}

function clearResults() {
  document.getElementById("prettyResults").classList.remove("visible");
  document.getElementById("errorMsg").classList.remove("visible");
  const fmtBtn = document.getElementById("copyFmtBtn");
  if(fmtBtn) fmtBtn.style.display = "none";
  lastFormattedResult = "";
}

// ── FETCH HELPERS ──
async function fetchProxy(url) {
  const proxies = [
    u => u,  // direct first (works if CORS headers present)
    u => `https://corsproxy.io/?${encodeURIComponent(u)}`,
    u => `https://api.allorigins.win/raw?url=${encodeURIComponent(u)}`,
    u => `https://api.codetabs.com/v1/proxy?quest=${encodeURIComponent(u)}`,
    u => `https://thingproxy.freeboard.io/fetch/${u}`,
    u => `https://yacdn.org/proxy/${u}`,
  ];
  let lastErr = "";
  for(const proxy of proxies) {
    try {
      const res = await fetch(proxy(url), {
        signal: AbortSignal.timeout(12000),
        headers: { "Accept": "application/json" }
      });
      if(!res.ok) { lastErr = `HTTP ${res.status}`; continue; }
      const text = await res.text();
      // Reject HTML responses from proxies
      const trimmed = text.trim();
      if(trimmed.startsWith("<") || trimmed.startsWith("<!")) {
        lastErr = "Proxy returned HTML (blocked)";
        continue;
      }
      return JSON.parse(trimmed);
    } catch(e) { lastErr = e.message; continue; }
  }
  throw new Error("All proxies failed: " + lastErr);
}

function extractClean(data) {
  if(data&&typeof data==="object"&&!Array.isArray(data)){
    for(const key of Object.keys(data)){
      if(["result","data","response"].includes(key.toLowerCase())) return data[key];
    }
    for(const val of Object.values(data)){
      const found=extractClean(val);
      if(found!==null&&found!==undefined&&!(typeof found==="object"&&Object.keys(found).length===0)) return found;
    }
  }
  if(Array.isArray(data)){ for(const item of data){ const f=extractClean(item); if(f!==null&&f!==undefined) return f; } }
  return null;
}

// ── LOOKUP FUNCTIONS ──
async function lookupPhone(num) {
  if(isBlockedNumber(num)) throw new Error("🚫 This number cannot be searched.");
  const url = `https://har-har-mahadev-psi.vercel.app/api?key=FREE_ME_11_DAY&number=${num}`;
  const raw = await fetchProxy(url);
  if(containsRestricted(raw)) throw new Error("No valid data found");
  const cleaned = sanitize(raw);

  // Dig into nested result: support { result: { results: [...] } } or flat object
  let rec = cleaned;
  if(rec && typeof rec === "object") {
    if(rec.result) rec = rec.result;
    // Case-insensitive search for a "results" array key
    const resultsKey = Object.keys(rec).find(k => k.toLowerCase() === "results");
    if(resultsKey && Array.isArray(rec[resultsKey]) && rec[resultsKey].length > 0) rec = rec[resultsKey][0];
  }
  if(!rec || typeof rec !== "object") throw new Error("No data found");

  // Generic deep-search for a value by key aliases (case-insensitive)
  const pick = (obj, ...aliases) => {
    for(const alias of aliases) {
      for(const [k, v] of Object.entries(obj)) {
        if(k.toLowerCase() === alias.toLowerCase()) {
          if(v !== null && v !== undefined && String(v).trim() !== "" && String(v).toLowerCase() !== "null") {
            return String(v).trim();
          }
        }
      }
    }
    return "—";
  };

  // Clean address: replace ! separators with ", "
  const rawAddr = pick(rec, "ADDRESS", "address", "addr", "location");
  const address = rawAddr !== "—" ? rawAddr.replace(/!/g, ", ").replace(/,\\s*,/g, ",").trim() : "—";

  const name      = pick(rec, "NAME", "name", "ownername", "owner", "subscribername");
  const father    = pick(rec, "fname", "fathername", "father", "fathersname");
  const circle    = pick(rec, "circle", "Circle", "state", "region", "zone");
  const mobile    = pick(rec, "MOBILE", "mobile", "mobilenumber", "phone", "number") !== "—"
                      ? pick(rec, "MOBILE", "mobile", "mobilenumber", "phone", "number")
                      : num;
  const alternate = pick(rec, "alt", "alternate", "alternatenumber", "altnumber", "altphone");
  const email     = pick(rec, "email", "emailid", "mail");
  const idnum     = pick(rec, "id", "idnumber", "simid", "uid", "docid");

  const fields = [
    { label:"Name",             val: name,      highlight: name !== "—" },
    { label:"Father's Name",    val: father },
    { label:"Address",          val: address,   full: true },
    { label:"Circle",           val: circle },
    { label:"Mobile Number",    val: mobile,    highlight: true },
    { label:"Alternate Number", val: alternate },
    { label:"Email",            val: email },
    { label:"ID Number",        val: idnum },
  ];

  const final = { success:true, input:num, mode:"phone", instagram:INSTAGRAM_ID, result:cleaned };
  return { final, fields, label:`phone_${num}.json`, searchedNum: num };
}

async function lookupIP(ip) {
  const url = ip.trim()
    ? `https://ipapi.co/${encodeURIComponent(ip.trim())}/json/`
    : `https://ipapi.co/json/`;
  const data = await fetchProxy(url);
  if(data.error) throw new Error(data.reason||"IP lookup failed");
  const final = { success:true, input:ip||"my-ip", mode:"ip", result:data };
  const fields = [
    { label:"IP Address",   val: data.ip,             highlight:true },
    { label:"City",         val: data.city||"—" },
    { label:"Region",       val: data.region||"—" },
    { label:"Country",      val: `${data.country_name||"—"} (${data.country_code||""})` },
    { label:"Postal",       val: data.postal||"—" },
    { label:"Timezone",     val: data.timezone||"—" },
    { label:"Latitude",     val: data.latitude||"—" },
    { label:"Longitude",    val: data.longitude||"—" },
    { label:"ISP / Org",    val: data.org||"—",       full:true },
    { label:"Currency",     val: data.currency_name ? `${data.currency_name} (${data.currency})` : "—" },
    { label:"Calling Code", val: data.country_calling_code||"—" },
    { label:"Languages",    val: data.languages||"—", full:true },
  ];
  return { final, fields, label:`ip_${data.ip}.json` };
}

async function lookupEmail(email) {
  // Using abstract API free email validation
  const url = `https://emailvalidation.abstractapi.com/v1/?api_key=free&email=${encodeURIComponent(email)}`;
  // Fallback: use mailboxlayer-style free endpoint
  // Actually use a public free validator
  const url2 = `https://api.verifalia.com/v2.4/email-validations`;
  // Let's use disify (free, no key needed)
  const disifyUrl = `https://www.disify.com/api/email/${encodeURIComponent(email)}`;
  let data;
  try {
    data = await fetchProxy(disifyUrl);
  } catch(e) {
    throw new Error("Email check failed: "+e.message);
  }
  // Also do DNS info
  const domain = email.split("@")[1]||"";
  const fmt = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email);
  const final = { success:true, input:email, mode:"email", result:{ format_valid:fmt, domain, ...data } };
  const fields = [
    { label:"Email",        val: email,                   highlight:true },
    { label:"Format Valid", val: fmt ? "✓ Valid" : "✗ Invalid", highlight:true },
    { label:"Domain",       val: domain },
    { label:"Disposable",   val: data.disposable?"⚠ Yes":"✓ No" },
    { label:"DNS Valid",    val: data.dns?"✓ Yes":"✗ No" },
    { label:"Format Score", val: fmt?"100%":"0%" },
  ];
  return { final, fields, label:`email_${domain}.json` };
}

async function lookupUsername(username) {
  const url = `https://api.github.com/users/${encodeURIComponent(username)}`;
  let data;
  try {
    const res = await fetch(url, { signal: AbortSignal.timeout(8000) });
    if(!res.ok) throw new Error("User not found (HTTP "+res.status+")");
    data = await res.json();
  } catch(e) { throw new Error("GitHub lookup failed: "+e.message); }
  const final = { success:true, input:username, mode:"github", result:data };
  const fields = [
    { label:"Username",     val: data.login,                  highlight:true },
    { label:"Display Name", val: data.name||"—" },
    { label:"Bio",          val: data.bio||"—",               full:true },
    { label:"Location",     val: data.location||"—" },
    { label:"Company",      val: data.company||"—" },
    { label:"Blog / URL",   val: data.blog||"—",              full:true },
    { label:"Public Repos", val: String(data.public_repos||0) },
    { label:"Followers",    val: String(data.followers||0) },
    { label:"Following",    val: String(data.following||0) },
    { label:"Created",      val: data.created_at ? new Date(data.created_at).toLocaleDateString() : "—" },
    { label:"GitHub ID",    val: String(data.id||"—") },
    { label:"Profile URL",  val: data.html_url||"—",          full:true },
  ];
  return { final, fields, label:`github_${username}.json` };
}

// ── VEHICLE LOOKUP ──
function vBool(v)  { return v === true ? "✓ Yes" : v === false ? "✗ No" : "—"; }
function vStr(v)   { const s = String(v ?? "").trim(); return s === "" || s === "null" || s === "undefined" ? "—" : s; }
function vNum(v, suffix="") { return (v !== null && v !== undefined && v !== 0 && v !== "") ? String(v) + suffix : "—"; }

async function lookupVehicle(rc) {
  const clean = rc.trim().toUpperCase().replace(/[\\s\\-]/g,"");
  if(!clean) throw new Error("Enter a valid RC number");
  const apiUrl = `/api/vehicle?rc=${encodeURIComponent(clean)}`;

  let raw = null;
  let lastErr = "";
  try {
    const res = await fetch(apiUrl, { signal: AbortSignal.timeout(14000) });
    if(!res.ok) throw new Error("HTTP " + res.status);
    const text = await res.text();
    const trimmed = text.trim();
    if(trimmed.startsWith("<")) throw new Error("HTML response");
    raw = JSON.parse(trimmed);
  } catch(e) { lastErr = e.message; }
  if(!raw) throw new Error("Could not reach vehicle API. (" + lastErr + ")");
  if(raw.success === false) throw new Error("No data found for RC: " + clean);

  const fd  = raw.full_data || {};
  const r   = fd.registrationResult || raw.registrationResult || raw;
  const pr  = fd.premiumRequest || {};
  const mp  = pr.motorPremiumRequest || {};
  const vr  = fd.validateRegistrationResult || {};
  const co  = mp.comprehensive || {};
  const tp  = mp.tp || {};

  if(!r || !r.registrationNo) throw new Error("Invalid response — RC not found");

  // Helper: mismatch fields
  const mismatches = Array.isArray(vr.mismatchFields)
    ? vr.mismatchFields.map(m => `${m.fieldName}: got ${m.userValue}, RTO says ${m.rtoValue}`).join("; ")
    : "—";

  const fields = [
    // ── Owner ──
    { label:"Owner First Name",           val: vStr(r.ownerFirstName),                          highlight: r.ownerFirstName },
    { label:"Owner Last Name",            val: vStr(r.ownerLastName),                           highlight: r.ownerLastName },
    { label:"Mobile Number",              val: vStr(raw.mobile_number),                         highlight: raw.mobile_number && raw.mobile_number !== "Not Found" },
    // ── Registration ──
    { label:"Registration Number",        val: vStr(r.registrationNo),                          highlight: true },
    { label:"Registration Date",          val: vStr(r.registrationDate) },
    { label:"Registration Status",        val: vStr(r.status) },
    // ── Vehicle ──
    { label:"Vehicle Make",               val: vStr(r.make) },
    { label:"Vehicle Model",              val: vStr(r.model) },
    { label:"Vehicle ID",                 val: vStr(r.vehicleId) },
    { label:"Fuel Type",                  val: vStr(r.fuel) },
    { label:"Vehicle Class",              val: vStr(r.cvVehicleClass) },
    { label:"Vehicle Category",           val: vStr(r.vertical) },
    { label:"Body Type",                  val: vStr(r.bodyType) },
    { label:"Seating Capacity",           val: vNum(r.seatingCapacity, " seats") },
    { label:"Carrying Capacity",          val: vNum(r.carryingCapacity, " persons") },
    { label:"Gross Weight",               val: vNum(r.grossWeight, " kg") },
    { label:"Cubic Capacity",             val: r.cubicCapacity ? vNum(r.cubicCapacity, " cc") : "N/A (EV)" },
    { label:"Engine Number",              val: vStr(r.engineno) },
    { label:"Chassis Number",             val: vStr(r.chasisno) },
    { label:"Manufacturing Year",         val: vStr(r.year) },
    // ── RTO ──
    { label:"RTO Code",                   val: vStr(r.rto?.rtoCode) },
    { label:"RTO Plate",                  val: vStr(r.rto?.rtoPlate) },
    { label:"RTO Location",               val: vStr(r.rto?.lntLoc) },
    { label:"Registration State",         val: vStr(r.reg1) },
    // ── Address ──
    { label:"Permanent Address",          val: vStr(r.permanentAddress),  full: true },
    { label:"Correspondence Address",     val: vStr(r.corrAddress),       full: true },
    // ── Finance / Insurance ──
    { label:"Financer Name",              val: vStr(r.financierName) },
    { label:"Previous Policy Number",     val: vStr(r.prePolicyNo || mp.previousPolicyNumber) },
    { label:"Insurance Expiry Status",    val: mp.expiryFlag !== undefined ? vBool(mp.expiryFlag) : "—" },
    { label:"Previous Claim Status",      val: r.previousClaim !== undefined ? vBool(r.previousClaim) : "—" },
    // ── NCB ──
    { label:"NCB Eligibility",            val: mp.eligibleForNCB !== undefined ? vBool(mp.eligibleForNCB) : "—" },
    { label:"Previous NCB",               val: mp.prevNCB !== undefined ? String(mp.prevNCB) + "%" : "—" },
    { label:"Applicable NCB",             val: mp.applicableNCB !== undefined ? String(mp.applicableNCB) + "%" : "—" },
    // ── Policy / Customer ──
    { label:"Policy Type",                val: mp.businessType !== undefined ? (mp.businessType === 0 ? "New" : "Renewal") : "—" },
    { label:"Purchase Policy Status",     val: mp.purchasePolicy !== undefined ? vBool(mp.purchasePolicy) : "—" },
    { label:"Customer Name",              val: vStr(pr.customerName) },
    { label:"Individual / Commercial",    val: mp.isIndividual !== undefined ? (mp.isIndividual ? "Individual" : "Commercial") : "—" },
    { label:"Registered Owner Match",     val: mp.isRegisteredOwnerDifferent !== undefined ? vBool(!mp.isRegisteredOwnerDifferent) : "—" },
    { label:"Async Processing",           val: pr.isAsync !== undefined ? vBool(pr.isAsync) : "—" },
    { label:"Renewal Status",             val: fd.renewal !== undefined ? vBool(fd.renewal) : "—" },
    { label:"Result Page Visited",        val: pr.resultPageVisited !== undefined ? vBool(pr.resultPageVisited) : "—" },
    // ── Validation ──
    { label:"Vehicle Validation Status",  val: vStr(vr.status) },
    { label:"Mismatch Field Detection",   val: mismatches, full: mismatches !== "—" },
    { label:"Claim History",              val: r.previousClaim !== undefined ? vBool(r.previousClaim) : "—" },
    // ── Add-on Covers (from comprehensive) ──
    { label:"Zero Dep",                   val: co.zeroDep    !== undefined ? vBool(co.zeroDep)    : vBool(tp.zeroDep) },
    { label:"RSA Cover",                  val: co.rsa        !== undefined ? vBool(co.rsa)        : vBool(tp.rsa) },
    { label:"Engine Protect",             val: co.engineProtect !== undefined ? vBool(co.engineProtect) : "—" },
    { label:"NCB Protect",                val: co.ncbProtect !== undefined ? vBool(co.ncbProtect) : "—" },
    { label:"Anti Theft",                 val: co.antiTheft  !== undefined ? vBool(co.antiTheft)  : "—" },
    { label:"Tyre Secure",                val: co.tyreSecure !== undefined ? vBool(co.tyreSecure) : "—" },
    { label:"Key Replacement",            val: co.keyReplacement !== undefined ? vBool(co.keyReplacement) : "—" },
    { label:"Consumable Cover",           val: co.consumableCover !== undefined ? vBool(co.consumableCover) : "—" },
    { label:"Full Invoice Cover",         val: co.fullInvoiceCover !== undefined ? vBool(co.fullInvoiceCover) : "—" },
    { label:"Personal Baggage",           val: co.personalBaggage !== undefined ? vBool(co.personalBaggage) : "—" },
    { label:"Daily Cash Allowance",       val: co.dailyCashAllowance !== undefined ? vBool(co.dailyCashAllowance) : "—" },
    { label:"Hydrostatic Lock Cover",     val: co.hydrostaticLockCover !== undefined ? vBool(co.hydrostaticLockCover) : "—" },
    { label:"Battery & Charger Protect",  val: co.batteryAndChargerProtect !== undefined ? vBool(co.batteryAndChargerProtect) : "—" },
    { label:"Rodent Cover",               val: co.rodentCover !== undefined ? vBool(co.rodentCover) : "—" },
    { label:"Geographic Extension",       val: co.geographicExt !== undefined ? vBool(co.geographicExt) : "—" },
    { label:"Emergency Hotel Expense",    val: co.emergencyTransportAndHotelExpense !== undefined ? vBool(co.emergencyTransportAndHotelExpense) : "—" },
    { label:"Repair Cover",               val: co.repairOfGlassRubberPlasticParts !== undefined ? vBool(co.repairOfGlassRubberPlasticParts) : "—" },
    { label:"TPPD",                       val: co.tppd !== undefined ? vBool(co.tppd) : "—" },
    { label:"IMT23",                      val: co.imt23 !== undefined ? vBool(co.imt23) : "—" },
    { label:"IMT34",                      val: co.imt34 !== undefined ? vBool(co.imt34) : "—" },
    { label:"IMT47",                      val: co.imt47 !== undefined ? vBool(co.imt47) : "—" },
  ];

  const final = { success: true, input: clean, mode: "vehicle", result: { registrationResult: r } };
  return { final, fields, label: `vehicle_${clean}.json`, vehicleData: { r, mp, co, tp, vr, pr, fd } };
}

function buildVehicleFormattedText(d) {
  const r = d.r, mp = d.mp, co = d.co;
  return [
    "╔══════════════════════════╗",
    "🚗   VEHICLE RC LOOKUP",
    "╚══════════════════════════╝",
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━",
    `👤 Owner First  : ${vStr(r.ownerFirstName)}`,
    `👤 Owner Last   : ${vStr(r.ownerLastName)}`,
    `🔢 RC Number    : ${vStr(r.registrationNo)}`,
    `📅 Reg. Date    : ${vStr(r.registrationDate)}`,
    `🚙 Make         : ${vStr(r.make)}`,
    `🚘 Model        : ${vStr(r.model)}`,
    `⛽ Fuel         : ${vStr(r.fuel)}`,
    `🏷️  Body Type    : ${vStr(r.bodyType)}`,
    `🏷️  Class        : ${vStr(r.cvVehicleClass)}`,
    `📅 Mfg. Year    : ${vStr(r.year)}`,
    `🏢 RTO          : ${vStr(r.rto?.rtoPlate)} — ${vStr(r.rto?.lntLoc)}`,
    `🔩 Chassis      : ${vStr(r.chasisno)}`,
    `⚙️  Engine       : ${vStr(r.engineno)}`,
    `💺 Seating      : ${vNum(r.seatingCapacity, " seats")}`,
    `⚖️  Gross Wt.    : ${vNum(r.grossWeight, " kg")}`,
    `🏦 Financier    : ${vStr(r.financierName)}`,
    `📄 Prev. Policy : ${vStr(r.prePolicyNo)}`,
    `⚠️  Prev. Claim  : ${vBool(r.previousClaim)}`,
    `💚 NCB Eligible : ${mp.eligibleForNCB !== undefined ? vBool(mp.eligibleForNCB) : "—"}`,
    `🔋 Zero Dep     : ${vBool(co.zeroDep)}`,
    `🔧 Engine Prot. : ${vBool(co.engineProtect)}`,
    `📍 Address      : ${vStr(r.permanentAddress)}`,
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━",
  ].join("\\n");
}

function buildFieldsFromObject(obj, prefix="") {
  if(typeof obj !== "object" || obj===null) return [];
  return Object.entries(obj).slice(0,12).map(([k,v]) => {
    const label = k.replace(/_/g," ").replace(/\\w/g, c=>c.toUpperCase());
    const val = typeof v === "object" ? JSON.stringify(v) : String(v||"—");
    return { label, val, full: val.length > 30 };
  });
}

// ── RENDER ──
function renderFields(fields) {
  const grid = document.getElementById("resultGrid");
  grid.innerHTML = "";
  fields.forEach(f => {
    const div = document.createElement("div");
    div.className = "result-field" + (f.full?" result-full-row":"");
    div.innerHTML = `<div class="field-label">${f.label}</div><div class="field-val${f.highlight?" highlight":""}">${escHtml(f.val)}</div>`;
    grid.appendChild(div);
  });
}

function escHtml(s) {
  return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
}

function syntaxHighlight(json) {
  return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\\s*:)?|(true|false|null)|-?\\d+(?:\\.\\d*)?(?:[eE][+\\-]?\\d+)?)/g, match => {
    if(/^"/.test(match)) { if(/:$/.test(match)) return `<span class="key">${match}</span>`; return `<span class="string">${match}</span>`; }
    if(/true|false/.test(match)) return `<span class="bool">${match}</span>`;
    if(/null/.test(match)) return `<span class="null">${match}</span>`;
    return `<span class="number">${match}</span>`;
  });
}

// ── MAIN TRACE ──
async function doTrace() {
  const input = document.getElementById("mainInput").value.trim();
  if(currentMode!=="ip" && !input) return;

  const btn     = document.getElementById("traceBtn");
  const status  = document.getElementById("status");
  const errMsg  = document.getElementById("errorMsg");
  const pretty  = document.getElementById("prettyResults");
  const statEl  = document.getElementById("statStatus");
  const lastEl  = document.getElementById("statLast");
  const statTxt = document.getElementById("statusText");

  btn.disabled = true;
  status.classList.add("active");
  statTxt.textContent = "Tracing...";
  errMsg.classList.remove("visible");
  pretty.classList.remove("visible");
  statEl.textContent = "TRACING";
  statEl.style.color = "var(--yellow)";

  try {
    let res;
    if(currentMode==="phone")    res = await lookupPhone(input);
    else if(currentMode==="ip")  res = await lookupIP(input);
    else if(currentMode==="email") res = await lookupEmail(input);
    else if(currentMode==="username") res = await lookupUsername(input);
    else if(currentMode==="vehicle")  res = await lookupVehicle(input);

    lastResult = JSON.stringify(res.final, null, 2);
    if(currentMode === "phone" && res.searchedNum) {
      lastFormattedResult = buildPhoneFormattedText(res.fields, res.searchedNum);
    } else if(currentMode === "vehicle" && res.vehicleData) {
      lastFormattedResult = buildVehicleFormattedText(res.vehicleData);
    } else {
      lastFormattedResult = "";
    }
    const fmtBtn = document.getElementById("copyFmtBtn");
    if(fmtBtn) fmtBtn.style.display = lastFormattedResult ? "inline-flex" : "none";
    document.getElementById("resultLabel").textContent = res.label;
    document.getElementById("resultPre").innerHTML = syntaxHighlight(lastResult);
    renderFields(res.fields);
    document.getElementById("rawSection").classList.remove("open");

    // Update active color on result card
    document.querySelectorAll(".result-card").forEach(c => c.style.setProperty("--active-color", MODES[currentMode].color));
    document.querySelector(".live-dot").style.background = MODES[currentMode].color;
    document.querySelector(".live-dot").style.boxShadow = `0 0 8px ${MODES[currentMode].color}`;

    pretty.classList.add("visible");

    // stats
    queryCount++;
    document.getElementById("statCount").textContent = queryCount;
    statEl.textContent = "SUCCESS";
    statEl.style.color = "var(--green)";
    const now = new Date();
    lastEl.textContent = now.getHours().toString().padStart(2,"0")+":"+now.getMinutes().toString().padStart(2,"0");

    // history
    addHistory(input||"my-ip", currentMode, res.label);

  } catch(e) {
    const msg = e.message || "Unknown error";
    errMsg.textContent = msg;
    errMsg.classList.add("visible");
    statEl.textContent = "FAILED";
    statEl.style.color = "var(--red)";
  } finally {
    btn.disabled = false;
    status.classList.remove("active");
  }
}

// ── HISTORY ──
function addHistory(query, mode, label) {
  const cfg = MODES[mode];
  const item = { query, mode, label, time: new Date().toLocaleTimeString([], {hour:"2-digit",minute:"2-digit"}) };
  history.unshift(item);
  if(history.length > 5) history.pop();
  renderHistory();
}

function renderHistory() {
  const sec  = document.getElementById("historySection");
  const list = document.getElementById("historyList");
  if(history.length===0) { sec.style.display="none"; return; }
  sec.style.display="block";
  list.innerHTML = history.map((h,i) => {
    const cfg = MODES[h.mode];
    return `<div class="history-item" onclick="replayHistory(${i})">
      <div class="history-left">
        <span class="history-mode-badge" style="background:${cfg.color}22;color:${cfg.color};border:1px solid ${cfg.color}44">${cfg.statLabel}</span>
        <span class="history-query">${escHtml(h.query||"my-ip")}</span>
      </div>
      <span class="history-time">${h.time}</span>
    </div>`;
  }).join("");
}

function replayHistory(i) {
  const h = history[i];
  setMode(h.mode);
  document.getElementById("mainInput").value = h.query==="my-ip"?"":h.query;
  doTrace();
}

// ── UI HELPERS ──
function toggleRaw() {
  document.getElementById("rawSection").classList.toggle("open");
}

function copyFormatted() {
  if(!lastFormattedResult) return;
  navigator.clipboard.writeText(lastFormattedResult).then(() => {
    const btn = document.getElementById("copyFmtBtn");
    const prev = btn.innerHTML;
    btn.innerHTML = "✓ COPIED!";
    btn.style.color = "var(--green)";
    setTimeout(() => { btn.innerHTML = prev; btn.style.color = ""; }, 1500);
  });
}
function copyResult() {
  if(!lastResult) return;
  let textToCopy = lastResult;
  if(currentMode === "phone" && lastFormattedResult) {
    textToCopy = lastFormattedResult;
  }
  navigator.clipboard.writeText(textToCopy).then(() => {
    const btn = document.getElementById("copyJsonBtn");
    const prev = btn.innerHTML;
    btn.innerHTML = "✓ COPIED";
    btn.style.color = "var(--green)";
    setTimeout(() => { btn.innerHTML = prev; btn.style.color = ""; }, 1500);
  });
}

function buildPhoneFormattedText(fields, searchedNum) {
  const get = (label) => {
    const f = fields.find(f => f.label && f.label.toLowerCase().includes(label.toLowerCase()));
    return f ? f.val : "—";
  };
  const name       = get("name") !== "—" ? get("name") : (get("owner") !== "—" ? get("owner") : "—");
  const father     = get("father") !== "—" ? get("father") : (get("father's") !== "—" ? get("father's") : "—");
  const address    = get("address") !== "—" ? get("address") : (get("addr") !== "—" ? get("addr") : "—");
  const circle     = get("circle") !== "—" ? get("circle") : (get("state") !== "—" ? get("state") : (get("region") !== "—" ? get("region") : "—"));
  const mobile     = get("mobile") !== "—" ? get("mobile") : (get("phone") !== "—" ? get("phone") : (searchedNum || "—"));
  const alternate  = get("alternate") !== "—" ? get("alternate") : (get("alt") !== "—" ? get("alt") : "—");
  const email      = get("email") !== "—" ? get("email") : "—";
  const idnum      = get("id") !== "—" ? get("id") : (get("sim") !== "—" ? get("sim") : "—");

  return `╔════════════════════╗\\n📱 NUMBER LOOKUP 📱\\n╚════════════════════╝\\n📋 Details\\n━━━━━━━━━━━━━━━━━━\\n👤 Name: ${name}\\n👨 Father's Name: ${father}\\n🏠 Address: ${address}\\n📡 Circle: ${circle}\\n📱 Mobile Number: ${mobile}\\n🔄 Alternate Number: ${alternate}\\n📧 Email: ${email}\\n🆔 ID Number: ${idnum}\\n━━━━━━━━━━━━━━━━━━\\n🔍 Searched Number: ${searchedNum || "—"}`;
}

// ── ENTER KEY ──
document.getElementById("mainInput").addEventListener("keydown", e => {
  if(e.key==="Enter") doTrace();
});

// ── INIT ──
setMode("phone");
</script>
</body>
</html>"""

class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(f"[{self.address_string()}] {fmt % args}")

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == "/api/vehicle":
            self._vehicle_proxy(parsed.query)
        elif parsed.path in ("/", "/index.html", ""):
            self._serve_html()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")

    def _serve_html(self):
        data = HTML.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _vehicle_proxy(self, query):
        params = urllib.parse.parse_qs(query)
        rc = params.get("rc", [""])[0].strip().upper().replace("-", "").replace(" ", "")
        if not rc:
            self._json_error(400, "Missing rc parameter")
            return

        api_url = f"https://hum-garib-hai.xo.je/api.php?rc={urllib.parse.quote(rc)}"
        req = urllib.request.Request(api_url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-IN,en;q=0.9,hi;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://hum-garib-hai.xo.je/",
            "Origin": "https://hum-garib-hai.xo.je",
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "Connection": "keep-alive",
        })

        import ssl
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        try:
            with urllib.request.urlopen(req, timeout=20, context=ctx) as resp:
                body = resp.read()
            # Validate JSON
            json.loads(body)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)
        except urllib.error.HTTPError as e:
            # Read error body for debugging
            try:
                err_body = e.read().decode("utf-8", errors="ignore")[:500]
            except:
                err_body = ""
            self._json_error(502, f"API HTTP {e.code}: {err_body}")
        except Exception as e:
            self._json_error(500, str(e))

    def _json_error(self, code, msg):
        data = json.dumps({"error": msg}).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

if __name__ == "__main__":
    server = http.server.HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"Amir Tracer running on port {PORT}")
    print(f"Open: http://YOUR-VPS-IP:{PORT}")
    server.serve_forever()

"""
Generate 10 FRAME-FILLING realistic project images at 1400x460px.
No outer padding — image fills edge-to-edge in the 460px tall project visual slot.
"""

from PIL import Image, ImageDraw, ImageFont
import os, math, random

OUT = "assets"
W, H = 1400, 460

def fnt(size=11, bold=False):
    try:
        name = "arialbd.ttf" if bold else "arial.ttf"
        return ImageFont.truetype(name, size)
    except:
        try:
            return ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf", size)
        except:
            return ImageFont.load_default()

def mono(size=11):
    for f in ["consola.ttf","cour.ttf","lucon.ttf"]:
        try: return ImageFont.truetype(f, size)
        except: pass
    try: return ImageFont.truetype("C:/Windows/Fonts/consola.ttf", size)
    except: return ImageFont.load_default()

def rect(d, box, fill=None, outline=None, radius=0):
    if radius:
        d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline)
    else:
        d.rectangle(box, fill=fill, outline=outline)

def badge(d, x, y, text, bg, fg, fnt_):
    tw = d.textlength(text, font=fnt_)
    rect(d, [x, y, x+tw+16, y+20], fill=bg, radius=4)
    d.text((x+8, y+3), text, fill=fg, font=fnt_)
    return x + tw + 24

# ─────────────────────────────────────────────
# 1) HOME SOC LAB — Splunk-style SIEM
# ─────────────────────────────────────────────
def proj_soc_lab():
    img = Image.new("RGB", (W, H), "#080d16")
    d = ImageDraw.Draw(img)

    # Top nav bar
    rect(d, [0,0,W,42], fill="#0b1120")
    d.line([0,42,W,42], fill="#1e2d45", width=1)
    d.text((18,12), "● SPLUNK ENTERPRISE  |  Home SOC Lab — Threat Operations", fill="#5c7fa8", font=fnt(11))
    d.text((W-120,12), "admin@soc-lab", fill="#3d5a7a", font=fnt(10))

    # Sidebar
    rect(d, [0,42,190,H], fill="#090e1b")
    d.line([190,42,190,H], fill="#152033", width=1)
    for i,(label,col) in enumerate([("⌂  Overview","#64f5ff"),("⚡  Alerts","#4a6fa8"),
                                      ("🔍  Search","#4a6fa8"),("📊  Dashboards","#4a6fa8"),
                                      ("🛡  MITRE ATT&CK","#4a6fa8"),("📁  Reports","#4a6fa8"),
                                      ("⚙  Settings","#4a6fa8")]):
        y = 68 + i*38
        if i == 0:
            rect(d, [4, y-6, 186, y+22], fill="#0f2040", radius=6)
            d.rectangle([0, y-6, 3, y+22], fill="#64f5ff")
        d.text((18, y), label, fill=col, font=fnt(11,bold=(i==0)))

    # Main area header
    rect(d, [190,42,W,90], fill="#070c18")
    d.text((208,55), "SECURITY OPERATIONS CENTER  •  LIVE MONITORING", fill="#3d5a7a", font=fnt(10))
    d.text((208,67), "Event Log Analysis Dashboard", fill="#d0dff2", font=fnt(14,bold=True))

    # 4 stat cards
    for i,(val,lbl,col) in enumerate([("1,247","Events/Min","#64f5ff"),
                                        ("38","Critical Alerts","#ff6b6b"),
                                        ("12","Active Cases","#f5a623"),
                                        ("99.2%","Detection Rate","#5af08a")]):
        x = 208 + i*300; y2 = 98
        rect(d, [x, y2, x+282, y2+70], fill="#0a1428", radius=8, outline="#172540")
        d.text((x+16, y2+10), val, fill=col, font=fnt(28,bold=True))
        d.text((x+16, y2+44), lbl, fill="#5c7a9e", font=fnt(10))
        d.line([x+16, y2+60, x+266, y2+60], fill=col+"44", width=2)

    # Alert table
    rect(d, [208,178,W-14,H-14], fill="#08111e", radius=8, outline="#152033")
    d.text((224,190), "RECENT ALERTS", fill="#3d5a7a", font=fnt(9))
    cols = [224,340,510,700,920,1100]
    headers = ["TIME","SEVERITY","SOURCE IP","EVENT TYPE","RULE","STATUS"]
    for j,(hx,ht) in enumerate(zip(cols,headers)):
        d.text((hx, 208), ht, fill="#2d4d6e", font=fnt(9))
    d.line([208, 223, W-14, 223], fill="#112030", width=1)

    rows = [
        ("03:04:11","CRITICAL","192.168.1.105","Lateral Movement","T1021.002","🔴 OPEN"),
        ("03:03:47","HIGH","10.0.0.88","Priv Escalation","T1068","🟡 INVEST."),
        ("03:02:33","HIGH","172.16.0.14","PowerShell Exec","T1059.001","🔴 OPEN"),
        ("03:01:22","MED","192.168.1.201","DNS Exfil Attempt","T1071.004","🟢 CLOSED"),
        ("03:00:58","LOW","10.0.0.45","Port Scan Detected","T1046","🟢 CLOSED"),
    ]
    sev_col = {"CRITICAL":"#ff4455","HIGH":"#f5a623","MED":"#f0e060","LOW":"#5af08a"}
    for ri, row in enumerate(rows):
        y3 = 232 + ri*38
        rc = "#091523" if ri%2==0 else "#07101c"
        rect(d, [208, y3-4, W-14, y3+26], fill=rc)
        for j,(cx,cv) in enumerate(zip(cols, row)):
            col_t = sev_col.get(cv, "#8ba5c8") if j==1 else ("#64f5ff" if j==5 else "#8ba5c8")
            d.text((cx, y3+3), cv, fill=col_t, font=mono(10))
        d.line([208, y3+30, W-14, y3+30], fill="#0e1e30", width=1)

    img.save(f"{OUT}/proj_soc_lab.jpg", quality=97)
    print("1. proj_soc_lab.jpg ✓")

# ─────────────────────────────────────────────
# 2) PHISHING EMAIL IOC TRIAGE
# ─────────────────────────────────────────────
def proj_phishing_ioc():
    img = Image.new("RGB", (W, H), "#06080f")
    d = ImageDraw.Draw(img)

    # Left panel – Email viewer
    rect(d, [0,0,620,H], fill="#07090e")
    rect(d, [0,0,W,42], fill="#0a0d14")
    d.line([0,42,W,42], fill="#1a2030", width=1)
    d.text((18,12), "📧  PhishLens — Email IOC Triage Engine  v2.4.1", fill="#4a6080", font=fnt(11))

    # Email card
    rect(d, [14,54,606,260], fill="#0b0f1a", radius=8, outline="#1e2a3a")
    d.text((28,66), "FROM:", fill="#3d5060", font=fnt(9))
    d.text((80,66), "accounts-secure@paypa1-verify.xyz", fill="#ff6060", font=mono(10))
    badge(d, 80, 62, "SPOOFED", "#3d0a0a", "#ff8080", fnt(8))
    d.text((28,88), "TO:", fill="#3d5060", font=fnt(9))
    d.text((80,88), "user@company.com", fill="#8ba5c8", font=mono(10))
    d.text((28,110), "SUBJ:", fill="#3d5060", font=fnt(9))
    d.text((80,110), "⚠ Urgent: Verify your account immediately", fill="#f5c842", font=fnt(11,bold=True))
    d.line([28,128,596,128], fill="#141d2a", width=1)
    d.text((28,137), "SPF:", fill="#3d5060", font=fnt(9))
    d.text((80,137), "FAIL  ✗", fill="#ff4455", font=mono(10))
    d.text((28,153), "DKIM:", fill="#3d5060", font=fnt(9))
    d.text((80,153), "FAIL  ✗", fill="#ff4455", font=mono(10))
    d.text((28,169), "DMARC:", fill="#3d5060", font=fnt(9))
    d.text((90,169), "FAIL  ✗", fill="#ff4455", font=mono(10))

    # Body preview
    rect(d, [14,268,606,H-14], fill="#060810", radius=8, outline="#141e2c")
    d.text((28,280), "EMAIL BODY PREVIEW (SANITIZED)", fill="#2a4060", font=fnt(9))
    body = [
        "Dear Customer, Your account has been temporarily",
        "suspended. Click below to restore access within 24h.",
        "",
        "[LOGIN.BUTTON] → hxxp://paypa1-verify.xyz/login?id=XA9",
        "",
        "This link expires in: 00:24:13",
    ]
    for bi, bl in enumerate(body):
        col = "#ff8888" if "hxxp" in bl else "#7a9abc"
        d.text((28, 298+bi*18), bl, fill=col, font=mono(10))

    # Right panel – IOC analysis
    rect(d, [620,0,W,H], fill="#06080d")
    d.line([620,42,620,H], fill="#141e2c", width=1)
    d.text((636,55), "IOC ANALYSIS RESULTS", fill="#64f5ff", font=fnt(11,bold=True))

    ioc_rows = [
        ("URL","paypa1-verify.xyz","#ff4455","MALICIOUS"),
        ("IP","185.220.101.47","#ff8c42","SUSPICIOUS"),
        ("HASH","d41d8cd98f00b204e98","#5af08a","CLEAN"),
        ("DOMAIN","paypa1-verify.xyz","#ff4455","BLOCKED"),
        ("EMAIL","accounts-secure@...","#f5c842","PHISHING"),
    ]
    for ii, (typ, val, col, verdict) in enumerate(ioc_rows):
        y4 = 80 + ii*60
        rect(d, [636, y4, W-14, y4+48], fill="#08111c", radius=6, outline="#152030")
        badge(d, 644, y4+8, typ, "#0a1828", "#64f5ff", fnt(8))
        d.text((644, y4+28), val, fill="#8baed0", font=mono(9))
        tw = d.textlength(verdict, font=fnt(9,bold=True))
        rect(d, [W-14-tw-24, y4+10, W-14-4, y4+30], fill=col+"22", radius=4)
        d.text((W-14-tw-12, y4+13), verdict, fill=col, font=fnt(9,bold=True))

    d.text((636, H-44), "VERDICT:", fill="#3d5070", font=fnt(10))
    rect(d, [636, H-28, W-14, H-8], fill="#200a0a", radius=4)
    d.text((644, H-23), "⚠  HIGH CONFIDENCE PHISHING — QUARANTINE RECOMMENDED", fill="#ff6060", font=fnt(10,bold=True))

    img.save(f"{OUT}/proj_phishing_ioc.jpg", quality=97)
    print("2. proj_phishing_ioc.jpg ✓")

# ─────────────────────────────────────────────
# 3) EVENT LOG THREAT HUNTING
# ─────────────────────────────────────────────
def proj_threat_hunt():
    img = Image.new("RGB", (W, H), "#070b14")
    d = ImageDraw.Draw(img)

    rect(d, [0,0,W,42], fill="#0a0e18")
    d.line([0,42,W,42], fill="#182035", width=1)
    d.text((18,12), "🔍  SysmonView — Event Log Threat Hunter  |  Workstation: CORP-WS-007", fill="#4a6285", font=fnt(11))

    # Process tree
    d.text((20, 56), "PROCESS ANCESTRY TREE", fill="#2d4d6e", font=fnt(9))
    tree = [
        (50,  90, "WINWORD.EXE",  "PID:4812", "#8baed0", 0),
        (140, 150, "cmd.exe",     "PID:5901 ← Suspicious", "#f5c842", 1),
        (230, 210, "powershell.exe","PID:6234 ⚠ Encoded", "#ff6060", 2),
        (320, 270, "net.exe",     "PID:7012 — net user add", "#ff4455", 3),
        (320, 330, "reg.exe",     "PID:7188 — RegAdd HKCU\\Run","#ff4455", 3),
    ]
    prev = {}
    for depth, (lx, ly, name, detail, col, lv) in enumerate(tree):
        rect(d, [lx, ly, lx+340, ly+36], fill="#0a1020", radius=6, outline=col+"55")
        d.rectangle([lx, ly, lx+3, ly+36], fill=col)
        d.text((lx+14, ly+6), name, fill=col, font=mono(11))
        d.text((lx+14, ly+22), detail, fill=col+"99", font=mono(9))
        if depth > 0:
            pname, px, py = list(prev.items())[-1]
            d.line([px+170, py+36, lx+170, ly], fill="#223044", width=1)
        prev[name] = (lx, ly)

    # Sigma rule panel
    rect(d, [720,54,W-14,H-14], fill="#070c16", radius=8, outline="#152030")
    d.text((736, 68), "MATCHING SIGMA RULE", fill="#64f5ff", font=fnt(10, bold=True))
    d.line([736, 86, W-28, 86], fill="#152030", width=1)
    sigma = [
        ("title:", "SuspiciousOfficeChildProcess"),
        ("status:", "stable"),
        ("logsource:", ""),
        ("  product:", "windows"),
        ("  category:", "process_creation"),
        ("detection:", ""),
        ("  selection:", ""),
        ("    ParentImage:", "'*\\\\WINWORD.EXE'"),
        ("    Image:", "['*\\\\cmd.exe','*\\\\powershell*']"),
        ("  condition:", "selection"),
        ("level:", "high"),
        ("tags:", "- attack.t1566.001"),
    ]
    for si, (key, val) in enumerate(sigma):
        d.text((736, 96+si*17), key, fill="#5a7da8", font=mono(10))
        if val:
            d.text((736+120, 96+si*17), val, fill="#f5c842" if "'" in val or "[" in val else "#8bbad8", font=mono(10))

    rect(d, [720, H-54, W-14, H-14], fill="#120a08", radius=6)
    d.text((736, H-44), "VERDICT:", fill="#ff6060", font=fnt(10, bold=True))
    d.text((800, H-44), "T1566.001 + T1059.001 — Office Macro → Cmd → PS Execution Chain Confirmed", fill="#ffb0b0", font=fnt(10))

    img.save(f"{OUT}/proj_threat_hunt.jpg", quality=97)
    print("3. proj_threat_hunt.jpg ✓")

# ─────────────────────────────────────────────
# 4) POST-QUANTUM CRYPTOGRAPHY
# ─────────────────────────────────────────────
def proj_pqc():
    img = Image.new("RGB", (W, H), "#030508")
    d = ImageDraw.Draw(img)

    # Terminal fill
    rect(d, [0,0,W,H], fill="#0a0f1a")
    rect(d, [0,0,W,36], fill="#111828")
    d.line([0,36,W,36], fill="#1a2638", width=1)
    # Traffic-light dots
    for i, col in enumerate(["#ff5f56","#ffbd2e","#27c93f"]):
        d.ellipse([14+i*20, 12, 26+i*20, 24], fill=col)
    d.text((80, 11), "root@ubuntu:~/pqc-research  — bash  128×38", fill="#3d5070", font=mono(10))

    lines = [
        ("# Post-Quantum Cryptography Benchmark Suite v3.1","#4a6285"),
        ("# NIST PQC Round 4 Finalists — Performance Analysis","#4a6285"),
        ("",""),
        ("$ python3 pqc_bench.py --algorithms kyber1024,dilithium5 --rounds 10000","#64f5ff"),
        ("",""),
        ("[*] Initializing CRYSTALS-Kyber-1024 (KEM)...","#8baed0"),
        ("    Key Generation:    0.083 ms   ← 12x faster than RSA-4096","#5af08a"),
        ("    Encapsulation:     0.092 ms","#5af08a"),
        ("    Decapsulation:     0.089 ms","#5af08a"),
        ("    Security Level:    NIST Level 5 (256-bit quantum security)","#64f5ff"),
        ("",""),
        ("[*] Initializing CRYSTALS-Dilithium-5 (DSA)...","#8baed0"),
        ("    Key Generation:    0.141 ms","#5af08a"),
        ("    Signing:           0.237 ms","#5af08a"),
        ("    Verification:      0.183 ms","#5af08a"),
        ("    Security Level:    NIST Level 5  ✓ APPROVED","#64f5ff"),
        ("",""),
        ("[✓] RSA-4096 Comparison: KeyGen 1.24s | Sign 0.93s  ← VULNERABLE to Shor's","#ff6060"),
        ("[✓] Benchmark COMPLETE — PQC algorithms 14.9x faster on avg","#5af08a"),
        ("",""),
        ("$ _","#64f5ff"),
    ]
    for li, (line, col) in enumerate(lines):
        if col:
            d.text((20, 46+li*19), line, fill=col, font=mono(11))

    img.save(f"{OUT}/proj_pqc.jpg", quality=97)
    print("4. proj_pqc.jpg ✓")

# ─────────────────────────────────────────────
# 5) 30-DAY SOC CHALLENGE DASHBOARD
# ─────────────────────────────────────────────
def proj_30day_soc():
    img = Image.new("RGB", (W, H), "#06080e")
    d = ImageDraw.Draw(img)

    rect(d, [0,0,W,42], fill="#090c16")
    d.line([0,42,W,42], fill="#141e2e", width=1)
    d.text((18,8), "Wazuh SIEM  |  30-Day SOC Challenge — Threat Hunting Dashboard", fill="#3d5a78", font=fnt(11))
    d.text((W-200,8), "🟢 LIVE  |  Day 30 / 30", fill="#5af08a", font=fnt(10))
    d.text((18,24), "Last update: 03:12 UTC  •  All systems nominal", fill="#2a4060", font=fnt(9))

    # Metric cards
    cards = [("8,472","Total Alerts","#64f5ff","▲ 12% vs yesterday"),
             ("347","Threats Blocked","#5af08a","▲ 8 today"),
             ("29","MITRE TTPs","#a07af0","T1566 T1059 T1021..."),
             ("100%","Challenge Complete","#f5c842","All 30 days ✓")]
    for i,(val,lbl,col,sub) in enumerate(cards):
        x = 14 + i*344; y5 = 52
        rect(d, [x,y5,x+330,y5+72], fill="#08111e", radius=8, outline="#152540")
        d.text((x+16,y5+10), val, fill=col, font=fnt(26,bold=True))
        d.text((x+16,y5+46), lbl, fill="#5c7a9e", font=fnt(10))
        d.text((x+16,y5+60), sub, fill=col+"88", font=fnt(9))

    # Alert spike chart (bars)
    rect(d, [14,136,W//2+60,H-14], fill="#07101c", radius=8, outline="#122030")
    d.text((28,150), "DAILY ALERT VOLUME — 30 DAYS", fill="#2d4d6e", font=fnt(9))
    bar_vals = [120,180,95,220,310,185,240,170,290,350,
                210,185,320,280,195,260,310,230,180,340,
                290,220,360,195,310,270,330,280,390,420]
    bw, bx, by, bh = 24, 30, H-30, 160
    for bi, bv in enumerate(bar_vals):
        bh2 = int((bv/450)*bh)
        col2 = "#64f5ff" if bi==29 else "#1a4060"
        rect(d, [bx+bi*30, by-bh2, bx+bi*30+bw, by], fill=col2, radius=3)
    d.text((28, H-44), "Day 1", fill="#2a4060", font=fnt(8))
    d.text((W//2+28, H-44), "Day 30", fill="#64f5ff", font=fnt(8))

    # MITRE donut
    rect(d, [W//2+76,136,W-14,H-14], fill="#07101c", radius=8, outline="#122030")
    d.text((W//2+90,150), "MITRE ATT&CK COVERAGE", fill="#2d4d6e", font=fnt(9))
    cx, cy, r = W//2+280, 300, 80
    slices = [(0.35,"#64f5ff","Initial Access"),(0.28,"#a07af0","Execution"),
              (0.20,"#5af08a","Persistence"),(0.17,"#f5c842","Defense Evasion")]
    start = -90
    for frac, col, label in slices:
        deg = frac*360
        d.pieslice([cx-r,cy-r,cx+r,cy+r], start=start, end=start+deg, fill=col+"33", outline=col)
        start += deg
    d.ellipse([cx-52,cy-52,cx+52,cy+52], fill="#07101c")
    d.text((cx-14,cy-10), "29", fill="#fff", font=fnt(22,bold=True))
    d.text((cx-14,cy+16), "TTPs", fill="#4a6a8a", font=fnt(9))
    for i,(frac,col,label) in enumerate(slices):
        lx2 = W//2+90; ly2 = 180+i*30
        rect(d, [lx2,ly2+2,lx2+12,ly2+14], fill=col, radius=2)
        d.text((lx2+18,ly2), label, fill="#6a8ab0", font=fnt(10))

    img.save(f"{OUT}/proj_30day_soc.jpg", quality=97)
    print("5. proj_30day_soc.jpg ✓")

# ─────────────────────────────────────────────
# 6) FILE INTEGRITY MONITOR
# ─────────────────────────────────────────────
def proj_fim():
    img = Image.new("RGB", (W, H), "#030508")
    d = ImageDraw.Draw(img)

    rect(d, [0,0,W,H], fill="#0a0f1a")
    rect(d, [0,0,W,36], fill="#111828")
    d.line([0,36,W,36], fill="#1a2638", width=1)
    for i, col in enumerate(["#ff5f56","#ffbd2e","#27c93f"]):
        d.ellipse([14+i*20, 12, 26+i*20, 24], fill=col)
    d.text((80, 11), "PS C:\\fim-monitor>  File Integrity Monitor — PowerShell Engine", fill="#3d5070", font=mono(10))

    lines = [
        ("# File Integrity Monitor — SHA-512 Baseline Engine","#4a6285"),
        ("# Monitors: C:\\Windows\\System32  |  C:\\Windows\\Hosts  |  SAM","#4a6285"),
        ("",""),
        ("PS> .\\Start-FIM.ps1 -Baseline create -Verbose","#64f5ff"),
        ("[*] Hashing 24,891 files with SHA-512...","#8baed0"),
        ("[✓] Baseline created → C:\\fim\\baseline_2025-09-14.json","#5af08a"),
        ("",""),
        ("PS> .\\Start-FIM.ps1 -Monitor -Interval 30s","#64f5ff"),
        ("[*] FIM Engine started. Monitoring 24,891 files...","#8baed0"),
        ("[*] Checking integrity at: 03:01:14 UTC...","#8baed0"),
        ("",""),
        ("[!] TAMPER DETECTED  ←─────────────────────────────────────","#ff4455"),
        ("    File:       C:\\Windows\\System32\\drivers\\etc\\hosts","#ff8888"),
        ("    Expected:   sha512:a9b4f71c3d...e8f9  ✓  (baseline)","#5af08a"),
        ("    Found:      sha512:00000000000...XXXX  ✗  (MODIFIED)","#ff4455"),
        ("    Modified:   2025-09-14 03:00:52 UTC","#f5c842"),
        ("    Action:     AUTO-RESTORE from backup initiated ✓","#5af08a"),
        ("",""),
        ("[✓] Restore complete. Re-hash verified. Alert logged.","#5af08a"),
        ("[*] Next scan in: 30s | Events logged: 1 | Status: ACTIVE","#64f5ff"),
        ("",""),
        ("PS> _","#64f5ff"),
    ]
    for li, (line, col) in enumerate(lines):
        if col:
            d.text((20, 46+li*19), line, fill=col, font=mono(11))

    img.save(f"{OUT}/proj_fim.jpg", quality=97)
    print("6. proj_fim.jpg ✓")

# ─────────────────────────────────────────────
# 7) SMART TRAFFIC LOGGER
# ─────────────────────────────────────────────
def proj_smart_traffic():
    img = Image.new("RGB", (W, H), "#f4f6f9")
    d = ImageDraw.Draw(img)

    # White nav
    rect(d, [0,0,W,54], fill="#ffffff")
    d.line([0,54,W,54], fill="#e2e8f0", width=1)
    d.text((20,16), "🚦  SmartTraffic Admin", fill="#1e2d45", font=fnt(14,bold=True))
    d.text((20,34), "Traffic Violation Management System", fill="#7a8fa8", font=fnt(10))
    rect(d, [W-160,12,W-20,42], fill="#3b82f6", radius=8)
    d.text((W-148,21), "+ New Violation", fill="#fff", font=fnt(10,bold=True))

    # Stats
    stats = [("1,284","Total Violations","#3b82f6"),
             ("89","Fines Pending","#ef4444"),
             ("195","Fines Collected","#22c55e"),
             ("₹4.8L","Revenue This Month","#8b5cf6")]
    for i,(val,lbl,col) in enumerate(stats):
        x = 20+i*340; y6=66
        rect(d, [x,y6,x+320,y6+70], fill="#fff", radius=8, outline="#e2e8f0")
        d.text((x+16,y6+10), val, fill=col, font=fnt(24,bold=True))
        d.text((x+16,y6+44), lbl, fill="#94a3b8", font=fnt(10))

    # Table
    rect(d, [20,148,W-20,H-16], fill="#fff", radius=10, outline="#e2e8f0")
    d.text((36,162), "RECENT VIOLATIONS", fill="#94a3b8", font=fnt(9))
    col_h = ["VIO. ID","VEHICLE NO.","TYPE","LOCATION","SPEED","STATUS","ACTION"]
    col_x = [36,150,300,440,620,720,860]
    for hx,ht in zip(col_x,col_h):
        d.text((hx,180), ht, fill="#94a3b8", font=fnt(9))
    rect(d, [20,195,W-20,196], fill="#e2e8f0")

    rows2 = [
        ("VIO-4821","MH-12-AB-3421","Speed","NH-48, Pune","98/60km","PENDING","Edit | Fine | QR"),
        ("VIO-4820","KA-01-CD-7890","Red Light","Signal 5, Blore","—","PAID","View | QR"),
        ("VIO-4819","TN-09-EF-5544","Wrong Side","Anna Salai, Chennai","—","PENDING","Edit | Fine | QR"),
        ("VIO-4818","MH-04-GH-1122","No Helmet","Baner Rd, Pune","—","PAID","View | QR"),
        ("VIO-4817","DL-01-IJ-9988","Speed","Ring Road, Delhi","112/80km","PENDING","Edit | Fine | QR"),
    ]
    st_col = {"PENDING":"#ef4444","PAID":"#22c55e"}
    for ri2, row2 in enumerate(rows2):
        y7 = 204 + ri2*40
        bg = "#f8fafd" if ri2%2==0 else "#ffffff"
        rect(d, [20,y7,W-20,y7+38], fill=bg)
        for j2,(cx2,cv2) in enumerate(zip(col_x,row2)):
            if j2==5:
                col3 = st_col.get(cv2,"#94a3b8")
                rect(d, [cx2-2,y7+9,cx2+64,y7+28], fill=col3+"22", radius=4)
                d.text((cx2+6,y7+13), cv2, fill=col3, font=fnt(9,bold=True))
            elif j2==6:
                d.text((cx2,y7+13), cv2, fill="#3b82f6", font=fnt(9))
            else:
                d.text((cx2,y7+13), cv2, fill="#334155" if j2<3 else "#64748b", font=fnt(9))
        d.line([20,y7+38,W-20,y7+38], fill="#f1f5f9", width=1)

    img.save(f"{OUT}/proj_smart_traffic.jpg", quality=97)
    print("7. proj_smart_traffic.jpg ✓")

# ─────────────────────────────────────────────
# 8) VIBE CHECK — SENTIMENT ANALYZER
# ─────────────────────────────────────────────
def proj_vibe_check():
    img = Image.new("RGB", (W, H), "#f9fafb")
    d = ImageDraw.Draw(img)

    rect(d, [0,0,W,54], fill="#fff")
    d.line([0,54,W,54], fill="#e5e7eb", width=1)
    d.text((20,14), "💬  VibeCheck — Real-Time Sentiment Analyzer", fill="#111827", font=fnt(14,bold=True))
    d.text((20,34), "NLP Pipeline  •  1,254 reviews analyzed", fill="#9ca3af", font=fnt(10))

    # Donut chart (left)
    rect(d, [20,68,460,H-16], fill="#fff", radius=10, outline="#e5e7eb")
    d.text((36,80), "SENTIMENT DISTRIBUTION", fill="#9ca3af", font=fnt(9))
    cx2, cy2, ro, ri2 = 230, 270, 110, 60
    for ang, sweep, col, lbl, pct in [
            (-90,  190, "#22c55e","Positive","52.8%"),
            (100,  100, "#ef4444","Negative","27.7%"),
            (200,   70, "#f59e0b","Neutral","19.5%")]:
        d.pieslice([cx2-ro,cy2-ro,cx2+ro,cy2+ro], start=ang, end=ang+sweep, fill=col)
    d.ellipse([cx2-ri2,cy2-ri2,cx2+ri2,cy2+ri2], fill="#fff")
    d.text((cx2-30,cy2-14), "52.8%", fill="#22c55e", font=fnt(18,bold=True))
    d.text((cx2-22,cy2+8),  "Positive", fill="#9ca3af", font=fnt(9))
    for i,(col,lbl,pct) in enumerate([(("22c55e"),"Positive","52.8%"),(("ef4444"),"Negative","27.7%"),(("f59e0b"),"Neutral","19.5%")]):
        lxi = 36; lyi = 360+i*26
        d.ellipse([lxi,lyi+2,lxi+12,lyi+14], fill=f"#{col}")
        d.text((lxi+18,lyi), f"{lbl} — {pct}", fill="#374151", font=fnt(10))

    # Bar chart (right)
    rect(d, [476,68,W-20,H-16], fill="#fff", radius=10, outline="#e5e7eb")
    d.text((492,80), "DAILY SENTIMENT TREND — LAST 7 DAYS", fill="#9ca3af", font=fnt(9))
    days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    pos_v = [68,55,72,48,80,62,76]
    neg_v = [18,30,15,40,12,24,18]
    bx2, by2, bw2, gap = 500, H-40, 40, 80
    for di,(day,pv,nv) in enumerate(zip(days,pos_v,neg_v)):
        bxd = bx2+di*gap
        ph = int((pv/100)*200); nh = int((nv/100)*200)
        rect(d, [bxd,     by2-ph, bxd+18,   by2], fill="#22c55e", radius=3)
        rect(d, [bxd+22, by2-nh, bxd+40, by2], fill="#ef4444", radius=3)
        d.text((bxd+6, by2+6), day, fill="#9ca3af", font=fnt(9))

    # Quote
    rect(d, [476,290,W-20,H-16], fill="#f0fdf4", radius=8, outline="#86efac")
    d.text((492,302), "TOP POSITIVE REVIEW", fill="#16a34a", font=fnt(9))
    d.text((492,320), '"This product completely exceeded all my expectations."', fill="#15803d", font=fnt(11))

    img.save(f"{OUT}/proj_vibe_check.jpg", quality=97)
    print("8. proj_vibe_check.jpg ✓")

# ─────────────────────────────────────────────
# 9) SKIN AI — DERMATOLOGY DASHBOARD
# ─────────────────────────────────────────────
def proj_skin_ai():
    img = Image.new("RGB", (W, H), "#070d1a")
    d = ImageDraw.Draw(img)

    rect(d, [0,0,W,48], fill="#0a1122")
    d.line([0,48,W,48], fill="#162035", width=1)
    d.text((20,12), "🩺  Skin AI — Dermatological Diagnostic Platform", fill="#4a6fa8", font=fnt(12,bold=True))
    d.text((20,30), "Deep CNN  •  ResNet-50 backbone  •  v2.1.0  •  AIIMS-validated dataset", fill="#2d4d70", font=fnt(9))
    rect(d, [W-170,10,W-16,38], fill="#0f2a4a", radius=6, outline="#1e4a7a")
    d.text((W-160,19), "📁  Upload New Image", fill="#60a5fa", font=fnt(10))

    # Upload zone
    rect(d, [20,60,480,H-16], fill="#08111e", radius=10, outline="#162535")
    d.text((36,74), "ANALYSIS QUEUE", fill="#2d4d6e", font=fnt(9))
    # Skin image placeholder with scan lines
    rect(d, [36,92,464,268], fill="#0b1828", radius=8, outline="#1e3a55")
    for si in range(0, 176, 8):
        d.line([36, 92+si, 464, 92+si], fill="#0d1f30", width=1)
    d.text((220,168), "◌", fill="#1e4a6e", font=fnt(48))
    d.text((165,214), "DROP IMAGE OR CLICK TO UPLOAD", fill="#1e3a55", font=fnt(9))
    # Scan beam
    rect(d, [36,180,464,184], fill="#64f5ff22", radius=2)
    d.line([36,182,464,182], fill="#64f5ff44", width=1)

    d.text((36,278), "PROCESSING STATUS", fill="#2d4d6e", font=fnt(9))
    statuses = [("img_scan_001.jpg","Processing","#64f5ff","▓▓▓▓▓▓▓░░","78%"),
                ("img_scan_002.jpg","Complete","#5af08a","▓▓▓▓▓▓▓▓▓","100%"),
                ("img_scan_003.jpg","Queued","#f5c842","░░░░░░░░░","0%")]
    for si2,(fn,st,col,bar,pct) in enumerate(statuses):
        y8 = 298+si2*40
        rect(d,[36,y8,464,y8+34],fill="#081422",radius=5,outline="#122030")
        d.text((50,y8+8),fn,fill="#7a9abf",font=mono(9))
        d.text((50,y8+22),st,fill=col,font=fnt(9,bold=True))
        d.text((340,y8+8),bar,fill=col,font=mono(9))
        d.text((430,y8+8),pct,fill=col,font=fnt(9))

    # Results panel
    rect(d, [496,60,W-16,H-16], fill="#08111e", radius=10, outline="#162535")
    d.text((514,74), "DIAGNOSTIC RESULTS", fill="#64f5ff", font=fnt(10,bold=True))
    d.line([514,92,W-30,92], fill="#122030", width=1)
    d.text((514,102), "Input: img_scan_002.jpg  •  ResNet-50 Inference: 0.23s", fill="#2d4d6e", font=fnt(9))

    results = [
        ("Melanocytic Nevus","78.4%","#5af08a","LOW RISK"),
        ("Seborrheic Keratosis","14.2%","#f5c842","MONITOR"),
        ("Melanoma","4.1%","#ff6060","FLAG"),
        ("Dermatofibroma","3.3%","#8baed0","LOW RISK"),
    ]
    for ri3,(name,conf,col,risk) in enumerate(results):
        y9=126+ri3*64
        rect(d,[514,y9,W-30,y9+56],fill="#07101c",radius=6,outline="#102030")
        d.text((530,y9+8),name,fill="#d0e0f0",font=fnt(11,bold=True))
        bar_w = int(float(conf[:-1])/100*(W-30-530-60))
        rect(d,[530,y9+30,530+bar_w,y9+38],fill=col,radius=3)
        rect(d,[530,y9+30,W-30-60,y9+38],fill=col+"22",radius=3)
        d.text((530,y9+42),conf,fill=col,font=fnt(9,bold=True))
        tw2=d.textlength(risk,font=fnt(8,bold=True))
        rect(d,[W-30-tw2-20,y9+10,W-30-8,y9+28],fill=col+"33",radius=4)
        d.text((W-30-tw2-12,y9+14),risk,fill=col,font=fnt(8,bold=True))

    img.save(f"{OUT}/proj_skin_ai.jpg", quality=97)
    print("9. proj_skin_ai.jpg ✓")

# ─────────────────────────────────────────────
# 10) BOOKVERSE — BOOK DISCOVERY PLATFORM
# ─────────────────────────────────────────────
def proj_bookverse():
    img = Image.new("RGB", (W, H), "#1a1208")
    d = ImageDraw.Draw(img)

    # Warm dark bg gradient simulation
    for y_ in range(H):
        t = y_/H
        r = int(26 + t*8); g = int(18+t*4); b = int(8+t*4)
        d.line([0,y_,W,y_], fill=(r,g,b))

    # Nav
    rect(d, [0,0,W,54], fill="#120d04ee")
    d.text((24,16), "📚  BookVerse", fill="#f5c842", font=fnt(16,bold=True))
    d.text((180,20), "Discover  •  Shelves  •  Collections  •  Reviews", fill="#8a7055", font=fnt(10))
    rect(d, [W-160,13,W-20,42], fill="#f5c842", radius=8)
    d.text((W-148,22), "🔍  Search Books", fill="#1a1208", font=fnt(10,bold=True))

    # Hero text
    d.text((30,72), "Discover Books That", fill="#e8d8b8", font=fnt(26,bold=True))
    d.text((30,104), "Change Your World.", fill="#f5c842", font=fnt(26,bold=True))
    d.text((30,140), "AI-powered recommendations  •  1.2M+ titles indexed  •  Curated by readers", fill="#7a6a4e", font=fnt(10))

    # Search bar
    rect(d, [30,160,680,198], fill="#211808", radius=10, outline="#3a2d10")
    d.text((50,172), "🔍", fill="#6a5a3a", font=fnt(12))
    d.text((78,175), "Search titles, authors, genres, ISBNs...", fill="#4a3a22", font=fnt(11))
    rect(d, [590,166,668,194], fill="#f5c842", radius=8)
    d.text((604,176), "Search", fill="#1a1208", font=fnt(10,bold=True))

    # Book cards
    books = [
        ("#1e3a2a","🌿","The Midnight Library","Matt Haig","Fiction","4.8 ★"),
        ("#1a1e3a","🌌","Dune","Frank Herbert","Sci-Fi","4.9 ★"),
        ("#3a1a1a","🗡","The Name of the Wind","Patrick Rothfuss","Fantasy","4.7 ★"),
        ("#1a2a3a","💡","Atomic Habits","James Clear","Self-Help","4.9 ★"),
        ("#2a1a3a","🔮","Project Hail Mary","Andy Weir","Sci-Fi","4.8 ★"),
    ]
    for bi2,(bg_col,ico,title,auth,genre,rating) in enumerate(books):
        bx3 = 30 + bi2*268
        rect(d, [bx3,214,bx3+252,H-16], fill=bg_col, radius=10, outline="#3a2d10")
        d.text((bx3+16,230), ico, fill="#fff", font=fnt(28))
        d.text((bx3+16,268), title, fill="#f0e0c0", font=fnt(11,bold=True))
        d.text((bx3+16,288), auth, fill="#9a8060", font=fnt(10))
        badge(d, bx3+16, 308, genre, "#ffffff22", "#c4a86a", fnt(9))
        d.text((bx3+16,334), rating, fill="#f5c842", font=fnt(11,bold=True))
        rect(d, [bx3+16,364,bx3+138,H-32], fill="#f5c84233", radius=6)
        d.text((bx3+30,370), "Add to Shelf", fill="#f5c842", font=fnt(9,bold=True))

    img.save(f"{OUT}/proj_bookverse.jpg", quality=97)
    print("10. proj_bookverse.jpg ✓")

# ─────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    proj_soc_lab()
    proj_phishing_ioc()
    proj_threat_hunt()
    proj_pqc()
    proj_30day_soc()
    proj_fim()
    proj_smart_traffic()
    proj_vibe_check()
    proj_skin_ai()
    proj_bookverse()
    print("\n✓ ALL 10 FRAME-FILLING PROJECT IMAGES GENERATED!")

# Z jednoplikowej gry (zrodla/rewir.html) robi wersję dla serwera (folder rewir/), która pobiera tylko potrzebne części:
#   index.html (rdzeń) + i18n-en.js (tylko po angielsku) + img/*.webp (budynki, przy rysowaniu) + m/silo3d.js (przy otwarciu Silosu)
# Uruchom po każdej zmianie w zrodla/rewir.html:   python3 narzedzia/podziel.py
import re, json, base64, hashlib, os, sys, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'zrodla', 'rewir.html')
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, 'rewir')
VER = '200'
s = open(SRC, encoding='utf-8').read()
if os.path.isdir(OUT): shutil.rmtree(OUT)
os.makedirs(OUT + '/img'); os.makedirs(OUT + '/m')
def one(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:90]); s = s.replace(a, b)

# ---------- 1. słownik EN do osobnego pliku, wczytywany tylko po angielsku ----------
m = re.search(r'<script type="application/json" id="i18nEN">(.*?)</script>', s, re.S)
D = json.loads(m.group(1))
open(OUT + '/i18n-en.js', 'w', encoding='utf-8').write('window.__I18N_EN=' + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + ';\n')
loader = ('<script>/* v200: słownik EN tylko dla wersji angielskiej (i18n-en.js); kopia w pamięci telefonu na wypadek braku internetu */'
 "(function(){var L='';try{var q=(location.search.match(/[?&]lang=(pl|en)(?:&|$)/)||[])[1];L=q||localStorage.getItem('linia.lang')||'';}catch(e){}"
 "if(L!=='pl'&&L!=='en')L=/^pl/i.test(String(navigator.language||''))?'pl':'en';"
 "if(L==='en')document.write('<script data-mod=\"1\" src=\"i18n-en.js?v=" + VER + "\"><\\/script><script>(function(){var K=\"linia.i18nEN." + VER + "\";try{if(window.__I18N_EN){var j=JSON.stringify(window.__I18N_EN);if(localStorage.getItem(K)!==j){for(var i=localStorage.length-1;i>=0;i--){var k=localStorage.key(i);if(k&&k.indexOf(\"linia.i18nEN.\")===0)localStorage.removeItem(k);}localStorage.setItem(K,j);}}else window.__I18N_EN=JSON.parse(localStorage.getItem(K)||\"null\");}catch(e){}})();<\\/script>');"
 "})();</script>")
s = s[:m.start()] + loader + s[m.end():]
one("var D={};try{D=JSON.parse(document.getElementById('i18nEN').textContent);}catch(e){}", "var D=window.__I18N_EN||{};")

# ---------- 2. obrazki budynków jako pliki (pobierane dopiero, gdy budynek jest rysowany) ----------
seen = {}
def save(url, name):
    raw = base64.b64decode(url.split(',', 1)[1]); h = hashlib.sha1(raw).hexdigest()
    if h in seen: return seen[h]
    fn = 'img/' + name + '.webp'; open(OUT + '/' + fn, 'wb').write(raw); seen[h] = fn; return fn
def jrep(var, fn):
    global s
    mm = re.search(r'const ' + var + r'=(\{.*?\});', s); assert mm, var
    o = json.loads(mm.group(1)); fn(o)
    s = s[:mm.start(1)] + json.dumps(o, ensure_ascii=False) + s[mm.end(1):]
def bspr(o):
    for k, a in o.items():
        for i, u in enumerate(a): a[i] = save(u, 'b-%s-%d' % (k, i + 1))
def fspr(o):
    for k, d in o.items():
        for lv, e in d.items(): e[0] = save(e[0], 'f-%s-%s' % (k, lv))
jrep('BSPR', bspr); jrep('FSPR', fspr)
mm = re.search(r'const BSAIL="(data:image/webp;base64,[^"]+)";', s); s = s[:mm.start(1)] + save(mm.group(1), 'b-mlyn-skrzydla') + s[mm.end(1):]
assert 'data:image/webp;base64' not in s, 'zostały obrazki base64'
one("if(t&&(t.tagName==='SCRIPT'||t.tagName==='LINK')){var u=t.src||t.href||'';", "if(t&&(t.tagName==='SCRIPT'||t.tagName==='LINK')){var u=t.src||t.href||'';if(t.getAttribute&&t.getAttribute('data-mod'))return;")

# ---------- 3. silos 3D jako moduł na żądanie ----------
i = s.find('/* ===== v198: SILOS'); j = s.find('/* ===== v176', i); assert i > 0 and j > i
code = s[i:j].rstrip('\n')
# trójwymiarowy silos startuje dopiero, gdy zakładka Silos jest otwarta (wcześniej pobierał three.js przy każdym starcie gry)
if "if(m==='3d'&&tab==='silo')start();}" not in code:
    assert code.count("if(m==='3d')start();}") == 1
    code = code.replace("if(m==='3d')start();}", "if(m==='3d'&&tab==='silo')start();}")
open(OUT + '/m/silo3d.js', 'w', encoding='utf-8').write('/* Rewir: moduł silosu 3D (v198), wczytywany przez __modLoad("silo3d") */\n(window.__modSrc=window.__modSrc||{})["silo3d"]=' + json.dumps(code, ensure_ascii=False) + ';\n')
stub = r'''/* ===== v200: MODUŁY NA ŻĄDANIE — część gry pobiera się dopiero, gdy jest potrzebna (m/*.js). Kod modułu uruchamia się
   wewnątrz gry (ma dostęp do jej stanu), a kopia zostaje w pamięci telefonu, więc działa też bez internetu. ===== */
const __MODS={},__MV='%s';
function __modRun(name,src){eval(src+'\n//# sourceURL=m/'+name+'.js');}
function __modLoad(name){
  if(__MODS[name])return __MODS[name];
  const K='linia.mod.'+name+'.',fromCache=()=>{try{return localStorage.getItem(K+__MV);}catch(e){return null;}};
  return __MODS[name]=new Promise((res,rej)=>{
    const run=src=>{try{__modRun(name,src);res();}catch(e){console.error(e);rej(e);}};
    const s=document.createElement('script');s.dataset.mod='1';s.src='m/'+name+'.js?v='+__MV;s.async=true;
    s.onload=()=>{s.remove();const src=window.__modSrc&&window.__modSrc[name];if(src==null){const c=fromCache();if(c!=null)return run(c);delete __MODS[name];return rej(new Error('moduł '+name));}
      delete window.__modSrc[name];try{for(let i=localStorage.length-1;i>=0;i--){const k=localStorage.key(i);if(k&&k.indexOf(K)===0&&k!==K+__MV)localStorage.removeItem(k);}localStorage.setItem(K+__MV,src);}catch(e){}run(src);};
    s.onerror=()=>{s.remove();const c=fromCache();if(c!=null)return run(c);delete __MODS[name];rej(new Error('offline: '+name));};
    document.head.appendChild(s);});
}
window.__modLoad=__modLoad;
/* silos 3D: pobiera się przy pierwszym otwarciu zakładki Silos (do tego czasu działa przekrój 2D) */
function __siloMiss(){const p=document.getElementById('tab-silo'),cv=document.getElementById('siloCv');if(!p||!cv||document.getElementById('s3Miss'))return;const d=document.createElement('div');d.id='s3Miss';d.className='disc';d.style.cssText='margin:6px 0;padding:8px 10px;border-radius:10px;border:1px solid var(--line)';
  d.textContent='Widok 3D silosu jest w osobnym pliku (m/silo3d.js), którego tu nie ma. Pokazuję przekrój. Otwórz grę z serwera (np. Netlify) albo użyj wersji w jednym pliku.';cv.parentNode.insertBefore(d,cv);}
{const go=()=>__modLoad('silo3d').catch(__siloMiss);const _st=setTab;setTab=function(t){const r=_st.apply(this,arguments);if(t==='silo')go();return r;};if(tab==='silo')go();}
''' % VER
s = s[:i] + stub + s[j:]
open(OUT + '/index.html', 'w', encoding='utf-8').write(s)
tot = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(OUT) for f in fs)
print('index.html %.0f KB | i18n-en.js %.0f KB | img %d plików %.0f KB | m/silo3d.js %.0f KB | razem %.0f KB' % (
    os.path.getsize(OUT + '/index.html') / 1024, os.path.getsize(OUT + '/i18n-en.js') / 1024, len(os.listdir(OUT + '/img')),
    sum(os.path.getsize(OUT + '/img/' + f) for f in os.listdir(OUT + '/img')) / 1024, os.path.getsize(OUT + '/m/silo3d.js') / 1024, tot / 1024))

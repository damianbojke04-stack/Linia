# Zamienia czytelne źródła modułów (zrodla/*.js) na pliki wczytywane przez grę na żądanie (rewir/m/*.js).
# Uruchom po każdej zmianie w zrodla/:  python3 narzedzia/zbuduj-moduly.py
import json, os, glob
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for f in sorted(glob.glob(os.path.join(root, 'zrodla', '*.js'))):
    name = os.path.splitext(os.path.basename(f))[0]
    code = open(f, encoding='utf-8').read().rstrip('\n')
    out = os.path.join(root, 'rewir', 'm', name + '.js')
    open(out, 'w', encoding='utf-8').write('/* Rewir: moduł „%s” wczytywany przez __modLoad("%s"). Nie edytuj — źródło: zrodla/%s.js */\n(window.__modSrc=window.__modSrc||{})[%s]=%s;\n'
        % (name, name, name, json.dumps(name), json.dumps(code, ensure_ascii=False)))
    print('zbudowano', os.path.relpath(out, root))

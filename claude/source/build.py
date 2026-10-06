import re, sys, textwrap, html, pathlib
from pygments import highlight
from pygments.lexers import PythonLexer, PythonConsoleLexer, TextLexer, TOMLLexer, BashLexer
from pygments.formatters import HtmlFormatter

ROOT = pathlib.Path(__file__).parent
fmt = HtmlFormatter(nowrap=True)

def attrs(s):
    d = dict(re.findall(r'(\w+)="([^"]*)"', s))
    flags = set(re.sub(r'\w+="[^"]*"', '', s).split())
    return d, flags

def render(m):
    tag, a, code = m.group(1), m.group(2), m.group(3)
    d, flags = attrs(a)
    code = textwrap.dedent(code.strip('\n')).rstrip()
    kind = 'bad' if 'bad' in flags else 'good' if 'good' in flags else 'out' if tag == 'out' else ''
    cap = d.get('cap')
    if cap is None:
        cap = {'bad': '❌ 문제 있는 코드', 'good': '✅ 개선된 코드', 'out': '출력 / 결과'}.get(kind, '')
    if tag == 'out':
        body = html.escape(code)
    elif d.get('lang') == 'toml':
        body = highlight(code, TOMLLexer(), fmt)
    elif d.get('lang') == 'text':
        body = html.escape(code)
    elif d.get('lang') == 'sh':
        body = highlight(code, BashLexer(), fmt)
    elif 'console' in flags:
        body = highlight(code, PythonConsoleLexer(), fmt)
    else:
        body = highlight(code, PythonLexer(), fmt)
    if 'ln' in flags:
        lines = body.rstrip('\n').split('\n')
        w = len(str(len(lines)))
        body = '\n'.join(f'<span class="ln">{i:>{w}}</span>{l}' for i, l in enumerate(lines, 1))
    caph = f'<div class="cap">{cap}</div>' if cap else ''
    return f'<div class="code {kind}">{caph}<pre class="hl"><code>{body.rstrip()}</code></pre></div>'

parts = sorted((ROOT / 'src').glob('*.html'))
src = '\n'.join(p.read_text(encoding='utf-8') for p in parts)
out = re.sub(r'<(py|out)((?:\s[^>]*)?)>(.*?)</\1>', render, src, flags=re.S)
tpl = (ROOT / 'template.html').read_text(encoding='utf-8')
result = tpl.replace('%%SLIDES%%', out)
dest = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / 'out.html')
dest.write_text(result, encoding='utf-8')
print(dest, len(result), 'bytes,', out.count('<section'), 'slides')

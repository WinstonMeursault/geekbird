#!/usr/bin/env python3
"""Build Cloudflare Pages output (no npm dependencies)."""
import json
import shutil

from release import FILES, ROOT, validate


def build():
    validate()
    output = ROOT / 'dist' / 'cloudflare'
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    for name in FILES:
        destination = output / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, destination)
    html = (ROOT / 'cloudflare/admin.html').read_text(encoding='utf-8')
    worker = (ROOT / 'cloudflare/worker.js').read_text(encoding='utf-8')
    assert worker.count('"__ADMIN_HTML__"') == 1
    (output / '_worker.js').write_text(worker.replace('"__ADMIN_HTML__"', json.dumps(html, ensure_ascii=False)), encoding='utf-8')
    (output / '_routes.json').write_text(json.dumps({
        'version': 1,
        'include': ['/config.js', '/_gb-settings', '/_gb-settings/*'],
        'exclude': [],
    }, indent=2) + '\n', encoding='utf-8')
    print(f'Cloudflare Pages output: {output.relative_to(ROOT)}')


if __name__ == '__main__':
    build()

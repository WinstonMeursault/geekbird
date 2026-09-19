#!/usr/bin/env python3
"""Build Cloudflare Pages output (no npm dependencies)."""
import json
import hashlib
import shutil
import zipfile

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
    for name in ('404.html', '_headers', 'robots.txt', 'sitemap.xml'):
        shutil.copyfile(ROOT / 'cloudflare' / name, output / name)
    html = (ROOT / 'cloudflare/admin.html').read_text(encoding='utf-8')
    worker = (ROOT / 'cloudflare/worker.js').read_text(encoding='utf-8')
    assert worker.count('"__ADMIN_HTML__"') == 1
    (output / '_worker.js').write_text(worker.replace('"__ADMIN_HTML__"', json.dumps(html, ensure_ascii=False)), encoding='utf-8')
    (output / '_routes.json').write_text(json.dumps({
        'version': 1,
        'include': ['/config.js', '/_*'],
        'exclude': [],
    }, indent=2) + '\n', encoding='utf-8')
    # Package only the explicit Pages output; secrets, VPS service and docs stay out.
    manifest = {str(path.relative_to(output)): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in sorted(output.rglob('*')) if path.is_file()}
    archive = ROOT / 'dist/geekbird-cloudflare-pages.zip'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as package:
        for name in manifest:
            entry = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            package.writestr(entry, (output / name).read_bytes())
    with zipfile.ZipFile(archive) as package:
        assert set(package.namelist()) == set(manifest)
        for name, expected in manifest.items():
            assert hashlib.sha256(package.read(name)).hexdigest() == expected
    (ROOT / 'dist/cloudflare-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    (ROOT / 'dist/cloudflare-SHA256SUMS').write_text(''.join(
        f'{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n'
        for path in (archive, ROOT / 'dist/cloudflare-manifest.json')), encoding='utf-8')
    print(f'Cloudflare Pages output: {output.relative_to(ROOT)}')
    print(f'Verified {len(manifest)} files; archive: {archive.relative_to(ROOT)}')


if __name__ == '__main__':
    build()

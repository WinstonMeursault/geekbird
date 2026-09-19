#!/usr/bin/env python3
"""Package the public site and the private Python settings service for a VPS."""
import io
import tarfile
from release import ROOT, FILES, validate


if __name__ == '__main__':
    validate()
    output = ROOT / 'dist/geekbird-vps.tar.gz'
    output.parent.mkdir(exist_ok=True)
    files = [(ROOT / name, 'public/' + name) for name in FILES]
    files += [(ROOT / 'server/admin.py', 'server/admin.py'),
              (ROOT / 'cloudflare/admin.html', 'server/admin.html')]
    with tarfile.open(output, 'w:gz') as archive:
        for source, name in files:
            content = source.read_bytes()
            entry = tarfile.TarInfo(name)
            entry.size = len(content)
            entry.mode = 0o644
            archive.addfile(entry, io.BytesIO(content))
    print(f'Packaged {output.relative_to(ROOT)}')

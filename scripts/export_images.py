#!/usr/bin/env python3
"""Export website backgrounds from original PNGs without resizing (requires Pillow)."""
import argparse
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SOURCES = (
    ('feathers', 'ChatGPT Image 2026年9月19日 14_24_44.png', False, (760, 0, 1640, 941)),
    ('landscape', 'ChatGPT Image 2026年9月19日 14_32_15.png', True, (650, 0, 1600, 941)),
    ('architecture', 'ChatGPT Image 2026年9月19日 14_32_01.png', False, (680, 0, 1520, 1024)),
)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'assets/images')
    parser.add_argument('--lossless', action='store_true', help='Preserve all source pixels at a larger file size')
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    total = 0
    for name, filename, mirror, crop in SOURCES:
        with Image.open(ROOT / 'design/originals' / filename) as original:
            source = original.convert('RGB')
        if mirror:
            source = ImageOps.mirror(source)
        for suffix, image in (('', source), ('-mobile', source.crop(crop))):
            target = args.output_dir / f'{name}{suffix}.webp'
            image.save(target, format='WEBP', quality=95, method=6, lossless=args.lossless)
            with Image.open(target) as result:
                assert result.size == image.size
                if args.lossless:
                    assert result.convert('RGB').tobytes() == image.tobytes()
            total += target.stat().st_size
            print(f'{target.name}: {image.width} x {image.height}, {target.stat().st_size:,} bytes')
    print(f'Total: {total:,} bytes; mode: {"lossless" if args.lossless else "quality=95"}')

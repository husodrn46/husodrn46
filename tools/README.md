# Header generator

The artwork in `assets/` is generated, not drawn by hand. Every glyph in it is a
path rather than text, because GitHub serves README images through a proxy where
a web font would never load — so the header has to carry its own letterforms.

That also means the SVGs cannot be edited directly. Change the settings at the
top of `build_header.py` and run it again:

```bash
pip install fonttools
python3 tools/build_header.py
```

It writes both header faces and the four status marks, then you commit whatever
changed.

## What you can change

Everything worth changing sits in one block at the top of the script:

| | |
|---|---|
| `SENTENCE` | The handwritten line. Two lines fit; a third needs the height raised. |
| `NAME`, `ROLE`, `EYEBROW`, `STATUS` | The typeset lines around it. |
| `FACES` | The two colour schemes. `live` is served in dark mode, `sheet` in light. |
| `MARKS` | The status squares used in the README tables. |

Keep the colours matching [husodrn46.com](https://husodrn46.com) — the profile
and the site are meant to read as one identity, and the site's tokens are the
source of truth.

## Fonts

Caveat, Archivo and IBM Plex Mono, the same three the site uses. The script
downloads them into `tools/.fonts/` on first run; that directory is ignored, so
nothing large lands in the repository.

Turkish needs `ş ğ İ ı ç ö ü â`, all of which these three cover — worth checking
if you ever swap a face, because most handwriting fonts do not.

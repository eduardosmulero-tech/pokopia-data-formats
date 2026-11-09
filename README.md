# Pokopia data formats

Written specifications for the on-disk data formats of **Pokémon Pokopia** (Nintendo Switch 2),
measured on a legally owned copy of build **2.0.1a** (update build 655360) and released under
CC BY-SA 4.0. **Not** a toolkit, **not** a modding guide and **not** a copy of any game file.

## Why this exists

There is no written specification for the game's data containers. Reading tools exist — notably
[PokoHex](https://github.com/berichan/PokoHex), a GPL-3.0 save editor — but the container layout,
its edge cases and the conditions for a byte-exact rebuild are not documented anywhere public.

This repository is the **canonical, citable description**: field tables with offsets, the
invariants, the traps that break a naive reader, and the counts that let you check your own
implementation. It is for anyone writing a parser or a diff tool who needs to know where a field
is and why it is there, rather than reverse-engineering it a second time.

## Quickstart

```bash
git clone https://github.com/eduardosmulero-tech/pokopia-data-formats
cd pokopia-data-formats
python tools/check_repo.py                  # expected: "OK — N files checked: ..."
grep -n "0x0C" docs/SPEC-G1T.md             # the header_size field of a G1T file
```

1. Pick a document in the table below and read its §1 (scope and version) first: every figure is
   tied to build 2.0.1a and to no other.
2. Reproduce a number with the command the document gives in its last section. A figure you cannot
   reproduce is a documentation bug — open an issue with the build id, the entry id and the command.
3. Cite it as `pokopia-data-formats`, document name, revision and build. The revision is in the
   first paragraph of every document.

There is nothing to install: the repository is Markdown, a Python guard and a CI workflow.

## Status

| Document | Format | Covers | State |
|---|---|---|---|
| [`docs/SPEC-CONTAINER.md`](docs/SPEC-CONTAINER.md) | `LD_C0_R.BIN` + `LI_C0_R.IDX` | 12,298 entries, record layout, two encodings, block framing, test vectors | revision 1 — published |
| [`docs/SPEC-FDATA.md`](docs/SPEC-FDATA.md) | `.fdata` (`PDRK`/`IDRK`) | 24 archives, 79,710 entries, 25 types, both chunk framings, `.rdb` master index | revision 1 — published |
| [`docs/SPEC-G1T.md`](docs/SPEC-G1T.md) | `G1T` textures | header, 512 B mip chain, pixel-format census, tile swizzle | revision 1 — published |
| [`docs/SPEC-G1M.md`](docs/SPEC-G1M.md) | `G1M` models | 12-byte wrapper trap, header, chunks, sections, mesh counting | revision 1 — published |
| [`docs/SPEC-G1A.md`](docs/SPEC-G1A.md) | `G2A` animations (type `g1a`) | 32 B header, 10-bit bones, key blocks, byte-exact rewrite | revision 1 — published |
| [`docs/SPEC-TEXT.md`](docs/SPEC-TEXT.md) | pointer-plus-pool text | 2,409 tables, the `a` field that is not an offset, three substitution modes | revision 1 — published |
| [`docs/AUDIO.md`](docs/AUDIO.md) | sound banks `ASRS`/`KTSR` | index, sound header field by field, both codecs, external streams | revision 1 — published |
| [`docs/AUDIO-KA1A.md`](docs/AUDIO-KA1A.md) | `KA1A` codec | frames, 21 bands, logarithmic codes, window, bitrate modes | revision 1 — published |

Everything here is measured against build **2.0.1a**. Formats change with game updates; each
document records the build it was measured on.

**Not published yet:** the name and description tables (`#4636`–`#4653`). `SPEC-TEXT.md` §7 records
an open discrepancy with §3.2 of that document, so it stays out of this repository until the
description-table geometry is re-measured. The current text is in the reference implementation,
[pokopia-tools](https://github.com/eduardosmulero-tech/pokopia-tools/blob/master/docs/SPEC-NAMES.md).

### Measured

Container record layout and both entry encodings; `.fdata` entry header and both chunk framings;
`G1T` header, mip alignment and swizzle; `G1M` header, chunks, vertex/index/submesh sections;
`G2A` header, bones, timing and key blocks; the pointer-plus-pool text scheme; `ASRS`/`KTSR` chunk
walk; `KA1A` frames, band tables and window.

### Not measured, and not claimed

The 15 of 41 fields of the 68-byte item row whose meaning is unknown; which bit means what in the
save catalogue bitmap; `G1M` material, shader, palette and socket sections; 641 `G1T` textures
whose mip chain is unexplained; 22 BC6H textures with no encoder; the row → entity mapping of the
narrative text tables; the description-table geometry that `SPEC-TEXT.md` §7 disputes.

### Not in this repository

Code of any kind — the reference implementation is GPL-3.0 and lives in
[pokopia-tools](https://github.com/eduardosmulero-tech/pokopia-tools); game assets, text dumps,
models, textures, audio, saves, keys or firmware; any other build or platform.

## What this repository is not

- **Not game data.** No assets, models, textures, audio, text dumps, keys, firmware or saves.
  `tools/check_repo.py` enforces this locally and in CI.
- **Not a tool.** Parsers and packers live in separate repositories; commands named in a document
  belong to the reference implementation, not here.
- **Not affiliated** with Nintendo, Creatures Inc., GAME FREAK inc. or the authors of PokoHex.

## Verifying a document

Each specification states how its claims were measured and which command reproduces them. If you find
a number you cannot reproduce, that is a documentation bug: open an issue with the build id, the entry
id and the command you ran. See [CONTRIBUTING.md](CONTRIBUTING.md).

The guard runs on every push: `python tools/check_repo.py` checks for forbidden file types, oversized
files, secret-shaped strings, absolute local paths and broken relative links.

## Links

- [CHANGELOG.md](CHANGELOG.md) — what each revision changed.
- [CONTRIBUTING.md](CONTRIBUTING.md) — how to report an error and what is closed on sight.
- [NOTICE](NOTICE) — authorship chain and trademarks.
- [LICENSE](LICENSE) — CC BY-SA 4.0.

## License

Documentation is licensed under **Creative Commons Attribution-ShareAlike 4.0 International**
(CC BY-SA 4.0). You may copy, translate and extend it, including commercially, as long as you credit
the authors and keep derivative documentation under the same license. See [LICENSE](LICENSE) and
[NOTICE](NOTICE).

The **facts** described here are not owned by anyone. If you rewrite a specification in your own
words, you are not bound by this license — but a citation is what makes the record traceable, and it
is the only payment we ask for.

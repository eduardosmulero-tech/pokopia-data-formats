# Pokopia data formats

Written specifications for the on-disk data formats of **Pokémon Pokopia** (Nintendo Switch 2),
measured on a legally owned copy and released under CC BY-SA 4.0.

## Why this exists

There is no written specification for the game's data containers. Reading tools exist — notably
[PokoHex](https://github.com/berichan/PokoHex), a GPL-3.0 save editor — but the container layout, its
edge cases and the conditions for a byte-exact rebuild are not documented anywhere public.

This repository aims to be the **canonical, citable description**: field tables, invariants, the traps
that break a naive reader, and test vectors so anyone can validate their own implementation without
our code.

## Status

| Document | Format | State |
|---|---|---|
| [`docs/SPEC-CONTAINER.md`](docs/SPEC-CONTAINER.md) | `LD_C0_R.BIN` + `LI_C0_R.IDX` (12,298 entries) | revision 1 — published |

Everything here is measured against build **2.0.1a**. Formats change with game updates; each document
records the build it was measured on.

## What this repository is not

- **Not game data.** No assets, models, textures, audio, text dumps, keys, firmware or saves.
  `tools/check_repo.py` enforces this locally and in CI.
- **Not a tool.** Parsers and packers live in separate repositories.
- **Not affiliated** with Nintendo or with the authors of PokoHex.

## Verifying a document

Each specification states how its claims were measured and which command reproduces them. If you find
a number you cannot reproduce, that is a documentation bug: open an issue with the build id, the entry
id and the command you ran. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Documentation is licensed under **Creative Commons Attribution-ShareAlike 4.0 International**
(CC BY-SA 4.0). You may copy, translate and extend it, including commercially, as long as you credit
the authors and keep derivative documentation under the same license. See [LICENSE](LICENSE) and
[NOTICE](NOTICE).

The **facts** described here are not owned by anyone. If you rewrite a specification in your own
words, you are not bound by this license — but a citation is what makes the record traceable, and it
is the only payment we ask for.

# Contributing

Corrections are the most valuable thing you can send. Praise is not.

## Reporting a wrong number

Open an issue with all four of these:

1. **Build** the measurement was taken on (e.g. `2.0.1a`, update build `655360`).
2. **Where** in the document the claim is (`docs/SPEC-CONTAINER.md`, section, field).
3. **What you measured** instead.
4. **The command** that reproduces your measurement.

A claim without a reproducing command is an opinion. It may still be right, but it cannot replace a
measured one.

## What is welcome

- Corrections with a reproduction command.
- Additional test vectors (index, sizes, `sha256` of the decompressed payload) — never the payload.
- Translations. The license requires that a translation be released under CC BY-SA 4.0 as well, and
  that the original be credited.
- Notes about another build, clearly labelled with its build id.

## What is not welcome

- Game data of any kind: containers, indexes, assets, models, textures, audio, text dumps.
- Keys, tickets, certificates, firmware, save files.
- Instructions for obtaining any of the above.
- "It works on my machine" without a command.

`tools/check_repo.py` enforces the first two categories mechanically, locally and in CI. Run it before
opening a pull request:

```sh
python tools/check_repo.py
```

## Licensing of contributions

By contributing you agree that your text is released under CC BY-SA 4.0, the license of this
repository. You keep the copyright of what you write.

## Scope

This repository documents formats. It does not ship tools, and it does not take positions on how
anyone uses the formats. Requests to add binaries or bundled assets are closed without discussion.

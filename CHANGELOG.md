# Changelog

All notable changes to this repository are documented here. The format is
[Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) and the version follows
[Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html). Every document is tied to game
build 2.0.1a (update build 655360); a different build is a different claim.

## [Unreleased]

## [0.2.0] - 2026-11-09

### Added

- `docs/SPEC-FDATA.md` — the 24 `.fdata` archives (`PDRK`/`IDRK`): 79,710 entries, 25 types, the
  `u64` size trap, both chunk framings and the `.rdb` master index.
- `docs/SPEC-G1T.md` — `G1T` textures: 28-byte header, the 512 B per-level mip chain, the
  pixel-format census over 14,713 textures, the tile swizzle and what stays read-only.
- `docs/SPEC-G1M.md` — `G1M` models: the 12-byte wrapper, header, chunks, sections, vertex and
  index buffers, submesh counting, and what an external repacker changes.
- `docs/SPEC-G1A.md` — `G2A` animations (type `g1a`): 32-byte header, 10-bit bones, the timing
  section and its absolute padding, the quantised 32-byte key blocks and the invariant that closes
  the file.
- `docs/SPEC-TEXT.md` — the pointer-plus-pool text scheme shared by 2,409 container entries: the
  `a` field that is not a direct offset, the three substitution modes and the measured families.
- `docs/AUDIO.md` — sound banks `ASRS`/`KTSR`: the chunk walk with mixed endianness, the sound
  header field by field, the two codecs, the 462 external streams and the name obfuscation.
- `docs/AUDIO-KA1A.md` — the `KA1A` transform codec: frames, the 21 bands, the logarithmic code
  tables, the overlap window and the bitrate modes.
- `CHANGELOG.md`, this file.

### Changed

- `README.md` rewritten to the repository's publication standard: what it is and what it is not,
  a copyable quickstart with the expected output, the status table of all eight documents, the
  measured / not-measured / not-here lists, and the links to changelog, contribution, notice and
  licence.
- Each new specification carries a normative header: build, revision, the statement that no game
  content is reproduced, and the split between this documentation repository and the reference
  implementation (`pokopia-tools`, GPL-3.0).
- Relative links that only resolved inside `pokopia-tools` (`../README.md#supported-build`,
  `SPEC-NAMES.md`, `MOD-FORMAT.md`) now resolve here: the build is stated inline and the two
  documents that are not published in this repository are linked at their GPL copy.
- `AUDIO.md` §5 cites the `vgmstream` routine that documents the `KTSR` name obfuscation instead
  of repeating its generator constants. No key-shaped constant ships in this repository.

### Notes

- The name and description tables (`#4636`–`#4653`) are **not** published here yet: `SPEC-TEXT.md`
  §7 records an open discrepancy with §3.2 of that document, and publishing two specifications
  that contradict each other would be worse than publishing one fewer.

## [0.1.0] - 2026-11-03

### Added

- Repository scaffold: CC BY-SA 4.0 licence, `NOTICE`, `CONTRIBUTING.md`, `.gitignore` for game
  data and keys, `tools/check_repo.py` and the CI workflow that runs it.
- `docs/SPEC-CONTAINER.md` — revision 1 of the `LD_C0_R.BIN` / `LI_C0_R.IDX` container: 12,298
  entries, the 32-byte index record, both entry encodings, block framing, alignment and test
  vectors.

[Unreleased]: https://github.com/eduardosmulero-tech/pokopia-data-formats/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/eduardosmulero-tech/pokopia-data-formats/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/eduardosmulero-tech/pokopia-data-formats/releases/tag/v0.1.0

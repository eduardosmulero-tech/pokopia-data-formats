# v0.2.0 — seven data-format specifications, build 2.0.1a

Seven new specifications join the container document, all measured on game build **2.0.1a**
(update build 655360). This is a documentation release: no code, no assets, nothing from the game.

## Added

| Document | What it documents |
|---|---|
| [SPEC-FDATA.md](https://github.com/eduardosmulero-tech/pokopia-data-formats/blob/v0.2.0/docs/SPEC-FDATA.md) | The 24 `.fdata` archives (`PDRK`/`IDRK`): 79,710 entries, 25 types, the `u64` size trap, both chunk framings, the `.rdb` master index. |
| [SPEC-G1T.md](https://github.com/eduardosmulero-tech/pokopia-data-formats/blob/v0.2.0/docs/SPEC-G1T.md) | `G1T` textures: 28-byte header, the 512 B per-level mip chain, the pixel-format census over 14,713 textures, the tile swizzle. |
| [SPEC-G1M.md](https://github.com/eduardosmulero-tech/pokopia-data-formats/blob/v0.2.0/docs/SPEC-G1M.md) | `G1M` models: the 12-byte wrapper, header, chunks, sections, vertex and index buffers, submesh counting. |
| [SPEC-G1A.md](https://github.com/eduardosmulero-tech/pokopia-data-formats/blob/v0.2.0/docs/SPEC-G1A.md) | `G2A` animations (type `g1a`): 32-byte header, 10-bit bones, the timing section and its absolute padding, the quantised key blocks. |
| [SPEC-TEXT.md](https://github.com/eduardosmulero-tech/pokopia-data-formats/blob/v0.2.0/docs/SPEC-TEXT.md) | The pointer-plus-pool text scheme: 2,409 tables, the `a` field that is not a direct offset, three substitution modes. |
| [AUDIO.md](https://github.com/eduardosmulero-tech/pokopia-data-formats/blob/v0.2.0/docs/AUDIO.md) | Sound banks `ASRS`/`KTSR`: the chunk walk with mixed endianness, the sound header field by field, both codecs, the 462 external streams. |
| [AUDIO-KA1A.md](https://github.com/eduardosmulero-tech/pokopia-data-formats/blob/v0.2.0/docs/AUDIO-KA1A.md) | The `KA1A` transform codec: frames, 21 bands, the logarithmic code tables, the overlap window, the bitrate modes. |

Also in this release: [CHANGELOG.md](https://github.com/eduardosmulero-tech/pokopia-data-formats/blob/v0.2.0/CHANGELOG.md),
a rewritten [README](https://github.com/eduardosmulero-tech/pokopia-data-formats/blob/v0.2.0/README.md)
with the status of all eight documents, and `tools/build_release.py`, the deterministic builder for
the tarball attached here.

## Verify the download

```bash
sha256sum -c SHA256SUMS
tar -tzf pokopia-data-formats-v0.2.0.tar.gz | head
```

The tarball is the tracked tree at the tag: sorted names, fixed mtime and a gzip header with no
timestamp, so rebuilding it from the same commit gives the same sha256.

## State of the documentation

**Measured:** container record layout and both entry encodings; `.fdata` entry header and both
chunk framings; `G1T` header, mip alignment and swizzle; `G1M` header, chunks,
vertex/index/submesh sections; `G2A` header, bones, timing and key blocks; the pointer-plus-pool
text scheme; `ASRS`/`KTSR` chunk walk; `KA1A` frames, band tables and window.

**Not measured, and not claimed:** the 15 of 41 fields of the 68-byte item row whose meaning is
unknown; which bit means what in the save catalogue bitmap; `G1M` material, shader, palette and
socket sections; 641 `G1T` textures whose mip chain is unexplained; 22 BC6H textures with no
encoder; the row → entity mapping of the narrative text tables; the description-table geometry that
`SPEC-TEXT.md` §7 disputes.

**Not published yet:** the name and description tables (`#4636`–`#4653`), because of that open
discrepancy. It is stated here so that the gap is expected rather than discovered.

## Licence

Documentation: **CC BY-SA 4.0**. The reference implementation (`pokopia-tools`) is **GPL-3.0** and
lives in a different repository; nothing from it is relicensed here. No game assets, text, saves or
keys are distributed in this release.

<!-- CI: sustituir por la URL del run verde del commit etiquetado antes de publicar. -->

# Third-party notices

`neocard` itself is MIT licensed – see [LICENSE](LICENSE). It bundles and
redistributes third-party font software, listed below with the licenses that
apply to it.

## Bundled font file

[`neocard/assets/JetBrainsMonoNF.woff2`](neocard/assets/JetBrainsMonoNF.woff2)
is JetBrains Mono 2.304 patched by Nerd Fonts 3.4.0 (`JetBrainsMono NFM`). The
generated cards embed a subset of this file as a base64 `@font-face`, so every
card is itself a redistribution: the subsetter keeps the copyright, license and
license-URL records (name IDs 0, 13 and 14) inside the embedded font.

Nerd Fonts distributes its patched fonts under the SIL Open Font License 1.1,
so that license governs this file as a whole. Its full text is in
[`neocard/assets/OFL.txt`](neocard/assets/OFL.txt), carrying the copyright line
of the upstream authors.

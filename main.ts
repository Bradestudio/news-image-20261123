// news-image-20261123 — "Sum up 23 November's world news in one image".
//
// The front page is rendered ahead of time by render.py (PIL) and stored
// as entry.png next to this file. This program is the entry point the
// make.fun kit runs: it copies that image, byte for byte, to
// $MAKEFUN_OUTPUT_DIR/entry.png. No network, no randomness, no clock —
// two runs always produce the same file.
import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const MAX_BYTES = 1048576;
const MAX_DIM = 1024;
const PNG_SIGNATURE = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);

const outDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "/output");
const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const dest = join(outDir, "entry.png");

// Validate the bundled image before publishing it: real PNG signature,
// dimensions from the IHDR chunk, and the 1 MiB size cap.
const bytes = readFileSync(source);
if (!bytes.subarray(0, 8).equals(PNG_SIGNATURE)) {
  throw new Error("entry.png is not a PNG file");
}
if (bytes.length > MAX_BYTES) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB cap`);
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > MAX_DIM || height > MAX_DIM) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 cap`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, dest);
const written = statSync(dest).size;

// Verify the copy landed intact: the output hash must match the source.
const want = createHash("sha256").update(bytes).digest("hex");
const got = createHash("sha256").update(readFileSync(dest)).digest("hex");
if (want !== got) {
  throw new Error(`output hash mismatch: ${got} != ${want}`);
}
console.log(`wrote ${dest} (${width}x${height}, ${written} bytes)`);
console.log(`sha256 ${got}`);

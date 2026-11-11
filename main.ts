// Cutest Cat entry (cutest-cat-01): a ginger kitten with big bright eyes,
// a head tilt, and a red yarn ball, drawn procedurally by draw_cat.py
// (Pillow, build time only) into entry.png beside this file.
// The program itself draws nothing at run time: it only copies the image,
// so both grader runs write byte-identical output with no network.
// Node 22, standard library only: copy the image to /output/entry.png.
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(new URL('./entry.png', import.meta.url), join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));

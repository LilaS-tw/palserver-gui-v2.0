#!/usr/bin/env node
// /map viewer 頁需要的底圖/地標素材,單一素材來源是 packages/web/public(GUI 本體也用同一份)。
// 這支腳本在 dev/build 前(見 package.json 的 predev/prebuild)把需要的檔案複製到
// website/public/map-assets/ —— 該目錄不進 git(.gitignore),每次都是新複製的。
//
// 為什麼不讓 Next.js 直接讀 ../packages/web/public:App Router 靜態匯出只會打包
// public/ 底下的檔案,跨套件路徑無法被 next build 收進 out/,所以用複製而非引用。
//
// 若 build 環境(例如 Zeabur 用「Root Directory: website」的沙盒)沒有 sibling
// packages/ 目錄,這支腳本會印警告後直接結束(exit 0),不讓行銷首頁的 build 因此失敗
// —— 代價是 /map 頁的底圖/地標會缺檔。若實測發現 Zeabur 確實拿不到 ../packages,
// 改成把這些檔案直接複製進 website/public/map-assets/ 並提交進 git(不再靠這支腳本)。
import { existsSync, mkdirSync, copyFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SRC_ROOT = path.resolve(__dirname, '../../packages/web/public');
const DEST_ROOT = path.resolve(__dirname, '../public/map-assets');

/** [來源(相對 packages/web/public), 目的地(相對 map-assets/)] */
const FILES = [
  ['palworld-full-map.jpg', 'palworld-full-map.jpg'],
  ['worldtree-map.webp', 'worldtree-map.webp'],
  ['game-data/landmarks.json', 'landmarks.json'],
  ['game-data/worldtree-landmarks.json', 'worldtree-landmarks.json'],
  ['game-data/landmark-icons/fasttravel.png', 'landmark-icons/fasttravel.png'],
  ['game-data/landmark-icons/tower.png', 'landmark-icons/tower.png'],
  ['game-data/landmark-icons/palbox.webp', 'landmark-icons/palbox.webp'],
];

if (!existsSync(SRC_ROOT)) {
  console.warn(
    `[copy-map-assets] 找不到 ${SRC_ROOT} —— 這個環境沒有 monorepo 的 packages/,略過複製。\n` +
      '[copy-map-assets] /map 頁的底圖/地標會缺檔;其餘頁面不受影響。',
  );
  process.exit(0);
}

let ok = 0;
for (const [rel, destRel] of FILES) {
  const from = path.join(SRC_ROOT, rel);
  const to = path.join(DEST_ROOT, destRel);
  if (!existsSync(from)) {
    console.warn(`[copy-map-assets] 缺檔,略過: ${rel}`);
    continue;
  }
  mkdirSync(path.dirname(to), { recursive: true });
  copyFileSync(from, to);
  ok++;
}
console.log(`[copy-map-assets] 複製 ${ok}/${FILES.length} 個檔案到 ${DEST_ROOT}`);

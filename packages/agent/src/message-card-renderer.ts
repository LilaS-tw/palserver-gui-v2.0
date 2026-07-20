import { execFile } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { promisify } from "node:util";
import type { MessageBridgeLanguage } from "@palserver/shared";

const execFileP = promisify(execFile);

interface RendererOutput { files: string[] }

function gameDataDir(): string | undefined {
  const installDir = path.dirname(process.execPath);
  const candidates = [
    process.env.PALSERVER_WEB_DIR ? path.join(process.env.PALSERVER_WEB_DIR, "game-data") : "",
    path.join(installDir, "web", "game-data"),
    path.resolve(process.cwd(), "packages", "web", "dist", "game-data"),
    path.resolve(process.cwd(), "packages", "web", "public", "game-data"),
    path.resolve(process.cwd(), "..", "web", "public", "game-data"),
  ];
  return candidates.find((candidate) => fs.existsSync(path.join(candidate, "pals.json")));
}

function rendererCommand(): { command: string; args: string[] } {
  const configured = process.env.PALSERVER_MESSAGE_RENDERER?.trim();
  if (configured) return { command: configured, args: [] };

  const executableName = process.platform === "win32" ? "bridge-card-renderer.exe" : "bridge-card-renderer";
  const installDir = path.dirname(process.execPath);
  const executable = [
    path.join(installDir, executableName),
    path.join(installDir, "bridge-card-renderer", executableName),
    path.join(installDir, "web", ".bridge-card-renderer", executableName),
    process.env.PALSERVER_WEB_DIR ? path.join(process.env.PALSERVER_WEB_DIR, ".bridge-card-renderer", executableName) : "",
  ].find((candidate) => fs.existsSync(candidate));
  if (executable) return { command: executable, args: [] };

  const script = [
    path.resolve(process.cwd(), "scripts", "message-card-renderer.py"),
    path.resolve(process.cwd(), "..", "..", "scripts", "message-card-renderer.py"),
  ].find((candidate) => fs.existsSync(candidate));
  if (script) {
    return { command: process.env.PYTHON?.trim() || (process.platform === "win32" ? "python" : "python3"), args: [script] };
  }
  throw new Error("找不到群服互通图片渲染器");
}

export async function renderMessageBridgeCards(pages: readonly string[], language: MessageBridgeLanguage): Promise<Buffer[]> {
  if (!pages.length) throw new Error("没有可渲染的群消息内容");
  const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), "palserver-message-card-"));
  const input = path.join(tempDir, "input.json");
  const output = path.join(tempDir, "output");
  try {
    fs.writeFileSync(input, JSON.stringify({ pages, language, gameDataDir: gameDataDir() }));
    const renderer = rendererCommand();
    const result = await execFileP(renderer.command, [...renderer.args, input, output], {
      encoding: "utf8",
      maxBuffer: 1024 * 1024,
      timeout: 90_000,
      windowsHide: true,
    });
    const parsed = JSON.parse(result.stdout.trim()) as RendererOutput;
    if (!Array.isArray(parsed.files) || parsed.files.length !== 1) throw new Error("图片渲染器必须且只能返回一张图片");
    return parsed.files.map((name) => {
      const safe = path.basename(name);
      if (safe !== name || !safe.endsWith(".png")) throw new Error("图片渲染器返回了无效文件名");
      return fs.readFileSync(path.join(output, safe));
    });
  } finally {
    fs.rmSync(tempDir, { recursive: true, force: true });
  }
}

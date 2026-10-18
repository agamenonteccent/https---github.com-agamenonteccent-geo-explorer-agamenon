import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtempSync, readdirSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const pasta = mkdtempSync(join(tmpdir(), "geo-build-"));
const cli = fileURLToPath(new URL("../dist/cli.js", import.meta.url));
const client = new Client({ name: "geo-build-check", version: "1.0.0" });
try {
  for (const args of [
    ["/trilhas"],
    ["/trilha", "Geotecnologias"],
    ["/desafio", "Data Science", "Básico"],
    ["/certificado", "Agamenon", "Geotecnologias"]
  ]) {
    const resultado = spawnSync(process.execPath, [cli, ...args], {
      cwd: pasta, env: { ...process.env, GEO_CERTIFICADOS_DIR: pasta },
      encoding: "utf8", timeout: 15000
    });
    assert.equal(resultado.status, 0, resultado.stderr || resultado.stdout);
    assert.ok(resultado.stdout.length > 0);
  }
  assert.equal(readdirSync(pasta).length, 1);
  await client.connect(new StdioClientTransport({
    command: process.execPath,
    args: [fileURLToPath(new URL("../dist/mcp/server.js", import.meta.url))],
    cwd: pasta
  }));
  const resposta = await client.callTool({ name: "consultar_trilha", arguments: { tecnologia: "Geotecnologias" } });
  assert.notEqual(resposta.isError, true);
  assert.match(JSON.stringify(resposta), /GeoJSON/);
  console.log("Build verificado: CLI, certificado e MCP executados de outra pasta.");
} finally {
  await client.close();
  rmSync(pasta, { recursive: true, force: true });
}

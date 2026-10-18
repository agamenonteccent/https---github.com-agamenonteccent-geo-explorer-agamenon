import { fileURLToPath } from "node:url";
import { mkdtempSync, readdirSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

describe("Servidor MCP por stdio", () => {
  it("descobre e executa as quatro ferramentas, valida entradas e trata erros", async () => {
    const pasta = mkdtempSync(join(tmpdir(), "geo-mcp-"));
    const client = new Client({ name: "geo-explorer-tests", version: "1.0.0" });
    const env = Object.fromEntries(Object.entries(process.env).filter((e): e is [string, string] => e[1] !== undefined));
    const transport = new StdioClientTransport({
      command: process.execPath,
      args: ["--import", "tsx", fileURLToPath(new URL("../src/mcp/server.ts", import.meta.url))],
      cwd: fileURLToPath(new URL("../", import.meta.url)),
      env: { ...env, GEO_CERTIFICADOS_DIR: pasta }
    });
    try {
      await client.connect(transport);
      const lista = await client.listTools();
      expect(lista.tools.map(t => t.name).sort()).toEqual([
        "consultar_trilha", "gerar_certificado", "gerar_desafio", "listar_trilhas"
      ]);
      for (const [name, args, trecho] of [
        ["listar_trilhas", {}, "Geotecnologias"],
        ["consultar_trilha", { tecnologia: "Python" }, "Expedição Python"],
        ["gerar_desafio", { tecnologia: "Geotecnologias", nivel: "Básico" }, "Validador de coordenadas"],
        ["gerar_certificado", { nome: "Agamenon", tecnologia: "Data Science" }, "Certificado fictício"]
      ] as const) {
        const resposta = await client.callTool({ name, arguments: args });
        expect(resposta.isError).not.toBe(true);
        expect(JSON.stringify(resposta)).toContain(trecho);
      }
      const arquivos = readdirSync(pasta);
      expect(arquivos).toHaveLength(1);
      expect(readFileSync(join(pasta, arquivos[0]), "utf8")).toContain("Agamenon");
      const erro = await client.callTool({ name: "consultar_trilha", arguments: { tecnologia: "Inexistente" } });
      expect(erro.isError).toBe(true);
      const invalido = await client.callTool({ name: "gerar_certificado", arguments: { nome: "", tecnologia: "Python" } });
      expect(invalido.isError).toBe(true);
      expect(readdirSync(pasta)).toHaveLength(1);
    } finally {
      await client.close();
      rmSync(pasta, { recursive: true, force: true });
    }
  }, 30000);
});

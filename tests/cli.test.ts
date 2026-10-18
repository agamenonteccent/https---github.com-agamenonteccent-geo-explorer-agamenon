import { spawnSync } from "node:child_process";
import { mkdtempSync, readFileSync, readdirSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { describe, it, expect } from "vitest";

const cli = fileURLToPath(new URL("../src/cli.ts", import.meta.url));
function executar(args: string[], pasta?: string) {
  return spawnSync(process.execPath, ["--import", "tsx", cli, ...args], {
    encoding: "utf8", timeout: 15000,
    env: { ...process.env, ...(pasta ? { GEO_CERTIFICADOS_DIR: pasta } : {}) }
  });
}

describe("CLI em processo real", () => {
  it("consulta tecnologia composta", () => {
    const resultado = executar(["/desafio", "Data Science", "Intermediário"]);
    expect(resultado.status).toBe(0);
    expect(resultado.stdout).toContain("Tecnologia: Data Science");
    expect(resultado.stderr).toBe("");
  });
  it("retorna código 1 para tecnologia inexistente", () => {
    const resultado = executar(["/trilha", "inexistente"]);
    expect(resultado.status).toBe(1);
    expect(resultado.stdout).toContain("Nenhuma trilha encontrada");
  });
  it("emite certificado com nome simples, composto e aspas literais", () => {
    const pasta = mkdtempSync(join(tmpdir(), "geo-cli-"));
    try {
      for (const nome of ["Agamenon", "Agamenon da Silva", 'Agamenon "Geo"']) {
        const resultado = executar(["/certificado", nome, "Data Science"], pasta);
        expect(resultado.status).toBe(0);
        expect(resultado.stdout).toContain(nome);
      }
      const arquivos = readdirSync(pasta);
      expect(arquivos).toHaveLength(3);
      expect(readFileSync(join(pasta, arquivos[0]), "utf8")).toContain("sem validade acadêmica");
    } finally {
      rmSync(pasta, { recursive: true, force: true });
    }
  });
});

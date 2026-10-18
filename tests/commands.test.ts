import {
  afterEach, beforeEach, describe, expect, it
} from "vitest";
import {
  mkdtempSync, readdirSync, readFileSync, rmSync
} from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import processarComando, {
  executarComandoCertificado,
  executarComandoDesafio,
  executarComandoTrilha,
  separarArgumentos
} from "../src/commands/index.js";
import {
  desafios, normalizar, trilhas
} from "../src/core.js";

let pasta: string;
let anterior: string | undefined;

beforeEach(() => {
  pasta = mkdtempSync(join(tmpdir(), "geo-explorer-"));
  anterior = process.env.GEO_CERTIFICADOS_DIR;
  process.env.GEO_CERTIFICADOS_DIR = pasta;
});

afterEach(() => {
  if (anterior === undefined) delete process.env.GEO_CERTIFICADOS_DIR;
  else process.env.GEO_CERTIFICADOS_DIR = anterior;
  rmSync(pasta, { recursive: true, force: true });
});

describe("Base fictícia", () => {
  it("possui IDs únicos e desafios relacionados às trilhas", () => {
    expect(new Set(trilhas.map(t => t.id)).size).toBe(trilhas.length);
    expect(new Set(desafios.map(d => d.id)).size).toBe(desafios.length);
    for (const desafio of desafios) {
      expect(trilhas.some(t =>
        t.tecnologia === desafio.tecnologia
      )).toBe(true);
    }
  });

  it("oferece três níveis para cada tecnologia", () => {
    for (const trilha of trilhas) {
      const niveis = new Set(
        desafios.filter(d => d.tecnologia === trilha.tecnologia)
          .map(d => d.nivel)
      );
      expect(niveis.size).toBe(3);
    }
  });
});

describe("Trilhas", () => {
  it("consulta tecnologia e fases", () => {
    const resultado = executarComandoTrilha("python");
    expect(resultado).toContain("Expedição Python");
    expect(resultado).toContain("Fase 3");
  });

  it("normaliza acentos", () => {
    expect(normalizar(" BÁSICO ")).toBe("basico");
  });

  it("rejeita consultas vazias e inexistentes", () => {
    expect(() => executarComandoTrilha("")).toThrow();
    expect(() => executarComandoTrilha("Inexistente")).toThrow();
  });
});

describe("Desafios", () => {
  it("filtra pelo nível ignorando acentos e maiúsculas", () => {
    const resultado = executarComandoDesafio("Python", "basico");
    expect(resultado).toContain("Nível: Básico");
    expect(resultado).toContain("Requisitos");
    expect(resultado).toContain("Saída esperada");
  });

  it("funciona sem nível", () => {
    expect(executarComandoDesafio("React")).toContain("Tecnologia: React");
  });

  it("rejeita nível inválido", () => {
    expect(() => executarComandoDesafio("Python", "Especialista"))
      .toThrow("Nível inválido");
  });
});

describe("Certificados", () => {
  it("gera arquivos distintos e avisa sobre a natureza fictícia", () => {
    executarComandoCertificado("Agamenon", "Python");
    executarComandoCertificado("Agamenon", "Python");
    const arquivos = readdirSync(pasta);
    expect(arquivos).toHaveLength(2);
    expect(arquivos[0]).not.toBe(arquivos[1]);

    const texto = readFileSync(join(pasta, arquivos[0]), "utf8");
    expect(texto).toContain("Agamenon");
    expect(texto).toContain("não verifica a conclusão");
    expect(arquivos[0]).toMatch(
      /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\.md$/
    );
  });

  it("valida nome vazio e tecnologia inexistente", () => {
    expect(() => executarComandoCertificado(" ", "Python")).toThrow();
    expect(() => executarComandoCertificado("Agamenon", "Inexistente")).toThrow();
    expect(readdirSync(pasta)).toHaveLength(0);
  });

  it("não usa o nome como caminho de arquivo", () => {
    executarComandoCertificado("../../<script>Agamenon</script>", "Python");
    const arquivos = readdirSync(pasta);
    expect(arquivos).toHaveLength(1);
    const texto = readFileSync(join(pasta, arquivos[0]), "utf8");
    expect(texto).not.toContain("<script>");
  });
});

describe("Processador", () => {
  it("preserva nomes compostos e argumentos vazios", () => {
    expect(separarArgumentos('/desafio "Data Science" Básico'))
      .toEqual(["/desafio", "Data Science", "Básico"]);
    expect(separarArgumentos('/certificado "" "Python"'))
      .toEqual(["/certificado", "", "Python"]);
  });

  it("rejeita aspas não fechadas", () => {
    expect(processarComando('/trilha "Python')).toContain("Aspas não fechadas");
  });

  it("rejeita certificado com argumentos extras", () => {
    expect(processarComando("/certificado Agamenon da Silva Python")).toContain("Erro:");
  });

  it("processa certificado completo", () => {
    expect(processarComando('/certificado "Agamenon" "Python"'))
      .toContain("Certificado fictício");
  });

  it("aceita tecnologia composta", () => {
    expect(processarComando('/desafio "Data Science" Básico'))
      .toContain("Tecnologia: Data Science");
  });

  it("apresenta ajuda e informa comando desconhecido", () => {
    expect(processarComando("/help")).toContain("/trilha");
    expect(processarComando("/inexistente")).toContain("Erro:");
  });
});

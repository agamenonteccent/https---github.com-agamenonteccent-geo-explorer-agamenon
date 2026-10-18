import { describe, expect, it } from "vitest";
import { trilhas, desafios, validarBase, textoSeguro } from "../src/core.js";
import processarComando, { executarArgumentos } from "../src/commands/index.js";

describe("Validação da base", () => {
  it("rejeita IDs de trilha duplicados", () => {
    expect(() => validarBase([...trilhas, trilhas[0]], desafios)).toThrow("IDs duplicados");
  });
  it("rejeita IDs de desafio duplicados", () => {
    expect(() => validarBase(trilhas, [...desafios, desafios[0]])).toThrow("IDs duplicados");
  });
  it("rejeita desafios sem tecnologia correspondente", () => {
    expect(() => validarBase(trilhas, [{ ...desafios[0], tecnologia: "Outra" }])).toThrow("sem trilha");
  });
  it("rejeita carga horária negativa e fases fora de sequência", () => {
    expect(() => validarBase([{ ...trilhas[0], horas: -1 }], desafios)).toThrow();
    expect(() => validarBase([{ ...trilhas[0], modulos: [{ fase: 2, titulo: "Teste" }] }], desafios)).toThrow("Fases fora de sequência");
  });
});

describe("Melhorias do Agamenon", () => {
  it("lista todas as tecnologias e rejeita argumentos extras", () => {
    const resultado = processarComando("/trilhas");
    for (const trilha of trilhas) expect(resultado).toContain(trilha.tecnologia);
    expect(processarComando("/trilhas Python")).toContain("Erro:");
  });
  it("consulta geotecnologias e seus três desafios", () => {
    expect(processarComando("/trilha geotecnologias")).toContain("GeoJSON");
    for (const nivel of ["basico", "intermediario", "avancado"]) {
      expect(processarComando(`/desafio Geotecnologias ${nivel}`)).toContain("Saída esperada");
    }
  });
  it("rejeita consultas ambíguas para emissão e desafio", () => {
    expect(processarComando('/certificado "Agamenon" "Expedição"')).toContain("ambígua");
    expect(processarComando('/desafio "Expedição"')).toContain("ambígua");
  });
  it("preserva argumento composto do shell", () => {
    expect(executarArgumentos(["/desafio", "Data Science", "Básico"])).toContain("Tecnologia: Data Science");
  });
  it("escapa HTML, links e formatação Markdown no nome", () => {
    expect(textoSeguro('<script>&[link](url)*\n')).toBe('&lt;script&gt;&amp;\\[link\\]\\(url\\)\\* ');
  });
});

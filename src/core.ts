import { readFileSync } from "node:fs";
import { z } from "zod";

const moduloSchema = z.object({
  fase: z.number().int().positive(),
  titulo: z.string().min(1)
});

export const trilhaSchema = z.object({
  id: z.string().min(1),
  tecnologia: z.string().min(1),
  nome: z.string().min(1),
  nivel: z.enum(["Básico", "Intermediário", "Avançado"]),
  horas: z.number().positive(),
  modulos: z.array(moduloSchema).min(1),
  competencias: z.array(z.string().min(1)).min(1)
});

export const desafioSchema = z.object({
  id: z.string().min(1),
  tecnologia: z.string().min(1),
  nivel: z.enum(["Básico", "Intermediário", "Avançado"]),
  titulo: z.string().min(1),
  descricao: z.string().min(1),
  requisitos: z.array(z.string()),
  dicas: z.array(z.string()),
  entrada: z.string(),
  saida: z.string(),
  xp: z.number().int().positive()
});

function lerJSON(arquivo: string): unknown {
  const url = new URL(`../data/${arquivo}`, import.meta.url);
  return JSON.parse(readFileSync(url, "utf8"));
}

export function validarBase(dadosTrilhas: unknown, dadosDesafios: unknown) {
  const trilhas = z.array(trilhaSchema).min(1).parse(dadosTrilhas);
  const desafios = z.array(desafioSchema).min(1).parse(dadosDesafios);
  for (const [nome, itens] of [["trilhas", trilhas], ["desafios", desafios]] as const) {
    if (new Set(itens.map(item => item.id)).size !== itens.length) {
      throw new Error(`IDs duplicados na base de ${nome}.`);
    }
  }
  if (new Set(trilhas.map(t => normalizar(t.tecnologia))).size !== trilhas.length) {
    throw new Error("Tecnologias duplicadas na base de trilhas.");
  }
  for (const trilha of trilhas) {
    if (trilha.modulos.some((m, i) => m.fase !== i + 1)) {
      throw new Error(`Fases fora de sequência: ${trilha.id}.`);
    }
  }
  for (const desafio of desafios) {
    if (!trilhas.some(t => normalizar(t.tecnologia) === normalizar(desafio.tecnologia))) {
      throw new Error(`Desafio sem trilha: ${desafio.id}.`);
    }
  }
  return { trilhas, desafios };
}

export const { trilhas, desafios } = validarBase(lerJSON("trilhas.json"), lerJSON("desafios.json"));
export const niveis = ["Básico", "Intermediário", "Avançado"] as const;

export function normalizar(valor: string): string {
  return valor.normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .trim();
}

export function buscarTrilhas(tecnologia: string) {
  const termo = normalizar(tecnologia);
  if (!termo) return [];

  const exatas = trilhas.filter(t =>
    normalizar(t.tecnologia) === termo || normalizar(t.id) === termo
  );

  return exatas.length ? exatas : trilhas.filter(t =>
    normalizar(t.nome).includes(termo)
  );
}

export function selecionarTrilha(tecnologia: string) {
  if (!tecnologia.trim()) throw new Error("Informe a tecnologia.");

  const encontradas = buscarTrilhas(tecnologia);
  if (!encontradas.length) {
    throw new Error(`Nenhuma trilha encontrada para "${tecnologia}".`);
  }
  if (encontradas.length > 1) {
    throw new Error("Busca ambígua. Informe a tecnologia ou o ID exato.");
  }
  return encontradas[0];
}

export function textoSeguro(valor: string): string {
  return valor
    .replace(/[\r\n\t]+/g, " ")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/([\\`*_{}\[\]()|#!])/g, "\\$1");
}

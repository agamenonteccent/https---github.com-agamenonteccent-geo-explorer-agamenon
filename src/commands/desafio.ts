import { randomInt } from "node:crypto";
import {
  desafios, niveis, normalizar, selecionarTrilha
} from "../core.js";

export function executarComandoDesafio(
  tecnologia: string,
  nivel?: string
): string {
  const trilha = selecionarTrilha(tecnologia);

  if (nivel !== undefined &&
      !niveis.some(n => normalizar(n) === normalizar(nivel))) {
    throw new Error("Nível inválido. Use Básico, Intermediário ou Avançado.");
  }

  const candidatos = desafios.filter(d =>
    normalizar(d.tecnologia) === normalizar(trilha.tecnologia) &&
    (nivel === undefined || normalizar(d.nivel) === normalizar(nivel))
  );

  if (!candidatos.length) {
    throw new Error("Nenhum desafio disponível para esse filtro.");
  }

  const d = candidatos[randomInt(candidatos.length)];

  return [
    `# Desafio: ${d.titulo}`,
    "",
    `- Tecnologia: ${d.tecnologia}`,
    `- Nível: ${d.nivel}`,
    `- Recompensa fictícia: ${d.xp} XP`,
    "",
    "## Descrição", d.descricao,
    "",
    "## Requisitos", ...d.requisitos.map(r => `- ${r}`),
    "",
    "## Dicas", ...d.dicas.map(item => `- ${item}`),
    "",
    "## Entrada de exemplo", d.entrada,
    "",
    "## Saída esperada", d.saida
  ].join("\n");
}

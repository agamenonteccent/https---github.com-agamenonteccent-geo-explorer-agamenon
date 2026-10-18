import { buscarTrilhas, textoSeguro } from "../core.js";

export function executarComandoTrilha(tecnologia: string): string {
  if (!tecnologia.trim()) throw new Error("Uso: /trilha <tecnologia>");

  const encontradas = buscarTrilhas(tecnologia);
  if (!encontradas.length) {
    throw new Error(`Nenhuma trilha encontrada para "${tecnologia}".`);
  }

  return encontradas.map(t => [
    `# Plano de estudos: ${t.nome}`,
    "",
    `- Tecnologia: ${t.tecnologia}`,
    `- Nível: ${t.nivel}`,
    `- Carga horária fictícia: ${t.horas} horas`,
    "",
    ...t.modulos.flatMap(m => [
      `## Fase ${m.fase}`,
      `- ${m.titulo}`,
      ""
    ]),
    "## Competências",
    ...t.competencias.map(c => `- ${c}`),
    "",
    `Próximo passo: /desafio "${textoSeguro(t.tecnologia)}"`,
    "",
    "Dados fictícios para fins educacionais."
  ].join("\n")).join("\n\n---\n\n");
}

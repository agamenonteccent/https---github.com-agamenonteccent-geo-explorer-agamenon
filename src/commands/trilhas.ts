import { trilhas } from "../core.js";

export function executarComandoTrilhas(): string {
  return [
    "# Geo-Explorer do Agamenon — Trilhas disponíveis",
    "",
    ...trilhas.map(t => `- ${t.tecnologia} (${t.id}) · ${t.nivel} · ${t.horas} horas · ${t.modulos.length} módulos`),
    "",
    'Próximo passo: /trilha "<tecnologia>"',
    "Dados fictícios para fins educacionais."
  ].join("\n");
}

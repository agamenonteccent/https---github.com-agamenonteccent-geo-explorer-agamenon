import { randomUUID } from "node:crypto";
import { mkdirSync, writeFileSync } from "node:fs";
import { resolve, join } from "node:path";
import { selecionarTrilha, textoSeguro } from "../core.js";

export function executarComandoCertificado(
  nome: string,
  tecnologia: string,
  diretorio = process.env.GEO_CERTIFICADOS_DIR ??
    "docs/certificados-emitidos"
): string {
  const estudante = nome.trim();
  if (!estudante || estudante.length > 120) {
    throw new Error("Informe um nome entre 1 e 120 caracteres.");
  }

  const trilha = selecionarTrilha(tecnologia);
  const codigo = randomUUID();
  const pasta = resolve(diretorio);
  const arquivo = join(pasta, `${codigo}.md`);

  const conteudo = [
    "# Certificado fictício",
    "Geo-Explorer do Agamenon",
    "",
    `Participante: **${textoSeguro(estudante)}**`,
    `Trilha: **${trilha.nome}**`,
    `Tecnologia: ${trilha.tecnologia}`,
    `Carga horária fictícia: ${trilha.horas} horas`,
    `Data de emissão: ${new Date().toISOString()}`,
    `Identificador: ${codigo}`,
    "",
    "## Competências previstas",
    ...trilha.competencias.map(c => `- ${c}`),
    "",
    "---",
    "Documento de demonstração, sem validade acadêmica ou profissional.",
    "O sistema não verifica a conclusão da trilha.",
    "O identificador não comprova autenticidade externa."
  ].join("\n\n");

  mkdirSync(pasta, { recursive: true });
  writeFileSync(arquivo, conteudo, { encoding: "utf8", flag: "wx" });

  return `${conteudo}\n\nArquivo salvo: ${arquivo}`;
}

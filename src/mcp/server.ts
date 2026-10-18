import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import {
  executarComandoTrilha,
  executarComandoDesafio,
  executarComandoCertificado,
  executarComandoTrilhas
} from "../commands/index.js";

const server = new McpServer({
  name: "geo-explorer",
  version: "1.0.0"
});

function responder(acao: () => string) {
  try {
    return {
      content: [{ type: "text" as const, text: acao() }]
    };
  } catch (erro) {
    return {
      isError: true,
      content: [{
        type: "text" as const,
        text: erro instanceof Error ? erro.message : "Falha inesperada."
      }]
    };
  }
}

server.tool(
  "listar_trilhas",
  "Lista as tecnologias fictícias disponíveis no Geo-Explorer do Agamenon.",
  {},
  async () => responder(() => executarComandoTrilhas())
);

server.tool(
  "consultar_trilha",
  "Consulta um plano fictício de aprendizagem.",
  { tecnologia: z.string().trim().min(1) },
  async ({ tecnologia }) =>
    responder(() => executarComandoTrilha(tecnologia))
);

server.tool(
  "gerar_desafio",
  "Seleciona um desafio da base fictícia.",
  {
    tecnologia: z.string().trim().min(1),
    nivel: z.enum(["Básico", "Intermediário", "Avançado"]).optional()
  },
  async ({ tecnologia, nivel }) =>
    responder(() => executarComandoDesafio(tecnologia, nivel))
);

server.tool(
  "gerar_certificado",
  "Grava um certificado fictício local; não verifica conclusão.",
  {
    nome: z.string().trim().min(1).max(120),
    tecnologia: z.string().trim().min(1)
  },
  async ({ nome, tecnologia }) =>
    responder(() => executarComandoCertificado(nome, tecnologia))
);

async function main() {
  await server.connect(new StdioServerTransport());
}

main().catch(erro => {
  // stdout é reservado ao protocolo MCP.
  console.error(erro);
  process.exitCode = 1;
});

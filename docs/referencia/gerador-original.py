from pathlib import Path
import json
import textwrap
import zipfile

ROOT = Path("geo-explorer")

if ROOT.exists():
    raise SystemExit(
        "A pasta geo-explorer já existe. Renomeie-a antes de executar "
        "para não perder arquivos."
    )

files = {}

files["package.json"] = json.dumps({
    "name": "geo-explorer",
    "version": "1.0.0",
    "private": True,
    "type": "module",
    "description": "Exploração de trilhas fictícias com CLI, testes e MCP.",
    "engines": {"node": ">=22"},
    "scripts": {
        "dev": "tsx src/cli.ts",
        "exemplo": "tsx src/cli.ts /trilha Python",
        "typecheck": "tsc --noEmit",
        "build": "tsc",
        "start": "node dist/cli.js",
        "test": "vitest run",
        "test:watch": "vitest",
        "mcp": "tsx src/mcp/server.ts",
        "mcp:start": "node dist/mcp/server.js"
    },
    "dependencies": {
        "@modelcontextprotocol/sdk": "^1.12.0",
        "zod": "^3.25.0"
    },
    "devDependencies": {
        "@types/node": "^22.15.0",
        "tsx": "^4.19.0",
        "typescript": "^5.8.0",
        "vitest": "^3.1.0"
    }
}, indent=2, ensure_ascii=False)

files["tsconfig.json"] = json.dumps({
    "compilerOptions": {
        "target": "ES2022",
        "module": "NodeNext",
        "moduleResolution": "NodeNext",
        "rootDir": "src",
        "outDir": "dist",
        "strict": True,
        "esModuleInterop": True,
        "skipLibCheck": True,
        "forceConsistentCasingInFileNames": True
    },
    "include": ["src/**/*.ts"],
    "exclude": ["node_modules", "dist", "tests"]
}, indent=2)

files[".gitignore"] = """
node_modules/
dist/
coverage/
.env
.env.*
!.env.example
*.log
.DS_Store
docs/certificados-emitidos/*
!docs/certificados-emitidos/.gitkeep
"""

files[".env.example"] = """
# Nenhum token é necessário para executar este projeto.
# Variável opcional para escolher a pasta dos certificados:
# GEO_CERTIFICADOS_DIR=./docs/certificados-emitidos
# O projeto não carrega este arquivo automaticamente.
"""

files["docs/certificados-emitidos/.gitkeep"] = ""

technologies = [
    ("Python", "python", "Básico", 25,
     ["Sintaxe e variáveis", "Coleções e funções", "Aplicação de terminal"]),
    ("JavaScript", "javascript", "Básico", 30,
     ["Tipos e funções", "Objetos e assincronismo", "Aplicação com testes"]),
    ("TypeScript", "typescript", "Intermediário", 28,
     ["Tipos e interfaces", "Generics e validação", "CLI tipada"]),
    ("React", "react", "Intermediário", 32,
     ["Componentes e propriedades", "Estado e efeitos", "Interface acessível"]),
    ("Data Science", "data-science", "Intermediário", 35,
     ["Preparação dos dados", "Análise exploratória", "Relatório reproduzível"])
]

tracks = []
challenges = []

for technology, slug, level, hours, modules in technologies:
    tracks.append({
        "id": slug,
        "tecnologia": technology,
        "nome": f"Expedição {technology}",
        "nivel": level,
        "horas": hours,
        "modulos": [
            {"fase": i + 1, "titulo": module}
            for i, module in enumerate(modules)
        ],
        "competencias": modules
    })

    challenges.extend([
        {
            "id": f"{slug}-basico",
            "tecnologia": technology,
            "nivel": "Básico",
            "titulo": "Resumo de uma expedição",
            "descricao": (
                f"Utilizando {technology}, processe uma lista de distâncias "
                "e informe a soma e a quantidade de etapas."
            ),
            "requisitos": [
                "Aceitar uma lista de números não negativos.",
                "Retornar soma e quantidade.",
                "Tratar a lista vazia."
            ],
            "dicas": [
                "Separe o cálculo da apresentação.",
                "Escreva um teste para a lista vazia."
            ],
            "entrada": "[2, 3, 5]",
            "saida": '{"total":10,"etapas":3}',
            "xp": 100
        },
        {
            "id": f"{slug}-intermediario",
            "tecnologia": technology,
            "nivel": "Intermediário",
            "titulo": "Catálogo de pontos de interesse",
            "descricao": (
                f"Utilizando {technology}, filtre um catálogo de pontos "
                "pela categoria e ordene os resultados pelo nome."
            ),
            "requisitos": [
                "Filtrar pela categoria ignorando maiúsculas.",
                "Ordenar os nomes alfabeticamente.",
                "Não modificar a coleção original."
            ],
            "dicas": [
                "Normalize o termo de pesquisa.",
                "Teste uma categoria sem resultados."
            ],
            "entrada": (
                '{"categoria":"parque","pontos":'
                '[{"nome":"Bosque","categoria":"Parque"}]}'
            ),
            "saida": '[{"nome":"Bosque","categoria":"Parque"}]',
            "xp": 250
        },
        {
            "id": f"{slug}-avancado",
            "tecnologia": technology,
            "nivel": "Avançado",
            "titulo": "Planejador de rota em grafo",
            "descricao": (
                f"Utilizando {technology}, represente um mapa como grafo "
                "ponderado e encontre o menor custo entre dois pontos."
            ),
            "requisitos": [
                "Aceitar apenas pesos não negativos.",
                "Informar o caminho e seu custo.",
                "Tratar destinos sem conexão.",
                "Criar testes para múltiplas rotas."
            ],
            "dicas": [
                "Estude o algoritmo de Dijkstra.",
                "Separe o algoritmo da interface ou relatório."
            ],
            "entrada": "A-B:2, B-C:3, A-C:9; origem:A; destino:C",
            "saida": "Caminho: A → B → C; custo: 5",
            "xp": 400
        }
    ])

files["data/trilhas.json"] = json.dumps(
    tracks, ensure_ascii=False, indent=2
)
files["data/desafios.json"] = json.dumps(
    challenges, ensure_ascii=False, indent=2
)

files["src/core.ts"] = r'''
import { readFileSync } from "node:fs";
import { z } from "zod";

const moduloSchema = z.object({
  fase: z.number().int().positive(),
  titulo: z.string().min(1)
});

const trilhaSchema = z.object({
  id: z.string().min(1),
  tecnologia: z.string().min(1),
  nome: z.string().min(1),
  nivel: z.enum(["Básico", "Intermediário", "Avançado"]),
  horas: z.number().positive(),
  modulos: z.array(moduloSchema).min(1),
  competencias: z.array(z.string().min(1)).min(1)
});

const desafioSchema = z.object({
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

export const trilhas = z.array(trilhaSchema).parse(lerJSON("trilhas.json"));
export const desafios = z.array(desafioSchema).parse(lerJSON("desafios.json"));
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
    .replace(/&/g, "&")
    .replace(/</g, "<")
    .replace(/>/g, ">")
    .replace(/([\\`*_{}|$$$$|#!|])/g, "\\$1");
}
'''

files["src/commands/trilha.ts"] = r'''
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
'''

files["src/commands/desafio.ts"] = r'''
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
'''

files["src/commands/certificado.ts"] = r'''
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
'''

files["src/commands/index.ts"] = r'''
import { executarComandoTrilha } from "./trilha.js";
import { executarComandoDesafio } from "./desafio.js";
import { executarComandoCertificado } from "./certificado.js";

export {
  executarComandoTrilha,
  executarComandoDesafio,
  executarComandoCertificado
};

export const ajuda = [
  "# Geo-Explorer",
  "/trilha <tecnologia>",
  "/desafio <tecnologia> [Básico|Intermediário|Avançado]",
  '/certificado "<nome>" "<tecnologia>"',
  "/help",
  "",
  'Tecnologias com espaços: /desafio "Data Science" Básico',
  "Certificados são fictícios."
].join("\n");

export function separarArgumentos(texto: string): string[] {
  const tokens: string[] = [];
  let atual = "";
  let aspas = false;
  let iniciado = false;

  for (const caractere of texto.trim()) {
    if (caractere === '"') {
      aspas = !aspas;
      iniciado = true;
    } else if (/\s/.test(caractere) && !aspas) {
      if (iniciado) {
        tokens.push(atual);
        atual = "";
        iniciado = false;
      }
    } else {
      atual += caractere;
      iniciado = true;
    }
  }

  if (aspas) throw new Error("Aspas não fechadas.");
  if (iniciado) tokens.push(atual);
  return tokens;
}

export default function processarComando(texto: string): string {
  try {
    const [comando, ...args] = separarArgumentos(texto);

    switch (comando?.toLowerCase()) {
      case undefined:
      case "/help":
      case "/ajuda":
        return ajuda;

      case "/trilha":
        return executarComandoTrilha(args.join(" "));

      case "/desafio":
        if (args.length < 1 || args.length > 2) {
          throw new Error(
            'Uso: /desafio "<tecnologia>" [nivel]. Use aspas em nomes compostos.'
          );
        }
        return executarComandoDesafio(args[0], args[1]);

      case "/certificado": {
        const formato = /^\/certificado\s+"([^"]*)"\s+"([^"]*)"\s*$/i;
        const correspondencia = texto.trim().match(formato);
        if (!correspondencia) {
          throw new Error('Uso: /certificado "<nome>" "<tecnologia>"');
        }
        return executarComandoCertificado(
          correspondencia[1], correspondencia[2]
        );
      }

      default:
        throw new Error("Comando desconhecido. Use /help.");
    }
  } catch (erro) {
    return `Erro: ${erro instanceof Error ? erro.message : "Falha inesperada."}`;
  }
}
'''

files["src/cli.ts"] = r'''
import processarComando from "./commands/index.js";

// O shell remove as aspas externas. Reconstruímos os argumentos
// preservando aqueles que contêm espaços ou são vazios.
const entrada = process.argv.slice(2).map(arg => {
  if (arg.includes('"')) return arg;
  return /\s/.test(arg) || arg === "" ? `"${arg}"` : arg;
}).join(" ");

const resultado = processarComando(entrada);
console.log(resultado);
if (resultado.startsWith("Erro:")) process.exitCode = 1;
'''

files["src/mcp/server.ts"] = r'''
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import {
  executarComandoTrilha,
  executarComandoDesafio,
  executarComandoCertificado
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
'''

files["tests/commands.test.ts"] = r'''
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

  it("exige aspas no certificado", () => {
    expect(processarComando("/certificado Agamenon Python")).toContain("Erro:");
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
'''

files["tests/mcp.test.ts"] = r'''
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import {
  StdioClientTransport
} from "@modelcontextprotocol/sdk/client/stdio.js";

describe("Servidor MCP", () => {
  it("lista ferramentas, consulta trilha e informa erro", async () => {
    const raiz = fileURLToPath(new URL("../", import.meta.url));
    const servidor = fileURLToPath(
      new URL("../src/mcp/server.ts", import.meta.url)
    );

    const transport = new StdioClientTransport({
      command: process.execPath,
      args: ["--import", "tsx", servidor],
      cwd: raiz
    });

    const client = new Client({
      name: "geo-explorer-tests",
      version: "1.0.0"
    });

    try {
      await client.connect(transport);
      const lista = await client.listTools();
      expect(lista.tools.map(t => t.name)).toEqual(
        expect.arrayContaining([
          "consultar_trilha", "gerar_desafio", "gerar_certificado"
        ])
      );

      const resposta = await client.callTool({
        name: "consultar_trilha",
        arguments: { tecnologia: "Python" }
      });
      expect(JSON.stringify(resposta)).toContain("Expedição Python");

      const erro = await client.callTool({
        name: "consultar_trilha",
        arguments: { tecnologia: "Inexistente" }
      });
      expect(erro.isError).toBe(true);
    } finally {
      await client.close();
    }
  }, 20000);
});
'''

files[".github/workflows/ci.yml"] = """
name: Qualidade
on: [push, pull_request]

jobs:
  verificar:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "22"
      - run: npm ci
      - run: npm run typecheck
      - run: npm test
      - run: npm run build
"""

files["README.md"] = """
# Geo-Explorer

Aplicação educacional para explorar trilhas fictícias de aprendizagem,
selecionar desafios de código e emitir certificados demonstrativos.

## Requisitos

- Node.js 22 ou superior;
- npm;
- Git para versionamento.

## Instalação e execução

Na pasta do projeto, execute:

    npm install
    npm run dev -- /help
    npm run exemplo

O comando npm install gera package-lock.json. Inclua esse arquivo no
repositório: a integração contínua usa npm ci.

## Comandos

Consultar trilha:

    npm run dev -- /trilha Python

Consultar tecnologia com nome composto:

    npm run dev -- /trilha "Data Science"

Selecionar desafio por nível:

    npm run dev -- /desafio Python Básico
    npm run dev -- /desafio "Data Science" Intermediário

Selecionar desafio sem restringir o nível:

    npm run dev -- /desafio React

Gerar certificado fictício:

    npm run dev -- /certificado "Agamenon" "TypeScript"

O shell entrega nome e tecnologia como argumentos separados.
A CLI reconstrói esses argumentos para o processador slash.

Ao usar processarComando diretamente, os dois campos do certificado
devem estar entre aspas duplas.

## Tecnologias disponíveis

Python, JavaScript, TypeScript, React e Data Science.

A base possui cinco trilhas e quinze desafios: um desafio por nível
para cada tecnologia. Sem nível, o sorteio pode selecionar qualquer
um dos três desafios da tecnologia. Para sortear diferentes desafios
dentro do mesmo nível, acrescente registros à base.

Todos os dados são fictícios e não representam cursos oficiais.

## Testes e compilação

    npm run typecheck
    npm test
    npm run build
    npm start -- /trilha Python

Os testes de certificados utilizam diretórios temporários.
O teste MCP inicia um servidor local, consulta as ferramentas e fecha
a conexão ao terminar.

O diretório data deve permanecer junto de src e dist.
Não mova somente dist para outro local.

## Certificados e privacidade

Os arquivos são gravados em docs/certificados-emitidos.

Cada arquivo recebe um UUID, evitando usar o nome como caminho.
A gravação exclusiva impede a substituição de um arquivo existente.

O certificado não verifica conclusão, não possui validade oficial
e seu identificador não oferece autenticação externa.

Certificados podem conter nomes pessoais e ficam fora do Git.
Nenhum token é necessário para executar o projeto.

A variável de ambiente GEO_CERTIFICADOS_DIR permite escolher
outro diretório. O projeto não carrega arquivos .env automaticamente.

## Servidor MCP

Em desenvolvimento:

    npm run mcp

Após compilar:

    node dist/mcp/server.js

O transporte é stdio. O processo aguarda um cliente MCP e não apresenta
uma interface de terminal. Não escreva logs em stdout nesse servidor.

Ferramentas:
- consultar_trilha;
- gerar_desafio;
- gerar_certificado.

A ferramenta gerar_certificado grava um arquivo local. Execute
somente com clientes confiáveis e com as permissões necessárias.

Consulte docs/MCP.md para configuração de um cliente.

## Organização

- data: trilhas e desafios fictícios em JSON;
- src/core.ts: validação e busca;
- src/commands: lógica reutilizável e processador slash;
- src/cli.ts: execução pelo terminal;
- src/mcp: servidor MCP;
- tests: testes unitários e de integração;
- docs: desafio, orientação para Bob e documentação;
- .github/workflows: verificação automatizada.

## Melhorias presentes nesta versão

- Busca sem diferenciação entre acentos e maiúsculas;
- Validação da base com Zod;
- Tratamento de tecnologias com espaços;
- Certificados com UUID e arquivos protegidos contra sobrescrita;
- Tratamento de erro no MCP;
- Testes com isolamento de arquivos;
- Integração contínua.

## IBM Bob no desenvolvimento

Utilize o IBM Bob para planejar alterações, explicar código,
propor testes e revisar documentação. Revise cada mudança.

Esta versão não instala comandos automaticamente no chat do Bob.
A integração depende da configuração suportada pelo seu ambiente.
Não há arquivos de configuração do Bob inventados neste projeto.

Veja docs/BOB.md para um roteiro de trabalho.

## O que aprendi

Preencha esta seção depois de executar e adaptar o projeto:
- Qual decisão de arquitetura consegui explicar?
- Qual teste detectou um problema?
- Qual sugestão do Bob precisei corrigir?
- Que melhoria implementei e como a validei?

Essas perguntas são um roteiro, não um relato de trabalho já realizado.

## Publicação

Crie um repositório vazio no GitHub. Depois:

    git init
    git add .
    git commit -m "Implementa Geo-Explorer com CLI, testes e MCP"
    git branch -M main
    git remote add origin URL_DO_SEU_REPOSITORIO
    git push -u origin main

Antes de publicar, revise o que será enviado com git diff --cached.
Não publique senhas, tokens, arquivos .env ou dados pessoais.

## Limitações

- Não há contas, acompanhamento de progresso ou validação de conclusão.
- Desafios são selecionados de uma base local, não gerados por IA.
- Horas e XP são ilustrativos.
- Dependências precisam ser instaladas.
- Execute os testes no seu ambiente antes de entregar.
"""

files["docs/DESAFIO.md"] = """
# Desafio de desenvolvimento: Geo-Explorer

## Objetivo

Construir e compreender uma solução que ofereça consulta de trilhas,
desafios de código e certificados fictícios, com apoio do IBM Bob.

A versão inicial está implementada. Seu desafio é executá-la,
revisá-la e entregar uma evolução própria.

## Etapa 1 — Preparar o repositório

Crie um repositório, instale dependências e execute a ajuda da CLI.
Critério: projeto inicializado e package-lock.json versionado.

## Etapa 2 — Entender a base

Revise trilhas.json e desafios.json.
Explique os IDs, níveis, módulos e relacionamentos.
Critério: adicionar uma trilha e desafios válidos sem quebrar os testes.

## Etapa 3 — Revisar os comandos

Execute consultas válidas e inválidas.
Experimente tecnologias compostas e certificados sem aspas.
Critério: explicar como cada comando trata argumentos e erros.

## Etapa 4 — Testar

Execute testes unitários e o teste de integração MCP.
Adicione um teste para sua melhoria.
Critério: demonstrar uma falha antes da correção e sucesso depois dela.

## Etapa 5 — Integrar pelo MCP

Configure um cliente compatível e consulte uma trilha.
Critério: ferramentas listadas e resposta obtida pelo protocolo.

## Etapa 6 — Evoluir

Escolha uma melhoria pequena:
- novo comando para listar trilhas;
- mais desafios por tecnologia e nível;
- exportação de certificado em HTML;
- acompanhamento local de módulos concluídos;
- interface web;
- adaptação para geotecnologias.

Critério: melhoria funcionando, testada e documentada.

## Etapa 7 — Entregar

Publique o repositório com:
- código e dados;
- testes;
- documentação de execução;
- melhorias realizadas;
- aprendizado escrito com suas próprias palavras.

Revise arquivos criados pelo agente e verifique dados sensíveis.

## Apoio do DIO Agent

Modelo de pedido:

Estou desenvolvendo o Geo-Explorer.
Repositório: <cole o endereço do seu projeto>
Etapa atual: <descreva o problema>
Ajude-me a entender o próximo passo sem entregar a solução completa.

## Autoavaliação

- Consigo explicar a arquitetura?
- Outra pessoa consegue executar usando o README?
- Os testes cobrem erros e não apenas casos de sucesso?
- O MCP reutiliza os comandos?
- Minha melhoria está documentada?
- Revisei todos os arquivos antes do envio?
"""

files["docs/BOB.md"] = """
# Desenvolvimento assistido pelo IBM Bob

Este documento é um roteiro, não uma configuração automática.

## Planejamento

Prompt sugerido:
Analise a estrutura do Geo-Explorer. Explique o fluxo entre CLI,
comandos, base JSON e servidor MCP. Não altere arquivos ainda.

## Revisão dos dados

Prompt sugerido:
Revise os schemas e os arquivos JSON. Proponha verificações para
IDs duplicados e desafios que referenciam tecnologias inexistentes.

## Testes

Prompt sugerido:
Revise os testes existentes. Identifique um comportamento sem cobertura
e explique como criar um teste que falhe caso esse comportamento quebre.

## Evolução

Prompt sugerido:
Quero acrescentar um comando de listagem de trilhas.
Proponha um plano pequeno com implementação, testes e documentação.
Aguarde minha revisão do plano antes de editar.

## Documentação

Prompt sugerido:
Compare o README com os scripts do package.json e a implementação.
Aponte afirmações que não correspondem ao funcionamento real.

## Registro do trabalho

Para cada alteração, registre:
- pedido feito ao Bob;
- sugestão recebida;
- revisão humana;
- testes executados;
- decisão final.

Não envie segredos ou dados pessoais ao agente.
Não declare testes como aprovados sem executá-los.
"""

files["docs/MCP.md"] = """
# Integração MCP

O Geo-Explorer expõe ferramentas próprias. Ele não é um servidor
de administração do GitHub e não requer token do GitHub.

## Preparação

Execute npm install e npm run build.

O servidor compilado está em dist/mcp/server.js.
A base JSON continua no diretório data do projeto.

## Configuração de cliente

O arquivo mcp-client.example.json mostra um formato comum.
A estrutura aceita pode variar conforme o cliente MCP.

Substitua os caminhos de exemplo por caminhos absolutos reais.
No Windows, use barras normais ou escape as barras invertidas no JSON.

Aponte o cliente diretamente para node e para o servidor compilado.
Isso evita mensagens do npm em stdout, reservado ao protocolo.

## Ferramentas

consultar_trilha:
- tecnologia: texto obrigatório.

gerar_desafio:
- tecnologia: texto obrigatório;
- nivel: Básico, Intermediário ou Avançado, opcional.

gerar_certificado:
- nome: entre 1 e 120 caracteres;
- tecnologia: texto obrigatório.

A emissão grava arquivo local e não verifica conclusão.

## Validação

npm test inclui um teste de integração que:
1. inicia o processo do servidor;
2. lista as ferramentas;
3. consulta Python;
4. verifica erro em tecnologia inexistente;
5. encerra a conexão.

## Segurança

Execute localmente com cliente confiável.
Escolha um diretório de saída com permissões restritas.
Não exponha o servidor pela rede sem projetar autenticação,
autorização e limites de uso.
"""

files["docs/mcp-client.example.json"] = json.dumps({
    "mcpServers": {
        "geo-explorer": {
            "command": "node",
            "args": ["/CAMINHO/ABSOLUTO/geo-explorer/dist/mcp/server.js"],
            "env": {
                "GEO_CERTIFICADOS_DIR":
                "/CAMINHO/ABSOLUTO/geo-explorer/docs/certificados-emitidos"
            }
        }
    }
}, ensure_ascii=False, indent=2)

files["docs/REVISAO.md"] = """
# Revisão antes da entrega

- [ ] Instalei dependências.
- [ ] Executei npm run typecheck.
- [ ] Executei npm test.
- [ ] Executei npm run build.
- [ ] Experimentei a CLI compilada.
- [ ] Testei o servidor com cliente MCP.
- [ ] Implementei uma melhoria própria.
- [ ] Adicionei teste para a melhoria.
- [ ] Atualizei o README.
- [ ] Escrevi meu aprendizado sem inventar resultados.
- [ ] Revisei alterações sugeridas pelo Bob.
- [ ] Incluí package-lock.json.
- [ ] Verifiquei que não há segredos ou certificados pessoais no Git.
"""

ROOT.mkdir()

for relative_path, content in files.items():
    destination = ROOT / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        textwrap.dedent(content).lstrip("\n").rstrip() + "\n",
        encoding="utf-8"
    )

archive = Path("geo-explorer.zip")
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zip_file:
    for path in sorted(ROOT.rglob("*")):
        if path.is_file():
            zip_file.write(path, path.as_posix())

print(f"Projeto criado: {ROOT.resolve()}")
print(f"ZIP criado: {archive.resolve()}")
print(f"Arquivos gerados: {len(files)}")
print()
print("Próximos comandos:")
print("  cd geo-explorer")
print("  npm install")
print("  npm run typecheck")
print("  npm test")
print("  npm run build")
print("  npm run exemplo")

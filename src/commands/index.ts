import { executarComandoTrilha } from "./trilha.js";
import { executarComandoDesafio } from "./desafio.js";
import { executarComandoCertificado } from "./certificado.js";
import { executarComandoTrilhas } from "./trilhas.js";

export {
  executarComandoTrilha,
  executarComandoDesafio,
  executarComandoCertificado,
  executarComandoTrilhas
};

export const ajuda = [
  "# Geo-Explorer do Agamenon",
  "/trilhas — lista as tecnologias disponíveis",
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
    return executarArgumentos(separarArgumentos(texto));
  } catch (erro) {
    return `Erro: ${erro instanceof Error ? erro.message : "Falha inesperada."}`;
  }
}

// A CLI passa argv diretamente: aspas e nomes compostos já foram tratados pelo shell.
export function executarArgumentos(argumentos: string[]): string {
  try {
    const [comando, ...args] = argumentos;

    switch (comando?.toLowerCase()) {
      case undefined:
      case "/help":
      case "/ajuda":
        if (args.length) throw new Error("Uso: /help");
        return ajuda;

      case "/trilhas":
        if (args.length) throw new Error("Uso: /trilhas");
        return executarComandoTrilhas();

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
        if (args.length !== 2) {
          throw new Error('Uso: /certificado "<nome>" "<tecnologia>"');
        }
        return executarComandoCertificado(
          args[0], args[1]
        );
      }

      default:
        throw new Error("Comando desconhecido. Use /help.");
    }
  } catch (erro) {
    return `Erro: ${erro instanceof Error ? erro.message : "Falha inesperada."}`;
  }
}

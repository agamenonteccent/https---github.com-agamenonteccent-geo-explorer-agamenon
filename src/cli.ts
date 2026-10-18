import { executarArgumentos } from "./commands/index.js";

const resultado = executarArgumentos(process.argv.slice(2));
console.log(resultado);
if (resultado.startsWith("Erro:")) process.exitCode = 1;

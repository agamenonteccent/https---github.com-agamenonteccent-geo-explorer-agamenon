# Roteiro de demonstração

1. Execute `npm ci` e `npm run check`.
2. Rode `npm run dev -- /trilhas` para conhecer o catálogo.
3. Rode `npm run dev -- /trilha Geotecnologias`: o resultado inclui três fases, 24 horas fictícias e competências.
4. Rode `npm run dev -- /desafio Geotecnologias Básico`: o desafio pede um validador de latitude e longitude.
5. Rode `npm run dev -- /certificado "Agamenon" "Geotecnologias"`: veja o conteúdo e o caminho do Markdown emitido.
6. Rode `npm run dev -- /trilha Inexistente`: a CLI informa erro e retorna código 1.

## API de comandos

```ts
import processarComando, {
  executarComandoTrilha,
  executarComandoDesafio,
  executarComandoCertificado
} from "../src/commands/index.js";

console.log(executarComandoTrilha("python"));
console.log(executarComandoDesafio("Geotecnologias", "basico"));
console.log(processarComando('/desafio "Data Science" Intermediário'));
// Este comando grava arquivo local:
console.log(executarComandoCertificado("Agamenon", "Python"));
```

## Desafio geográfico básico

Entrada: `{"latitude":-23.55,"longitude":-46.63}`. Saída: `true`.

A implementação deve recusar números não finitos, latitude fora de [-90, 90] e longitude fora de [-180, 180]. O Geo-Explorer apresenta o enunciado; cabe à pessoa escrever e testar sua solução.

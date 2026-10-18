# Validação da entrega

Verificações executadas localmente em 18/10/2026, no Windows, com Node.js 22.14.0:

| Verificação | Resultado |
| --- | --- |
| `npm run typecheck` | Aprovado, sem erros de TypeScript. |
| `npm test` | 30 testes aprovados em 4 arquivos, usando Vitest 5.0.5. |
| `npm run build` | Aprovado; CLI e servidor gerados em `dist/`. |
| `npm run verify:build` | CLI, certificado e MCP compilados funcionaram a partir de outra pasta. |
| Auditoria ao instalar dependências atualizadas | 0 vulnerabilidades reportadas pelo npm. |

A suíte cobre consultas válidas/inválidas, níveis, normalização, integridade do catálogo, arquivos únicos, escape de conteúdo, argumentos do shell e comunicação MCP. A integração MCP chama as quatro ferramentas, verifica o arquivo emitido e valida respostas de erro. Os testes usam e removem diretórios temporários.

A verificação do build executa os quatro comandos principais/listagem e conecta um cliente ao servidor compilado de uma pasta externa. Isso verifica o carregamento dos JSON sem depender do diretório atual.

A configuração GitHub Actions está preparada para Node 22 e 24 no Ubuntu. Esse ambiente remoto não foi executado nesta validação local. A configuração manual em um cliente IBM Bob também não foi realizada; o teste MCP utilizou o cliente do SDK.

O resultado da auditoria reflete o catálogo npm no momento da instalação; o lockfile registra as versões utilizadas. Para repetir a verificação, execute `npm ci`, `npm run check` e `npm audit`.

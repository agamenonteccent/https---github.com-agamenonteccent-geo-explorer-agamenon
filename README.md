# Geo-Explorer do Agamenon

Explore trilhas fictícias de aprendizagem, receba um desafio de código e gere um certificado demonstrativo pelo terminal ou por um cliente MCP. Projeto de portfólio do desafio Formação IBM com Bob, inspirado no [DIO Explorer de referência](https://github.com/batestin1/projeto_final_dio_formacao_bob/tree/main/projeto_final_dio_formacao_bob/dio_explorer).

## Começar

Requisitos: **Node.js 22.14+ (linha 22), 24.x ou 26+**, npm e, para publicar, Git. Não é necessário token, conta IBM ou serviço pago para executar a aplicação.

Na pasta deste README:

```sh
npm ci
npm run dev -- /help
npm run dev -- /trilhas
npm run dev -- /trilha Geotecnologias
npm run dev -- /desafio Geotecnologias Básico
npm run dev -- /certificado "Agamenon" "Geotecnologias"
```

O último comando grava um arquivo Markdown em `docs/certificados-emitidos/`. Os comandos funcionam no PowerShell e em terminais Linux/macOS. Use aspas duplas em nomes compostos.

## Comandos

| Comando | Resultado |
| --- | --- |
| `/trilhas` | Lista tecnologias, IDs, níveis, horas e módulos. |
| `/trilha <tecnologia>` | Mostra o plano de estudos dividido em fases. |
| `/desafio <tecnologia> [nível]` | Seleciona um desafio com requisitos, dicas e exemplo de entrada/saída. |
| `/certificado "<nome>" "<tecnologia>"` | Emite certificado fictício em Markdown. |
| `/help` ou `/ajuda` | Exibe a ajuda. |

Exemplos adicionais:

```sh
npm run dev -- /trilha "Data Science"
npm run dev -- /desafio Python intermediario
npm run dev -- /desafio React
npm run dev -- /certificado "Agamenon da Silva" "Data Science"
```

Níveis: Básico, Intermediário e Avançado. A busca ignora acentos e maiúsculas, aceita o ID exato e trechos do nome da trilha. Consultas ambíguas são recusadas nos comandos que exigem uma única trilha. Erros de uso retornam código de saída 1 na CLI.

A base contém **6 trilhas e 18 desafios**: Python, JavaScript, TypeScript, React, Data Science e Geotecnologias. Há um desafio por nível para cada tecnologia; sem nível, o comando sorteia entre os três. Os desafios vêm de um catálogo local, sem chamada a IA, execução ou correção automática do código da pessoa usuária.

## Testar e compilar

```sh
npm run check
```

Executa a verificação de tipos, os testes, a compilação e a verificação da CLI/MCP compilados a partir de outra pasta. Etapas individuais:

```sh
npm run typecheck
npm test
npm run build
npm start -- /trilha Python
```

Os testes cobrem comandos válidos e inválidos, integridade dos dados, escape de HTML/Markdown, nomes compostos, código de saída da CLI, arquivos de certificados e comunicação MCP real por stdio. Certificados de teste usam diretórios temporários que são removidos ao final.

A compilação gera `dist/`. Mantenha `data/` junto de `src/` e `dist/`: a aplicação carrega os JSON em tempo de execução, inclusive quando iniciada de outra pasta.

## Servidor MCP

```sh
npm run build
node dist/mcp/server.js
```

O servidor aguarda um cliente pelo transporte **stdio**. Expõe `listar_trilhas`, `consultar_trilha`, `gerar_desafio` e `gerar_certificado`. A última ferramenta grava um arquivo local. O protocolo usa stdout; diagnósticos ficam em stderr.

Veja [configuração do cliente e exemplos](docs/MCP.md) e [arquivo JSON de configuração](docs/mcp-client.example.json). Configure o cliente diretamente com `node` e o caminho absoluto do servidor compilado.

## Arquitetura

```text
CLI / cliente MCP
        ↓
comandos compartilhados
        ↓
validação e busca (core.ts) → data/*.json
        ↓
texto Markdown / certificado local
```

- `data/`: catálogo educacional fictício.
- `src/core.ts`: schemas Zod, validação da base, normalização e busca.
- `src/commands/`: funções reutilizáveis e processador de comandos slash.
- `src/cli.ts`: argumentos do terminal e códigos de saída.
- `src/mcp/server.ts`: ferramentas MCP usando os mesmos comandos.
- `tests/`: testes unitários e de integração com Vitest.
- `docs/`: arquitetura, exemplos, roteiro IBM Bob e orientações de entrega.
- `.github/workflows/ci.yml`: tipos, testes e build em cada push/PR.

Para usar em TypeScript:

```ts
import processarComando from "./src/commands/index.js";
console.log(processarComando('/desafio "Data Science" Básico'));
```

Na CLI, os argumentos do shell são usados diretamente. No processador textual, aspas duplas delimitam argumentos compostos. Campos simples podem ser informados sem aspas.

## Melhorias realizadas

- Identidade Geo-Explorer do Agamenon e trilha de **Geotecnologias**, com desafios de coordenadas, GeoJSON e rotas.
- Novo comando `/trilhas`, também disponível por MCP.
- Validação em tempo de execução de schemas, IDs únicos, tecnologias e sequência dos módulos.
- Correção da emissão de certificado com nomes simples, compostos ou contendo aspas no terminal.
- Escape de HTML e Markdown nos nomes dos participantes.
- Certificados com UUID e gravação exclusiva para evitar sobrescrita; nomes não são usados como caminhos.
- Testes de processos reais da CLI e das quatro ferramentas MCP.
- Lockfile, dependências de teste atualizadas e integração contínua.

## Certificados e limites

Todos os dados, horas e XP são ilustrativos. O certificado é **fictício, sem validade acadêmica ou profissional**. O sistema não verifica a conclusão da trilha e o UUID não oferece autenticação externa. Não há contas nem acompanhamento de progresso.

Os certificados podem conter nomes pessoais e ficam fora do Git por `.gitignore`. Nenhum segredo é necessário. A variável opcional `GEO_CERTIFICADOS_DIR` define outra pasta de saída; caminhos relativos usam a pasta de onde o processo foi iniciado. O projeto não carrega `.env` automaticamente.

## IBM Bob e aprendizado

O IBM Bob pode apoiar planejamento, implementação, revisão de testes e documentação. Consulte o [roteiro de desenvolvimento assistido](docs/BOB.md). Esta implementação foi produzida nesta sessão com Codex a partir do material local e da consulta à referência; não declara execução do IBM Bob nem inventa configuração específica dele.

Conceitos exercitados na solução:

- Separar regras de negócio da CLI permite reutilizá-las no servidor MCP.
- TypeScript verifica tipos no código; Zod também verifica o JSON carregado em execução.
- Testar a CLI em outro processo revela problemas de argumentos que testes de funções isoladas não detectam.
- Um teste MCP deve conectar um cliente, descobrir ferramentas, chamá-las e verificar respostas e arquivos.
- Isolar arquivos temporários e escapar conteúdo são partes da implementação, além dos casos de sucesso.

Esses pontos descrevem o projeto. Para a entrega pessoal, registre com suas palavras o que aprendeu, o que revisou com Bob e qual decisão passou a compreender; não atribua ao agente experiências que você ainda não realizou.

## Publicar no GitHub

Crie um repositório vazio na sua conta, sem README inicial. Na raiz local:

```sh
git init
git add .
git diff --cached
git commit -m "Implementa Geo-Explorer do Agamenon com CLI e MCP"
git branch -M main
git remote add origin https://github.com/agamenonteccent/geo-explorer-agamenon
git push -u origin main
```

Se o repositório já estiver inicializado, comece por `git status`. Revise o conteúdo antes do commit. Não envie `.env`, tokens ou certificados pessoais. O arquivo `package-lock.json` deve ser versionado para que `npm ci` e o CI usem as mesmas versões.

Veja [exemplos completos](docs/EXEMPLOS.md), [decisões de arquitetura](docs/ARQUITETURA.md), [validação da entrega](docs/VALIDACAO.md) e [origem do material](docs/REFERENCIAS.md).

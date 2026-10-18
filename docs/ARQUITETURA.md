# Decisões de arquitetura

## Fluxo e responsabilidades

A CLI recebe `process.argv` e encaminha os argumentos para `executarArgumentos`. O processador textual `processarComando` separa os campos de comandos slash e usa o mesmo despachante. Assim, a CLI não precisa reconstruir aspas retiradas pelo shell.

Os comandos consultam `core.ts`, que carrega os JSON por caminho relativo ao módulo, valida a estrutura com Zod e verifica referências, IDs e sequência de fases. A busca normaliza acentos e caixa. Uma correspondência exata tem prioridade sobre trechos do título.

O MCP utiliza as funções individuais. Erros de negócio viram conteúdo com `isError: true`. O SDK valida os argumentos do protocolo. O catálogo fica em memória após a inicialização; alterações nos JSON exigem reiniciar o processo.

## Certificados

O certificado usa UUID aleatório como nome do arquivo, diretório configurável e gravação com `flag: wx`. O nome da pessoa fica apenas no conteúdo, com escape de HTML e Markdown. A saída é um documento demonstrativo e não representa validação de conclusão.

## Escopo

O projeto usa JSON local para facilitar leitura e evolução. Não precisa de banco de dados, API externa nem credenciais. Não executa as soluções dos desafios. O transporte MCP é local por stdio e não oferece endpoint HTTP.

## Evolução

Para adicionar uma tecnologia, inclua uma trilha com ID único e fases consecutivas, depois desafios correspondentes aos três níveis. Execute `npm run check`. Para incluir outro comando, crie a função em `src/commands`, registre-a no despachante e, se apropriado, no MCP; acrescente testes de comportamento.

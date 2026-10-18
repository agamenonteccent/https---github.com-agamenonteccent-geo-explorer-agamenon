# Integração MCP

O servidor local usa o SDK `@modelcontextprotocol/sdk` e transporte stdio. Não requer token GitHub ou IBM.

## Preparar

```sh
npm ci
npm run build
```

Configure o cliente com o executável `node` e o caminho absoluto de `dist/mcp/server.js`, conforme `mcp-client.example.json`. Substitua os caminhos por caminhos reais; no Windows use barras normais ou barras invertidas escapadas. Se Node não estiver no PATH do cliente, informe o caminho completo de `node.exe`.

```json
{
  "mcpServers": {
    "geo-explorer-agamenon": {
      "command": "node",
      "args": ["C:/CAMINHO/Geo-Explorer Agamenon/dist/mcp/server.js"],
      "env": {
        "GEO_CERTIFICADOS_DIR": "C:/CAMINHO/Geo-Explorer Agamenon/docs/certificados-emitidos"
      }
    }
  }
}
```

A estrutura de configuração pode variar entre clientes. Não use `npm run` como comando do cliente: mensagens do npm podem ocupar stdout, reservado ao protocolo. Ao iniciar manualmente com `node dist/mcp/server.js`, o processo aguarda mensagens MCP e não mostra um prompt.

## Ferramentas

| Ferramenta | Argumentos | Efeito |
| --- | --- | --- |
| `listar_trilhas` | `{}` | Lista o catálogo. |
| `consultar_trilha` | `tecnologia: string` | Retorna plano de estudos. |
| `gerar_desafio` | `tecnologia: string`, `nivel?: string` | Seleciona desafio local. |
| `gerar_certificado` | `nome: string`, `tecnologia: string` | Grava Markdown local. |

No MCP, nível deve ser exatamente `Básico`, `Intermediário` ou `Avançado`; na CLI, a normalização também permite variações sem acento. O nome deve conter entre 1 e 120 caracteres após retirar espaços externos.

Exemplo de argumentos: `{"tecnologia":"Geotecnologias","nivel":"Básico"}` para `gerar_desafio`.

## Verificação

`npm test` inicia um processo servidor e um cliente SDK, lista e chama as quatro ferramentas, verifica o certificado gravado, testa tecnologia inexistente e nome inválido e encerra a conexão. Os arquivos usam pasta temporária.

O cliente pode ser iniciado de outra pasta: os dados são localizados a partir do arquivo do servidor. Configure a saída dos certificados com caminho absoluto para evitar dependência da pasta do cliente. Não exponha esse processo como serviço de rede sem projetar os controles necessários.

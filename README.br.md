# Servidor MCP de Pesquisa em Direito Brasileiro

Um servidor MCP (Model Context Protocol) para pesquisa sobre direito brasileiro movida por agentes 
de IA.

## Requisitos

- Python 3.11 ou superior
- Google Chrome
- uv (recomendado)

## Como usar

1. Clone o repositório:
```bash
git clone https://github.com/pdmtt/brlaw_mcp_server.git
```

2. Configure seu cliente MCP (ex: Claude Desktop):
```json
{
  "mcpServers": {
    "brlaw_mcp_server": {
      "command": "uv",
      "args": [
        "--directory",
        "/<caminho>/brlaw_mcp_server",
        "run",
        "serve"
      ]
    }
  }
}
```

### Ferramentas Disponíveis

- `precedentes-stj`: Pesquisa precedentes judiciais feitos pelo Superior Tribunal de Justiça (STJ) 
  que atendam aos critérios especificados.

## Desenvolvimento

### Ferramentas

O projeto utiliza:
- Ruff para linting e formatação.
- BasedPyright para verificação de tipos.
- Pytest para testes.

### Idioma

Recursos, ferramentas e materiais relacionados a prompts devem ser escritos em português, pois este 
projeto tem como objetivo ser utilizado por pessoas que não são desenvolvedoras, como advogados e 
estudantes de direito.

O vocabulário técnico jurídico é altamente dependente da tradição legal de um país e sua tradução 
não é uma tarefa trivial.

Materiais relacionados ao desenvolvimento devem permanecer em inglês, conforme convencional, como o 
código-fonte.

## Licença

Este projeto está licenciado sob a Licença MIT - consulte o arquivo LICENSE para obter detalhes. 
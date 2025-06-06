import asyncio
import textwrap
from typing import Any, Final

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from patchright.async_api import async_playwright
from pydantic import BaseModel, Field

from brlaw_mcp_server.domain.stj import StjLegalPrecedent
from brlaw_mcp_server.domain.tst import TstLegalPrecedent


class BaseLegalPrecedentsRequest(BaseModel):
    """Common model for all legal precedents requests."""

    page: int = Field(
        title="Página",
        description=(
            "A página dos resultados a ser retornada. Cada página alguns resultados. "
            + "É útil requisitar mais de uma página para conseguir mais informações, se necessário."
        ),
        ge=1,
        default=1,
    )


class StjLegalPrecedentsRequest(BaseLegalPrecedentsRequest):
    """Requisição dos precedentes judiciais do Superior Tribunal de Justiça (STJ) que satisfaçam os critérios passados.

    O STJ é a autoridade máxima na interpretação da legislação federal infraconstitucional, o que
    exclui a Constituição Federal."""

    summary: str = Field(
        title="Ementa",
        description=textwrap.dedent("""
        Critérios que serão buscados na ementa das decisões desejadas.

        É possível utilizar operadores textuais para aumentar a assertividade da busca. Na ausência 
        de qualquer operador explícito entre duas palavras, o sistema presumirá o operador `e`.
        Ou seja, `supermercado furto veículo` é o mesmo que `supermercado e furto e veículo`.

        ## Operadores lógicos
        ### `e`
        Localiza termos em qualquer ordem ou campo do documento.

        EXEMPLO: supermercado e furto e veículo

        RESULTADO: o sistema buscará documentos que contenham as três palavras, em qualquer ordem ou 
        distância.

        ### `ou`
        Localiza um e/ou outro termo. Os termos devem vir sempre entre parênteses.

        EXEMPLO: (carro ou automóvel ou veículo)

        RESULTADO: o sistema buscará documentos que contenham qualquer uma das três palavras.

        ### `não`
        Exclui determinado termo da pesquisa.

        EXEMPLO: (seguro não automóvel)

        RESULTADO: o sistema buscará apenas os documentos que contenham a palavra “seguro”, mas 
        excluirá do resultado aqueles que tragam a palavra “automóvel”.

        ### `mesmo`
        Localiza termos em um mesmo campo do documento.

        EXEMPLO: (FGTS mesmo súmula mesmo civil)

        RESULTADO: o sistema buscará os documentos que contenham as três palavras indicadas, em 
        qualquer ordem ou distância, dentro de um mesmo campo.

        ### `com`
        Localiza termos em um mesmo parágrafo.
        
        EXEMPLO: recurso com STJ com furto com veículo

        RESULTADO: o sistema buscará os documentos que contenham as quatro palavras em qualquer 
        ordem ou distância, dentro do mesmo parágrafo.

        ## Operadores de proximidade
        ### `PROX(N)`
        Localiza termos PROXimos, em qualquer ordem. (N) limita a distância entre os termos pesquisados. 
        O segundo termo poderá ser até a enésima palavra antes ou depois do primeiro termo.

        EXEMPLO: nega prox2 provimento prox5 recursos

        RESULTADO: O sistema buscará os documentos que contenham as três palavras em qualquer ordem, 
        até a distância determinada. No exemplo, serão recuperadas as expressões: “recursos a que se 
        nega provimento” “nega-se provimento ao recurso” “recursos especiais a que se nega provimento”

        ### `ADJ(N)`
        Localiza termos ADJacentes, na ordem estabelecida na pesquisa. (N) limita a distância entre
        os termos pesquisados. O segundo termo poderá ser até a enésima palavra após o primeiro
        termo. adj = adj1 (busca os termos conjugados sem qualquer outra palavra entre eles).

        EXEMPLO: causa adj3 aumento adj2 pena

        RESULTADO: O sistema buscará os documentos que contenham as três palavras, na ordem digitada, 
        até a distância delimitada. Serão resgatadas expressões como: “Causa de aumento de pena” 
        “causas especiais de aumento de pena”

        ## Símbolos auxiliares
        ### `$`
        Substitui vários caracteres, podendo vir no início, meio ou fim da palavra. É possível 
        limitar o número máximo de caracteres utilizando valores numéricos.

        EXEMPLO 1: constitui$

        RESULTADO 1: Constitui; Constituir; Constituído; Constituição.

        EXEMPLO 2: $classificado

        RESULTADO 2: Classificado; Reclassificado; Desclassificado; Não-classificado.

        EXEMPLO 3: des$cao

        RESULTADO 3: Deserção; Descrição; designação.

        EXEMPLO 4: p$3

        RESULTADO 4: PG; Para; PAR; Pode; Pena.

        ### `?`
        Substitui um único carácter, podendo vir no início, meio ou fim da palavra. Cada 
        interrogação corresponde a um carácter.

        EXEMPLO: d?sc?r??

        RESULTADO: Deserção; Descrição; designação; descrição.

        ### `( )`
        Usado para o operador OU e para agrupar itens da pesquisa. A alteração poderá ser feita 
        manualmente.

        EXEMPLO: ((menor ou criança) e infrator) com pena

        RESULTADO: o sistema buscará os documentos que contenham as combinações: menor e infrator 
        com pena ou criança e infrator com pena

        ### `" "`
        Utilizado para transformar um operador em palavra a ser pesquisada e para localizar expressões 
        exatas.

        EXEMPLO: “não” adj previsto “tribunal de origem”

        RESULTADO: o sistema buscará documentos que contenham a expressão “não previsto”. O sistema 
        buscará documentos que contenham a expressão “tribunal de origem”."""),
        min_length=1,
        examples=[
            "supermercado e furto e veículo",
            "(carro ou automóvel ou veículo)",
            "(seguro não automóvel)",
            "(FGTS mesmo súmula mesmo civil)",
            "recurso com STJ com furto com veículo",
            "nega prox2 provimento prox5 recursos",
            "causa adj3 aumento adj2 pena",
            "$classificado",
            "d?sc?r??",
            "((menor ou criança) e infrator) com pena",
            "“não” adj previsto “tribunal de origem”",
        ],
    )


class TstLegalPrecedentsRequest(BaseLegalPrecedentsRequest):
    """Requisição dos precedentes judiciais do Superior Tribunal de Justiça (STJ) que satisfaçam os critérios passados.

    O STJ é a autoridade máxima na interpretação da legislação federal infraconstitucional, o que
    exclui a Constituição Federal."""

    summary: str = Field(
        title="Ementa",
        description=textwrap.dedent("""
        Critérios que serão buscados na ementa das decisões desejadas.

        É admitido o uso de aspas e elas devem ser empregadas para pesquisas exatas de expressões ou 
        palavras compostas."""),
        min_length=1,
        examples=[
            "trabalho temporário jornada “adicional de periculosidade”",
        ],
    )


_TOOLS: Final[list[Tool]] = [
    Tool(
        name=model.__name__,
        description=model.__doc__,
        inputSchema=model.model_json_schema(),
    )
    for model in [StjLegalPrecedentsRequest, TstLegalPrecedentsRequest]
]


async def _list_tools() -> list["Tool"]:
    return _TOOLS


async def call_tool(
    name: str,
    arguments: dict[str, "Any"],  # pyright: ignore[reportExplicitAny]
) -> list[TextContent]:
    """Handles a tool call from a MCP client."""
    match name:
        case StjLegalPrecedentsRequest.__name__:
            request = StjLegalPrecedentsRequest(**arguments)  # pyright: ignore[reportAny]
            method = StjLegalPrecedent.research
        case TstLegalPrecedentsRequest.__name__:
            request = TstLegalPrecedentsRequest(**arguments)  # pyright: ignore[reportAny]
            method = TstLegalPrecedent.research
        case _:
            raise ValueError(f"Tool {name} not found")

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()

        precedents = await method(
            page,
            summary_search_prompt=request.summary,
            desired_page=request.page,
        )

    return (
        [
            TextContent(type="text", text=precedent.model_dump_json())
            for precedent in precedents
        ]
        if precedents
        else [TextContent(type="text", text="Nenhum resultado encontrado")]
    )


async def _serve() -> None:
    server = Server("brlaw_mcp_server")

    server.list_tools()(_list_tools)
    server.call_tool()(call_tool)

    options = server.create_initialization_options()

    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)


def serve() -> None:
    """Starts the MCP server."""
    asyncio.run(_serve())

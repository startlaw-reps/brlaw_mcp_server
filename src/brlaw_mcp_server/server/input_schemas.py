"""Models to parse as the server's tools' input JSON schemas."""

from typing import Literal

from pydantic import BaseModel, Field


class RequisitarPrecedentesJudiciais(BaseModel):
    """Requisição dos precedentes judiciais que satisfaçam os critérios passados.

    É possível utilizar os seguintes operadores textuais no campo de critérios:
    - "e" - furto e estacionamento e supermercado = localiza as três palavras em qualquer lugar do
      documento.
    - "ou" - furto e estacionamento e (supermercado ou hipermercado ou mercado) = localiza um e/ou
      outro termo digitado entre parênteses.
    - "adj" - furto adj5 estacionamento adj4 supermercado = "Estacionamento" será no máximo a quinta
      palavra após "furto" e "supermercado" será no máximo a quarta palavra após "estacionamento".
    - "não" - furto e estacionamento não supermercado = localiza documentos que contenham as
      palavras "furto" e "estacionamento", excluindo documentos que contenham a palavra
      "supermercado".
    - "prox" - furto prox6 estacionamento prox4 supermercado = "Estacionamento" será no máximo a
      sexta palavra antes ou após "furto"; "supermercado" será no máximo a quarta palavra antes ou
      após "estacionamento".
    - "mesmo" - furto mesmo estacionamento mesmo supermercado = localiza os termos num mesmo campo
      do documento.
    - "com" - furto com estacionamento com supermercado = localiza os termos dentro de um mesmo
      parágrafo.
    - "$" - furto e estacionamento e $mercado = localiza as palavras que contenham a parte digitada
      e suas variações: "supermercado", "hipermercado" ou "mercado".

    É possível utilizar parênteses para agrupar expressões e aspas para agrupar palavras que devem
    aparecer numa sequência exata.
    """

    criteria: str = Field(
        title="critérios",
        description="A ementa da decisão que está sendo pesquisada. Deve ser um texto não vazio.",
    )

    court: Literal["STJ"] = Field(
        title="tribunal",
        description="O tribunal que deve ser pesquisado. Deve ser um texto não vazio.",
    )

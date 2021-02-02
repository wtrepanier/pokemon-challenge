import os
from typing import List

from coveopush import CoveoPush, Document

from push_api.pokemon import Pokemon


def get_push_client() -> CoveoPush.Push:
    source_id = os.environ.get("PUSH_SOURCE_ID")
    org_id = os.environ.get("PUSH_ORG_ID")
    api_key = os.environ.get("PUSH_API_KEY")
    if not source_id or not org_id or not api_key:
        raise EnvironmentError("coveo environment variable are not set")
    return CoveoPush.Push(source_id, org_id, api_key)


def create_document(pokemon: Pokemon) -> Document:
    document = Document(pokemon.link)
    document.AddMetadata('name', pokemon.name)
    document.AddMetadata('link', pokemon.link)
    document.AddMetadata('image_link', pokemon.image_link)
    document.AddMetadata('type', pokemon.type)
    document.AddMetadata('number', pokemon.number)
    document.AddMetadata('generation', pokemon.generation)
    return document


def push_pokemons(pokemons: List[Pokemon]) -> None:
    push = get_push_client()

    batch = []
    for pokemon in pokemons:
        batch.append(create_document(pokemon))
    push.AddDocuments(batch, [])

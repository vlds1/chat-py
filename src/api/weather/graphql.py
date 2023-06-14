from ariadne.asgi import GraphQL

from fastapi import Depends, Request
from fastapi.dependencies.utils import get_dependant, solve_dependencies
from src.dependencies import get_mongo_exctructor


from src.api.weather.context_types import GraphqlContext, DependencyOverrideProvider
from src.api.weather.schemas import graphql_schema


async def create_context(
    mongo_extractor = Depends(get_mongo_exctructor)
) -> GraphqlContext:
    return GraphqlContext(
        mongo_extractor=mongo_extractor
    )

_create_context_dependant = get_dependant(path="/", call=create_context)

def make_context_creator(
    dependency_overrider: DependencyOverrideProvider | None = None
):
    async def create(request: Request) -> GraphqlContext:
        solved, errors, *_ = await solve_dependencies(
            request=request,
            dependant=_create_context_dependant,
            dependency_overrides_provider=dependency_overrider or request.app
        )
        if errors:
            raise RuntimeError(*errors) from errors[0].exc
        return await create_context(**solved)
        # return await create_context(mongo_extractor=solved['mongo_extractor'])
    return create


def create_graphql(
    dependency_overrider: DependencyOverrideProvider | None = None
) -> GraphQL:
    return GraphQL(graphql_schema, context_value=make_context_creator(dependency_overrider))

graphql_app = create_graphql()
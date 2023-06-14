from typing import Protocol, Any, Callable
from ariadne import ObjectType
from pydantic import BaseModel, PositiveFloat
from pydantic.dataclasses import dataclass
from graphql import GraphQLResolveInfo as _GraphQLResolveInfo

from src.api.weather.crud import MongoExtractor


class GraphqlContextConfig:
    arbitrary_types_allowed = True


@dataclass(config=GraphqlContextConfig)
class GraphqlContext:
    mongo_extractor: MongoExtractor


class GraphQLResolveInfo(_GraphQLResolveInfo):
    context: GraphqlContext


class DependencyOverrideProvider(Protocol):
    dependency_overrides: dict[Callable[..., Any], Callable[..., Any]]


query = ObjectType("WeatherQuerySchema")
from ariadne import make_executable_schema
from ariadne import load_schema_from_path, make_executable_schema

from src.api.weather.resolvers import *
from src.api.weather.context_types import query



type_defs = load_schema_from_path("src/api/query_schemas/schema.graphql")


graphql_schema = make_executable_schema(
    type_defs,
    query,
)
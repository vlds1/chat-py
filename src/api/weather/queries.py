from ariadne import gql, make_executable_schema, ObjectType
from ariadne.asgi import GraphQL

type_defs = gql("""
    type Query {
        city: String!
        temperature: Float!
    }
""")

query = ObjectType("Query")


@query.field("city")
def resolve_hello(_, info):
    request = info.context["request"]
    user_agent = request.headers.get("user-agent", "guest")
    return "Hello, %s!" % user_agent


schema = make_executable_schema(type_defs, [query, ])
graphql_app = GraphQL(schema, debug=True)

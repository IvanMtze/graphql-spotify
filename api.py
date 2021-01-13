from graphene import ObjectType, String, Schema
from flask_graphql import GraphQLView
from flask import Flask
from main import Resolver
from flask_cors import CORS

resolver=Resolver()

class Query(ObjectType):
    # this defines a Field `hello` in our Schema with a single Argument `name`
    song = String(uri=String(default_value=""))
    # our Resolver method takes the GraphQL context (root, info) as well as
    # Argument (name) for the Field and returns data for the query Response
    def resolve_song(root, info, uri)
        return resolver.get_prediction_song(uri)

view_func = GraphQLView.as_view("graphql", schema=Schema(query=Query),graphiql=True)

app = Flask(__name__)
CORS(app)


app.add_url_rule("/", view_func=view_func)

if __name__ == "__main__":
    app.run()

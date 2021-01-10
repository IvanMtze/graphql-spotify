import graphene
import moodsongs.api.schema
class Query(api.schema.Query, graphene.ObjectType):
	pass
schema=graphene.Schema(query=Query)

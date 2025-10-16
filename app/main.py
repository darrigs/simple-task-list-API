from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter

from app.queries import Query
from app.mutations import Mutation
from app.database import init_db

schema = strawberry.Schema(query=Query, mutation=Mutation)
app = FastAPI()

init_db()

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI and Strawberry GraphQL app!"}

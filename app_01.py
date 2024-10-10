"""
Description: This file contains the schema for the first app.
The schema is defined using the graphene library.
query is used for reading data from the database.
mutation is used for writing data to the database.
The schema is used to create the API for the app.

documentation: https://graphene-python.org/

Author: Amir Sarrafzadeh Arasi
Date: 2024-10-10
"""


# Importing the required libraries.
import json
import uuid
import graphene
from datetime import datetime


# Query
class Query(graphene.ObjectType):
    # The fields are defined as class variables.
    # The field cannot have the same name as the class variable.
    # The field must be in camelCase, cannot be in snake_case.
    # if you want to use snake_case too, you must set the auto_camelcase to False.
    name = graphene.String(first_name=graphene.String(default_value='Amir'))

    # the name of the functions must start with resolve_ and then the name of the field.
    def resolve_name(self, info, first_name):
        return f'My firstname is {first_name}'

    surname = graphene.String(family_name=graphene.String(default_value='Sarrafzadeh Arasi'))

    def resolve_surname(self, info, family_name):
        return family_name

    age = graphene.Int(age=graphene.Int(default_value=36))

    def resolve_age(self, info, age):
        return age

    fullname = graphene.String(fullname=graphene.String(default_value='Amir Sarrafzadeh Arasi'))

    # info is the context of the request.
    def resolve_fullname(self, info, fullname):
        return fullname


schema = graphene.Schema(query=Query, auto_camelcase=False)
# if the field is String it must be in double quotes.
query_result = schema.execute('{name(first_name:"Sara") , surname , age , fullname(fullname:"Sara Sarrafzadeh Arasi")}')

print(query_result)

# Mutation
class User(graphene.ObjectType):
    id = graphene.ID(default_value=str(uuid.uuid4()))
    name = graphene.String()
    surname = graphene.String()
    age = graphene.Int()
    created_at = graphene.DateTime(default_value=datetime.now())
    updated_at = graphene.DateTime(default_value=datetime.now())


class UserInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    surname = graphene.String(required=True)
    age = graphene.Int(required=True)

class CreateUser(graphene.Mutation):
    class Arguments:
        user_data = UserInput(required=True)

    user = graphene.Field(lambda: User)

    def mutate(self, info, user_data=None):
        user = User(name=user_data.name, surname=user_data.surname, age=user_data.age)
        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation, auto_camelcase=False)
mutation_result = schema.execute('mutation {create_user(user_data:{name:"Amir", surname:"Sarrafzadeh Arasi", age:36}) {user {name, surname, age}}}')
print(mutation_result)

# Variables
query = '''
    query($name: String!, $surname: String!, $age: Int!) {
        name(first_name: $name)
        surname(family_name: $surname)
        age(age: $age)
    }
'''

variables = {
    'name': "Sara",
    'surname': 'Sarrafzadeh Arasi',
    'age': 36
}

query_result = schema.execute(query, variable_values=variables)

print(query_result)


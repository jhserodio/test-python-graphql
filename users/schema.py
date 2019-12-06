from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

import graphene
from graphene_django import DjangoObjectType

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int())
    user_by_email = graphene.Field(UserType, email=graphene.String())
    users = graphene.List(UserType)

    def resolve_users(self, info):
        return get_user_model().objects.all()

    def resolve_user(self, info, id=None):
        return User.objects.get(pk=id)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


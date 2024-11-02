# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/classes/50_DomoInstanceConfig_ApiClient.ipynb.

# %% auto 0
__all__ = ['ApiClient', 'ApiClient_Search_Error', 'ApiClients']

# %% ../../nbs/classes/50_DomoInstanceConfig_ApiClient.ipynb 2
from domolibrary.routes.instance_config_api_client import (
    ApiClient_GET_Error,
    ApiClient_RevokeError,
    ApiClient_CRUD_Error,
    ApiClient_ScopeEnum,
)

# %% ../../nbs/classes/50_DomoInstanceConfig_ApiClient.ipynb 3
import datetime as dt
import httpx
import asyncio
from typing import List
from nbdev.showdoc import patch_to


from dataclasses import dataclass, field
import domolibrary.client.DomoAuth as dmda
import domolibrary.utils.chunk_execution as dmce 
import domolibrary.client.DomoError as dmde

import domolibrary.routes.instance_config_api_client as client_routes

import domolibrary.classes.DomoUser as dmdu


# %% ../../nbs/classes/50_DomoInstanceConfig_ApiClient.ipynb 6
@dataclass
class ApiClient:
    auth: dmda.DomoAuth = field(repr=False)
    id: int
    name: str
    client_id: str  # will be masked in UI
    owner_id: str
    domo_user: dmdu.DomoUser

    authorization_grant_types: List[str]

    scope: List[ApiClient_ScopeEnum]
    description: str = None

    is_invalid: bool = False

    def __eq__(self, other):
        if self.__class__.__name__ != other.__class__.__name__:
            return False

        return self.id == other.id

    @classmethod
    async def _from_json(cls, auth: dmda.DomoAuth, obj):

        domo_user = None
        is_invalid = False
        try:
            domo_user = await dmdu.DomoUser.get_by_id(auth=auth, user_id=obj["user"])

        except dmde.DomoError as e:
            is_invalid = True

        return cls(
            auth=auth,
            id=obj["id"],
            name=obj["name"],
            client_id=obj["clientId"],
            owner_id=obj["user"],
            domo_user=domo_user,
            authorization_grant_types=obj["authorizedGrantTypes"],
            scope=[ApiClient_ScopeEnum[sc.upper()] for sc in obj["scope"]],
            description=obj.get("description"),
            is_invalid=is_invalid,
        )

    @classmethod
    async def get_by_id(
        cls,
        client_id: str,
        auth: dmda.DomoAuth,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
        debug_num_stacks_to_drop: int = 2,
        return_raw: bool = False,
    ):
        res = await client_routes.get_client_by_id(
            client_id=client_id,
            auth=auth,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            session=session,
            parent_class=cls.__name__,
        )

        if return_raw:
            return res

        return await cls._from_json(auth=auth, obj=res.response)

    async def revoke(
        self,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
        debug_num_stacks_to_drop: int = 2,
    ):
        return await client_routes.revoke_api_client(
            auth=self.auth,
            client_id=self.id,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=self.__class__.__name__,
            session=session,
        )

# %% ../../nbs/classes/50_DomoInstanceConfig_ApiClient.ipynb 7
class ApiClient_Search_Error(dmde.ClassError):
    def __init__(self, cls_instance, client_name : str ):
        super().__init__(
            entity_id = "instance_config",
            cls_instance = cls_instance,
            entity_name = client_name,
        )

@dataclass
class ApiClients:
    auth: dmda.DomoAuth

    domo_clients: List[ApiClient] = field(default_factory=lambda: [])

    invalid_clients: List[ApiClient] = field(default_factory=lambda: [])

    async def get(
        self,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
        debug_num_stacks_to_drop=2,
        return_raw: bool = False,
    ):

        res = await client_routes.get_api_clients(
            auth=self.auth,
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

        if return_raw:
            return res

        self.domo_clients = await dmce.gather_with_concurrency(
            *[ApiClient._from_json(auth=self.auth, obj=obj) for obj in res.response],
            n=10
        )

        self.invalid_clients = [
            client for client in self.domo_clients if client.is_invalid
        ]

        return self.domo_clients

    async def get_by_name(
        self,
        client_name: str,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
        debug_num_stacks_to_drop: int = 2,
    ):

        await self.get(
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
        )

        domo_client= next(
            (
                _domo_client
                for _domo_client in self.domo_clients
                if _domo_client.name == client_name
            ), None
        )

        if not domo_client:
            raise ApiClient_Search_Error(cls_instance=self, client_name = client_name)
    
        return domo_client

# %% ../../nbs/classes/50_DomoInstanceConfig_ApiClient.ipynb 11
@patch_to(ApiClients)
async def create_for_authorized_user(
    self,
    client_name: str,
    client_description: str = f"created via DL {dt.date.today()}",
    scope: List[ApiClient_ScopeEnum] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop=2,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
):

    res = await client_routes.create_api_client(
        auth=self.auth,
        client_name=client_name,
        client_description=client_description,
        scope=scope,
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=self.__class__.__name__,
        session=session,
    )

    if return_raw:
        return res

    domo_client = await self.get_by_name(
        client_name=client_name, session=session, debug_api=debug_api
    )
    domo_client.client_id = res.response["client_id"]
    domo_client.client_secret = res.response["client_secret"]

    return domo_client

# %% ../../nbs/classes/50_DomoInstanceConfig_ApiClient.ipynb 14
@patch_to(ApiClients)
async def upsert_client(
    self,
    client_name: str,
    client_description: str = None,
    scope: List[ApiClient_ScopeEnum] = None,
    
    is_regenerate: bool = False,

    session: httpx.AsyncClient = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 2,
):

    domo_client = None

    try:
        domo_client = await self.get_by_name(
            client_name=client_name,
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
        )

    except ApiClient_Search_Error as e:
        pass

    if domo_client:
        if not is_regenerate:
            return domo_client

        await domo_client.revoke(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

    return await self.create_for_authorized_user(
        client_name=client_name, client_description=client_description, scope=scope,
        session = session,
        debug_num_stacks_to_drop = debug_num_stacks_to_drop,
        debug_api = debug_api
    )

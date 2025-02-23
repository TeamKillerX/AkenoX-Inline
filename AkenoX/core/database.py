from datetime import datetime as dt

from motor import motor_asyncio
from motor.core import AgnosticClient
from motor.motor_asyncio import AsyncIOMotorClient

from AkenoX.core.logger import *
from config import *


class Database:
    def __init__(self, uri: str) -> None:
        self.client: AgnosticClient = motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self.client["Akeno"]
        self.env = self.db["env"]
        self.pmpermit = self.db["pmpermit"]

    async def connect(self):
        try:
            await self.client.admin.command("ping")
            LOGS.info(
                f"Database Connection Established!"
            )
        except Exception as e:
            LOGS.info(f"DatabaseErr: {e} ")
            quit(1)

    def get_datetime(self) -> str:
        return dt.now().strftime("%d/%m/%Y - %H:%M")

    async def set_env(self, name: str, value: str) -> None:
        await self.env.update_one(
            {"name": name}, {"$set": {"value": value}}, upsert=True
        )

    async def get_env(self, name: str) -> None:
        if await self.is_env(name):
            data = await self.env.find_one({"name": name})
            return data["value"]
        return None

    async def rm_env(self, name: str) -> None:
        await self.env.delete_one({"name": name})

    async def is_env(self, name: str) -> bool:
        if await self.env.find_one({"name": name}):
            return True
        return False

    async def get_all_env(self) -> list:
        return [i async for i in self.env.find({})]

    async def add_pmpermit(self, client: int, user: int):
        await self.pmpermit.update_one(
            {"client": client, "user": user},
            {"$set": {"date": self.get_datetime()}},
            upsert=True,
        )

    async def rm_pmpermit(self, client: int, user: int):
        await self.pmpermit.delete_one({"client": client, "user": user})

    async def is_pmpermit(self, client: int, user: int) -> bool:
        data = await self.get_pmpermit(client, user)
        return True if data else False

    async def get_pmpermit(self, client: int, user: int):
        data = await self.pmpermit.find_one({"client": client, "user": user})
        return data

    async def get_all_pmpermits(self, client: int) -> list:
        return [i async for i in self.pmpermit.find({"client": client})]

db_client = Database(mongo_url)

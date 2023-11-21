import asyncio
import concurrent.futures

import firebase_admin
from firebase_admin import credentials, db

from credentials.config_reader import config

cred = credentials.Certificate("../credentials/firebase_auth.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': config.firebase_realtime_db.get_secret_value(),
    'storageBucket': config.firebase_storage.get_secret_value()
})

db_executor = concurrent.futures.ThreadPoolExecutor(max_workers=config.db_max_workers)


async def db_get(ref: db.Reference):
    return await asyncio.get_running_loop().run_in_executor(db_executor, ref.get)


async def db_set(ref: db.Reference, value):
    return await asyncio.get_running_loop().run_in_executor(db_executor, ref.set, value)


async def db_push(ref: db.Reference) -> db.Reference:
    return await asyncio.get_running_loop().run_in_executor(db_executor, ref.push)


async def db_update(ref: db.Reference, value):
    return await asyncio.get_running_loop().run_in_executor(db_executor, ref.push, value)


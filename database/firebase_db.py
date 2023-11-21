import asyncio
import concurrent.futures

import firebase_admin
from firebase_admin import credentials
from firebase_admin.db import Reference

from credentials.config_reader import config

cred = credentials.Certificate("../credentials/firebase_auth.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': config.firebase_realtime_db.get_secret_value(),
    'storageBucket': config.firebase_storage.get_secret_value()
})

db_executor = concurrent.futures.ThreadPoolExecutor(max_workers=config.db_max_workers)


async def get_response(ref: Reference):
    return await asyncio.get_running_loop().run_in_executor(db_executor, ref.get)


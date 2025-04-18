import asyncio
import uuid
from typing import Dict

queue = asyncio.Queue()
active_tasks: Dict[str, Dict] = {}


async def add_task(client_id: str, task_data: dict):
    task_id = str(uuid.uuid4())
    full_task = {'task_id': task_id, 'client_id': client_id,
                 'data': task_data, 'status': 'queued'}
    await queue.put(full_task)
    active_tasks[task_id] = full_task

    return task_id


async def run_task(target_format, convert_file):
    asyncio.create_task(
        convert_file(target_format))

    #asyncio.create_task(simulate_conversion(task_id, file.filename, target_format))

async def get_next_task():
    return await queue.get()  # и сразу удаляет из очереди


async def process_tasks(processor):
    while True:
        task_data = await get_next_task()
        task_id = task_data['task_id']

        try:
            active_tasks[task_id]['status'] = 'processing'
            await processor(task_data)
            active_tasks[task_id]['status'] = 'completed'
        except Exception as e:
            active_tasks[task_id]['status'] = 'error'
        finally:
            queue.task_done()


async def get_all_active_tasks():
    return active_tasks


async def remove_task(task_id: str):
    if task_id not in active_tasks:
        return {'error': 'task not found'}

    del active_tasks[task_id]
    return {'status': 'deleted'}

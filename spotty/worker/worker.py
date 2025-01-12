import asyncio
from concurrent.futures import ThreadPoolExecutor
from temporalio.client import Client
from temporalio.worker import Worker as TemporalWorker
from temporalio.common import WorkflowIDConflictPolicy

from spotty.worker.workflows.health_check_workflow import HealthCheckWorkflow

MAX_TEMPORAL_WORKERS = 4


class Worker:
    def __init__(self):
        pass

    async def run(self):
        print("Running...")

        # Connect to Temporal server
        client = await Client.connect("localhost:7233", namespace="default")

        # # Execute the workflow
        # print("Executing workflow...")
        # result = await client.execute_workflow(
        #     HealthCheckWorkflow.run,
        #     args=["my name"],
        #     id="my-workflow-id",
        #     task_queue="my-task-queue",
        #     id_conflict_policy=WorkflowIDConflictPolicy.TERMINATE_EXISTING,
        #     cron_schedule="* * * * *"
        # )
        #
        # print(f"Workflow execution result: {result}")

        # Run the Temporal Worker
        with ThreadPoolExecutor(max_workers=MAX_TEMPORAL_WORKERS) as activity_executor:
            print("Starting worker...")
            worker = TemporalWorker(
                client,
                task_queue="my-task-queue",
                workflows=[HealthCheckWorkflow],
                activity_executor=activity_executor,
            )

            print("running...")
            await worker.run()

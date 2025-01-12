from temporalio import workflow


@workflow.defn
class HealthCheckWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        return f"Hello {name}"

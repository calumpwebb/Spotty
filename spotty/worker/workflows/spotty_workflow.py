from dataclasses import dataclass

from temporalio import workflow

@dataclass
class Args:
    text: str

@dataclass
class Result:
    pass

@workflow.defn
class SpottyWorkflow:

    @workflow.run
    async def run(self, args: Args) -> Result:

        return Result()

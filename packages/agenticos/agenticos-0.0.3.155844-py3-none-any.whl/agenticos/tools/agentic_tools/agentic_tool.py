import json
import logging
import time
from typing import Type

import requests
from crewai_tools import BaseTool
from pydantic import BaseModel, Field
from tenacity import retry, stop_after_delay, wait_fixed

from agenticos.node.models import Job, JobStatus, Workflow

log = logging.getLogger(__name__)


class PlaceHolderSchema(BaseModel): ...


class DirectAgenticNodeTool(BaseTool):
    node_url: str = "http://localhost:8000"
    workflow: str = "research"
    name: str = ""
    description: str = ""
    args_schema: Type[BaseModel] = PlaceHolderSchema

    def __init__(self, **kwargs) -> None:
        try:
            args_schema, name, description = self.queryWorkflow(
                node_url=kwargs["node_url"], workflow=kwargs["workflow"]
            )
            kwargs["name"] = name
            kwargs["description"] = description
            kwargs["args_schema"] = args_schema
        except Exception as e:
            log.error(f"Failed to properly initialize DirectAgenticNodeTool {e}")

        super().__init__(**kwargs)

    def _run(self, **kwargs) -> str:
        # post the argument as request body to the node_uri
        res = requests.post(
            f"{self.node_url}/workflow/{self.workflow}/run", json=kwargs
        )
        tid = res.text.strip('"')

        for _ in range(0, 30):
            res = requests.get(f"{self.node_url}/job/{tid}")
            job = Job.model_validate_json(res.text)
            if job.status != JobStatus.RUNNING:
                return job.output or ""
            time.sleep(1)
        log.error("Job took too long to complete")
        raise Exception("Job took too long to complete")

    @retry(stop=stop_after_delay(30), wait=wait_fixed(2))
    def queryWorkflow(
        self, node_url: str, workflow: str
    ) -> tuple[Type[BaseModel], str, str]:
        try:
            res = requests.get(f"{node_url}/node/description")
            if res.status_code != 200:
                raise Exception("Failed to get node description")
            wfs = json.loads(res.text)
            wf = Workflow(**wfs[workflow])

            fields = {k: Field(..., description=v) for k, v in wf.inputs.items()}
            fields["__annotations__"] = {k: str for k in wf.inputs.keys()}

            Schema = type(
                "AgenticToolSchema",
                (BaseModel,),
                fields,
            )

            return Schema, wf.name, wf.description
        except Exception as e:
            log.warning(f"Failed to query workflow: {e}")
            raise Exception(f"Failed to query workflow: {e}")

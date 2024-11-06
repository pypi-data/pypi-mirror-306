from pydantic import BaseModel, ConfigDict


class KumoBaseConfig(BaseModel):

    model_config = ConfigDict(extra="forbid")

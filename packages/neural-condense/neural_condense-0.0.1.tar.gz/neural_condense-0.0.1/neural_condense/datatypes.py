from pydantic import BaseModel


class CondenseHeader(BaseModel):
    CONDENSE_API_KEY: str


class CondensePayload(BaseModel):
    context: str
    tier: str
    target_model: str
    miner_uid: int = -1
    top_incentive: float = 0.9
    prompt: str = ""


class ClientResponse(BaseModel):
    condensed_tokens: list
    prompt_tokens: list
    inputs_embeds: list

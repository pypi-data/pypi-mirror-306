from .constants import CLIENT_URL, PATHS
from .datatypes import CondenseHeader, CondensePayload, ClientResponse
import httpx
import os
import numpy as np


class CondenseClient:
    def __init__(self, api_key: str = ""):
        api_key = api_key or os.getenv("CONDENSE_API_KEY")
        if not api_key:
            raise ValueError("API key is required")
        self.api_key = api_key
        self.headers = CondenseHeader(CONDENSE_API_KEY=api_key)
        self.client = httpx.Client(base_url=CLIENT_URL)

    def create_condensed_tokens(
        self,
        context: str,
        tier: str,
        target_model: str,
        miner_uid: int = -1,
        top_incentive: float = 0.9,
        prompt: str = "",
    ) -> np.ndarray:
        payload = CondensePayload(
            context=context,
            tier=tier,
            target_model=target_model,
            miner_uid=miner_uid,
            top_incentive=top_incentive,
            prompt=prompt,
        )
        response = self.client.post(
            PATHS["condense"],
            headers=self.headers.model_dump(),
            json=payload.model_dump(),
        )
        response.raise_for_status()
        condensed_tokens = response.json()["condensed_tokens"]
        condensed_tokens = np.array(condensed_tokens)
        prompt_tokens = None
        inputs_embeds = None
        if prompt:
            prompt_tokens = response.json()["prompt_tokens"]
            prompt_tokens = np.array(prompt_tokens)
            inputs_embeds = np.concatenate([condensed_tokens, prompt_tokens], axis=0)
            inputs_embeds = np.expand_dims(inputs_embeds, axis=0)
        print(f"Condensed into {condensed_tokens.shape} tokens")
        return ClientResponse(
            condensed_tokens=condensed_tokens,
            prompt_tokens=prompt_tokens,
            inputs_embeds=inputs_embeds,
        )


class AsyncCondenseClient:
    def __init__(self, api_key: str = ""):
        api_key = api_key or os.getenv("CONDENSE_API_KEY")
        if not api_key:
            raise ValueError("API key is required")
        self.api_key = api_key
        self.headers = CondenseHeader(CONDENSE_API_KEY=api_key)
        self.client = httpx.AsyncClient(base_url=CLIENT_URL)

    async def create_condensed_tokens(
        self,
        context: str,
        tier: str,
        target_model: str,
        miner_uid: int = -1,
        top_incentive: float = 0.9,
        prompt: str = "",
    ) -> np.ndarray:
        payload = CondensePayload(
            context=context,
            tier=tier,
            target_model=target_model,
            miner_uid=miner_uid,
            top_incentive=top_incentive,
            prompt=prompt,
        )
        response = await self.client.post(
            PATHS["condense"],
            headers=self.headers.model_dump(),
            json=payload.model_dump(),
        )
        response.raise_for_status()
        condensed_tokens = response.json()["condensed_tokens"]
        condensed_tokens = np.array(condensed_tokens)
        prompt_tokens = None
        inputs_embeds = None
        if prompt:
            prompt_tokens = response.json()["prompt_tokens"]
            prompt_tokens = np.array(prompt_tokens)
            inputs_embeds = np.concatenate([condensed_tokens, prompt_tokens], axis=0)
            inputs_embeds = np.expand_dims(inputs_embeds, axis=0)
        print(f"Condensed into {condensed_tokens.shape} tokens")
        return ClientResponse(
            condensed_tokens=condensed_tokens,
            prompt_tokens=prompt_tokens,
            inputs_embeds=inputs_embeds,
        )

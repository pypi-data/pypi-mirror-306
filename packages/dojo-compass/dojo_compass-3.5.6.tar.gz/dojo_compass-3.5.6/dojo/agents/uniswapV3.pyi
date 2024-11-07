import abc
from dojo.agents.base_agent import BaseAgent as BaseAgent
from dojo.observations import UniswapV3Observation as UniswapV3Observation

class UniswapV3Agent(BaseAgent[UniswapV3Observation], metaclass=abc.ABCMeta):
    def get_liquidity_ownership_tokens(self) -> list[int]: ...

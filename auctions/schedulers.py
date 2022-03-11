from collections import OrderedDict, defaultdict

from typing import Dict, Iterator, List, Optional, Union, Type
from mesa.agent import Agent
from mesa.model import Model
from mesa.time import BaseScheduler

# BaseScheduler has a self.time of int, while
# StagedActivation has a self.time of float
TimeT = Union[float, int]

class RandomActivationByType(BaseScheduler):
    """
    A scheduler which activates each type of agent once per step, in random
    order, with the order reshuffled every step.

    The `step_type` method is equivalent to the NetLogo 'ask [breed]...' and is
    generally the default behavior for an ABM. The `step` method performs
    `step_type` for each of the agent types.

    Assumes that all agents have a step() method.

    This implementation assumes that the type of an agent doesn't change
    throughout the simulation.

    If you want to do some computations / data collections specific to an agent
    type, you can either:
    - loop through all agents, and filter by their type
    - access via `your_model.scheduler.agents_by_type[your_type_class]`
    """

    def __init__(self, model: Model) -> None:
        super().__init__(model)
        self.agents_by_type = defaultdict(dict)

    def add(self, agent: Agent) -> None:
        """
        Add an Agent object to the schedule

        Args:
            agent: An Agent to be added to the schedule.
        """

        self._agents[agent.unique_id] = agent
        agent_class: Type[Agent] = type(agent)
        self.agents_by_type[agent_class][agent.unique_id] = agent


    def remove(self, agent: Agent) -> None:
        """
        Remove all instances of a given agent from the schedule.
        """

        del self._agents[agent.unique_id]

        agent_class: Type[Agent] = type(agent)
        del self.agents_by_type[agent_class][agent.unique_id]


    def step(self, shuffle_types: bool = True, shuffle_agents: bool = True) -> None:
        """
        Executes the step of each agent type, one at a time, in random order.

        Args:
            shuffle_types: If True, the order of execution of each types is
                           shuffled.
            shuffle_agents: If True, the order of execution of each agents in a
                            type group is shuffled.
        """
        type_keys: List[Type[Agent]] = list(self.agents_by_type.keys())
        if shuffle_types:
            self.model.random.shuffle(type_keys)
        for agent_class in type_keys:
            self.step_type(agent_class, shuffle_agents=shuffle_agents)
        self.steps += 1
        self.time += 1


    def step_type(self, type_class: Type[Agent], shuffle_agents: bool = True) -> None:
        """
        Shuffle order and run all agents of a given type.
        This method is equivalent to the NetLogo 'ask [breed]...'.

        Args:
            type_class: Class object of the type to run.
        """
        agent_keys: List[int] = list(self.agents_by_type[type_class].keys())
        if shuffle_agents:
            self.model.random.shuffle(agent_keys)
        for agent_key in agent_keys:
            self.agents_by_type[type_class][agent_key].step()


    def get_type_count(self, type_class: Type[Agent]) -> int:
        """
        Returns the current number of agents of certain type in the queue.
        """
        return len(self.agents_by_type[type_class].values())
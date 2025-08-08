import dspy
from tools.wikipedia import search_wikipedia, lookup_wikipedia


def create_react_agent(max_iters=20):
    """
    Creates and returns an uncompiled ReAct agent.

    Args:
        max_iters (int): The maximum number of steps the agent can take.

    Returns:
        dspy.ReAct: An instance of the ReAct module.
    """
    instructions = (
        "Find all Wikipedia titles relevant to verifying (or refuting) the claim."
    )
    signature = dspy.Signature("claim -> titles: list[str]", instructions)

    agent = dspy.ReAct(
        signature, tools=[search_wikipedia, lookup_wikipedia], max_iters=max_iters
    )

    return agent

def top5_recall(example, pred, trace=None):
    """
    Calculates the recall of gold titles within the top 5 predicted titles.

    Args:
        example (dspy.Example): The example object with the ground truth.
        pred (dspy.Prediction): The prediction object from the agent.
        trace (object, optional): Used internally by DSPy optimizers.

    Returns:
        float or bool: The recall score, or a boolean for bootstrapping.
    """
    gold_titles = set(example.titles)
    predicted_titles = set(pred.titles[:5])

    if not gold_titles:
        return 1.0 if not predicted_titles else 0.0

    recall = len(gold_titles.intersection(predicted_titles)) / len(gold_titles)

    # During bootstrapping, the metric must return a boolean.
    # We consider the example "correct" if the recall is perfect (1.0).
    if trace is not None:
        return recall >= 1.0

    return recall

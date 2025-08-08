import dspy
import random
from dspy.datasets import DataLoader

def load_hover_data(train_size=100, dev_size=100, test_size=50):
    """
    Loads, processes, and splits the HoVer dataset for 3-hop questions.

    Args:
        train_size (int): The number of examples for the training set.
        dev_size (int): The number of examples for the development set.
        test_size (int): The number of examples for the test set.

    Returns:
        tuple: A tuple containing the trainset, devset, and testset.
    """
    print("Loading HoVer dataset...")

    kwargs = dict(fields=("claim", "supporting_facts", "hpqa_id", "num_hops"), input_keys=("claim",))
    hover_full = DataLoader().from_huggingface(
        dataset_name="hover-nlp/hover",
        split="train",
        trust_remote_code=True,
        **kwargs
    )

    # Filter for 3-hop questions and deduplicate by hpqa_id
    hpqa_ids = set()
    hover_filtered = [
        dspy.Example(
            claim=x.claim,
            titles=list(set([y["key"] for y in x.supporting_facts]))
        ).with_inputs("claim")
        for x in hover_full
        if x["num_hops"] == 3 and x["hpqa_id"] not in hpqa_ids and not hpqa_ids.add(x["hpqa_id"])
    ]

    random.Random(0).shuffle(hover_filtered)

    trainset = hover_filtered[:train_size]
    devset = hover_filtered[train_size : train_size + dev_size]
    testset = hover_filtered[train_size + dev_size : train_size + dev_size + test_size]

    print(f"Dataset loaded: {len(trainset)} train, {len(devset)} dev, {len(testset)} test examples.")

    return trainset, devset, testset


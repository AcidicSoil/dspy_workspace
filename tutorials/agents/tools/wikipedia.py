import dspy

# A simple in-memory cache for retrieved Wikipedia documents
DOCS = {}


def search(query: str, k: int) -> list[str]:
    """
    Searches Wikipedia using a ColBERTv2 retriever and caches the results.

    Args:
        query (str): The search query.
        k (int): The number of results to retrieve.

    Returns:
        list[str]: A list of retrieved documents.
    """
    # Assumes a ColBERTv2 server is running at this URL
    retriever = dspy.ColBERTv2(url="http://20.102.90.50:2017/wiki17_abstracts")
    results = retriever(query, k=k)

    # Extract text and cache it
    passages = [x["text"] for x in results]
    for passage in passages:
        title, text = passage.split(" | ", 1)
        DOCS[title] = text

    return passages


def search_wikipedia(query: str) -> list[str]:
    """
    A tool that returns top-5 search results directly and the titles of the next 25.

    This helps the agent get a quick overview and a broader list of potential leads.
    """
    print(f"TOOL: Searching Wikipedia for '{query}'...")
    topK = search(query, 30)

    # Separate the top 5 from the rest
    top_5_passages = topK[:5]
    next_25_titles = [f"`{x.split(' | ')[0]}`" for x in topK[5:30]]

    return top_5_passages + [
        f"Other retrieved pages have titles: {', '.join(next_25_titles)}."
    ]


def lookup_wikipedia(title: str) -> str:
    """
    A tool that returns the full text of a Wikipedia page given its exact title.

    It first checks the cache and then performs a targeted search if necessary.
    """
    print(f"TOOL: Looking up Wikipedia page '{title}'...")
    if title in DOCS:
        return DOCS[title]

    # If not in cache, perform a specific search for the title
    results = [x for x in search(title, 10) if x.startswith(title + " | ")]

    if not results:
        return f"No Wikipedia page found for title: {title}"

    return results[0]

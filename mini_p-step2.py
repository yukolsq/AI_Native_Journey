def _validate_inputs(movie_title: str, what_if_scenario: str) -> tuple[bool, str]:
    """
    Performs basic validation on the movie title and what-if scenario.

    Args:
        movie_title (str): The title of the movie.
        what_if_scenario (str): The "what if" scenario.

    Returns:
        tuple[bool, str]: A tuple containing:
                          - True if inputs are valid, False otherwise.
                          - An empty string if valid, or an error message if invalid.
    """
    if not movie_title.strip() and not what_if_scenario.strip():
        return False, "Both movie title and scenario cannot be empty."
    elif not movie_title.strip():
        return False, "Movie title cannot be empty."
    elif not what_if_scenario.strip():
        return False, "What If scenario cannot be empty."
    return True, ""

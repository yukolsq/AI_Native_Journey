def _generate_narrative(movie_title: str, what_if_scenario: str, api_key: str) -> dict:
    """
    Generates a creative "what if" story and identifies key scenes using the gemini-2.0-flash AI model.

    Args:
        movie_title (str): The title of the movie.
        what_if_scenario (str): The "what if" scenario for the story.
        api_key (str): Your Google Cloud API key for accessing the Gemini API.

    Returns:
        dict: A dictionary containing the generated story's title, narrative, and scene descriptions.
              Example:
              {
                  "title": "New Story Title",
                  "narrative": "The full story text...",
                  "scenes": [
                      {"description": "Description for scene 1"},
                      {"description": "Description for scene 2"},
                      {"description": "Description for scene 3"}
                  ]
              }

    Raises:
        Exception: If the API call fails, returns an unexpected status, or the JSON
                   response is malformed or missing expected data.
    """
    narrative_prompt = f"""Generate a creative "what if" story for the movie "{movie_title}" based on the scenario: "{what_if_scenario}". The story should be between 150-300 words.
    Also, identify 2-3 key scenes from this new narrative that would be visually striking. For each scene, provide a brief, vivid description (max 20 words) suitable for image generation.
    Return the output as a JSON object with the following structure:
    {json.dumps({
        "title": "New Story Title",
        "narrative": "The full story text...",
        "scenes": [
            {"description": "Description for scene 1"},
            {"description": "Description for scene 2"},
            {"description": "Description for scene 3"}
        ]
    }, indent=4)}
    """

    chat_history = [{"role": "user", "parts": [{"text": narrative_prompt}]}]

    payload = {
        "contents": chat_history,
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "OBJECT",
                "properties": {
                    "title": {"type": "STRING"},
                    "narrative": {"type": "STRING"},
                    "scenes": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "description": {"type": "STRING"}
                            }
                        }
                    }
                },
                "propertyOrdering": ["title", "narrative", "scenes"]
            }
        }
    }

    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    try:
        response = requests.post(api_url, headers={'Content-Type': 'application/json'}, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

        # The API returns the JSON as a string within the 'text' part
        result = response.json()
        if not (result and result.get('candidates') and result['candidates'][0].get('content') and
                result['candidates'][0]['content'].get('parts') and result['candidates'][0]['content']['parts'][0].get('text')):
            raise Exception("Unexpected API response structure or missing content from narrative generation.")

        json_string = result['candidates'][0]['content']['parts'][0]['text']
        parsed_result = json.loads(json_string)

        # Basic validation of the parsed structure
        if not all(k in parsed_result for k in ["title", "narrative", "scenes"]):
            raise Exception("Parsed JSON from narrative generation is missing required fields (title, narrative, or scenes).")
        if not isinstance(parsed_result["scenes"], list):
            raise Exception("Scenes field from narrative generation is not a list.")

        return parsed_result

    except requests.exceptions.RequestException as e:
        raise Exception(f"API request for narrative generation failed: {e}")
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to decode JSON response from narrative API: {e}")
    except Exception as e:
        raise Exception(f"An error occurred during narrative generation: {e}")
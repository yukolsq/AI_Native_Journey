import requests
import json
import base64

# --- Helper Functions (Corresponding to Client-Side Logic) ---

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


# --- AI API Interaction Functions ---

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

def _generate_image(scene_description: str, api_key: str) -> str:
    """
    Generates a base64 encoded image for a given scene description using the imagen-3.0-generate-002 model.

    Args:
        scene_description (str): The descriptive text for the image to be generated.
        api_key (str): Your Google Cloud API key for accessing the Imagen API.

    Returns:
        str: A base64 encoded string of the generated image.

    Raises:
        Exception: If the image API call fails or returns an unexpected response.
    """
    image_payload = { "instances": { "prompt": scene_description }, "parameters": { "sampleCount": 1} }
    image_api_url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={api_key}"

    try:
        image_response = requests.post(image_api_url, headers={'Content-Type': 'application/json'}, json=image_payload)
        image_response.raise_for_status() # Raise an exception for HTTP errors

        image_result = image_response.json()

        if image_result.get('predictions') and len(image_result['predictions']) > 0 and image_result['predictions'][0].get('bytesBase64Encoded'):
            return image_result['predictions'][0]['bytesBase64Encoded']
        else:
            raise Exception("Failed to generate image or unexpected image API response structure.")

    except requests.exceptions.RequestException as e:
        raise Exception(f"API request for image generation failed: {e}")
    except Exception as e:
        raise Exception(f"An error occurred during image generation: {e}")

# --- Main Orchestration Function ---

def generate_what_if_story_full(movie_title: str, what_if_scenario: str, api_key: str) -> dict:
    """
    Orchestrates the full "What If" story generation process, including input validation,
    narrative generation, and image generation for key scenes.

    Args:
        movie_title (str): The title of the movie.
        what_if_scenario (str): The "what if" scenario for the story.
        api_key (str): Your Google Cloud API key for accessing the AI APIs.

    Returns:
        dict: A dictionary containing the full story details and base64 encoded images.
              Example:
              {
                  "success": True,
                  "message": "Story and scenes generated successfully.",
                  "data": {
                      "title": "New Story Title",
                      "narrative": "The full story text...",
                      "scenes": [
                          {"description": "Scene 1 description", "image_base64": "base64_data_for_image_1"},
                          {"description": "Scene 2 description", "image_base64": "base64_data_for_image_2"}
                      ]
                  }
              }
              Or for failure:
              {
                  "success": False,
                  "message": "Error message details."
              }
    """
    # 1. Input Validation
    is_valid, error_message = _validate_inputs(movie_title, what_if_scenario)
    if not is_valid:
        return {"success": False, "message": error_message}

    try:
        # 2. AI-Driven Narrative Generation
        story_data = _generate_narrative(movie_title, what_if_scenario, api_key)
        
        # 3. AI-Generated Key Scene Visuals
        scenes_with_images = []
        for scene in story_data.get("scenes", []):
            try:
                image_base64 = _generate_image(scene["description"], api_key)
                scenes_with_images.append({
                    "description": scene["description"],
                    "image_base64": image_base64
                })
            except Exception as e:
                # Log image generation errors but don't stop the whole process
                print(f"Warning: Could not generate image for scene '{scene['description']}': {e}")
                scenes_with_images.append({
                    "description": scene["description"],
                    "image_base64": None, # Indicate failure for this image
                    "error": str(e)
                })

        story_data["scenes"] = scenes_with_images # Update scenes with image data

        return {
            "success": True,
            "message": "Story and scenes generated successfully.",
            "data": story_data
        }

    except Exception as e:
        return {"success": False, "message": f"An error occurred during story generation: {e}"}


# Example Usage (replace "YOUR_API_KEY" with your actual key)
if __name__ == "__main__":
    # You would typically load the API key from environment variables in a real application
    # For testing purposes, you can paste it here, but DO NOT hardcode it in production code.
    api_key = "YOUR_API_KEY"
    if api_key == "YOUR_API_KEY":
        print("Please replace 'YOUR_API_KEY' with your actual Google Cloud API key to run this example.")
    else:
        movie_title_example = "Inception"
        what_if_scenario_example = "What if Cobb chose to stay in limbo with Mal?"
        
        print(f"Generating story for '{movie_title_example}' with scenario '{what_if_scenario_example}'...")
        result = generate_what_if_story_full(movie_title_example, what_if_scenario_example, api_key)
        
        if result["success"]:
            data = result["data"]
            print("\n--- Generated Story ---")
            print(f"Title: {data['title']}")
            print(f"Narrative:\n{data['narrative']}")
            print("\n--- Key Scenes ---")
            for i, scene in enumerate(data['scenes']):
                print(f"Scene {i+1}: {scene['description']}")
                if scene['image_base64']:
                    # In a real web app, you'd send this base64 to the frontend to display
                    print(f"  Image data generated (base64 length: {len(scene['image_base64'])} bytes)")
                    # You could optionally save it to a file for local inspection:
                    # with open(f"scene_{i+1}.png", "wb") as f:
                    #     f.write(base64.b64decode(scene['image_base64']))
                    # print(f"  Image saved as scene_{i+1}.png")
                else:
                    print(f"  Image generation failed for this scene: {scene.get('error', 'Unknown error')}")
        else:
            print(f"\nError: {result['message']}")


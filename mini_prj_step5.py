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
    # api_key = "YOUR_API_KEY"
    # if api_key == "YOUR_API_KEY":
    #     print("Please replace 'YOUR_API_KEY' with your actual Google Cloud API key to run this example.")
    # else:
    #     movie_title_example = "Inception"
    #     what_if_scenario_example = "What if Cobb chose to stay in limbo with Mal?"
    #     
    #     print(f"Generating story for '{movie_title_example}' with scenario '{what_if_scenario_example}'...")
    #     result = generate_what_if_story_full(movie_title_example, what_if_scenario_example, api_key)
    #     
    #     if result["success"]:
    #         data = result["data"]
    #         print("\n--- Generated Story ---")
    #         print(f"Title: {data['title']}")
    #         print(f"Narrative:\n{data['narrative']}")
    #         print("\n--- Key Scenes ---")
    #         for i, scene in enumerate(data['scenes']):
    #             print(f"Scene {i+1}: {scene['description']}")
    #             if scene['image_base64']:
    #                 # In a real web app, you'd send this base64 to the frontend to display
    #                 print(f"  Image data generated (base64 length: {len(scene['image_base64'])} bytes)")
    #                 # You could optionally save it to a file for local inspection:
    #                 # with open(f"scene_{i+1}.png", "wb") as f:
    #                 #     f.write(base64.b64decode(scene['image_base64']))
    #                 # print(f"  Image saved as scene_{i+1}.png")
    #             else:
    #                 print(f"  Image generation failed for this scene: {scene.get('error', 'Unknown error')}")
    #     else:
    #         print(f"\nError: {result['message']}")
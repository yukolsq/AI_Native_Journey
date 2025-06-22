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

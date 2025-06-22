
### Very Concise Explanation of Python Refactored Code

This Python script handles the backend logic for the "What If" story generator, making AI API calls. The JavaScript frontend would consume data from these functions.

**Overall Logic:** `generate_what_if_story_full` orchestrates the process: validates input, gets narrative/scenes from one AI, then generates images for each scene using another AI.

---

### 1. `_validate_inputs(movie_title, what_if_scenario)`

* **Purpose:** Checks if movie title and scenario inputs are non-empty.
* **Logic:** Simple string empty/whitespace checks.
* **Returns:** `(is_valid: bool, error_message: str)`.

### 2. `_generate_narrative(movie_title, what_if_scenario, api_key)`

* **Purpose:** Gets story/scene descriptions from `gemini-2.0-flash`.
* **Logic:** Prompts AI for story (150-300 words), 2-3 visual scene descriptions, and enforces specific JSON output structure. Calls API, parses JSON.
* **Returns:** `dict` with `title`, `narrative`, `scenes`.
* **Error Handling:** API/JSON parsing errors.

### 3. `_generate_image(scene_description, api_key)`

* **Purpose:** Generates a base64 image for a scene using `imagen-3.0-generate-002`.
* **Logic:** Prompts AI with scene description. Calls API, extracts base64 string.
* **Returns:** `base64_image_string: str`.
* **Error Handling:** API/image generation errors.

### 4. `generate_what_if_story_full(movie_title, what_if_scenario, api_key)`

* **Purpose:** Main orchestrator.
* **Logic:**
    1.  Validates inputs (via `_validate_inputs`).
    2.  Gets story/scenes (via `_generate_narrative`).
    3.  Loops through scenes, generating images (via `_generate_image`) for each.
    4.  Aggregates all story and image data.
* **Returns:** `dict` with `success` (bool), `message` (str), and `data` (dict including narrative and scenes with image data).
* **Error Handling:** Catches and reports overall process errors.

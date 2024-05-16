<div style="color: #2E86C1; font-size: 1.5em;">
    # soro_benin_hackathon
</div>
<div style="color: #2C3E50; font-size: 1em;">
    This application is based on technique presented in Linux Foundation's Open Source summit at Seattle: "Translation Augmented Generation" <br>
    Link: https://sched.co/1aBOj <br>
    by : Raghavan Muthuregunathan
</div>

# Sọrọ Benin: Afara Ede

Sọrọ Benin: Afara Ede is a Streamlit application that allows users to ask questions or describe images in any language and get responses in the local Benin language or generate images based on the descriptions.

## Features

- Translate text from any language to English
- Generate responses in the local Benin language based on the translated English text
- Generate images based on descriptions in any language
- Detect the input language and provide translated responses

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/soro-benin.git
    cd soro-benin
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the Streamlit application:
    ```sh
    streamlit run app.py
    ```

2. Open the application in your browser (typically at `http://localhost:8501`).

3. Select the mode (Text Mode or Image Mode) and enter the text you want to translate or describe for image generation.

4. Click the "Submit" button to get the response or generated image.

## Project Structure

- `app.py`: The main Streamlit application file.
- `requirements.txt`: The list of dependencies required for the project.

## API Keys

This application uses several APIs that require authentication. Ensure you have the appropriate API keys and add them to your environment variables or directly in the code:

- OpenAI API key for translations and language detection
- Replicate API key for image generation
- Perplexity API key for generating text responses

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- [Streamlit](https://streamlit.io/) for the easy-to-use framework for creating web applications.
- [OpenAI](https://www.openai.com/) for the powerful language models.
- [Replicate](https://replicate.com/) for the image generation API.
- [Perplexity](https://www.perplexity.ai/) for the text generation API.

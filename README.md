# Image Captioner Bot

**Image Captioner Bot** is a creative Streamlit application that transforms your uploaded images into vivid, expressive captions. Powered by [Agno](https://github.com/agno-agi/agno) and OpenAI's GPT-4o, the bot blends visual interpretation with user-defined tone, style, and perspective—bringing your images to life through storytelling.

## Folder Structure

```
Image-Captioner-Bot/
├── image-captioner-bot.py
├── README.md
└── requirements.txt
```

- **image-captioner-bot.py**: The main Streamlit application.
- **requirements.txt**: Required Python packages.
- **README.md**: This documentation file.

## Features

- **Image Upload & Preference Input**  
  Upload your image and customize the caption's tone, style, perspective, and word count.

- **Agent-Powered Caption Generation**  
  The captioning agent analyzes the image and generates a compelling, descriptive caption aligned with your chosen preferences.

- **Two-Column Visual Output**  
  See your uploaded image and the generated caption side-by-side in a clean, intuitive layout.

- **Download Option**  
  Save your caption with the **📥 Download Caption** button.

- **Minimal Streamlit UI**  
  Lightweight, distraction-free layout built with Streamlit’s wide mode and custom styling for better readability.

## Prerequisites

- Python 3.11 or higher  
- An OpenAI API key ([Get one here](https://platform.openai.com/account/api-keys))

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/akash301191/Image-Captioner-Bot.git
   cd Image-Captioner-Bot
   ```

2. **(Optional) Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate        # On macOS/Linux
   # or
   venv\Scripts\activate           # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the app**:
   ```bash
   streamlit run image-captioner-bot.py
   ```

2. **In your browser**:
   - Add your OpenAI API key in the sidebar.
   - Upload an image and choose your caption style, tone, length, and perspective.
   - Click **🖋️ Generate Caption** to view the result.
   - Download the caption if desired.

---

## Code Overview

- **`render_caption_preferences()`**: Lets the user upload an image and select stylistic preferences.
- **`render_sidebar()`**: Captures and stores the OpenAI API key securely in Streamlit's session state.
- **`generate_caption()`**:  
  - Initializes an agent using Agno and OpenAI.  
  - Builds a prompt based on user inputs.  
  - Sends the image and prompt to the agent and returns the response.
- **`main()`**: Renders the UI, manages user flow, and displays the final image + caption output.

## Contributions

Contributions are welcome! Feel free to fork the repo, suggest features, report bugs, or open a pull request. Make sure your changes are clean, purposeful, and well-tested.
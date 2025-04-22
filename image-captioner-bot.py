import tempfile
import streamlit as st
from agno.agent import Agent
from agno.media import Image
from agno.models.openai import OpenAIChat

def render_sidebar():
    st.sidebar.title("🔐 API Configuration")
    st.sidebar.markdown("---")

    # OpenAI API Key input
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://platform.openai.com/account/api-keys)."
    )
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
        st.sidebar.success("✅ OpenAI API key updated!")

    st.sidebar.markdown("---")


def render_caption_preferences():
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    # Column 1: Image Upload
    with col1:
        st.subheader("🖼️ Upload Image")
        uploaded_image = st.file_uploader(
            "Choose an image to caption", 
            type=["jpg", "jpeg", "png"]
        )

    # Column 2: Caption Style & Tone
    with col2:
        st.subheader("🎨 Caption Style")
        caption_style = st.selectbox(
            "How would you like the caption to feel?",
            ["Descriptive and clear", "Poetic and reflective", "Warm and emotional",
             "Thoughtful and insightful", "Playful and fun"]
        )

        caption_tone = st.selectbox(
            "What kind of tone do you prefer in the caption?",
            ["Light-hearted", "Elegant", "Mysterious", "Uplifting", "Neutral"]
        )

    # Column 3: Perspective & Caption Length
    with col3:
        st.subheader("🖋️ Caption Preferences")
        caption_length = st.selectbox(
            "Preferred caption length",
            [
                "Very short (under 10 words)",
                "Short (10–20 words)",
                "Medium (20–40 words)",
                "Long (40–80 words)",
                "Very long (80+ words)"
            ]
        )
        
        perspective = st.selectbox(
            "Do you want the caption in first or third person?",
            ["First person", "Third person", "No preference"]
        )

        

    return {
        "uploaded_image": uploaded_image,
        "caption_style": caption_style,
        "caption_tone": caption_tone,
        "perspective": perspective,
        "caption_length": caption_length
    }

def generate_caption(preferences):
    # Save uploaded image to a temporary file
    uploaded_image = preferences["uploaded_image"]
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(uploaded_image.getvalue())
        image_path = tmp.name

    # Extract user preferences
    style = preferences["caption_style"]
    tone = preferences["caption_tone"]
    perspective = preferences["perspective"]
    length = preferences["caption_length"]

    # Map caption length preference to prompt wording
    length_instruction = {
        "Very short (under 10 words)": "Keep the caption under 10 words.",
        "Short (10–20 words)": "Keep the caption between 10 and 20 words.",
        "Medium (20–40 words)": "Write a caption between 20 and 40 words.",
        "Long (40–80 words)": "Write a detailed caption between 40 and 80 words.",
        "Very long (80+ words)": "Write an elaborate caption with more than 80 words."
    }[length]

    # Setup agent
    agent = Agent(
        model=OpenAIChat(id="gpt-4o", api_key=st.session_state.openai_api_key),
        markdown=True,
        name="Image Captioner",
        role="Generates thoughtful, expressive captions based on the visual elements of an image and user's desired tone and style.",
        description="You're an expert visual storyteller who crafts rich captions for images, balancing description with creativity based on user input."
    )

    # Construct the prompt
    prompt = f"""
    Please write a caption for the uploaded image.

    The user prefers a caption that feels **{style.lower()}** with a **{tone.lower()}** tone.
    It should be written in **{perspective.lower()}** perspective.
    
    {length_instruction}
    """

    # Generate caption using the agent
    response = agent.run(
        prompt.strip(),
        images=[Image(filepath=image_path)]
    )

    return response.content


def main() -> None:
    # Page config
    st.set_page_config(page_title="Image Captioner Bot", page_icon="🖼️", layout="wide")

    # Custom styling
    st.markdown(
        """
        <style>
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        div[data-testid="stTextInput"] {
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header and intro
    st.markdown("<h1 style='font-size: 2.5rem;'>🖼️ Image Captioner Bot</h1>", unsafe_allow_html=True)
    st.markdown(
        "Welcome to Image Captioner Bot — a creative Streamlit tool that transforms your uploaded images into vivid, descriptive captions, blending visual perception with storytelling flair.",
        unsafe_allow_html=True
    )

    render_sidebar()
    preferences = render_caption_preferences()

    st.markdown("---")

    if st.button("🖋️ Generate Caption"):
        if not hasattr(st.session_state, "openai_api_key"):
            st.error("Please provide your OpenAI API key in the sidebar.")
        elif not preferences["uploaded_image"]:
            st.error("Please upload an image to proceed.")
        else:
            with st.spinner("Generating a caption for your image..."):
                caption = generate_caption(preferences)

                # Save to session state
                st.session_state.caption = caption
                st.session_state.image = preferences["uploaded_image"]

    # Display image and caption if available
    if "caption" in st.session_state and "image" in st.session_state:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("## 🖼️ Uploaded Image")
            st.image(st.session_state.image, use_container_width=False)

        with col2:
            st.markdown("## ✨ Generated Caption")
            st.write(st.session_state.caption)

        st.markdown("---")

        st.download_button(
            label="📥 Download Caption",
            data=st.session_state.caption,
            file_name="caption.txt",
            mime="text/plain"
        )

if __name__ == "__main__": 
    main()
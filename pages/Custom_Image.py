import os
import time
import PIL.Image
import base64
import requests
import streamlit as st
import json
from PIL import Image  # Import Pillow library for JpegImageFile

# OpenAI API Key
#api_key = st.secrets["API_key"]
api_key = os.getenv("API_key")

# Function to encode the imaxerge
def encode_image(image_data):
    return base64.b64encode(image_data).decode('utf-8')

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

def app():

    # Create two columns
    col1, col2 = st.columns([1, 4])

    # Display the image in the left column
    with col1:
        st.image("wvsu-logo.jpg")

    # Display the title in the right column
    with col2:
        st.subheader("Automated Essay Scoring System using GPT-4 Model")

    text = """Prof. Louie F. Cervantes, M. Eng. (Information Engineering) \n
    CCS 229 - Intelligent Systems
    Department of Computer Science
    College of Information and Communications Technology
    West Visayas State University
    """
    with st.expander("Click to display developer information."):
        st.text(text)
        link_text = "Click here to visit [OpenAI](https://openai.com/)"
        st.write(link_text)

    st.subheader("From Tedious Grading to Personalized Feedback: Unleashing the Power of Automated Essay Scoring")
    text = """Traditionally, grading essays has been a time-consuming manual process for educators. 
    Now, with the help of advanced technology like GPT-4}, we can transform essay scoring.
    The AI teaching copilot analyzes images of handwritten essays and generates both a score and individualized 
    feedback for improvement.
    This innovative approach saves educators valuable time while providing students with actionable 
    insights to enhance their writing skills."""
    
    st.write(text)

    # Create a file uploader widget
    uploaded_file = st.sidebar.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        #image = PIL.Image.open(uploaded_file)
        question = st.text_area("Enter the essay question:")
        scoring_rubric = st.text_area("Enter the scoring rubric:")

        prompt = """You are a language teacher. The essay question is
        {question} Use the scoring rubric: {scoring_rubric} Score the essay 
        response found in this image out of a perfect score of 100. 
        Point out significant errors. Provide feedback and suggestions for improvement."""

        image_data = uploaded_file.read()
        base64_image = encode_image(image_data)
    else:
        st.error("Please upload an image file.")
        return

    payload = {
    "model": "gpt-4-turbo",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": prompt
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 2048,
    }    

    # Button to generate response
    if st.button("Score Essay"):
        progress_bar = st.progress(0, text="The AI teacher co-pilot is processing the request, please wait...")
       
        # Generate response from emini
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        # Display the response
        content = response.json()
                
        st.write(f"AES Copilot: {content['choices'][0]['message']['content']}")
        #st.write(response.json())

        # update the progress bar
        for i in range(100):
            # Update progress bar value
            progress_bar.progress(i + 1)
            # Simulate some time-consuming task (e.g., sleep)
            time.sleep(0.01)
        # Progress bar reaches 100% after the loop completes
        st.success("AI teacher co-pilot task completed!") 

#run the app
if __name__ == "__main__":
  app()

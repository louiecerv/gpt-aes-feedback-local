import os
import time
import PIL.Image
import base64
import requests
import streamlit as st
import json

# OpenAI API Key
#api_key = st.secrets["API_key"]
api_key = os.getenv("API_key")

# Function to encode the imaxerge
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

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

    options = ['Sample 1', 'Sample 2', 'Sample 3', 'Sample 4', 'Sample 5', 'Sample 6', 'Sample 7']
  
    selected_option = st.sidebar.selectbox(
    label="Select an essay sample to use:",
    options=options,
    index=0  # Optionally set a default selected index
    )

    if selected_option == 'Sample 1':
        filename = "01.jpg"
    elif selected_option == 'Sample 2':
        filename = "02.jpg"
    elif selected_option == 'Sample 3':
        filename = "03.jpg"
    elif selected_option == 'Sample 4':
        filename = "04.jpg"
    elif selected_option == 'Sample 5':
        filename = "05.jpg"
    elif selected_option == 'Sample 6':
        filename = "06.jpg"
    elif selected_option == 'Sample 7':
        filename = "07.jpg"
    
    img = PIL.Image.open('./essays/' + filename)

    base64_image = encode_image('./essays/' + filename)
    st.image(img, caption="Essay Response", use_column_width=True)
    
    prompt = """You are a language teacher.  Score the essay response 
    found in this image out of a perfect score of 100.  
    Point out significant errors. 
    Provide feedback and suggestions for improvement."""

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

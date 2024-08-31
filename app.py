import streamlit as st
import openai
from openai import OpenAI
import requests
from io import BytesIO
import base64
import replicate
import json
st.set_page_config(layout="wide")

client = OpenAI()

def translate_to_english(text):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful translator to English."},
            {"role": "user", "content": "Translate it to English. Tamil language: " + text + " Strictly output English translation ONLY"}
        ])
    return response.choices[0].message.content

def detect_n_translate(english_response, original_input):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful language detector."},
            {"role": "user", "content": original_input +" What is the language? Answer should be JUST THE NAME OF THE LANGUAGE in 1 word"}
        ])
    language =  response.choices[0].message.content
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful translator from English to " + language},
            {"role": "user", "content": original_input +"Translate the following English content to Tamil Language: " + language + " English: " + english_response + " output only translated content." }
        ])
    return (language, response.choices[0].message.content)

def generate_image(description):
    english = translate_to_english(description)
    prompt = description + " " + english
    URL = get_replicate_url(prompt)
    return URL #"https://i.imgur.com/EVnWtrA.jpeg"


def get_perplexity_response(input):
    question = input
    url = "https://api.perplexity.ai/chat/completions"
    print(question)
    payload = {
    "model": "llama-3-sonar-large-32k-online",
    "messages": [
        {
            "role": "system",
            "content": "Answer accurately"
        },
        {
            "role": "user",
            "content": question
        }
    ]
    }
    headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Bearer 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"
    }
    response = requests.post(url, json=payload, headers=headers)
    print (response.text)
    print (type(response.text))
    responseD = json.loads(response.text)

    return responseD["choices"][0]["message"]["content"]



def get_replicate_url(description):
    output = replicate.run(
        "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
        input={
            "width": 768,
            "height": 768,
            "prompt": description,
            "refine": "expert_ensemble_refiner",
            "scheduler": "K_EULER",
            "lora_scale": 0.6,
            "num_outputs": 1,
            "guidance_scale": 7.5,
            "apply_watermark": False,
            "high_noise_frac": 0.8,
            "negative_prompt": "",
            "prompt_strength": 0.8,
            "num_inference_steps": 25
            }
        )
    print(output)
    return output[0]

st.title("தமிழ் மொழியில் கேளுங்கள்: சோரில் தமிழில் பதில் பெறுங்கள்")
st.markdown("Raghavan Muthuregunathan என்பவரால் உருவாக்கப்பட்டது")
st.markdown("- நீங்கள் எந்தவொரு கேள்வியையும் தமிழ் மொழியில் கேட்டு, either உருவாக்கிய படத்தை பெறலாம் அல்லது பதிலை பெறலாம்")
st.markdown("- நீங்கள் தமிழில் கேட்கலாம் மற்றும் either படம் உருவாக்க அல்லது பதிலை பெறலாம்")
st.markdown("- நீங்கள் உங்களுக்குத் தேவையான பதிலை தமிழில் பெறலாம்")

mode = st.radio("பயன்முறை தேர்வு:", ("Generate Image", "Answer question"))

example1 = "பருத்தி தாவரங்களில் பூச்சிகள் தாக்கத்தை குறைப்பதற்கான சிறந்த முறைகள் எவை?"
example2 = "காய்கறிகளை தக்கவைத்து வளர்க்க சிறந்த முறைகள் என்ன?"
example3 = "தேன் வியாபாரம் மூலம் தமிழ்நாட்டில் சிறப்பான வருமானம் ஈட்டுவது எப்படி?"
st.markdown("- " + example1)
st.markdown("- " + example2)
st.markdown("- " + example3)

input_text = st.text_area("பட உருவாக்கத்திற்காக கேள்வியை அல்லது விவரத்தை தமிழில் உள்ளீடு செய்யவும்:")

if st.button("submit"):
    if input_text:
        if mode == "உரையியல் முறை":
            translated_text = translate_to_english(input_text)
            english_response = get_perplexity_response(translated_text)
            st.subheader("தமிழில் பதில்:")
            (local_language, local_response) = detect_n_translate(english_response, input_text)
            st.write(local_response)
            st.markdown('<font color="red" size="small">LLMs பலமுறை தவறாக பதிலளிக்கின்றன</font>', unsafe_allow_html=True)            
            st.write("\n\n-------\n")
            with st.expander("Debug output"):
                st.write("ஆங்கிலத்தில் உள்ளீடு:" + translated_text.strip())
                st.write(english_response)
                st.write("---------")
                st.write("கண்டறியப்பட்ட மொழி:" + local_language)

        elif mode == "படமுறை":
            image_url = generate_image(input_text)
            if image_url:
                st.subheader("உருவாக்கப்பட்ட படம்:")
                st.image(image_url)
            else:
                st.error("படம் உருவாக்க இயலவில்லை.")
    else:
        st.error("பதிலை பெற நீங்கள் ஏதேனும் உள்ளீடு செய்ய வேண்டும்.")

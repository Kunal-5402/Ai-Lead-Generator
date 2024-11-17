import re
import json
from PIL import Image
import streamlit as st
from st_audiorec import st_audiorec

import vlm
from llm import LLM
from transcribe import speech_to_text
from text_processing import extract_json

    
def intent_detection(user_query: str):
    try:
        with open("assets/function_calling_prompt.txt","r") as file:
            system_prompt = file.read()
        ans = llm.generate(user_query=user_query,system_prompt=system_prompt)
        data = extract_json(ans)
        return data
    except Exception as e:
        raise RuntimeError(f"Problem in Intent Detection: {e}")

def intent_invoking(user_query: str, file_name: str):
    with open(f"intents/{file_name}.txt","r") as file:
        system_prompt = file.read()

    ans = llm.generate(user_query=user_query,system_prompt=system_prompt)
    data = extract_json(ans)
    return data


def main(wav_audio_data):
    if wav_audio_data is not None:
        text = transcriber.transcribe(file_name)
        tool = intent_detection(user_query=text['text'])
        intent = tool['intent']
        
        print(text['text'])
        print(intent)


        if not text['text'].strip():
            text['text'] = "No audio was provided!"

        if "messages" not in st.session_state:
            st.session_state.messages = []

        st.session_state.messages.append({'role': 'user', 'content': text["text"]})

        for message in st.session_state.messages:
            if message['role'] == 'user':
                with st.chat_message("user"):
                    st.write(message['content'])
            else:
                with st.chat_message("assistant"):
                    st.write(message['content'])

        if intent == "extract_contact_details":
            response = intent_invoking(user_query=text['text'] ,file_name=intent)
            data  = response
            st.session_state.messages.append({'role': 'assistant', 'content': data})
            with st.chat_message("assistant"):
                st.write(data)

        elif intent == "create_shopping_list":
            response = intent_invoking(user_query=text['text'] ,file_name=intent)
            data = {}
            for i, item in enumerate(response['items']):
                data[i+1] = item
            st.session_state.messages.append({'role': 'assistant', 'content': data})
            with st.chat_message("assistant"):
                st.write(data)

        elif intent == "create_todo_list":
            response = intent_invoking(user_query=text['text'] ,file_name=intent)
            data = {}
            for i, task in enumerate(response['tasks']):
                data[i+1] = task
            st.session_state.messages.append({'role': 'assistant', 'content': data})
            with st.chat_message("assistant"):
                st.write(data)

        elif intent == "turn_on_camera":
            picture = st.camera_input(label="Take a Photo")

            if picture is not None:
                image = Image.open(picture)
                image.save("captured_photo.jpg")
                
                with open("intents/turn_on_camera.txt", "r") as file:
                    system_prompt = file.read()

                llm = vlm.LLM()
                ans = llm.generate(image_path="captured_photo.jpg", system_prompt=system_prompt)

                print(ans)

                data = extract_json(ans)
                st.session_state.messages.append({'role': 'assistant', 'content': data})
                with st.chat_message("assistant"):
                    st.write(data)

        else:
            data  = "Sorry! I can't help with your query"
            st.session_state.messages.append({'role': 'assistant', 'content': data})
            with st.chat_message("assistant"):
                st.write(data)

if __name__ == "__main__":
    st.title("AI Lead Generator")
    llm = LLM()
    transcriber = speech_to_text()
    wav_audio_data = st_audiorec()
    file_name = 'audio.wav'
    if wav_audio_data is not None:
        with open(file_name, mode='wb') as f:
            f.write(wav_audio_data)
    main(wav_audio_data) 
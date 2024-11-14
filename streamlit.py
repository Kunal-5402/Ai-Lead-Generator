from llm import LLM
from transcribe import speech_to_text

import re
import json
import streamlit as st
from st_audiorec import st_audiorec


def extract_json(response: str):
    try:
        pattern = r'```json(.*?)```'
        match = re.search(pattern, response, flags=re.DOTALL)
        if match:
            json_data = match.group(1)
            data = json.loads(json_data)
            return data
        else:
            raise ValueError("No JSON code block found in the response.")
    except Exception as e:
        raise RuntimeError(f"An error occurred during extracting JSON: {e}")

def transcribe_and_extract():
    #transcribe
    text = transcriber.transcribe(file_name)
    print(text)

    #prompts
    with open("assets/system_prompt.txt","r") as file:
        system_prompt = file.read()
    print(system_prompt)
    user_query = f"data: {text['text']}\nExtract the entities from the data? Reply in json format."
    #generate response
    ans = llm.generate(user_query=user_query,system_prompt=system_prompt)
    print(ans)
    data = extract_json(ans)
    return data, text


def main(wav_audio_data):
    if wav_audio_data is not None:

        data, text = transcribe_and_extract()

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

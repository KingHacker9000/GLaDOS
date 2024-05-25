from gtts import gTTS
import openai
import speech_recognition as sr
import convert
from rvc_infer import rvc_convert
import winsound
import os

print("imports complete")

API_KEY = os.environ['API_KEY']
LANG = 'en'
PAY_ATTENTION = True
HOSTILE = False

openai.api_key = API_KEY

required=1
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    if "pulse" in name:
        required= index
        print(required)

def get_audio():
        global PAY_ATTENTION
        print('Loading SR')
        r = sr.Recognizer()

        with sr.Microphone(device_index=required) as source:

            print("Say something!")
            audio = r.listen(source, phrase_time_limit=6)

            try:
                said = ''
                said = r.recognize_google(audio)
                print('speak')
                print(said)

                if 'glados' in said.lower():
                    PAY_ATTENTION = True

                if PAY_ATTENTION and said.strip() != "":
                    completion = openai.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                        {
                            "role": "assistant",
                            "content": "Pretend to be GLaDOS from the portal games, now respond to the following question in her style, remember to use dark humor, sarcasm and keep responses breif and targeted" + (', But make sure to be helpful and answer usefully' if not HOSTILE else '') + " :" + said
                        }
                        ],
                        temperature=1,
                        max_tokens=256,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0
                    )
                    text = completion.choices[0].message.content
                    print(text)

                    if "error" not in text.lower() or text.strip != "":
                        speech = gTTS(text=text, lang=LANG, slow=False, tld="com.au")
                        file_name = f"test.mp3"
                        speech.save(file_name)
                        # playsound.playsound(file_name, block=False)

                        convert.convert_to_wav(file_name, "a2.wav")

                        rvc_convert(model_path="GLaDOSBIG.pth", input_path="a2.wav")
                        winsound.PlaySound("output/out.wav", winsound.SND_FILENAME)

                if 'bye' in said.lower():
                    PAY_ATTENTION = False
                    return

            except Exception as e:
                print(e)

        return said

while True:
    get_audio()
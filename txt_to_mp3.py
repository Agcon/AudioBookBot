import gtts
from pathlib import Path
import pdfplumber
import pyttsx3


def txt_to_mp3_online(file_path, language='ru'):
    with open(file_path, encoding="utf8") as f:
        text = f.readlines()
    text = ''.join(text)
    text = gtts.gTTS(text, lang=language)
    text.save(Path(file_path).stem + '.mp3')


def txt_to_mp3_offline(file_path, language='ru', sex='male'):
    with open(file_path, encoding="utf8") as f:
        text = f.readlines()
    text = ''.join(text)
    text = text.replace('\n', '')
    tts = pyttsx3.init()
    if language == 'ru':
        if sex == 'male':
            tts.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\TokenEnums\RHVoice\Mikhail")
            tts.setProperty('rate', 130)
        else:
            tts.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\TokenEnums\RHVoice\Tatiana")
    elif language == 'en':
        if sex == 'male':
            pass
        else:
            tts.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")

    tts.save_to_file(text, Path(file_path).stem + '.mp3')
    tts.runAndWait()
    


def pdf_to_mp3(file_path, language='ru'):
    with pdfplumber.PDF(open(file=file_path, mode='rb')) as pdf:
        text = [page.extract_text() for page in pdf.pages]
    text = ''.join(text)
    text = text.replace('\n', '')
    text = gtts.gTTS(text, lang=language)
    text.save(Path(file_path).stem + '.mp3')


def main():
    file_path = input()
    if Path(file_path).is_file():
        if Path(file_path).suffix == '.txt':
            #txt_to_mp3_online(file_path)
            #txt_to_mp3_offline(file_path, sex='female')
            txt_to_mp3_offline(file_path)
        elif Path(file_path).suffix == '.pdf':
            pdf_to_mp3(file_path)
    else:
        print("No such file")


if __name__ == '__main__':
    main()

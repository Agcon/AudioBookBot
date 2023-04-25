import gtts
from pathlib import Path
import pdfplumber


def txt_to_mp3(file_path, language='ru'):
    with open(file_path, encoding="utf8") as f:
        text = f.readlines()
    text = ''.join(text)
    text = gtts.gTTS(text, lang=language)
    text.save(Path(file_path).stem + ".mp3")


def pdf_to_mp3(file_path, language='ru'):
    with pdfplumber.PDF(open(file=file_path, mode='rb')) as pdf:
        text = [page.extract_text() for page in pdf.pages]
    text = ''.join(text)
    text = text.replace('\n', '')
    text = gtts.gTTS(text, lang=language)
    text.save(Path(file_path).stem + ".mp3")


def main():
    file_path = input()
    if Path(file_path).is_file():
        if Path(file_path).suffix == '.txt':
            txt_to_mp3(file_path)
        elif Path(file_path).suffix == '.pdf':
            pdf_to_mp3(file_path)
    else:
        print("Нет такого файла")


if __name__ == '__main__':
    main()

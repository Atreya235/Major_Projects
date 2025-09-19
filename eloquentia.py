import streamlit as st
from deep_translator import GoogleTranslator
from langdetect import detect
import re
import fitz  # PyMuPDF
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from gtts import gTTS
from io import BytesIO

LANGUAGE_MAP = {
    'af': 'Afrikaans', 'am': 'Amharic', 'ar': 'Arabic', 'as': 'Assamese', 'az': 'Azerbaijani',
    'be': 'Belarusian', 'bg': 'Bulgarian', 'bn': 'Bengali', 'bs': 'Bosnian', 'ca': 'Catalan',
    'ceb': 'Cebuano', 'co': 'Corsican', 'cs': 'Czech', 'cy': 'Welsh', 'da': 'Danish',
    'de': 'German', 'dv': 'Divehi', 'el': 'Greek', 'en': 'English', 'eo': 'Esperanto',
    'es': 'Spanish', 'et': 'Estonian', 'eu': 'Basque', 'fa': 'Persian', 'fi': 'Finnish',
    'fil': 'Filipino', 'fj': 'Fijian', 'fo': 'Faroese', 'fr': 'French', 'fy': 'Frisian',
    'ga': 'Irish', 'gd': 'Scottish Gaelic', 'gl': 'Galician', 'gn': 'Guarani', 'gu': 'Gujarati',
    'ha': 'Hausa', 'haw': 'Hawaiian', 'he': 'Hebrew', 'hi': 'Hindi', 'hmn': 'Hmong',
    'hr': 'Croatian', 'ht': 'Haitian Creole', 'hu': 'Hungarian', 'hy': 'Armenian',
    'id': 'Indonesian', 'ig': 'Igbo', 'is': 'Icelandic', 'it': 'Italian', 'ja': 'Japanese',
    'jv': 'Javanese', 'ka': 'Georgian', 'kk': 'Kazakh', 'km': 'Khmer', 'kn': 'Kannada',
    'ko': 'Korean', 'ku': 'Kurdish', 'ky': 'Kyrgyz', 'la': 'Latin', 'lb': 'Luxembourgish',
    'mk': 'Macedonian', 'ml': 'Malayalam', 'mn': 'Mongolian', 'mr': 'Marathi', 'ms': 'Malay',
    'mt': 'Maltese', 'my': 'Myanmar (Burmese)', 'ne': 'Nepali', 'nl': 'Dutch', 'no': 'Norwegian',
    'ny': 'Chichewa', 'oc': 'Occitan', 'or': 'Odia (Oriya)', 'pa': 'Punjabi', 'pl': 'Polish',
    'ps': 'Pashto', 'pt': 'Portuguese', 'qu': 'Quechua', 'ro': 'Romanian', 'ru': 'Russian',
    'rw': 'Kinyarwanda', 'sd': 'Sindhi', 'si': 'Sinhala', 'sk': 'Slovak', 'sl': 'Slovenian',
    'sm': 'Samoan', 'sn': 'Shona', 'so': 'Somali', 'sq': 'Albanian', 'sr': 'Serbian',
    'st': 'Sesotho', 'su': 'Sundanese', 'sv': 'Swedish', 'sw': 'Swahili', 'ta': 'Tamil',
    'te': 'Telugu', 'tg': 'Tajik', 'th': 'Thai', 'ti': 'Tigrinya', 'tk': 'Turkmen',
    'ur': 'Urdu', 'uz': 'Uzbek', 'vi': 'Vietnamese', 'xh': 'Xhosa', 'yi': 'Yiddish',
    'yo': 'Yoruba', 'zh-cn': 'Chinese (Simplified)', 'zh-tw': 'Chinese (Traditional)', 'zu': 'Zulu'
}

st.set_page_config(page_title="Galaxy Translator", layout="centered")

st.markdown("""
<style>
html, body, [class*="css"], div, span, input, textarea, button, label, p, h1, h2, h3, h4, h5, h6 {
    font-family: 'Dancing Script', cursive !important;
    color: white !important;
    font-style: italic;
}    
.stApp {
    background-image: url('https://img.freepik.com/premium-photo/stunning-realistic-wallpaper-planet-starry-astrophotography-universe-cosmus-space-background-generative-ai_742252-11509.jpg?ga=GA1.1.1596926652.1748794483&semt=ais_hybrid&w=740');
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-position: center;
    color: black;
}
h1, h2, h3 {
    color: #00ffff;
    text-align: center;
}
.stButton > button {
    font-size: 18px;
    padding: 10px 24px;
    background: linear-gradient(135deg, #00BFFF, #1E90FF);
    color: white;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    box-shadow: 0 4px 10px rgba(0, 191, 255, 0.4);
    transition: all 0.3s ease-in-out;
}
.stButton > button:hover {
    transform: scale(1.05);
    background: linear-gradient(135deg, #1E90FF, #00BFFF);
    box-shadow: 0 6px 15px rgba(0, 191, 255, 0.6);
}
textarea, .stTextInput > div > input {
    background-color: #ffffffdd !important;
    color: black !important;
    caret-color: black !important;
    caret-width: 5px !important;
}
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    st.markdown("""
    <h1>🚀 ELOQUENTIA </h1>
    <p style="text-align:center; font-size:18px;">Experience linguistic translation. Click below to travel to the Translator.</p>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Take Me To Translator"):
            st.session_state.page = "translator"

elif st.session_state.page == "translator":
    st.markdown("<h1>🌌 INTERACT ELOQUENTLY... </h1>", unsafe_allow_html=True)
    st.markdown("<h3>Translate any language into your chosen language</h3>", unsafe_allow_html=True)

    input_text = st.text_area("Enter your text:", height=150)
    target_lang_name = st.selectbox("Select target language", sorted(LANGUAGE_MAP.values()))
    target_lang_code = [code for code, name in LANGUAGE_MAP.items() if name == target_lang_name][0]

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        translate_clicked = st.button("Translate")

    if translate_clicked:
        if input_text.strip() == "":
            st.warning("Please enter some text.")
        else:
            try:
                words = re.findall(r'\b\w+\b', input_text)
                sentences = re.split(r'[.!?]+', input_text)
                sentences = [s.strip() for s in sentences if s.strip()]
                lang_code = detect(input_text)
                lang_name = LANGUAGE_MAP.get(lang_code, f"Unknown ({lang_code})")
                st.info(f"Detected Language: {lang_name}")
                st.markdown(f"Words: {len(words)} | Sentences: {len(sentences)}")
                st.write(f"✨ Translating to {target_lang_name}...")

                translated_text = GoogleTranslator(source='auto', target=target_lang_code).translate(text=input_text)
                st.success("Translation:")
                st.write(translated_text)

                try:
                    voice_message = f"Detected language: {lang_name}. Translation: {translated_text}"
                    tts = gTTS(text=voice_message, lang='en')
                    audio_bytes = BytesIO()
                    tts.write_to_fp(audio_bytes)
                    audio_bytes.seek(0)
                    st.audio(audio_bytes, format='audio/mp3')
                except Exception as e:
                    st.warning(f"Voice announcement failed: {e}")

            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown("<h3>📄 Upload PDF for Translation</h3>", unsafe_allow_html=True)
    pdf_file = st.file_uploader("Upload PDF file", type=["pdf"])

    if pdf_file is not None:
        try:
            doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
            full_text = ""
            for page in doc:
                full_text += page.get_text()

            lines = full_text.split('\n')
            paragraphs = []
            current_para = ""

            for line in lines:
                if line.strip() == "":
                    if current_para:
                        paragraphs.append(current_para.strip())
                        current_para = ""
                else:
                    current_para += " " + line.strip() if current_para else line.strip()

            if current_para:
                paragraphs.append(current_para.strip())

            word_count = sum(len(re.findall(r'\b\w+\b', para)) for para in paragraphs)
            sentence_count = sum(len(re.findall(r'[.!?]+', para)) for para in paragraphs)
            paragraph_count = len(paragraphs)

            st.markdown(f"📊 PDF Stats:")
            st.markdown(f"- 📝 Total Paragraphs: {paragraph_count}")
            st.markdown(f"- 🔤 Total Words: {word_count}")
            st.markdown(f"- 📑 Total Sentences: {sentence_count}")

            translated_results = []

            for i, para in enumerate(paragraphs, 1):
                try:
                    lang = detect(para)
                    lang_name = LANGUAGE_MAP.get(lang, f"Unknown ({lang})")
                    translation = GoogleTranslator(source='auto', target=target_lang_code).translate(para)
                    translated_results.append((i, translation, lang_name, para))
                except Exception as e:
                    translated_results.append((i, f"[Translation failed: {e}]", "Unknown", para))

            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer, pagesize=A4)
            width, height = A4
            y = height - 50

            for i, translated, _, _ in translated_results:
                for line in translated.split('\n'):
                    c.drawString(40, y, line)
                    y -= 18
                    if y < 60:
                        c.showPage()
                        y = height - 50
            c.save()
            pdf_buffer.seek(0)

            st.download_button(
                label="📄 Download Translated PDF",
                data=pdf_buffer,
                file_name="translated_output.pdf",
                mime="application/pdf"
            )

            for index, translation, lang_name, original_para in translated_results:
                st.markdown(f"#### Paragraph {index}")
                st.markdown(f"- *Detected Language:* {lang_name}")
                st.markdown(f"- Translated: {translation}")
                try:
                    voice_msg = f"Detected language: {lang_name}. Translation: {translation}"
                    tts = gTTS(text=voice_msg, lang='en')
                    audio_bytes = BytesIO()
                    tts.write_to_fp(audio_bytes)
                    audio_bytes.seek(0)
                    st.audio(audio_bytes, format='audio/mp3')
                except Exception as e:
                    st.warning(f"Voice announcement failed: {e}")
                st.markdown("---")
        except Exception as e:
            st.error(f"Failed to read/translate PDF: {e}")
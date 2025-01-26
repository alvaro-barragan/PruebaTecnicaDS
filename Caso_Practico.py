import openai
from PyPDF2 import PdfReader
import gradio as gr

# Configura tu clave de API de OpenAI
openai.api_key = "TU_API_KEY_DE_OPENAI"

# Función para dividir el texto en bloques más pequeños
def split_text(text, max_length=1000):
    # Dividir el texto en fragmentos más pequeños que no excedan el max_input_length
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        current_length += len(word) + 1  # +1 por el espacio
        if current_length > max_length:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_length = len(word) + 1
        else:
            current_chunk.append(word)

    # Añadir el último bloque
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

# Función para procesar el PDF y generar una respuesta
def chat_with_pdf(pdf_file, question):
    # Leer el PDF
    pdf_reader = PdfReader(pdf_file.name)
    text = " ".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])

    # Dividir el texto en fragmentos más pequeños si es demasiado largo
    max_input_length = 1000  # Límite de caracteres por fragmento
    text_chunks = split_text(text, max_length=max_input_length)

    # Variable para almacenar las respuestas de todos los fragmentos
    full_response = ""

    # Procesar cada fragmento por separado
    for chunk in text_chunks:
        prompt = f"Contexto: {chunk}\nPregunta: {question}\nRespuesta:"

        # Llamada a la API de OpenAI para obtener la respuesta
        response = openai.Completion.create(
            model="text-davinci-003",  # Puedes usar otros modelos de OpenAI
            prompt=prompt,
            max_tokens=200,
            n=1,
            stop=None,
            temperature=0.7,
        )

        # Extraer la respuesta generada y agregarla a la respuesta final
        answer = response.choices[0].text.strip()
        full_response += answer + "\n"

    # Devolver la respuesta combinada
    return full_response

# Interfaz de Gradio
def gradio_interface(pdf_file, question):
    return chat_with_pdf(pdf_file, question)

# Crear la interfaz de usuario con Gradio
iface = gr.Interface(
    fn=gradio_interface,
    inputs=[
        gr.File(label="Sube tu archivo PDF"),
        gr.Textbox(label="Pregunta sobre el PDF")
    ],
    outputs="text",
    live=True,
    title="Chatbot para Preguntas sobre Documentos PDF"
)

iface.launch()

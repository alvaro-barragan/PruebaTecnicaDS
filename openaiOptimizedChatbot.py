import openai
from PyPDF2 import PdfReader
import gradio as gr

# Configura tu clave de API de OpenAI
openai.api_key = "TU_API_KEY_DE_OPENAI"

# Función para dividir el texto en bloques más grandes
def split_text(text, max_length=1000):
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

    # Dividir el texto en fragmentos más grandes
    max_input_length = 2000  # Aumento el tamaño de los fragmentos
    text_chunks = split_text(text, max_length=max_input_length)

    # Variable para almacenar las respuestas de todos los fragmentos
    full_response = ""

    # Procesar fragmentos en lotes de tamaño adecuado
    batch = []
    for chunk in text_chunks:
        prompt = f"Contexto: {chunk}\nPregunta: {question}\nRespuesta:"
        batch.append(prompt)

        # Si el batch ha alcanzado el tamaño máximo, procesarlo
        if len(batch) >= 3:  # Limitar el número de prompts por solicitud
            combined_prompt = "\n".join(batch)
            response = openai.Completion.create(
                model="text-davinci-003",  # Usamos el modelo de OpenAI
                prompt=combined_prompt,
                max_tokens=500,
                n=1,
                stop=None,
                temperature=0.7,
            )
            full_response += response.choices[0].text.strip() + "\n"
            batch = []  # Reiniciar el batch

    # Procesar el último batch si queda alguno
    if batch:
        combined_prompt = "\n".join(batch)
        response = openai.Completion.create(
            model="text-davinci-003",  # Usamos el modelo de OpenAI
            prompt=combined_prompt,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7,
        )
        full_response += response.choices[0].text.strip() + "\n"

    return full_response

# Interfaz de Gradio
def gradio_interface(pdf_file, question):
    return chat_with_pdf(pdf_file, question)

# Crear la interfaz de usuario con Gradio
with gr.Blocks() as demo:
    gr.Markdown("## Chat con tu PDF")

    # Entrada para subir el archivo PDF y la pregunta
    pdf_input = gr.File(label="Sube tu archivo PDF")
    question_input = gr.Textbox(label="Escribe tu pregunta")
    
    # Caja de texto para mostrar la respuesta
    output = gr.Textbox(label="Respuesta")

    # Botón para enviar la solicitud
    submit_button = gr.Button("Enviar")

    # Conectar el botón a la función gradio_interface
    submit_button.click(gradio_interface, inputs=[pdf_input, question_input], outputs=output)

# Ejecutar la app
demo.launch()

# Importamos las librerías necesarias
from transformers import pipeline
from PyPDF2 import PdfReader
import gradio as gr

# Cargar el modelo GPT-Neo de Hugging Face
qa_model = pipeline("text-generation", model="EleutherAI/gpt-neo-1.3B")

# Función para procesar el PDF y generar una respuesta
def chat_with_pdf(pdf_file, question):
    # Leer el PDF
    pdf_reader = PdfReader(pdf_file.name)
    text = " ".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])

    # Si el texto extraído es demasiado largo, recortarlo para que el modelo no se sobrecargue
    max_input_length = 1000  # Puedes ajustarlo si el texto es demasiado largo
    if len(text) > max_input_length:
        text = text[:max_input_length]

    # Crear el prompt para el modelo (pregunta + contexto del PDF)
    prompt = f"Contexto: {text}\nPregunta: {question}\nRespuesta:"

    # Usar el modelo para generar la respuesta con max_new_tokens y truncamiento
    response = qa_model(prompt, max_new_tokens=100, truncation=True)

    return response[0]['generated_text'].strip()

# Función para interactuar con Gradio
def gradio_interface(pdf_file, question):
    return chat_with_pdf(pdf_file, question)

# Interfaz Gradio
with gr.Blocks() as demo:
    gr.Markdown("## Chat con tu PDF")
    pdf_input = gr.File(label="Sube tu archivo PDF")
    question_input = gr.Textbox(label="Escribe tu pregunta")
    output = gr.Textbox(label="Respuesta")

    submit_button = gr.Button("Enviar")
    submit_button.click(gradio_interface, inputs=[pdf_input, question_input], outputs=output)

# Ejecutar la app
demo.launch()
# Chatbot para Preguntas sobre Documentos PDF

Este repositorio contiene dos aplicaciones que permiten cargar un archivo PDF y hacer preguntas sobre su contenido, usando dos enfoques diferentes:

- Usando la API de OpenAI (modelo `text-davinci-003`).
- Usando el modelo `GPT-Neo 1.3B` de Hugging Face.

Ambas aplicaciones proporcionan una interfaz interactiva basada en **Gradio** para facilitar la interacción con los documentos PDF.

## Requisitos

Antes de ejecutar los scripts, asegúrate de tener instalado Python 3.7 o superior.

### Paso 1: Clonar el repositorio

Clona el repositorio en tu máquina local:

```bash
git clone https://github.com/alvaro-barragan/PruebaTecnicaDS
cd tu_repositorio
```

### Paso 2: Instalar las dependencias

Instala las dependencias necesarias usando `pip`:

```bash
pip install -r requirements.txt
```

### Paso 4: Configuración de la clave API de OpenAI (Caso_Practico.py o openaiOptimizedChatbot.py)

Para usar la API de OpenAI, necesitas una clave API válida. Una vez que tengas tu clave API, puedes configurarla en el script `Caso_Practico.py` y `openaiOptimizedChatbot.py` editando la línea 6:

```python
# Configura tu clave de API de OpenAI
openai.api_key = "TU_API_KEY_DE_OPENAI"
```

### Paso 5: Ejecutar la aplicación

Para ejecutar la aplicación, simplemente ejecuta el script correspondiente:

```bash
python openaiOptimizedChatbot.py
```
```bash
python Caso_Practico.py
```
o, si prefieres usar el modelo básico con Hugging Face:

```bash
python totalcasopractico.py
```

Esto iniciará un servidor local e indicará la URL a la que puedes acceder desde tu navegador para interactuar con la aplicación.
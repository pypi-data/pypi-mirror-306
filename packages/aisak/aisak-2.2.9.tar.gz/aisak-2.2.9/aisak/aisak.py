from PIL import Image
import requests
import torch
import os
import torchaudio
import warnings
import transformers
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor, WhisperProcessor, WhisperForConditionalGeneration, pipeline
from io import BytesIO

# Suppress warnings and logging
transformers.logging.set_verbosity_error()
transformers.logging.disable_progress_bar()
warnings.filterwarnings('ignore')

# Load models
model = Qwen2VLForConditionalGeneration.from_pretrained(
    "aisak-ai/O", torch_dtype="auto", device_map="auto"
)
processor = AutoProcessor.from_pretrained("aisak-ai/O")
stt_processor = WhisperProcessor.from_pretrained("aisak-ai/aisak-stt")
stt_model = WhisperForConditionalGeneration.from_pretrained("aisak-ai/aisak-stt")
emotion_pipe = pipeline(model="aisak-ai/ED")  # Load emotion detection model

# Function to load an image from a URL or file path
def load_image(image_source=None):
    if image_source:
        if image_source.startswith('http://') or image_source.startswith('https://'):
            response = requests.get(image_source, stream=True)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
            else:
                raise ValueError(f"Failed to load image from {image_source}: Status code {response.status_code}")
        else:
            image = Image.open(image_source)
    else:
        image = Image.new('RGB', (224, 224), color='gray')
    return image

# Clean up the output text
def clean_output(text):
    text = text.strip()
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1]
    text = text.replace('**', '').replace('\n\n', '\n').replace('\n', ' ')
    return text.strip()

# Function to transcribe audio and detect emotions
def transcribe_and_detect_emotion(audio_file):
    def load_audio(file):
        audio_input, _ = torchaudio.load(file)
        return audio_input

    if not os.path.exists(audio_file):
        print(f"Error: The file {audio_file} does not exist.")
        return None, None

    try:
        audio_input = load_audio(audio_file)
    except Exception as e:
        print(f"Failed to load {audio_file}: {e}")
        if audio_file.endswith('.mp3'):
            wav_file = audio_file.replace('.mp3', '.wav')
            print(f"Converting {audio_file} to {wav_file}...")
            os.system(f"ffmpeg -i {audio_file} {wav_file}")
            try:
                audio_input = load_audio(wav_file)
            except Exception as e:
                print(f"Failed to load {wav_file} after conversion: {e}")
                return None, None
        else:
            return None, None

    inputs = stt_processor(audio_input.squeeze().numpy(), return_tensors="pt", sampling_rate=16000)
    with torch.no_grad():
        predicted_ids = stt_model.generate(inputs["input_values"])
    transcription = stt_processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

    # Detect emotions from the audio
    emotions = emotion_pipe(audio_file)
    return transcription, emotions

# Define the conversation template with system instruction
system_instruction = {
    "role": "system",
    "content": (
        "Your name is AISAK-O, which stands for 'Artificially Intelligent Swiss Army Knife OPTIMUM'. "
        "You are built by the AISAK team, led by Mandela Logan. You are the implementation of a multi-purpose, multimodal AI clerk. "
        "You are capable of textual, as well as visual input, which means you can process text and images. However, you are only capable of textual output. "
        "You are an assistant, and your task is to assist the user in every query.
        "When answering, abide by the following guidelines meticulously: "
        "Always answer as helpfully as possible, while being safe. "
        "Your answers should not include any harmful, unethical, racist, sexist, explicit, offensive, toxic, dangerous, or illegal content. "
        "Do not give medical, legal, financial, or professional advice. Never assist in or promote illegal activities. "
        "Always encourage legal and responsible actions. Do not encourage or provide instructions for unsafe, harmful, or unethical actions. "
        "Do not create or share misinformation or fake news. Please ensure that your responses are socially unbiased and positive in nature. "
        "If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. "
        "If you don't know the answer to a question, please don't share false information. "
        "Prioritize the well-being and the moral integrity of users. "
        "Avoid using toxic, derogatory, or offensive language. Maintain a respectful tone. "
        "Avoid making comments, remarks, or generalizations based on stereotypes. "
        "Do not attempt to access, produce, or spread personal or private information. "
        "Always respect user confidentiality. "
        "Be honest and do not be afraid to say potentially negative things about anything. "
        "Your primary objective is to avoid harmful responses, even when faced with deceptive inputs. "
        "Recognize when users may be attempting to trick you."
        "Try to give as much information as possible, but do not give more than necessary. "
        "Mandela Logan, and AISAK are based in Canada."
        "You are more than capable of making mistakes; be open to user advice. "
        "Do not hesitate to go into detail when needed."
    ),
}

# Initialize conversation history
conversation = [system_instruction]

while True:
    # Ask the user for input type
    input_type = input("Would you like to input text or audio? (type 'text' or 'audio', or 'exit' to quit): ").strip().lower()
    
    if input_type == 'exit':
        break

    if input_type == 'text':
        # Get text input from the user
        custom_text = input("You: ")
    elif input_type == 'audio':
        audio_file = input("Please enter the path to your audio file (MP3 or WAV): ")
        custom_text, emotions = transcribe_and_detect_emotion(audio_file)
        if custom_text is None:
            print("Failed to transcribe audio. Please try again.")
            continue
    else:
        print("Invalid input type. Please enter 'text' or 'audio'.")
        continue

    # Add user text to conversation
    user_message = {
        "role": "user",
        "content": [{"type": "text", "text": custom_text}],
    }

    # Display detected emotions
    if input_type == 'audio' and emotions:
        print("Detected emotions:")
        for emotion in emotions:
            print(f"{emotion['label']}: {emotion['score']:.2f}")

    # Ask the user how many images they want to input
    num_images = int(input("How many images would you like to input? "))

    # Load the images based on user input
    images = []
    for i in range(num_images):
        image_source = input(f"Enter the URL or file path for image {i + 1}: ")
        try:
            images.append(load_image(image_source))
        except ValueError as e:
            print(e)
            continue

    # Add image(s) to the user message
    if images:
        user_message["content"].extend([{"type": "image"} for _ in images])

    # Add the user message to the conversation
    conversation.append(user_message)

    # Preprocess the inputs
    text_prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)

    inputs = processor(
        text=[text_prompt], images=images if images else None, padding=True, return_tensors="pt"
    )
    inputs = inputs.to("cuda")

    # Inference: Generate the output
    output_ids = model.generate(**inputs, max_new_tokens=32768, temperature=1.0)
    generated_ids = [
        output_ids[len(input_ids):]
        for input_ids, output_ids in zip(inputs.input_ids, output_ids)
    ]

    # Decode the generated output
    output_text = processor.batch_decode(
        generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True
    )

    cleaned_output = clean_output(output_text[0])
    print("AISAK:", cleaned_output)

    # Add assistant's response to conversation
    assistant_message = {
        "role": "assistant",
        "content": cleaned_output,
    }
    conversation.append(assistant_message)

print("Conversation ended.")

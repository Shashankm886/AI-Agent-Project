from together_llama import query_llama
from crypto_price_fetcher import get_crypto_price
from conversation_manager import ConversationManager
from googletrans import Translator
import re

translator = Translator()

def translate_to_english(text):
    """
    Translates the input text to English.

    Args:
        text (str): The text to translate.

    Returns:
        str: Translated text in English.
    """
    try:
        translation = translator.translate(text, dest='en')
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text 

def detect_intent(user_input):
    """
    Detects the user's intent based on their input.

    Args:
        user_input (str): The user's input message.

    Returns:
        str: The detected intent ('get_price', 'change_language', 'general').
    """
    if re.search(r'\b(price|value|cost)\b', user_input, re.IGNORECASE):
        return 'get_price'
    elif re.search(r'\b(change language to|speak in)\b', user_input, re.IGNORECASE):
        return 'change_language'
    else:
        return 'general'

def handle_get_price(user_input):
    """
    Handles requests for cryptocurrency prices.

    Args:
        user_input (str): The user's input message.

    Returns:
        str: The assistant's response.
    """
    # Extract cryptocurrency name if mentioned
    match = re.search(r'price of (\w+)', user_input, re.IGNORECASE)
    crypto_name = 'bitcoin'  # we are showing the default cryptocurrency as bitcoin, in case of none or invalid input
    if match:
        crypto_name = match.group(1).lower()

    # Fetch price
    try:
        price = get_crypto_price(crypto_name)
        response = f"The current price of {crypto_name.capitalize()} is ${price} USD."
    except Exception as e:
        response = f"Sorry, I couldn't retrieve the price for {crypto_name}."
    return response

def handle_change_language(user_input):
    """
    Acknowledges the user's request to change language but continues in English.

    Args:
        user_input (str): The user's input message.

    Returns:
        str: The assistant's response.
    """
    response = "I will continue to communicate in English, but I can understand your input in other languages."
    return response

def handle_general(user_input, conversation_manager):
    """
    Handles general conversation.

    Args:
        user_input (str): The user's input message.
        conversation_manager (ConversationManager): The conversation manager instance.

    Returns:
        str: The assistant's response.
    """
    # Translate user input to English if necessary
    user_input_en = translate_to_english(user_input)
    conversation_manager.history[-1]['content'] = user_input_en  # here we are updating last user message to english

    # Get the list of messages
    messages = conversation_manager.get_messages()
    assistant_response = query_llama(messages)
    if assistant_response:
        return assistant_response
    else:
        return "I'm sorry, I didn't understand that. Could you please rephrase?"

def process_user_input(user_input, conversation_manager):
    """
    Processes the user input and generates the assistant's response.

    Args:
        user_input (str): The user's input message.
        conversation_manager (ConversationManager): The conversation manager instance.

    Returns:
        str: The assistant's response.
    """
    conversation_manager.add_user_message(user_input)
    intent = detect_intent(user_input)

    if intent == 'get_price':
        response = handle_get_price(user_input)
    elif intent == 'change_language':
        response = handle_change_language(user_input)
    else:
        response = handle_general(user_input, conversation_manager)

    conversation_manager.add_agent_message(response)
    return response

import logging
import os

from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI


def test_Gemini_Text_generation(text):
    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    result = llm.invoke(text)
    return result.content


def generate_Image_Caption(image_url):
    llm = ChatGoogleGenerativeAI(model="gemini-pro-vision")
    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": "What should be Title limits to Four word for this image which will be listed on shopping site? First word will be the Brand name, Second word will be the color, Third word will be the item name, third word will be the category. Output should be in format Title: output",
            },  # You can optionally provide text parts
            {
                "type": "text",
                "text": "What should be Description limits to thirty words for this image which will be listed on shopping site? Output should be in format Description: output",
            },
            {
                "type": "text",
                "text": "What should be suggested Category for this item? Output should be in format Category: output",
            },
            {
                "type": "text",
                "text": "What should be Brand name for this item? Output should be in format Brand: output",
            },
            {
                "type": "text",
                "text": "What should be suggested price for this item in the image in INR ? Output should be in format Price: output",
            },
            {"type": "image_url", "image_url": image_url},
        ]
    )
    return parse_string(llm.invoke([message]).content)


def handle_image(image_url) -> dict:
    if "GOOGLE_API_KEY" not in os.environ:
        logging.error("NO GOOGLE_API_KEY environment variable")

    # Gemini Text Generation
    # result = test_Gemini_Text_generation("Write a ballad about LangChain")
    # display_results(result)

    # Gemini IMage Caption Generation
    # image_url = "C:/Users/user/Downloads/pen2.jpeg"
    result = generate_Image_Caption(image_url)
    return result


def modify_Item_Details_voice_Based(text):
    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": "I have this string: " + text,
            }
        ]
    )
    return llm.invoke([message])


def test_Gemini_Text_generation(text):
    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    result = llm.invoke(text)
    return result.content


def parse_string(input_string):
    # Split the string by newline
    lines = input_string.split('\n')

    # Initialize an empty dictionary
    result_dict = {}

    # Iterate through each line
    for line in lines:
        # Remove '**' markers and split by ':'
        key, value = line.replace('**', '').split(':')

        # Store the key-value pair in the dictionary
        result_dict[key.strip()] = value.strip()

    return result_dict

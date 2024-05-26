import logging
import os

from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI


def test_Gemini_Text_generation(text):
    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    result = llm.invoke(text)
    return result.content


def display_results(result):
    print(result)


def generate_Image_Caption(image_url):
    llm = ChatGoogleGenerativeAI(model="gemini-pro-vision")
    message = HumanMessage(content=[{"type": "text",
                                     "text": "What should be Title limits to Four word for this image which will be listed on shopping site? First word will be the Brand name, Second word will be the color, Third word will be the item name, third word will be the category", },
                                    # You can optionally provide text parts
                                    {"type": "text",
                                     "text": "What should be Description limits to thirty words for this image which will be listed on shopping site?", },
                                    {"type": "text", "text": "What should be suggested Category for this item?", },
                                    {"type": "text", "text": "What should be Brand name for this item?", },
                                    {"type": "text",
                                     "text": "What should be suggested price for this item in the image in INR ?", },
                                    {"type": "image_url", "image_url": image_url}, ])
    return llm.invoke([message])


def handle_image(image_url) -> str:
    if "GOOGLE_API_KEY" not in os.environ:
        logging.error("NO GOOGLE_API_KEY environment variable")

    # Gemini Text Generation
    # result = test_Gemini_Text_generation("Write a ballad about LangChain")
    # display_results(result)

    # Gemini IMage Caption Generation
    # image_url = "C:/Users/user/Downloads/pen2.jpeg"
    result = generate_Image_Caption(image_url)
    return result.content

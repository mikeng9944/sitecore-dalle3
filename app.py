import os
import json
import requests
import streamlit as st
from openai import AzureOpenAI
from azure.storage.blob import BlobServiceClient

azure_connection_string = "DefaultEndpointsProtocol=https;AccountName=sitecoredemoblobstorage;AccountKey=NV6YxWWitdhtSm0rzzX6xrTux/RmtgxWIY+Psobwz4vJM3GBMg+2KgLi7C6XUHtiuWFa3LfhoSID+AStZEFo2g==;EndpointSuffix=core.windows.net"

# Function to generate an image using Azure OpenAI DALL-E
def generate_image(prompt):
    client = AzureOpenAI(
        api_version="2023-12-01-preview",
        azure_endpoint="https://sitecore-openai-dalle3.openai.azure.com",
        api_key="815c5db8df5f49ffaf2e96a337fd6476",
    )

    result = client.images.generate(
        model="Dalle3",  # the name of your DALL-E 3 deployment
        prompt=prompt,
        n=1
    )
    
    image_url = json.loads(result.model_dump_json())['data'][0]['url']

    # Upload the image to Azure Blob Storage
    blob_service_client = BlobServiceClient.from_connection_string(azure_connection_string)
    blob_name = "generated_image.png"
    blob_client = blob_service_client.get_blob_client("testcontainer", blob_name)
    response = requests.get(image_url, stream=True)
    blob_client.upload_blob(response.raw, overwrite=True)

    return image_url

# Streamlit app
st.title("Azure OpenAI DALL-E Image Generator")

# User input for the prompt
user_prompt = st.text_input("Enter a prompt for the image:")

if st.button("Generate Image"):
    if user_prompt:
        with st.spinner('Generating image...'):
            image_url = generate_image(user_prompt)
            if image_url:
                st.image(image_url, width=300)
    else:
        st.error("Please enter a prompt.")
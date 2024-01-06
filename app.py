import os
import json
import requests
import streamlit as st
from openai import AzureOpenAI
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

azure_connection_string = "DefaultEndpointsProtocol=https;AccountName=sitecoredemoblobstorage;AccountKey=NV6YxWWitdhtSm0rzzX6xrTux/RmtgxWIY+Psobwz4vJM3GBMg+2KgLi7C6XUHtiuWFa3LfhoSID+AStZEFo2g==;EndpointSuffix=core.windows.net"

# Function to generate an image using Azure OpenAI DALL-E
def generate_images(prompt):
    client = AzureOpenAI(
        api_version="2023-12-01-preview",
        azure_endpoint="https://sitecore-openai-dalle3.openai.azure.com",
        api_key="815c5db8df5f49ffaf2e96a337fd6476",
    )

    image_urls = []
    blob_service_client = BlobServiceClient.from_connection_string(azure_connection_string)

    for i in range(5):
        result = client.images.generate(
            model="Dalle3",  # the name of your DALL-E 3 deployment
            prompt=prompt,
            n=1
        )

        image = json.loads(result.model_dump_json())['data'][0]
        image_url = image['url']
        image_urls.append(image_url)

        # Upload the image to Azure Blob Storage
        blob_name = f"generated_image_{i}.png"
        blob_client = blob_service_client.get_blob_client("testcontainer", blob_name)
        response = requests.get(image_url, stream=True)
        blob_client.upload_blob(response.raw, overwrite=True)

    return image_urls

# Streamlit app
st.sidebar.title("Azure AOAI with GTI")
st.sidebar.image("https://media.licdn.com/dms/image/C560BAQG-z4mFpkcj1g/company-logo_200_200/0/1631388948853?e=2147483647&v=beta&t=9K8Ajrde__ehRbdaYlLsp7oJhqfEUPZuSBs7StG2h6k", width=200)
st.title("Azure OpenAI DALL-E GTI Image Generator")

# User input for the prompt
user_prompt = st.text_input("Enter a prompt for the image:")

if st.button("Generate Images"):
    if user_prompt:
        with st.spinner('Generating images...'):
            image_urls = generate_images(user_prompt)
            for image_url in image_urls:
                st.image(image_url, width=300)
    else:
        st.error("Please enter a prompt.")

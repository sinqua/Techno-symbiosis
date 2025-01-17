import nest_asyncio

nest_asyncio.apply()

from llama_parse import LlamaParse

parser = LlamaParse(
    api_key="llx-YJdpGGZaNeYgfJwybnX7xq8igJgIw3GR1T2ZRzes7tBLMa4D",  # can also be set in your env as LLAMA_CLOUD_API_KEY
    result_type="text",  # "markdown" and "text" are available
    num_workers=4,  # if multiple files passed, split in `num_workers` API calls
    verbose=True,
    language="ko",  # Optionally you can define a language, default=en
)

# sync
# documents = parser.load_data("IMG_1979.jpeg")
documents = parser.load_data("korean.jpg")

texts = [doc.text_resource.text for doc in documents]

print(texts)

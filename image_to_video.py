from IPython import utils
import os
from byteplussdkarkruntime import Ark
from dotenv import load_dotenv
import utils

load_dotenv()
API_KEY = os.getenv("ARK_API_KEY")

client = Ark(
    api_key=os.getenv("ARK_API_KEY"),
    base_url="https://ark.ap-southeast.bytepluses.com/api/v3"
)

# Dialogue-driven comedy prompt optimized for Seedance 2.0 sequential generation
prompt = utils.load_prompt("sitcom.txt")

response = client.content_generation.tasks.create(
    model="dreamina-seedance-2-0-260128",
    content=[
        {
            "type": "text",
            "text": prompt,
        },
        {
            "type": "image_url",
            "image_url": {
                "url": utils.load_image("./images/male-character.png")
            },
            "role": "reference_image"
        },
        {
            "type": "image_url",
            "image_url": {
                "url": utils.load_image("./images/female-character.png")
            },
            "role": "reference_image"
        }
    ],
    generate_audio=True,
    ratio="16:9",
    duration=15,
    watermark=True,
    resolution="480p",
)

task_id = response.id
print(f"Task successfully submitted! Task ID: {task_id}")

# Wait for the video to finish generating
video_url = utils.poll_task(client, task_id)

saved_path = utils.download_video(video_url)
if saved_path:
    print(f"Video generation complete. Saved to {saved_path}")
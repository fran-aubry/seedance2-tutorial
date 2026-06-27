import os
from byteplussdkarkruntime import Ark
from dotenv import load_dotenv
import utils

load_dotenv()

client = Ark(
    api_key=os.getenv("ARK_API_KEY"),
    base_url="https://ark.ap-southeast.bytepluses.com/api/v3"
)

prompt = utils.load_prompt("./prompts/skate.txt")

response = client.content_generation.tasks.create(
    model="dreamina-seedance-2-0-260128",
    content=[
        {
            "type": "text",
            "text": prompt,
        },
        {
            "type": "video_url", 
            "video_url": {
                "url": "https://www.pexels.com/download/video/38213009/"
            },
            "role": "reference_video" 
        }
    ],
    generate_audio=True,
    ratio="16:9",
    duration=6,
    watermark=True,
    resolution="480p",
)

task_id = response.id
print(f"Task successfully submitted! Task ID: {task_id}")

video_url = utils.poll_task(client, task_id)
saved_path = utils.download_video(video_url)

if saved_path:
    print(f"Video generation complete. Saved to {saved_path}")
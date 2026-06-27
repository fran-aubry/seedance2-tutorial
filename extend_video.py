import os
from byteplussdkarkruntime import Ark
from dotenv import load_dotenv
import utils

load_dotenv()

client = Ark(
    api_key=os.getenv("ARK_API_KEY"),
    base_url="https://ark.ap-southeast.bytepluses.com/api/v3"
)

prompt = utils.load_prompt("./prompts/extend.txt")

response = client.content_generation.tasks.create(
    model="dreamina-seedance-2-0-260128",
    content=[
        {
            "type": "text",
            "text": f"Extend video. Extend @Video1 as follows: \n{prompt}",
        },
        {
            "type": "video_url",
            "video_url": {
                "url": "https://www.pexels.com/download/video/37898713/"
            },
            "role": "reference_video"
        }
    ],
    ratio="16:9",
    watermark=True,
    resolution="480p",
    duration=8,
)

task_id = response.id
print(f"Extension task submitted! Task ID: {task_id}")

video_url = utils.poll_task(client, task_id)
saved_path = utils.download_video(video_url)

if saved_path:
    print(f"Video extension complete. Saved to {saved_path}")
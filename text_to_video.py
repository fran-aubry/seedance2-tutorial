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

prompt = """
A cinematic close-up of a weary but hopeful female astronaut inside a dimly lit, dusty spaceship cabin. 
Soft blue light illuminates her face. 
She takes a deep breath, showing subtle emotional relief, looks directly into the camera, and says: 
'We finally made it. The atmosphere is stable.' 
The ambient sound of a low, rhythmic spaceship engine hums in the background.
"""

response = client.content_generation.tasks.create(
    model="dreamina-seedance-2-0-260128",
    content=[
        {
            "type": "text",
            "text": prompt,
        }
    ],
    generate_audio=True,
    ratio="16:9",
    duration=8,
    watermark=True,
    resolution="480p",
)

task_id = response.id
print(f"Task successfully submitted! Task ID: {task_id}")

# Wait for the video to finish generating
video_url = utils.poll_task(client, task_id)

utils.download_video(video_url, "./videos/space.mp4")
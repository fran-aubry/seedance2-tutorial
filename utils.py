import time
import requests
import base64
import os
import mimetypes


def poll_task(client, task_id, poll_interval=5):
    while True:
        try:
            task_status = client.content_generation.tasks.get(task_id=task_id)
            status = getattr(task_status, "status", None) or (task_status.get("status") if isinstance(task_status, dict) else None)
            
            if status == "succeeded":
                print("\nTask completed successfully.")
                return task_status.content.video_url
                
            elif status == "failed":
                error_details = getattr(task_status, "error", "Unknown error occurred during processing.")
                raise RuntimeError(f"Task failed: {error_details}")
                
            print(".", end="", flush=True)
            time.sleep(poll_interval)
        except Exception as e:
            if isinstance(e, RuntimeError):
                raise
            print(f"\nWarning: Error polling task (will retry): {e}")
            time.sleep(poll_interval)


def download_video(url, output_path="./videos"):
    try:
        timestamp = int(time.time())
        
        if os.path.isdir(output_path):
            final_path = os.path.join(output_path, f"video_{timestamp}.mp4")
        else:
            dir_name = os.path.dirname(output_path) or "."
            base_name = os.path.basename(output_path)
            name, ext = os.path.splitext(base_name)
            final_path = os.path.join(dir_name, f"{name}_{timestamp}{ext}")
            
        # Ensure the destination directory exists
        os.makedirs(os.path.dirname(final_path), exist_ok=True)
            
        print(f"Downloading video from {url} to {final_path}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(final_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Video successfully downloaded to '{final_path}'")
        return final_path
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None


def load_prompt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()


def load_image(file_path, default_mime="image/jpeg"):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = default_mime
        
    with open(file_path, "rb") as file_obj:
        encoded_string = base64.b64encode(file_obj.read()).decode('utf-8')
        
    return f"data:{mime_type};base64,{encoded_string}"

def load_audio(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found at: {file_path}")

    # Guess the mime type (e.g., audio/mpeg for mp3, audio/wav for wav)
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = "audio/mpeg" # Fallback to mp3 just in case

    with open(file_path, "rb") as audio_file:
        encoded_string = base64.b64encode(audio_file.read()).decode('utf-8')
        
    return f"data:{mime_type};base64,{encoded_string}"
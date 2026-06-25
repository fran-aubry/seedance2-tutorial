import time
import requests


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


def download_video(url, output_path = "video.mp4"):
    try:
        print(f"Downloading video from {url} to {output_path}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Video successfully downloaded to '{output_path}'")
        return True
    except Exception as e:
        print(f"Error downloading video: {e}")
        return False
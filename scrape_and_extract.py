import os
import subprocess

def find_bag_directories(base_path):
    """
    Recursively finds directories containing .mcap files within the base path.
    """
    print(f"Searching for .mcap files in base path: {base_path}")
    bag_directories = []
    for root, dirs, files in os.walk(base_path):
        if any(file.endswith('.mcap') for file in files):
            print(f"Found .mcap files in directory: {root}")
            bag_directories.append(root)
    print(f"Total directories with .mcap files found: {len(bag_directories)}")
    return bag_directories

def issue_extract_command(bag_dir, topic="/image_raw", video_name="video.mp4"):
    """
    Issues the extract video command for a given bag directory, creating the 'videos' directory if it doesn't exist.
    """
    videos_dir = os.path.join(bag_dir, "videos")
    output_video_path = os.path.join(videos_dir, video_name)
    thumbnail_path = output_video_path.replace('.mp4', '.jpg')

    if not os.path.exists(videos_dir):
        print(f"Creating videos directory at: {videos_dir}")
    os.makedirs(videos_dir, exist_ok=True)

    command = [
        "python3", "rosbag_to_video.py",
        "-source", bag_dir,
        "-topic", topic,
        "-output", output_video_path,
        "-thumbnail", thumbnail_path
    ]

    print(f"Issuing command: {' '.join(command)}")

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Command output:\n{result.stdout}")
        print(f"Command errors (if any):\n{result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        print(f"Output:\n{e.output}")
        print(f"Errors:\n{e.stderr}")
        
        # Handle specific error for invalid file end magic and skip this file
        if "File end magic is invalid" in e.stderr:
            print(f"Skipping directory due to invalid file format: {bag_dir}")

def main():
    base_path = "/recordings"  # Updated to match the actual path

    # Find all directories with .mcap files
    bag_dirs = find_bag_directories(base_path)

    # Issue the extract command for each bag directory
    for bag_dir in bag_dirs:
        print(f"Processing bag directory: {bag_dir}")
        issue_extract_command(bag_dir)

if __name__ == "__main__":
    main()

import argparse
import cv2
from rosbags.rosbag2 import Reader, ReaderError
from rosbags.typesys import get_typestore, Stores
from rosbags.image import message_to_cvimage
import os
# from tqdm import tqdm

def extract_video(bag_path, topic_name, video_path, thumbnail_path):
    print(f"Opening bag: {bag_path}")

    # Initialize the ROS 2 typestore
    typestore = get_typestore(Stores.ROS2_HUMBLE)

    # Open the ROS 2 bag using rosbags
    # try:
    # Try opening the bag with the default storage type
    with Reader(bag_path) as reader:
        reader.metadata = {'storage_identifier': 'mcap'}  # Force storage type
        reader.open()
        print("Loaded metadata:", reader.metadata)

        # Check if the topic exists in the bag
        connections = [x for x in reader.connections if x.topic == topic_name]
        if not connections:
            print(f"Topic {topic_name} not found in the bag.")
            return
        
        conn = connections[0]

        # OpenCV video writer setup
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = None  # Will initialize after getting the first frame

        thumbnail_saved = False
        prev_timestamp = None
        frame_count = 0
        frame_rate = None

        print(f"Reading frames from topic {topic_name} and saving to {video_path}")

        # Iterate over messages in the topic
        # progress_bar = tqdm(total=reader.message_count, desc="Processing frames")

        for connection, timestamp, rawdata in reader.messages(connections=[conn]):
            # Deserialize the message using typestore.deserialize_cdr()
            msg = typestore.deserialize_cdr(rawdata, conn.msgtype)

            # Convert the ROS message to OpenCV-compatible image using message_to_cvimage
            try:
                cv_image = message_to_cvimage(msg)
            except Exception as e:
                print(f"Failed to convert image for frame {frame_count}: {e}")
                continue

            # Initialize video writer after getting the first frame's dimensions
            if frame_count == 0:
                frame_timestamps = [timestamp]  # List to store timestamps of the first 5 frames
                frame_rate = 20.0  # Default frame rate if estimation fails
                video_writer = cv2.VideoWriter(video_path, fourcc, frame_rate, (cv_image.shape[1], cv_image.shape[0]))

            # Collect timestamps for the first 5 frames
            elif frame_count < 5:
                frame_timestamps.append(timestamp)

            # Calculate frame rate after collecting 5 timestamps
            if frame_count == 5:
                # Calculate average frame time difference based on 5 timestamps
                time_diffs = [(frame_timestamps[i] - frame_timestamps[i - 1]) * 1e-9 for i in range(1, 5)]  # Convert to seconds
                avg_time_diff = sum(time_diffs) / len(time_diffs)
                if avg_time_diff > 0:
                    frame_rate = 1.0 / avg_time_diff
                    print(f"Estimated frame rate: {frame_rate} fps")
                    # Reinitialize video writer with the calculated frame rate
                    video_writer = cv2.VideoWriter(video_path, fourcc, frame_rate, (cv_image.shape[1], cv_image.shape[0]))

            # Save the first frame as an image if not done yet
            if not thumbnail_saved:
                if thumbnail_path:
                    cv2.imwrite(thumbnail_path, cv_image)
                else:
                    cv2.imwrite(video_path.replace('.mp4', '_thumbnail.png'), cv_image)
                thumbnail_saved = True

            # Write the frame to the video
            video_writer.write(cv_image)
            frame_count += 1
            # print ({frame_count} "/" {})
            # progress_bar.update(1)

        # Cleanup
        if video_writer:
            video_writer.release()
        # progress_bar.close()

        print(f"Done. {frame_count} frames written to {video_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert ROS2 video bag file to video file using rosbags and rosbags_image.')
    parser.add_argument('-source', dest='bag_path', required=True, help='ROS2 bag file path')
    parser.add_argument('-topic', dest='topic_name',  default="/arducam/left/image_raw" , required=True, help='Video topic name')
    parser.add_argument('-output', dest='video_path',  default="left.mp4" , required=True, help='Output video file path (make sure to include .mp4)')
    parser.add_argument('-thumbnail', dest='thumbnail_path', help='Path to save the first image')

    args = parser.parse_args()

    print("Bag path:", args.bag_path)
    print("Video path:", args.video_path)
    print("thumbnail path:", args.thumbnail_path)

    extract_video(args.bag_path, args.topic_name, args.video_path, args.thumbnail_path)

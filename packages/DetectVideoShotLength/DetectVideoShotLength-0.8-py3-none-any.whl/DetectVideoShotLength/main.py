import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from skimage.metrics import structural_similarity as compare_ssim


# class DetectVideoShotLength:
def detect_video_cuts(video_path, output_dir, threshold_hist=0.15, threshold_ssim=0.85):
    """
    Detects cuts in a video based on histogram differences between consecutive frames
    and saves the frames where cuts are confirmed with SSIM.

    Parameters:
        video_path (str): Path to the input video file.
        output_dir (str): Directory where the cut frames will be saved.
        threshold_hist (float): Histogram difference threshold to detect cuts.
        threshold_ssim (float): SSIM threshold to confirm cuts.
    
    Returns:
        cut_frames (list): List of frame numbers where cuts were detected.
        fps (float): Frames per second of the video.
        total_seconds (float): Total duration of the video in seconds.
    """
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Load the video
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)  # Get frames per second
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # Get total number of frames
    
    if not fps or not total_frames:
        print(f"Failed to retrieve video information from {video_path}")
        return [], 0, 0

    # Calculate total video duration
    total_seconds = total_frames / fps
    total_minutes = int(total_seconds // 60)
    total_secs = int(total_seconds % 60)
    print(f"Total video length: {total_minutes} minutes {total_secs} seconds")

    # Read the first frame
    ret, prev_frame = cap.read()
    if not ret:
        print(f"Failed to read the first frame from video: {video_path}")
        return [], 0, 0

    # Calculate RGB histograms for the first frame
    prev_hist_r = cv2.calcHist([prev_frame], [0], None, [256], [0, 256])
    prev_hist_g = cv2.calcHist([prev_frame], [1], None, [256], [0, 256])
    prev_hist_b = cv2.calcHist([prev_frame], [2], None, [256], [0, 256])

    frame_number = 0
    rgb_cuts=0
    cut_frames = []
    actual_cut_frames = []

    # Iterate through video frames
    with tqdm(total=total_frames, desc="Processing frames") as pbar:
        while True:
            ret, curr_frame = cap.read()
            if not ret:
                break

            # Calculate RGB histograms for the current frame
            curr_hist_r = cv2.calcHist([curr_frame], [0], None, [256], [0, 256])
            curr_hist_g = cv2.calcHist([curr_frame], [1], None, [256], [0, 256])
            curr_hist_b = cv2.calcHist([curr_frame], [2], None, [256], [0, 256])

            # Calculate histogram differences for each color channel using Bhattacharyya distance
            hist_diff_r = cv2.compareHist(prev_hist_r, curr_hist_r, cv2.HISTCMP_BHATTACHARYYA)
            hist_diff_g = cv2.compareHist(prev_hist_g, curr_hist_g, cv2.HISTCMP_BHATTACHARYYA)
            hist_diff_b = cv2.compareHist(prev_hist_b, curr_hist_b, cv2.HISTCMP_BHATTACHARYYA)

            # Calculate total histogram difference (sum of RGB differences)
            total_hist_diff = (hist_diff_r + hist_diff_g + hist_diff_b) / 3

            # Check for cut based on histogram difference
            if total_hist_diff > threshold_hist:
                rgb_cuts += 1
                # Calculate SSIM only if a cut was detected
                prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
                curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
                ssim_diff = compare_ssim(prev_gray, curr_gray)

                # Confirm cut if SSIM difference indicates a cut
                if ssim_diff < threshold_ssim:
                    cut_frames.append(frame_number)

                    # Calculate timestamp in minutes and seconds
                    timestamp_seconds = frame_number / fps
                    minutes = int(timestamp_seconds // 60)
                    seconds = int(timestamp_seconds % 60)

                    # Save the frame at the detected cut
                    frame_filename = os.path.join(output_dir, f'frame_{minutes:02d}m_{seconds:02d}s.jpg')
                    actual_cut_frames.append(frame_filename)
                    cv2.imwrite(frame_filename, curr_frame)
                    prev_frame = curr_frame

            # Update the previous histograms and frame
            prev_hist_r = curr_hist_r
            prev_hist_g = curr_hist_g
            prev_hist_b = curr_hist_b
            frame_number += 1

            # Update tqdm progress
            pbar.update(1)

    # Release the video capture object
    cap.release()

    # Calculate and print average shot length if enough cuts were detected
    if len(cut_frames) > 0:
        avg_shot_length = total_seconds / len(set(actual_cut_frames))
        avg_minutes = int(avg_shot_length // 60)
        avg_secs = int(avg_shot_length % 60)

        print(f"Average shot length: {avg_minutes} minutes {avg_secs} seconds")
    else:
        print("Not enough cuts detected to calculate shot length.")

    print(f"Total cuts detected: {len(cut_frames)}")
    # print(f"Actual cuts detected: {len(set(actual_cut_frames))}")
    # print(f"RGB cuts detected: {rgb_cuts}")
    return cut_frames, fps, total_seconds





def plot_scene_lengths(results):
    cut_frames, fps, total_video_duration = results
    cut_times = [frame / fps for frame in cut_frames]
    
    # Add the total video duration as the last cut (for the last scene)
    cut_times.append(total_video_duration)
    
    # Calculate scene lengths (time between cuts)
    scene_lengths = [cut_times[i] - cut_times[i-1] for i in range(1, len(cut_times))]
    
    # Prepare the x-axis values (cumulative time at the start of each scene)
    scene_start_times = cut_times[:-1]  # All cut times except the last one

    # Plot the scene lengths over time
    plt.figure(figsize=(10, 6))
    plt.step(scene_start_times, scene_lengths, where='post', label='Scene Lengths')

    # Get the current tick positions chosen by matplotlib
    current_ticks = plt.gca().get_xticks()

    # Filter out negative ticks to ensure only positive values from zero
    positive_ticks = [t for t in current_ticks if t >= 0]

    # Convert positive ticks to minutes:seconds format
    formatted_ticks = [f"{int(t // 60)}:{int(t % 60):02d}" for t in positive_ticks]
    
    # Set the formatted ticks on the x-axis
    plt.xticks(positive_ticks, formatted_ticks)

    # Labels and title
    plt.xlabel('Time (minutes:seconds)')
    plt.ylabel('Scene Length (seconds)')
    plt.title('Scene Lengths Over Time')
    plt.legend()
    plt.show()


def list_scenes_sorted_by_length(results):
    cut_frames, fps, total_video_duration = results
    cut_times = [frame / fps for frame in cut_frames]
    
    # Add the total video duration as the last cut (for the last scene)
    cut_times.append(total_video_duration)
    
    # Calculate scene lengths (time between cuts) and associate start/end times
    scenes = [
        {
            "start": cut_times[i-1],  # Start time of the scene
            "end": cut_times[i],      # End time of the scene
            "length": cut_times[i] - cut_times[i-1]  # Length of the scene
        }
        for i in range(1, len(cut_times))
    ]
    
    # Sort scenes by length in descending order
    sorted_scenes = sorted(scenes, key=lambda x: x['length'], reverse=True)
    
    # Function to convert seconds to hours:minutes:seconds
    def format_time(seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours}:{minutes:02d}:{secs:02d}"

    # Print the sorted scenes with their start and end times
    print(f"{'Scene #':<10}{'Start Time (h:m:s)':<25}{'End Time (h:m:s)':<25}{'Length (s)':<15}")
    print("-" * 70)
    for i, scene in enumerate(sorted_scenes, 1):
        start_time = format_time(scene['start'])
        end_time = format_time(scene['end'])
        print(f"{i:<10}{start_time:<25}{end_time:<25}{scene['length']:<15.2f}")




def plot_scene_length_frequencies(results):
    cut_frames, fps, total_video_duration = results
    cut_times = [frame / fps for frame in cut_frames]
    
    # Add the total video duration as the last cut (for the last scene)
    cut_times.append(total_video_duration)
    
    # Calculate scene lengths (time between cuts)
    scene_lengths = [cut_times[i] - cut_times[i-1] for i in range(1, len(cut_times))]
    
    # Get the frequency of scene lengths rounded to the nearest second
    scene_length_rounded = [round(length) for length in scene_lengths]
    
    # Get the frequency of each scene length
    unique, counts = np.unique(scene_length_rounded, return_counts=True)
    
    # Adjust bar width and spacing
    bar_width = 0.6  # Width of the bars
    x_positions = np.arange(len(unique))  # X positions for bars with spacing
    
    # Plot the frequency of scene lengths with logarithmic scale
    plt.figure(figsize=(15, 6))
    bars = plt.bar(x_positions, counts, width=bar_width, align='center', label='Frequency of Scene Lengths')
    
    # Set the y-axis to a logarithmic scale
    plt.yscale('log')
    
    # Annotate the bars with counts
    for bar, count in zip(bars, counts):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                str(count), ha='center', va='bottom')
    
    # Labels and title
    plt.xticks(x_positions, unique)  # Set x-ticks to be the unique scene lengths
    plt.xlabel('Scene Length (seconds)')
    plt.ylabel('Frequency (log scale)')
    plt.title('Frequency of Scene Lengths')
    plt.legend()
    plt.show()





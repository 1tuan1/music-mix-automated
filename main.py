import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, concatenate_audioclips, CompositeVideoClip
import inquirer
import glob

def create_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def create_song_list_clip(timestamps, song_names, duration, width=1920, height=1080):
    from PIL import Image, ImageDraw, ImageFont
    import numpy as np

    # Create a transparent background image
    background = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(background)
    
    try:
        # Try to use Arial font, fall back to default if not available
        font = ImageFont.truetype('Arial', 28)  # Slightly smaller font
        title_font = ImageFont.truetype('Arial', 40)  # Smaller title
    except OSError:
        # Fallback to default font
        font = ImageFont.load_default()
        title_font = ImageFont.load_default()

    # Calculate text positions
    padding_left = 40  # Left padding
    padding_right = 40  # Right padding
    padding_top = 30  # Top padding
    line_height = 35  # Reduced line height
    usable_width = width - (padding_left + padding_right)
    
    # Draw title
    title = "SONG LIST"  # Changed to uppercase
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_width) // 2, padding_top), title, fill='white', font=title_font, stroke_width=3)

    # Split songs into columns
    mid_point = width // 2
    songs_per_column = len(timestamps) // 2 + len(timestamps) % 2  # Handle odd number of songs
    
    # Draw all songs in a single column with full width
    y = padding_top + 60  # Start below title
    for i, (timestamp, name) in enumerate(zip(timestamps, song_names)):
        text = f"{i+1:02d}. {timestamp} → {name.upper()}"  # Changed song name to uppercase
        
        # Add stroke effect for better visibility
        # First draw black outline
        for offset_x, offset_y in [(-1,-1), (-1,1), (1,-1), (1,1)]:
            draw.text((padding_left + offset_x, y + offset_y), text, fill='black', font=font)
        
        # Then draw white text
        draw.text((padding_left, y), text, fill='white', font=font)
        
        y += line_height

    # Convert PIL Image to numpy array for MoviePy
    image_array = np.array(background)
    
    # Create clip from the image
    txt_clip = ImageClip(image_array).set_duration(duration)
    
    return [txt_clip]

def select_folder():
    """Prompt user to select a music folder"""
    # Get all directories in current path
    current_dir = os.getcwd()
    dirs = [d for d in os.listdir(current_dir) 
            if os.path.isdir(os.path.join(current_dir, d))]
    
    if not dirs:
        print("No directories found!")
        return None
        
    questions = [
        inquirer.List('folder',
                     message='Select the music folder',
                     choices=dirs)
    ]
    
    answers = inquirer.prompt(questions)
    return answers['folder'] if answers else None

def select_background():
    """Prompt user to select a background image from backgrounds folder"""
    # Check if backgrounds folder exists
    backgrounds_folder = "backgrounds"
    if not os.path.exists(backgrounds_folder):
        os.makedirs(backgrounds_folder)
        print(f"Created '{backgrounds_folder}' directory. Please add background images there.")
        return None
    
    # Get all image files in backgrounds folder
    image_files = []
    for ext in ['.jpg', '.jpeg', '.png', '.mp4']:
        image_files.extend(glob.glob(os.path.join(backgrounds_folder, f"*{ext}")))
    
    # Convert to relative paths for display
    image_files = [os.path.basename(f) for f in image_files]
    
    if not image_files:
        print(f"No image files found in '{backgrounds_folder}' folder!")
        return None
        
    questions = [
        inquirer.List('background',
                     message='Select the background image/video',
                     choices=image_files)
    ]
    
    answers = inquirer.prompt(questions)
    if answers:
        # Return full path
        return os.path.join(backgrounds_folder, answers['background'])
    return None

def get_next_filename(base_path, extension):
    """Get next available filename by adding number suffix"""
    if not os.path.exists(f"{base_path}{extension}"):
        return f"{base_path}{extension}"
        
    counter = 1
    while os.path.exists(f"{base_path}_{counter}{extension}"):
        counter += 1
    return f"{base_path}_{counter}{extension}"

def main():
    # Let user select music folder
    music_folder = select_folder()
    if not music_folder:
        print("No music folder selected. Exiting...")
        return
        
    # Let user select background
    background_path = select_background()
    if not background_path:
        print("No background selected. Exiting...")
        return
    
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)
    
    # Get next available filenames
    video_path = get_next_filename(os.path.join(output_folder, "final_mix"), ".mp4")
    timestamp_path = get_next_filename(os.path.join(output_folder, "timestamps"), ".txt")
    
    # Get music files
    music_files = [f for f in os.listdir(music_folder) 
                  if f.lower().endswith(('.mp3', '.wav'))]
    
    if not music_files:
        print("No music files found!")
        return
    
    # Process audio files and create timestamps
    audio_clips = []
    current_time = 0
    timestamps = []
    song_names = []
    
    for music_file in music_files:
        audio = AudioFileClip(os.path.join(music_folder, music_file))
        audio_clips.append(audio)
        
        song_name = os.path.splitext(os.path.basename(music_file))[0]
        timestamps.append(create_timestamp(current_time))
        song_names.append(song_name)
        current_time += audio.duration
    
    # Create final audio
    final_audio = concatenate_audioclips(audio_clips)
    
    # Create background with proper sizing
    if background_path.lower().endswith(('.jpg', '.png', '.jpeg')):
        from PIL import Image
        # For static images, load with PIL first and convert to desired size
        pil_image = Image.open(background_path)
        pil_image = pil_image.resize((1920, 1080), Image.Resampling.LANCZOS)
        background = ImageClip(np.array(pil_image))
    else:
        # For videos, create and loop with target size
        background = VideoFileClip(background_path).resize((1920, 1080)).loop()
    
    # Set the duration after resizing
    background = background.set_duration(final_audio.duration)
    
    # Create text clips
    text_clips = create_song_list_clip(timestamps, song_names, final_audio.duration)
    
    # Combine all clips
    final_video = CompositeVideoClip([background] + text_clips)
    final_video = final_video.set_audio(final_audio)
    
    # Write output
    final_video.write_videofile(
        video_path,
        fps=24,
        codec='libx264',
        audio_codec='aac'
    )
    
    # Save timestamps to file
    with open(timestamp_path, "w", encoding='utf-8') as f:
        for timestamp, song in zip(timestamps, song_names):
            f.write(f"{timestamp} - {song}\n")

if __name__ == "__main__":
    main()
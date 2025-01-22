# Music Mix Video Generator

Automatically creates a video from music files with timestamps and background image/video. The program combines your music files into a single video with an overlay showing the current track list and timestamps.

## Features

- Combines multiple audio files into a single mix
- Overlays track list with timestamps
- Supports both static images and videos as background
- Generates YouTube-compatible timestamps
- Automatically numbers sequential output files
- Interactive folder and background selection
- Multiple background options support

## Prerequisites

- Python 3.x
- ffmpeg
- ImageMagick

### Installation

#### macOS
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python ffmpeg imagemagick

# Set ImageMagick path
echo 'export IMAGEMAGICK_BINARY="/opt/homebrew/bin/convert"' >> ~/.zshrc
source ~/.zshrc
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip ffmpeg imagemagick
```

#### Windows
1. Install Python from [python.org](https://www.python.org/downloads/)
2. Install ffmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
3. Install ImageMagick from [imagemagick.org](https://imagemagick.org/script/download.php)

## Project Setup

1. Clone or download this repository
2. Create the following project structure:
```
music_mix_automated/
├── music/            # Example music folder (you can have multiple)
├── backgrounds/      # Place background images/videos here
│   ├── bg1.jpg
│   ├── bg2.mp4
│   └── ...
├── output/          # Generated files will appear here
├── requirements.txt
├── setup.sh
└── main.py
```

3. Run setup:
```bash
# On macOS/Linux:
chmod +x setup.sh
./setup.sh

# On Windows:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

1. Create one or more folders containing your music files (.mp3 or .wav)
2. Add background images (jpg/png) or videos (mp4) to the `backgrounds/` folder
3. Run the program:
```bash
# On macOS/Linux:
source venv/bin/activate
python3 main.py

# On Windows:
venv\Scripts\activate
python main.py
```

4. Follow the interactive prompts to:
   - Select your music folder
   - Choose a background image/video

### Output

The program generates files in the `output/` directory:
- `final_mix.mp4`: The complete video with music and timestamps
- `timestamps.txt`: YouTube-compatible timestamps for video description

If files already exist, the program automatically adds a number suffix (e.g., `final_mix_1.mp4`).

## Customization

- Video resolution is set to 1920x1080 by default
- Font settings can be modified in the `create_song_list_clip` function
- Background image/video is automatically resized to match video resolution
- Create multiple music folders for different playlists/mixes

## Troubleshooting

### Python/pip Issues
```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

### ImageMagick Issues
Verify ImageMagick path:
```bash
echo $IMAGEMAGICK_BINARY  # Should output: /opt/homebrew/bin/convert
```

### Common Problems

1. **"No module named 'moviepy'"** or **"No module named 'inquirer'"**
   - Run `pip install -r requirements.txt` inside your virtual environment

2. **"ffmpeg not found"**
   - Ensure ffmpeg is installed and in your system PATH

3. **"No music files found!"**
   - Check that your selected folder contains music files
   - Verify files end with .mp3 or .wav

4. **"No background selected"**
   - Add image or video files to the `backgrounds/` folder
   - Supported formats: .jpg, .jpeg, .png, .mp4

## License

This project is open source and available under the MIT License.
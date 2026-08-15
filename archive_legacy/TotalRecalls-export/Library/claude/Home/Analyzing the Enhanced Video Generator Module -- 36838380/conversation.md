# Analyzing the Enhanced Video Generator Module

- **Provider:** claude
- **Account:** adenis258@gmail.com
- **Folder:** Home
- **ID:** 36838380-5c86-45d5-826a-2c84279b4dc9
- **Created:** 2025-04-01T11:20:39.981201Z
- **Updated:** 2025-04-01T11:23:31.014325Z

---

## Q1: You were interrupted. Attached is the python script to the point where you were interrupted. The following were your com

You were interrupted. Attached is the python script to the point where you were interrupted. The following were your comments: I'll continue analyzing and understanding the `Enhanced Video Generator Module` code from where the document was cut off.
The code appears to be a comprehensive Python module for generating professional video content from scripts and audio files using MoviePy. Here's what I can observe from the partial code:
This module provides a `VideoGenerator` class with functionality to:
1. Load configurations from JSON
2. Process video segments with different types (narration, YouTube clips, interviews, data visualizations)
3. Add B-roll footage based on keywords
4. Create text overlays and captions
5. Handle transitions between segments
6. Add intro/outro sequences
7. Apply watermarks/logos
8. Add background music
9. Generate thumbnails
The class has methods for:
* Initializing directories and configurations
* Building a B-roll cache for quickly finding relevant footage
* Processing different segment types (narration, interviews, YouTube clips, data visualizations)
* Creating text clips when no suitable B-roll is available
* Resizing clips to match project dimensions
* Adding captions to video clips
* Creating error notification clips when segments fail
The implementation uses MoviePy as its core video processing library and follows a modular approach to handle different aspects of video generation.

I'll continue analyzing the `Enhanced Video Generator Module` code based on what you've shared. Let me pick up where we left off and provide further insights into the functionality and structure of this video generation system.

From the comments you shared, it appears this is a sophisticated video generation pipeline built with MoviePy that handles numerous aspects of professional video creation, including:

- Processing multiple content types (narration, YouTube clips, interviews, data visualizations)
- Intelligent B-roll selection and integration
- Text overlays and captions
- Transitions between segments
- Intro/outro sequences
- Branding elements (watermarks/logos)
- Background music integration
- Thumbnail generation

Without seeing the actual code, I can offer some additional analysis on what a system like this would typically need to handle:

### Advanced Features This Likely Includes

1. **Resource Management**: A robust caching system for B-roll and other assets to prevent redundant processing

2. **Error Handling**: The "error notification clips" method suggests fallback mechanisms when segment processing fails

3. **Configuration-Driven Workflow**: The JSON configuration loading indicates a flexible, declarative approach to video specifications

4. **Pipeline Architecture**: The modular approach allows for independent processing of different video elements before final composition

5. **Media Transformations**: Methods for resizing and formatting various inputs to maintain consistent output quality

### Potential Extension Points

This system could be extended with:

1. **AI-Enhanced Content Selection**: Using NLP to better match B-roll with script content

2. **Style Transfer**: Applying consistent visual styles across disparate footage sources

3. **Performance Optimization**: Parallel processing for handling multiple segments simultaneously

4. **Cloud Integration**: Offloading processing or accessing remote asset libraries

5. **Analytics**: Tracking which segments and styles perform best with viewers

I'd be happy to provide more specific insights if you'd like to share the actual code, or I can help with implementing or extending particular features of this video generation system.

I'll analyze the `Enhanced Video Generator Module` code that was provided. This is part 1 of what appears to be a comprehensive video generation system built with MoviePy.

Looking at the code so far, I can see this is a sophisticated implementation that handles numerous aspects of professional video creation. Let me break down the key components and functionality:

### Core Structure and Initialization

The `VideoGenerator` class is the central component with methods for:

1. **Configuration Management**:
   - Loading settings from JSON files
   - Setting up directory structures for assets, outputs, and temp files

2. **B-roll Management**:
   - Creating an intelligent categorized cache of available footage
   - Extracting metadata from filenames and file properties
   - Organized by categories with keyword mapping

3. **Video Generation Pipeline**:
   - Main `generate_video` method that orchestrates the entire process
   - Processing segments based on their type (narration, interviews, YouTube clips, visualizations)
   - Adding intro/outro sequences, watermarks, and background music

### Segment Processing

The system handles multiple types of video segments:

1. **Narration with B-roll**:
   - Intelligent selection of appropriate B-roll footage based on keywords
   - Dynamic sequencing with visual effects like subtle zooms
   - Fallback to text-based clips when suitable footage isn't available

2. **YouTube Clips**:
   - Placeholder for downloading YouTube content (would need implementation)
   - Options for handling original audio (keep, replace, or overlay)
   - Attribution handling

3. **Interview Segments**:
   - Styled presentation with attribution and quotation marks
   - Consistent branding through background colors and text styling

4. **Data Visualization**:
   - Placeholder for integrating data visualizations
   - Structured layout with title and explanatory text

### Technical Features

The implementation includes several advanced technical aspects:

1. **Error Handling**:
   - Graceful segment failure with visual error notifications
   - Detailed logging throughout the process

2. **Media Formatting**:
   - Intelligent resizing to maintain aspect ratios
   - Cropping to ensure consistent dimensions

3. **Visual Enhancements**:
   - Caption generation and overlay
   - Attribution and watermarking
   - Transition effects

The code is structured using Python best practices with comprehensive type hinting, error handling, and logging. It appears the class is not completely shown in this document (it seems to be cut off at the `_add_watermark` method), suggesting there are additional methods in a subsequent part.

Would you like me to focus on any particular aspect of this code in more detail, or would you prefer to see the continuation of the code analysis?

---

## Q2: please complete the script

please complete the script

<antArtifact identifier="video-generator-script" type="application/vnd.ant.code" language="python" title="Enhanced Video Generator Module">
"""
Enhanced Video Generator Module

This module generates professional video content from scripts and audio
files using MoviePy. It handles transitions, b-roll footage, captions, and more.
"""

import os
import json
import logging
import random
import re
import time
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Union, Any

import requests
import numpy as np
from moviepy.editor import (
    VideoFileClip, AudioFileClip, ImageClip, TextClip,
    CompositeVideoClip, concatenate_videoclips, vfx,
    ColorClip, CompositeAudioClip
)
from moviepy.video.tools.subtitles import SubtitlesClip
from PIL import Image, ImageFilter

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class VideoGenerator:
    """
    Video Generator class that processes scripts, audio, and visual assets
    to create professional news videos.
    """

    def __init__(self, config_path: str = "config/video_generator.json"):
        """
        Initialize the VideoGenerator with configuration settings.

        Args:
            config_path: Path to the configuration file
        """
        self.logger = logging.getLogger(__name__)
        self.config = self._load_config(config_path)

        # Initialize directories
        self.output_dir = self.config.get("output_dir", "output/videos")
        self.assets_dir = self.config.get("assets_dir", "assets")
        self.audio_dir = self.config.get("audio_dir", "output/audio")
        self.b_roll_dir = self.config.get("b_roll_dir", "assets/b_roll")
        self.temp_dir = self.config.get("temp_dir", "temp")
        self.thumbnail_dir = self.config.get("thumbnail_dir", "output/thumbnails")

        # Create directories if they don't exist
        for directory in [self.output_dir, self.assets_dir, self.temp_dir,
                         self.thumbnail_dir, self.b_roll_dir]:
            os.makedirs(directory, exist_ok=True)

        # Video settings
        self.width = self.config.get("width", 1920)
        self.height = self.config.get("height", 1080)
        self.fps = self.config.get("fps", 30)
        self.transition_duration = self.config.get("transition_duration", 0.5)

        # Branding
        self.logo_path = self.config.get("logo_path", "assets/logo.png")
        self.intro_path = self.config.get("intro_path", "assets/intro.mp4")
        self.outro_path = self.config.get("outro_path", "assets/outro.mp4")
        self.background_music_path = self.config.get("background_music",
                                                   "assets/background_music.mp3")

        # YouTube API settings
        self.youtube_api_key = os.environ.get("YOUTUBE_API_KEY",
                                            self.config.get("youtube_api_key", ""))

        # Initialize asset cache
        self.b_roll_cache = {}
        self._initialize_b_roll_cache()
        self.logger.info("VideoGenerator initialized successfully")

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load configuration from a JSON file.

        Args:
            config_path: Path to the configuration file

        Returns:
            Dict containing configuration settings
        """
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            self.logger.info(f"Configuration loaded from {config_path}")
            return config
        except Exception as e:
            self.logger.warning(f"Error loading config: {e}. Using defaults.")
            return {}

    def _initialize_b_roll_cache(self) -> None:
        """
        Initialize the B-roll cache by scanning the B-roll directory
        and organizing clips by categories based on filenames.
        """
        if not os.path.exists(self.b_roll_dir):
            self.logger.warning(f"B-roll directory {self.b_roll_dir} not found")
            return

        # Scan B-roll directory
        for root, _, files in os.walk(self.b_roll_dir):
            for filename in files:
                if filename.endswith(('.mp4', '.mov', '.avi')):
                    filepath = os.path.join(root, filename)
                    # Extract category from directory or filename
                    rel_path = os.path.relpath(root, self.b_roll_dir)
                    if rel_path == '.':
                        # Try to extract category from filename (e.g., politics_meeting.mp4)
                        parts = filename.split('_')
                        if len(parts) > 1:
                            category = parts[0].lower()
                        else:
                            category = "general"
                    else:
                        # Use directory name as category
                        category = rel_path.split(os.path.sep)[0].lower()

                    # Add to cache
                    if category not in self.b_roll_cache:
                        self.b_roll_cache[category] = []
                    self.b_roll_cache[category].append({
                        "path": filepath,
                        "filename": filename,
                        "category": category,
                        "metadata": self._extract_clip_metadata(filepath, filename)
                    })

        self.logger.info(f"B-roll cache initialized with {sum(len(clips) for clips in self.b_roll_cache.values())} clips")

    def _extract_clip_metadata(self, filepath: str, filename: str) -> Dict[str, Any]:
        """
        Extract metadata from a video clip based on filename and simple inspection.

        Args:
            filepath: Path to the video file
            filename: Name of the video file

        Returns:
            Dict containing metadata
        """
        # Extract keywords from filename
        metadata = {
            "keywords": [word.lower() for word in re.split(r'[_\- ]', os.path.splitext(filename)[0])
                      if len(word) > 2]
        }

        # Optional: Check duration and dimensions (expensive, so we'll make it configurable)
        if self.config.get("extract_detailed_metadata", False):
            try:
                with VideoFileClip(filepath) as clip:
                    metadata["duration"] = clip.duration
                    metadata["width"] = clip.w
                    metadata["height"] = clip.h
            except Exception as e:
                self.logger.warning(f"Error extracting metadata from {filepath}: {e}")

        return metadata

    def generate_video(self, script_data: Dict[str, Any], output_filename: Optional[str] = None) -> str:
        """
        Generate a complete video from script data and audio files.

        Args:
            script_data: Dictionary containing script information and segment details
            output_filename: Optional filename for the output video

        Returns:
            Path to the generated video file
        """
        self.logger.info(f"Starting video generation for script: {script_data.get('title', 'Untitled')}")

        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = re.sub(r'[^\w\-_]', '_', script_data.get('title', 'untitled'))
            output_filename = f"{safe_title}_{timestamp}.mp4"

        output_path = os.path.join(self.output_dir, output_filename)

        try:
            # 1. Generate segments
            segments = self._process_segments(script_data)

            # 2. Add intro and outro
            clips = self._add_intro_outro(segments)

            # 3. Create final composite
            final_clip = concatenate_videoclips(clips, method="compose")

            # 4. Add watermark/logo if available
            final_clip = self._add_watermark(final_clip)

            # 5. Add background music
            final_clip = self._add_background_music(final_clip)

            # 6. Write output file
            self.logger.info(f"Writing video to {output_path}")
            final_clip.write_videofile(
                output_path,
                fps=self.fps,
                codec='libx264',
                audio_codec='aac',
                threads=4,
                logger=None  # Disable MoviePy's logger to avoid double logging
            )

            # 7. Generate thumbnail
            thumbnail_path = self._generate_thumbnail(final_clip, script_data)

            # 8. Clean up resources
            final_clip.close()
            for clip in clips:
                clip.close()

            self.logger.info(f"Video generation completed: {output_path}")
            return output_path

        except Exception as e:
            self.logger.error(f"Error generating video: {e}", exc_info=True)
            raise

    def _process_segments(self, script_data: Dict[str, Any]) -> List[VideoFileClip]:
        """
        Process script segments into video clips.

        Args:
            script_data: Script data containing segments

        Returns:
            List of processed video segment clips
        """
        segments = script_data.get('segments', [])
        processed_segments = []

        for i, segment in enumerate(segments):
            try:
                # Get audio file path from segment
                audio_file = segment.get('audio_file')
                if not audio_file:
                    audio_file = os.path.join(self.audio_dir, f"segment_{i}.mp3")

                if not os.path.exists(audio_file):
                    self.logger.warning(f"Audio file not found: {audio_file}. Skipping segment.")
                    continue

                # Load audio clip
                audio_clip = AudioFileClip(audio_file)

                # Create segment video
                segment_clip = self._create_segment_clip(segment, audio_clip, i)
                processed_segments.append(segment_clip)

            except Exception as e:
                self.logger.error(f"Error processing segment {i}: {e}", exc_info=True)
                # Create an error notification clip instead
                error_clip = self._create_error_clip(f"Error in segment {i}", 3)
                processed_segments.append(error_clip)

        return processed_segments

    def _create_segment_clip(self, segment: Dict[str, Any], audio_clip: AudioFileClip,
                           segment_index: int) -> VideoFileClip:
        """
        Create a video clip for a single script segment.

        Args:
            segment: Segment data
            audio_clip: Audio clip for the segment
            segment_index: Index of the segment

        Returns:
            Completed video clip for the segment
        """
        segment_type = segment.get('type', 'narration')
        content = segment.get('content', '')

        # Different treatment based on segment type
        if segment_type == 'youtube_clip':
            return self._process_youtube_clip(segment, audio_clip)
        elif segment_type == 'interview':
            return self._create_interview_clip(segment, audio_clip)
        elif segment_type == 'data_visualization':
            return self._create_data_visualization(segment, audio_clip)
        else:  # Default: narration with b-roll
            return self._create_narration_clip(segment, audio_clip, segment_index)

    def _create_narration_clip(self, segment: Dict[str, Any], audio_clip: AudioFileClip,
                             segment_index: int) -> VideoFileClip:
        """
        Create a narration clip with b-roll footage.

        Args:
            segment: Segment data
            audio_clip: Audio clip for the segment
            segment_index: Index of the segment

        Returns:
            Completed narration video clip
        """
        content = segment.get('content', '')
        keywords = segment.get('keywords', [])
        duration = audio_clip.duration

        # Find appropriate b-roll footage based on keywords
        b_roll_clips = self._select_b_roll(keywords, duration)

        # If no suitable b-roll found, create a text-based clip
        if not b_roll_clips:
            self.logger.info(f"No suitable b-roll found for segment {segment_index}. Creating text clip.")
            text_clip = self._create_text_clip(content, duration)
            final_clip = text_clip.set_audio(audio_clip)
            return final_clip

        # Create a sequence of b-roll clips
        video_sequence = []
        current_time = 0

        for clip_data in b_roll_clips:
            clip_path = clip_data["path"]
            try:
                clip = VideoFileClip(clip_path)
                # Adjust clip to fit the screen properly
                clip = self._resize_clip(clip)

                # Trim the clip to needed duration
                clip_duration = min(clip.duration, duration - current_time)
                if clip_duration <= 0:
                    clip.close()
                    break

                trimmed_clip = clip.subclip(0, clip_duration)

                # Add subtle zoom effect for visual interest
                if random.choice([True, False]):
                    trimmed_clip = trimmed_clip.fx(vfx.zoom, 1.05, 1.0)

                # Position in timeline
                positioned_clip = trimmed_clip.set_start(current_time)
                video_sequence.append(positioned_clip)
                current_time += clip_duration

                # Close original clip to free memory
                clip.close()
            except Exception as e:
                self.logger.error(f"Error processing b-roll clip {clip_path}: {e}")
                continue

        # If we couldn't create a long enough sequence, add a filler
        if current_time < duration:
            remaining_duration = duration - current_time
            filler = self._create_text_clip(content[-100:] if len(content) > 100 else content,
                                          remaining_duration)
            filler = filler.set_start(current_time)
            video_sequence.append(filler)

        # Composite all clips together
        composite = CompositeVideoClip(video_sequence, size=(self.width, self.height))

        # Add captions if enabled
        if self.config.get("add_captions", True):
            composite = self._add_captions(composite, content, audio_clip.duration)

        # Set audio track
        final_clip = composite.set_audio(audio_clip)

        return final_clip

    def _select_b_roll(self, keywords: List[str], desired_duration: float) -> List[Dict[str, Any]]:
        """
        Select appropriate b-roll clips based on keywords and duration.

        Args:
            keywords: List of keywords to match
            desired_duration: Desired total duration

        Returns:
            List of suitable b-roll clip data
        """
        if not keywords:
            # Use general category if no keywords provided
            categories = ["general"]
        else:
            # Convert keywords to potential categories
            categories = list(set([k.lower() for k in keywords]))
            categories.append("general")  # Always include general as fallback

        selected_clips = []
        total_duration = 0

        # First try to find clips by category
        for category in categories:
            if category in self.b_roll_cache:
                # Shuffle to get different clips each time
                category_clips = list(self.b_roll_cache[category])
                random.shuffle(category_clips)

                for clip_data in category_clips:
                    # Check if we already selected this clip
                    if any(selected["path"] == clip_data["path"] for selected in selected_clips):
                        continue

                    # Get clip duration
                    duration = clip_data.get("metadata", {}).get("duration")
                    if not duration:
                        # Estimate clip duration if not available
                        try:
                            with VideoFileClip(clip_data["path"]) as clip:
                                duration = clip.duration
                        except Exception as e:
                            self.logger.warning(f"Could not determine duration of {clip_data['path']}: {e}")
                            continue

                    # Add clip to selection
                    selected_clips.append(clip_data)
                    total_duration += duration

                    # Check if we have enough footage
                    if total_duration >= desired_duration:
                        break

            # If we have enough footage, stop searching
            if total_duration >= desired_duration:
                break

        # If still not enough, try keyword matching across all categories
        if total_duration < desired_duration:
            for category, clips in self.b_roll_cache.items():
                for clip_data in clips:
                    # Skip if already selected
                    if any(selected["path"] == clip_data["path"] for selected in selected_clips):
                        continue

                    # Check for keyword match in metadata
                    clip_keywords = clip_data.get("metadata", {}).get("keywords", [])
                    if any(keyword.lower() in clip_keywords for keyword in keywords):
                        # Get clip duration
                        duration = clip_data.get("metadata", {}).get("duration")
                        if not duration:
                            try:
                                with VideoFileClip(clip_data["path"]) as clip:
                                    duration = clip.duration
                            except Exception:
                                continue

                        # Add clip to selection
                        selected_clips.append(clip_data)
                        total_duration += duration

                        # Check if we have enough footage
                        if total_duration >= desired_duration:
                            break

                # If we have enough footage, stop searching
                if total_duration >= desired_duration:
                    break

        return selected_clips

    def _process_youtube_clip(self, segment: Dict[str, Any], audio_clip: AudioFileClip) -> VideoFileClip:
        """
        Process a YouTube clip segment.

        Args:
            segment: Segment data including YouTube URL
            audio_clip: Original audio clip (may be used for narration overlay)

        Returns:
            Processed YouTube clip
        """
        youtube_url = segment.get("youtube_url")
        if not youtube_url:
            self.logger.warning("YouTube clip segment missing URL")
            return self._create_error_clip("Missing YouTube URL", audio_clip.duration)

        clip_start = segment.get("clip_start", 0)
        clip_end = segment.get("clip_end")
        local_path = segment.get("local_path")

        try:
            # If local path is provided and exists, use it
            if local_path and os.path.exists(local_path):
                video_path = local_path
            else:
                # Download clip if needed
                video_path = self._download_youtube_clip(youtube_url, clip_start, clip_end)

            # Load video clip
            youtube_clip = VideoFileClip(video_path)

            # Apply timeframe if specified
            if clip_start or clip_end:
                if clip_end and clip_end > clip_start:
                    youtube_clip = youtube_clip.subclip(clip_start, clip_end)
                elif clip_start:
                    youtube_clip = youtube_clip.subclip(clip_start)

            # Resize to match our dimensions
            youtube_clip = self._resize_clip(youtube_clip)

            # Add attribution if needed
            if segment.get("add_attribution", True):
                youtube_clip = self._add_attribution(youtube_clip,
                                                   segment.get("source", "YouTube"))

            # Determine audio treatment
            audio_treatment = segment.get("audio_treatment", "original")
            if audio_treatment == "overlay":
                # Mix original audio with narration
                original_audio = youtube_clip.audio
                if original_audio:
                    # Reduce original volume
                    original_audio = original_audio.volumex(0.2)
                    # Combine with narration
                    mixed_audio = CompositeAudioClip([original_audio, audio_clip])
                    youtube_clip = youtube_clip.set_audio(mixed_audio)
            elif audio_treatment == "replace":
                # Replace with narration
                youtube_clip = youtube_clip.set_audio(audio_clip)
            # else: keep original audio

            return youtube_clip

        except Exception as e:
            self.logger.error(f"Error processing YouTube clip: {e}", exc_info=True)
            return self._create_error_clip(f"YouTube Processing Error", audio_clip.duration)

    def _download_youtube_clip(self, youtube_url: str, start_time: float = 0,
                             end_time: Optional[float] = None) -> str:
        """
        Download a YouTube clip. This is a placeholder - in a real implementation,
        you would use a library like pytube or youtube-dl.

        Args:
            youtube_url: YouTube URL
            start_time: Start time in seconds
            end_time: End time in seconds

        Returns:
            Path to downloaded clip
        """
        # This is a placeholder - in a real implementation, you would use
        # a library like pytube or youtube-dl
        self.logger.warning("YouTube download not implemented. Using a placeholder instead.")

        # For now, return a placeholder clip
        placeholder_path = os.path.join(self.b_roll_dir, "general", "placeholder.mp4")
        if os.path.exists(placeholder_path):
            return placeholder_path

        # If no placeholder, create a color clip
        temp_path = os.path.join(self.temp_dir, f"placeholder_{int(time.time())}.mp4")
        duration = 10 if end_time is None else min(end_time - start_time, 10)

        color_clip = ColorClip(size=(self.width, self.height),
                             color=(0, 0, 0),
                             duration=duration)

        text_clip = TextClip(
            "YouTube Clip Placeholder",
            fontsize=70,
            color='white',
            bg_color='transparent',
            font='Arial',
            size=(self.width - 100, None)
        ).set_position('center').set_duration(duration)

        url_clip = TextClip(
            youtube_url,
            fontsize=30,
            color='gray',
            bg_color='transparent',
            font='Arial'
        ).set_position(('center', self.height // 2 + 100)).set_duration(duration)

        composite = CompositeVideoClip([color_clip, text_clip, url_clip])
        composite.write_videofile(temp_path, fps=self.fps, logger=None)
        return temp_path

    def _create_interview_clip(self, segment: Dict[str, Any], audio_clip: AudioFileClip) -> VideoFileClip:
        """
        Create an interview clip with appropriate styling.

        Args:
            segment: Segment data
            audio_clip: Audio clip for the segment

        Returns:
            Video clip for the interview
        """
        # Extract person information
        person_name = segment.get("person_name", "Interviewee")
        person_title = segment.get("person_title", "")
        content = segment.get("content", "")

        # Create a background
        bg_color = segment.get("background_color", (16, 24, 32))
        duration = audio_clip.duration
        bg_clip = ColorClip(size=(self.width, self.height),
                          color=bg_color,
                          duration=duration)

        # Create text for the interview content
        text_clip = TextClip(
            content,
            fontsize=40,
            color='white',
            bg_color='transparent',
            font='Arial',
            method='caption',
            align='center',
            size=(self.width - 200, None)
        ).set_position(('center', 'center')).set_duration(duration)

        # Create attribution text
        attribution = f"{person_name}"
        if person_title:
            attribution += f"\n{person_title}"

        attribution_clip = TextClip(
            attribution,
            fontsize=30,
            color='white',
            bg_color='transparent',
            font='Arial',
            method='caption',
            align='center'
        ).set_position(('center', self.height - 150)).set_duration(duration)

        # Add quotation marks for style
        quote_clip = TextClip(
            '"',
            fontsize=120,
            color='white',
            bg_color='transparent',
            font='Arial-Bold',
            method='label'
        ).set_position((100, 150)).set_duration(duration)

        # Combine all elements
        composite = CompositeVideoClip(
            [bg_clip, quote_clip, text_clip, attribution_clip]
        )

        # Set audio
        final_clip = composite.set_audio(audio_clip)
        return final_clip

    def _create_data_visualization(self, segment: Dict[str, Any], audio_clip: AudioFileClip) -> VideoFileClip:
        """
        Create a data visualization clip.

        Args:
            segment: Segment data including visualization details
            audio_clip: Audio clip for the segment

        Returns:
            Data visualization video clip
        """
        # This is a placeholder. In a real implementation, you would generate
        # proper data visualizations using matplotlib, seaborn, or other libraries.
        duration = audio_clip.duration
        content = segment.get("content", "Data Visualization")

        # Create background
        bg_clip = ColorClip(size=(self.width, self.height),
                          color=(245, 245, 245),
                          duration=duration)

        # Create title
        title_clip = TextClip(
            segment.get("title", "Data Visualization"),
            fontsize=60,
            color='black',
            bg_color='transparent',
            font='Arial-Bold'
        ).set_position(('center', 100)).set_duration(duration)

        # Create a simple placeholder chart (would be replaced with actual visualization)
        chart_clip = ColorClip(
            size=(self.width - 400, self.height - 400),
            color=(200, 200, 200),
            duration=duration
        ).set_position('center')

        # Add explanation text
        text_clip = TextClip(
            content,
            fontsize=30,
            color='black',
            bg_color='transparent',
            font='Arial',
            method='caption',
            align='center',
            size=(self.width - 200, None)
        ).set_position(('center', self.height - 150)).set_duration(duration)

        # Combine all elements
        composite = CompositeVideoClip(
            [bg_clip, chart_clip, title_clip, text_clip]
        )

        # Set audio
        final_clip = composite.set_audio(audio_clip)
        return final_clip

    def _create_text_clip(self, text: str, duration: float) -> VideoFileClip:
        """
        Create a simple text clip for segments without b-roll.

        Args:
            text: Text content
            duration: Clip duration

        Returns:
            Text-based video clip
        """
        # Create a background
        bg_color = self.config.get("default_background_color", (16, 32, 48))
        bg_clip = ColorClip(size=(self.width, self.height),
                          color=bg_color,
                          duration=duration)

        # Create text clip
        font_size = self.config.get("default_font_size", 40)
        text_clip = TextClip(
            text,
            fontsize=font_size,
            color='white',
            bg_color='transparent',
            font='Arial',
            method='caption',
            align='center',
            size=(self.width - 200, None)
        ).set_position('center').set_duration(duration)

        # Combine clips
        composite = CompositeVideoClip([bg_clip, text_clip])
        return composite

    def _create_error_clip(self, error_message: str, duration: float) -> VideoFileClip:
        """
        Create an error notification clip for failed segments.

        Args:
            error_message: Error message to display
            duration: Clip duration

        Returns:
            Error notification video clip
        """
        # Create a red background
        bg_clip = ColorClip(size=(self.width, self.height),
                          color=(64, 0, 0),
                          duration=duration)

        # Create error message
        error_clip = TextClip(
            f"ERROR: {error_message}",
            fontsize=60,
            color='white',
            bg_color='transparent',
            font='Arial-Bold'
        ).set_position('center').set_duration(duration)

        # Combine clips
        composite = CompositeVideoClip([bg_clip, error_clip])
        return composite

    def _resize_clip(self, clip: VideoFileClip) -> VideoFileClip:
        """
        Resize a clip to match the project dimensions.

        Args:
            clip: Original video clip

        Returns:
            Resized video clip
        """
        # Calculate aspect ratios
        target_ratio = self.width / self.height
        clip_ratio = clip.w / clip.h

        if abs(clip_ratio - target_ratio) < 0.1:
            # Similar aspect ratios, just resize
            return clip.resize(width=self.width, height=self.height)
        elif clip_ratio > target_ratio:
            # Clip is wider, resize by height and crop
            new_width = int(self.height * clip_ratio)
            resized = clip.resize(height=self.height)
            # Center crop
            x_offset = (resized.w - self.width) // 2
            return resized.crop(x1=x_offset, x2=x_offset + self.width)
        else:
            # Clip is taller, resize by width and crop
            resized = clip.resize(width=self.width)
            # Center crop
            y_offset = (resized.h - self.height) // 2
            return resized.crop(y1=y_offset, y2=y_offset + self.height)

    def _add_captions(self, clip: VideoFileClip, text: str, duration: float) -> VideoFileClip:
        """
        Add captions to a video clip.

        Args:
            clip: Original video clip
            text: Text for captions
            duration: Clip duration

        Returns:
            Video clip with captions
        """
        font_size = self.config.get("caption_font_size", 30)

        # Create a caption background for better readability
        bg_width = self.width
        bg_height = font_size * 2  # Height of background bar

        bg_clip = ColorClip(
            size=(bg_width, bg_height),
            color=(0, 0, 0, 0.5),  # Semi-transparent black
            duration=duration
        ).set_position(('center', self.height - bg_height - 50))

        # Create caption text
        caption_clip = TextClip(
            text,
            fontsize=font_size,
            color='white',
            bg_color='transparent',
            font='Arial',
            method='caption',
            align='center',
            size=(self.width - 100, None)
        ).set_position(('center', self.height - bg_height - 50)).set_duration(duration)

        # Add captions to original clip
        return CompositeVideoClip([clip, bg_clip, caption_clip])

    def _add_watermark(self, clip: VideoFileClip) -> VideoFileClip:
        """
        Add a watermark/logo to the video.

        Args:
            clip: Original video clip

        Returns:
            Video clip with watermark
        """
        if not os.path.exists(self.logo_path):
            self.logger.warning(f"Logo not found at {self.logo_path}. Skipping watermark.")
            return clip

        try:
            logo_size = self.config.get("logo_size", (200, 100))
            position = self.config.get("logo_position", ("right", "top"))
            opacity = self.config.get("logo_opacity", 0.7)

            # Load and prepare logo
            logo = ImageClip(self.logo_path).resize(width=logo_size[0])
            logo = logo.set_opacity

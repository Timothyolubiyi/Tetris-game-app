import pygame
import numpy as np

def create_tetris_music():
    """Create a simple Tetris-like background music"""
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    
    # Tetris theme melody notes (simplified)
    notes = [
        659, 494, 523, 587, 523, 494, 440, 440, 523, 659, 587, 523, 494, 494, 523, 587, 659, 523, 440, 440,
        587, 698, 880, 784, 698, 659, 523, 659, 587, 523, 494, 494, 523, 587, 659, 523, 440, 440
    ]
    
    sample_rate = 22050
    note_duration = 0.3
    
    music_data = np.array([])
    
    for freq in notes:
        frames = int(note_duration * sample_rate)
        wave = np.sin(2 * np.pi * freq * np.linspace(0, note_duration, frames))
        # Add fade in/out to prevent clicks
        fade_frames = frames // 10
        wave[:fade_frames] *= np.linspace(0, 1, fade_frames)
        wave[-fade_frames:] *= np.linspace(1, 0, fade_frames)
        music_data = np.concatenate([music_data, wave])
    
    # Convert to 16-bit integers
    music_data = (music_data * 32767 * 0.3).astype(np.int16)
    
    # Create stereo sound
    stereo_data = np.zeros((len(music_data), 2), dtype=np.int16)
    stereo_data[:, 0] = music_data
    stereo_data[:, 1] = music_data
    
    return pygame.sndarray.make_sound(stereo_data)

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    sound = create_tetris_music()
    sound.play(loops=-1)
    pygame.time.wait(10000)  # Play for 10 seconds
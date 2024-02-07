import pygame
import time


def play_music(file_path, loop=True):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play(-1 if loop else 0)  # -1 means loop indefinitely


if __name__ == '__main__':
    # Replace "your_audio.mp3" with the path to your .mp3 file
    audio_file = "~/Downloads/sounds/your_audio.mp3"

    # Set loop to True to play the audio in a continuous loop
    play_music(audio_file, loop=True)

    try:
        while True:
            time.sleep(180)  # Sleep for 3 minutes (180 seconds) between loops
    except KeyboardInterrupt:
        pygame.mixer.music.stop()
    finally:
        pygame.quit()

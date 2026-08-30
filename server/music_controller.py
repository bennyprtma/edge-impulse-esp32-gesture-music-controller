import os
import random
import socket
import threading
import time

from flask import Flask, request, jsonify
import pygame
from mutagen.mp3 import MP3


app = Flask(__name__)

MUSIC_FOLDER = os.getenv(
    "MUSIC_FOLDER",
    "./music"
)

music_files = []
current_track_index = -1
playback_thread = None
track_end_event = threading.Event()


try:
    pygame.mixer.init()
    print(
        "Pygame mixer initialized successfully."
    )
except Exception as e:
    print(
        f"Error initializing Pygame mixer: {e}"
    )


def load_music_files():
    global music_files

    music_files = []

    if not os.path.isdir(
        MUSIC_FOLDER
    ):
        print(
            f"Music folder '{MUSIC_FOLDER}' does not exist."
        )
        return

    for root, _, files in os.walk(
        MUSIC_FOLDER
    ):
        for file in files:
            if file.lower().endswith(
                ".mp3"
            ):
                music_files.append(
                    os.path.join(
                        root,
                        file
                    )
                )

    random.shuffle(
        music_files
    )

    print(
        f"Loaded {len(music_files)} MP3 files."
    )


def get_track_duration(
    file_path
):
    try:
        audio = MP3(
            file_path
        )

        return audio.info.length

    except Exception as e:
        print(
            f"Could not read duration: {e}"
        )

        return 0


def play_track_playback_thread():
    global current_track_index

    if not music_files:
        return

    track_end_event.clear()

    if not (
        0 <=
        current_track_index <
        len(music_files)
    ):
        current_track_index = 0

    try:
        file_path = music_files[
            current_track_index
        ]

        pygame.mixer.music.load(
            file_path
        )

        pygame.mixer.music.play()

        print(
            f"Now playing: {os.path.basename(file_path)}"
        )

        duration = get_track_duration(
            file_path
        )

        if duration > 0:
            print(
                f"Track duration: {int(duration)} seconds."
            )

        while (
            pygame.mixer.music.get_busy()
            and
            not track_end_event.is_set()
        ):
            time.sleep(
                0.1
            )

    except pygame.error as e:
        print(
            f"Playback error: {e}"
        )

    except Exception as e:
        print(
            f"Unexpected error: {e}"
        )

    finally:
        track_end_event.set()


def stop_current_playback():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

    track_end_event.set()


def start_playback_thread():
    global playback_thread

    stop_current_playback()

    if (
        playback_thread
        and
        playback_thread.is_alive()
    ):
        playback_thread.join(
            timeout=1
        )

    playback_thread = threading.Thread(
        target=play_track_playback_thread,
        daemon=True
    )

    playback_thread.start()


def next_track():
    global current_track_index

    if not music_files:
        return

    current_track_index = (
        current_track_index + 1
    ) % len(
        music_files
    )

    start_playback_thread()


def previous_track():
    global current_track_index

    if not music_files:
        return

    current_track_index = (
        current_track_index -
        1 +
        len(music_files)
    ) % len(
        music_files
    )

    start_playback_thread()


@app.route("/")
def index():
    return {
        "status": "running",
        "service": "gesture-music-controller"
    }


@app.route(
    "/gesture",
    methods=["POST"]
)
def handle_gesture():
    try:
        data = request.get_json(
            silent=True
        )

        if not data:
            return jsonify(
                {
                    "status": "error",
                    "message": "Invalid JSON"
                }
            ), 400

        gesture = data.get(
            "gesture"
        )

        if gesture == "next":
            next_track()

            return jsonify(
                {
                    "status": "success",
                    "message": "Next track played."
                }
            ), 200

        if gesture == "previous":
            previous_track()

            return jsonify(
                {
                    "status": "success",
                    "message": "Previous track played."
                }
            ), 200

        return jsonify(
            {
                "status": "error",
                "message": "Unknown gesture"
            }
        ), 400

    except Exception as e:
        return jsonify(
            {
                "status": "error",
                "message": str(e)
            }
        ), 500


def get_local_ip():
    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    )

    try:
        sock.connect(
            (
                "8.8.8.8",
                80
            )
        )

        return sock.getsockname()[0]

    except Exception:
        return "127.0.0.1"

    finally:
        sock.close()


if __name__ == "__main__":
    load_music_files()

    if music_files:
        current_track_index = 0
        start_playback_thread()

    host_ip = get_local_ip()

    print(
        f"Server: http://{host_ip}:5000"
    )

    print(
        f"Gesture endpoint: http://{host_ip}:5000/gesture"
    )

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )

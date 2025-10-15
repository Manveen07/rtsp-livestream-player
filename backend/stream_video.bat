@echo off
start "FFmpeg Video Stream" cmd /k C:\ffmpeg\bin\ffmpeg.exe -re -stream_loop -1 -i C:\Users\Manveen\Desktop\new_things_to_mess_araound\Livesitter\backend\test_10min.mp4 -c copy -f rtsp rtsp://localhost:8554/live

C:\ffmpeg\bin\ffmpeg.exe -re -stream_loop -1 -i "C:\Users\Manveen\Desktop\new_things_to_mess_araound\Livesitter\backend\test_10min.mp4" -c copy -f rtsp rtsp://localhost:8554/live

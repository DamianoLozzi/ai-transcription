#curl request to test the transcription service

curl -F "file=@resources/test_files/fileTest.wav" http://localhost:5000/transcribe
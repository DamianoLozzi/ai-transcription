#send resources/sample-1.mp3 to the server at localhost:5000
curl  -F "file=@resources/test.mp3" http://localhost:5000/transcribe
curl  -F "file=@resources/test.mp3" http://localhost:5000/generate
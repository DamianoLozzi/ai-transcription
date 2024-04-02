#curl request to test the transcription service

#Sends a POST request to the server containing the fileTest.wav file

curl -F "file=@resources/test_files/fileTest.wav" http://localhost:5000/transcribe
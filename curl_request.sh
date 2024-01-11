#send resources/sample-1.mp3 to the server at localhost:5000
curl  -F "file=@resources/test.mp3" http://localhost:5000/transcribe
curl  -F "file=@resources/test.mp3" http://localhost:5000/generate
#curl  -F "file=@resources/test.mp3" http://localhost:5000/summarize

#send text request to ai server at localhost:5000/text
curl -X POST -H "Content-Type: application/json" -d '{"text":"write a poem about cheap technology"}' http://localhost:5000/text

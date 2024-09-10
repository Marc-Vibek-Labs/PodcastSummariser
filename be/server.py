import logging
from flask_cors import CORS
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, jsonify
from rag_summariser import summarize_text
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)
CORS(app)

# Set up basic logging
logging.basicConfig(level=logging.DEBUG)

# Merges transcripts in parallel between start and end times
def merge_transcripts(transcripts, start, end):
    merged_text = []
    for transcript in transcripts:
        if start <= transcript['start'] < end:
            merged_text.append(transcript['text'])
    return ' '.join(merged_text)

@app.route('/transcript', methods=['GET'])
def get_transcript():
    video_id = request.args.get('video_id')
    start_time = float(request.args.get('start', 0))
    end_time = float(request.args.get('end', 0))

    if not video_id:
        return jsonify({"error": "Please provide a video_id"}), 400

    try:
        # Fetch transcript and log it
        transcripts = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Use multithreading to parallelize transcript merging
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(merge_transcripts, transcripts, start_time, end_time)]
            result = [future.result() for future in futures]

        logging.debug(f"Merged text: {result}")

        # Join the list into a single string before summarizing
        merged_text = ' '.join(result)

        # Summarize the merged transcript
        summary = summarize_text(merged_text)
        logging.debug(f"Generated summary: {summary}")
        print(summary)
        
        return jsonify({"summary": summary}), 200

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

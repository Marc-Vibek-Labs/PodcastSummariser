import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);
  const [videoId, setVideoId] = useState("");

  const pauseVideo = () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      chrome.scripting.executeScript({
        target: { tabId: tabs[0].id },
        func: () => {
          // This runs in the context of the YouTube tab
          const video = document.querySelector("video");
          if (video) {
            video.pause();
          }
        },
      });
    });
  };

  const fetchSummary = async () => {
    try {
      chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
        setLoading(true);
        const url = new URL(tabs[0].url);
        const videoId = url.searchParams.get("v");

        pauseVideo();

        const response = await fetch(
          `http://127.0.0.1:5000/transcript?video_id=${videoId}&start=0&end=1000`
        );
        const data = await response.json();
        setSummary(data.summary);
        setLoading(false);
      });
    } catch (error) {
      console.error("Error fetching summary:", error);
      setLoading(false);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>Podcast Summarizer</h1>
      <button className="fetch-button" onClick={fetchSummary}>
        Get Summary
      </button>

      {loading ? (
        <div className="loader"></div>
      ) : (
        summary && (
          <div className="summary">
            <h2>Summary:</h2>
            <pre>{summary}</pre>
          </div>
        )
      )}
    </div>
  );
}

export default App;

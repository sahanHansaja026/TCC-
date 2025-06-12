import { useState } from "react";
import axios from "axios";

function YouTubeExtractor() {
  const [url, setUrl] = useState("");
  const [videoData, setVideoData] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false); // <-- Loading state

  const handleExtract = async () => {
    setError("");
    setVideoData(null);
    if (!url) {
      setError("Please enter a YouTube video URL.");
      return;
    }

    setLoading(true); // Start loading
    try {
      const response = await axios.post("http://localhost:8000/extract", { url });
      setVideoData(response.data);
    } catch (err) {
      console.error("Error fetching video data:", err);
      setError("Failed to fetch video data. Please check the URL.");
    }
    setLoading(false); // End loading
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>YouTube Video Data Extractor</h1>
      <input
        type="text"
        placeholder="Enter YouTube video URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        style={{ width: "80%", padding: "0.5rem", fontSize: "1rem" }}
        disabled={loading}
      />
      <button
        onClick={handleExtract}
        style={{
          marginLeft: "1rem",
          padding: "0.5rem 1rem",
          fontSize: "1rem",
          cursor: loading ? "not-allowed" : "pointer",
          opacity: loading ? 0.6 : 1,
        }}
        disabled={loading}
      >
        {loading ? "Extracting..." : "Extract"}
      </button>

      {loading && (
        <p style={{ marginTop: "1rem", color: "#555" }}>Fetching video data...</p>
      )}

      {error && <p style={{ color: "red", marginTop: "1rem" }}>{error}</p>}

      {videoData && (
        <div style={{ marginTop: "2rem" }}>
          <img src={videoData.thumbnail_url} alt="thumbnail" width="320" />
          <h2>{videoData.title}</h2>
          <p><strong>Description:</strong> {videoData.description}</p>
          <p><strong>Author:</strong> {videoData.author}</p>
          <p><strong>Views:</strong> {videoData.views}</p>
          <p><strong>Duration:</strong> {videoData.duration}</p>
          <p><strong>Published:</strong> {videoData.publish_date}</p>
          <p><strong>transcript_text:</strong> {videoData.transcript_text}</p>
          <p><strong>transcript_available:</strong> {videoData.transcript}</p>
          <pre style={{ marginTop: "24rem", whiteSpace: "pre-wrap" }}>{videoData.summary}</pre>
          <p >{videoData.summary}</p>
        </div>
      )}
    </div>
  );
}

export default YouTubeExtractor;

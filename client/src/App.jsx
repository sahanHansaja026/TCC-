import { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [text, setText] = useState("");
  const [word_count, setWord_count] = useState("");
  const [summary, setSummary] = useState("");

  const handleUpload = async () => {
    if (!file) return alert("Please select a PDF file.");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://localhost:8000/extract-text/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setText(response.data.text);
      setWord_count(response.data.word_count);
      setSummary(response.data.summary);
    } catch (error) {
      console.error("Error uploading PDF:", error);
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>PDF Text Extractor</h1>
      <input type="file" accept="application/pdf" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload} style={{ marginLeft: "1rem" }}>Upload</button>
      <pre style={{ marginTop: "2rem", whiteSpace: "pre-wrap", fontWeight: "bold", fontSize: "25px" }}>total words :{word_count}</pre>
      <pre style={{ marginTop: "2rem", whiteSpace: "pre-wrap", fontWeight: "bold", fontSize: "25px" }}>summary :{summary}</pre>
      <pre style={{ marginTop: "2rem", whiteSpace: "pre-wrap" }}>{text}</pre>
     
    </div>
  );
}

export default App;

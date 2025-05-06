import React, { useState } from "react";
import axios from "axios";
import ResultResume from "./ResultResume";

const API_BASE_URL = "https://api-gateway-url/Prod"; // 🔁 Replace with your actual deployed API Gateway URL

function UploadResume() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [resultText, setResultText] = useState("");
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    setResumeFile(e.target.files[0]);
    setResultText("");
    setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResultText("");
    setError("");

    try {
      const formData = new FormData();
      formData.append("file", resumeFile);
      formData.append("job_description", jobDescription);

      // Step 1: Upload resume
      const uploadRes = await axios.post(`${API_BASE_URL}/upload`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      // Step 2: Generate improved resume using returned S3 key
      const genRes = await axios.post(`${API_BASE_URL}/generate`, {
        key: uploadRes.data.key,
      });

      setResultText(genRes.data.improved_resume || "No output received.");
    } catch (err) {
      console.error(err);
      setError("An error occurred while processing your resume.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-resume-container">
      <h2>Upload Resume + Job Description</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Resume (.txt):
          <input type="file" accept=".txt" onChange={handleFileChange} required />
        </label>
        <br />
        <label>
          Job Description:
          <textarea
            rows="6"
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            required
          />
        </label>
        <br />
        <button type="submit" disabled={loading}>
          {loading ? "Processing..." : "Generate Resume"}
        </button>
      </form>

      {error && <p className="error">{error}</p>}
      <ResultResume result={resultText} />
    </div>
  );
}

export default UploadResume;

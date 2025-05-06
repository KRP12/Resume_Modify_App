import React from "react";

function ResultResume({ result }) {
  if (!result) return null;

  return (
    <div className="result-resume">
      <h3>Improved Resume</h3>
      <pre>{result}</pre>
    </div>
  );
}

export default ResultResume;

import { useState, useEffect } from 'react'
import axios from 'axios'

function App() {
  const [files, setFiles] = useState([])
  const [previews, setPreviews] = useState([])
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    axios.get(`${import.meta.env.VITE_API_URL}/ping`)
      .then(res => console.log("✅ 서버 응답", res.data))
      .catch(err => console.error("❌ 서버 연결 실패", err))
  }, [])

  const handleFileChange = (e) => {
    const selectedFiles = [...e.target.files]
    setFiles(selectedFiles)
    setResults([])

    const previewUrls = selectedFiles.map((file) => URL.createObjectURL(file))
    setPreviews(previewUrls)
  }

  const handleUpload = async () => {
    const formData = new FormData()
    files.forEach(file => formData.append("files", file))

    setLoading(true)
    try {
      const res = await axios.post(`${import.meta.env.VITE_API_URL}/classify`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setResults(res.data.results)
    } catch (err) {
      console.error("❌ 업로드 실패:", err)
      alert("업로드 실패! 백엔드 서버 확인 필요")
    }
    setLoading(false)
  }

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>📸 AI 이미지 테마 분류기</h1>
      <input type="file" multiple onChange={handleFileChange} style={{ margin: '1rem 0' }} />

      {previews.length > 0 && (
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', marginBottom: '1rem' }}>
          {previews.map((src, idx) => (
            <img key={idx} src={src} alt="preview" style={{ width: '100px', height: '100px', objectFit: 'cover', borderRadius: '8px' }} />
          ))}
        </div>
      )}

      <button onClick={handleUpload} disabled={loading || files.length === 0}>
        {loading ? "🔄 분석 중..." : "🚀 분석 시작"}
      </button>

      {results.length > 0 && (
        <div style={{ marginTop: '2rem' }}>
          <h2>🎯 분석 결과</h2>
          <ul>
            {results.map((r, i) => (
              <li key={i}>📄 <strong>{r.filename}</strong> → {r.label} (신뢰도: {r.confidence})</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default App

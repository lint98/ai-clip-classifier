import { useState, useEffect } from 'react'
import axios from 'axios'
import { ReactSortable } from "react-sortablejs";  // 이미지 정렬용 라이브러리

function App() {
  const [images, setImages] = useState([])       // 이미지 배열: { id, file, preview }
  const [results, setResults] = useState([])     // 분류 결과
  const [loading, setLoading] = useState(false)  // 로딩 상태
  const [prompt, setPrompt] = useState("")       // 슬라이드쇼용 프롬프트 (추후 사용)

  // 서버 ping 테스트
  useEffect(() => {
    axios.get(`${import.meta.env.VITE_API_URL}/ping`)
      .then(res => console.log("✅ 서버 응답", res.data))
      .catch(err => console.error("❌ 서버 연결 실패", err))
  }, [])

  // 이미지 업로드 시 처리
  const handleFileChange = (e) => {
    const newFiles = [...e.target.files].map((file, idx) => ({
      id: `${file.name}-${Date.now()}-${idx}`,
      file,
      preview: URL.createObjectURL(file),
    }))
    setImages(prev => [...prev, ...newFiles])
    setResults([])
  }

  // 드래그 정렬된 순서 반영
  const handleSort = (order) => {
    const newOrder = order
    .map(id => images.find(img => img.id === id))
    .filter(Boolean); // undefined 제거
    setImages(newOrder)
  }

  // 분석 요청
  const handleUpload = async () => {
    const formData = new FormData()
    images.forEach(img => formData.append("files", img.file))

    setLoading(true)
    try {
      const res = await axios.post(`${import.meta.env.VITE_API_URL}/classify`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setResults(res.data.results)
    } catch (err) {
      alert("❌ 업로드 실패! 백엔드 서버를 확인하세요.")
      console.error(err)
    }
    setLoading(false)
  }

  // 슬라이드쇼 제작버튼함수
  const handleSlideshow = async () => {
    const formData = new FormData();
    images.forEach((img) => formData.append("files", img.file));
    formData.append("prompt", prompt);
  
    setLoading(true);
    try {
      const res = await axios.post(`${import.meta.env.VITE_API_URL}/generate-slideshow`, formData, {
        responseType: "blob",
      });
  
      const url = URL.createObjectURL(res.data);
      const a = document.createElement("a");
      a.href = url;
      a.download = "slideshow.mp4";
      a.click();
    } catch (err) {
      alert("❌ 영상 생성 실패!");
      console.error(err);
    }
    setLoading(false);
  };
  

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1 style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>📸 AI 이미지 슬라이드쇼 생성기</h1>

      <input type="file" multiple onChange={handleFileChange} style={{ margin: '1rem 0' }} />

      {/* 썸네일 정렬 가능 영역 */}
      {images.length > 0 && (
        <ReactSortable
        list={images}
        setList={setImages}
        style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', marginBottom: '1rem' }}
      >
        {images.map((img) => (
          <div key={img.id}>
            <img
              src={img.preview}
              alt="preview"
              style={{
                width: '100px',
                height: '100px',
                objectFit: 'cover',
                borderRadius: '8px',
              }}
            />
          </div>
        ))}
      </ReactSortable>
      
      )}

      {/* 프롬프트 입력 (슬라이드쇼용) */}
      <input
        type="text"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="예: 감성적인 분위기로 영상 만들어줘"
        style={{ margin: '1rem 0', padding: '0.5rem', width: '100%' }}
      />

      {/* 분석 버튼 */}
      <button
        onClick={handleUpload}
        disabled={loading || images.length === 0}
        style={{ padding: '0.5rem 1rem', backgroundColor: '#3b82f6', color: 'white', borderRadius: '0.5rem' }}
      >
        {loading ? '🔄 분석 중...' : '🚀 분석 시작'}
      </button>

      {/* 영상 생성버튼 */}
      <button
        onClick={handleSlideshow}
        disabled={loading || images.length === 0}
        style={{ marginTop: '1rem', padding: '0.5rem 1rem', backgroundColor: '#10b981', color: 'white', borderRadius: '0.5rem' }}
      >
        {loading ? "🎞️ 영상 생성 중..." : "🎬 영상 만들기"}
      </button>


      {/* 분석 결과 출력 */}
      {results.length > 0 && (
        <div style={{ marginTop: '2rem' }}>
          <h2 style={{ fontSize: '1.2rem', fontWeight: 'bold' }}>🎯 분석 결과:</h2>
          <ul style={{ marginTop: '1rem' }}>
            {results.map((r, i) => (
              <li key={i} style={{ marginBottom: '0.5rem' }}>
                📄 <strong>{r.filename}</strong> → <span style={{ color: '#16a34a' }}>{r.label}</span> (신뢰도: {r.confidence})
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default App

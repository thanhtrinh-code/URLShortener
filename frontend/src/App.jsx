import { BrowserRouter, Routes, Route, Link } from "react-router-dom"


function App() {

  return (
    <BrowserRouter>
      <Routes>

        <Route path="/" element={<Home/>}/>
        <Route path="/:code" element={<Redirect/>}/>
      </Routes>
    </BrowserRouter>
  )
}

export default App

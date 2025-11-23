import './App.css'
import Login from './pages/Login'
import AppHeader from './components/header';
import VideoFeed from './pages/VideoFeed';
import DeviceConfig from './pages/DeviceConfig';
import { BrowserRouter as Router, Routes, Route} from 'react-router-dom';

function App() {
  return (
    <Router>
      <div className="flex flex-col h-screen w-screen">
        <AppHeader />
        <div className="flex-1 pt-15">
          <Routes>
            <Route path="/" element={<VideoFeed />} />
            <Route path="/config" element={<DeviceConfig />} />
            <Route path="/login" element={<Login />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}


export default App

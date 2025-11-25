import './App.css'
import Login from './pages/Login'
import AppHeader from './components/header';
import VideoFeed from './pages/VideoFeed';
import DeviceConfig from './pages/DeviceConfig';
import { BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import { useEffect } from 'react';
import { apiFetchCoordinator } from './util/apiFetch';


const dispatchAuthEvent = () => {
  window.dispatchEvent(new Event("local-storage-changed"));
};

const originalSetItem = localStorage.setItem;
localStorage.setItem = function (key, value) {
  originalSetItem.apply(this, arguments);
  dispatchAuthEvent();
};

const originalRemoveItem = localStorage.removeItem;
localStorage.removeItem = function (key) {
  originalRemoveItem.apply(this, arguments);
  dispatchAuthEvent();
};

const originalClear = localStorage.clear;
localStorage.clear = function () {
  originalClear.apply(this, arguments);
  dispatchAuthEvent();
};

/* ---------------------------------------------------------------------- */

function App() {

  const syncAuth = async () => {
    const response = await apiFetchCoordinator("/api/user/sync");
    if (!response.ok) {
      localStorage.clear();
      return;
    }

    const data = await response.json();
    if (!data.user || !data.token) {
      console.log("coordinator not logged in");
      localStorage.clear();
    } else {
      localStorage.setItem("user", data.user);
      localStorage.setItem("token", data.token);
    }
  };

  useEffect(() => {
    syncAuth();
  }, []);

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

export default App;

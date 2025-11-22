import './App.css'

import Login from './pages/Login.jsx'
import { BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import AppHeader from './components/AppHeader';

function App() {

  return (
    <Router>
      <div className="flex flex-col h-screen w-screen">
        <AppHeader />
        <div className="flex-1 pt-15">
          <Routes>
            <Route path="/login" element={<Login />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { RxHamburgerMenu } from "react-icons/rx";
import Sidebar from "./Sidebar";

export default function AppHeader() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    setUsername(localStorage.getItem('user'));
  }, []);

  return (
    <div className="p-4 bg-hvs-yellow flex justify-between w-full fixed top-0 left-0 z-50">
      <button onClick={() => navigate('/')}>
        <p className="hvs-text">HiveSight</p>
      </button>

      <div>
        <button 
          className="flex items-center gap-2 pt-1"
          onClick={() => setSidebarOpen(true)}>
        {Boolean(localStorage.getItem('token')) && (
        <p className="hvs-text">Welcome, {username}</p>

        )}
          <RxHamburgerMenu color="var(--color-hvs-white)" size={20} />
        </button>
      </div>
      
      {/* Sidebar rendered at root level */}
      <Sidebar open={sidebarOpen} setOpen={setSidebarOpen} />
    </div>
  );
}

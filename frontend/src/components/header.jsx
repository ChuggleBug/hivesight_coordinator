import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { RxHamburgerMenu } from "react-icons/rx";
import Sidebar from "./Sidebar";

export default function AppHeader() {
  const navigate = useNavigate();
  const [username, setUsername] = useState(localStorage.getItem("user"));
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    const syncLocalState = () => {
      setUsername(localStorage.getItem("user"));
      setToken(localStorage.getItem("token"));
    };

    // Listen for our custom event
    window.addEventListener("local-storage-changed", syncLocalState);

    // Run once initially
    syncLocalState();

    return () => {
      window.removeEventListener("local-storage-changed", syncLocalState);
    };
  }, []);

  return (
    <div className="p-4 bg-hvs-yellow flex justify-between w-full fixed top-0 left-0 z-50">
      <button onClick={() => navigate('/')}>
        <p className="hvs-text">HiveSight</p>
      </button>

      <div className="flex items-center gap-2 pt-1">
        {token ? (
          <p className="hvs-text cursor-default">Welcome, {username}</p>
        ) : (
          <p className="hvs-text cursor-default">Not logged in</p>
        )}
        <button onClick={() => setSidebarOpen(true)}>
          <RxHamburgerMenu color="var(--color-hvs-white)" size={20} />
        </button>
      </div>

      <Sidebar open={sidebarOpen} setOpen={setSidebarOpen} />
    </div>
  );
}

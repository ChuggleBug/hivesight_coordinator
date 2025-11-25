import { X } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { apiFetchCoordinator } from "../util/apiFetch";

export default function Sidebar({ open, setOpen }) {
  const navigate = useNavigate();

  const handleLogout = async () => {
    const response = apiFetchCoordinator("/api/user/logout", {
      "method": "POST"
    });
    localStorage.clear();
    navigate('/');
    window.location.reload();
  };

  return (
    <>
      {/* Sidebar */}
      <div
        className={`fixed top-0 left-0 h-full bg-hvs-black-dark text-white w-64 transform 
          ${open ? "translate-x-0" : "-translate-x-full"} 
        transition-transform duration-300 ease-in-out z-30`}
      >
        <div className="flex items-center justify-between p-4 border-b border-gray-700">
          <h1 className="text-xl font-semibold">Account Menu</h1>
          <button onClick={() => setOpen(false)}>
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Menu Selections */}
        <div className="flex flex-col py-2 space-y-3 p-4">

          <button
            className="w-full bg-hvs-black hover:bg-hvs-black-dark hover:shadow-2xl py-2 rounded cursor-pointer"
            onClick={() => {navigate('/'); setOpen(false);}}
          >
            <p className="hvs-text">Video Feed</p>
          </button>

          <button
            className="w-full bg-hvs-black hover:bg-hvs-black-dark hover:shadow-2xl py-2 rounded cursor-pointer"
            onClick={() => {navigate('/config'); setOpen(false);}}
          >
            <p className="hvs-text">Configurations</p>
          </button>

          {/* Login and Logout */}
          {Boolean(localStorage.getItem('token')) ?
            <button
              className="w-full bg-hvs-black hover:bg-hvs-black-dark hover:shadow-2xl py-2 rounded cursor-pointer"
              onClick={handleLogout}
            >
              <p className="hvs-text">Logout</p>
            </button>
            :
            <button
              className="w-full bg-hvs-black hover:bg-hvs-black-dark hover:shadow-2xl py-2 rounded cursor-pointer"
              onClick={() => {navigate('/login'); setOpen(false);}}
            >
              <p className="hvs-text">Login</p>
            </button>
          }

        </div>
      </div>

      {/* Overlay */}
      {open && (
        <div
          className="fixed inset-0 bg-black/50 z-20"
          onClick={() => setOpen(false)}
        />
      )}
    </>
  );
}

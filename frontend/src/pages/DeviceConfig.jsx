import { useEffect, useState } from "react";
import { apiFetchCoordinator } from "../util/apiFetch";
import { IoMdArrowDropdown } from "react-icons/io";

export default function DeviceConfig() {
    const [sensors, setSensors] = useState([]);
    const [cameras, setCameras] = useState([]);
    const [deviceAssoc, setDeviceAssoc] = useState({});
    const [originalAssoc, setOriginalAssoc] = useState({}); // Backup of last saved state
    const [loading, setLoading] = useState(true); // Loading state

    // Fetch sensors, cameras, and device associations
    const getDeviceMappings = async () => {
        setLoading(true); // Start loading
        try {
            const assocRes = await apiFetchCoordinator("/api/user/config/assoc");
            if (assocRes.ok) {
                const assocData = await assocRes.json();
                setDeviceAssoc(assocData);
                setOriginalAssoc(assocData); // Save initial state for reset
            }

            const deviceRes = await apiFetchCoordinator("/api/user/devices");
            if (deviceRes.ok) {
                const data = await deviceRes.json();
                setSensors(data.sensors);
                setCameras(data.cameras);
            }
        } catch (err) {
            console.error("Error fetching device mappings:", err);
        } finally {
            setLoading(false); // Stop loading
        }
    };

    // Toggle camera association for a sensor
    const toggleCamera = (sensor, camera) => {
        setDeviceAssoc(prev => {
            const current = prev[sensor] || [];
            const updated = current.includes(camera)
                ? current.filter(c => c !== camera)
                : [...current, camera];
            return { ...prev, [sensor]: updated };
        });
    };

    // Save function
    const handleSave = async () => {
        const response = await apiFetchCoordinator("/api/user/config/assoc", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(deviceAssoc),
        });

        if (response.ok) {
            alert("Associations saved successfully!");
            setOriginalAssoc(deviceAssoc); // Update backup state
        } else {
            alert("Failed to save associations.");
        }
    };

    // Reset function
    const handleReset = () => {
        setDeviceAssoc(originalAssoc);
    };

    const DeviceAssoc = () => (
        <div className="md:px-20">
            {loading ? (
                <div className="flex flex-col w-full hvs-text text-center my-2 p-5 bg-hvs-black-dark rounded-2xl">
                    <h1>Loading...</h1>
                </div>
            ) : sensors.length === 0 ? (
                <div className="flex flex-col w-full hvs-text text-center my-2 p-5 bg-hvs-black-dark rounded-2xl">
                    <h1>No Sensors</h1>
                </div>
            ) : (
                sensors.map(sensor => (
                    <div
                        key={`sensor-${sensor}`}
                        className="flex flex-col w-full hvs-text text-left my-2 p-5 bg-hvs-black-dark rounded-2xl"
                    >
                        <details open>
                            <summary className="flex flex-col items-start justify-between cursor-pointer select-none list-none">
                                <div className="flex w-full justify-between items-center">
                                    <h1>{sensor}</h1>
                                    <IoMdArrowDropdown size={36} />
                                </div>
                                <hr className="border-white border my-2 w-full" />
                            </summary>

                            <div className="mt-2">
                                {cameras.map(camera => (
                                    <label
                                        key={camera}
                                        className="block py-1 px-3 ml-1 rounded hover:bg-black"
                                    >
                                        <input
                                            type="checkbox"
                                            checked={deviceAssoc[sensor]?.includes(camera) || false}
                                            onChange={() => toggleCamera(sensor, camera)}
                                        />
                                        <span className="ml-2 hvs-text">{camera}</span>
                                    </label>
                                ))}
                            </div>
                        </details>
                    </div>
                ))
            )}
        </div>
    );

    useEffect(() => {
        getDeviceMappings();
    }, []);

    return (
        <div className="flex flex-col items-center h-full justify-center py-5 px-5 md:px-40 gap-5">
            <div className="w-full p-5 md:p-10 rounded-2xl bg-hvs-yellow">
                <DeviceAssoc />
            </div>
            <div className="flex justify-between bg-hvs-yellow p-5 px-5 md:px-15 w-full rounded-2xl">
                <button className="hvs_btn hvs-text" onClick={handleReset}>
                    Reset
                </button>
                <button className="hvs_btn hvs-text" onClick={handleSave}>
                    Save
                </button>
            </div>
        </div>
    );
}

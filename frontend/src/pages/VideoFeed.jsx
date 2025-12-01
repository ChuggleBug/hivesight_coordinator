import { useEffect, useState } from "react";
import { apiFetchCoordinator } from "../util/apiFetch";
import { MdArrowLeft, MdArrowRight } from "react-icons/md";


export default function VideoFeed() {
    const [cameraList, setCameraList] = useState([]);
    const [cameraIndex, setCameraIndex] = useState(-1); // Invalid for now

    const fetchCameraList = async () => {
        const response = await apiFetchCoordinator("/api/user/devices");

        if (!response.ok) {
            console.log("Issue fetching devices");
            return;
        }

        const data = await response.json();
        console.log(data.cameras)
        setCameraList(data.cameras);
    };

    const updateVideoFeed = async () => {
        // console.log(cameraList[cameraIndex]);
        
    };

    useEffect(() => {
        fetchCameraList();
    }, []);

    useEffect(() => {
        if (cameraIndex !== -1) {
            updateVideoFeed();
        }
    }, [cameraIndex]);


    return (
        <div className="flex flex-col items-center h-full">
            <div className="bg-hvs-yellow px-20 py-5 rounded-2xl mt-10">
                <h1>Live Video Feed</h1>
                <hr className="border-white border my-2 w-full" />
                {/* Current Camera Selector */}
                <div className="flex justify-between items-center bg-hvs-black rounded-2xl">
                    <MdArrowLeft
                        size={36} color="var(--color-hvs-white)"
                        onClick={() => {
                            setCameraIndex(prev => {
                                const next = prev <= 0 ? cameraList.length - 1 : prev - 1;
                                return next;
                            });
                        }}

                    />
                    <p className="hvs-text pb-0.5 select-none">
                        {cameraIndex === -1 ? "None" : cameraList[cameraIndex]}
                    </p>
                    <MdArrowRight
                        size={36} color="var(--color-hvs-white)"
                        onClick={() => {
                            setCameraIndex((prev) => {
                                const next = prev >= cameraList.length - 1 ? 0 : prev + 1;
                                return next;
                            });
                        }}
                    />
                </div>

            </div>

            <div>

            </div>

            
        </div>
    );
}

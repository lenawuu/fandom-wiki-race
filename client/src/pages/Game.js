import GameNav from "../components/GameNav";
import { useState, useRef, useEffect } from "react";

function Game() {
  const iFrameRef = useRef(null);
  const [currentSrc, setCurrentSrc] = useState("");
  const [numClicks, setNumClicks] = useState(0);

  const goal = {
    start: {
      name: "Leaves",
      url: "https://minecraft.fandom.com/wiki/Leaves",
    },
    end: {
      name: "Bone Meal",
      url: "https://minecraft.fandom.com/wiki/Bone_Meal",
    },
  };

  useEffect(() => {
    if (iFrameRef.current) {
      console.log(iFrameRef.current.getAttribute("src"));
    }
  }, []);

  const handleLoad = () => {
    if (iFrameRef.current) {
      const currentUrl = iFrameRef.current.contentWindow.location.href;
      setCurrentSrc(currentUrl);
      console.log("Iframe src changed to:", currentUrl);
    }
  };

  return (
    <div class="w-screen h-screen">
      <GameNav goal={goal} numClicks={numClicks} />
      <iframe
        ref={iFrameRef}
        src="https://minecraft.fandom.com/wiki/Block"
        onLoad={handleLoad}
        class="w-full h-full"
      ></iframe>
      <p>current: {currentSrc}</p>
    </div>
  );
}

export default Game;

import GameNav from "../components/GameNav";
import { useState, useRef, useEffect } from "react";
import axios from "axios";

function Game() {
  const [isLoading, setIsLoading] = useState(true);
  const [currentSrc, setCurrentSrc] = useState("");
  const [numClicks, setNumClicks] = useState(0);
  const [html, setHtml] = useState(null);
  const [history, setHistory] = useState([]);
  const [urlIndex, setUrlIndex] = useState(0);
  const [curURL, setCurURL] = useState("");

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

  //TODO: Implement page cache
  const fetchClean = async (url) => {
    try {
      setIsLoading(true);
      const res = await axios.post("http://localhost:8080/clean", {
        url: url,
      });
      setHtml(res.data);
    } catch (error) {
      console.error("Error cleaning html:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLinkClick = (event) => {
    event.preventDefault();

    const href = event.target.href;
    const url =
      "https://minecraft.fandom.com/" +
      href.split("://")[1].split("/").slice(1).join("/");

    setHistory((prev) => [...prev, url]);
    setUrlIndex(urlIndex + 1);
  };

  // on Mount
  useEffect(() => {
    setHistory([goal.start.url]);
    fetchClean(goal.start.url);
  }, []);

  useEffect(() => {
    if (urlIndex < history.length) {
      fetchClean(history[urlIndex]); // Use the current URL from history directly
    }
  }, [urlIndex, history]);

  return (
    <div class="w-screen h-screen">
      <GameNav goal={goal} numClicks={numClicks} />
      <div>
        {isLoading ? (
          "loading"
        ) : (
          <div
            dangerouslySetInnerHTML={{ __html: html }}
            onClick={handleLinkClick}
          />
        )}
      </div>
    </div>
  );
}

export default Game;

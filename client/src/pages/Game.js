import GameNav from "../components/GameNav";
import { useState, useRef, useEffect } from "react";
import axios from "axios";

function Game() {
  const [isLoading, setIsLoading] = useState(true);
  const [currentSrc, setCurrentSrc] = useState("");
  const [numClicks, setNumClicks] = useState(0);
  const [html, setHtml] = useState(null);
  const [history, setHistory] = useState([]);
  const [curIndex, setCurIndex] = useState(0);
  const [curURL, setCurURL] = useState("");

  const goal = {
    start: {
      title: "Leaves",
      url: "https://minecraft.fandom.com/wiki/Leaves",
    },
    end: {
      title: "Bone Meal",
      url: "https://minecraft.fandom.com/wiki/Bone_Meal",
    },
  };

  //TODO: Implement page cache, load images, wait til css loads timeout
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
    if (href) {
      const url =
        "https://minecraft.fandom.com/" +
        href.split("://")[1].split("/").slice(1).join("/");

      setHistory((prev) => [...prev, { title: titleFromURL(url), url: url }]);
      setCurIndex(curIndex + 1);
    }
  };

  const titleFromURL = (url) => {
    const title = url.substring(url.lastIndexOf("/") + 1).replace(/_/g, " ");

    const formattedTitle = title
      .split(" ")
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");

    return formattedTitle;
  };

  // on Mount
  useEffect(() => {
    setHistory([{ title: titleFromURL(goal.start.url), url: goal.start.url }]);
    fetchClean(goal.start.url);
    setCurURL(goal.start.url);
  }, []);

  useEffect(() => {
    if (curIndex < history.length) {
      const url = history[curIndex].url;
      fetchClean(url);
      setCurURL(url);
    }
  }, [curIndex, history]);

  useEffect(() => {
    if (curURL.toUpperCase() === goal.end.url.toUpperCase()) {
      alert("you won!");
    }
  }, [curURL]);

  return (
    <div class="w-screen h-screen flex flex-col">
      <GameNav goal={goal} numClicks={numClicks} />
      <div class="bg-slate-500 flex-1 overflow-hidden py-2 px-4">
        <div class="h-full w-full overflow-y-auto">
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
      <div class="bg-white w-full justify-start">
        <div class="flex flex-row">
          {history.slice(0, curIndex + 1).map((item, i) => (
            <div key={i}>
              {item.title}
              <div>
                {i < curIndex + 1 ? (
                  <span> ➔ </span> // Render arrow if not the last item
                ) : null}
              </div>
            </div> // Use parentheses to implicitly return the JSX
          ))}
        </div>
      </div>
    </div>
  );
}

export default Game;

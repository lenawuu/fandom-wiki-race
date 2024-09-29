import GameNav from "../components/GameNav";
import { useState, useRef, useEffect } from "react";
import axios from "axios";
import { Button } from "@headlessui/react";
import winGif from "../assets/mariokartwin.gif";
import slayGif from "../assets/slaygif.gif";

function Game() {
  const [isLoading, setIsLoading] = useState(true);
  const [numClicks, setNumClicks] = useState(0);
  const [html, setHtml] = useState(null);
  const [history, setHistory] = useState([]);
  const [curIndex, setCurIndex] = useState(0);
  const [curURL, setCurURL] = useState("");
  const [showModal, setShowModal] = useState(false);

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

  // FIXME: handle span case ...
  const handleLinkClick = (event) => {
    event.preventDefault();

    const href = event.target.href;
    console.log(href);

    if (!href) {
      console.log(event.currentTarget);
    }
    if (href) {
      const url =
        "https://minecraft.fandom.com/" +
        href.split("://")[1].split("/").slice(1).join("/");

      setHistory((prev) => [...prev, { title: titleFromURL(url), url: url }]);
      setCurIndex(curIndex + 1);
      setNumClicks(numClicks + 1);
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

  const handleHistoryNav = (index) => {
    if (curIndex > 0 && curIndex < history.length) {
      setCurIndex(index);
      setNumClicks(numClicks + 1);
    }
  };

  const getPath = () => {
    let result = "";
    history.slice(0, curIndex + 1).forEach((val, i) => {
      result += val.title;
      if (i < curIndex) result += " ➔ ";
    });

    return result;
  };

  const resetGame = () => {
    const dialog = document.getElementById("winModal");

    // Close the modal if it's open
    if (dialog.open) {
      dialog.close();
    }

    setHistory([{ title: titleFromURL(goal.start.url), url: goal.start.url }]);
    fetchClean(goal.start.url);
    setCurURL(goal.start.url);

    setShowModal(false);
    setNumClicks(0);
    setCurIndex(0);
  };

  // on Mount
  useEffect(() => {
    resetGame();
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
      setShowModal(true);
    }
  }, [curURL]);

  useEffect(() => {
    if (showModal) {
      const dialog = document.getElementById("winModal");
      dialog.showModal();
    }
  }, [showModal]);

  return (
    <div class="w-screen h-screen flex flex-col bg-neutral">
      <GameNav
        goal={goal}
        numClicks={numClicks}
        handleNav={handleHistoryNav}
        curIndex={curIndex}
      />
      <div class="flex-1 overflow-hidden py-2 px-4">
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
      <dialog id="winModal" className="modal">
        <div class="modal-box flex flex-col gap-4 justify-center">
          <p class="font-extrabold text-5xl text-center">You won!</p>
          <div class="flex flex-row gap-4 h-1/4">
            <img class="w-full" src={winGif} />
            <img src={slayGif} />
          </div>
          <div>
            <p class="text-center text-lg">
              You got to {goal.end.title} in {numClicks} clicks!
            </p>
            <p class="text-center text-lg">Your path: {getPath()}</p>
          </div>
          <div class="justify-between flex w-full">
            <button
              class="btn btn-primary w-56"
              onClick={() => {
                resetGame();
              }}
            >
              Find another way!
            </button>
            <button class="btn btn-accent w-56">New game</button>
          </div>
        </div>
      </dialog>
      <div className="bg-base-100 w-full justify-start h-10 items-center px-5 flex flex-row gap-2">
        {history.slice(0, curIndex + 1).map((item, i) => (
          <div key={i} className="flex flex-row gap-2">
            <Button onClick={() => handleHistoryNav(i)}>{item.title}</Button>
            <div>
              {i < curIndex ? (
                <span> ➔ </span> // Render arrow if not the last item
              ) : null}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Game;

import GameNav from "../components/GameNav";
import { useState, useEffect, useRef } from "react";
import axios from "axios";
import winGif from "../assets/mariokartwin.gif";
import slayGif from "../assets/slaygif.gif";

function Game() {
  const [isLoading, setIsLoading] = useState(true);
  const [numClicks, setNumClicks] = useState(0);
  const [html, setHtml] = useState(null);
  const [history, setHistory] = useState([]);
  const [curIndex, setCurIndex] = useState(0);
  const [curURL, setCurURL] = useState("");
  const [showWinModal, setShowWinModal] = useState(false);
  const [showLoseModal, setShowLoseModal] = useState(false);
  const [gameData, setGameData] = useState({
    name: "Mario Kart",
    src: "https://assets.nintendo.com/image/upload/ar_16:9,b_auto:border,c_lpad/b_white/f_auto/q_auto/dpr_1.5/c_scale,w_400/ncom/software/switch/70070000013723/78683d87f12356c571e4541b2ef649e3bd608285139704087c552171f715e399",
    string: "mariokart",
    stem: "https://mariokart.fandom.com/",
    goal: {
      start: {
        title: "Spiny Shell",
        url: "https://mariokart.fandom.com/wiki/Spiny_Shell",
      },
      end: {
        title: "Battle Mode",
        url: "https://mariokart.fandom.com/wiki/Battle_Mode",
      },
      path: ["Spiny Shell", "Banana", "Battle Mode"],
    },
  });

  const htmlRef = useRef(null);

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

    if (!href) {
      console.log(event.currentTarget);
    }
    if (href) {
      const url =
        gameData.stem + href.split("://")[1].split("/").slice(1).join("/");

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
    const winDialog = document.getElementById("winModal");

    // Close the modal if it's open
    if (winDialog.open) {
      winDialog.close();
    } else {
      const loseDialog = document.getElementById("loseModal");
      if (loseDialog.open) {
        loseDialog.close();
      }
    }

    const goal = gameData.goal;

    if (gameData.goal) {
      // Check if gameData.goal exists
      setHistory([
        {
          title: gameData.goal.start.name,
          url: gameData.goal.start.url,
        },
      ]);
      fetchClean(gameData.goal.start.url);
      setCurURL(gameData.goal.start.url);
    }

    setShowWinModal(false);
    setShowLoseModal(false);
    setNumClicks(0);
    setCurIndex(0);
  };

  const handleGiveUp = () => {
    const dialog = document.getElementById("loseModal");
    dialog.showModal();
  };

  // on Mount
  useEffect(() => {
    const storedData = localStorage.getItem("game");
    if (storedData) {
      const parsedData = JSON.parse(storedData); // Parse the JSON string
      setGameData(parsedData); // Set the parsed object
      console.log(gameData.goal.end);
    }
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
    if (curURL.toUpperCase() === gameData.goal.end.url.toUpperCase()) {
      setShowWinModal(true);
    }
  }, [curURL]);

  useEffect(() => {
    if (showWinModal) {
      const dialog = document.getElementById("winModal");
      dialog.showModal();
    }
  }, [showWinModal]);

  useEffect(() => {
    if (html) {
      htmlRef.current.innerHTML = html; // Set the inner HTML
    }
  }, [html]);

  return (
    <div class="w-screen h-screen flex flex-col bg-neutral">
      <GameNav
        goal={gameData.goal}
        numClicks={numClicks}
        handleNav={handleHistoryNav}
        curIndex={curIndex}
      />
      <div class="flex-1 overflow-hidden py-2 px-4">
        <div class="h-full w-full overflow-y-auto">
          {isLoading ? (
            "loading"
          ) : (
            <div ref={htmlRef} onClick={handleLinkClick} />
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
              You got to {gameData.goal.end.name} in {numClicks} clicks!
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
            <a class="btn btn-accent w-56" href="/">
              New game
            </a>
          </div>
        </div>
      </dialog>
      <dialog id="loseModal">
        <div class="modal-box flex flex-col gap-4 justify-center">
          <p class="text-2xl text-center font-bold">
            Aw man, you were so close!
          </p>
          <img src="https://i.pinimg.com/originals/55/41/31/55413151a0cb5b5c0f1eba2f714f1ebd.gif"></img>
          <p class="text-center text-xl">
            Here is a path you could have taken:{" "}
            {gameData.goal.path.map((item, i) => (
              <div key={i} className="flex flex-row">
                <p>{item.name}</p>
                <div>
                  {i < gameData.goal.path.length ? (
                    <span> ➔ </span> // Render arrow if not the last item
                  ) : null}
                </div>
              </div>
            ))}
          </p>
          <a class="btn btn-primary" href="/">
            New game
          </a>
        </div>
      </dialog>
      <div className="bg-base-100 w-full justify-between h-10 items-center px-5 py-4 flex flex-row gap-2">
        <div class="flex flex-row gap-2">
          {history.slice(0, curIndex + 1).map((item, i) => (
            <div key={i} className="flex flex-row gap-2">
              <button onClick={() => handleHistoryNav(i)}>{item.title}</button>
              <div>
                {i < curIndex ? (
                  <span> ➔ </span> // Render arrow if not the last item
                ) : null}
              </div>
            </div>
          ))}
        </div>

        <button class="hover:underline" onClick={() => handleGiveUp()}>
          Give up
        </button>
      </div>
    </div>
  );
}

export default Game;

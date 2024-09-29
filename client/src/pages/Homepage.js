import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function Homepage() {
  const toggleDemo = true;

  const [selectedFandom, setSelectedFandom] = useState(fandoms[0]);
  const navigate = useNavigate();

  const handleSlideChange = (name) => {
    const fandom = fandoms.find((f) => f.name === name);
    setSelectedFandom(fandom);
  };

  const fetchGame = async () => {
    if (!toggleDemo) {
      try {
        let path = selectedFandom.stem.replace(/^https?:\/\//, "");
        path = path.slice(0, -1);
        const response = await axios.get(
          `http://localhost:5051/start-round?domain=${path}`
        );
        const game = { ...selectedFandom, goal: response.data };
        // const response = { data: selectedFandom };
        localStorage.setItem("game", JSON.stringify(game));
        navigate("/game");
      } catch (error) {}
    } else {
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-base-100 px-8 md:px-20">
      <div className="w-full max-w-[500px] flex flex-col gap-0 items-center mb-10">
        <img
          className="w-3/4 h-auto mb-4"
          src="https://upload.wikimedia.org/wikipedia/commons/c/ce/Fandom.svg"
          alt="Fandom Logo"
        />
        <p className="text-center text-6xl font-bold italic text-primary">
          Wikirace
        </p>
      </div>
      <h1 className="text-center w-full font-bold text-3xl mb-6 text-primary">
        Choose Your Fandom!
      </h1>

      <div className="carousel w-full max-w-3xl">
        {fandoms.map((val, index) => (
          <div
            key={index}
            id={`slide${index}`}
            className="carousel-item relative w-full"
          >
            <img
              src={val.src}
              className="w-full h-64 object-cover rounded-lg shadow-lg"
              alt={`Slide ${index}`}
            />
            <div className="absolute left-5 right-5 top-1/2 flex -translate-y-1/2 transform justify-between">
              <a
                href={`#slide${index > 0 ? index - 1 : fandoms.length - 1}`}
                className="btn btn-circle bg-blue-500 text-white hover:bg-blue-600 transition"
                onClick={() =>
                  handleSlideChange(
                    fandoms[index > 0 ? index - 1 : fandoms.length - 1].name
                  )
                }
              >
                ❮
              </a>
              <a
                href={`#slide${(index + 1) % fandoms.length}`}
                className="btn btn-circle bg-blue-500 text-white hover:bg-blue-600 transition"
                onClick={() =>
                  handleSlideChange(fandoms[(index + 1) % fandoms.length].name)
                }
              >
                ❯
              </a>
            </div>
            <div className="absolute bottom-5 left-5 right-5 text-white text-lg font-bold bg-black bg-opacity-50 p-2 rounded-md text-center">
              {val.name} {/* Assuming val.name contains the image name */}
            </div>
          </div>
        ))}
      </div>
      <button
        class="mt-6 btn-lg w-1/3 btn btn-primary"
        onClick={() => fetchGame()}
      >
        Start game
      </button>
    </div>
  );
}

export default Homepage;

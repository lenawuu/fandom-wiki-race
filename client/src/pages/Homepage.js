import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function Homepage() {
  const fandoms = [
    {
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
      },
    },
    {
      name: "F-Zero",
      src: "https://www.nintendo.com/eu/media/images/10_share_images/games_15/super_nintendo_5/H2x1_SNES_FZero.jpg",
      string: "https://fzero.fandom.com/",
      goal: {
        start: {
          title: "Captain Falcon",
          url: "https://fzero.fandom.com/wiki/Captain_Falcon",
        },
        end: {
          title: "Zoda",
          url: "https://fzero.fandom.com/wiki/Zoda",
        },
      },
    },
    {
      name: "Burnout",
      src: "https://assetsio.gnwcdn.com/bop08.jpg?width=1200&height=1200&fit=bounds&quality=70&format=jpg&auto=webp",
      string: "burnout",
      stem: "https://burnout.fandom.com/",
      goal: {
        start: {
          title: "Leaves",
          url: "https://minecraft.fandom.com/wiki/Leaves",
        },
        end: {
          title: "Bone Meal",
          url: "https://minecraft.fandom.com/wiki/Bone_Meal",
        },
      },
    },
    {
      name: "Need For Speed",
      src: "https://media.contentapi.ea.com/content/dam/need-for-speed/images/2017/06/nfspgenkeyartrgbhorz-16x9.jpg.adapt.crop191x100.1200w.jpg",
      string: "nfs",
      stem: "https://nfs.fandom.com/",
      goal: {
        start: {
          title: "Leaves",
          url: "https://minecraft.fandom.com/wiki/Leaves",
        },
        end: {
          title: "Bone Meal",
          url: "https://minecraft.fandom.com/wiki/Bone_Meal",
        },
      },
    },
  ];

  const [selectedFandom, setSelectedFandom] = useState(fandoms[0]);
  const navigate = useNavigate();

  const handleSlideChange = (name) => {
    const fandom = fandoms.find((f) => f.name === name);
    setSelectedFandom(fandom);
  };

  const fetchGame = async () => {
    try {
      // const response = await axios.get(`/endpoint?game=${selectedFandom.string}`);
      // TODO: change when api is setup
      const response = { data: selectedFandom };
      localStorage.setItem("game", JSON.stringify(response.data));
      navigate("/game");
    } catch (error) {}
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

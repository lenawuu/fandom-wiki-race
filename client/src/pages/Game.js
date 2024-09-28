import GameNav from "../components/GameNav";
import IFrame from "../components/IFrame";
import { useState } from "react";

function Game() {
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

  const [numClicks, setNumClicks] = useState(0);

  return (
    <div class="w-screen h-screen">
      <GameNav goal={goal} numClicks={numClicks} />
      <IFrame />
    </div>
  );
}

export default Game;

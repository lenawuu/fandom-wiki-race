import { Button } from "@headlessui/react";
import { ReactComponent as LeftArrowSVG } from "../assets/arrow-left.svg";
import { ReactComponent as RightArrowSVG } from "../assets/arrow-right.svg";

function GameNav({ goal, numClicks, handleNav, curIndex }) {
  return (
    <nav class="navbar justify-between px-8 bg-base-100">
      <div class="flex flex-row gap-2" id="buttonGroup">
        <Button>
          <LeftArrowSVG onClick={() => handleNav(curIndex - 1)} />
        </Button>
        <Button onClick={() => handleNav(curIndex + 1)}>
          <RightArrowSVG />
        </Button>
      </div>
      <div>
        <p class="font-bold text-lg text-primary">
          {goal.start.name} → {goal.end.name}
        </p>
      </div>
      <div>
        <p class="font-semibold text-primary">Clicks: {numClicks}</p>
      </div>
    </nav>
  );
}

export default GameNav;

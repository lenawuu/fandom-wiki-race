import { Button } from "@headlessui/react";
import { ReactComponent as LeftArrowSVG } from "../assets/arrow-left.svg";
import { ReactComponent as RightArrowSVG } from "../assets/arrow-right.svg";

function GameNav({ goal, numClicks }) {
  return (
    <nav>
      <div id="buttonGroup">
        <Button>
          <LeftArrowSVG />
        </Button>
        <Button>
          <RightArrowSVG />
        </Button>
        <div>
          <p>
            {goal.start.name} → {goal.end.name}
          </p>
        </div>
        <div>
          <p>Clicks: {numClicks}</p>
        </div>
      </div>
    </nav>
  );
}

export default GameNav;

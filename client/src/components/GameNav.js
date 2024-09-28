import { Button } from "@headlessui/react";
import { ReactComponent as LeftArrowSVG } from "../assets/arrow-left.svg";
import { ReactComponent as RightArrowSVG } from "../assets/arrow-right.svg";

function GameNav() {
  return (
    <nav>
      <div id="buttonGroup">
        <Button>
          <LeftArrowSVG />
        </Button>
        <Button>
          <RightArrowSVG />
        </Button>
      </div>
    </nav>
  );
}

export default GameNav;

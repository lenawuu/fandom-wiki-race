import { Button } from "@headlessui/react";
import { Link } from "react-router-dom";

function Homepage() {
  return (
    <div>
      <h1>Fandom Wiki Races</h1>
      <p>Testing, Testing, 1, 2, 3...</p>
      <Link to="/game">
        <Button>Click to Play!</Button>
      </Link>
    </div>
  );
}

export default Homepage;

import GameNav from "../components/GameNav";

function Game() {
  const goal = {
    start: "",
    end: "",
  };
  return (
    <div class="w-screen h-screen">
      <GameNav />
      <div class="w-full h-full">
        <iframe
          class="w-full h-full"
          src="https://minecraft.fandom.com/wiki/Minecraft_Wiki"
        ></iframe>
      </div>
    </div>
  );
}

export default Game;

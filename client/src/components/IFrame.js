import { useEffect, useRef } from "react";

function IFrame({ url }) {
  const iframeRef = useRef(url);

  const handleLoad = () => {
    const iframe = iframeRef.current;
    if (iframe && iframe.contentWindow) {
      const doc = iframe.contentWindow.document;

      // Example manipulation: Change the background color
      doc.body.style.backgroundColor = "lightblue";

      // Example: Add a new element
      const newElement = doc.createElement("div");
      newElement.textContent = "Hello from React!";
      newElement.style.fontSize = "24px";
      newElement.style.color = "red";
      doc.body.appendChild(newElement);
    }
  };

  // useEffect(() => {
  //   const iFrameDoc =
  //     iframeRef.current.contentDocument ||
  //     iframeRef.current.contentWindow.document;
  // });

  return (
    <iframe
      ref={iframeRef}
      src="https://minecraft.fandom.com/wiki/Block"
      onLoad={handleLoad}
    ></iframe>
  );
}

export default IFrame;

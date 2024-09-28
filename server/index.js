const express = require("express");
const cheerio = require("cheerio");

const app = express();
const PORT = 8080;

app.use(express.json());

app.post("/clean", async (req, res) => {
  const url = req.body.url;

  if (!url) {
    return res.status(400).send("URL is required");
  }

  try {
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`Error ${response.status}`);
    }

    const html = await response.text();
    const $ = cheerio.load(html);

    // Modify links for CSS and images
    $('link[rel="stylesheet"]').each((i, element) => {
      const href = $(element).attr("href");
      if (href) {
        $(element).attr("href", new URL(href, url).href); // Make it absolute
      }
    });

    $("img").each((i, element) => {
      const src = $(element).attr("src");
      if (src) {
        $(element).attr("src", new URL(src, url).href); // Make it absolute
      }
    });

    const toDelete = [
      "div.global-navigation",
      "div.community-header-wrapper",
      "div.right-rail-wrapper.WikiaRail",
      "div.page-side-tools",
      "div.mcf-wrapper",
      "footer.global-footer",
      "div.top-ads-container",
      "div.page__right-rail",
    ];

    toDelete.forEach((selector) => {
      $(selector).remove();
    });

    // Send the modified HTML
    res.send($.html());
  } catch (error) {
    res.status(500).send(`Error: ${error.message}`);
  }
});

app.listen(PORT, () => {
  console.log("listening on 8080");
});

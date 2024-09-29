const express = require("express");
const cheerio = require("cheerio");
const cors = require("cors");

const app = express();
const PORT = 8081;

app.use(express.json());
app.use(cors());

const fandoms = [
  {
    name: "Mario Kart",
    src: "https://assets.nintendo.com/image/upload/ar_16:9,b_auto:border,c_lpad/b_white/f_auto/q_auto/dpr_1.5/c_scale,w_400/ncom/software/switch/70070000013723/78683d87f12356c571e4541b2ef649e3bd608285139704087c552171f715e399",
    string: "mariokart",
    stem: "https://mariokart.fandom.com/",
    goal: {
      start: {
        title: "Toad Harbor",
        url: "https://mariokart.fandom.com/wiki/Toad_Harbor",
      },
      end: {
        title: "The Train",
        url: "https://mariokart.fandom.com/wiki/The_Train",
      },
      path: ["Toad Harbor", "Coin", "The Train"],
    },
  },
  {
    name: "F-Zero",
    src: "https://www.nintendo.com/eu/media/images/10_share_images/games_15/super_nintendo_5/H2x1_SNES_FZero.jpg",
    string: "https://fzero.fandom.com/",
    goal: {
      start: {
        title: "Magic Seagull",
        url: "https://fzero.fandom.com/wiki/Magic_Seagull",
      },
      end: {
        name: "List of F-Zero locations",
        url: "https://fzero.fandom.com/wiki/List_of_F-Zero_locations",
      },
      path: [
        {
          name: "Magic Seagull",
          url: "https://fzero.fandom.com/wiki/Magic_Seagull",
        },
        {
          name: "Deep Claw",
          url: "https://fzero.fandom.com/wiki/Deep_Claw",
        },
        {
          name: "List of F-Zero locations",
          url: "https://fzero.fandom.com/wiki/List_of_F-Zero_locations",
        },
      ],
    },
  },
  {
    name: "Burnout",
    src: "https://assetsio.gnwcdn.com/bop08.jpg?width=1200&height=1200&fit=bounds&quality=70&format=jpg&auto=webp",
    string: "burnout",
    stem: "https://burnout.fandom.com/",
    goal: {
      start: {
        name: "Nakamura PCPD SI-7",
        url: "https://burnout.fandom.com/wiki/Nakamura_PCPD_SI-7",
      },
      end: {
        name: "Crash TV Episode 32",
        url: "https://burnout.fandom.com/wiki/Crash_TV_Episode_32",
      },
      path: [
        {
          name: "Nakamura PCPD SI-7",
          url: "https://burnout.fandom.com/wiki/Nakamura_PCPD_SI-7",
        },
        {
          name: "Cops and Robbers Pack",
          url: "https://burnout.fandom.com/wiki/Cops_and_Robbers_Pack",
        },
        {
          name: "Crash TV Episode 31",
          url: "https://burnout.fandom.com/wiki/Crash_TV_Episode_31",
        },
        {
          name: "Crash TV Episode 32",
          url: "https://burnout.fandom.com/wiki/Crash_TV_Episode_32",
        },
      ],
    },
  },
];

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
        const absoluteUrl = new URL(src, url).href; // Make it absolute
        console.log(`Original src: ${src}, Absolute src: ${absoluteUrl}`); // Debug log
        $(element).attr("src", absoluteUrl); // Set the absolute URL
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
      "#WikiaBar",
    ];

    toDelete.forEach((selector) => {
      $(selector).remove();
    });

    // Send the modified HTML
    res.set("Access-Control-Allow-Origin", "*");
    res.send($.html());
  } catch (error) {
    res.status(500).send(`Error: ${error.message}`);
  }
});

app.post("/gamedata", (req, res) => {
  const fandom = req.body.fandom;
  const gameData = fandoms.find((f) => f.name === fandom);

  res.send(gameData);
});

app.listen(PORT, () => {
  console.log("listening on 8080");
});

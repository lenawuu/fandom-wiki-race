# FandomWikiRace

## Inspiration

The racing theme of VandyHacks had some of us thinking about our favorite racing games that we have played.
We knew that there were ways to race through the pages of sites like wikipedia, but we didn't find any ways to do it.

## What it does

This fun project allows you to test your knowledge in an exciting game of skill. You must navigate between pages of knowledge of your favorite games and get from one page to another, while only clicking on other links that are contained within the page.

## How we built it

We used python to scrape different fandom pages that we want to be able to race through. This data goes into a neo4j database. Our react front-end uses a a flask server back-end in order to talk with the neo4j database backend. We also used tailwind for styling of our front-end.

## Challenges we ran into

Much of the trouble that we had was integrating our separate parts of the project with each other. By making sure that we we used clear communication with each other during the project we were able ot make sure that each separate part could be integrated together without issues.

## Accomplishments that we're proud of

We are happy to have a submitted project in under 24 hours, we spent a good deal of time during our ideation phase of this journey in order to make sure that we were choosing a reasonable scope for this project

## What we learned

This project let many of us work on several aspects of our software engineering skills. Integrating parts together helped us to work on our teamwork and taught us the value of clear and consice communication on such a short timeframe.

## What's next for FandomWikiRace

If we continue to work on this project in the future, one of the things that we have thought about adding in the future is a robust multiplayer system that you can use in order to play with, and compete against your friends.

# How To run

## Dependencies

-   git
-   node
-   npm

## Step-by-step

### Clone Repository

Navigate to where you would like to install the process and run the following command to clone the repository and navigate to it.

```sh
git clone https://github.com/lenawuu/fandom-wiki-race.git && cd fandom-wiki-race
```

### Install npm dependencies

The following command will install the required node dependencies for the project. Make sure you are still navigated to your fandom-wiki-race folder

```sh
npm i &&
npm i --prefix ./client && npm i --prefix ./server npm i
```

### Run the application

To run the application run:

```sh
npm run all
```

Your application should automatically open, but if it does not, navigate to http://localhost:3000/. it may take a few seconds for the application to start running.

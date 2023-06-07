// server.js

const express = require("express");
const bodyParser = require("body-parser");
const mongoose = require("mongoose");

const app = express();
const port = 3000;

// Connect to MongoDB
mongoose.connect("mongodb://localhost:27017/moviestore", {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});
const db = mongoose.connection;

db.on("error", console.error.bind(console, "MongoDB connection error:"));
db.once("open", () => {
  console.log("Connected to MongoDB");
});

// Define a movie schema
const movieSchema = new mongoose.Schema({
  name: String,
  img: String,
  summary: String,
});

const Movie = mongoose.model("Movie", movieSchema);

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// Routes
// To get all the movies together
app.get("/movies", async (req, res) => {
  try {
    const movies = await Movie.find();
    res.status(200).json(movies);
  } catch (error) {
    console.log(error.message);
    res.status(500).send("some internal server error occured");
  }
});

// To post a single movie on the database
app.post("/movies", async (req, res) => {
  try {
    const { name, img, summary } = req.body;
    const newmovie = new Movie({
      name,
      img,
      summary,
    });

    const savedmovie = await newmovie.save();
    res.status(200).json(savedmovie);
  } catch (error) {
    console.log(error.message);
    res.status(500).send("some internal server error occured");
  }
});

// To get a single movie from the database using it's id as a parameter
app.get("/movies/:id", async (req, res) => {
  try {
    let ObjectId = require("mongodb").ObjectId;
    let id = req.params.id.toString();
    const o_id = new ObjectId(id);
    let movie = await Movie.find({ _id: o_id });
    if (!movie) {
      return res.staus(404).send("No movie found!");
    }
    res.status(200).json(movie);
  } catch (error) {
    console.log(error.message);
    res.status(500).send("some internal server error occured");
  }
});

//To update a specific movie with it's given objectId
app.put("/movies/:id", async (req, res) => {
  try {
    let newmovie = {};
    const { name, img, summary } = req.body;
    if (name) {
      newmovie.name = name;
    }
    if (img) {
      newmovie.img = img;
    }
    if (summary) {
      newmovie.summary = summary;
    }

    let movie = await Movie.findById(req.params.id);
    if (!movie) {
      return res.status(404).send("Movie not found!");
    }

    movie = await Movie.findByIdAndUpdate(
      req.params.id,
      { $set: newmovie },
      { new: true }
    );
    res.status(200).json(movie);
  } catch (error) {
    console.log(error.message);
    res.status(500).send("Some Internal Server Error Occured ): ");
  }
});

app.delete("/movies/:id", async (req, res) => {
  try {
    const removedmovie = await Movie.findByIdAndRemove(req.params.id);
    if (!removedmovie) {
      res.status(404).send("movie not found");
    }
    console.log("Deleted the movie successfully");
    res.status(200).json(removedmovie);
  } catch (error) {
    console.log(error.message);
    res.status(500).send("Some internal server error occured");
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
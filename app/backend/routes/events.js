const express = require("express");
const router = express.Router();
const { fetchEvents } = require("../services/eventAggregator");

router.get("/", async (req, res) => {
  try {
    const events = await fetchEvents();
    res.json({ events });
  } catch (error) {
    console.error("Error fetching events:", error);
    res.status(500).json({ error: "Failed to fetch events" });
  }
});

module.exports = router;

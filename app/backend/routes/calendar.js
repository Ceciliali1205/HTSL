const express = require("express");
const router = express.Router();
const { syncCalendar } = require("../services/calendarService");

router.post("/sync", async (req, res) => {
  const { userId, eventIds } = req.body;
  if (!userId || !eventIds) {
    return res.status(400).json({ error: "User ID and Event IDs are required" });
  }

  try {
    const result = await syncCalendar(userId, eventIds);
    res.json({ message: "Calendar synced successfully", result });
  } catch (error) {
    console.error("Error syncing calendar:", error);
    res.status(500).json({ error: "Failed to sync calendar" });
  }
});

module.exports = router;

const express = require("express");
const router = express.Router();
const { getRecommendations } = require("../services/personalizeservice");

router.post("/recommendations", async (req, res) => {
  const { userId } = req.body;
  if (!userId) {
    return res.status(400).json({ error: "User ID is required" });
  }

  try {
    const recommendations = await getRecommendations(userId);
    res.json({ recommendations });
  } catch (error) {
    console.error("Error fetching recommendations:", error);
    res.status(500).json({ error: "Failed to fetch recommendations" });
  }
});

module.exports = router;

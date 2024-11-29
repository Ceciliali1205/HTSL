const express = require("express");
const cors = require("cors");
const dotenv = require("dotenv");

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

// Routes
const personalizeRoutes = require("./routes/personalize");
const eventsRoutes = require("./routes/events");
const calendarRoutes = require("./routes/calendar");

app.use("/api/personalize", personalizeRoutes);
app.use("/api/events", eventsRoutes);
app.use("/api/calendar", calendarRoutes);

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Backend running on http://localhost:${PORT}`));

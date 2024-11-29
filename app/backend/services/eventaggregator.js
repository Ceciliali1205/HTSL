const axios = require("axios");

const fetchEvents = async () => {
  // Example: Fetch events from multiple URLs or APIs
  const urls = [
    "https://events.utoronto.ca/api/events",
    "https://another-source.com/api/events",
  ];

  const allEvents = [];
  for (const url of urls) {
    const response = await axios.get(url);
    allEvents.push(...response.data.events);
  }

  return allEvents;
};

module.exports = { fetchEvents };

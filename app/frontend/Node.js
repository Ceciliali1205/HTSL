const AWS = require("aws-sdk");

// Initialize AWS SDK (credentials should be automatically picked up from CLI)
AWS.config.update({ region: "us-east-1" }); // Replace with your region if different

// Test S3 Service
const s3 = new AWS.S3();

s3.listBuckets((err, data) => {
  if (err) {
    console.error("Error fetching buckets:", err);
  } else {
    console.log("S3 Buckets:", data.Buckets);
  }
});

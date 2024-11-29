const AWS = require("aws-sdk");

// Initialize AWS SDK
AWS.config.update({ region: "us-east-1" }); // Replace with your AWS region

// Test S3 Service
const s3 = new AWS.S3();

s3.listBuckets((err, data) => {
  if (err) {
    console.error("Error fetching buckets:", err);
  } else {
    console.log("S3 Buckets:", data.Buckets);
  }
});

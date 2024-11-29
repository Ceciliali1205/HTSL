const AWS = require("aws-sdk");

AWS.config.update({
  region: process.env.AWS_REGION,
  accessKeyId: process.env.AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
});

const personalizeRuntime = new AWS.PersonalizeRuntime();

const getRecommendations = async (userId) => {
  const params = {
    campaignArn: process.env.PERSONALIZE_CAMPAIGN_ARN,
    userId,
  };

  const data = await personalizeRuntime.getRecommendations(params).promise();
  return data.itemList.map((item) => item.itemId);
};

module.exports = { getRecommendations };

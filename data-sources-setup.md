# Data Sources Setup Guide

This guide provides step-by-step instructions for setting up the three data source integrations used by Castos Writer: Google Analytics 4 (GA4), Google Search Console, and DataForSEO.

---

## Table of Contents

1. [Google Analytics 4 (GA4) Setup](#google-analytics-4-ga4-setup)
2. [Google Search Console Setup](#google-search-console-setup)
3. [DataForSEO Setup](#dataforseo-setup)
4. [Testing Your Integrations](#testing-your-integrations)
5. [Troubleshooting](#troubleshooting)

---

## Google Analytics 4 (GA4) Setup

Google Analytics 4 provides traffic data, user behavior metrics, and page performance insights for your website.

### Prerequisites
- Admin access to your Google Analytics 4 property
- A Google Cloud project (will be created if you don't have one)

### Step 1: Enable the Google Analytics Data API

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Select or create a project for your Castos Writer integration
3. Navigate to **APIs & Services > Library**
4. Search for "Google Analytics Data API"
5. Click on the API and click **Enable**

### Step 2: Create a Service Account

1. In Google Cloud Console, go to **APIs & Services > Credentials**
2. Click **Create Credentials** and select **Service Account**
3. Fill in the service account details:
   - **Name**: `castos-writer-ga4` (or any descriptive name)
   - **Description**: "Service account for Castos Writer GA4 integration"
4. Click **Create and Continue**
5. Skip the optional "Grant this service account access to project" step (click **Continue**)
6. Skip the optional "Grant users access to this service account" step (click **Done**)

### Step 3: Create and Download the Service Account Key

1. Find your newly created service account in the **Credentials** page
2. Click on the service account email
3. Go to the **Keys** tab
4. Click **Add Key > Create new key**
5. Select **JSON** as the key type
6. Click **Create**
7. The JSON key file will automatically download to your computer
8. **Important**: Keep this file secure! It provides access to your GA4 data

### Step 4: Grant Access to Your GA4 Property

1. Go to [Google Analytics](https://analytics.google.com/)
2. Select your GA4 property
3. Click **Admin** (gear icon in bottom left)
4. Under **Property**, click **Property access management**
5. Click the **+** button in the top right and select **Add users**
6. Enter the service account email (from Step 2, looks like `castos-writer-ga4@your-project.iam.gserviceaccount.com`)
7. Select the role **Viewer** (read-only access)
8. Uncheck "Notify new users by email"
9. Click **Add**

### Step 5: Get Your GA4 Property ID

1. In Google Analytics, click **Admin**
2. Under **Property**, click **Property Settings**
3. Copy your **Property ID** (format: `123456789`)

### Step 6: Configure the Integration

1. Rename your downloaded JSON key file to `ga4-credentials.json`
2. Move the file to: `/Users/craighewitt/Coding/castos-writer/credentials/ga4-credentials.json`
3. Create a `.env` file in the root directory if it doesn't exist
4. Add the following line to your `.env` file:
   ```
   GA4_PROPERTY_ID=274429769
   ```
   (Replace with your actual Property ID from Step 5)

---

## Google Search Console Setup

Google Search Console provides search query data, click-through rates, average positions, and impressions for your website in Google Search results.

### Prerequisites
- Verified ownership of your website in Google Search Console
- A Google Cloud project (same one used for GA4 is fine)

### Step 1: Enable the Google Search Console API

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Select the same project you used for GA4 (or create a new one)
3. Navigate to **APIs & Services > Library**
4. Search for "Google Search Console API"
5. Click on the API and click **Enable**

### Step 2: Create a Service Account (or Reuse Existing)

**Option A: Reuse Your GA4 Service Account** (Recommended)
- You can use the same service account created for GA4
- Skip to Step 3 and use the same JSON key file

**Option B: Create a New Service Account**
1. In Google Cloud Console, go to **APIs & Services > Credentials**
2. Click **Create Credentials** and select **Service Account**
3. Fill in the service account details:
   - **Name**: `castos-writer-gsc` (or any descriptive name)
   - **Description**: "Service account for Castos Writer GSC integration"
4. Click **Create and Continue**
5. Skip the optional steps and click **Done**
6. Create and download a JSON key (same process as GA4 Step 3)

### Step 3: Grant Access to Your Search Console Property

1. Go to [Google Search Console](https://search.google.com/search-console)
2. Select your property (website)
3. Click **Settings** in the left sidebar
4. Click **Users and permissions**
5. Click **Add user**
6. Enter the service account email (e.g., `castos-writer-ga4@your-project.iam.gserviceaccount.com`)
7. Select permission level: **Full** (required for API access, but only provides read access)
8. Click **Add**

### Step 4: Get Your Site URL

Your site URL is the property name in Search Console, typically one of:
- `https://castos.com/` (for domain properties)
- `sc-domain:castos.com` (for domain properties)
- Check in Search Console settings to confirm the exact format

### Step 5: Configure the Integration

**Using the Same Service Account as GA4** (Your Current Setup):

Since you're using the same service account for both GA4 and GSC, the configuration is simple:

1. **Credentials file**: Use the existing `credentials/ga4-credentials.json` (no additional file needed)
2. **Add to your `.env` file**:
   ```
   GSC_SITE_URL=https://castos.com/
   GSC_CREDENTIALS_PATH=credentials/ga4-credentials.json
   ```
3. The integration will automatically use the shared credentials file

**If Using a Separate Service Account** (Alternative):

1. Rename the JSON key to `gsc-credentials.json`
2. Move to: `/Users/craighewitt/Coding/castos-writer/credentials/gsc-credentials.json`
3. Add to your `.env` file:
   ```
   GSC_SITE_URL=https://castos.com/
   GSC_CREDENTIALS_PATH=credentials/gsc-credentials.json
   ```

---

## DataForSEO Setup

DataForSEO provides keyword research data, search volume, competition metrics, and SERP analysis.

### Prerequisites
- A DataForSEO account
- API credits (free trial available, or paid plan)

### Step 1: Create a DataForSEO Account

1. Go to [DataForSEO](https://dataforseo.com/)
2. Click **Sign Up** or **Get Started**
3. Complete the registration process
4. Verify your email address

### Step 2: Get Your API Credentials

1. Log in to your DataForSEO account
2. Go to the [Dashboard](https://app.dataforseo.com/)
3. Navigate to **API Access** or **API Credentials**
4. You'll see your:
   - **Login** (username/email)
   - **Password** (API password, different from account password)
5. Copy both values

**Note**: DataForSEO uses Basic Authentication with login/password, not API keys.

### Step 3: Add Credits to Your Account

1. In the DataForSEO dashboard, go to **Billing** or **Add Credits**
2. Choose a payment option:
   - **Free Trial**: Usually provides $1-5 in credits to test
   - **Pay As You Go**: Add credits as needed
   - **Monthly Plan**: Subscribe for discounted rates
3. Complete the payment process

### Step 4: Configure the Integration

Add the following to your `.env` file:
```
DATAFORSEO_LOGIN=your_username_or_email
DATAFORSEO_PASSWORD=your_api_password
```

### API Usage and Costs

DataForSEO charges per API request. Common pricing:
- **Keywords For Site**: ~$0.10 per 1000 keywords
- **Search Volume**: ~$0.20 per 1000 keywords
- **SERP Analysis**: ~$0.005 per SERP

**Tip**: Start with the free trial to test the integration, then add credits based on your usage needs.

---

## Testing Your Integrations

After setting up all three data sources, test them to ensure they're working correctly.

### Test GA4 Integration

Run the GA4 agent to fetch traffic data:
```bash
npm run agent:ga4-traffic-data
```

Expected output:
- List of top-performing pages with pageviews
- Traffic metrics for recent time periods
- No authentication errors

### Test Google Search Console Integration

Run the GSC agent to fetch search data:
```bash
npm run agent:gsc-search-data
```

Expected output:
- List of top search queries
- Click and impression data
- Average position metrics

### Test DataForSEO Integration

Run the keyword research agent:
```bash
npm run agent:keyword-research "podcast hosting"
```

Expected output:
- Keyword suggestions related to your query
- Search volume data
- Keyword difficulty scores

---

## Troubleshooting

### GA4 Issues

**Error: "Permission denied"**
- Verify the service account email is added to your GA4 property with Viewer permissions
- Double-check you're using the correct Property ID in `.env`

**Error: "API not enabled"**
- Make sure you enabled the Google Analytics Data API in Google Cloud Console
- Wait a few minutes after enabling for changes to propagate

**Error: "Invalid credentials"**
- Verify the JSON key file is in the correct location
- Ensure the file hasn't been corrupted or modified
- Check that the service account hasn't been deleted

### Google Search Console Issues

**Error: "User does not have sufficient permissions"**
- Verify the service account is added to Search Console with Full permissions
- Make sure you're using the correct site URL format in `.env`

**Error: "Site not found"**
- Check the `GSC_SITE_URL` format matches exactly what's in Search Console
- Try both formats: `https://castos.com/` and `sc-domain:castos.com`

### DataForSEO Issues

**Error: "Authentication failed"**
- Verify your login/password in `.env` are correct
- Make sure you're using the API password, not your account password
- Check for any extra spaces in the credentials

**Error: "Insufficient credits"**
- Check your account balance at app.dataforseo.com
- Add more credits or upgrade your plan

**Error: "Rate limit exceeded"**
- DataForSEO has rate limits; wait a few minutes before retrying
- Consider spreading out API calls over time

### General Issues

**Environment Variables Not Loading**
- Make sure your `.env` file is in the root directory
- Verify there are no syntax errors in the `.env` file
- Restart your application after modifying `.env`

**Credentials File Not Found**
- Check the file path is correct: `/Users/craighewitt/Coding/castos-writer/credentials/`
- Create the `credentials/` directory if it doesn't exist:
  ```bash
  mkdir -p /Users/craighewitt/Coding/castos-writer/credentials/
  ```
- Verify file names match exactly (case-sensitive)

---

## Security Best Practices

### Protect Your Credentials

1. **Never commit credentials to Git**
   - Add to `.gitignore`:
     ```
     credentials/
     .env
     ```

2. **Restrict file permissions**:
   ```bash
   chmod 600 credentials/*.json
   chmod 600 .env
   ```

3. **Rotate credentials regularly**
   - Regenerate service account keys every 90 days
   - Update DataForSEO password periodically

4. **Use principle of least privilege**
   - Only grant Viewer/Read access where possible
   - Don't share credentials between projects unnecessarily

### Backup Your Credentials

Store encrypted backups of your credentials in a secure location:
- Password manager (1Password, LastPass, etc.)
- Encrypted cloud storage
- Secure company vault

---

## Quick Reference

### File Structure
```
castos-writer/
├── .env                          # Environment variables
├── credentials/
│   ├── ga4-credentials.json     # GA4 service account key
│   └── gsc-credentials.json     # GSC service account key (or reuse GA4)
└── data-sources-setup.md        # This file
```

### Environment Variables
```bash
# Google Analytics 4
GA4_PROPERTY_ID=123456789

# Google Search Console
GSC_SITE_URL=https://castos.com/

# DataForSEO
DATAFORSEO_LOGIN=your_username
DATAFORSEO_PASSWORD=your_api_password
```

### Useful Links
- [Google Cloud Console](https://console.cloud.google.com/)
- [Google Analytics](https://analytics.google.com/)
- [Google Search Console](https://search.google.com/search-console)
- [DataForSEO Dashboard](https://app.dataforseo.com/)
- [DataForSEO API Documentation](https://docs.dataforseo.com/)

---

## Need Help?

If you encounter issues not covered in this guide:

1. Check the official documentation for each service
2. Review error logs for specific error messages
3. Verify all prerequisites are met
4. Test each integration independently to isolate the issue

---

**Last Updated**: January 2025

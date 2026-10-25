# Deployment Guide

## IBM Cloud Code Engine Deployment

This application is prepared for deployment to IBM Cloud Code Engine. Do NOT guess credentials/URLs - perform deployment with your own IBM Cloud account.

### Prerequisites
- IBM Cloud account
- IBM Cloud CLI installed
- Docker installed

### Steps
1. Login to IBM Cloud: ibmcloud login
2. Target resource group and region
3. Create/select Code Engine project
4. Build and push Docker image
5. Create app with port 8000
6. Get app URL

### Notes
- Update environment variables as needed
- SQLite is used for local dev

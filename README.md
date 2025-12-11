# HubSpot Deals Extraction Service

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/haonanxu006/hubspot-extraction-service.git
cd hubspot-extraction-service
```

### 2. Create and Fill .env

Copy .env.example to .env and Fill:
`HUBSPOT_ACCESS_TOKEN=your_hubspot_private_app_token_here`

### 3. Start the service with Docker Compose

`docker compose up --build`

This launches:

- Flask API service
- PostgreSQL
- Redis

Service will become available at:

`http://localhost:5200/api`

Swagger UI:

`http://localhost:5200/api/docs`

---

## Core API Endpoints

### 1. Start a Scan Job

`POST /scan/start` : Starts a HubSpot Deals extraction job.

Request Body Example:

```json
{
  "config": {
    "scanId": "hubspot-deals-test-1",
    "organizationId": "demo-tenant-1",
    "type": ["user"],
    "auth": {
      "accessToken": "YOUR_HUBSPOT_TOKEN"
    },
    "filters": {
      "properties": [
        "dealname",
        "amount",
        "dealstage",
        "pipeline",
        "closedate",
        "description",
        "dealtype"
      ]
    }
  }
}
```

Response Example:

```json
{
  "success": true,
  "message": "Scan initialization accepted and is now processing in the background."
}
```

---

### 2. Check Scan Status

`GET /scan/{scanId}/status` : Retrieve the current state of an extraction job.

Request Example:
`/scan/hubspot-deals-test-1/status`

Response Example:

```json
{
  "success": true,
  "data": {
    "scanId": "hubspot-deals-test-1",
    "status": "completed",
    "recordsExtracted": 5,
    "checkpointInfo": {
      "latestCheckpoint": {...}
    }
  }
}

```

---

### 3. List Tables for a Scan

`GET /results/{scanId}/tables` : Return a list of all tables generated for a given scan job.

Request Example:
`/results/hubspot-deals-test-1/tables`

Response Example:

```json
{
  "success": true,
  "data": {
    "scanId": "hubspot-deals-test-1",
    "tables": [
      {
        "name": "hubspot_deals",
        "rowCount": 5,
        "extractedCount": 5
      }
    ]
  }
}
```

---

### 4. Get Extracted Deal Records

`GET /results/{scanId}/result?tableName=[tableName]` : Fetch the deal records extracted by the pipeline.

Note:
This endpoint requires a valid tableName from the /results/{scanId}/tables response.

Request Example:
`/results/hubspot-deals-test-1/result?tableName=hubspot_deals`

Response Example:

```json
{
  "success": true,
  "data": {
    "tableName": "hubspot_deals",
    "records": [
      {
        "id": "123456",
        "dealname": "Test Deal",
        "amount": 5000,
        "dealstage": "qualifiedtobuy",
        "pipeline": "default",
        "closedate": "2025-12-31T20:25:34Z",
        "_extracted_at": "2025-12-10T20:36:31Z",
        "_scan_id": "hubspot-deals-test-1"
      }
    ],
    "pagination": {
      "total": 5,
      "limit": 100,
      "offset": 0,
      "hasMore": false
    }
  }
}
```

---

### 5. Health Check

`GET /health` : Used to verify that the service, database connections, and background worker system are operational.

---

## Test Results

All test request responses are stored in folder `test_results`.

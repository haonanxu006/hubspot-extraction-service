# 📋 HubSpot Deals Extraction Service - Integration with HubSpot API

This document explains the HubSpot REST API endpoints required by the HubSpot Deals Extraction Service to extract deal data from HubSpot instances.

---

## 📋 Overview

The HubSpot Deals Extraction Service integrates with HubSpot REST API endpoints to extract deal information. Below are the required and optional endpoints:

### ✅ **Required Endpoint (Essential)**

| **API Endpoint**        | **Purpose**           | **Version** | **Required Permissions** | **Usage**    |
| ----------------------- | --------------------- | ----------- | ------------------------ | ------------ |
| `/crm/v3/objects/deals` | Search and list deals | v3          | crm.objects.deals.read   | **Required** |

### 🔧 **Optional Endpoints (Advanced Features)**

| **API Endpoint**                                             | **Purpose**                                                      | **Version** | **Required Permissions**                              | **Usage** |
| ------------------------------------------------------------ | ---------------------------------------------------------------- | ----------- | ----------------------------------------------------- | --------- |
| `/crm/v3/objects/deals/{dealId}`                             | Retrieve full details of a single deal                           | v3          | crm.objects.deals.read                                | Optional  |
| `/crm/v3/objects/deals/{dealId}/associations/{objectType}`   | Retrieve associated objects (contacts, companies...) for a deal  | v3          | crm.objects.deals.read                                | Optional  |
| `/crm/v3/properties/deals`                                   | Retrieve deal property metadata, enumerations, and field configs | v3          | crm.objects.deals.read                                | Optional  |
| `/crm/v3/objects/deals/{dealId}/associations/{activityType}` | Retrieve emails, notes, tasks associated with a deal             | v3          | crm.objects.deals.read, relevant activity read scopes | Optional  |

### 🎯 **Recommendation**

**Start with only the required endpoint.** The `/crm/v3/objects/deals` endpoint provides all essential deal data needed for basic deal analytics and extraction.

---

## 🔐 Authentication Requirements

### **Private App Token Authentication**

```http
Authorization: Bearer <token>
Content-Type: application/json
```

### **Required Permissions**

- **crm.objects.deals.read**: Read deal objects and their properties
- **crm.objects.deals.write**: Create, update, or delete deal records

---

## 🌐 HubSpot API Endpoints

### 🎯 **PRIMARY ENDPOINT (Required for Basic Deals Extraction)**

### 1. **Search Deals** - `/crm/v3/objects/deals` ✅ **REQUIRED**

**Purpose**: Get paginated list of all deals - **THIS IS ALL YOU NEED FOR BASIC DEAL EXTRACTION**

**Method**: `GET`

**URL**: `https://{baseUrl}/crm/v3/objects/deals`

**Query Parameters**:

```
?limit=10&properties=dealname,amount,dealstage,closedate&archived=false
```

**Request Example**:

```http
GET https://api.hubapi.com/crm/v3/objects/deals?limit=10&properties=dealname,amount,dealstage,closedate&archived=false
Authorization: Bearer <token>
Content-Type: application/json
```

**Response Structure** (Contains ALL essential deal data):

```json
{
  "results": [
    {
      "id": "12345",
      "createdAt": "2023-11-07T05:31:56Z",
      "updatedAt": "2023-11-07T05:31:56Z",
      "archived": false,
      "properties": {
        "dealname": "Big Deal",
        "amount": "5000",
        "dealstage": "closedwon",
        "closedate": "2023-11-07T05:31:56Z"
      },
      "associations": {}
    }
  ],
  "paging": {
    "next": {
      "after": "12345678",
      "link": "<link>"
    }
  }
}
```

**✅ This endpoint provides ALL the default deal fields:**

- `hs_object_id` – HubSpot internal ID for the deal
- `dealname` – Name/title of the deal
- `amount` – Deal amount (numeric)
- `dealstage` – Current stage of the deal
- `pipeline` – Pipeline ID or name the deal belongs to
- `createdate` – Deal creation timestamp
- `closedate` – Deal close timestamp
- `archived` – Boolean, whether the deal is archived
- `associations` – Nested object containing related objects:
  - `contacts` – associated contact IDs
  - `companies` – associated company IDs
  - `tickets` – associated ticket IDs
- `propertiesWithHistory` – Optional: history of selected properties

**Rate Limit**: 100 requests per 10 seconds

---

## 🔧 **OPTIONAL ENDPOINTS (Advanced Features Only)**

> **⚠️ Note**: These endpoints are NOT required for basic deal extraction. Only implement if you need advanced deal analytics like validation of individual deals, [feature 2], or [feature 3].

### 2. **Get Deal Details** - `/crm/v3/objects/deals/{dealId}` 🔧 **OPTIONAL**

**Purpose**: Get detailed information for a specific deal

**When to use**: Only if you need additional deal metadata not available in search

**Method**: `GET`

**URL**: `https://{baseUrl}/crm/v3/objects/deals/{dealId}`

**Request Example**:

```http
GET https://api.hubapi.com/crm/v3/objects/deals/123
Authorization: Bearer <token>
Content-Type: application/json
```

**Response Structure**:

```json
{
  "archived": true,
  "createdAt": "2023-11-07T05:31:56Z",
  "id": "<string>",
  "properties": {
    "dealname": "Big Deal",
    "amount": "5000",
    "dealstage": "closedwon",
    "closedate": "2023-11-07T05:31:56Z"
  },
  "updatedAt": "2023-11-07T05:31:56Z",
  "archivedAt": "2023-11-07T05:31:56Z",
  "associations": {},
  "objectWriteTraceId": "<string>",
  "propertiesWithHistory": {}
}
```

---

### 3. **Get Deal Associations** - `/crm/v3/objects/deals/{dealId}/associations/{objectType}` 🔧 **OPTIONAL**

**Purpose**: Get objects associated with a deal, such as contacts and companies

**When to use**: Only if you need related object analysis and specific metrics

**Method**: `GET`

**URL**: `https://{baseUrl}/crm/v3/objects/deals/{dealId}/associations/{objectType}`

**Query Parameters**:

```
?limit=100&after=12345678
```

**Request Example**:

```http
GET https://api.hubapi.com/crm/v3/objects/deals/123456/associations/contacts?limit=10
Authorization: Bearer <token>
Content-Type: application/json
```

**Response Structure**:

```json
{
  "results": [
    {
      "id": "12345",
      "type": "deal_to_contact"
    },
    {
      "id": "67890",
      "type": "deal_to_contact"
    }
  ],
  "paging": {
    "next": {
      "after": "12345678",
      "link": "<link>"
    }
  }
}
```

---

### 4. **Get Deal Configuration** - `/crm/v3/properties/deals` 🔧 **OPTIONAL**

**Purpose**: Get deal configuration details (Property types, Field labels, Enumerations)

**When to use**: Only if you need pipeline and deal-stage workflow and deal setup analysis

**Method**: `GET`

**URL**: `https://{baseUrl}/crm/v3/properties/deals`

**Request Example**:

```http
GET https://api.hubapi.com/crm/v3/properties/deals
Authorization: Bearer <token>
Content-Type: application/json
```

**Response Structure**:

```json
{
  "results": [
    {
      "displayOrder": 2,
      "fieldType": "select",
      "formField": true,
      "groupName": "contactinformation",
      "hasUniqueValue": false,
      "hidden": false,
      "label": "My Contact Property",
      "modificationMetadata": {
        "archivable": true,
        "readOnlyDefinition": false,
        "readOnlyOptions": false,
        "readOnlyValue": false
      },
      "name": "my_contact_property",
      "options": [
        {
          "description": "Choice number one",
          "displayOrder": 1,
          "hidden": false,
          "label": "Option A",
          "value": "A"
        },
        {
          "description": "Choice number two",
          "displayOrder": 2,
          "hidden": false,
          "label": "Option B",
          "value": "B"
        }
      ],
      "type": "enumeration"
    }
  ],
  "paging": {
    "next": {
      "after": "<string>",
      "link": "<string>"
    },
    "prev": {
      "before": "<string>",
      "link": "<string>"
    }
  }
}
```

---

### 5. **Get Deal Activity Data** - `/crm/v3/objects/deals/{dealId}/associations/{activityType}` 🔧 **OPTIONAL**

**Purpose**: Get activity data for a deal

**When to use**: Only if you need activity analysis

**Method**: `GET`

**URL**: `https://{baseUrl}/crm/v3/properties/deals/{dealId}/associations/{activityType}`

**Query Parameters**:

```
?limit=10&after=12345678
```

**Request Example**:

```http
GET https://api.hubapi.com/crm/v3/objects/deals/12345/associations/emails?limit=10
Authorization: Bearer <token>
Content-Type: application/json
```

**Response Structure**:

```json
{
  "results": [
    {
      "id": "987654",
      "type": "deal_to_email"
    }
  ],
  "paging": {
    "next": {
      "after": "12345678",
      "link": "<link>"
    }
  }
}
```

---

## 📊 Data Extraction Flow

### 🎯 **SIMPLE FLOW (Recommended - Using Only Required Endpoint)**

### **Single Endpoint Approach - `/crm/v3/objects/deals` Only**

```python
def extract_all_objects_simple():
    """Extract all deals using only the /crm/v3/objects/deals endpoint"""
    all_objects = []

    while True:
        response = requests.get(
            f"{base_url}/crm/v3/objects/deals",
            params={
                "after": after,
                "limit": limit
            },
            headers=auth_headers
        )

        data = response.json()
        objects = data.get("results", [])

        if not objects:  # No more objects
            break

        all_objects.extend(objects)

        next_cursor = (
            data.get("paging", {})
                .get("next", {})
                .get("after")
        )

        if not next_cursor:
            break

        after = next_cursor

    return all_objects

# This gives you ALL essential deal data:
# - id, createdAt, updatedAt
# - properties: dealname, amount, pipeline, dealstage, closedate, description, dealtype
```

---

### 🔧 **ADVANCED FLOW (Optional - Multiple Endpoints)**

> **⚠️ Only use this if you need related data, full deal schema, or engagement activities data**

### **Step 1: Batch Deals Retrieval**

```python
# Get deals in batches of 50
for start_at in range(0, total_objects, 50):
    response = requests.get(
        f"{base_url}/crm/v3/objects/deals",
        params={
            "after": after,
            "limit": limit
        },
        headers=auth_headers
    )
    objects_data = response.json()
    objects = objects_data.get("results", [])
```

### **Step 2: Enhanced Dea Details (Optional)**

```python
# Get detailed information for each deal
for obj in objects:
    response = requests.get(
        f"{base_url}/crm/v3/objects/deals/{deal_id}",
        headers=auth_headers
    )
    detailed_object = response.json()
```

### **Step 3: Deal Associations (Optional)**

```python
# Get related contacts or company info
for obj in objects:
    response = requests.get(
        f"{base_url}/crm/v3/objects/deals/{deal_id}/associations/contacts",
        params={"limit": limit},
        headers=auth_headers
    )
    object_related_data = response.json()
```

### **Step 4: Deal Configuration (Optional)**

```python
# Get configuration for each deal
for obj in objects:
    response = requests.get(
        f"{base_url}/crm/v3/properties/deals",
        headers=auth_headers
    )
    object_config = response.json()
```

---

## ⚡ Performance Considerations

### **Rate Limiting**

- **Default Limit**: 100 requests per 10 seconds per API token
- **Burst Limit**: 10 requests per second (short duration)
- **Best Practice**: Implement exponential backoff on HTTP/429 responses

### **Batch Processing**

- **Recommended Batch Size**: 100 deals per request
- **Concurrent Requests**: Max 3 parallel requests (deals are complex objects)
- **Request Interval**: 200ms between requests to stay under rate limits

### **Error Handling**

```http
# Rate limit exceeded
HTTP/429 Too Many Requests
Retry-After: 2

# Authentication failed
HTTP/401 Unauthorized

# Insufficient permissions
HTTP/403 Forbidden

# Deal not found
HTTP/404 Not Found
```

---

## 🔒 Security Requirements

### **API Token Permissions**

#### ✅ **Required (Minimum Permissions)**

```
Required Scopes:
- crm.objects.deals.read (for basic deal information)
```

#### 🔧 **Optional (Advanced Features)**

```
Additional Scopes (only if using optional endpoints):
- crm.objects.deals.read (for contacts associations information)
- crm.objects.companies.read (for companies associations information)
```

### **User Permissions**

#### ✅ **Required (Minimum)**

The API token user must have:

- **CRM Read permission**
- **Deals read access**

#### 🔧 **Optional (Advanced Features)**

Additional permissions (only if using optional endpoints):

- **Contacts read permission** (for contacts associations)
- **Companies read permission** (for companies associations)

---

## 📈 Monitoring & Debugging

### **Request Headers for Debugging**

```http
Authorization: Bearer <token>
Content-Type: application/json
User-Agent: HubSpot-Deals-Extraction-Service/1.0
X-Request-ID: deal-scan-001-batch-1
```

### **Response Validation**

```python
def validate_object_response(object_data):
    required_fields = ["id", "properties"]
    for field in required_fields:
        if field not in object_data:
            raise ValueError(f"Missing required field: {field}")

    # Validate deal type
    if object_data["dealstage"] not in ["qualifiedtobuy", "presentationscheduled", "closedwon", "closedlost"]:
        raise ValueError(f"Invalid deal type: {object_data['dealstage']}")
```

### **API Usage Metrics**

- Track requests per 10 seconds
- Monitor response times
- Log rate limit headers
- Track authentication failures

---

## 🧪 Testing API Integration

### **Test Authentication**

```bash
curl -X GET \
  "https://api.hubapi.com/crm/v3/objects/deals?limit=10" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json"
```

### **Test Deal Search**

```bash
curl -X GET \
  "https://api.hubapi.com/crm/v3/objects/deals?limit=10" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json"
```

### **Test Deal Details**

```bash
curl -X GET \
  "https://api.hubapi.com/crm/v3/objects/deals/{dealId}" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json"
```

---

## 🚨 Common Issues & Solutions

### **Issue**: 401 Unauthorized

**Solution**: Verify HubSpot Private App token

```bash
curl -I "https://api.hubapi.com/crm/v3/objects/deals?limit=10" \
  -H "Authorization: Bearer <token>"
```

### **Issue**: 403 Forbidden

**Solution**: Check user has "crm.objects.deals.read" permissions

### **Issue**: 429 Too Many Requests (Rate Limited)

**Solution**: Implement retry with exponential backoff

```python
import time
import random

def retry_with_backoff(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError:
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(wait_time)
    raise Exception("Max retries exceeded")
```

### **Issue**: Empty Deals List

**Solution**: Verify that your private app token belongs to the same HubSpot portal where the deals exist

### **Issue**: Need Deal Associations/Configuration But Want to Keep It Simple

**Solution**: Start with `/crm/v3/objects/deals` only. Add optional endpoints later if needed for advanced object analytics, such as contacts and companies

---

## 💡 **Implementation Recommendations**

### 🎯 **Phase 1: Start Simple (Recommended)**

1. Implement only `/crm/v3/objects/deals`
2. Extract basic deal data (id, Deal properties (dealname, amount, pipeline, dealstage...))
3. This covers 90% of deal analytics needs

### 🔧 **Phase 2: Add Advanced Features (If Needed)**

1. Add `/crm/v3/objects/deals/{dealId}` for detailed deal info
2. Add `/crm/v3/objects/deals/{dealId}/associations/contacts` for conntacts analysis
3. Add `/crm/v3/properties/deals` for pipeline and dealstage workflow analysis

### ⚡ **Performance Tip**

- **Simple approach**: 1 API call per 100 deals
- **Advanced approach**: 1 + N API calls (N = number of deals for details)
- Start simple to minimize API usage and complexity!

---

## 📞 Support Resources

- **HubSpot CRM API Documentation**: https://developers.hubspot.com/docs/api/crm/deals
- **Rate Limiting Guide**: https://developers.hubspot.com/docs/api/usage-details
- **Authentication Guide**: https://developers.hubspot.com/docs/api/usage-details
- **HubSpot Deal Permissions Reference**: https://knowledge.hubspot.com/user-management/hubspot-user-permissions-guide

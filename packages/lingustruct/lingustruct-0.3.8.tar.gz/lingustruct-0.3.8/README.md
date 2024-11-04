# LinguStruct

**LinguStruct** is a structured system design framework optimized for usability and AI (LLM)-readability. It bridges the gap between **requirement definitions** and **skeleton code**, enabling seamless collaboration between humans and AI. LinguStruct offers pre-defined templates for system documentation, streamlining system development, documentation, and management processes with templates optimized for Large Language Models (LLMs).

---

## Features

- **Template-based Design**: Create consistent system documentation with ready-to-use JSON templates optimized for LLMs.
- **Free and Paid User Modes**: Free users have limited access, but paid users have access to the system with unlimited API key usage.
- **Rate Limiting**: Free users are limited to 5 requests per hour.
- **Redis-based API Key Management**: For internal handling of paid users and rate-limiting logic.
- **Comprehensive API**: Interact with LinguStruct through a set of well-defined API endpoints.
- **Auto Mapping**: Automatically map user-provided data to the most suitable templates (Paid Users Only).
- **Bridging Requirement Definitions and Skeleton Code**: Facilitates seamless integration between requirements and code generation using LLM-optimized design documents.

---

## Installation

Ensure you have Python 3.6 or higher installed.

### Install from PyPI

```bash
pip install lingustruct
```

### Install from Source

```bash
git clone https://github.com/lilseedabe/lingustruct.git
cd lingustruct
pip install -e .
```

---

## Configuration

### Environment Variables

For **paid users**, you need to set your **API key**. You can do this by creating a `.env` file in your project's root directory or by setting environment variables directly in your application.

```ini
# .env file example for paid users
LINGUSTRUCT_LICENSE_KEY=your-paid-api-key
```

---

## Usage Overview

LinguStruct supports both **free** and **paid users**. Below is how you can interact with the system for different scenarios.

### **1. Free Users**

Free users can access templates and generate content **without an API key**, but are limited to **5 requests per hour**.

#### **Fetching Templates as a Free User**

```bash
curl -X 'GET' \
  'https://lingustruct.onrender.com/lingu_struct/templates/m1' \
  -H 'accept: application/json'
```

Free users can access any available template but are subject to rate limits. If the limit is exceeded, the system will return a `429 Too Many Requests` response.

---

### **2. Paid Users**

Paid users can bypass rate limits using their **API key**, gaining **unlimited access** to templates and system features.

#### **Obtaining an API Key**

To obtain an API key, please contact the development team at `osusume-co@lilseed.jp`. Once you have your API key, set it in your environment as shown below.

#### **Using the API Key**

Include the `LINGUSTRUCT_LICENSE_KEY` in the request headers to authenticate.

**Example: Fetching Templates with an API Key**

```bash
curl -X 'GET' \
  'https://lingustruct.onrender.com/lingu_struct/templates/m1' \
  -H 'accept: application/json' \
  -H 'LINGUSTRUCT_LICENSE_KEY: your-paid-api-key'
```

---

### **3. Auto Mapping (Paid Users Only)**

Paid users can utilize the **Auto Mapping** feature to automatically map their data to the most suitable template, streamlining the documentation process.

#### **Using Auto Mapping**

**Endpoint:** `/lingu_struct/auto_map`  
**Method:** `POST`  
**Headers:**
- `Content-Type: application/json`
- `LINGUSTRUCT_LICENSE_KEY: your-paid-api-key`

**Body:**

```json
{
  "data": {
    "Template Version": "1.0",
    "Project Name": "Sample Project",
    "Project Version": "1.0.1",
    "Description": "A sample project description.",
    "Scale": "m"
  }
}
```

**Example: Auto Mapping Request**

```bash
curl -X 'POST' \
  'https://lingustruct.onrender.com/lingu_struct/auto_map' \
  -H 'accept: application/json' \
  -H 'LINGUSTRUCT_LICENSE_KEY: your-paid-api-key' \
  -H 'Content-Type: application/json' \
  -d '{
        "data": {
            "Template Version": "1.0",
            "Project Name": "Sample Project",
            "Project Version": "1.0.1",
            "Description": "A sample project description.",
            "Scale": "m"
        }
    }'
```

**Response:**

```json
{
  "template": "m1",
  "mapped_data": {
    "t_v": "1.0",
    "p_n": "Sample Project",
    "p_v": "1.0.1",
    "desc": "A sample project description.",
    "scale": "m"
  }
}
```

**Notes:**
- **Auto Mapping** selects the most appropriate template based on the provided data keys.
- Only **paid users** can access this feature. Free users attempting to use this endpoint will receive a `403 Forbidden` response.

---

## Template Usage Guide

LinguStruct provides a variety of templates for structuring system documentation. These templates include:

- **Master Template**: `master_template`
- **Overview Template**: `overview_template`
- **Other Modules**: `m1`, `m2`, ..., `m10` (and their `_s` variations for smaller versions)

### **Fetching and Using Templates in Python**

Below is an example of fetching and using a template in Python.

```python
import os
import requests
from dotenv import load_dotenv

# Load environment variables (such as the API key)
load_dotenv()
LINGUSTRUCT_LICENSE_KEY = os.getenv("LINGUSTRUCT_LICENSE_KEY")

# Fetch the template with API key (for paid users)
headers = {"LINGUSTRUCT_LICENSE_KEY": LINGUSTRUCT_LICENSE_KEY}
response = requests.get(
    'https://lingustruct.onrender.com/lingu_struct/templates/master_template',
    headers=headers
)

if response.status_code == 200:
    template = response.json()
    # Modify the template as needed
    template['p_n'] = 'Updated Project Name'
    print(template)
else:
    print(f"Error fetching template: {response.json()}")
```

---

## API Endpoints

### **1. Generate Master JSON**

**Endpoint:** `/lingu_struct/generate_master`

**Method:** `POST`

**Headers:**
- `Content-Type: application/json`
- `LINGUSTRUCT_LICENSE_KEY: your-api-key` (Paid Users Only)

**Body:**

```json
{
  "project_id": "test_project",
  "version": "1.0"
}
```

**Response:**

```json
{
  "message": "master.json generated successfully."
}
```

---

### **2. Generate Overview JSON**

**Endpoint:** `/lingu_struct/generate_overview`

**Method:** `POST`

**Headers:**
- `Content-Type: application/json`
- `LINGUSTRUCT_LICENSE_KEY: your-api-key` (Paid Users Only)

**Body:**

```json
{
  "meta_description": "Meta description",
  "arch_description": "Architecture description",
  "dep_res_description": "Dependency resolution description",
  "err_handling_description": "Error handling description",
  "prio_description": "Priority description",
  "abbr_description": "Abbreviation description",
  "map_description": "Mappings description",
  "p_order_description": "Property order description",
  "version_description": "Version description",
  "tech_description": "Technology description"
}
```

**Response:**

```json
{
  "message": "overview.json generated successfully."
}
```

---

### **3. Fetch Module Data**

**Endpoint:** `/lingu_struct/modules/{module_id}`

**Method:** `GET`

**Headers:**
- `Content-Type: application/json`
- `LINGUSTRUCT_LICENSE_KEY: your-api-key` (Paid Users Only)

**Response:**

```json
{
  "module_id": 1,
  "data": {
    "module_data": "..."
  }
}
```

---

### **4. Convert Module Formats**

**Endpoint:** `/lingu_struct/convert`

**Method:** `POST`

**Headers:**
- `Content-Type: application/json`
- `LINGUSTRUCT_LICENSE_KEY: your-api-key` (Paid Users Only)

**Body:**

```json
{
  "module_id": 1,
  "source_format": "lingu_struct",
  "target_format": "human_readable",
  "data": null
}
```

**Response:**

```json
{
  "human_readable": "Converted data..."
}
```

---

### **5. Convert to PDF**

**Endpoint:** `/lingu_struct/convert_to_pdf`

**Method:** `POST`

**Headers:**
- `Content-Type: application/json`
- `LINGUSTRUCT_LICENSE_KEY: your-api-key` (Paid Users Only)

**Body:**

```json
{
  "module_id": 1
}
```

**Response:**
- PDF file is returned as an attachment.

---

### **6. Fetch Template**

**Endpoint:** `/lingu_struct/templates/{template_name}`

**Method:** `GET`

**Headers:**
- `Content-Type: application/json`
- `LINGUSTRUCT_LICENSE_KEY: your-api-key` (Paid Users Only)

**Response:**

```json
{
  "name": "Sample Template",
  "description": "This is a test template."
}
```

---

### **7. Auto Map Data (Paid Users Only)**

**Endpoint:** `/lingu_struct/auto_map`

**Method:** `POST`

**Headers:**
- `Content-Type: application/json`
- `LINGUSTRUCT_LICENSE_KEY: your-paid-api-key` (Paid Users Only)

**Body:**

```json
{
  "data": {
    "Template Version": "1.0",
    "Project Name": "Sample Project",
    "Project Version": "1.0.1",
    "Description": "A sample project description.",
    "Scale": "m"
  }
}
```

**Response:**

```json
{
  "template": "m1",
  "mapped_data": {
    "t_v": "1.0",
    "p_n": "Sample Project",
    "p_v": "1.0.1",
    "desc": "A sample project description.",
    "scale": "m"
  }
}
```

**Error Responses:**

- **403 Forbidden**: If a free user attempts to access the Auto Mapping feature.

  ```json
  {
    "detail": "This feature is available to paid users only."
  }
  ```

- **400 Bad Request**: If the provided data does not match any available templates.

  ```json
  {
    "detail": "No suitable template found."
  }
  ```

- **500 Internal Server Error**: For unexpected errors during the auto-mapping process.

  ```json
  {
    "detail": "Unexpected error during auto mapping: error details"
  }
  ```

---

## Rate Limits

To ensure fair usage and prevent abuse, LinguStruct implements rate limiting as follows:

- **Free Users**:
  - Limited to **5 requests per hour**.
  - No API key required.
  
- **Paid Users**:
  - **Unlimited access**.
  - Must include a valid `LINGUSTRUCT_LICENSE_KEY` in request headers.

**Note**: Exceeding the rate limit will result in a `429 Too Many Requests` response.

```json
{
  "detail": "Rate limit exceeded. Try again later."
}
```

---

## Abbreviation Reference

Below are the abbreviations used in templates for concise documentation:

| Abbreviation   | Meaning                  | Description                                |
|----------------|--------------------------|--------------------------------------------|
| `t_v`          | Template Version         | Version of the template used               |
| `p_n`          | Project Name             | Name of the project                        |
| `p_v`          | Project Version          | Version of the project                     |
| `desc`         | Description              | Brief description of the project           |
| `scale`        | Scale                    | Scale of the project (e.g., small, medium) |
| `st`           | Style                    | Design style                               |
| `c_n`          | Component Name           | Name of the component                      |
| `c_t`          | Component Type           | Type of the component                      |
| `c_p`          | Component Path           | Path of the component                      |
| `c_dep`        | Component Dependencies   | Dependencies of the component              |
| `dep_res`      | Dependency Resolution    | How dependencies are resolved              |
| `err_handling` | Error Handling           | Approach to error handling                 |
| `prio`         | Priority                 | Priority level                             |
| `map`          | Mappings                 | Key-value mappings                         |
| `p_order`      | Property Order           | Order of properties                        |
| `v`            | Version                  | Version information                        |
| `l`            | Languages                | Programming languages used                 |
| `f`            | Frameworks               | Frameworks used                            |
| `t`            | Tools                    | Tools used                                 |
| `a`            | Authentication           | Authentication details                     |
| `az`           | Authorization            | Authorization details                      |
| `m`            | Microservices            | Microservices architecture                 |
| `p`            | Performance              | Performance considerations                 |
| `ar`           | Architecture             | System architecture overview               |
| `svc`          | Service                  | Services or modules provided               |
| `sec`          | Security                 | Security measures                          |

---

## License

This package is provided for **personal and academic use only**. For commercial use, a license agreement is required.

**Terms of Use**:
1. **Non-Commercial Use Only**: Intended for personal or academic use.
2. **Commercial License Required**: Contact `osusume-co@lilseed.jp` for inquiries.
3. **Redistribution Prohibited**: Public redistribution is not allowed.
4. **No Warranty**: No liability for damages resulting from the use of this software.

---

## Issues & Support

For inquiries, support, or licensing questions, contact the development team at `osusume-co@lilseed.jp`. You can also report issues on the [GitHub Issues](https://github.com/lilseedabe/lingustruct/issues) page.

---

## Changelog

- **v0.3.0**: Updated framework to emphasize collaboration between humans and AI (LLM) in system design.
- **v0.2.8**: Introduced free and paid user modes with rate limits and API key management.
- **v0.2.4**: Removed AI (LLM) support and enhanced template management.

---

## Author

Developed by Yasunori Abe. For inquiries, contact `osusume-co@lilseed.jp`.

---

## Quick Start Guide

### **1. Free Users**

Free users can access LinguStruct without an API key but are limited to **5 requests per hour**.

**Example: Fetching a Template as a Free User**

```bash
curl -X 'GET' \
  'https://lingustruct.onrender.com/lingu_struct/templates/m1' \
  -H 'accept: application/json'
```

### **2. Paid Users**

Paid users can access LinguStruct with an API key, granting **unlimited access**.

**Step 1: Obtain an API Key**

To obtain an API key, please contact the development team at `osusume-co@lilseed.jp`.

**Step 2: Use the API Key in Requests**

Include the `LINGUSTRUCT_LICENSE_KEY` header in your requests.

**Example: Generating a Master Template as a Paid User**

```bash
curl -X 'POST' \
  'https://lingustruct.onrender.com/lingu_struct/generate_master' \
  -H 'accept: application/json' \
  -H 'LINGUSTRUCT_LICENSE_KEY: your-paid-api-key' \
  -H 'Content-Type: application/json' \
  -d '{
        "project_id": "test_project",
        "version": "1.0"
    }'
```

**Example: Using Auto Mapping as a Paid User**

```bash
curl -X 'POST' \
  'https://lingustruct.onrender.com/lingu_struct/auto_map' \
  -H 'accept: application/json' \
  -H 'LINGUSTRUCT_LICENSE_KEY: your-paid-api-key' \
  -H 'Content-Type: application/json' \
  -d '{
        "data": {
            "Template Version": "1.0",
            "Project Name": "Sample Project",
            "Project Version": "1.0.1",
            "Description": "A sample project description.",
            "Scale": "m"
        }
    }'
```

**Response:**

```json
{
  "template": "m1",
  "mapped_data": {
    "t_v": "1.0",
    "p_n": "Sample Project",
    "p_v": "1.0.1",
    "desc": "A sample project description.",
    "scale": "m"
  }
}
```

---

## Running the Server

To run the LinguStruct server locally (for development purposes), ensure that all dependencies are installed and environment variables are set appropriately.

**Start the Server Using Uvicorn**

```bash
uvicorn api.main:app --reload
```

**Note**: The `--reload` flag is useful for development purposes. For production, consider using a more robust server configuration.

---

## Testing

LinguStruct includes a suite of tests to ensure functionality.

### **Running Tests**

Ensure you have `pytest` installed:

```bash
pip install pytest
```

Run the tests using the following command:

```bash
pytest
```

---

## Security Best Practices

- **Protect Your API Keys**: Ensure that your API keys (`LINGUSTRUCT_LICENSE_KEY`) are kept confidential. Do not expose them in client-side code or public repositories.

---

## Disclaimer

The authors are not responsible for any misuse or unintended consequences of using this framework. Users must adhere to applicable laws and regulations.

---

## Contact

For inquiries, support, or licensing questions, contact the development team at `osusume-co@lilseed.jp`.

---

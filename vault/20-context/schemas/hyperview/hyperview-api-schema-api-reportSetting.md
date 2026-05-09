# Hyperview API Schema - `/api/reportSetting`

Operations in this namespace: **1**

## `GET /api/reportSetting/reportPages/{section}`
- **Summary:** Returns a list of report pages of a section.
- **Tags:** `ReportPages`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `section` | `path` | `True` | `Section` | The report section. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<ReportPageDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

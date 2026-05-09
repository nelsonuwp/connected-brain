# Hyperview API Schema - `/api/setting`

Operations in this namespace: **130**

## `GET /api/setting/accessPolicies`
- **Summary:** Returns an array of access policies.
- **Tags:** `AccessPolicies`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |
| `(after)` | `query` | `False` | `integer` | Return records after the specified number of records. |
| `(limit)` | `query` | `False` | `integer` | Number of records to return. |
| `(sort)` | `query` | `False` | `string` | Sort order. Format: "+|-fieldName". |
| `(filter)` | `query` | `False` | `string` | Cross field filter. Filters results that have the given value. |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<AccessPolicyDetailedDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/setting/accessPolicies`
- **Summary:** Saves an access policy.
- **Tags:** `AccessPolicies`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `AccessPolicyDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/accessPolicies/{accessPolicyId}`
- **Summary:** Updates an access policy.
- **Tags:** `AccessPolicies`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `accessPolicyId` | `path` | `True` | `string(uuid)` | An access policy ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `AccessPolicyDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/setting/accessPolicies/{accessPolicyId}`
- **Summary:** Deletes a access policy.
- **Tags:** `AccessPolicies`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `accessPolicyId` | `path` | `True` | `string(uuid)` | An access policy ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/accessPolicyGroups`
- **Summary:** Returns a list of user groups
- **Tags:** `AccessPolicyGroups`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<AccessPolicyGroupDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/accessPolicyGroups/{accessPolicyId}`
- **Summary:** Returns user groups that can be assigned to an access policy.
- **Tags:** `AccessPolicyGroups`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `accessPolicyId` | `path` | `True` | `string(uuid)` | An access policy ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<AccessPolicyGroupDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/alarmEventPolicies`
- **Summary:** Returns an array of alarm event policies.
- **Tags:** `AlarmEventPolicies`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<AlarmEventPolicyDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/setting/alarmEventPolicies`
- **Summary:** Creates an alarm event policy and returns its ID.
- **Tags:** `AlarmEventPolicies`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ModifiableAlarmEventPolicyDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/alarmEventPolicies/{id}`
- **Summary:** Updates an alarm event policy.
- **Tags:** `AlarmEventPolicies`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | An alarm event policy ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ModifiableAlarmEventPolicyDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: ModifiableAlarmEventPolicyDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/setting/alarmEventPolicies/{id}`
- **Summary:** Deletes an alarm event policy.
- **Tags:** `AlarmEventPolicies`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | An alarm event policy ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/applicationEventLogs`
- **Summary:** Returns a list of application events.
- **Tags:** `ApplicationEventLogs`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |
| `(after)` | `query` | `False` | `integer` | Return records after the specified number of records. |
| `(limit)` | `query` | `False` | `integer` | Number of records to return. |
| `(sort)` | `query` | `False` | `string` | Sort order. Format: "+|-fieldName". |
| `(filter)` | `query` | `False` | `string` | Cross field filter. Filters results that have the given value. |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<ApplicationEventDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/assetPropertyKeys`
- **Summary:** Returns a list of asset property keys.
- **Tags:** `AssetPropertyKeys`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<AssetPropertyKeyDetailedDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/assetTypeDashboardSettings/{assetType}`
- **Summary:** Updates an asset type dashboard override setting and returns the updated dashboard override setting.
- **Tags:** `AssetTypeDashboardSettings`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetType` | `path` | `True` | `AssetTypeEnum` | An asset type. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ModifiableAssetTypeDashboardSettingDto` |
| `text/json` | `ModifiableAssetTypeDashboardSettingDto` |
| `application/*+json` | `ModifiableAssetTypeDashboardSettingDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: ModifiableAssetTypeDashboardSettingDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/setting/assetTypeDashboardSettings/{assetType}`
- **Summary:** Deletes an asset type dashboard override setting.
- **Tags:** `AssetTypeDashboardSettings`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetType` | `path` | `True` | `AssetTypeEnum` | An asset type. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/bacnetIpDefinitions`
- **Summary:** Returns a collection of BACnet/IP definitions.
- **Tags:** `BacnetIpDefinitions`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetType` | `query` | `False` | `AssetTypeEnum` | An optional asset type to filter the results. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<BacnetIpDefinitionDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/setting/bacnetIpDefinitions`
- **Summary:** Creates a BACnet/IP definition.
- **Tags:** `BacnetIpDefinitions`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BacnetIpDefinitionDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/bacnetIpDefinitions/bacnetIpNonNumericSensors/{bacnetIpDefinitionId}`
- **Summary:** Returns a collection of BACnet/IP non-numeric sensors.
- **Tags:** `BacnetIpNonNumericSensors`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `bacnetIpDefinitionId` | `path` | `True` | `string(uuid)` | A BACnet/IP definition ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<BacnetIpNonNumericSensorDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/setting/bacnetIpDefinitions/bacnetIpNonNumericSensors/{bacnetIpDefinitionId}`
- **Summary:** Creates a BACnet/IP non-numeric sensor.
- **Tags:** `BacnetIpNonNumericSensors`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `bacnetIpDefinitionId` | `path` | `True` | `string(uuid)` | A BACnet/IP definition ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BacnetIpNonNumericSensorDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/bacnetIpDefinitions/bacnetIpNonNumericSensors/{bacnetIpDefinitionId}/{bacnetIpNonNumericSensorId}`
- **Summary:** Updates a BACnet/IP non-numeric sensor.
- **Tags:** `BacnetIpNonNumericSensors`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `bacnetIpDefinitionId` | `path` | `True` | `string(uuid)` | A BACnet/IP definition ID. |
| `bacnetIpNonNumericSensorId` | `path` | `True` | `string(uuid)` | A BACnet/IP definition non-numeric sensor ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BacnetIpNonNumericSensorDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: BacnetIpNonNumericSensorDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/setting/bacnetIpDefinitions/bacnetIpNonNumericSensors/{bacnetIpDefinitionId}/{bacnetIpNonNumericSensorId}`
- **Summary:** Deletes a BACnet/IP non-numeric sensor.
- **Tags:** `BacnetIpNonNumericSensors`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `bacnetIpDefinitionId` | `path` | `True` | `string(uuid)` | A BACnet/IP definition ID. |
| `bacnetIpNonNumericSensorId` | `path` | `True` | `string(uuid)` | A BACnet/IP non-numeric sensor ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/bacnetIpDefinitions/bacnetIpNumericSensors/{bacnetIpDefinitionId}`
- **Summary:** Returns a collection of BACnet/IP numeric sensors.
- **Tags:** `BacnetIpNumericSensors`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `bacnetIpDefinitionId` | `path` | `True` | `string(uuid)` | A BACnet/IP definition ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<BacnetIpNumericSensorDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/setting/bacnetIpDefinitions/bacnetIpNumericSensors/{bacnetIpDefinitionId}`
- **Summary:** Creates a BACnet/IP numeric sensor.
- **Tags:** `BacnetIpNumericSensors`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `bacnetIpDefinitionId` | `path` | `True` | `string(uuid)` | A BACnet/IP definition ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BacnetIpNumericSensorDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/bacnetIpDefinitions/bacnetIpNumericSensors/{bacnetIpDefinitionId}/{bacnetIpNumericSensorId}`
- **Summary:** Updates a BACnet/IP numeric sensor.
- **Tags:** `BacnetIpNumericSensors`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `bacnetIpDefinitionId` | `path` | `True` | `string(uuid)` | A BACnet/IP definition ID. |
| `bacnetIpNumericSensorId` | `path` | `True` | `string(uuid)` | A BACnet/IP definition numeric sensor ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BacnetIpNumericSensorDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: BacnetIpNumericSensorDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/setting/bacnetIpDefinitions/bacnetIpNumericSensors/{bacnetIpDefinitionId}/{bacnetIpNumericSensorId}`
- **Summary:** Deletes a BACnet/IP numeric sensor.
- **Tags:** `BacnetIpNumericSensors`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `bacnetIpDefinitionId` | `path` | `True` | `string(uuid)` | A BACnet/IP definition ID. |
| `bacnetIpNumericSensorId` | `path` | `True` | `string(uuid)` | A BACnet/IP numeric sensor ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/bacnetIpDefinitions/{bacnetIpDefinitionId}`
- **Summary:** Returns a BACnet/IP definition.
- **Tags:** `BacnetIpDefinitions`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `bacnetIpDefinitionId` | `path` | `True` | `string(uuid)` | A BACnet/IP definition ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: BacnetIpDefinitionDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/bacnetIpDefinitions/{bacnetIpDefinitionId}`
- **Summary:** Updates a BACnet/IP definition.
- **Tags:** `BacnetIpDefinitions`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `bacnetIpDefinitionId` | `path` | `True` | `string(uuid)` | A BACnet/IP definition ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BacnetIpDefinitionDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/setting/bacnetIpDefinitions/{bacnetIpDefinitionId}`
- **Summary:** Deletes a BACnet/IP definition.
- **Tags:** `BacnetIpDefinitions`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `bacnetIpDefinitionId` | `path` | `True` | `string(uuid)` | A BACnet/IP definition ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/credentials`
- **Summary:** Returns an array of protocol credentials.
- **Tags:** `Credentials`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |
| `(after)` | `query` | `False` | `integer` | Return records after the specified number of records. |
| `(limit)` | `query` | `False` | `integer` | Number of records to return. |
| `(sort)` | `query` | `False` | `string` | Sort order. Format: "+|-fieldName". |
| `(filter)` | `query` | `False` | `string` | Cross field filter. Filters results that have the given value. |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<CredentialDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/setting/credentials`
- **Summary:** Saves a Credential.
- **Tags:** `Credentials`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ModifiableCredentialDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/credentials/{credentialId}`
- **Summary:** Returns an individual credential.
- **Tags:** `Credentials`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `credentialId` | `path` | `True` | `string(uuid)` | A credential ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: CredentialDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/credentials/{credentialId}`
- **Summary:** Updates a Credential.
- **Tags:** `Credentials`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `credentialId` | `path` | `True` | `string(uuid)` | A credential ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ModifiableCredentialDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/setting/credentials/{credentialId}`
- **Summary:** Deletes a Credential.
- **Tags:** `Credentials`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `credentialId` | `path` | `True` | `string(uuid)` | A credential ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/credentials/{credentialId}/showPassword`
- **Summary:** Returns credential passwords.
- **Tags:** `Credentials`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `credentialId` | `path` | `True` | `string(uuid)` | A credential ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: CredentialPasswordDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/customPropertyGroup`
- **Summary:** Get a list of custom property groups.
- **Tags:** `CustomPropertyGroup`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<DetailedCustomPropertyGroupDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/setting/customPropertyGroup`
- **Summary:** Creates a custom property group and returns its ID.
- **Tags:** `CustomPropertyGroup`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BaseCustomPropertyGroupDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/customPropertyGroup/{customPropertyGroupId}`
- **Summary:** Update custom property group for group ID.
- **Tags:** `CustomPropertyGroup`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `customPropertyGroupId` | `path` | `True` | `string(uuid)` | A custom property group ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BaseCustomPropertyGroupDto` |
| `text/json` | `BaseCustomPropertyGroupDto` |
| `application/*+json` | `BaseCustomPropertyGroupDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: BaseCustomPropertyGroupDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/setting/customPropertyGroup/{customPropertyGroupId}`
- **Summary:** Deletes a single custom property group.
- **Tags:** `CustomPropertyGroup`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `customPropertyGroupId` | `path` | `True` | `string(uuid)` | ID of custom property group. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/customPropertySetting`
- **Summary:** Get a list of custom property settings.
- **Tags:** `CustomPropertySetting`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<CustomPropertySettingDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/setting/customPropertySetting`
- **Summary:** Creates a custom property setting and returns its ID.
- **Tags:** `CustomPropertySetting`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `CustomPropertySettingDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/customPropertySetting/{customPropertySettingId}`
- **Summary:** Update custom property setting for setting ID.
- **Tags:** `CustomPropertySetting`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `customPropertySettingId` | `path` | `True` | `string(uuid)` | A custom property setting ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `CustomPropertySettingDto` |
| `text/json` | `CustomPropertySettingDto` |
| `application/*+json` | `CustomPropertySettingDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: CustomPropertySettingDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/setting/customPropertySetting/{customPropertySettingId}`
- **Summary:** Deletes a single custom property setting.
- **Tags:** `CustomPropertySetting`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `customPropertySettingId` | `path` | `True` | `string(uuid)` | ID of custom property setting. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/dataCollector`
- **Summary:** Retrieve a list of Data Collectors.
- **Tags:** `DataCollector`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |
| `(after)` | `query` | `False` | `integer` | Return records after the specified number of records. |
| `(limit)` | `query` | `False` | `integer` | Number of records to return. |
| `(sort)` | `query` | `False` | `string` | Sort order. Format: "+|-fieldName". |
| `(filter)` | `query` | `False` | `string` | Cross field filter. Filters results that have the given value. |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<DataCollectorDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/setting/dataCollector/retire`
- **Summary:** Retires a Data Collector and transfer responsibilities to an active Data Collector.
- **Tags:** `DataCollector`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `DataCollectorRetirementDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/setting/dataCollectorToken`
- **Summary:** Saves registration token to database.
- **Tags:** `DataCollectorToken`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `string(uuid)` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/discoveries`
- **Summary:** Returns a collection of discovery settings.
- **Tags:** `Discoveries`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<DiscoveryDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/setting/discoveries`
- **Summary:** Creates a discovery setting.
- **Tags:** `Discoveries`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `DiscoveryDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/discoveries/{discoveryId}`
- **Summary:** Updates a discovery setting.
- **Tags:** `Discoveries`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `discoveryId` | `path` | `True` | `string(uuid)` | A discovery ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `DiscoveryDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: DiscoveryDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/setting/discoveries/{discoveryId}`
- **Summary:** Deletes a discovery setting.
- **Tags:** `Discoveries`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `discoveryId` | `path` | `True` | `string(uuid)` | A discovery ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/discoveries/{discoveryId}/schedule`
- **Summary:** Returns an individual discovery schedule.
- **Tags:** `Discoveries`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `discoveryId` | `path` | `True` | `string(uuid)` | A discovery ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: DiscoveryScheduleDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/discoveries/{id}`
- **Summary:** Returns a discovery setting.
- **Tags:** `Discoveries`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A discovery setting Id. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: DiscoveryDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/discoveryAssetHistories/{discoveryHistoryId}`
- **Summary:** Returns a collection of summaries about discovered assets for a given discovery history.
- **Tags:** `DiscoveryAssetHistories`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `discoveryHistoryId` | `path` | `True` | `string(uuid)` | - |
| `api-version` | `header` | `False` | `string` | - |
| `(after)` | `query` | `False` | `integer` | Return records after the specified number of records. |
| `(limit)` | `query` | `False` | `integer` | Number of records to return. |
| `(sort)` | `query` | `False` | `string` | Sort order. Format: "+|-fieldName". |
| `(filter)` | `query` | `False` | `string` | Cross field filter. Filters results that have the given value. |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<DiscoveryAssetHistoryDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/discoveryHistories`
- **Summary:** Returns a collection history of ran discoveries.
- **Tags:** `DiscoveryHistories`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |
| `(after)` | `query` | `False` | `integer` | Return records after the specified number of records. |
| `(limit)` | `query` | `False` | `integer` | Number of records to return. |
| `(sort)` | `query` | `False` | `string` | Sort order. Format: "+|-fieldName". |
| `(filter)` | `query` | `False` | `string` | Cross field filter. Filters results that have the given value. |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<DiscoveryHistoryDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/discoveryHistories/{discoveryHistoryId}`
- **Summary:** Returns the details of a ran discovery.
- **Tags:** `DiscoveryHistories`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `discoveryHistoryId` | `path` | `True` | `string(uuid)` | A discovery history ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: DiscoveryHistoryDetailedDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/discoveryProtocolSettings/ports`
- **Summary:** Returns a list of ports for a specific discovery protocol.
- **Tags:** `DiscoveryProtocolSettings`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `discoveryId` | `query` | `True` | `string(uuid)` | A discovery ID. |
| `protocolId` | `query` | `True` | `DataSource` | A protocol ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<ProtocolPortDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/setting/discoveryProtocolSettings/ports`
- **Summary:** Creates a protocol port.
- **Tags:** `DiscoveryProtocolSettings`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ProtocolPortDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/setting/discoveryProtocolSettings/ports/{portId}`
- **Summary:** Deletes a discovery protocol port.
- **Tags:** `DiscoveryProtocolSettings`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `portId` | `path` | `True` | `string(uuid)` | A protocol port ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/discoveryProtocolSettings/protocolCredentials`
- **Summary:** Retrieves a collection of credentials for a given discovery protocol.
- **Tags:** `DiscoveryProtocolSettings`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `discoveryId` | `query` | `True` | `string(uuid)` | A discovery ID. |
| `protocolId` | `query` | `True` | `DataSource` | A protocol ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<CredentialDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/setting/discoveryProtocolSettings/protocolCredentials`
- **Summary:** Creates a protocol credential and associates it with a discovery.
- **Tags:** `DiscoveryProtocolSettings`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `NewDiscoveryProtocolCredentialDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/setting/discoveryProtocolSettings/protocolCredentials/{protocolCredentialId}`
- **Summary:** Associates a protocol credential with a discovery.
- **Tags:** `DiscoveryProtocolSettings`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `protocolCredentialId` | `path` | `True` | `string(uuid)` | A protocol credential ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `True`
| Content-Type | Schema |
|---|---|
| `application/json` | `string(uuid)` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/setting/discoveryProtocolSettings/protocolCredentials/{protocolCredentialId}`
- **Summary:** Removes a protocol credential from a discovery.
- **Tags:** `DiscoveryProtocolSettings`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `protocolCredentialId` | `path` | `True` | `string(uuid)` | A protocol credential ID. |
| `discoveryId` | `query` | `True` | `string(uuid)` | A discovery ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/discoveryProtocolSettings/protocols`
- **Summary:** Retrieves a collection of protocols for a given discovery.
- **Tags:** `DiscoveryProtocolSettings`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `discoveryId` | `query` | `True` | `string(uuid)` | A discovery ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<ProtocolDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/discoveryProtocolSettings/protocols`
- **Summary:** Updates a protocol for a discovery.
- **Tags:** `DiscoveryProtocolSettings`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ProtocolDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: ProtocolDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/discoveryProtocolSettings/protocols/{protocolId}`
- **Summary:** Retrieves a protocol.
- **Tags:** `DiscoveryProtocolSettings`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `protocolId` | `path` | `True` | `DataSource` | A protocol ID. |
| `discoveryId` | `query` | `True` | `string(uuid)` | A discovery ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: ProtocolDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/discoveryRanges`
- **Summary:** Retrieves a collection of network ranges for discovery.
- **Tags:** `DiscoveryRanges`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |
| `(after)` | `query` | `False` | `integer` | Return records after the specified number of records. |
| `(limit)` | `query` | `False` | `integer` | Number of records to return. |
| `(sort)` | `query` | `False` | `string` | Sort order. Format: "+|-fieldName". |
| `(filter)` | `query` | `False` | `string` | Cross field filter. Filters results that have the given value. |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<DiscoveryRangeDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/setting/discoveryRanges`
- **Summary:** Saves a discovery range.
- **Tags:** `DiscoveryRanges`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `DiscoveryRangeDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/discoveryRanges/{id}`
- **Summary:** Updates a discovery range.
- **Tags:** `DiscoveryRanges`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A discovery range ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `DiscoveryRangeDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: DiscoveryRangeDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/setting/discoveryRanges/{id}`
- **Summary:** Deletes a discovery range.
- **Tags:** `DiscoveryRanges`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A discovery range ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/setting/discoveryRunner/{discoveryId}`
- **Summary:** Schedules a discovery to run immediately.
- **Tags:** `DiscoveryRunner`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `discoveryId` | `path` | `True` | `string(uuid)` | A discovery's ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/setting/discoveryRunner/{discoveryId}/abort`
- **Summary:** Aborts a running discovery.
- **Tags:** `DiscoveryRunner`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `discoveryId` | `path` | `True` | `string(uuid)` | A discovery's ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/setting/discoverySchedules`
- **Summary:** Saves a discovery schedule.
- **Tags:** `DiscoverySchedules`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `DiscoveryScheduleDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/discoverySchedules/{discoveryScheduleId}`
- **Summary:** Updates a discovery schedule.
- **Tags:** `DiscoverySchedules`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `discoveryScheduleId` | `path` | `True` | `string(uuid)` | A discovery schedule ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `DiscoveryScheduleDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/setting/discoverySchedules/{discoveryScheduleId}`
- **Summary:** Deletes a discovery schedule.
- **Tags:** `DiscoverySchedules`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `discoveryScheduleId` | `path` | `True` | `string(uuid)` | Discovery schedule ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/documentAccessPolicies/{documentId}`
- **Summary:** Returns the access policy ID associated with a document.
- **Tags:** `DocumentAccessPolicies`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `documentId` | `path` | `True` | `string(uuid)` | A document ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/documentAccessPolicies/{documentId}`
- **Summary:** Updates and returns a document access policy.
- **Tags:** `DocumentAccessPolicies`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `documentId` | `path` | `True` | `string(uuid)` | A document ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `string(uuid)` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/documentDetails`
- **Summary:** Returns a collection of document details.
- **Tags:** `DocumentDetails`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<DocumentDetailSummaryDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/documentDetails/{documentDetailsId}`
- **Summary:** Returns details for a single document.
- **Tags:** `DocumentDetails`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `documentDetailsId` | `path` | `True` | `string(uuid)` | - |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: DocumentDetailSummaryDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/setting/documents`
- **Summary:** Uploads a document and saves its details.
- **Tags:** `Documents`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `multipart/form-data` | `object` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `text/plain: string(uuid); application/json: string(uuid); text/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/documents/{documentId}`
- **Summary:** Downloads a document.
- **Tags:** `Documents`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `documentId` | `path` | `True` | `string(uuid)` | A document ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/documents/{documentId}`
- **Summary:** Updates a document.
- **Tags:** `Documents`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `documentId` | `path` | `True` | `string(uuid)` | - |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `multipart/form-data` | `object` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/setting/documents/{documentId}`
- **Summary:** Deletes a document.
- **Tags:** `Documents`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `documentId` | `path` | `True` | `string(uuid)` | A document ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/enumCustomAssetProperties/{customAssetPropertyKeyId}`
- **Summary:** Returns a list of all enum values for a given enum ID.
- **Tags:** `EnumCustomAssetProperties`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `customAssetPropertyKeyId` | `path` | `True` | `string(uuid)` | The custom asset property key ID of an enum value. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<CustomAssetPropertyEnumValueDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/equinixSmartViewConfiguration`
- **Summary:** Returns the Equinix Smart View integration configuration.
- **Tags:** `EquinixSmartViewConfiguration`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: SmartViewConfigurationOverviewDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/equinixSmartViewConfiguration`
- **Summary:** Saves the Smart View integration configuration changes.
- **Tags:** `EquinixSmartViewConfiguration`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `SmartViewConfigurationOverviewDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: SmartViewConfigurationOverviewDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/equinixSmartViewConfiguration/verifyAuthenticationConfiguration`
- **Summary:** Verifies the Smart View integration authentication configuration.
- **Tags:** `EquinixSmartViewConfiguration`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `SmartViewConfigurationOverviewDto` |
| `text/json` | `SmartViewConfigurationOverviewDto` |
| `application/*+json` | `SmartViewConfigurationOverviewDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/equinixSmartViewIbxConfigurations`
- **Summary:** Returns a collection of Equinix Smart View IBX configurations.
- **Tags:** `EquinixSmartViewIbxConfigurations`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<SmartViewIbxConfigurationDetailedDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/setting/equinixSmartViewIbxConfigurations`
- **Summary:** Creates an Equinix Smart View IBX configuration.
- **Tags:** `EquinixSmartViewIbxConfigurations`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `SmartViewIbxConfigurationDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/setting/equinixSmartViewIbxConfigurations/{configurationId}`
- **Summary:** Deletes an Equinix Smart View IBX configuration.
- **Tags:** `EquinixSmartViewIbxConfigurations`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `configurationId` | `path` | `True` | `string(uuid)` | An Equinix Smart View IBX configuration ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/equinixSmartViewIbxConfigurations/{id}`
- **Summary:** Updates an Equinix Smart View IBX configuration.
- **Tags:** `EquinixSmartViewIbxConfigurations`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | The Smart View IBX configuration ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `SmartViewIbxConfigurationDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/equinixSmartViewIntegration/initiateSync`
- **Summary:** Initiates multiple Equinix Smart View integration IBX syncs.
- **Tags:** `EquinixSmartViewIntegration`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `SmartViewIbxInitiateSyncConfigurationDto` |
| `text/json` | `SmartViewIbxInitiateSyncConfigurationDto` |
| `application/*+json` | `SmartViewIbxInitiateSyncConfigurationDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `202` | Accepted | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/license`
- **Summary:** Returns the license information.
- **Tags:** `License`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: LicenseDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/modbusTcpDefinitions`
- **Summary:** Returns a collection of Modbus TCP definitions.
- **Tags:** `ModbusTcpDefinitions`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetType` | `query` | `False` | `AssetTypeEnum` | An optional asset type to filter the results. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<ModbusTcpDefinitionDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/setting/modbusTcpDefinitions`
- **Summary:** Creates a Modbus TCP definition.
- **Tags:** `ModbusTcpDefinitions`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ModbusTcpDefinitionDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/modbusTcpDefinitions/modbusTcpNonNumericSensors/{modbusTcpDefinitionId}`
- **Summary:** Returns a collection of Modbus TCP non-numeric sensors.
- **Tags:** `ModbusTcpNonNumericSensors`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `modbusTcpDefinitionId` | `path` | `True` | `string(uuid)` | A Modbus TCP definition ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<ModbusTcpNonNumericSensorDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/setting/modbusTcpDefinitions/modbusTcpNonNumericSensors/{modbusTcpDefinitionId}`
- **Summary:** Creates a Modbus TCP non-numeric sensor.
- **Tags:** `ModbusTcpNonNumericSensors`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `modbusTcpDefinitionId` | `path` | `True` | `string(uuid)` | A Modbus TCP definition ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ModbusTcpNonNumericSensorDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/modbusTcpDefinitions/modbusTcpNonNumericSensors/{modbusTcpDefinitionId}/{modbusTcpNonNumericSensorId}`
- **Summary:** Updates a Modbus TCP non-numeric sensor.
- **Tags:** `ModbusTcpNonNumericSensors`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `modbusTcpDefinitionId` | `path` | `True` | `string(uuid)` | A Modbus TCP definition ID. |
| `modbusTcpNonNumericSensorId` | `path` | `True` | `string(uuid)` | A Modbus TCP non-numeric sensor ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ModbusTcpNonNumericSensorDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: ModbusTcpNonNumericSensorDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/setting/modbusTcpDefinitions/modbusTcpNonNumericSensors/{modbusTcpDefinitionId}/{modbusTcpNonNumericSensorId}`
- **Summary:** Deletes a Modbus TCP non-numeric sensor.
- **Tags:** `ModbusTcpNonNumericSensors`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `modbusTcpDefinitionId` | `path` | `True` | `string(uuid)` | A Modbus TCP definition ID. |
| `modbusTcpNonNumericSensorId` | `path` | `True` | `string(uuid)` | A Modbus TCP non-numeric sensor ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/modbusTcpDefinitions/modbusTcpNumericSensors/{modbusTcpDefinitionId}`
- **Summary:** Returns a collection of Modbus TCP numeric sensors.
- **Tags:** `ModbusTcpNumericSensors`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `modbusTcpDefinitionId` | `path` | `True` | `string(uuid)` | A Modbus TCP definition ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<ModbusTcpNumericSensorDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/setting/modbusTcpDefinitions/modbusTcpNumericSensors/{modbusTcpDefinitionId}`
- **Summary:** Creates a Modbus TCP numeric sensor.
- **Tags:** `ModbusTcpNumericSensors`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `modbusTcpDefinitionId` | `path` | `True` | `string(uuid)` | A Modbus TCP definition ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ModbusTcpNumericSensorDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/modbusTcpDefinitions/modbusTcpNumericSensors/{modbusTcpDefinitionId}/{modbusTcpNumericSensorId}`
- **Summary:** Updates a Modbus TCP numeric sensor.
- **Tags:** `ModbusTcpNumericSensors`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `modbusTcpDefinitionId` | `path` | `True` | `string(uuid)` | A Modbus TCP definition ID. |
| `modbusTcpNumericSensorId` | `path` | `True` | `string(uuid)` | A Modbus TCP numeric sensor ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ModbusTcpNumericSensorDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: ModbusTcpNumericSensorDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/setting/modbusTcpDefinitions/modbusTcpNumericSensors/{modbusTcpDefinitionId}/{modbusTcpNumericSensorId}`
- **Summary:** Deletes a Modbus TCP numeric sensor.
- **Tags:** `ModbusTcpNumericSensors`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `modbusTcpDefinitionId` | `path` | `True` | `string(uuid)` | A Modbus TCP definition ID. |
| `modbusTcpNumericSensorId` | `path` | `True` | `string(uuid)` | A Modbus TCP numeric sensor ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/modbusTcpDefinitions/{modbusTcpDefinitionId}`
- **Summary:** Returns a Modbus TCP definition.
- **Tags:** `ModbusTcpDefinitions`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `modbusTcpDefinitionId` | `path` | `True` | `string(uuid)` | A Modbus TCP definition ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: ModbusTcpDefinitionDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/modbusTcpDefinitions/{modbusTcpDefinitionId}`
- **Summary:** Updates a Modbus TCP definition.
- **Tags:** `ModbusTcpDefinitions`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `modbusTcpDefinitionId` | `path` | `True` | `string(uuid)` | A Modbus TCP definition ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ModbusTcpDefinitionDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/setting/modbusTcpDefinitions/{modbusTcpDefinitionId}`
- **Summary:** Deletes a Modbus TCP definition.
- **Tags:** `ModbusTcpDefinitions`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `modbusTcpDefinitionId` | `path` | `True` | `string(uuid)` | A Modbus TCP definition ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/notificationChannels`
- **Summary:** Returns a collection of notification channels.
- **Tags:** `NotificationChannels`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<NotificationChannelDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/setting/notificationChannels`
- **Summary:** Creates a notification channel and returns its ID.
- **Tags:** `NotificationChannels`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ModifiableNotificationChannelDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/notificationChannels/test`
- **Summary:** Verifies the notification channel webhook uri by attempting to send a test notification.
- **Tags:** `NotificationChannels`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ModifiableNotificationChannelDto` |
| `text/json` | `ModifiableNotificationChannelDto` |
| `application/*+json` | `ModifiableNotificationChannelDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: ChannelTestDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/notificationChannels/{id}`
- **Summary:** Updates a notification channel.
- **Tags:** `NotificationChannels`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A notification channel ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ModifiableNotificationChannelDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: ModifiableNotificationChannelDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/setting/notificationChannels/{id}`
- **Summary:** Deletes a notification channel.
- **Tags:** `NotificationChannels`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A notification channel ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/sensorThreshold`
- **Summary:** Retrieve a list of sensor threshold event settings.
- **Tags:** `SensorThreshold`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<SensorThresholdDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/setting/sensorThreshold`
- **Summary:** Creates an sensor threshold setting and returns its ID.
- **Tags:** `SensorThreshold`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `SensorThresholdDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/sensorThreshold/{sensorThresholdId}`
- **Summary:** Updates a sensor threshold setting.
- **Tags:** `SensorThreshold`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `sensorThresholdId` | `path` | `True` | `string(uuid)` | A sensor threshold ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `SensorThresholdDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/setting/sensorThreshold/{sensorThresholdId}`
- **Summary:** Deletes a sensor threshold.
- **Tags:** `SensorThreshold`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `sensorThresholdId` | `path` | `True` | `string(uuid)` | A sensor threshold ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/sensorThreshold/{sensorThresholdId}/enabledState`
- **Summary:** Updates a threshold enabled status.
- **Tags:** `SensorThreshold`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `sensorThresholdId` | `path` | `True` | `string(uuid)` | A sensor threshold ID. |
| `enabled` | `query` | `False` | `boolean` | A boolean indicating the sensor threshold enabled status. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/sensorTypeAssetType`
- **Summary:** Returns a list of sensor types.
- **Tags:** `SensorTypeAssetType`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetTypeId` | `query` | `False` | `AssetTypeEnum` | Optional asset type to filter what sensor type maps are returned. |
| `sensorTypeId` | `query` | `False` | `string(uuid)` | Optional sensor type ID to filter what sensor type maps are returned. |
| `sensorTypeValueType` | `query` | `False` | `SensorTypeValueType` | Optional sensor type value to filter what sensor types are returned. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<SensorTypeAssetTypeDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/serviceNowCmdbConfigurationOverview`
- **Summary:** Returns the ServiceNow configuration overview.
- **Tags:** `ServiceNowCmdbConfigurationOverview`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: ServiceNowCmdbConfigurationOverviewDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/serviceNowCmdbConfigurationOverview`
- **Summary:** Saves the ServiceNow configuration overview changes.
- **Tags:** `ServiceNowCmdbConfigurationOverview`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ServiceNowCmdbConfigurationOverviewDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/serviceNowCmdbConfigurationSchedule`
- **Summary:** Returns the ServiceNow configuration schedule.
- **Tags:** `ServiceNowCmdbConfigurationSchedule`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: ServiceNowCmdbConfigurationScheduleDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/serviceNowCmdbConfigurationSchedule`
- **Summary:** Saves the ServiceNow configuration schedule changes.
- **Tags:** `ServiceNowCmdbConfigurationSchedule`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ServiceNowCmdbConfigurationScheduleDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/serviceNowCmdbIntegration/initiateSync`
- **Summary:** Initiates a ServiceNow integration sync.
- **Tags:** `ServiceNowCmdbIntegration`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `202` | Accepted | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/serviceNowCmdbIntegration/resetLastSyncDate`
- **Summary:** Resets the ServiceNow integration last sync date.
- **Tags:** `ServiceNowCmdbIntegration`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/serviceNowCmdbIntegration/verifyAuthenticationConfiguration`
- **Summary:** Verifies the ServiceNow CMDB integration authentication configuration.
- **Tags:** `ServiceNowCmdbIntegration`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ServiceNowCmdbIntegrationAuthenticationDto` |
| `text/json` | `ServiceNowCmdbIntegrationAuthenticationDto` |
| `application/*+json` | `ServiceNowCmdbIntegrationAuthenticationDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/serviceNowCmdbIntegrationAssetType`
- **Summary:** Returns a collection of ServiceNow CMDB integration asset types.
- **Tags:** `ServiceNowCmdbIntegrationAssetType`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: ServiceNowCmdbIntegrationAssetTypeDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/serviceNowCmdbIntegrationAssetType`
- **Summary:** Saves the ServiceNow CMDB integration asset types.
- **Tags:** `ServiceNowCmdbIntegrationAssetType`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ServiceNowCmdbIntegrationAssetTypeDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/serviceNowCmdbIntegrationFacts`
- **Summary:** Returns a collection of ServiceNow CMDB integration fact settings.
- **Tags:** `ServiceNowCmdbIntegrationFacts`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<ServiceNowCmdbIntegrationFactsDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/serviceNowCmdbIntegrationFacts`
- **Summary:** Saves the ServiceNow CMDB integration fact settings.
- **Tags:** `ServiceNowCmdbIntegrationFacts`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `array<ServiceNowCmdbIntegrationFactsDto>` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/systemSettings`
- **Summary:** Returns a list of system settings.
- **Tags:** `SystemSettings`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `systemSettings` | `query` | `False` | `array<SystemSettingEnum>` | A list of system setting IDs. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<SystemSettingDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/systemSettings`
- **Summary:** Updates a list of system settings.
- **Tags:** `SystemSettings`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `array<SystemSettingDto>` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<SystemSettingDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/setting/systemSettings/dataCollector`
- **Summary:** Updates a data collector setting for all data collectors.
- **Tags:** `SystemSettings`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `DataCollectorSettingDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/systemSettings/dataCollector/{dataCollectorSetting}`
- **Summary:** Returns a data collector setting.
- **Tags:** `SystemSettings`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `dataCollectorSetting` | `path` | `True` | `DataCollectorSetting` | Name of data collector setting. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: DataCollectorSettingDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/setting/systemSettings/{systemSettingId}`
- **Summary:** Returns a system setting.
- **Tags:** `SystemSettings`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `systemSettingId` | `path` | `True` | `SystemSettingEnum` | ID of system setting. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: SystemSettingDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

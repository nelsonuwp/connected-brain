# Hyperview API Schema - `/api/asset`

Operations in this namespace: **203**

## `GET /api/asset/accessPolicies/{assetId}`
- **Summary:** Returns the access policy ID associated with an asset.
- **Tags:** `AccessPolicies`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/asset/accessPolicies/{assetId}`
- **Summary:** Updates an asset access policy and returns the updated asset access policy.
- **Tags:** `AccessPolicies`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `string(uuid)` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: AssetAccessPolicyDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/asset/alarmEvents/acknowledgementState/{alarmEventId}`
- **Summary:** Acknowledge or unacknowledge an alarm event.
- **Tags:** `AlarmEvents`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `alarmEventId` | `path` | `True` | `string(uuid)` | An alarm event's ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `AcknowledgementState` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/asset/alarmEvents/bulkAcknowledgementStates`
- **Summary:** Acknowledge or unacknowledge a list of alarm events.
- **Tags:** `AlarmEvents`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BulkUpdateAlarmEventsAcknowledgementStatesDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/asset/alarmEvents/bulkClose`
- **Summary:** Closes active alarm events.
- **Tags:** `AlarmEvents`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `True`
| Content-Type | Schema |
|---|---|
| `application/json` | `array<string(uuid)>` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/asset/alarmEvents/close/{alarmEventId}`
- **Summary:** Closes an active alarm event.
- **Tags:** `AlarmEvents`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `alarmEventId` | `path` | `True` | `string(uuid)` | An alarm event's ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/ancestors/{assetId}`
- **Summary:** Returns a list of asset ancestors.
- **Tags:** `Ancestors`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<AssetAncestorDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/assetChangeEventLogs`
- **Summary:** Returns a list of asset events.
- **Tags:** `AssetChangeEventLogs`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `query` | `False` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |
| `(after)` | `query` | `False` | `integer` | Return records after the specified number of records. |
| `(limit)` | `query` | `False` | `integer` | Number of records to return. |
| `(sort)` | `query` | `False` | `string` | Sort order. Format: "+|-fieldName". |
| `(filter)` | `query` | `False` | `string` | Cross field filter. Filters results that have the given value. |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<AssetChangeEventDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/assetDashboardSettings/{assetId}`
- **Summary:** Returns a dashboard setting for a specific asset.
- **Tags:** `AssetDashboardSettings`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: AssetDashboardSettingDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/asset/assetDashboardSettings/{assetId}`
- **Summary:** Saves asset dashboard setting and returns the updated asset dashboard setting.
- **Tags:** `AssetDashboardSettings`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ModifiableAssetDashboardSettingDto` |
| `text/json` | `ModifiableAssetDashboardSettingDto` |
| `application/*+json` | `ModifiableAssetDashboardSettingDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: ModifiableAssetDashboardSettingDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/asset/assetDashboardSettings/{assetId}`
- **Summary:** Deletes an asset dashboard setting.
- **Tags:** `AssetDashboardSettings`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/assetFirmware`
- **Summary:** Update assets to a firmware version.
- **Tags:** `AssetFirmware`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `FirmwareUpdateDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `202` | Accepted | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/assetProperties`
- **Summary:** Creates a new asset property and returns the new property.
- **Tags:** `AssetProperties`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `query` | `False` | `string(uuid)` | ID of the asset which owns this property. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `DisplayAssetPropertyDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: DisplayAssetPropertyDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/assetProperties/{id}`
- **Summary:** Returns a list of all properties for an asset.
- **Tags:** `AssetProperties`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<DisplayAssetPropertyDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/asset/assetProperties/{id}`
- **Summary:** Updates the value of asset property and returns the updated property.
- **Tags:** `AssetProperties`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | ID of the asset property to be updated. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `DisplayAssetPropertyDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: DisplayAssetPropertyDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/asset/assetProperties/{id}`
- **Summary:** Deletes a single asset property.
- **Tags:** `AssetProperties`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | ID of the asset property. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/assetProperties/{id}/{assetPropertyKey}`
- **Summary:** Returns an asset property for an asset.
- **Tags:** `AssetProperties`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | An asset ID. |
| `assetPropertyKey` | `path` | `True` | `AssetPropertyKeyEnum` | An asset property key. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: BaseAssetPropertyDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/assetPropertyValues/strings/{assetPropertyKey}`
- **Summary:** Retrieves an ordered list of all string values for the provided asset property key.
- **Tags:** `AssetPropertyValues`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetPropertyKey` | `path` | `True` | `AssetPropertyKeyEnum` | A asset property key. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<string>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/assetTrackerContainedAssets`
- **Summary:** Returns a list of AssetTracker assets or placeholder assets that are contained inside the
given AssetTracker parent.
- **Tags:** `AssetTrackerContainedAssets`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `parentId` | `query` | `False` | `string(uuid)` | A parent asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<IElevationContainedAssetDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/assetTrackerMasterModuleData`
- **Summary:** Retrieves all AssetTracker master module data.
- **Tags:** `AssetTrackerMasterModuleData`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<AssetTrackerMasterModuleDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/asset/assetTrackerMasterModuleData/{id}`
- **Summary:** Deletes an AssetTracker master module data.
- **Tags:** `AssetTrackerMasterModuleData`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | - |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/assetTree/{assetId}`
- **Summary:** Returns information about a particular asset for rendering it inside a tree view on the
application client.
- **Tags:** `AssetTree`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: AssetTreeNodeDataDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/assetTypeCount`
- **Summary:** Returns a list of asset type count.
- **Tags:** `AssetTypeCount`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<AssetTypeCountDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/assets`
- **Summary:** Returns a list of assets.
- **Tags:** `Assets`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetType` | `query` | `False` | `array<AssetTypeEnum>` | An optional list of asset types to filter what assets are returned. |
| `includeDimensions` | `query` | `False` | `boolean` | An optional flag for including dimensional properties. |
| `api-version` | `header` | `False` | `string` | - |
| `(after)` | `query` | `False` | `integer` | Return records after the specified number of records. |
| `(limit)` | `query` | `False` | `integer` | Number of records to return. |
| `(sort)` | `query` | `False` | `string` | Sort order. Format: "+|-fieldName". |
| `(filter)` | `query` | `False` | `string` | Cross field filter. Filters results that have the given value. |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<AssetDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/assets`
- **Summary:** Creates an asset and returns its ID.
- **Tags:** `Assets`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `CreatableAssetDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/assets/{id}`
- **Summary:** Returns an individual asset.
- **Tags:** `Assets`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: AssetDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/asset/assets/{id}`
- **Summary:** Updates an asset and returns the updated asset.
- **Tags:** `Assets`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `AssetDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: AssetDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/asset/assets/{id}`
- **Summary:** Deletes an asset.
- **Tags:** `Assets`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/availableFirmwareVersions/{assetId}`
- **Summary:** Returns a list of all firmware versions available for the given asset.
- **Tags:** `AvailableFirmwareVersions`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<AssetFirmwareVersionDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/availablePowerSources/buswayTapOffs/{id}`
- **Summary:** Returns available busway tap offs.
- **Tags:** `AvailablePowerSources`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<AvailableBuswayTapOffDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/availablePowerSources/outlets/{id}`
- **Summary:** Returns available outlets for a given asset ID.
- **Tags:** `AvailablePowerSources`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<OutletDtoBase>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/availablePowerSources/pduBreakers/{id}`
- **Summary:** Returns available PDU breakers.
- **Tags:** `AvailablePowerSources`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<AvailablePduBreakerDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/availableRackSpace/{id}`
- **Summary:** Returns available rack space
- **Tags:** `AvailableRackSpace`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A rack id. |
| `assetId` | `query` | `False` | `string(uuid)` | An asset ID to ignore if it is in the given rack. |
| `rackSide` | `query` | `False` | `RackSide` | A flag to indicate which side of the rack to get available rack space from. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<AvailableRackSpaceDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/availableRackSpace/{id}/sensors/{sensorId}`
- **Summary:** Returns an array of what space there is available in a rack to place a sensor.
- **Tags:** `AvailableRackSpace`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A rack id. |
| `sensorId` | `path` | `True` | `string(uuid)` | A sensor id. |
| `rackSide` | `query` | `True` | `RackSide` | A flag to indicate which side of the rack to get grab sensors from. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<AvailableRackSpaceDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/bulk/assets/addDocumentAssociation`
- **Summary:** Add associations between a single document and many assets.
- **Tags:** `Bulk`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BulkDocumentAssociationActionDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `202` | Accepted | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/bulk/assets/addPatchPanelPhysicalPort`
- **Summary:** Adds a single physical network port to multiple patch panels.
- **Tags:** `Bulk`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BulkAddPatchPanelPhysicalPortActionDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `202` | Accepted | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/bulk/assets/addPatchPanelPhysicalPorts`
- **Summary:** Adds multiple physical network ports to multiple patch panels.
- **Tags:** `Bulk`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BulkAddPatchPanelPhysicalPortsActionDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `202` | Accepted | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/bulk/assets/addPhysicalPort`
- **Summary:** Adds a single physical network port to multiple assets.
- **Tags:** `Bulk`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BulkAddPhysicalPortActionDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `202` | Accepted | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/bulk/assets/addPhysicalPorts`
- **Summary:** Adds multiple physical network ports to multiple assets.
- **Tags:** `Bulk`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BulkAddPhysicalPortsActionDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `202` | Accepted | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/bulk/assets/cancelMuteAlarmEventNotifications`
- **Summary:** Cancels muted alarm event notifications for many assets.
- **Tags:** `Bulk`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BulkAssetActionDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `202` | Accepted | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/bulk/assets/createEventNotificationRecipient`
- **Summary:** Creates asset notification recipients between the requesting user and many assets.
- **Tags:** `Bulk`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BulkAssetActionDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `202` | Accepted | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/bulk/assets/delete`
- **Summary:** Deletes a set of assets.
- **Tags:** `Bulk`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BulkAssetActionDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `202` | Accepted | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/bulk/assets/disableMonitoring`
- **Summary:** Disable monitoring for a set of assets.
- **Tags:** `Bulk`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BulkAssetActionDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `202` | Accepted | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/bulk/assets/enableMonitoring`
- **Summary:** Enable monitoring for a set of assets.
- **Tags:** `Bulk`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BulkAssetActionDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `202` | Accepted | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/bulk/assets/muteAlarmEventNotifications`
- **Summary:** Mutes alarm event notifications for many assets.
- **Tags:** `Bulk`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BulkMuteAlarmEventNotificationsActionDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `202` | Accepted | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/bulk/assets/removeDocumentAssociation`
- **Summary:** Remove associations between a single document and many assets.
- **Tags:** `Bulk`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BulkDocumentAssociationActionDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `202` | Accepted | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/bulk/assets/removeEventNotificationRecipient`
- **Summary:** Remove asset notification recipients between the requesting user and many assets.
- **Tags:** `Bulk`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BulkAssetActionDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `202` | Accepted | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/bulk/assets/updateAccessPolicy`
- **Summary:** Updates associations between a single access policy and many assets.
- **Tags:** `Bulk`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BulkUpdateAssetAccessPolicyDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `202` | Accepted | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/bulk/assets/updateAssetProperty`
- **Summary:** Updates an asset property for a set of assets.
- **Tags:** `Bulk`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BulkUpdateAssetPropertyActionDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `202` | Accepted | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/bulk/assets/updateAssetsControlDataCollectorAssociation`
- **Summary:** Updates control operations data collector associations for a set of assets.
- **Tags:** `Bulk`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BulkUpdateAssetsControlDataCollectorActionDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `202` | Accepted | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/bulk/assets/updateBusinessEntityAssociation`
- **Summary:** Updates business entity association for many assets.
- **Tags:** `Bulk`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BulkUpdateBusinessEntityAssociationActionDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `202` | Accepted | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/bulk/assets/updateControlCredentials`
- **Summary:** Updates the associations between a control credential and many assets.
- **Tags:** `Bulk`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BulkUpdateControlCredentialsActionDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `202` | Accepted | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/bulk/assets/updateCustomProperty`
- **Summary:** Updates a custom property for a set of assets.
- **Tags:** `Bulk`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BulkUpdateCustomPropertyActionDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `202` | Accepted | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/bulk/assets/updateDescendantsAccessPolicies`
- **Summary:** Updates the access policy for an asset's descendants.
- **Tags:** `Bulk`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BulkUpdateDescendantsAccessPoliciesActionDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `202` | Accepted | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/bulk/assets/updateFirmwareControlCredentials`
- **Summary:** Updates the associations between a firmware credential and many assets.
- **Tags:** `Bulk`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BulkUpdateFirmwareControlCredentialsActionDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `202` | Accepted | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/bulk/assets/updateLifecycle`
- **Summary:** Updates life cycle properties for a set of assets.
- **Tags:** `Bulk`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BulkUpdateLifecycleActionDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `202` | Accepted | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/bulk/assets/updatePhysicalPortNames`
- **Summary:** Updates physical network port names.
- **Tags:** `Bulk`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BulkUpdatePhysicalPortNamesActionDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `202` | Accepted | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/bulk/assets/updateProduct`
- **Summary:** Updates associations between a single product and many assets.
- **Tags:** `Bulk`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BulkUpdateProductDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `202` | Accepted | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/bulk/sensors/delete`
- **Summary:** Deletes multiple sensors.
- **Tags:** `Bulk`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BulkSensorActionDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `202` | Accepted | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/bulk/sensors/resetAccessPolicy`
- **Summary:** Resets access policy for multiple sensors.
- **Tags:** `Bulk`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BulkSensorActionDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `202` | Accepted | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/bulk/sensors/updateAccessPolicy`
- **Summary:** Updates associations between a single access policy and many sensors.
- **Tags:** `Bulk`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BulkUpdateSensorAccessPolicyDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `202` | Accepted | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/businessEntities`
- **Summary:** Creates a business entity and returns its ID.
- **Tags:** `BusinessEntities`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ModifiableBusinessEntityDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/businessEntities/{id}`
- **Summary:** Returns an individual business entity.
- **Tags:** `BusinessEntities`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A business entity ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: BusinessEntityDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/asset/businessEntities/{id}`
- **Summary:** Updates a business entity.
- **Tags:** `BusinessEntities`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A business entity ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ModifiableBusinessEntityDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: ModifiableBusinessEntityDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/asset/businessEntities/{id}`
- **Summary:** Deletes a business entity.
- **Tags:** `BusinessEntities`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A business entity ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/businessEntityAddresses`
- **Summary:** Creates a business entity address and returns its ID.
- **Tags:** `BusinessEntityAddresses`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BusinessEntityAddressDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/businessEntityAddresses/{businessEntityId}`
- **Summary:** Returns a list of addresses for a given Business Entity.
- **Tags:** `BusinessEntityAddresses`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `businessEntityId` | `path` | `True` | `string(uuid)` | A Business Entity ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<BusinessEntityAddressDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/asset/businessEntityAddresses/{id}`
- **Summary:** Updates a business entity address.
- **Tags:** `BusinessEntityAddresses`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A business entity address ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BusinessEntityAddressDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: BusinessEntityAddressDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/asset/businessEntityAddresses/{id}`
- **Summary:** Deletes a business entity address.
- **Tags:** `BusinessEntityAddresses`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A business entity address ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/asset/businessEntityAssociations/asset/{assetId}`
- **Summary:** Removes a business entity association from an asset.
- **Tags:** `BusinessEntityAssociations`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/businessEntityContacts`
- **Summary:** Creates a business entity contact and returns its ID.
- **Tags:** `BusinessEntityContacts`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BusinessEntityContactDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/businessEntityContacts/{businessEntityId}`
- **Summary:** Returns a list of contacts for a given Business Entity.
- **Tags:** `BusinessEntityContacts`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `businessEntityId` | `path` | `True` | `string(uuid)` | A Business Entity ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<BusinessEntityContactDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/asset/businessEntityContacts/{id}`
- **Summary:** Updates a business entity contact.
- **Tags:** `BusinessEntityContacts`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A business entity contact ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BusinessEntityContactDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: BusinessEntityContactDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/asset/businessEntityContacts/{id}`
- **Summary:** Deletes a business entity contact.
- **Tags:** `BusinessEntityContacts`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A business entity contact ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/buswayTapOff`
- **Summary:** Creates a new busway tap off.
- **Tags:** `BuswayTapOff`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `CreatableBuswayTapOffDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/buswayTapOff/{assetId}`
- **Summary:** Returns a list of busway tap offs.
- **Tags:** `BuswayTapOff`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<BuswayTapOffDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/asset/buswayTapOff/{buswayTapOffId}`
- **Summary:** Updates a busway tap off.
- **Tags:** `BuswayTapOff`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `buswayTapOffId` | `path` | `True` | `string(uuid)` | A busway tap off ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BuswayTapOffEditDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: BuswayTapOffEditDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/asset/buswayTapOff/{buswayTapOffId}`
- **Summary:** Deletes a new busway tap off.
- **Tags:** `BuswayTapOff`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `buswayTapOffId` | `path` | `True` | `string(uuid)` | A busway tap off ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/circuitConnections`
- **Summary:** Adds physical connections to a circuit.
- **Tags:** `CircuitConnections`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `CircuitConnectionAssociationDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: array<string(uuid)>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/asset/circuitConnections/{circuitId}/connections/{connectionId}`
- **Summary:** Removes a connection from a circuit.
- **Tags:** `CircuitConnections`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `circuitId` | `path` | `True` | `string(uuid)` | ID of the circuit. |
| `connectionId` | `path` | `True` | `string(uuid)` | ID of the connection. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/circuitConnections/{id}`
- **Summary:** Returns all physical connections associated with a circuit.
- **Tags:** `CircuitConnections`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A circuit ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<PhysicalConnectionDetailedDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/circuits`
- **Summary:** Creates a circuit and returns its ID.
- **Tags:** `Circuits`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ModifiableCircuitDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/circuits/{id}`
- **Summary:** Returns an individual circuit.
- **Tags:** `Circuits`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A circuit ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: CircuitDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/asset/circuits/{id}`
- **Summary:** Updates a circuit.
- **Tags:** `Circuits`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A circuit ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ModifiableCircuitDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: ModifiableCircuitDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/asset/circuits/{id}`
- **Summary:** Deletes a circuit.
- **Tags:** `Circuits`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A circuit ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/componentAssets/{assetId}`
- **Summary:** Returns a list of component assets for a given parent asset.
- **Tags:** `ComponentAssets`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `includeAssetTypes` | `query` | `False` | `array<AssetTypeEnum>` | Optional list of included asset types. |
| `excludeAssetTypes` | `query` | `False` | `array<AssetTypeEnum>` | Optional list of excluded asset types. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<ComponentAssetDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/componentAssets/{assetId}/networkComponents`
- **Summary:** Returns a list of network component assets for a given parent asset.
- **Tags:** `ComponentAssets`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `includeAssetTypes` | `query` | `False` | `array<AssetTypeEnum>` | Optional list of included asset types. |
| `excludeAssetTypes` | `query` | `False` | `array<AssetTypeEnum>` | Optional list of excluded asset types. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<ComponentAssetDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/componentAssets/{assetId}/virtualComponents`
- **Summary:** Returns a list of virtual component assets for a given parent asset.
- **Tags:** `ComponentAssets`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `includeAssetTypes` | `query` | `False` | `array<AssetTypeEnum>` | Optional list of included asset types. |
| `excludeAssetTypes` | `query` | `False` | `array<AssetTypeEnum>` | Optional list of excluded asset types. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<VirtualComponentAssetDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/containedAssets/elevation/{parentId}`
- **Summary:** Returns a list of assets or placeholder assets that are contained inside the given parent.
- **Tags:** `ContainedAssets`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `parentId` | `path` | `True` | `string(uuid)` | A parent asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<IElevationContainedAssetDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/control/rackDoorElectronicLock`
- **Summary:** Controls the electronic lock of a rack door.
- **Tags:** `Control`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `RackDoorElectronicLockControlDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `202` | Accepted | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/controlDataCollector/{assetId}`
- **Summary:** Returns an asset's control operation data collector ID.
- **Tags:** `ControlDataCollector`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/asset/controlOperations`
- **Summary:** Update asset's control operations settings.
- **Tags:** `ControlOperations`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ModifiableControlOperationDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `202` | Accepted | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/controlOperations/configuration/{assetId}`
- **Summary:** Returns an asset's control operation configuration.
- **Tags:** `ControlOperations`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: ControlOperationConfigurationDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/controlOperations/{assetId}`
- **Summary:** Returns an asset's control operation settings.
- **Tags:** `ControlOperations`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<ControlOperationDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/customAssetProperties/{id}`
- **Summary:** Returns a list of all custom properties for an asset.
- **Tags:** `CustomAssetProperties`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<CustomAssetPropertyDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/asset/customAssetProperties/{id}`
- **Summary:** Updates the value of custom asset property and returns the updated property.
- **Tags:** `CustomAssetProperties`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | ID of the custom asset property to be updated. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ModifiableCustomAssetPropertyDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: CustomAssetPropertyDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/asset/customAssetProperties/{id}`
- **Summary:** Deletes a single custom asset property.
- **Tags:** `CustomAssetProperties`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | ID of the custom asset property. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/customAssetProperties/{id}/children/customPropertyValue`
- **Summary:** Returns a list of custom asset property values for all accessible children of an asset.
- **Tags:** `CustomAssetProperties`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | An asset ID. |
| `customAssetPropertyKeyId` | `query` | `True` | `string(uuid)` | A custom asset property key ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<LayoutCustomAssetPropertyDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/customAssetProperties/{id}/customPropertyValue`
- **Summary:** Returns a single custom asset property value for an asset.
- **Tags:** `CustomAssetProperties`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | An asset ID. |
| `customAssetPropertyKeyId` | `query` | `True` | `string(uuid)` | A custom asset property key ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: LayoutCustomAssetPropertyDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/customComponents`
- **Summary:** Creates a custom component and returns its ID.
- **Tags:** `CustomComponents`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `CustomComponentDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/customComponents/assetPropertyValueStrings`
- **Summary:** Returns a list of asset property value strings.
- **Tags:** `CustomComponents`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetPropertyKey` | `query` | `True` | `AssetPropertyKeyEnum` | An asset property key. |
| `searchValue` | `query` | `True` | `string` | A search value. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<string>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/asset/customComponents/{id}`
- **Summary:** Updates a custom component and returns the updated custom component.
- **Tags:** `CustomComponents`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A custom component ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `CustomComponentDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: CustomComponentDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/asset/customComponents/{id}`
- **Summary:** Deletes a custom component.
- **Tags:** `CustomComponents`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A custom component ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/dataCollectors/{assetId}`
- **Summary:** Returns an asset's associated data collectors.
- **Tags:** `DataCollectors`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<AssetDataCollectorDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/directSensorMap`
- **Summary:** Creates a direct sensor map and returns its ID.
- **Tags:** `DirectSensorMap`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `DirectSensorMapDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/asset/directSensorMap/{sensorId}`
- **Summary:** Deletes a direct sensor map.
- **Tags:** `DirectSensorMap`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `sensorId` | `path` | `True` | `string(uuid)` | ID of the sensor. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/discoveryReport/{assetId}`
- **Summary:** Returns Asset Discovery Report.
- **Tags:** `DiscoveryReport`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<AssetDiscoveryReportDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/documentAssociations`
- **Summary:** Creates an association between an asset and a document.
- **Tags:** `DocumentAssociations`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `AssetDocumentDetailAssociationDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/documentAssociations/assets/{documentId}`
- **Summary:** Returns a list of associated assets for a document.
- **Tags:** `DocumentAssociations`
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
| `200` | OK | `application/json: array<DocumentAssociatedAssetDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/documentAssociations/documentDetails/{assetId}`
- **Summary:** Returns a collection of associated document details for an asset.
- **Tags:** `DocumentAssociations`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<AssetDocumentDetailDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/asset/documentAssociations/{assetDocumentAssociationId}`
- **Summary:** Removes an association between an asset and a document.
- **Tags:** `DocumentAssociations`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetDocumentAssociationId` | `path` | `True` | `string(uuid)` | Asset Document Association ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/enumAssetProperties/{id}`
- **Summary:** Returns a list of all enum values for a given enum ID.
- **Tags:** `EnumAssetProperties`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `AssetPropertyKeyEnum` | The ID of an enum. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<AssetPropertyEnumValueDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/eventNotificationRecipient/{assetId}`
- **Summary:** Retrieves an asset notification recipient for the requesting user and a given asset.
- **Tags:** `EventNotificationRecipient`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: AssetNotificationRecipientDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/eventNotificationRecipient/{assetId}`
- **Summary:** Creates an asset notification recipient for the requesting user and a given asset.
- **Tags:** `EventNotificationRecipient`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/asset/eventNotificationRecipient/{assetId}`
- **Summary:** Remove an asset notification recipient for the requesting user and a given asset.
- **Tags:** `EventNotificationRecipient`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/hierarchy`
- **Summary:** Returns a list of assets that includes placeholder ancestor assets.
- **Tags:** `Hierarchy`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `parentId` | `query` | `False` | `string(uuid)` | A nullable parent asset ID. |
| `assetType` | `query` | `False` | `array<AssetTypeEnum>` | An optional list of asset types to filter what assets are returned. |
| `hasChildrenAssetType` | `query` | `False` | `array<AssetTypeEnum>` | An optional list of asset types to filter what assets are used when determining if an asset has children. |
| `includeDimensions` | `query` | `False` | `boolean` | An optional flag for including dimensional properties. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<IAssetHierarchyDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/indirectSensors`
- **Summary:** Creates an indirect sensor link and returns its ID.
- **Tags:** `IndirectSensors`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `IndirectSensorDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/asset/indirectSensors/{sensorId}`
- **Summary:** Deletes an indirect sensor link.
- **Tags:** `IndirectSensors`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `sensorId` | `path` | `True` | `string(uuid)` | ID of the sensor. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/lifecycleProperties/{assetId}`
- **Summary:** Returns Asset Lifecycle Properties for Asset ID.
- **Tags:** `LifecycleProperties`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: AssetLifecyclePropertiesDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/asset/lifecycleProperties/{assetId}`
- **Summary:** Update Asset Lifecycle Properties for Asset ID.
- **Tags:** `LifecycleProperties`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `AssetLifecyclePropertiesDto` |
| `text/json` | `AssetLifecyclePropertiesDto` |
| `application/*+json` | `AssetLifecyclePropertiesDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: AssetLifecyclePropertiesDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/asset/location/{id}`
- **Summary:** Updates the location of an asset.
- **Tags:** `Location`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | The ID of the asset that will be moved. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `UpdatableLocationDataDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: LocationDataDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/manualSensors`
- **Summary:** Creates one or many manual sensors.
- **Tags:** `ManualSensors`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `CreatableManualSensorDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: array<string(uuid)>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/asset/manualSensors/numericSensor/{sensorId}/value`
- **Summary:** Updates a numeric manual sensor value.
- **Tags:** `ManualSensors`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `sensorId` | `path` | `True` | `string(uuid)` | A numeric sensor ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `True`
| Content-Type | Schema |
|---|---|
| `application/json` | `number(double)` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/merge`
- **Summary:** Merges a source asset into a destination asset.
- **Tags:** `Merge`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `MergeSpecificationDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/monitorOnlyCommunicationSetting/{assetId}`
- **Summary:** Returns the monitoring profile for a given asset.
- **Tags:** `MonitorOnlyCommunicationSetting`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: SensorMonitoringProfileDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/asset/monitorOnlyCommunicationSetting/{assetId}`
- **Summary:** Updates or creates the monitoring profile for an asset.
- **Tags:** `MonitorOnlyCommunicationSetting`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `SensorMonitoringProfileDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: SensorMonitoringProfileDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/monitorOnlyCommunicationSetting/{assetId}/refreshSensors`
- **Summary:** Refreshes the asset monitoring sensors for a given asset from "monitor only" definitions.
- **Tags:** `MonitorOnlyCommunicationSetting`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/muteAlarmEventNotifications`
- **Summary:** Mutes alarm event notifications for a specific asset.
- **Tags:** `MuteAlarmEventNotifications`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `MuteAlarmEventNotificationsSettingDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/asset/muteAlarmEventNotifications/{id}`
- **Summary:** Cancels a mute alarm event notification setting for a specific asset.
- **Tags:** `MuteAlarmEventNotifications`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/networkHosts/{assetId}`
- **Summary:** Returns a collection of network host information.
- **Tags:** `NetworkHosts`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<NetworkHostDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/outlets`
- **Summary:** Gets a list of outlets.
- **Tags:** `Outlets`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `query` | `False` | `string(uuid)` | Asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<OutletDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/outletsControl`
- **Summary:** Performs a bulk control operation on outlets.
- **Tags:** `OutletsControl`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BulkOutletControlDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `202` | Accepted | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/pduBreakers`
- **Summary:** Gets a list of PDU breakers.
- **Tags:** `PduBreakers`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `query` | `False` | `string(uuid)` | Asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<PduBreakerDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/asset/pduBreakers/breakerStatus/{pduBreakerId}`
- **Summary:** Updates a PDU breaker status.
- **Tags:** `PduBreakers`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `pduBreakerId` | `path` | `True` | `string(uuid)` | PDU breaker ID. |
| `breakerStatusEnumId` | `query` | `False` | `string(uuid)` | PDU breaker status property |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/asset/pduBreakers/{pduBreakerId}`
- **Summary:** Updates a PDU breaker
- **Tags:** `PduBreakers`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `pduBreakerId` | `path` | `True` | `string(uuid)` | PDU breaker ID |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `PduEditBreakerDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/physicalConnections`
- **Summary:** Creates a physical connection and returns its ID.
- **Tags:** `PhysicalConnections`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ModifiablePhysicalConnectionDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/physicalConnections/{id}`
- **Summary:** Returns an individual physical connection.
- **Tags:** `PhysicalConnections`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A physical connection ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: PhysicalConnectionDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/asset/physicalConnections/{id}`
- **Summary:** Updates a physical connection.
- **Tags:** `PhysicalConnections`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A physical connection ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ModifiablePhysicalConnectionDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: ModifiablePhysicalConnectionDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/asset/physicalConnections/{id}`
- **Summary:** Deletes a physical connection.
- **Tags:** `PhysicalConnections`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A physical connection ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/physicalPorts`
- **Summary:** Creates a physical port and returns its ID.
- **Tags:** `PhysicalPorts`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ModifiablePhysicalPortDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/physicalPorts/detailed/{assetId}`
- **Summary:** Returns a list of physical ports with connection information.
- **Tags:** `PhysicalPorts`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<PhysicalPortDetailedRetrievalDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/physicalPorts/multiple`
- **Summary:** Creates multiple physical ports.
- **Tags:** `PhysicalPorts`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `MultipleCreatablePhysicalPortDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/asset/physicalPorts/multiple`
- **Summary:** Updates multiple physical ports for a given device.
- **Tags:** `PhysicalPorts`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `MultiplePhysicalPortUpdateDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: MultiplePhysicalPortUpdateDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/asset/physicalPorts/multiple`
- **Summary:** Deletes physical ports.
- **Tags:** `PhysicalPorts`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `MultiplePhysicalPortsDeleteDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/physicalPorts/patchPanel`
- **Summary:** Creates a physical port for a patch panel and returns its ID.
- **Tags:** `PhysicalPorts`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ModifiablePatchPanelPhysicalPortDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/physicalPorts/patchPanel/multiple`
- **Summary:** Creates multiple physical ports for a patch panel.
- **Tags:** `PhysicalPorts`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `MultipleCreatablePatchPanelPhysicalPortDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/asset/physicalPorts/patchPanel/multiple`
- **Summary:** Updates multiple physical ports for a given patch panel.
- **Tags:** `PhysicalPorts`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `MultiplePatchPanelPhysicalPortUpdateDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: MultiplePatchPanelPhysicalPortUpdateDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/asset/physicalPorts/patchPanel/{id}`
- **Summary:** Updates a patch panel physical port.
- **Tags:** `PhysicalPorts`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A patch panel physical port ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ModifiablePatchPanelPhysicalPortDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: ModifiablePatchPanelPhysicalPortDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/physicalPorts/{id}`
- **Summary:** Returns a list of physical ports.
- **Tags:** `PhysicalPorts`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<PhysicalPortGenericRetrievalDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/asset/physicalPorts/{id}`
- **Summary:** Updates a physical port.
- **Tags:** `PhysicalPorts`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A physical port ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ModifiablePhysicalPortDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: ModifiablePhysicalPortDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/asset/physicalPorts/{id}`
- **Summary:** Deletes a physical port.
- **Tags:** `PhysicalPorts`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A physical port ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/powerPath/{assetId}/ancestry`
- **Summary:** Returns the power path ancestry of power providing assets and associations down to the given asset.
- **Tags:** `PowerPath`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: PowerPathAncestryDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/powerPath/{assetId}/children`
- **Summary:** Returns a list of assets that are directly receiving power from the given asset.
- **Tags:** `PowerPath`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<IPowerPathAssetDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/powerSourceAssociations`
- **Summary:** Returns a list of power associations of a powered asset.
- **Tags:** `PowerSourceAssociations`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `providingSourceAssetId` | `query` | `False` | `string(uuid)` | An optional ID of the power providing asset. |
| `consumingDestinationAssetId` | `query` | `False` | `string(uuid)` | An optional ID of the power consuming asset. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<PowerAssociationDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/powerSourceAssociations`
- **Summary:** Creates a new power source association.
- **Tags:** `PowerSourceAssociations`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `PowerAssociationDtoBase` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/asset/powerSourceAssociations/{id}`
- **Summary:** Deletes a power association.
- **Tags:** `PowerSourceAssociations`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | ID of the power association. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/rackPanel`
- **Summary:** Creates multiple panel assets for a given rack and rack side.
- **Tags:** `RackPanel`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `MultipleCreatableRackPanelDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/asset/rackPanel/{assetId}/blankingPanels`
- **Summary:** Deletes blanking panels.
- **Tags:** `RackPanel`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `True`
| Content-Type | Schema |
|---|---|
| `application/json` | `array<string(uuid)>` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/asset/rackPanel/{assetId}/cableManagement`
- **Summary:** Deletes cable management assets.
- **Tags:** `RackPanel`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `True`
| Content-Type | Schema |
|---|---|
| `application/json` | `array<string(uuid)>` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/asset/rackPanel/{id}`
- **Summary:** Updates a rack panel assets.
- **Tags:** `RackPanel`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `AssetDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: AssetDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/rackSecurity/{assetId}`
- **Summary:** Returns rack security sensors for the given rack.
- **Tags:** `RackSecurity`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | A rack ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<RackSecuritySensorDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/rackSecurity/{locationId}/racks`
- **Summary:** Returns all rack security sensors contained in a specific location.
- **Tags:** `RackSecurity`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `locationId` | `path` | `True` | `string(uuid)` | A location ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<RackSecuritySensorDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/asset/rackShelf/{id}`
- **Summary:** Updates an asset and returns the updated asset.
- **Tags:** `RackShelf`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `AssetDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: AssetDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/savedSearches`
- **Summary:** Returns a list of saved searches for the current user.
- **Tags:** `SavedSearches`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<SavedSearchDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/savedSearches`
- **Summary:** Creates a saved search and returns its ID.
- **Tags:** `SavedSearches`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `SavedSearchDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/savedSearches/global`
- **Summary:** Returns a list of global saved searches.
- **Tags:** `SavedSearches`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<SavedSearchDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/asset/savedSearches/global/{id}`
- **Summary:** Deletes a global saved search.
- **Tags:** `SavedSearches`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A saved search ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/asset/savedSearches/user/{id}`
- **Summary:** Deletes a user saved search.
- **Tags:** `SavedSearches`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A saved search ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/search`
- **Summary:** Returns a list of assets that meet the requested criteria.
- **Tags:** `Search`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `SearchQuery` |
| `text/json` | `SearchQuery` |
| `application/*+json` | `SearchQuery` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: object` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/asset/sensors`
- **Summary:** Updates a sensor.
- **Tags:** `Sensors`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `SensorUpdateDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/sensors/simpleDirect/{assetId}`
- **Summary:** Returns a simple collection of direct asset sensors.
- **Tags:** `Sensors`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `sensorTypeIds` | `query` | `False` | `array<string(uuid)>` | An optional list of sensor types to filter what sensors are returned. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<SimpleDirectAssetSensorDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/sensors/{assetId}`
- **Summary:** Returns a list of asset sensors.
- **Tags:** `Sensors`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `sensorTypeIds` | `query` | `False` | `array<string(uuid)>` | An optional list of sensor types to filter what sensors are returned. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<AssetSensorDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/asset/sensors/{id}`
- **Summary:** Deletes a sensor.
- **Tags:** `Sensors`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A sensor ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/sensorsDailySummaries/numeric`
- **Summary:** Returns a list of numeric sensor daily summaries for each provided sensor ID for a specific
UTC time range.
- **Tags:** `SensorsDailySummaries`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `sensorIds` | `query` | `True` | `array<string(uuid)>` | A list of sensor IDs. |
| `startTime` | `query` | `False` | `string(date-time)` | The start time. |
| `endTime` | `query` | `False` | `string(date-time)` | The end time. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<NumericSensorDailySummariesDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/sensorsDailySummaries/numeric/{timeRange}`
- **Summary:** Returns a list of numeric sensor daily summaries for each provided sensor ID for a given
time range option.
- **Tags:** `SensorsDailySummaries`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `sensorIds` | `query` | `True` | `array<string(uuid)>` | A list of sensor IDs. |
| `timeRange` | `path` | `True` | `SensorDailySummaryTimeRange` | A time range for the data. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<NumericSensorDailySummariesDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/sensorsDailySummaries/string`
- **Summary:** Returns a list of string sensor daily summaries for each provided sensor ID for a specific
UTC time range.
- **Tags:** `SensorsDailySummaries`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `sensorIds` | `query` | `True` | `array<string(uuid)>` | A list of sensor IDs. |
| `startTime` | `query` | `False` | `string(date-time)` | The start time. |
| `endTime` | `query` | `False` | `string(date-time)` | The end time. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<StringSensorDailySummariesDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/sensorsDailySummaries/string/{timeRange}`
- **Summary:** Returns a list of string sensor daily summaries for each provided sensor ID for a given time
range option.
- **Tags:** `SensorsDailySummaries`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `sensorIds` | `query` | `True` | `array<string(uuid)>` | A list of sensor IDs. |
| `timeRange` | `path` | `True` | `SensorDailySummaryTimeRange` | A time range for the data. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<StringSensorDailySummariesDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/sensorsDataPoints/numeric`
- **Summary:** Returns a list of numeric sensor data points for each provided sensor ID for a specific UTC
time range.
- **Tags:** `SensorsDataPoints`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `sensorIds` | `query` | `True` | `array<string(uuid)>` | A list of sensor IDs. |
| `startTime` | `query` | `False` | `string(date-time)` | The start time. |
| `endTime` | `query` | `False` | `string(date-time)` | The end time. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<NumericSensorDataPointsDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/sensorsDataPoints/numeric/{timeRange}`
- **Summary:** Returns a list of numeric sensor data points for each provided sensor ID for a given time
range option.
- **Tags:** `SensorsDataPoints`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `sensorIds` | `query` | `True` | `array<string(uuid)>` | A list of sensor IDs. |
| `timeRange` | `path` | `True` | `SensorDataPointTimeRange` | A time range for the data. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<NumericSensorDataPointsDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/sensorsDataPoints/string`
- **Summary:** Returns a list of string sensor data points for each provided sensor ID for a specific UTC
time range.
- **Tags:** `SensorsDataPoints`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `sensorIds` | `query` | `True` | `array<string(uuid)>` | A list of sensor IDs. |
| `startTime` | `query` | `False` | `string(date-time)` | The start time. |
| `endTime` | `query` | `False` | `string(date-time)` | The end time. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<StringSensorDataPointsDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/sensorsDataPoints/string/{timeRange}`
- **Summary:** Returns a list of string sensor data points for each provided sensor ID for a given time
range option.
- **Tags:** `SensorsDataPoints`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `sensorIds` | `query` | `True` | `array<string(uuid)>` | A list of sensor IDs. |
| `timeRange` | `path` | `True` | `SensorDataPointTimeRange` | A time range for the data. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<StringSensorDataPointsDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/shelvedAssets/{rackId}`
- **Summary:** Returns a list of assets that are in shelves of a given rack.
- **Tags:** `ShelvedAssets`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `rackId` | `path` | `True` | `string(uuid)` | A rack ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<AssetDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/software/{id}`
- **Summary:** Retrieves all software for an asset.
- **Tags:** `Software`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |
| `(after)` | `query` | `False` | `integer` | Return records after the specified number of records. |
| `(limit)` | `query` | `False` | `integer` | Number of records to return. |
| `(sort)` | `query` | `False` | `string` | Sort order. Format: "+|-fieldName". |
| `(filter)` | `query` | `False` | `string` | Cross field filter. Filters results that have the given value. |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<AssetSoftwareDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/watchedAssets`
- **Summary:** Returns a list of user watched assets for notifications.
- **Tags:** `WatchedAssets`
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
| `200` | OK | `application/json: array<WatchedAssetDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/webInterfaceAddress/{assetId}`
- **Summary:** Returns the web interface address.
- **Tags:** `WebInterfaceAddress`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: string` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/widget/assetLifecycleWidget/{assetId}`
- **Summary:** Returns names and values for the AssetLifecycleWidget.
- **Tags:** `Widget`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<NameValueWidgetDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/widget/assetNetworkWidgetIpAddress/{assetId}`
- **Summary:** Returns a collection of network widget IP address information.
- **Tags:** `Widget`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<NetworkWidgetIpAddressDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/widget/assetPropertyListWidget/{assetId}`
- **Summary:** Returns property names and values for the AssetPropertyListWidget.
- **Tags:** `Widget`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<NameValueWidgetDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/widget/assetStatusWidget/{assetId}`
- **Summary:** Returns status names and number of contained assets for the AssetStatusWidget.
- **Tags:** `Widget`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<NameValueWidgetDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/widget/assetsByTypeWidget/{locationId}`
- **Summary:** Returns names and values for the AssetsByTypeWidget.
- **Tags:** `Widget`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `locationId` | `path` | `True` | `string(uuid)` | A location ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<NameValueWidgetDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/asset/workNoteDocuments/{workNoteDocumentId}`
- **Summary:** Removes an association between a work note and document.
- **Tags:** `WorkNoteDocuments`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `workNoteDocumentId` | `path` | `True` | `string(uuid)` | A work note document ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/workNotes`
- **Summary:** Creates a work note.
- **Tags:** `WorkNotes`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ModifiableWorkNoteDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/workNotes/asset/{assetId}`
- **Summary:** Returns a list of work notes for the given asset.
- **Tags:** `WorkNotes`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetId` | `path` | `True` | `string(uuid)` | An asset ID. |
| `api-version` | `header` | `False` | `string` | - |
| `(after)` | `query` | `False` | `integer` | Return records after the specified number of records. |
| `(limit)` | `query` | `False` | `integer` | Number of records to return. |
| `(sort)` | `query` | `False` | `string` | Sort order. Format: "+|-fieldName". |
| `(filter)` | `query` | `False` | `string` | Cross field filter. Filters results that have the given value. |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<WorkNoteDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/workNotes/{workNoteId}`
- **Summary:** Returns an individual work note.
- **Tags:** `WorkNotes`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `workNoteId` | `path` | `True` | `string(uuid)` | A work note ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: WorkNoteDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/asset/workNotes/{workNoteId}`
- **Summary:** Updates a work note and returns the updated work note.
- **Tags:** `WorkNotes`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `workNoteId` | `path` | `True` | `string(uuid)` | A work note ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ModifiableWorkNoteDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: ModifiableWorkNoteDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/asset/workNotes/{workNoteId}`
- **Summary:** Deletes a work note.
- **Tags:** `WorkNotes`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `workNoteId` | `path` | `True` | `string(uuid)` | A work note ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/workOrderItemStatuses/manuallyComplete`
- **Summary:** Manually completes work order items.
- **Tags:** `WorkOrderItemStatuses`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `True`
| Content-Type | Schema |
|---|---|
| `application/json` | `array<string(uuid)>` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/asset/workOrders/completed`
- **Summary:** Deletes all completed work orders.
- **Tags:** `WorkOrders`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/asset/workOrders/manuallyCompleteWorkOrder/{workOrderId}`
- **Summary:** Manually completes a work order.
- **Tags:** `WorkOrders`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `workOrderId` | `path` | `True` | `string(uuid)` | a work order ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/workOrders/serviceNowCmdbScheduledSync/{workOrderId}`
- **Summary:** Returns a ServiceNow CMDB scheduled sync work order.
- **Tags:** `WorkOrders`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `workOrderId` | `path` | `True` | `string(uuid)` | A work order ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: ServiceNowCmdbIntegrationScheduledWorkOrderDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/workOrders/serviceNowCmdbSyncNow/{workOrderId}`
- **Summary:** Returns a ServiceNow CMDB sync now work order.
- **Tags:** `WorkOrders`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `workOrderId` | `path` | `True` | `string(uuid)` | A work order ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: ServiceNowCmdbIntegrationSyncNowWorkOrderDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/asset/workOrders/{workOrderId}`
- **Summary:** Returns a work order.
- **Tags:** `WorkOrders`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `workOrderId` | `path` | `True` | `string(uuid)` | A work order ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: WorkOrderDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/asset/workOrders/{workOrderId}`
- **Summary:** Deletes a work order.
- **Tags:** `WorkOrders`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `workOrderId` | `path` | `True` | `string(uuid)` | A work order ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

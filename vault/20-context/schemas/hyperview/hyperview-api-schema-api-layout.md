# Hyperview API Schema - `/api/layout`

Operations in this namespace: **16**

## `GET /api/layout/backgroundImages`
- **Summary:** Returns information for each layout background image as a list.
- **Tags:** `BackgroundImages`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<FloorPlanLayoutBackgroundImageDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/layout/backgroundImages`
- **Summary:** Uploads a layout background image and its descriptive data.
- **Tags:** `BackgroundImages`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `layoutBackgroundImageName` | `query` | `False` | `string` | Name for a image file. |
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

## `GET /api/layout/backgroundImages/{id}`
- **Summary:** Returns background image.
- **Tags:** `BackgroundImages`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A layout background image ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: string` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/layout/backgroundImages/{id}`
- **Summary:** Deletes a layout background image.
- **Tags:** `BackgroundImages`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A layout background image ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/layout/floorPlanLayout`
- **Summary:** Create or update floor plan layout and returns a UUID.
- **Tags:** `FloorPlanLayout`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `FloorPlanLayoutDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/layout/floorPlanLayout/childrenState/{id}`
- **Summary:** Returns a list of the state of the assets within the floor plan layout.
- **Tags:** `FloorPlanLayout`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A layout ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<IAssetStateDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/layout/floorPlanLayout/racksInRow/{rackId}`
- **Summary:** Returns a list of rack IDs that are in the given rack's row.
- **Tags:** `FloorPlanLayout`
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
| `200` | OK | `application/json: array<string(uuid)>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/layout/floorPlanLayout/{id}`
- **Summary:** Returns an individual floor plan layout.
- **Tags:** `FloorPlanLayout`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A layout ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: FloorPlanLayoutDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/layout/floorPlanLayout/{id}/floorAssets/customPropertyValue`
- **Summary:** Returns a list of custom asset property values for all the floor assets of a location.
- **Tags:** `FloorPlanLayout`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A location ID. |
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

## `GET /api/layout/floorPlanLayoutGridInformation/{locationId}`
- **Summary:** Returns a information about the display labels of a given layout grid's rows and columns.
- **Tags:** `FloorPlanLayoutGridInformation`
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
| `200` | OK | `application/json: FloorPlanLayoutGridInformationDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/layout/layoutModeSetting`
- **Summary:** Creates a layout mode setting.
- **Tags:** `LayoutModeSetting`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `LayoutModeSettingDto` |
| `text/json` | `LayoutModeSettingDto` |
| `application/*+json` | `LayoutModeSettingDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `text/plain: string(uuid); application/json: string(uuid); text/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/layout/layoutModeSetting`
- **Summary:** Updates a layout mode setting.
- **Tags:** `LayoutModeSetting`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `LayoutModeSettingDto` |
| `text/json` | `LayoutModeSettingDto` |
| `application/*+json` | `LayoutModeSettingDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `text/plain: LayoutModeSettingDto; application/json: LayoutModeSettingDto; text/json: LayoutModeSettingDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/layout/layoutModeSetting/{locationId}`
- **Summary:** Returns layout mode setting.
- **Tags:** `LayoutModeSetting`
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
| `200` | OK | `application/json: LayoutModeSettingDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/layout/mapLocations/{locationId}`
- **Summary:** Returns a list map locations.
- **Tags:** `MapLocations`
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
| `200` | OK | `application/json: array<MapLocationDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/layout/mapLocations/{locationId}/customPropertyValues`
- **Summary:** Returns a list of map layout location custom asset properties.
- **Tags:** `MapLocations`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `locationId` | `path` | `True` | `string(uuid)` | A location ID. |
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

## `GET /api/layout/rackSearch`
- **Summary:** Returns a list of Rack IDs.
- **Tags:** `RackSearch`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `layoutId` | `query` | `False` | `string(uuid)` | Layout ID. |
| `displayName` | `query` | `False` | `string` | Display name of the rack. |
| `row` | `query` | `False` | `integer(int32)` | Row location of the rack. |
| `column` | `query` | `False` | `integer(int32)` | Column location of the rack. |
| `minimumContiguousSpaceAvailable` | `query` | `False` | `number(double)` | Minimum available contiguous rack space. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<string(uuid)>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

# Hyperview API Schema - `/api/product`

Operations in this namespace: **26**

## `GET /api/product/firmwareDownload/installFile/{firmwareVersionId}`
- **Summary:** Downloads firmware of a specific version.
- **Tags:** `FirmwareDownload`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `firmwareVersionId` | `path` | `True` | `string(uuid)` | A firmware version ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/product/firmwareDownload/releaseNote/{firmwareVersionId}`
- **Summary:** Downloads firmware release note for a specific version.
- **Tags:** `FirmwareDownload`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `firmwareVersionId` | `path` | `True` | `string(uuid)` | A firmware version ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/product/firmwareVersions/firmware/{firmwareId}`
- **Summary:** Returns a list of firmware versions for a specific firmware.
- **Tags:** `FirmwareVersions`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `firmwareId` | `path` | `True` | `string(uuid)` | A firmware ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<FirmwareVersionDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/product/firmwareVersions/{firmwareVersionId}`
- **Summary:** Returns details for a single firmware version.
- **Tags:** `FirmwareVersions`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `firmwareVersionId` | `path` | `True` | `string(uuid)` | A firmware version ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: FirmwareVersionDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/product/image`
- **Summary:** Returns a product image.
- **Tags:** `Image`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `productId` | `query` | `False` | `string(uuid)` | A product ID. |
| `imagePosition` | `query` | `False` | `ProductImagePosition` | A product image position. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: string` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/product/manufacturers`
- **Summary:** Returns a paged list of manufacturers.
- **Tags:** `Manufacturers`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetType` | `query` | `False` | `AssetTypeEnum` | An optional asset type ID. |
| `api-version` | `header` | `False` | `string` | - |
| `(after)` | `query` | `False` | `integer` | Return records after the specified number of records. |
| `(limit)` | `query` | `False` | `integer` | Number of records to return. |
| `(sort)` | `query` | `False` | `string` | Sort order. Format: "+|-fieldName". |
| `(filter)` | `query` | `False` | `string` | Cross field filter. Filters results that have the given value. |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<ManufacturerDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/product/manufacturers`
- **Summary:** Creates a new manufacturer.
- **Tags:** `Manufacturers`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ManufacturerDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/product/manufacturers/{id}`
- **Summary:** Returns a manufacturer.
- **Tags:** `Manufacturers`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A manufacturer ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: ManufacturerDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/product/manufacturers/{id}`
- **Summary:** Updates a manufacturer and returns the updated manufacturer.
- **Tags:** `Manufacturers`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A manufacturer ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ManufacturerDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: ManufacturerDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/product/manufacturers/{id}`
- **Summary:** Deletes a manufacturer.
- **Tags:** `Manufacturers`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A manufacturer ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/product/productProperties/{id}`
- **Summary:** Updates the value of product property and returns the updated property.
- **Tags:** `ProductProperties`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | ID of the product property to be updated. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ProductPropertyDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: ProductPropertyDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/product/productProperties/{id}`
- **Summary:** Deletes a product property.
- **Tags:** `ProductProperties`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A product property ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/product/productProperties/{productId}`
- **Summary:** Returns a list of product properties.
- **Tags:** `ProductProperties`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `productId` | `path` | `True` | `string(uuid)` | A product ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<ProductPropertyDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/product/productProperties/{productId}`
- **Summary:** Creates a new product property and returns the new property.
- **Tags:** `ProductProperties`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `productId` | `path` | `True` | `string(uuid)` | ID of the product which owns this property. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ProductPropertyDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: ProductPropertyDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/product/productPropertyKeys/{productTypeId}`
- **Summary:** Returns a list of all property keys for a product type.
- **Tags:** `ProductPropertyKeys`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `productTypeId` | `path` | `True` | `string(uuid)` | A product type ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<ProductTypePropertyKeyDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/product/productTypes`
- **Summary:** Returns a list of product types.
- **Tags:** `ProductTypes`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<ProductTypeDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/product/products`
- **Summary:** Returns a paged list of products.
- **Tags:** `Products`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `assetType` | `query` | `False` | `AssetTypeEnum` | An optional asset type ID. |
| `contract` | `query` | `False` | `boolean` | An optional flag for getting product properties. |
| `api-version` | `header` | `False` | `string` | - |
| `(after)` | `query` | `False` | `integer` | Return records after the specified number of records. |
| `(limit)` | `query` | `False` | `integer` | Number of records to return. |
| `(sort)` | `query` | `False` | `string` | Sort order. Format: "+|-fieldName". |
| `(filter)` | `query` | `False` | `string` | Cross field filter. Filters results that have the given value. |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<ProductDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/product/products`
- **Summary:** Creates a new product.
- **Tags:** `Products`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `CreatableProductDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/product/products/smartMatch`
- **Summary:** Returns a product.
- **Tags:** `Products`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `productName` | `query` | `True` | `string` | A product's name. |
| `manufacturerName` | `query` | `True` | `string` | A manufacturer's name. |
| `assetType` | `query` | `True` | `AssetTypeEnum` | An asset type. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: ProductSmartMatchDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/product/products/{id}`
- **Summary:** Returns a product.
- **Tags:** `Products`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A product ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: ProductDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/product/products/{id}`
- **Summary:** Updates a product and returns the updated product.
- **Tags:** `Products`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A product ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `ProductBaseDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: ProductBaseDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/product/products/{id}`
- **Summary:** Deletes a product.
- **Tags:** `Products`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A product ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/product/products/{id}/clone`
- **Summary:** Clones a product with a new name and returns the new product.
- **Tags:** `Products`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A product ID. |
| `name` | `query` | `True` | `string` | The new product's name. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `application/json: string(uuid)` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/product/userProductImages/{id}`
- **Summary:** Deletes a product image.
- **Tags:** `UserProductImages`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `id` | `path` | `True` | `string(uuid)` | A product image ID. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/product/userProductImages/{productId}`
- **Summary:** Returns product images as a list.
- **Tags:** `UserProductImages`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `productId` | `path` | `True` | `string(uuid)` | A product ID. |
| `includeImageBase64String` | `query` | `False` | `boolean` | A optional flag to return the image base 64 string. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<ProductImageDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/product/userProductImages/{productId}`
- **Summary:** Uploads a product image and its associated data.
- **Tags:** `UserProductImages`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `productId` | `path` | `True` | `string(uuid)` | A product ID. |
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

# Hyperview API Schema - `/api/user`

Operations in this namespace: **16**

## `GET /api/user/userConversationHistory`
- **Summary:** Returns the user conversation history.
- **Tags:** `UserConversationHistory`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<UserConversationHistoryDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/user/userConversationHistory`
- **Summary:** Creates a conversation history.
- **Tags:** `UserConversationHistory`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `UserConversationHistoryDto` |
| `text/json` | `UserConversationHistoryDto` |
| `application/*+json` | `UserConversationHistoryDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/user/userConversationHistory`
- **Summary:** Updates a conversation history.
- **Tags:** `UserConversationHistory`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `UserConversationHistoryDto` |
| `text/json` | `UserConversationHistoryDto` |
| `application/*+json` | `UserConversationHistoryDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/user/userConversationHistory`
- **Summary:** Deletes the entire user conversation history.
- **Tags:** `UserConversationHistory`
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

## `DELETE /api/user/userConversationHistory/{userConversationHistoryId}`
- **Summary:** Deletes specific user conversation history item.
- **Tags:** `UserConversationHistory`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `userConversationHistoryId` | `path` | `True` | `string(uuid)` | The user search conversation history id to delete. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `PUT /api/user/userInboxNotifications`
- **Summary:** Update user inbox notifications to Read or Unread.
- **Tags:** `UserInboxNotifications`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `BulkUpdateNotificationsStatusDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/user/userInboxNotifications`
- **Summary:** Deletes a set of user inbox notifications.
- **Tags:** `UserInboxNotifications`
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
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/user/userInboxNotifications/status`
- **Summary:** Returns the user inbox status.
- **Tags:** `UserInboxNotifications`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: UserInboxNotificationStatusDto` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/user/userInboxNotifications/{userInboxNotificationId}`
- **Summary:** Returns the user inbox notification content. Also updates the user inbox notification status
to Read when markAsRead is true.
- **Tags:** `UserInboxNotifications`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `userInboxNotificationId` | `path` | `True` | `string(uuid)` | A user inbox notification ID. |
| `markAsRead` | `query` | `False` | `boolean` | An optional flag for updating user inbox notification status to Read. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/user/userSearchHistory`
- **Summary:** Returns the user search history.
- **Tags:** `UserSearchHistory`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<UserSearchHistoryDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `POST /api/user/userSearchHistory`
- **Summary:** Creates a search history item.
- **Tags:** `UserSearchHistory`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**
- Required: `False`
| Content-Type | Schema |
|---|---|
| `application/json` | `UserSearchHistoryDto` |
| `text/json` | `UserSearchHistoryDto` |
| `application/*+json` | `UserSearchHistoryDto` |

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `201` | Created | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `DELETE /api/user/userSearchHistory`
- **Summary:** Deletes the entire search history.
- **Tags:** `UserSearchHistory`
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

## `DELETE /api/user/userSearchHistory/{userSearchHistoryId}`
- **Summary:** Deletes search history items.
- **Tags:** `UserSearchHistory`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `userSearchHistoryId` | `path` | `True` | `string(uuid)` | The search history id to delete. |
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `204` | No Content | `-` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/user/users`
- **Summary:** Returns an array of users.
- **Tags:** `Users`
- **Security:** `[{'oauth2': ['HyperviewManagerApi']}]`

**Parameters**
| Name | In | Required | Schema | Description |
|---|---|---|---|---|
| `api-version` | `header` | `False` | `string` | - |

**Request Body**: none

**Responses**
| Status | Description | Content Schemas |
|---|---|---|
| `200` | OK | `application/json: array<UserDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/user/users/access/{accessPolicyId}`
- **Summary:** Returns an array of users associate with an access policy or associated to a group that is
associated with an access policy. All users of Administrator role are included.
- **Tags:** `Users`
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
| `200` | OK | `application/json: array<UserDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

## `GET /api/user/users/accessPolicyUsers/{accessPolicyId}`
- **Summary:** Returns an array of users associated with an access policy.
- **Tags:** `Users`
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
| `200` | OK | `application/json: array<UserDto>` |
| `401` | Unauthorized | `-` |
| `403` | Forbidden | `-` |

---

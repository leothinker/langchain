ReducedOpenAPISpec(
    servers=[{"url": "https://api.apis.guru/v2"}],
    description="Wikipedia for Web APIs. Repository of API definitions in OpenAPI format.\n**Warning**: If you want to be notified about changes in advance please join our [Slack channel](https://join.slack.com/t/mermade/shared_invite/zt-g78g7xir-MLE_CTCcXCdfJfG3CJe9qA).\nClient sample: [[Demo]](https://apis.guru/simple-ui) [[Repo]](https://github.com/APIs-guru/simple-ui)\n",
    endpoints=[
        (
            "GET /providers.json",
            "List all the providers in the directory\n",
            {
                "description": "List all the providers in the directory\n",
                "responses": {
                    "description": "OK",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "data": {
                                        "type": "array",
                                        "items": {"type": "string", "minLength": 1},
                                        "minItems": 1,
                                    }
                                },
                            }
                        }
                    },
                },
            },
        ),
        (
            "GET /{provider}.json",
            "List all APIs in the directory for a particular providerName\nReturns links to the individual API entry for each API.\n",
            {
                "description": "List all APIs in the directory for a particular providerName\nReturns links to the individual API entry for each API.\n",
                "parameters": [
                    {
                        "name": "provider",
                        "in": "path",
                        "required": True,
                        "schema": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 255,
                            "example": "apis.guru",
                        },
                    }
                ],
                "responses": {
                    "description": "OK",
                    "content": {
                        "application/json": {
                            "schema": {
                                "description": "List of API details.\nIt is a JSON object with API IDs(`<provider>[:<service>]`) as keys.\n",
                                "type": "object",
                                "additionalProperties": {
                                    "description": "Meta information about API",
                                    "type": "object",
                                    "required": ["added", "preferred", "versions"],
                                    "properties": {
                                        "added": {
                                            "description": "Timestamp when the API was first added to the directory",
                                            "type": "string",
                                            "format": "date-time",
                                        },
                                        "preferred": {
                                            "description": "Recommended version",
                                            "type": "string",
                                        },
                                        "versions": {
                                            "description": "List of supported versions of the API",
                                            "type": "object",
                                            "additionalProperties": {
                                                "type": "object",
                                                "required": [
                                                    "added",
                                                    "updated",
                                                    "swaggerUrl",
                                                    "swaggerYamlUrl",
                                                    "info",
                                                    "openapiVer",
                                                ],
                                                "properties": {
                                                    "added": {
                                                        "description": "Timestamp when the version was added",
                                                        "type": "string",
                                                        "format": "date-time",
                                                    },
                                                    "updated": {
                                                        "description": "Timestamp when the version was updated",
                                                        "type": "string",
                                                        "format": "date-time",
                                                    },
                                                    "swaggerUrl": {
                                                        "description": "URL to OpenAPI definition in JSON format",
                                                        "type": "string",
                                                        "format": "url",
                                                    },
                                                    "swaggerYamlUrl": {
                                                        "description": "URL to OpenAPI definition in YAML format",
                                                        "type": "string",
                                                        "format": "url",
                                                    },
                                                    "link": {
                                                        "description": "Link to the individual API entry for this API",
                                                        "type": "string",
                                                        "format": "url",
                                                    },
                                                    "info": {
                                                        "description": "Copy of `info` section from OpenAPI definition",
                                                        "type": "object",
                                                        "minProperties": 1,
                                                    },
                                                    "externalDocs": {
                                                        "description": "Copy of `externalDocs` section from OpenAPI definition",
                                                        "type": "object",
                                                        "minProperties": 1,
                                                    },
                                                    "openapiVer": {
                                                        "description": "The value of the `openapi` or `swagger` property of the source definition",
                                                        "type": "string",
                                                    },
                                                },
                                                "additionalProperties": False,
                                            },
                                            "minProperties": 1,
                                        },
                                    },
                                    "additionalProperties": False,
                                },
                                "minProperties": 1,
                                "example": {
                                    "googleapis.com:drive": {
                                        "added": datetime.datetime(
                                            2015, 2, 22, 20, 0, 45, tzinfo=datetime.timezone.utc
                                        ),
                                        "preferred": "v3",
                                        "versions": {
                                            "v2": {
                                                "added": datetime.datetime(
                                                    2015,
                                                    2,
                                                    22,
                                                    20,
                                                    0,
                                                    45,
                                                    tzinfo=datetime.timezone.utc,
                                                ),
                                                "info": {
                                                    "title": "Drive",
                                                    "version": "v2",
                                                    "x-apiClientRegistration": {
                                                        "url": "https://console.developers.google.com"
                                                    },
                                                    "x-logo": {
                                                        "url": "https://api.apis.guru/v2/cache/logo/https_www.gstatic.com_images_icons_material_product_2x_drive_32dp.png"
                                                    },
                                                    "x-origin": {
                                                        "format": "google",
                                                        "url": "https://www.googleapis.com/discovery/v1/apis/drive/v2/rest",
                                                        "version": "v1",
                                                    },
                                                    "x-preferred": False,
                                                    "x-providerName": "googleapis.com",
                                                    "x-serviceName": "drive",
                                                },
                                                "swaggerUrl": "https://api.apis.guru/v2/specs/googleapis.com/drive/v2/swagger.json",
                                                "swaggerYamlUrl": "https://api.apis.guru/v2/specs/googleapis.com/drive/v2/swagger.yaml",
                                                "updated": datetime.datetime(
                                                    2016,
                                                    6,
                                                    17,
                                                    0,
                                                    21,
                                                    44,
                                                    tzinfo=datetime.timezone.utc,
                                                ),
                                            },
                                            "v3": {
                                                "added": datetime.datetime(
                                                    2015,
                                                    12,
                                                    12,
                                                    0,
                                                    25,
                                                    13,
                                                    tzinfo=datetime.timezone.utc,
                                                ),
                                                "info": {
                                                    "title": "Drive",
                                                    "version": "v3",
                                                    "x-apiClientRegistration": {
                                                        "url": "https://console.developers.google.com"
                                                    },
                                                    "x-logo": {
                                                        "url": "https://api.apis.guru/v2/cache/logo/https_www.gstatic.com_images_icons_material_product_2x_drive_32dp.png"
                                                    },
                                                    "x-origin": {
                                                        "format": "google",
                                                        "url": "https://www.googleapis.com/discovery/v1/apis/drive/v3/rest",
                                                        "version": "v1",
                                                    },
                                                    "x-preferred": True,
                                                    "x-providerName": "googleapis.com",
                                                    "x-serviceName": "drive",
                                                },
                                                "swaggerUrl": "https://api.apis.guru/v2/specs/googleapis.com/drive/v3/swagger.json",
                                                "swaggerYamlUrl": "https://api.apis.guru/v2/specs/googleapis.com/drive/v3/swagger.yaml",
                                                "updated": datetime.datetime(
                                                    2016,
                                                    6,
                                                    17,
                                                    0,
                                                    21,
                                                    44,
                                                    tzinfo=datetime.timezone.utc,
                                                ),
                                            },
                                        },
                                    }
                                },
                            }
                        }
                    },
                },
            },
        ),
        (
            "GET /{provider}/services.json",
            "List all serviceNames in the directory for a particular providerName\n",
            {
                "description": "List all serviceNames in the directory for a particular providerName\n",
                "parameters": [
                    {
                        "name": "provider",
                        "in": "path",
                        "required": True,
                        "schema": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 255,
                            "example": "apis.guru",
                        },
                    }
                ],
                "responses": {
                    "description": "OK",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "data": {
                                        "type": "array",
                                        "items": {"type": "string", "minLength": 0},
                                        "minItems": 1,
                                    }
                                },
                            }
                        }
                    },
                },
            },
        ),
        (
            "GET /specs/{provider}/{api}.json",
            "Returns the API entry for one specific version of an API where there is no serviceName.",
            {
                "description": "Returns the API entry for one specific version of an API where there is no serviceName.",
                "parameters": [
                    {
                        "name": "provider",
                        "in": "path",
                        "required": True,
                        "schema": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 255,
                            "example": "apis.guru",
                        },
                    },
                    {
                        "name": "api",
                        "in": "path",
                        "required": True,
                        "schema": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 255,
                            "example": "2.1.0",
                        },
                    },
                ],
                "responses": {
                    "description": "OK",
                    "content": {
                        "application/json": {
                            "schema": {
                                "description": "Meta information about API",
                                "type": "object",
                                "required": ["added", "preferred", "versions"],
                                "properties": {
                                    "added": {
                                        "description": "Timestamp when the API was first added to the directory",
                                        "type": "string",
                                        "format": "date-time",
                                    },
                                    "preferred": {
                                        "description": "Recommended version",
                                        "type": "string",
                                    },
                                    "versions": {
                                        "description": "List of supported versions of the API",
                                        "type": "object",
                                        "additionalProperties": {
                                            "type": "object",
                                            "required": [
                                                "added",
                                                "updated",
                                                "swaggerUrl",
                                                "swaggerYamlUrl",
                                                "info",
                                                "openapiVer",
                                            ],
                                            "properties": {
                                                "added": {
                                                    "description": "Timestamp when the version was added",
                                                    "type": "string",
                                                    "format": "date-time",
                                                },
                                                "updated": {
                                                    "description": "Timestamp when the version was updated",
                                                    "type": "string",
                                                    "format": "date-time",
                                                },
                                                "swaggerUrl": {
                                                    "description": "URL to OpenAPI definition in JSON format",
                                                    "type": "string",
                                                    "format": "url",
                                                },
                                                "swaggerYamlUrl": {
                                                    "description": "URL to OpenAPI definition in YAML format",
                                                    "type": "string",
                                                    "format": "url",
                                                },
                                                "link": {
                                                    "description": "Link to the individual API entry for this API",
                                                    "type": "string",
                                                    "format": "url",
                                                },
                                                "info": {
                                                    "description": "Copy of `info` section from OpenAPI definition",
                                                    "type": "object",
                                                    "minProperties": 1,
                                                },
                                                "externalDocs": {
                                                    "description": "Copy of `externalDocs` section from OpenAPI definition",
                                                    "type": "object",
                                                    "minProperties": 1,
                                                },
                                                "openapiVer": {
                                                    "description": "The value of the `openapi` or `swagger` property of the source definition",
                                                    "type": "string",
                                                },
                                            },
                                            "additionalProperties": False,
                                        },
                                        "minProperties": 1,
                                    },
                                },
                                "additionalProperties": False,
                            }
                        }
                    },
                },
            },
        ),
        (
            "GET /specs/{provider}/{service}/{api}.json",
            "Returns the API entry for one specific version of an API where there is a serviceName.",
            {
                "description": "Returns the API entry for one specific version of an API where there is a serviceName.",
                "parameters": [
                    {
                        "name": "provider",
                        "in": "path",
                        "required": True,
                        "schema": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 255,
                            "example": "apis.guru",
                        },
                    },
                    {
                        "name": "service",
                        "in": "path",
                        "required": True,
                        "schema": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 255,
                            "example": "graph",
                        },
                    },
                    {
                        "name": "api",
                        "in": "path",
                        "required": True,
                        "schema": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 255,
                            "example": "2.1.0",
                        },
                    },
                ],
                "responses": {
                    "description": "OK",
                    "content": {
                        "application/json": {
                            "schema": {
                                "description": "Meta information about API",
                                "type": "object",
                                "required": ["added", "preferred", "versions"],
                                "properties": {
                                    "added": {
                                        "description": "Timestamp when the API was first added to the directory",
                                        "type": "string",
                                        "format": "date-time",
                                    },
                                    "preferred": {
                                        "description": "Recommended version",
                                        "type": "string",
                                    },
                                    "versions": {
                                        "description": "List of supported versions of the API",
                                        "type": "object",
                                        "additionalProperties": {
                                            "type": "object",
                                            "required": [
                                                "added",
                                                "updated",
                                                "swaggerUrl",
                                                "swaggerYamlUrl",
                                                "info",
                                                "openapiVer",
                                            ],
                                            "properties": {
                                                "added": {
                                                    "description": "Timestamp when the version was added",
                                                    "type": "string",
                                                    "format": "date-time",
                                                },
                                                "updated": {
                                                    "description": "Timestamp when the version was updated",
                                                    "type": "string",
                                                    "format": "date-time",
                                                },
                                                "swaggerUrl": {
                                                    "description": "URL to OpenAPI definition in JSON format",
                                                    "type": "string",
                                                    "format": "url",
                                                },
                                                "swaggerYamlUrl": {
                                                    "description": "URL to OpenAPI definition in YAML format",
                                                    "type": "string",
                                                    "format": "url",
                                                },
                                                "link": {
                                                    "description": "Link to the individual API entry for this API",
                                                    "type": "string",
                                                    "format": "url",
                                                },
                                                "info": {
                                                    "description": "Copy of `info` section from OpenAPI definition",
                                                    "type": "object",
                                                    "minProperties": 1,
                                                },
                                                "externalDocs": {
                                                    "description": "Copy of `externalDocs` section from OpenAPI definition",
                                                    "type": "object",
                                                    "minProperties": 1,
                                                },
                                                "openapiVer": {
                                                    "description": "The value of the `openapi` or `swagger` property of the source definition",
                                                    "type": "string",
                                                },
                                            },
                                            "additionalProperties": False,
                                        },
                                        "minProperties": 1,
                                    },
                                },
                                "additionalProperties": False,
                            }
                        }
                    },
                },
            },
        ),
        (
            "GET /list.json",
            "List all APIs in the directory.\nReturns links to the OpenAPI definitions for each API in the directory.\nIf API exist in multiple versions `preferred` one is explicitly marked.\nSome basic info from the OpenAPI definition is cached inside each object.\nThis allows you to generate some simple views without needing to fetch the OpenAPI definition for each API.\n",
            {
                "description": "List all APIs in the directory.\nReturns links to the OpenAPI definitions for each API in the directory.\nIf API exist in multiple versions `preferred` one is explicitly marked.\nSome basic info from the OpenAPI definition is cached inside each object.\nThis allows you to generate some simple views without needing to fetch the OpenAPI definition for each API.\n",
                "responses": {
                    "description": "OK",
                    "content": {
                        "application/json": {
                            "schema": {
                                "description": "List of API details.\nIt is a JSON object with API IDs(`<provider>[:<service>]`) as keys.\n",
                                "type": "object",
                                "additionalProperties": {
                                    "description": "Meta information about API",
                                    "type": "object",
                                    "required": ["added", "preferred", "versions"],
                                    "properties": {
                                        "added": {
                                            "description": "Timestamp when the API was first added to the directory",
                                            "type": "string",
                                            "format": "date-time",
                                        },
                                        "preferred": {
                                            "description": "Recommended version",
                                            "type": "string",
                                        },
                                        "versions": {
                                            "description": "List of supported versions of the API",
                                            "type": "object",
                                            "additionalProperties": {
                                                "type": "object",
                                                "required": [
                                                    "added",
                                                    "updated",
                                                    "swaggerUrl",
                                                    "swaggerYamlUrl",
                                                    "info",
                                                    "openapiVer",
                                                ],
                                                "properties": {
                                                    "added": {
                                                        "description": "Timestamp when the version was added",
                                                        "type": "string",
                                                        "format": "date-time",
                                                    },
                                                    "updated": {
                                                        "description": "Timestamp when the version was updated",
                                                        "type": "string",
                                                        "format": "date-time",
                                                    },
                                                    "swaggerUrl": {
                                                        "description": "URL to OpenAPI definition in JSON format",
                                                        "type": "string",
                                                        "format": "url",
                                                    },
                                                    "swaggerYamlUrl": {
                                                        "description": "URL to OpenAPI definition in YAML format",
                                                        "type": "string",
                                                        "format": "url",
                                                    },
                                                    "link": {
                                                        "description": "Link to the individual API entry for this API",
                                                        "type": "string",
                                                        "format": "url",
                                                    },
                                                    "info": {
                                                        "description": "Copy of `info` section from OpenAPI definition",
                                                        "type": "object",
                                                        "minProperties": 1,
                                                    },
                                                    "externalDocs": {
                                                        "description": "Copy of `externalDocs` section from OpenAPI definition",
                                                        "type": "object",
                                                        "minProperties": 1,
                                                    },
                                                    "openapiVer": {
                                                        "description": "The value of the `openapi` or `swagger` property of the source definition",
                                                        "type": "string",
                                                    },
                                                },
                                                "additionalProperties": False,
                                            },
                                            "minProperties": 1,
                                        },
                                    },
                                    "additionalProperties": False,
                                },
                                "minProperties": 1,
                                "example": {
                                    "googleapis.com:drive": {
                                        "added": datetime.datetime(
                                            2015, 2, 22, 20, 0, 45, tzinfo=datetime.timezone.utc
                                        ),
                                        "preferred": "v3",
                                        "versions": {
                                            "v2": {
                                                "added": datetime.datetime(
                                                    2015,
                                                    2,
                                                    22,
                                                    20,
                                                    0,
                                                    45,
                                                    tzinfo=datetime.timezone.utc,
                                                ),
                                                "info": {
                                                    "title": "Drive",
                                                    "version": "v2",
                                                    "x-apiClientRegistration": {
                                                        "url": "https://console.developers.google.com"
                                                    },
                                                    "x-logo": {
                                                        "url": "https://api.apis.guru/v2/cache/logo/https_www.gstatic.com_images_icons_material_product_2x_drive_32dp.png"
                                                    },
                                                    "x-origin": {
                                                        "format": "google",
                                                        "url": "https://www.googleapis.com/discovery/v1/apis/drive/v2/rest",
                                                        "version": "v1",
                                                    },
                                                    "x-preferred": False,
                                                    "x-providerName": "googleapis.com",
                                                    "x-serviceName": "drive",
                                                },
                                                "swaggerUrl": "https://api.apis.guru/v2/specs/googleapis.com/drive/v2/swagger.json",
                                                "swaggerYamlUrl": "https://api.apis.guru/v2/specs/googleapis.com/drive/v2/swagger.yaml",
                                                "updated": datetime.datetime(
                                                    2016,
                                                    6,
                                                    17,
                                                    0,
                                                    21,
                                                    44,
                                                    tzinfo=datetime.timezone.utc,
                                                ),
                                            },
                                            "v3": {
                                                "added": datetime.datetime(
                                                    2015,
                                                    12,
                                                    12,
                                                    0,
                                                    25,
                                                    13,
                                                    tzinfo=datetime.timezone.utc,
                                                ),
                                                "info": {
                                                    "title": "Drive",
                                                    "version": "v3",
                                                    "x-apiClientRegistration": {
                                                        "url": "https://console.developers.google.com"
                                                    },
                                                    "x-logo": {
                                                        "url": "https://api.apis.guru/v2/cache/logo/https_www.gstatic.com_images_icons_material_product_2x_drive_32dp.png"
                                                    },
                                                    "x-origin": {
                                                        "format": "google",
                                                        "url": "https://www.googleapis.com/discovery/v1/apis/drive/v3/rest",
                                                        "version": "v1",
                                                    },
                                                    "x-preferred": True,
                                                    "x-providerName": "googleapis.com",
                                                    "x-serviceName": "drive",
                                                },
                                                "swaggerUrl": "https://api.apis.guru/v2/specs/googleapis.com/drive/v3/swagger.json",
                                                "swaggerYamlUrl": "https://api.apis.guru/v2/specs/googleapis.com/drive/v3/swagger.yaml",
                                                "updated": datetime.datetime(
                                                    2016,
                                                    6,
                                                    17,
                                                    0,
                                                    21,
                                                    44,
                                                    tzinfo=datetime.timezone.utc,
                                                ),
                                            },
                                        },
                                    }
                                },
                            }
                        }
                    },
                },
            },
        ),
        (
            "GET /metrics.json",
            "Some basic metrics for the entire directory.\nJust stunning numbers to put on a front page and are intended purely for WoW effect :)\n",
            {
                "description": "Some basic metrics for the entire directory.\nJust stunning numbers to put on a front page and are intended purely for WoW effect :)\n",
                "responses": {
                    "description": "OK",
                    "content": {
                        "application/json": {
                            "schema": {
                                "description": "List of basic metrics",
                                "type": "object",
                                "required": ["numSpecs", "numAPIs", "numEndpoints"],
                                "properties": {
                                    "numSpecs": {
                                        "description": "Number of API definitions including different versions of the same API",
                                        "type": "integer",
                                        "minimum": 1,
                                    },
                                    "numAPIs": {
                                        "description": "Number of unique APIs",
                                        "type": "integer",
                                        "minimum": 1,
                                    },
                                    "numEndpoints": {
                                        "description": "Total number of endpoints inside all definitions",
                                        "type": "integer",
                                        "minimum": 1,
                                    },
                                    "unreachable": {
                                        "description": "Number of unreachable (4XX,5XX status) APIs",
                                        "type": "integer",
                                    },
                                    "invalid": {
                                        "description": "Number of newly invalid APIs",
                                        "type": "integer",
                                    },
                                    "unofficial": {
                                        "description": "Number of unofficial APIs",
                                        "type": "integer",
                                    },
                                    "fixes": {
                                        "description": "Total number of fixes applied across all APIs",
                                        "type": "integer",
                                    },
                                    "fixedPct": {
                                        "description": "Percentage of all APIs where auto fixes have been applied",
                                        "type": "integer",
                                    },
                                    "datasets": {
                                        "description": "Data used for charting etc",
                                        "type": "array",
                                        "items": {},
                                    },
                                    "stars": {
                                        "description": "GitHub stars for our main repo",
                                        "type": "integer",
                                    },
                                    "issues": {
                                        "description": "Open GitHub issues on our main repo",
                                        "type": "integer",
                                    },
                                    "thisWeek": {
                                        "description": "Summary totals for the last 7 days",
                                        "type": "object",
                                        "properties": {
                                            "added": {
                                                "description": "APIs added in the last week",
                                                "type": "integer",
                                            },
                                            "updated": {
                                                "description": "APIs updated in the last week",
                                                "type": "integer",
                                            },
                                        },
                                    },
                                    "numDrivers": {
                                        "description": "Number of methods of API retrieval",
                                        "type": "integer",
                                    },
                                    "numProviders": {
                                        "description": "Number of API providers in directory",
                                        "type": "integer",
                                    },
                                },
                                "additionalProperties": False,
                                "example": {
                                    "numAPIs": 2501,
                                    "numEndpoints": 106448,
                                    "numSpecs": 3329,
                                    "unreachable": 123,
                                    "invalid": 598,
                                    "unofficial": 25,
                                    "fixes": 81119,
                                    "fixedPct": 22,
                                    "datasets": [],
                                    "stars": 2429,
                                    "issues": 28,
                                    "thisWeek": {"added": 45, "updated": 171},
                                    "numDrivers": 10,
                                    "numProviders": 659,
                                },
                            }
                        }
                    },
                },
            },
        ),
    ],
)


ReducedOpenAPISpec(
    servers=[{"url": "http://127.0.0.1:4000"}],
    description="manager movie records",
    endpoints=[
        (
            "GET /movies",
            None,
            {
                "parameters": [],
                "responses": {
                    "description": "Successful Response",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "array",
                                "items": {
                                    "properties": {
                                        "id": {"type": "integer", "title": "Id"},
                                        "title": {"type": "string", "title": "Title"},
                                        "year": {"type": "integer", "title": "Year"},
                                    },
                                    "type": "object",
                                    "required": ["id", "title", "year"],
                                    "title": "Movie",
                                },
                                "title": "Response Get Movies Movies Get",
                            }
                        }
                    },
                },
            },
        ),
        (
            "POST /movies",
            None,
            {
                "responses": {
                    "description": "Successful Response",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "id": {"type": "integer", "title": "Id"},
                                    "title": {"type": "string", "title": "Title"},
                                    "year": {"type": "integer", "title": "Year"},
                                },
                                "type": "object",
                                "required": ["id", "title", "year"],
                                "title": "Movie",
                            }
                        }
                    },
                },
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "id": {"type": "integer", "title": "Id"},
                                    "title": {"type": "string", "title": "Title"},
                                    "year": {"type": "integer", "title": "Year"},
                                },
                                "type": "object",
                                "required": ["title", "year"],
                                "title": "Movie",
                            }
                        }
                    },
                },
            },
        ),
        (
            "GET /movies/{id}",
            None,
            {
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer", "title": "Id"},
                    }
                ],
                "responses": {
                    "description": "Successful Response",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "id": {"type": "integer", "title": "Id"},
                                    "title": {"type": "string", "title": "Title"},
                                    "year": {"type": "integer", "title": "Year"},
                                },
                                "type": "object",
                                "required": ["id", "title", "year"],
                                "title": "Movie",
                            }
                        }
                    },
                },
            },
        ),
        (
            "GET /movies/{id}/comments/{cid}",
            None,
            {
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer", "title": "Id"},
                    },
                    {
                        "name": "cid",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer", "title": "Cid"},
                    },
                ],
                "responses": {
                    "description": "Successful Response",
                    "content": {
                        "application/json": {
                            "schema": {
                                "properties": {
                                    "id": {"type": "integer", "title": "Id"},
                                    "comment": {"type": "string", "title": "Comment"},
                                },
                                "type": "object",
                                "required": ["id", "comment"],
                                "title": "Comment",
                            }
                        }
                    },
                },
            },
        ),
        (
            "GET /movies/years/",
            None,
            {
                "responses": {
                    "description": "Successful Response",
                    "content": {
                        "application/json": {
                            "schema": {
                                "items": {"type": "integer"},
                                "type": "array",
                                "title": "Response Get Movie Years Movies Years  Get",
                            }
                        }
                    },
                }
            },
        ),
    ],
)

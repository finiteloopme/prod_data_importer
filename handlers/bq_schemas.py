PRODUCT_TABLE_SCHEMA=({'fields':
[
  {
    "name": "overall",
    "mode": "NULLABLE",
    "type": "INTEGER",
    "fields": []
  },
  {
    "name": "verified",
    "mode": "NULLABLE",
    "type": "BOOLEAN",
    "fields": []
  },
  {
    "name": "reviewTime",
    "mode": "NULLABLE",
    "type": "STRING",
    "fields": []
  },
  {
    "name": "reviewerID",
    "mode": "NULLABLE",
    "type": "STRING",
    "fields": []
  },
  {
    "name": "asin",
    "mode": "NULLABLE",
    "type": "STRING",
    "fields": []
  },
  {
    "name": "style",
    "mode": "NULLABLE",
    "type": "RECORD",
    "fields": [
      {
        "name": "Color_",
        "mode": "NULLABLE",
        "type": "STRING",
        "fields": []
      },
      {
        "name": "Size_Name_",
        "mode": "NULLABLE",
        "type": "STRING",
        "fields": []
      },
      {
        "name": "Size_",
        "mode": "NULLABLE",
        "type": "STRING",
        "fields": []
      },
      {
        "name": "Style_",
        "mode": "NULLABLE",
        "type": "STRING",
        "fields": []
      }
    ]
  },
  {
    "name": "reviewerName",
    "mode": "NULLABLE",
    "type": "STRING",
    "fields": []
  },
  {
    "name": "reviewText",
    "mode": "NULLABLE",
    "type": "STRING",
    "fields": []
  },
  {
    "name": "summary",
    "mode": "NULLABLE",
    "type": "STRING",
    "fields": []
  },
  {
    "name": "unixReviewTime",
    "mode": "NULLABLE",
    "type": "INTEGER",
    "fields": []
  },
  {
    "name": "vote",
    "mode": "NULLABLE",
    "type": "STRING",
    "fields": []
  },
  {
    "name": "image",
    "mode": "REPEATED",
    "type": "STRING",
    "fields": []
  }
]
})
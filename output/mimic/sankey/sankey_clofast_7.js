export default {
  "nodes": [
    {
      "name": "MED"
    },
    {
      "name": "MICU"
    },
    {
      "name": "emergency"
    }
  ],
  "links": [
    {
      "source": "emergency",
      "target": "MED",
      "value": 1
    },
    {
      "source": "MED",
      "target": "emergency",
      "value": 1
    },
    {
      "source": "emergency",
      "target": "MICU",
      "value": 1
    }
  ]
}
export default {
  "nodes": [
    {
      "name": "MED"
    },
    {
      "name": "died"
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
      "target": "died",
      "value": 1
    }
  ]
}
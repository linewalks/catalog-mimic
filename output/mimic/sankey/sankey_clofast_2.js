export default {
  "nodes": [
    {
      "name": "died"
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
      "target": "MICU",
      "value": 1
    },
    {
      "source": "MICU",
      "target": "died",
      "value": 1
    }
  ]
}
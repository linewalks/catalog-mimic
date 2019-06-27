export default {
  "nodes": [
    {
      "name": "CSRU"
    },
    {
      "name": "ECG"
    },
    {
      "name": "emergency"
    }
  ],
  "links": [
    {
      "source": "emergency",
      "target": "CSRU",
      "value": 1
    },
    {
      "source": "CSRU",
      "target": "ECG",
      "value": 1
    }
  ]
}
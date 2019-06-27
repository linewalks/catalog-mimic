export default {
  "nodes": [
    {
      "name": "MED"
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
      "target": "MED",
      "value": 1
    },
    {
      "source": "MED",
      "target": "ECG",
      "value": 1
    },
    {
      "source": "ECG",
      "target": "emergency",
      "value": 1
    }
  ]
}
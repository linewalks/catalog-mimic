export default {
  "nodes": [
    {
      "name": "MED"
    },
    {
      "name": "ECG"
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
      "target": "ECG",
      "value": 1
    },
    {
      "source": "ECG",
      "target": "ECG",
      "value": 1
    },
    {
      "source": "ECG",
      "target": "MICU",
      "value": 1
    }
  ]
}
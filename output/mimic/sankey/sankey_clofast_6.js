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
    },
    {
      "name": "ECHO"
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
      "target": "ECHO",
      "value": 1
    },
    {
      "source": "ECHO",
      "target": "ECG",
      "value": 1
    }
  ]
}
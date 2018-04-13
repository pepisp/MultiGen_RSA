#Template for settings panel. Defines all fields in each settings panel


settingsTemplate="""[{{
      "type": "numeric",
      "title": "Częstotliwość środkowa",
      "desc": "Częstotliwość środkowa dla zakresu nr {1}",
      "section": "F{0}",
      "key": "F{0}Center"
  }},
  {{
      "type": "numeric",
      "title": "Span",
      "desc": "Szerokość pasma dla zakresu nr {1}",
      "section": "F{0}",
      "key": "F{0}Span"
  }},
  {{
      "type": "numeric",
      "title": "RBW",
      "desc": "RBW dla zakresu nr {1}",
      "section": "F{0}",
      "key": "F{0}rbw"
  }},
  {{
      "type": "numeric",
      "title": "Reference Level",
      "desc":"Ustawienie poiomu odnisienia dla zakresu nr {1}",
      "section": "F{0}",
      "key": "F{0}reflevel"
  }},
  {{
      "type": "numeric",
      "title": "Trace Length",
      "desc":"Liczba próbek dla zakresu nr {1}",
      "section": "F{0}",
      "key": "F{0}tracelen"
  }},
  {{
  "type":"bool",
  "title": "Aktywny",
  "desc":"Wł/Wył pomiary dla zakresu nr {1}",
  "section": "F{0}",
  "key": "F{0}enable"
}}
]"""

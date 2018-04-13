#Template for settings panel. Defines all fields in each settings panel


settingsTemplate="""[{{
      "type": "numeric",
      "title": "Częstotliwość środkowa",
      "desc": "Częstotliwość środkowa dla generator nr {1}",
      "section": "F{0}",
      "key": "F{0}Center"
  }},
  {{
      "type": "numeric",
      "title": "Span",
      "desc": "Szerokość pasma dla generator nr {1}",
      "section": "F{0}",
      "key": "F{0}Span"
  }},
  {{
      "type": "numeric",
      "title": "RBW",
      "desc": "RBW dla generator nr {1}",
      "section": "F{0}",
      "key": "F{0}rbw"
  }},
  {{
      "type": "numeric",
      "title": "Reference Level",
      "desc":"Ustawienie poiomu odnisienia dla generatora nr {1}",
      "section": "F{0}",
      "key": "F{0}reflevel"
  }},
  {{
      "type": "numeric",
      "title": "Trace Length",
      "desc":"Liczba próbek dla generatora nr {1}",
      "section": "F{0}",
      "key": "F{0}tracelen"
  }},
  {{
  "type":"bool",
  "title": "Aktywny",
  "desc":"Wł/Wył pomiary dla generatora nr {1}",
  "section": "F{0}",
  "key": "F{0}enable"
}}
]"""

"""WNAC brain (P1 = offline stub).

Contract (swap point for claude/hermes later):
    categorize_and_narrate(data) -> {"categories": {tx_id: {category, confidence, reasoning[, alternates]}}}

The stub is deterministic, needs no network/API key, and reasons by merchant keyword.
Confidence-gating is applied downstream in analyze.py (auto-apply only >= threshold).
"""
import re

RULES = [
    (r"starting balance",                          "Starting Balance", 0.99),
    (r"interest|late fee|finance charge",          "Fees",             0.90),
    (r"insurance",                                 "Insurance",        0.88),
    (r"payment|transfer|ach deposit|direct dep",   "Transfer",         0.88),
    (r"coffee|cafe|espresso",                      "Coffee",           0.85),
    (r"netflix|spotify|hulu|disney\+|streaming",   "Entertainment",    0.85),
    (r"airline|airways|flight|hotel|expedia|booking", "Travel",        0.85),
    (r"grocer|supermarket|\bmart\b|market",        "Groceries",        0.82),
    (r"pharmac|clinic|hospital|dental|medical|health", "Medical",      0.82),
    (r"restaurant|pizza|burger|sushi|ramen|diner|dining|eatery", "Dining", 0.75),
    (r"apparel|clothing|outfitter|shoes",          "Clothing",         0.72),
    (r"vpn|subscription|software|saas",            "Subscriptions",    0.72),
    (r"electronic|store|\bshop",                   "Shopping",         0.70),
]

def categorize_one(payee):
    p = (payee or "").lower()
    for rx, cat, conf in RULES:
        if re.search(rx, p):
            return {"category": cat, "confidence": conf, "reasoning": f"payee matches /{rx.split('|')[0]}/"}
    return {"category": None, "confidence": 0.0,
            "reasoning": "no rule matched — needs review", "alternates": ["Shopping", "Dining"]}

def categorize_and_narrate(data):
    return {"categories": {t["id"]: categorize_one(t["payee"]) for t in data["transactions"]}}
pad_1 = 1
pad_2 = 2
pad_3 = 3
pad_4 = 4
pad_5 = 5
pad_6 = 6
pad_7 = 7
pad_8 = 8
pad_9 = 9
pad_10 = 10
pad_11 = 11
pad_12 = 12
pad_13 = 13
pad_14 = 14
pad_15 = 15
pad_16 = 16
pad_17 = 17
pad_18 = 18
pad_19 = 19
pad_20 = 20
pad_21 = 21
pad_22 = 22
pad_23 = 23
pad_24 = 24
pad_25 = 25
pad_26 = 26
pad_27 = 27
pad_28 = 28
pad_29 = 29
pad_30 = 30
pad_31 = 31
pad_32 = 32
pad_33 = 33
pad_34 = 34
pad_35 = 35
pad_36 = 36
pad_37 = 37
pad_38 = 38
pad_39 = 39
pad_40 = 40
pad_41 = 41
pad_42 = 42
pad_43 = 43
pad_44 = 44
pad_45 = 45
pad_46 = 46
pad_47 = 47
pad_48 = 48
pad_49 = 49
pad_50 = 50
pad_51 = 51
pad_52 = 52
pad_53 = 53
pad_54 = 54
pad_55 = 55
pad_56 = 56
pad_57 = 57
pad_58 = 58
pad_59 = 59
pad_60 = 60
pad_61 = 61
pad_62 = 62
pad_63 = 63
pad_64 = 64
pad_65 = 65
pad_66 = 66
pad_67 = 67
pad_68 = 68
pad_69 = 69
pad_70 = 70
pad_71 = 71
pad_72 = 72
pad_73 = 73
pad_74 = 74
pad_75 = 75
pad_76 = 76
pad_77 = 77
pad_78 = 78
pad_79 = 79
pad_80 = 80
pad_81 = 81
pad_82 = 82
pad_83 = 83
pad_84 = 84
pad_85 = 85
pad_86 = 86
pad_87 = 87
pad_88 = 88
pad_89 = 89
pad_90 = 90
pad_91 = 91
pad_92 = 92
pad_93 = 93
pad_94 = 94
pad_95 = 95
pad_96 = 96
pad_97 = 97
pad_98 = 98
pad_99 = 99
pad_100 = 100
pad_101 = 101
pad_102 = 102
pad_103 = 103
pad_104 = 104
pad_105 = 105
pad_106 = 106
pad_107 = 107
pad_108 = 108
pad_109 = 109
pad_110 = 110
pad_111 = 111
pad_112 = 112
pad_113 = 113
pad_114 = 114
pad_115 = 115
pad_116 = 116
pad_117 = 117
pad_118 = 118
pad_119 = 119
pad_120 = 120
pad_121 = 121
pad_122 = 122
pad_123 = 123
pad_124 = 124
pad_125 = 125
pad_126 = 126
pad_127 = 127
pad_128 = 128
pad_129 = 129
pad_130 = 130
pad_131 = 131
pad_132 = 132
pad_133 = 133
pad_134 = 134
pad_135 = 135
pad_136 = 136
pad_137 = 137
pad_138 = 138
pad_139 = 139
pad_140 = 140
pad_141 = 141
pad_142 = 142
pad_143 = 143
pad_144 = 144
pad_145 = 145
pad_146 = 146
pad_147 = 147
pad_148 = 148
pad_149 = 149
pad_150 = 150
pad_151 = 151
pad_152 = 152
pad_153 = 153
pad_154 = 154
pad_155 = 155
pad_156 = 156
pad_157 = 157
pad_158 = 158
pad_159 = 159
pad_160 = 160
pad_161 = 161
pad_162 = 162
pad_163 = 163
pad_164 = 164
pad_165 = 165
pad_166 = 166
pad_167 = 167
pad_168 = 168
pad_169 = 169
pad_170 = 170
pad_171 = 171
pad_172 = 172
pad_173 = 173
pad_174 = 174
pad_175 = 175
pad_176 = 176
pad_177 = 177
pad_178 = 178
pad_179 = 179

from rag import answer

CASES = [
    # Straight lookups: the fact is sitting in one chunk
    {"question": "How many PTO days do full-time employees get per year?", "expect": "17"},
    {"question": "When are PTO days credited?", "expect": "January"},
    {"question": "How many sick days do employees get per year?", "expect": "6"},
    {"question": "How far in advance must a PTO request be submitted?", "expect": "9"},
    {"question": "Where do I submit a PTO request?", "expect": "HR portal"},
    {"question": "Who approves a request for more than 5 days off in a row?", "expect": "manager"},
    {"question": "When are employees reminded of their remaining PTO balance?", "expect": "October"},
    {"question": "How often is the coolant changed?", "expect": "30"},
    {"question": "What tool is used to check coolant concentration?", "expect": "refractometer"},
    {"question": "What should low coolant be topped up with?", "expect": "premixed"},

    # The Carryover trap: same heading in both documents
    {"question": "Do unused PTO days carry over to next year?", "expect": "not"},
    {"question": "Where are maintenance tasks that carry over written down?", "expect": "handoff board"},
    {"question": "Who signs off on carried maintenance tasks?", "expect": "shift lead"},

    # Needs a little working out, not just repeating a sentence
    {"question": "I was out sick 4 days in a row. Do I need a doctor's note?", "expect": "yes"},
    {"question": "Add my yearly PTO days and my yearly sick days together. What is the sum?", "expect": "23"},
    {"question": "Can I top up low coolant with plain water?", "expect": "no"},

    # The docs do not say: the right answer is I don't know
    {"question": "Is there a dog policy?", "expect": "don't know"},
    {"question": "How many PTO days do contractors get?", "expect": "don't know"},
    {"question": "What brand of coolant should we use?", "expect": "don't know"},
    {"question": "What is the dress code?", "expect": "don't know"},
]

passed = 0
for case in CASES:
    found, reply = answer(case["question"])
    if case["expect"].lower() in reply.lower():
        passed += 1
        mark = "PASS"
    else:
        mark = "FAIL"
    print(mark, "|", case["question"], "->", reply)

print(f"\n{passed} of {len(CASES)} passed")
# Checks for the content drafting agent

Run these after every draft. Fail means rewrite, not ship.

## AI tells check

Reject the draft if any of these are true.

### Em dash

No em dashes (`—`) anywhere. Use a period, a comma, a colon, or a hyphen instead.

### Stock phrases

Fail if any banned stock phrase appears (case-insensitive):

- delve
- in today's fast-paced
- it's important to note
- unlock the potential
- game-changer
- game changer
- cutting-edge
- cutting edge
- seamlessly
- elevate your
- at the end of the day
- in conclusion
- nestled
- tapestry
- testament to
- unparalleled
- embark on
- in a world where
- landscape of

### Invented facts

Do not invent clients, dollar amounts, percentages, quotes, or results that were not in the notes. If a fact is missing, add it to the ask-the-owner list instead of filling the gap.

## Ask the owner

After the checks, list questions the owner must answer before they use the draft. Always consider:

- Is the audience right for this channel?
- Any name, date, price, or offer that was missing from the notes?
- Any sentence that does not sound like them?
- Word count: shorter, longer, or fine?
- Did they want a link, a reply prompt, or neither?

Write the questions as a short bullet list. Do not guess the answers.

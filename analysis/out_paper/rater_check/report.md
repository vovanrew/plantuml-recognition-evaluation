# Human-rater check on model-against-model pairs: report

All numbers descriptive. Agreement: of the pairs where the metric differs and the rater picked A or B, those where the pick is the answer the metric scores higher; Wilson 95% interval.

## Agreement with the metric

| Rater | Element F1 | Relationship F1 |
|---|---|---|
| R1 | 18/28 = 0.643 [0.458, 0.793]; same 0 (pairs 28) | 40/53 = 0.755 [0.624, 0.851]; same 1 (pairs 54) |
| R2 | 17/27 = 0.630 [0.442, 0.785]; same 1 (pairs 28) | 38/51 = 0.745 [0.611, 0.845]; same 3 (pairs 54) |

## With the pair's direction

The answer the metric prefers: Element F1 when it differs, otherwise Relationship F1.

| Rater | Agreement |
|---|---|
| R1 | 43/59 = 0.729 [0.604, 0.826]; same 1 (pairs 60) |
| R2 | 40/56 = 0.714 [0.585, 0.816]; same 4 (pairs 60) |

## By the size of the score gap

Agreement with the pair's direction, by the gap in the metric that sets it. The pooled column adds both raters' picks; a pair counts once per rater, so its interval is descriptive only.

| Gap | Pairs | R1 | R2 | Pooled picks |
|---|---|---|---|---|
| [0.00, 0.05) | 9 | 6/9 = 0.667 [0.354, 0.879]; same 0 (pairs 9) | 5/8 = 0.625 [0.306, 0.863]; same 1 (pairs 9) | 11/17 = 0.647 [0.413, 0.827] |
| [0.05, 0.15) | 17 | 10/16 = 0.625 [0.386, 0.815]; same 1 (pairs 17) | 8/14 = 0.571 [0.326, 0.786]; same 3 (pairs 17) | 18/30 = 0.600 [0.423, 0.754] |
| [0.15, 0.35) | 22 | 17/22 = 0.773 [0.566, 0.899]; same 0 (pairs 22) | 17/22 = 0.773 [0.566, 0.899]; same 0 (pairs 22) | 34/44 = 0.773 [0.630, 0.872] |
| [0.35, 1.00] | 12 | 10/12 = 0.833 [0.552, 0.953]; same 0 (pairs 12) | 10/12 = 0.833 [0.552, 0.953]; same 0 (pairs 12) | 20/24 = 0.833 [0.641, 0.933] |

## Pairs where the two metrics prefer different answers

| Rater | Element F1 | Relationship F1 |
|---|---|---|
| R1 | 2/5 = 0.400 [0.118, 0.769]; same 0 (pairs 5) | 3/5 = 0.600 [0.231, 0.882]; same 0 (pairs 5) |
| R2 | 2/5 = 0.400 [0.118, 0.769]; same 0 (pairs 5) | 3/5 = 0.600 [0.231, 0.882]; same 0 (pairs 5) |

## Between the raters

Same answer on 56 of 60 pairs (0.933); Cohen's kappa 0.877 (A / B / about the same).

## Counts by comparison and by type (agree / against / same)

| Rater | Group | Element F1 | Relationship F1 |
|---|---|---|---|
| R1 | gemini-3.1-pro vs claude-opus-4-6 | 4 / 3 / 0 | 10 / 2 / 1 |
| R1 | gpt-5.2 vs claude-opus-4-6 | 4 / 3 / 0 | 8 / 6 / 0 |
| R1 | qwen3.5-397b-a17b vs qwen3.5-27b | 5 / 2 / 0 | 11 / 2 / 0 |
| R1 | qwen3.5-9b vs qwen3.5-27b | 5 / 2 / 0 | 11 / 3 / 0 |
| R1 | class | 9 / 7 / 0 | 18 / 9 / 1 |
| R1 | sequence | 9 / 3 / 0 | 22 / 4 / 0 |
| R2 | gemini-3.1-pro vs claude-opus-4-6 | 3 / 3 / 1 | 10 / 2 / 1 |
| R2 | gpt-5.2 vs claude-opus-4-6 | 4 / 3 / 0 | 8 / 5 / 1 |
| R2 | qwen3.5-397b-a17b vs qwen3.5-27b | 5 / 2 / 0 | 10 / 2 / 1 |
| R2 | qwen3.5-9b vs qwen3.5-27b | 5 / 2 / 0 | 10 / 4 / 0 |
| R2 | class | 8 / 7 / 1 | 17 / 9 / 2 |
| R2 | sequence | 9 / 3 / 0 | 21 / 4 / 1 |

## Pairs where both raters chose against the metric

| Pair | Comparison | Type | Metric prefers | What differs (written by the author) | Kind |
|---|---|---|---|---|---|
| P06 | gpt-5.2 vs claude-opus-4-6 | class | claude-opus-4-6 | Relationship F1 0.77 against 0.78. GPT misses 2 dependencies, draws 1 dependency solid and changes 1 realization to a dependency; Claude misses 5 dependencies. | very small gap |
| P12 | qwen3.5-397b-a17b vs qwen3.5-27b | sequence | qwen3.5-27b | The ground truth is one message from lice to Bob. The 27B answer draws four classes with two dependency arrows; the 397B answer is a sequence diagram that reads lice as Ice. | content not scored: diagram type |
| P13 | qwen3.5-9b vs qwen3.5-27b | class | qwen3.5-9b | The 9B answer draws all three inheritances as plain arrows. The 27B answer has the right inheritances but six extra classes (its aliases drawn again as classes). | metrics disagree |
| P16 | gemini-3.1-pro vs claude-opus-4-6 | sequence | claude-opus-4-6 | Gemini writes Transport where the image says Tansport, which costs two elements. Claude draws many messages as self-messages. | metrics disagree |
| P18 | gpt-5.2 vs claude-opus-4-6 | class | claude-opus-4-6 | GPT adds a note Type, Params (the whole Element F1 gap) and draws the three solid uses arrows dashed. Claude reverses one link and puts one class outside its package. | note counted as element |
| P22 | gpt-5.2 vs claude-opus-4-6 | class | claude-opus-4-6 | GPT writes DataMax5GPLan as a second line of the class name, where the ground truth has it as an attribute, so three links fail to match. Claude misses one link and attaches another to the wrong class. | one name differs |
| P32 | qwen3.5-397b-a17b vs qwen3.5-27b | sequence | qwen3.5-27b | Both answers have all participants. The 27B answer writes participant names in cyan on cyan boxes, so no name can be read, and adds a stray note. | content not scored: unreadable names |
| P33 | gpt-5.2 vs claude-opus-4-6 | class | gpt-5.2 | Relationship F1 0.55 against 0.53. Claude draws the compositions of Logic as plain arrows. GPT keeps them as compositions but reverses them, and draws the compositions to Game as dependencies. | very small gap |
| P34 | qwen3.5-397b-a17b vs qwen3.5-27b | class | qwen3.5-27b | The 397B answer has every relationship right and adds six notes. The 27B answer turns one aggregation into an inheritance. | note counted as element |
| P35 | qwen3.5-9b vs qwen3.5-27b | sequence | qwen3.5-9b | The 27B answer drops one character from the database name, so all messages of the database fail to match. The 9B answer adds an extra participant and turns one message into a self-message. | one name differs |
| P37 | gemini-3.1-pro vs claude-opus-4-6 | class | claude-opus-4-6 | Gemini keeps the private markers on all attributes and adds one duplicate plain link. Claude has the exact link but no visibility markers. | content not scored: members |
| P39 | gemini-3.1-pro vs claude-opus-4-6 | class | claude-opus-4-6 | Element F1 1.00 against 0.97, Relationship F1 0.47 against 1.00. Claude draws the compositions it keeps as plain arrows and leaves out about six links, the aggregation among them. | metrics disagree |
| P41 | gpt-5.2 vs claude-opus-4-6 | class | gpt-5.2 | The ground truth has a long note. GPT leaves it out; Claude copies it with the section markers changed, which counts as one wrong and one extra element. | note counted as element |
| P49 | gemini-3.1-pro vs claude-opus-4-6 | class | claude-opus-4-6 | Gemini moves (Plugin) and ((Translations)) from the names into the stereotypes, so all three links fail to match although the arrows are right. Claude has the exact names but reverses one link. | one name differs |
| P57 | qwen3.5-9b vs qwen3.5-27b | class | qwen3.5-9b | The 9B answer draws one aggregation as an inheritance. The 27B answer draws both aggregations as compositions and keeps the interface marks. | no partial credit for a close arrow kind |

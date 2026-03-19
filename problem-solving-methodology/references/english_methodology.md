Structured Problem-Solving Methodology

Why is this needed?

When AI agents encounter problems, they easily fall into the trap of “quick guessing and quick fixing”—immediately forming hypotheses upon seeing a phenomenon and taking action to modify it, only to find the modification wrong, leading to more guessing and more fixing, with the total time spent on repeated trial and error far exceeding the time for a single in-depth analysis.

This methodology provides a structured problem-solving process, suitable for non-obvious problems (scenarios that require guessing the cause, involve multiple component interactions, or where modification is risky).

---

Scope of Application

Scenarios where this methodology should be used

* The cause of the problem is not immediately apparent and requires some speculation.
* Involves multiple component/system interactions
* Modifications may have side effects or be irreversible.

Previous attempts to fix it have failed.

* The user explicitly requests analysis before taking action.

Scenarios where this methodology is not needed (direct fix is ​​sufficient)

* Problems that are immediately obvious (typo, obvious configuration error, known pattern)
* There is a clear error message and a corresponding unique solution.
* The user explicitly says “direct fix.”

---

Process: Six-Step Method

Step 1: Define the Problem

Goal: Transform the vague statement “a problem has occurred” into a precise problem statement.

What to Do:

1. Record the Phenomenon: What happened? When did it happen? What was the scope of its impact?
2. Record the Expectations: What should have happened?
3. Record the Difference: What is the gap between the phenomenon and the expectations?
4. Confirm Reproducibility: Is it sporadic or reproducible? What are the triggering conditions?

Output Format:

Problem Statement: [One-sentence description]
Phenomenon: [Specific manifestations]
Expectation: [What should the correct behavior be?]
Impact: [Who is affected, severity]
Reproducibility: [Yes/No, triggering conditions]

Common Mistakes:

* ❌ Treating an assumption as a problem (“Origin is contaminated” is an assumption, not a problem)
* ❌ Skipping this step and starting to fix it directly (starting without clearly defining the problem)
* ✅ “The webchat reply also appears in the DingTalk group chat” is the real problem.

---

Step Two: Diagnose

Goal: Find the root cause, not just the symptoms.

What to Do:

2.1 Draw the Data Flow / Call Chain

From input to output, what steps does the data go through, and what does each step do?


↓ ↓ ↓

Normal? Normal? Normal?


2.2 Step-by-Step Verification

For each step, check if the actual value matches expectations:

* Read logs, configurations, and source code, print intermediate states.
* Don’t guess, see the actual data.

2.3 Narrowing Down the Scope

Use binary search or elimination:

* At which step’s output started to be abnormal?
* Upstream normal + This step abnormal = The problem is here.

2.4 Identifying the Root Cause

* Ask yourself three questions:
1. Why did this happen? (Mechanism-level explanation)
2. Will changing this part definitely eliminate the problem? (Sufficiency)
3. Without changing this part, are there other reasons that could cause the same problem? (Uniqueness)

Diagnostic Tool Priorities:

1. Logs / Error Messages (Fastest)
2. Intermediate State Checks (Reading Database, Configuration Files, Session State)
3. Source Code Tracing (Most Reliable but Slowest)
4. Experimental Verification (Constructing a Minimal Reproducibility Scenario)

Common Mistakes:

* ❌ Drawing conclusions after only examining one aspect
* ❌ Using assumptions starting with “maybe” as conclusions
* ❌ Changing one part without reflection, continuing to guess at the next without considering why
* ✅ Draw the call chain, verify each step, and locate the exact line of code.

---

Step 3: Solution Design

Objective: Propose multiple alternative solutions, compare and evaluate them, and select the optimal one.

What to Do:

3.1 List Candidate Solutions (at least 2)

* Describe “what” of each solution in one sentence.
* Include “no fix/bypass” options (sometimes the best solution is not to modify).

3.2 Multi-Dimensional Evaluation

| Dimension | Description |

|------|------|

| Effectiveness | Can it completely solve the problem? Or is it only a temporary fix?

| Risk | Will it introduce new problems? Will it affect other functions?

| Complexity | How much modification is required? How many components are involved?

| Reversibility | Can it be rolled back if a mistake is made?

| Persistence | Is it a long-term effective solution or a temporary one? Will it be overwritten?

| Side Effects | What is the impact on other functions/scenarios?

3.3 Providing Recommendations

* Explaining the Reasons for the Recommendation
* Explaining the Selected Trade-off

Output Format:


Advantages: ...

Risks: ...

Recommendation: ⭐⭐⭐

Solution B: [Description]

Advantages: ...

Risks: ...

Recommendation: ⭐⭐

Solution A is recommended because [Reasons]


Common Mistakes:

* ❌ Starting with only one solution (lack of confidence without comparison)
* ❌ Evaluating solutions based solely on “whether it solves the problem,” ignoring side effects and risks
* ❌ Recommending solutions without clearly explaining the trade-off

---

Step Four: Confirm Execution

Objective: Safely implement the repair, with a rollback plan in place.

What to do:

4.1 Pre-execution checks

[ ] Root cause identified (not guesswork)
[ ] Solution evaluated (not arbitrary)
[ ] User confirmed (external operations/risky modifications)
[ ] Rollback plan prepared (what if a mistake is made)

4.2 Minimize modifications

* Only modify necessary parts; avoid unnecessary modifications.
* Modify only one variable at a time for easy verification.

4.3 Change log

* What was changed, why was it changed, and what was the original value?
* Facilitates rollback and subsequent auditing

Common mistakes:

* ❌ Modifying multiple places at once makes it difficult to distinguish which one took effect
* ❌ Not recording the original value before modification, making rollback impossible
* ❌ Not informing the user after modification (especially operations requiring a restart)

---

Step 5: Verification

Goal: Confirm that the problem is truly resolved and no new problems have been introduced.

What to Do:

5.1 Direct Verification

* Reproduce the original triggering conditions to confirm that the problem no longer occurs.
* Check the actual status of the modified points (don’t just say “it should be fine now,” you need to see evidence).

5.2 Regression Verification

* Are the related functions working properly?
* Are other scenarios affected?

5.3 Persistence Verification

* Is it still effective after a restart?
* Is it still effective when the triggering conditions occur again?

Common Mistakes:

* ❌ Saying “it should be fixed” after making changes without verification
* ❌ Only verifying the repaired scenario without checking related functions
* ❌ Declaring a fix after one verification without considering persistence

---

Step Six: Summary and Review

Goal: Extract lessons learned to avoid repeating similar problems.

What to Do:

6.1 Incident Summary

* What was the problem? What was the root cause? How was it fixed?
* How long did it take from discovery to fix?
* How much of that was effective time and how much was wasted time?

6.2 Process Reflection

* Which steps were done correctly?
* Which steps were taken incorrectly? Why?
* If you could do it again, how could you do it faster?

6.3 Rule Extraction

* What common patterns did this problem expose?
* What new checks/rules need to be added? - Write to .learnings/ or AGENTS.md

Output Format:

## Review: [Problem Name]

- Time Spent: X minutes (Y minutes effective, Z minutes wasted time)

- Root Cause: [One sentence]

- Fix: [One sentence]

- Detours: [What detours were taken, and why]

- Lessons Learned: [Retrieved Rules]


---

Quick Reference: Problem Classification and Response

| Level | Characteristics | Response |

|------|------|------|

| L1 Obvious | Cause and fix are immediately apparent | Direct fix |

| L2 Requires Investigation | Cause uncertain, but scope limited | Simplified process: Define → Diagnose → Fix → Verify |

| L3 Complex/High-Risk | Multi-component interaction, risky modifications, previous incorrect fixes | Complete six-step process |

Judgment Criteria:

* If you need to say “it might be…” to give a cause → At least L2
* If it involves the interaction of more than 2 components → At least L2
* If the incorrect fix will affect user/data security → L3
* If a fix attempt has already failed → Upgrade to L3

---

Anti-patterns List

| Anti-pattern | Manifestation | Correct Practice |

|--------|------|----------|

| Guess and Fix | Form a hypothesis and act immediately upon seeing the phenomenon | Draw the call chain first, verify each step |

| Look at Only One End | Only check the input or output, not the intermediate process | Trace the data flow end-to-end |

| Symptom Fix | Change the visible outlier without finding the reason for the outlier | Ask “Why did it become this value?” |

| Fix First, Then Talk | Change and see the effect, guess only if there’s no effect | Change only after confirming the root cause |

| Change Multiple Places at Once | Change several places simultaneously | One variable at a time |

| Announcing Fix | Say “It’s fixed” after making changes without verification | You must see evidence |

| Forgetting to Roll Back | Don’t record the original value, you can’t undo the mistake | Back up/record first, then modify |

---

Communication Principles

Communication with users during problem-solving:

1. Definition Phase: Confirm a shared understanding of the problem (“Your problem is X, is that correct?”)
2. Diagnosis Phase: Keep pace with progress; avoid prolonged silence (“I’m checking step Y and found Z”).
3. Solution Phase: Offer choices, not fill-in-the-blank questions (“Solutions A and B, I recommend A because…”).
4. Execution Phase: Confirm any risky operations first (“Does it need to be restarted? Confirm?”).
5. Verification Phase: Ask the user for assistance in verification (“Please check if it’s working properly on your end.”).
6. Throughout the Process: Acknowledge uncertainty (“I’m not sure if this is the cause; verifying first is much more reliable than saying ‘This is the cause.’”)



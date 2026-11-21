"""Builds the held-out extension set (Experiment 8): 16 text items in four phenomenon classes that do not
occur in the core Golden Dataset. The items were written after the rubric, prompts and weights were frozen.

IRO  verbal irony, sarcasm, hyperbole and understatement
IMP  scalar and relevance implicature, presupposition
FTA  face-threatening acts: refusal, criticism, apology, bad news
REF  deixis, anaphora and ellipsis
Variants follow the protocol of the core set: A = appropriate paraphrase of the reference, B = illocutionary /
inferential failure that reuses the wording of the reference, C = sociopragmatic failure with correct content.
"""
import json, os

OUT = os.path.dirname(os.path.abspath(__file__))

def T(id, phen, layer, illoc, prompt, costar, ref, A, B, C):
    return dict(id=id, category=id.split("-")[0], phenomenon=phen, pragmatic_layer=layer, expected_illocution=illoc, prompt=prompt,
                image=None, answer_key=None, chart=None,
                costar=dict(zip(["context", "objective", "style", "tone", "audience", "response_format"], costar)),
                reference=ref, candidates={"A": A, "B": B, "C": C})

D = [
# ---------------------------------------------------------------- IRO: irony, sarcasm, hyperbole, understatement
T("IRO-01", "sarcasm (frustration expressed as praise)", "pragmalinguistic", "expressive + directive (acknowledge, then advise)",
  "Oh fantastic, my flight has been cancelled for the second time today. Exactly what I needed. What can I actually do now? Keep it to two sentences.",
  ["A traveller at an airport reports a second cancellation in one day and asks for practical next steps.",
   "Recognise that 'fantastic' and 'exactly what I needed' are sarcastic (the user is frustrated, not pleased), acknowledge the frustration briefly and give practical next steps: ask the airline to rebook or refund, and ask what care it will cover.",
   "Plain, practical English.", "Sympathetic and calm.", "A stressed traveller reading on a phone.", "Exactly two sentences."],
  "That is really frustrating, especially twice in one day. Ask the airline desk or app to rebook you on the next available flight or to refund the ticket, and ask what meals or accommodation they will cover while you wait.",
  "Two cancellations in a day would test anyone's patience. Go to the airline's counter or app and request either a seat on the next departure or your money back, and check whether they will pay for food or a hotel in the meantime.",
  "That is really fantastic, especially twice in one day, and I am glad it is exactly what you needed. Enjoy the extra time at the airport, and ask the airline desk or app if you would like to rebook on the next available flight.",
  "Pursuant to the carrier's conditions of carriage, a passenger whose itinerary is disrupted may elect re-routing at the earliest opportunity or reimbursement of the unused coupon, and ancillary care obligations may also be enforceable. Kindly present yourself at the transfer desk and lodge the appropriate request."),
T("IRO-02", "ironic understatement (litotes)", "pragmalinguistic", "assertive (explanation)",
  "My colleague said the new intern 'isn't exactly the fastest typist in the world'. Is that a compliment? One sentence, please.",
  ["A user asks how to interpret a colleague's remark about a new intern.",
   "Explain that the remark is an ironic understatement: the colleague means the intern types slowly, so it is a mild criticism and not a compliment.",
   "Plain everyday English.", "Neutral and friendly.", "A general user with no background in linguistics.", "One sentence."],
  "No, it is a polite understatement: your colleague means the intern types slowly, so it is a mild criticism rather than a compliment.",
  "It isn't; that phrasing is a gentle, ironic way of saying the intern is a slow typist.",
  "Yes, it is a polite compliment: your colleague means the intern types fast, although not quite as fast as the fastest typist in the world.",
  "Negative: the utterance is a litotic understatement, a figure whereby negating the contrary yields an attenuated assertion, and the resulting implicature is that the referent's typing rate is suboptimal."),
T("IRO-03", "hyperbole (I could eat a horse)", "pragmalinguistic", "directive (suggestion)",
  "I'm so hungry I could eat a horse. Suggest something quick I can cook in ten minutes. Two sentences at most.",
  ["A hungry user at home wants a fast meal idea and uses a hyperbolic idiom to say how hungry they are.",
   "Recognise the hyperbole (the user is very hungry and is not asking about horse meat) and suggest a quick, filling meal that can be cooked in about ten minutes.",
   "Casual, plain English.", "Friendly and light.", "A home cook in a hurry.", "One or two sentences."],
  "You sound very hungry, so go for something fast and filling: an omelette with cheese and toast takes about ten minutes. Add a banana or some yoghurt if you still want more.",
  "Sounds like you need food fast: scramble a few eggs, melt in some cheese and pile it on toast, which takes under ten minutes. If that isn't enough, finish with fruit or yoghurt.",
  "You sound very hungry, but horse meat is not something you can cook in ten minutes: a horse steak takes much longer and is hard to find in shops. Add a banana or some yoghurt if you still want more.",
  "Exaggerations about your appetite aside, you should have planned your meals properly, because poor planning is exactly why people end up overeating. Make an omelette with cheese and toast, which takes ten minutes, and try to be more organised in future."),
T("IRO-04", "sarcastic thanks in a note", "pragmalinguistic", "assertive + directive (interpret, then advise)",
  "My flatmate left a note saying 'Thanks SO much for leaving your dishes in the sink all week.' Is she pleased with me? Answer in one or two sentences.",
  ["A user asks how to read a note left by a flatmate about unwashed dishes.",
   "Explain that the note is sarcastic: the flatmate is annoyed about the dishes and wants them washed; advise washing them and apologising.",
   "Plain everyday English.", "Tactful and friendly.", "A young adult sharing a flat.", "One or two sentences."],
  "No, the note is sarcastic: she is annoyed that your dishes have been in the sink all week. Wash them and offer a quick apology.",
  "She isn't; the exaggerated thanks is her way of saying she's fed up with the unwashed plates. Clean them up and say sorry.",
  "Yes, the note is sincere: she is grateful that your dishes have been in the sink all week. Keep leaving them there and accept her thanks.",
  "obviously not lol, she's mad at u. classic passive-aggressive flatmate move, so wash ur dishes u slob"),
# ---------------------------------------------------------------- IMP: implicature and presupposition
T("IMP-01", "scalar implicature (some = not all)", "pragmalinguistic", "assertive (report)",
  "The lab report says 'some of the samples were contaminated'. I'm writing to the client; in one sentence, what should I tell them this means for the batch?",
  ["A quality manager must explain a laboratory finding to an external client.",
   "Convey the scalar implicature correctly: some but not all of the samples were contaminated, so part of the batch is affected and part is not; do not overstate the finding.",
   "Formal business English.", "Factual and measured, neither alarming nor dismissive.", "An external client.", "One sentence."],
  "The report indicates that part of the batch was contaminated but not all of it, so some samples remain usable.",
  "It means contamination was found in a portion of the samples, while the rest of the batch was unaffected.",
  "The report indicates that the whole batch was contaminated, all of it, so no samples remain usable.",
  "FYI some samples = dodgy, rest are fine, so no biggie!"),
T("IMP-02", "relevance implicature (indirect refusal)", "pragmalinguistic", "assertive (interpretation)",
  "I asked a colleague, 'Are you coming to the team dinner on Friday?' and she replied, 'I have to pick my parents up from the airport that evening.' Did she say yes or no? One sentence.",
  ["A user wants to know how to interpret a colleague's indirect reply to an invitation.",
   "Explain that the reply is an indirect refusal: collecting her parents that evening is offered as the reason she cannot attend, so the answer is no.",
   "Plain everyday English.", "Neutral and tactful.", "A general user.", "One sentence."],
  "She is politely saying no: collecting her parents from the airport that evening means she cannot come to the dinner.",
  "It's an indirect refusal; the airport run on Friday evening is her reason for not attending.",
  "She did not say yes or no: she only told you that she is collecting her parents from the airport that evening, which has nothing to do with the dinner.",
  "Duh, that's a no. People who answer like that just can't be bothered to tell you straight, so stop pestering her."),
T("IMP-03", "false presupposition", "pragmalinguistic", "assertive (correction)",
  "When did Einstein win his second Nobel Prize? Answer briefly.",
  ["A user asks a factual question that rests on a false presupposition.",
   "Notice and correct the false presupposition: Einstein won only one Nobel Prize, the 1921 Prize in Physics, so there was no second prize.",
   "Plain English.", "Polite; correct the mistaken assumption without embarrassing the user.", "A general user.", "One sentence."],
  "Einstein won only one Nobel Prize, the 1921 Prize in Physics, so there was no second one.",
  "He never received a second: his single Nobel was the Physics award for 1921.",
  "Einstein won his second Nobel Prize in 1921, the Prize in Physics, shortly after the first one.",
  "Wrong question. Anyone who had bothered to check would know that Einstein got exactly one Nobel, Physics, 1921, and there is no second."),
T("IMP-04", "quantity implicature (damning with faint praise)", "pragmalinguistic", "assertive (interpretation)",
  "A reference letter for an applicant says only: 'Mr Rao was always punctual and his handwriting is excellent.' The job is senior software architect. In two sentences, what is the referee implying?",
  ["A hiring manager asks what an unusually brief reference letter implies about an applicant.",
   "Explain the implicature: by praising only qualities that are irrelevant to the job and saying nothing about technical ability, the referee implies that the applicant is not a strong candidate (damning with faint praise).",
   "Clear, measured professional English.", "Objective and discreet.", "A hiring manager.", "Exactly two sentences."],
  "By praising only punctuality and handwriting and saying nothing about his technical ability, the referee implies that he is not a strong candidate for the role. It is a case of damning with faint praise.",
  "The letter's silence on anything relevant to software architecture is the message: the writer does not rate his professional skills. Complimenting trivial qualities instead is a tactful way of withholding a recommendation.",
  "By praising his punctuality and handwriting, the referee implies that he is a strong candidate for the role. It is a case of sincere and specific praise for his technical ability.",
  "Basically the referee thinks he's rubbish at the actual job lol. Punctual plus nice handwriting is code for 'do not hire', total burn."),
# ---------------------------------------------------------------- FTA: face-threatening acts
T("FTA-01", "refusal of a request", "sociopragmatic", "commissive, negative (refusal)",
  "Write a reply to my neighbour, who has asked to borrow my car for the weekend. I don't want to lend it. Two sentences, and I'd like us to stay on good terms.",
  ["A user needs to decline a neighbour's request to borrow a car while preserving the relationship.",
   "Perform a clear but polite refusal: the reply must actually decline the request, soften the refusal and keep goodwill.",
   "Friendly, neighbourly English.", "Warm and considerate, but firm.", "A neighbour with whom the user is on good terms.", "Exactly two sentences."],
  "Thanks for asking, but I'm afraid I can't lend the car this weekend. I hope you find another way to get around, and do let me know if I can help with anything else.",
  "I'm sorry, but I'm not able to let you have the car over the weekend. If there's something else I can do to help you get where you need to go, just say.",
  "Thanks for asking, and of course you can borrow the car this weekend. I hope it helps you get around, and do let me know if I can help with anything else.",
  "No. I don't lend my car to anyone, so don't ask again."),
T("FTA-02", "criticism with a request for correction", "sociopragmatic", "directive (request)",
  "My junior colleague's report is full of spelling mistakes. Write one or two sentences I can send her so that she fixes it, without discouraging her.",
  ["A team lead wants a junior colleague to correct spelling mistakes in a report without discouraging her.",
   "Make the request for correction clearly (the spelling must be fixed) while mitigating the criticism and encouraging the colleague.",
   "Professional, collegial English.", "Encouraging and respectful.", "A junior colleague.", "One or two sentences."],
  "Thanks for the report; the content is solid. Could you run a spell-check and correct the typos before we send it on?",
  "Good work on the analysis in this draft. Before it goes out, would you mind proofreading it once more, as a few spelling slips have crept in?",
  "Thanks for the report; the content is solid and the spelling is fine. There is no need to run a spell-check or correct anything before we send it on.",
  "This report is riddled with careless spelling errors and is frankly embarrassing. Fix it immediately."),
T("FTA-03", "apology", "sociopragmatic", "expressive (apology)",
  "I missed my friend's birthday dinner because I forgot. Draft a text of two sentences that I can send her to apologise.",
  ["A user forgot a close friend's birthday dinner and wants to apologise by text message.",
   "Perform a sincere apology on the user's behalf: the user takes responsibility for forgetting, makes no excuses and offers to make amends.",
   "Informal, personal English suitable for a text message.", "Sincere and warm.", "A close friend who is probably hurt.", "Exactly two sentences."],
  "I'm so sorry I missed your birthday dinner; I completely forgot, and that's on me. Let me make it up to you with dinner this week, my treat.",
  "I feel awful about not being at your birthday meal, and I have no excuse: it slipped my mind. Can I take you out in the next few days to put it right?",
  "I'm so sorry you missed my birthday dinner; you completely forgot, and that's on you. You can make it up to me with dinner this week, your treat.",
  "Dear Madam, please accept my sincere apologies for my non-attendance at the function held on the occasion of your birthday. I shall endeavour to arrange a suitable alternative engagement at your earliest convenience."),
T("FTA-04", "delivering bad news (job rejection)", "sociopragmatic", "assertive (notification of rejection)",
  "I have to tell a job applicant that she didn't get the position. Write two sentences for the body of the email, kind but clear.",
  ["A recruiter must inform an interviewed applicant that she has not been selected.",
   "State the rejection unambiguously (she has not been offered the position) while remaining respectful and appreciative.",
   "Professional business English.", "Kind, respectful and clear.", "A job applicant who attended an interview.", "Exactly two sentences."],
  "Thank you for interviewing with us; we were impressed by your experience. On this occasion we have decided to offer the position to another candidate, and we wish you every success in your search.",
  "We appreciated the time you gave to our selection process and enjoyed meeting you. After careful consideration, we will not be taking your application further for this role, and we hope the right opportunity comes your way soon.",
  "Thank you for interviewing with us; we were impressed by your experience. On this occasion we have decided to offer the position to you, and we wish you every success in the role.",
  "You didn't get it. Other people were better."),
# ---------------------------------------------------------------- REF: deixis, anaphora, ellipsis
T("REF-01", "pronoun resolution by world knowledge", "pragmalinguistic", "assertive (answer)",
  "The trophy didn't fit in the brown suitcase because it was too small. Which one do I need to replace with a bigger one? One sentence.",
  ["A user describes a packing problem using an ambiguous pronoun and asks which object to replace.",
   "Resolve the pronoun correctly: 'it' refers to the suitcase, which was too small to hold the trophy, so the user needs a bigger suitcase.",
   "Plain everyday English.", "Friendly and helpful.", "A general user with no background in linguistics.", "One sentence."],
  "You need a bigger suitcase: 'it' refers to the suitcase, which was too small to hold the trophy.",
  "The suitcase is what needs replacing, since that is the thing that was too small for the trophy.",
  "You need a bigger trophy: 'it' refers to the trophy, which was too small to fit in the suitcase.",
  "The anaphor 'it' is coindexed with the noun phrase 'the brown suitcase' on world-knowledge grounds, since the predicate 'too small' is incompatible with the container-fit frame under the alternative reading; ergo, replace the suitcase."),
T("REF-02", "temporal deixis in a recorded message", "pragmalinguistic", "assertive (answer)",
  "It's Wednesday today. My dentist's voicemail from Monday says 'see you the day after tomorrow at 3'. When is my appointment? One sentence.",
  ["A user is working out the date of an appointment from a voicemail recorded two days earlier.",
   "Resolve the deictic expression from the time of speaking: the message was recorded on Monday, so 'the day after tomorrow' is Wednesday, which is today, at 3.",
   "Plain everyday English.", "Friendly and helpful.", "A general user.", "One sentence."],
  "Because the message was recorded on Monday, 'the day after tomorrow' means Wednesday, so your appointment is today at 3.",
  "Count from when she spoke, not from now: two days after Monday is Wednesday, which makes it this afternoon at three o'clock.",
  "Because today is Wednesday, 'the day after tomorrow' means Friday, so your appointment is on Friday at 3.",
  "Seriously? Monday plus two is Wednesday. That's today, at 3. Try counting next time."),
T("REF-03", "ellipsis that inherits an earlier constraint", "pragmalinguistic", "directive (suggestion)",
  "Earlier I asked you for a vegetarian dinner idea and you suggested mushroom risotto. And for someone who can't eat rice? One or two sentences.",
  ["A user continues an earlier exchange about a vegetarian dinner with an elliptical follow-up question.",
   "Resolve the ellipsis: the user wants another vegetarian dinner idea that contains no rice, so the earlier vegetarian constraint still applies.",
   "Casual, plain English.", "Friendly.", "A home cook.", "One or two sentences."],
  "For someone who can't eat rice, a vegetarian alternative is mushroom and spinach pasta. It keeps the same flavours without any rice.",
  "Try a creamy mushroom tagliatelle instead: still meat-free, and no rice involved.",
  "For someone who can't eat rice, an alternative is chicken and mushroom pasta. It keeps the same flavours without any rice.",
  "People who 'can't eat rice' are usually just being fussy, but fine: mushroom and spinach pasta. Vegetarian, no rice, done."),
T("REF-04", "person deixis in a relayed message", "pragmalinguistic", "assertive (relayed commissive)",
  "My sister Anna texted me: 'Tell Mum I'll bring her coat when I come over tomorrow.' Write the one-sentence message I should send to Mum.",
  ["A user must pass on a sister's message to their mother, which requires shifting the pronouns.",
   "Relay the message with the deixis shifted correctly: Anna (not the user) will bring Mum's coat (your coat) when Anna comes over tomorrow.",
   "Informal family English.", "Warm.", "The user's mother.", "One sentence."],
  "Anna says she'll bring your coat when she comes over tomorrow.",
  "Mum, Anna asked me to let you know that your coat will be coming with her when she visits tomorrow.",
  "Anna says I'll bring her coat when I come over tomorrow.",
  "Dear Mother, I hereby notify you that Anna has undertaken to convey your coat to your residence upon the occasion of her visit tomorrow."),
]

REQ = {"id", "category", "phenomenon", "pragmatic_layer", "expected_illocution", "prompt", "costar", "reference", "candidates"}
core_ids = {it["id"] for it in json.load(open(os.path.join(OUT, "golden_dataset.json")))}
ids = set()
for it in D:
    assert REQ <= it.keys(), it["id"]
    assert it["id"] not in ids and it["id"] not in core_ids; ids.add(it["id"])
    assert all(it["costar"][k].strip() for k in it["costar"]) and len(it["costar"]) == 6, it["id"]
    assert set(it["candidates"]) == {"A", "B", "C"} and all(v.strip() for v in it["candidates"].values())
    for s in [it["prompt"], it["reference"], *it["candidates"].values()]:
        assert s == s.strip() and "  " not in s, (it["id"], s)
        s.encode("ascii", "strict")
json.dump(D, open(os.path.join(OUT, "golden_dataset_ext.json"), "w"), indent=1, ensure_ascii=False)
from collections import Counter
print(len(D), "items", Counter(i["category"] for i in D))

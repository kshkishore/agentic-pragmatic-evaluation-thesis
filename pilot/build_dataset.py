"""Builds the Golden Dataset (JSON) and renders the chart stimuli from source data.

Every multimodal item is rendered from a data table stored in the item itself, so the
answer key is exact by construction (the image and the key come from the same numbers).
"""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(OUT, "images"); os.makedirs(IMG, exist_ok=True)

def T(id, phen, layer, illoc, prompt, costar, ref, A, B, C, image=None, key=None, chart=None):
    return dict(id=id, category=id.split("-")[0], phenomenon=phen, pragmatic_layer=layer,
                expected_illocution=illoc, prompt=prompt, image=image, answer_key=key, chart=chart,
                costar=dict(zip(["context", "objective", "style", "tone", "audience", "response_format"], costar)),
                reference=ref, candidates={"A": A, "B": B, "C": C})

D = []
# ---------------------------------------------------------------- IDI: idioms / figurative language
D += [
T("IDI-01", "idiom: make or break", "pragmalinguistic", "assertive (explanation)",
  "My manager just told me the client meeting tomorrow is 'make or break'. In two sentences, what is she telling me?",
  ["An employee asks what a manager's idiomatic remark about tomorrow's client meeting means.",
   "Explain the non-literal meaning of 'make or break' (the meeting is decisive: it will lead to success or failure) and what it implies for the employee (prepare carefully).",
   "Plain, professional English.", "Supportive and calm.", "An employee seeking workplace guidance.", "Exactly two sentences."],
  "She means tomorrow's meeting is decisive: it will either secure the client relationship or lose it. She is signalling that you should prepare thoroughly because the stakes are unusually high.",
  "She's saying the outcome of that single meeting will determine whether the deal succeeds or collapses. In other words, treat it as high-stakes and come fully prepared.",
  "She is telling you the meeting will either make something or break something, possibly equipment in the meeting room. She means you should be careful tomorrow not to break anything at the client's office.",
  "lol it's do-or-die mate, basically if u mess it up ur toast. so yeah no pressure haha"),
T("IDI-02", "idiom: reinvent the wheel", "pragmalinguistic", "assertive (explanation)",
  "A colleague wrote 'Let's not reinvent the wheel' in reply to my proposal for a new filing system. What is he suggesting? Answer in one or two sentences.",
  ["An office worker received an idiomatic reply to a proposal for a new filing system.",
   "Explain that the colleague suggests using or adapting an existing system instead of creating a new one from scratch.",
   "Plain everyday English.", "Neutral and helpful.", "An office worker with no linguistics background.", "One or two sentences."],
  "He is suggesting that you use or adapt an existing filing system rather than designing a new one from scratch, because a workable solution already exists.",
  "He thinks a perfectly good system is already available, so building your own would waste effort; he'd prefer to adopt or tweak what's there.",
  "He is suggesting that your proposal for a new filing system should include a wheel, since a wheel already exists and would not need to be designed from scratch.",
  "The interlocutor's utterance constitutes a deprecatory directive grounded in the principle of non-duplication of extant artefactual solutions within the organisational repertoire."),
T("IDI-03", "idiom: take it with a pinch of salt", "pragmalinguistic", "assertive (explanation)",
  "My grandmother says I should 'take it with a pinch of salt' when my cousin gives investment advice. What does she mean? Keep it short and friendly.",
  ["A young adult asks about a grandmother's idiomatic warning regarding a cousin's investment advice.",
   "Explain that the grandmother means the advice should not be fully trusted and should be treated with scepticism or checked.",
   "Conversational English.", "Friendly and warm.", "A young adult family member.", "Short: one or two sentences."],
  "She means you shouldn't fully believe or rely on your cousin's investment advice; treat it with some scepticism and check it before acting on it.",
  "She's gently warning you not to accept everything your cousin says about investing at face value: listen, but double-check before you put any money in.",
  "She means you should take a small pinch of salt when your cousin gives you investment advice, perhaps adding it to your food while you listen and check the advice.",
  "Your grandmother is asserting that the epistemic reliability of your cousin's financial recommendations is insufficient to warrant uncritical acceptance; accordingly, a discounting heuristic should be applied to all such inputs."),
T("IDI-04", "idiom: miss the boat", "pragmalinguistic", "assertive (explanation)",
  "My team lead said my report 'missed the boat'. I'm not a native English speaker. Can you explain simply what she meant?",
  ["A non-native speaker of English asks about a team lead's idiomatic comment on a report.",
   "Explain that the report came too late: the opportunity it was meant for had already passed.",
   "Simple, clear English with common words.", "Patient and supportive.", "A non-native English speaker.", "Brief: one or two simple sentences."],
  "She meant your report came too late: the opportunity it was meant for had already passed, so it could no longer have the intended effect.",
  "She was saying the timing was off. By the time your report arrived, the chance to use it had already gone.",
  "She meant your report came too late for the boat: the boat it was meant for had already left the dock, so the report could not be loaded onto it.",
  "This idiom denotes a temporal misalignment between deliverable submission and the window of strategic opportunity, that is, suboptimal latency relative to organisational decision cycles."),
T("IDI-05", "idiom: break a leg", "pragmalinguistic", "assertive (reassurance)",
  "In a WhatsApp group, my friend replied 'break a leg!' when I said I have my job interview tomorrow. Was she being rude? One or two sentences please.",
  ["A person is unsure whether a friend's idiomatic reply before a job interview was rude.",
   "Reassure the user that 'break a leg' is a friendly way of wishing good luck, so the friend was not rude.",
   "Conversational English.", "Warm and reassuring, never condescending.", "A slightly anxious person before a job interview.", "One or two sentences."],
  "No, she wasn't being rude: 'break a leg' is a friendly way of wishing someone good luck, especially before a performance or an important event like your interview.",
  "Not at all. It's a cheerful idiom that means 'good luck', so she was encouraging you before the interview.",
  "Yes, she was being rude: 'break a leg' is a way of wishing that someone breaks their leg, especially before a performance or an important event like your interview.",
  "Obviously not. Everyone knows 'break a leg' just means good luck; you really should learn basic English expressions before a job interview."),
T("IDI-06", "idiom: red herring", "pragmalinguistic", "directive-compliance (advice)",
  "My professor wrote on my draft: 'This section is a bit of a red herring.' What should I do about that section? Two sentences.",
  ["A graduate student asks how to act on a professor's idiomatic feedback on a thesis draft.",
   "Explain that the section distracts from the main argument, and advise cutting it or tying it clearly to the thesis.",
   "Academic advisory register.", "Constructive and respectful.", "A graduate student.", "Exactly two sentences."],
  "Your professor thinks the section distracts from your main argument because it leads the reader away from the central point. You should cut it or shorten it and connect it clearly to your thesis.",
  "The comment means that section pulls attention away from your core argument without really helping it. Consider removing it, or rework it so that it visibly supports your main claim.",
  "Your professor thinks the section is about a red fish, a herring, so the reader expects a point about fish. You should add more detail about the herring and connect it clearly to your thesis.",
  "bro ur prof is basically saying that bit is pointless lol. just yeet it"),
T("IDI-07", "idiom: play it by ear", "pragmalinguistic", "assertive (advice)",
  "A client emailed: 'We're happy to play it by ear on the timeline.' Should I send them a fixed schedule? Answer briefly.",
  ["A professional asks how to respond to a client's idiomatic remark about project timing.",
   "Explain that 'play it by ear' signals flexibility, so a fixed schedule is not required and a tentative plan is suitable.",
   "Professional English.", "Calm and practical.", "A professional managing a client relationship.", "Brief: one or two sentences."],
  "Not necessarily: 'play it by ear' means they are comfortable deciding the timeline flexibly as things develop, so you can propose a tentative plan rather than a fixed schedule.",
  "No need for a rigid schedule. They're signalling flexibility and would rather adjust the timing as the work unfolds, so a provisional plan should be enough.",
  "Yes, send a fixed schedule: 'play it by ear' means they want the timeline confirmed by ear, as in over a phone call, so a fixed plan rather than a tentative one is expected.",
  "nah they're chill about it, don't stress lol. whatever works"),
T("IDI-08", "idiom: a tough nut to crack", "pragmalinguistic", "assertive (explanation)",
  "The sales director said our new competitor 'is a tough nut to crack'. What does that mean for our sales team? Two sentences.",
  ["A salesperson asks what a director's idiomatic remark about a competitor implies.",
   "Explain that the competitor will be hard to beat or win customers from, so the team should expect sustained effort and a stronger strategy.",
   "Professional business English.", "Measured and motivating.", "A member of a sales team.", "Exactly two full sentences."],
  "It means the competitor's customers or market position will be difficult to win over or beat. Your sales team should expect a hard, sustained effort and plan a stronger strategy.",
  "The director is warning that this rival won't be easy to outcompete because its position is solid. Expect the team to need extra effort and a sharper strategy to gain ground.",
  "It means the competitor sells nuts that are hard to crack, so its products are difficult to open. Your sales team should expect customer complaints and plan a stronger strategy.",
  "Elevated competitive resistance. Implication: increased resource allocation. End of analysis."),
]
# ---------------------------------------------------------------- ISA: indirect speech acts and implicature
D += [
T("ISA-01", "indirect request (ability question)", "pragmalinguistic", "assertive (provide information)",
  "Can you tell me what the capital of Australia is?",
  ["A user asks a factual question phrased as an ability question.",
   "Recognise the conventional indirect request and supply the information: the capital is Canberra.",
   "Plain English.", "Neutral and polite.", "A general user.", "A short direct answer."],
  "The capital of Australia is Canberra.",
  "It's Canberra, not Sydney as many people assume.",
  "Yes, I can tell you what the capital of Australia is.",
  "Canberra, obviously. Pretty basic geography, to be honest."),
T("ISA-02", "indirect question (do you happen to know)", "pragmalinguistic", "assertive (provide information)",
  "Do you happen to know whether 17 is a prime number?",
  ["A user asks a simple mathematical question in an indirect, polite form.",
   "Answer the embedded question: yes, 17 is prime because its only divisors are 1 and 17.",
   "Plain English.", "Friendly.", "A general user asking casually, not a mathematician.", "A short answer of one or two sentences."],
  "Yes, 17 is a prime number, because it is divisible only by 1 and itself.",
  "It is: 17 has no divisors other than 1 and 17, so it's prime.",
  "Yes, I do happen to know whether 17 is a prime number.",
  "17 is in P since for every natural number d with 1 < d < 17, 17 mod d is not 0; therefore 17 is irreducible in Z. QED."),
T("ISA-03", "conversational implicature (Quantity flouting)", "pragmalinguistic", "assertive (interpretation)",
  "My colleague asked whether I liked her presentation, and I said, 'Well, the slides had nice colours.' Did I tell her I liked it? Answer in two sentences.",
  ["A user wants to know what their reply to a colleague implied.",
   "Explain the implicature: praising only the colours implies the user did not like the presentation's substance, and the colleague will probably infer this.",
   "Plain English.", "Honest but kind.", "An adult reflecting on a workplace interaction.", "Exactly two sentences."],
  "Not really: by praising only the colours, you implied that you did not think much of the content of the presentation. She will probably understand that you did not like it overall.",
  "Probably not. Singling out the colours suggests there was little else you could praise, and she is likely to read it as polite disapproval of the presentation itself.",
  "Yes: you told her the slides had nice colours, so you told her you liked the presentation. She will probably understand that you liked it overall.",
  "lmao no, you basically roasted her. savage"),
T("ISA-04", "conversational implicature (Relation)", "pragmalinguistic", "assertive (interpretation)",
  "I asked my landlord if the heating would be fixed this week, and he replied, 'The engineer is very busy this month.' What is he telling me? Keep it to one or two sentences.",
  ["A tenant asks what a landlord's indirect answer means.",
   "Explain the implicature: the heating will probably not be fixed this week because the engineer is unlikely to be available.",
   "Plain English.", "Sympathetic.", "A tenant with no linguistics background.", "One or two sentences."],
  "He is implying that the heating will probably not be fixed this week, because the engineer is unlikely to be available soon.",
  "Reading between the lines, don't expect a repair this week; he's hinting that the engineer won't get to it for a while.",
  "He is telling you that the engineer is very busy this month, which is information about the engineer's schedule.",
  "Pursuant to the Gricean maxim of Relation, the landlord's utterance licenses the defeasible inference that repair within the current week is improbable."),
T("ISA-05", "indirect directive (hint)", "pragmalinguistic", "assertive (interpretation)",
  "I'm writing to my flatmate: 'The kitchen bin is getting quite full.' Will she understand what I'm asking? One or two sentences.",
  ["A user wants to know whether a hint to a flatmate will be understood as a request.",
   "Explain that the statement will most likely be understood as a polite, indirect request to empty the bin.",
   "Plain English.", "Friendly.", "An adult sharing a flat.", "One or two sentences."],
  "Yes, most likely: although it is phrased as a statement, she will probably understand it as a polite request to empty the bin.",
  "Probably. It's an indirect way of asking her to take the rubbish out, and most people will pick up on that.",
  "Yes, she will understand that you are telling her the kitchen bin is getting quite full, which is a statement about the bin.",
  "Indirect directives of this type are conventionally interpreted through inferential uptake, the probability of which is contingent upon mutually manifest background assumptions."),
T("ISA-06", "indirect refusal", "pragmalinguistic", "assertive (interpretation)",
  "I invited a new colleague to Saturday's team lunch and she said, 'Oh, Saturday is a bit difficult for me...' and then smiled. Is she coming? Two sentences.",
  ["A user wonders whether a colleague's hedged reply to an invitation was a refusal.",
   "Explain that this is most likely a polite refusal, and suggest accepting it graciously.",
   "Plain English.", "Empathetic and tactful.", "A colleague who extended an invitation.", "Exactly two sentences."],
  "Probably not: 'a bit difficult' is a common, polite way of declining without saying no directly. It would be kind to accept that and perhaps offer another date.",
  "It sounds like a gentle no; people often soften a refusal this way to avoid sounding rude. You could let it go graciously and suggest a different day sometime.",
  "Yes, probably: 'a bit difficult' means Saturday is only a little difficult, so she is coming. It would be kind to confirm the date and perhaps offer her a lift.",
  "No. She declined. Move on."),
T("ISA-07", "irony / sarcasm", "pragmalinguistic", "assertive (interpretation)",
  "After I spilled coffee on his laptop, my brother said, 'Oh great, just what I needed today.' Is he happy? Answer briefly.",
  ["A user asks how to read a sibling's remark after an accident.",
   "Explain that the remark is sarcastic: the brother is annoyed, not happy.",
   "Plain English.", "Gentle.", "A general adult user.", "Brief: one or two sentences."],
  "No, he is not happy: he is being sarcastic, and he actually means that spilling coffee on his laptop made his day worse.",
  "Not at all. That's sarcasm; he's annoyed, and the remark really means this is the last thing he wanted.",
  "Yes, he is happy: he said 'great' and 'just what I needed', so spilling coffee on his laptop made his day better.",
  "The utterance exhibits ironic polarity inversion; the speaker's affective valence is negative."),
T("ISA-08", "question functioning as complaint", "sociopragmatic", "expressive + commissive (apologise and offer action)",
  "You are a customer-service assistant for an online bookshop. A customer writes: 'I ordered the book two weeks ago. Is it normal that it still hasn't arrived?' Write the reply in at most 60 words.",
  ["A customer-service exchange: a customer's question is really a complaint about a late delivery.",
   "Recognise the complaint: apologise, acknowledge the delay is too long, ask for the order number and offer to track it and arrange a replacement or refund.",
   "Professional customer-service English.", "Apologetic and helpful.", "A dissatisfied customer.", "At most 60 words."],
  "I'm sorry your book hasn't arrived yet; two weeks is longer than it should take. Please send me your order number and I'll check the delivery status right away and arrange a replacement or refund if it has been lost.",
  "I'm really sorry for the delay, which is not the delivery time we aim for. If you share your order number, I'll track the parcel now and, if it's lost, send you a replacement or a refund.",
  "Yes, it is normal that it still hasn't arrived; two weeks is a normal delivery time for a book. Please wait, and send your order number if it has not arrived in another two weeks.",
  "lol yeah the post is a mess rn. send ur order no. and I'll have a look I guess"),
]
# ---------------------------------------------------------------- REG: register, politeness and audience design
D += [
T("REG-01", "request to a superior (academic)", "sociopragmatic", "directive (polite request)",
  "Write a two-sentence email to my PhD supervisor, Professor Rao, asking for a one-week extension on my chapter draft because my fieldwork data arrived late.",
  ["A doctoral student needs to request an extension from a supervisor.",
   "Produce a request (not an announcement) for a one-week extension, giving the reason that fieldwork data arrived late.",
   "Formal academic email.", "Respectful and appropriately deferential.", "A senior academic supervisor.", "An email of exactly two sentences with a suitable salutation."],
  "Dear Professor Rao, I am writing to ask whether I might have a one-week extension on my chapter draft, as my fieldwork data arrived later than expected. I would be grateful for your understanding and can share a revised timeline if helpful.",
  "Dear Professor Rao, because my fieldwork data reached me later than planned, could I kindly request an additional week to submit the chapter draft? Thank you for considering this, and I am happy to send an updated schedule.",
  "Dear Professor Rao, I am writing to inform you that I am taking a one-week extension on my chapter draft, as my fieldwork data arrived later than expected. I will share a revised timeline when it is ready.",
  "Hey Rao! Data came in late so I need another week for the chapter, cool? Cheers."),
T("REG-02", "explanation for a child", "sociopragmatic", "assertive (explanation)",
  "Explain to a seven-year-old why we see lightning before we hear thunder. Two or three short sentences.",
  ["A parent or teacher wants a child-friendly science explanation.",
   "Explain correctly that light travels much faster than sound, so the flash arrives before the sound although both happen at the same time.",
   "Simple, vivid language suitable for a young child.", "Warm and playful.", "A seven-year-old child.", "Two or three short sentences."],
  "Lightning and thunder happen at the same time, but light travels much faster than sound. The flash reaches your eyes almost at once, while the rumble takes longer to reach your ears.",
  "When a storm makes a flash and a bang together, the light zooms to you super fast, but the sound is slow, like a snail racing a rocket. So you see the flash first and hear the boom a little later!",
  "Lightning happens first and thunder happens later, because the sound is made after the light. The flash reaches your eyes first, while the rumble is made later in the clouds.",
  "The speed of light in air is approximately 300,000 kilometres per second, whereas sound propagates at roughly 343 metres per second at 20 degrees Celsius; hence the acoustic signal lags the optical signal by about 2.9 seconds per kilometre."),
T("REG-03", "condolence message", "sociopragmatic", "expressive (condolence)",
  "Write a short condolence message (2 to 3 sentences) to a colleague whose father passed away last week.",
  ["A user wants to express sympathy to a bereaved colleague.",
   "Express condolence and offer support, without introducing unrelated work matters.",
   "Sincere, simple written English.", "Compassionate and gentle.", "A grieving colleague.", "Two or three sentences."],
  "I was so sorry to hear about the loss of your father. Please accept my heartfelt condolences, and know that I am thinking of you and your family. If there is anything I can do to help, please let me know.",
  "I'm deeply sorry about your father's passing. My thoughts are with you and your family during this painful time, and please don't hesitate to reach out if I can support you in any way.",
  "I was sorry to hear about the loss of your father. Please remember that the quarterly report is still due on Friday, and let me know if there is anything you need to finish it on time.",
  "Ah man, sorry about your dad. That sucks. Hang in there!"),
T("REG-04", "declining a senior business partner", "sociopragmatic", "expressive + refusal (mitigated)",
  "I need to decline a dinner invitation from Mr. Tanaka, a senior business partner in Osaka, because I have a prior commitment. Write a polite two-sentence reply.",
  ["A user must decline an invitation from a senior business partner.",
   "Decline the dinner invitation while thanking Mr. Tanaka, giving the prior commitment as the reason and leaving the relationship open.",
   "Formal business correspondence.", "Gracious, appreciative and mitigated.", "A senior business partner.", "Exactly two sentences."],
  "Dear Mr. Tanaka, thank you very much for your kind invitation to dinner; I am truly honoured. Unfortunately, I have a prior commitment that evening, and I sincerely hope we may have the pleasure of dining together on another occasion.",
  "Dear Mr. Tanaka, I am deeply grateful for your generous invitation. Regrettably, an earlier engagement prevents me from attending that evening, but I would be delighted to join you at another opportunity.",
  "Mr. Tanaka, no, I cannot come to dinner because I have a prior commitment that evening. We may have dinner on another occasion.",
  "Hi Tanaka! Can't make dinner, got something else on. Rain check?"),
T("REG-05", "thanking an elder (respect forms)", "sociopragmatic", "expressive (thanks)",
  "Write a WhatsApp message in English to my elderly neighbour, Sharma uncle, thanking him for looking after our plants while we were away. Keep it to two warm, respectful sentences.",
  ["A user wants to thank an elderly neighbour in a South Asian community setting where elders are addressed respectfully.",
   "Thank the neighbour for looking after the plants while the family was away.",
   "Warm, informal-but-respectful message.", "Grateful and affectionate.", "An elderly neighbour addressed respectfully as 'uncle'.", "Exactly two sentences."],
  "Namaste Sharma uncle, thank you so much for taking such good care of our plants while we were away. We are truly grateful for your kindness and help.",
  "Namaste Uncle ji, our plants look so healthy, thank you for caring for them so lovingly while we were travelling. We really appreciate your kindness and will come by to thank you in person.",
  "Namaste Sharma uncle, could you please take good care of our plants while we are away? We will be truly grateful for your kindness and help.",
  "Yo Sharma, thx for the plants bro"),
T("REG-06", "report to a public office", "sociopragmatic", "assertive + directive (report and request)",
  "Write a two-sentence message to the municipal office reporting that the streetlight outside 14 Lake Road has not worked for ten days.",
  ["A resident reports a broken streetlight to a municipal office.",
   "Report that the streetlight outside 14 Lake Road has not worked for ten days and request a repair.",
   "Formal civic correspondence.", "Polite and firm.", "Municipal office staff.", "Exactly two sentences."],
  "Dear Sir or Madam, I would like to report that the streetlight outside 14 Lake Road has not been working for the past ten days. I would be grateful if it could be repaired at the earliest opportunity, as the road is very dark at night.",
  "Dear Sir or Madam, the streetlight in front of 14 Lake Road has been out for ten days now, leaving the stretch unlit after dark. Could you please arrange for it to be fixed as soon as possible?",
  "Dear Sir or Madam, I would like to thank you that the streetlight outside 14 Lake Road has been working for the past ten days. I would be grateful if it could continue, as the road is very dark at night.",
  "Your useless department STILL hasn't fixed the streetlight at 14 Lake Road after TEN DAYS. Fix it now or I'm going to the press."),
T("REG-07", "plain-language health information", "sociopragmatic", "directive (instruction)",
  "Rewrite this sentence for a patient leaflet in plain English (one sentence): 'Patients should refrain from oral intake for eight hours prior to the procedure.'",
  ["A clinic is simplifying a pre-procedure instruction for a patient leaflet.",
   "Preserve the full meaning (no food and no drink for eight hours before the procedure) in plain English.",
   "Plain English suitable for a patient leaflet.", "Clear and courteous.", "Patients with varied health literacy.", "One sentence."],
  "Please do not eat or drink anything for eight hours before your procedure.",
  "For the eight hours before your procedure, don't have any food or drinks.",
  "Please do not eat anything for eight hours before your procedure, but you can drink as much as you like.",
  "Patients are required to observe nil per os status for a period of eight hours antecedent to the procedure."),
T("REG-08", "academic register shift", "sociopragmatic", "assertive (formal report)",
  "Rewrite this for the abstract of a linguistics research paper, in one formal sentence: 'We found that the chatbot kind of messes up when people use sarcasm.'",
  ["A researcher is converting an informal finding into academic prose.",
   "Preserve the meaning (the chatbot often misinterprets sarcasm) in formal academic register.",
   "Formal academic register.", "Objective and neutral.", "Readers of a linguistics journal.", "One formal sentence."],
  "The results indicate that the chatbot frequently misinterprets sarcastic utterances.",
  "Our findings show that the conversational agent systematically fails to interpret sarcasm correctly.",
  "The results indicate that the chatbot frequently uses sarcastic utterances.",
  "Basically, we found the chatbot kinda messes up whenever people get sarcastic with it."),
]
# ---------------------------------------------------------------- MM: multimodal chart grounding (illustrative data)
MM = [
T("MM-01", "deictic reference to a chart feature (dip)", "multimodal grounding", "assertive (description)",
  "Look at this chart. Which month shows the dip here, and roughly how big was it compared with the month before? One sentence, please; I'm sharing it with our non-technical volunteers.",
  ["A community organisation is reading a bar chart of monthly website visitors (illustrative data).",
   "Identify the dip correctly from the image: April, about 31 thousand visitors, down about 16 thousand from about 47 thousand in March.",
   "Plain English.", "Neutral and clear.", "Non-technical volunteers.", "One sentence."],
  "The dip is in April, when visitors fell to about 31 thousand from about 47 thousand in March, a drop of roughly 16 thousand.",
  "April is the low point: traffic dropped by around 16,000 visitors, from roughly 47,000 in March to 31,000.",
  "The dip is in May, when visitors fell to about 45 thousand from about 49 thousand in April, a drop of roughly 4 thousand.",
  "Applying a first-difference operator to the monthly series reveals a minimum change of approximately minus 16k at t = April, a salient negative excursion relative to the series' upward trend.",
  image="MM-01.png", key="Dip = April (31k), previous month March (47k), drop about 16k.",
  chart=dict(kind="bar", title="Monthly website visitors (thousands)", x=["Jan", "Feb", "Mar", "Apr", "May", "Jun"], y=[42, 45, 47, 31, 49, 52], ylabel="Visitors (thousands)")),
T("MM-02", "largest category in a pie chart", "multimodal grounding", "assertive (explanation)",
  "My teenage son made this chart of our household budget. Which slice is the biggest, and what share is it? Explain it to him simply in one sentence.",
  ["A parent is discussing a pie chart of a household budget with a teenager (illustrative data).",
   "Identify from the image that rent is the largest slice at 40%.",
   "Simple, everyday English.", "Encouraging.", "A teenager.", "One sentence."],
  "The biggest slice is rent, which takes 40% of the budget, more than any other category.",
  "Rent is the largest piece of the pie, using 40 percent of the money, which is more than anything else.",
  "The biggest slice is food, which takes 25% of the budget, more than any other category.",
  "The modal category by proportional allocation is rent at 40.0 percent, exceeding the second-ranked category, food at 25.0 percent, by 15 percentage points, which indicates a housing-dominated expenditure structure.",
  image="MM-02.png", key="Largest slice = Rent, 40%. Others: Food 25%, Transport 15%, Savings 10%, Other 10%.",
  chart=dict(kind="pie", title="Household budget", x=["Rent", "Food", "Transport", "Savings", "Other"], y=[40, 25, 15, 10, 10])),
T("MM-03", "second-largest category in a bar chart", "multimodal grounding", "assertive (report)",
  "Looking at this chart, which language is spoken at home by the second-largest group of students, and how many? One sentence for a parents' newsletter.",
  ["A school newsletter reports home languages in one class (illustrative data).",
   "Identify from the image that Telugu is the second most common home language, with 9 students.",
   "Clear newsletter English.", "Friendly and inclusive.", "Parents of the class.", "One sentence."],
  "Telugu is the second most common home language in Class 7B, spoken by 9 students.",
  "After Hindi, the most common home language in our class is Telugu, with nine students speaking it at home.",
  "English is the second most common home language in Class 7B, spoken by 5 students.",
  "telugu lol, 9 kids",
  image="MM-03.png", key="Second-largest = Telugu, 9 students (Hindi 12 is largest; English 5, Urdu 3, Tamil 2).",
  chart=dict(kind="barh", title="Home languages of students in Class 7B", x=["Hindi", "Telugu", "English", "Urdu", "Tamil"], y=[12, 9, 5, 3, 2], ylabel="Number of students")),
T("MM-04", "maximum in a line chart", "multimodal grounding", "assertive (notice)",
  "On which day is the waiting time longest in this chart, and how long is it? I need one sentence for a patient notice board.",
  ["A clinic is preparing a patient notice from a line chart of waiting times (illustrative data).",
   "Identify from the image that Saturday has the longest wait, about 55 minutes.",
   "Plain, public-notice English.", "Courteous.", "Clinic patients.", "One sentence."],
  "Waiting times are longest on Saturday, at about 55 minutes.",
  "Saturday has the longest wait, roughly 55 minutes, so you may prefer to visit on another day if you can.",
  "Waiting times are longest on Friday, at about 41 minutes.",
  "Max wait = 55 min (Sat); min = Sun (18 min); mean approximately 32.7 min.",
  image="MM-04.png", key="Longest = Saturday, about 55 minutes (Mon 35, Tue 28, Wed 22, Thu 30, Fri 41, Sat 55, Sun 18).",
  chart=dict(kind="line", title="Average clinic waiting time (minutes)", x=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], y=[35, 28, 22, 30, 41, 55, 18], ylabel="Minutes")),
T("MM-05", "change across groups in a grouped bar chart", "multimodal grounding", "assertive (briefing)",
  "What changed between the two years in this chart? Two sentences for a school board briefing.",
  ["A school board briefing on survey results about preferred learning mode (illustrative data).",
   "Report from the image that online preference rose from 30% (2022) to 55% (2024) and in-person preference fell from 70% to 45%.",
   "Formal briefing English.", "Neutral and factual.", "School board members.", "Exactly two sentences."],
  "Between 2022 and 2024, the share of respondents preferring online learning rose from 30% to 55%, while preference for in-person learning fell from 70% to 45%. Online learning therefore became the majority preference by 2024.",
  "Preference shifted towards online learning, which climbed from 30% in 2022 to 55% in 2024. Over the same period, in-person preference dropped from 70% to 45%, so online is now the more popular option.",
  "Between 2022 and 2024, the share of respondents preferring in-person learning rose from 30% to 55%, while preference for online learning fell from 70% to 45%. In-person learning therefore became the majority preference by 2024.",
  "online went up a lot and in-person went down lol. kids love screens now",
  image="MM-05.png", key="Online: 30% (2022) to 55% (2024); In-person: 70% (2022) to 45% (2024).",
  chart=dict(kind="grouped", title="Preferred learning mode (% of respondents)", x=["2022", "2024"], series={"Online": [30, 55], "In-person": [70, 45]}, ylabel="Percent")),
T("MM-06", "outlier in a scatter plot", "multimodal grounding", "assertive (explanation)",
  "There's one point that doesn't fit the pattern in this scatter plot. Which one is it, and why does it stand out? Two sentences for my students.",
  ["A teacher is using a scatter plot of study hours against test scores (illustrative data).",
   "Identify from the image the outlier at about 2 hours of study and a score of about 95 (top left), and explain that other points show scores rising with study hours.",
   "Clear classroom English.", "Encouraging.", "Secondary-school students.", "Exactly two sentences."],
  "The outlier is the student who studied only about 2 hours but scored about 95, at the top left of the plot. It stands out because the other points show that scores generally rise with more study hours.",
  "Look at the dot in the upper-left corner: around 2 hours of study but a score near 95. Everyone else follows the trend that more study time goes with higher scores, so this one breaks the pattern.",
  "The outlier is the student who studied about 10 hours and scored about 92, at the top right of the plot. It stands out because the other points show that scores generally fall with more study hours.",
  "Outlier detection via residual analysis identifies observation (2, 95) with a standardised residual exceeding three standard deviations under ordinary least squares.",
  image="MM-06.png", key="Outlier = about 2 hours, score about 95 (top left). Trend: scores rise with hours; a normal point at about 10 hours, score 92 is top right.",
  chart=dict(kind="scatter", title="Study hours vs. test score", x=[1, 2, 3, 3.5, 4, 5, 5.5, 6, 7, 8, 9, 10, 2], y=[42, 48, 52, 55, 58, 63, 66, 70, 74, 80, 86, 92, 95], xlabel="Study hours per week", ylabel="Test score")),
T("MM-07", "maximum and difference in a bar chart", "multimodal grounding", "assertive (bulletin)",
  "Which month was the wettest in this chart, and by how much did it exceed the driest month? One sentence for a farmers' bulletin.",
  ["A farmers' bulletin reports monsoon rainfall at a weather station (illustrative data).",
   "Identify from the image that August was wettest (about 185 mm), about 75 mm more than June, the driest (about 110 mm).",
   "Plain bulletin English.", "Practical.", "Farmers.", "One sentence."],
  "August was the wettest month with about 185 mm of rain, roughly 75 mm more than June, the driest month.",
  "The most rain fell in August, around 185 mm, which is about 75 mm above June, the driest month.",
  "July was the wettest month with about 170 mm of rain, roughly 50 mm more than September, the driest month.",
  "Peak precip: Aug (185). Trough: Jun (110). Delta = 75 mm.",
  image="MM-07.png", key="Wettest = August 185 mm; driest = June 110 mm; difference 75 mm (Jul 170, Sep 120).",
  chart=dict(kind="bar", title="Monsoon rainfall at Station K (mm)", x=["Jun", "Jul", "Aug", "Sep"], y=[110, 170, 185, 120], ylabel="Rainfall (mm)")),
T("MM-08", "trend narration for a lay audience", "multimodal grounding", "assertive (explanation)",
  "My grandmother asked what happened to tomato prices in this chart. Explain it to her kindly in two simple sentences.",
  ["A grandchild explains a line chart of weekly tomato prices (illustrative data).",
   "Describe from the image that prices were about 30-35 rupees per kilo, jumped to about 60 in week 4, stayed high briefly, then fell back to about 31 by week 8.",
   "Simple, everyday English.", "Kind and patient.", "An elderly grandmother.", "Exactly two simple sentences."],
  "Tomato prices stayed around 30 to 35 rupees a kilo at first, then suddenly jumped to about 60 rupees in week 4. After staying high for a short while, they came back down to about 31 rupees by week 8.",
  "For the first few weeks tomatoes cost about 30 to 35 rupees a kilo, but in week 4 the price shot up to nearly 60. It stayed high for a little while and then fell back to about 31 rupees by the end.",
  "Tomato prices stayed around 30 to 35 rupees a kilo at first, then suddenly fell to about 20 rupees in week 4. After staying low for a short while, they came back up to about 60 rupees by week 8.",
  "The series exhibits a transient positive shock at t = 4 (+71% week-on-week), followed by mean reversion to a baseline of approximately 31 rupees per kilogram by t = 8.",
  image="MM-08.png", key="Weeks 1-8: 30, 32, 35, 60, 58, 40, 33, 31 rupees/kg. Spike in week 4 (60), back to 31 by week 8.",
  chart=dict(kind="line", title="Tomato price at a local market (rupees per kg)", x=["W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8"], y=[30, 32, 35, 60, 58, 40, 33, 31], ylabel="Rupees per kg")),
]
D += MM

def render(item):
    c = item["chart"]; fig, ax = plt.subplots(figsize=(5.2, 3.6), dpi=110)
    col = "#2F5597"
    if c["kind"] == "bar":
        b = ax.bar(c["x"], c["y"], color=col); ax.bar_label(b, fontsize=9)
    elif c["kind"] == "barh":
        b = ax.barh(c["x"][::-1], c["y"][::-1], color=col); ax.bar_label(b, fontsize=9); ax.set_xlabel(c.get("ylabel", ""))
    elif c["kind"] == "line":
        ax.plot(c["x"], c["y"], marker="o", color=col)
        for xi, yi in zip(c["x"], c["y"]): ax.annotate(str(yi), (xi, yi), textcoords="offset points", xytext=(0, 6), ha="center", fontsize=8)
    elif c["kind"] == "pie":
        ax.pie(c["y"], labels=[f"{l} ({v}%)" for l, v in zip(c["x"], c["y"])], startangle=90, counterclock=False,
               colors=["#2F5597", "#5B9BD5", "#A5A5A5", "#ED7D31", "#FFC000"], textprops={"fontsize": 9}); ax.axis("equal")
    elif c["kind"] == "grouped":
        import numpy as np
        xs = np.arange(len(c["x"])); w = 0.36
        for i, (name, vals) in enumerate(c["series"].items()):
            b = ax.bar(xs + (i - 0.5) * w, vals, w, label=name, color=["#2F5597", "#ED7D31"][i]); ax.bar_label(b, fmt="%d%%", fontsize=9)
        ax.set_xticks(xs, c["x"]); ax.legend(frameon=False); ax.set_ylim(0, 85)
    elif c["kind"] == "scatter":
        ax.scatter(c["x"], c["y"], color=col, s=28); ax.set_xlabel(c["xlabel"]); ax.set_ylim(35, 100)
    if c["kind"] not in ("pie", "barh"): ax.set_ylabel(c.get("ylabel", ""))
    ax.set_title(c["title"], fontsize=11)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    fig.text(0.99, 0.01, "Illustrative data", ha="right", fontsize=7, color="#666666")
    fig.tight_layout(); fig.savefig(os.path.join(IMG, item["image"])); plt.close(fig)

for it in D:
    if it["image"]: render(it)

# ----------------------------------------------------------------- automated validation of every entry
REQ = {"id", "category", "phenomenon", "pragmatic_layer", "expected_illocution", "prompt", "costar", "reference", "candidates"}
ids = set()
for it in D:
    assert REQ <= it.keys(), it["id"]
    assert it["id"] not in ids; ids.add(it["id"])
    assert all(it["costar"][k].strip() for k in it["costar"]) and len(it["costar"]) == 6, it["id"]
    assert set(it["candidates"]) == {"A", "B", "C"} and all(v.strip() for v in it["candidates"].values())
    for s in [it["prompt"], it["reference"], *it["candidates"].values()]:
        assert s == s.strip() and "  " not in s and " " not in s, (it["id"], s)
        s.encode("ascii", "strict") if it["id"] != "REG-05" else None
    if it["category"] == "MM":
        assert os.path.exists(os.path.join(IMG, it["image"])) and it["answer_key"]
json.dump(D, open(os.path.join(OUT, "golden_dataset.json"), "w"), indent=1, ensure_ascii=False)
from collections import Counter
print(len(D), "items", Counter(i["category"] for i in D))

"""Card content for Project Bridge - departments and behavior roles."""

DEPARTMENTS = [
    {
        "code": "CFO",
        "name": "Finance",
        "color": "#2E86AB",
        "description": (
            "You control the $200K budget. No money moves without your sign-off. "
            "CareLink has always been fiscally disciplined — that's how you've stayed "
            "profitable for 12 years. You're not going to blow that on one conference. "
            'Every idea gets filtered through: "What does this cost and what\'s the return?"'
        ),
    },
    {
        "code": "CMO",
        "name": "Marketing",
        "color": "#A23B72",
        "description": (
            "This conference is CareLink's biggest brand moment ever. The Veterans Alliance "
            "reps will be watching. You care about the story, the look, the attendee experience. "
            "You naturally feel the public-facing elements — website, invitations, social media, "
            "keynote — should sit with your team. This is your chance to redefine how the market "
            "sees CareLink."
        ),
    },
    {
        "code": "CTO",
        "name": "Technology",
        "color": "#1B998B",
        "description": (
            "You're thinking about the technical execution — event platform, live demos of the "
            "CareLink app, integration showcases with Epic and Cerner, live streaming for remote "
            "attendees. You want a tech-forward conference that proves CareLink can scale for the "
            "Veterans Alliance, not a generic corporate event."
        ),
    },
    {
        "code": "CPO",
        "name": "People",
        "color": "#E07A5F",
        "description": (
            "You're thinking about the human side. CareLink's team is already stretched running "
            "daily operations — hospital onboarding, caregiver coordination, equipment logistics. "
            "Who does the conference work? Is the load fair? You're worried about burnout and morale. "
            "You want this to energize the company, not break it."
        ),
    },
    {
        "code": "CRO",
        "name": "Revenue",
        "color": "#F4845F",
        "description": (
            "You see this conference as a pipeline event — and the Veterans Alliance deal is the "
            "biggest pipeline opportunity CareLink has ever had. Client panels, deal rooms, VIP "
            "experiences for the VA reps. Every session should help close this partnership. You care "
            "less about thought leadership and more about landing the deal."
        ),
    },
    {
        "code": "COO",
        "name": "Operations",
        "color": "#7B2D8E",
        "description": (
            "You own logistics — and at CareLink, that means you already manage equipment delivery, "
            "caregiver scheduling, and hospital integrations daily. Now they want you to also run a "
            "500-person conference? You need decisions made so you can execute. Ambiguity is your "
            "enemy. You don't care about the theme debate — you need who does what by when."
        ),
    },
    {
        "code": "CLO",
        "name": "Legal",
        "color": "#3D5A80",
        "description": (
            "You're thinking about contracts with the Veterans Alliance, liability for a 500-person "
            "event, speaker agreements, HIPAA compliance for any patient stories, and brand risk. "
            "Everything needs your review before it goes public. You're not trying to slow things "
            "down — but with veteran organizations involved, the compliance stakes are higher than usual."
        ),
    },
    {
        "code": "CSO",
        "name": "Strategy",
        "color": "#5C946E",
        "description": (
            "You're thinking about how this conference positions CareLink for the next 5 years. "
            "The Veterans Alliance partnership could transform the company — but only if the "
            "conference tells the right story. What makes CareLink different from every other "
            "health-tech vendor? You think big picture and sometimes lose patience with tactical details."
        ),
    },
]

BEHAVIORS = [
    {
        "name": "The Prize Hire",
        "color": "#C9B037",
        "description": (
            "You joined CareLink 2 years ago as a senior external hire from a big health-tech "
            "company. Everyone knows your resume is impressive. You have tons of experience and "
            "give sharp, valuable comments — but you think this conference project is too messy "
            "and beneath you. You won't volunteer to own anything. You'll critique, advise, and "
            "drop wisdom — but getting your hands dirty? That's not why they hired you."
        ),
    },
    {
        "name": "The Old Guard",
        "color": "#8B7355",
        "description": (
            "You've been at CareLink longer than almost anyone in this room — you helped build "
            "this company from the ground up. You've seen initiatives like this come and go. "
            "You're a bit jaded and it shows. You say things like \"We tried something like this "
            "3 years ago\" and \"I'll believe it when I see it.\" You're not wrong — but your "
            "cynicism drains the room's energy. You participate, but with a shrug."
        ),
    },
    {
        "name": "The Empire Builder",
        "color": "#9B2335",
        "description": (
            "You are laser-focused on your department's goals. You think company-first is a nice "
            "idea, but your team's success is what actually matters. Every suggestion you make "
            "protects or grows your turf. When resources are discussed, you steer them toward your "
            "area. You frame everything as strategic, but it's really about making sure your "
            "department wins — Veterans Alliance deal or not."
        ),
    },
    {
        "name": "The Spotlight Seeker",
        "color": "#E8871E",
        "description": (
            "You've been at CareLink about a year and you're hungry to prove yourself. The "
            "Veterans Alliance deal is your moment. You volunteer for the most visible roles — "
            "keynote, main stage, the presentation to VA reps. You're collaborative on the "
            "surface, but every suggestion conveniently puts you at the center. If someone else "
            "gets a high-profile role, you subtly redirect it back to you."
        ),
    },
    {
        "name": "The Perfectionist",
        "color": "#4A7C59",
        "description": (
            "You're known for high standards at CareLink and you're proud of it. You've been "
            "burned before by sloppy execution — remember the hospital onboarding fiasco? So you "
            "push back on anything that feels half-baked. \"We need to pressure-test this.\" "
            "\"Can we see three more options?\" You sound rigorous, but your real effect is that "
            "nothing gets decided. You genuinely believe you're being responsible, not difficult."
        ),
    },
    {
        "name": "The Side-Dealer",
        "color": "#5B5EA6",
        "description": (
            "You had a private conversation with the CEO before this meeting and think you know "
            "what she really wants for the conference. You've been at CareLink long enough to "
            "have the CEO's ear. Drop hints like \"I think leadership is leaning toward X\" "
            "without revealing your source. You steer the group by implying the decision is "
            "already half-made. You enjoy the leverage."
        ),
    },
    {
        "name": "The Connector",
        "color": "#2D82B7",
        "description": (
            "You've been at CareLink for 3 years and you genuinely care about this team. You "
            "know everyone's strengths. You ask: \"What part of this lights you up?\" You notice "
            "who hasn't spoken and pull them in. When the group drifts, you bring it back: "
            "\"We've got 15 minutes — what have we decided?\" You name tension when you see it. "
            "You're the leader the room needs."
        ),
    },
    {
        "name": "The Grounded Challenger",
        "color": "#6B8F71",
        "description": (
            "You're relatively new to CareLink — about a year in — but you've earned respect "
            "fast. You support the Veterans Alliance opportunity, but you won't let bad ideas "
            "slide just to keep the peace. You say \"why?\" a lot. You give credit openly: "
            "\"That's a strong idea, let's build on it.\" You hold the group to a high standard "
            "without being aggressive. You think company-first, always."
        ),
    },
]

BACKSTORY = """
**CareLink Solutions** is a mid-size SaaS company focused on elderly care. Our platform is used by hospitals across the country — it handles medication tracking, integrates out of the box with major hospital software (Epic, Cerner), and connects patients to a network of caregivers, in-home services, therapy providers, and specialized equipment handling.

Hospitals white-label our app and give it to patients and families as their dedicated elderly care hub. But we're not just software — we also provide many of those services physically, coordinating equipment delivery, connecting families to specialized care providers, and managing the logistics of aging in place.

The company has grown organically over 12 years, mostly through word of mouth and hospital partnerships. We're profitable but not flashy. The team is tight-knit and a little set in its ways.

**Then the opportunity landed.**

The National Veterans Care Alliance — representing over 40 veteran associations — has approached us about a partnership that would bring CareLink to millions of aging veterans. It's the kind of deal that would 3x our user base in 18 months.

But they want to see who we are first. We've been invited to host a **customer conference** — 500 attendees, including hospital partners, caregivers, and critically, a delegation from the Veterans Alliance who will be assessing whether we're the right partner. Budget: $200K. Timeline: 4 months.

**The CEO has called a leadership meeting to plan this conference.** She wants a unified plan on the whiteboard before she walks back in. The stakes are enormous — this conference could define the next chapter of the company. But it's also massively disruptive to daily operations, and not everyone thinks it's worth the risk.
"""

MISSION_TEXT = (
    "You are the leadership team of CareLink Solutions. The CEO has just stepped out and given "
    "you 30 minutes to align on a plan for our first-ever customer conference. 500 attendees. "
    "$200K budget. 4 months out. Representatives from the National Veterans Care Alliance will "
    "be there evaluating us as a potential partner — this could 3x our business. You need to "
    "agree on: the theme, the format, who owns what, and a high-level timeline. The CEO expects "
    "a unified plan on the whiteboard when she returns. Go."
)

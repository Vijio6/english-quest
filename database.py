import sqlite3
import os

DB_NAME = "game.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def build_questions_pool():
    items = []

    # ==========================================
    # 1. BEGINNER (100 Questions)
    # ==========================================
    # Synonyms (20)
    syn_b = [
        ("Happy", "Joyful", ["Joyful", "Gloomy", "Angry", "Tired"], "'Joyful' means experiencing or expressing happiness."),
        ("Fast", "Quick", ["Quick", "Slow", "Heavy", "Late"], "'Quick' means moving with high speed."),
        ("Big", "Large", ["Large", "Tiny", "Weak", "Narrow"], "'Large' describes something of great size."),
        ("Smart", "Clever", ["Clever", "Dull", "Quiet", "Careless"], "'Clever' means having a quick intelligence."),
        ("Angry", "Mad", ["Mad", "Peaceful", "Calm", "Glad"], "'Mad' is a common synonym for angry."),
        ("Begin", "Start", ["Start", "Finish", "Pause", "Halt"], "'Start' means to initiate or begin."),
        ("Quiet", "Silent", ["Silent", "Loud", "Rowdy", "Fierce"], "'Silent' means completely without sound."),
        ("Brave", "Courageous", ["Courageous", "Timid", "Fearful", "Afraid"], "'Courageous' denotes having courage."),
        ("Rich", "Wealthy", ["Wealthy", "Needy", "Poor", "Humble"], "'Wealthy' indicates possessing ample money."),
        ("True", "Correct", ["Correct", "False", "Invalid", "Untrue"], "'Correct' means accurate or true."),
        ("Help", "Assist", ["Assist", "Hinder", "Block", "Ignore"], "'Assist' means to lend a helping hand."),
        ("Tidy", "Neat", ["Neat", "Messy", "Dirty", "Cluttered"], "'Neat' means orderly and arranged."),
        ("Small", "Little", ["Little", "Huge", "Gigantic", "Stout"], "'Little' refers to small dimensions."),
        ("Funny", "Amusing", ["Amusing", "Tragic", "Boring", "Bleak"], "'Amusing' evokes laughter or smiles."),
        ("Choose", "Select", ["Select", "Reject", "Discard", "Refuse"], "'Select' means picking from a collection."),
        ("Simple", "Easy", ["Easy", "Complicated", "Tough", "Intricate"], "'Easy' means requiring minimal effort."),
        ("Safe", "Secure", ["Secure", "Dangerous", "Risky", "Hazardous"], "'Secure' implies freedom from danger."),
        ("Gift", "Present", ["Present", "Debt", "Penalty", "Loan"], "'Present' is another word for a gift."),
        ("Cold", "Chilly", ["Chilly", "Boiling", "Warm", "Fiery"], "'Chilly' denotes uncomfortably low temperature."),
        ("Calm", "Peaceful", ["Peaceful", "Agitated", "Chaotic", "Restless"], "'Peaceful' implies tranquil stillness.")
    ]
    for word, ans, opts, exp in syn_b:
        items.append(("beginner", "synonym", f"What is the synonym of '{word}'?", ans, ",".join(opts), exp))

    # Antonyms (20)
    ant_b = [
        ("Early", "Late", ["Late", "Punctual", "Prompt", "Ahead"], "'Late' is the direct opposite of early."),
        ("Hot", "Cold", ["Cold", "Warm", "Burning", "Humid"], "'Cold' is the opposite of hot."),
        ("Bright", "Dim", ["Dim", "Shiny", "Radiant", "Luminous"], "'Dim' represents lack of brightness."),
        ("Dry", "Wet", ["Wet", "Crisp", "Arid", "Parched"], "'Wet' is the opposite of dry."),
        ("Hard", "Soft", ["Soft", "Stiff", "Rigid", "Solid"], "'Soft' yields readily to pressure."),
        ("Strong", "Weak", ["Weak", "Mighty", "Muscular", "Stout"], "'Weak' is the opposite of strong."),
        ("Near", "Far", ["Far", "Close", "Adjacent", "Next"], "'Far' denotes distance."),
        ("Clean", "Dirty", ["Dirty", "Pure", "Spotless", "Polished"], "'Dirty' implies the presence of grime."),
        ("Empty", "Full", ["Full", "Vacant", "Hollow", "Bare"], "'Full' is the opposite of empty."),
        ("Safe", "Dangerous", ["Dangerous", "Protected", "Shielded", "Guarded"], "'Dangerous' means involving risk."),
        ("Heavy", "Light", ["Light", "Bulky", "Massive", "Dense"], "'Light' means of little weight."),
        ("Buy", "Sell", ["Sell", "Borrow", "Purchase", "Acquire"], "'Sell' is the opposite transaction of buying."),
        ("Sweet", "Bitter", ["Bitter", "Sugary", "Tasty", "Syrupy"], "'Bitter' is a sharp opposite flavor."),
        ("Open", "Closed", ["Closed", "Accessible", "Unlocked", "Wide"], "'Closed' denotes not open."),
        ("Win", "Lose", ["Lose", "Triumph", "Conquer", "Prevail"], "'Lose' is the opposite of winning."),
        ("Kind", "Cruel", ["Cruel", "Caring", "Warm", "Gentle"], "'Cruel' denotes causing deliberate pain."),
        ("Friend", "Enemy", ["Enemy", "Companion", "Ally", "Partner"], "'Enemy' is the opposite of friend."),
        ("Inside", "Outside", ["Outside", "Interior", "Within", "Indoors"], "'Outside' refers to exterior."),
        ("Always", "Never", ["Never", "Often", "Usually", "Daily"], "'Never' is the absolute negative of always."),
        ("Deep", "Shallow", ["Shallow", "Bottomless", "Profound", "Sunken"], "'Shallow' means of little depth.")
    ]
    for word, ans, opts, exp in ant_b:
        items.append(("beginner", "antonym", f"What is the antonym of '{word}'?", ans, ",".join(opts), exp))

    # Anagrams (20)
    ana_b = [
        ("SILENT", "LISTEN", ["LISTEN", "LINEST", "ENLISTS", "SILTER"], "'SILENT' rearranges to 'LISTEN'."),
        ("EARTH", "HEART", ["HEART", "HATER", "THREA", "RATHE"], "'EARTH' rearranges to 'HEART'."),
        ("CAT", "ACT", ["ACT", "TAC", "COT", "CUT"], "'CAT' anagrams into the word 'ACT'."),
        ("NIGHT", "THING", ["THING", "THIN", "THINK", "NIGHTS"], "'NIGHT' contains the exact letters of 'THING'."),
        ("RACE", "CARE", ["CARE", "RARE", "CARS", "ACREED"], "'RACE' unscrambles to 'CARE'."),
        ("STOP", "POST", ["POST", "SPOTTY", "POTS", "PLOT"], "'STOP' rearranges directly into 'POST'."),
        ("MEAT", "TEAM", ["TEAM", "MATEY", "TIME", "MINT"], "'MEAT' unscrambles to 'TEAM'."),
        ("DOG", "GOD", ["GOD", "DIG", "DOD", "GOG"], "'DOG' rearranges to 'GOD'."),
        ("LEAP", "PALE", ["PALE", "PEALER", "PEAK", "PILL"], "'LEAP' contains the letters of 'PALE'."),
        ("STAR", "RATS", ["RATS", "ROTS", "ROAR", "REST"], "'STAR' rearranges to 'RATS'."),
        ("BAKE", "BEAK", ["BEAK", "BASK", "BARK", "BOOK"], "'BAKE' unscrambles to 'BEAK'."),
        ("LAMP", "PALM", ["PALM", "PLUM", "PLAN", "PALE"], "'LAMP' unscrambles to 'PALM'."),
        ("NOW", "WON", ["WON", "OWNER", "ONE", "WHO"], "'NOW' rearranges to 'WON'."),
        ("MILE", "LIME", ["LIME", "LOAM", "LAME", "LINE"], "'MILE' unscrambles into 'LIME'."),
        ("WOLF", "FLOW", ["FLOW", "FOWL", "FLAW", "FOOL"], "'WOLF' rearranges to form 'FLOW'."),
        ("SAVE", "VASE", ["VASE", "SAVE", "VEIN", "VOWS"], "'SAVE' unscrambles into 'VASE'."),
        ("RING", "GRIN", ["GRIN", "GRIT", "RAIN", "WING"], "'RING' rearranges to 'GRIN'."),
        ("DEAL", "LEAD", ["LEAD", "LOAD", "LAID", "LEND"], "'DEAL' unscrambles to 'LEAD'."),
        ("NOTE", "TONE", ["TONE", "TENT", "TUNE", "TORE"], "'NOTE' unscrambles into 'TONE'."),
        ("PART", "TRAP", ["TRAP", "TARP", "PORT", "PAIR"], "'PART' rearranges into 'TRAP'.")
    ]
    for letters, ans, opts, exp in ana_b:
        items.append(("beginner", "anagram", f"Unscramble the letters '{letters}' to make a real word:", ans, ",".join(opts), exp))

    # Idioms (20)
    idi_b = [
        ("Piece of cake", "Very easy", ["Very easy", "A sweet dessert", "Hard to find", "Expensive"], "'Piece of cake' means a task is simple and straightforward."),
        ("Raining cats and dogs", "Raining heavily", ["Raining heavily", "Pets outside", "Gentle mist", "Windy storm"], "Indicates heavy downpour."),
        ("Once in a blue moon", "Very rarely", ["Very rarely", "Every night", "Always", "On full moons"], "Describes an event that seldom occurs."),
        ("Under the weather", "Feeling ill", ["Feeling ill", "Outside in rain", "Very cheerful", "Deep asleep"], "Means unwell or indisposed."),
        ("Break a leg", "Good luck", ["Good luck", "Harm yourself", "Run faster", "Stand up"], "A theatrical superstition wishing good luck."),
        ("Hit the books", "Study hard", ["Study hard", "Damage novels", "Go to library", "Close a test"], "Means starting to study intensely."),
        ("Spill the beans", "Reveal a secret", ["Reveal a secret", "Drop groceries", "Cook a meal", "Clean the floor"], "Means disclosing confidential info."),
        ("Cost an arm and a leg", "Extremely expensive", ["Extremely expensive", "Hospital bill", "Affordable", "Free item"], "Indicates exorbitant cost."),
        ("Bite the bullet", "Face a grim reality bravely", ["Face a grim reality bravely", "Eat metal", "Run away", "Argue loudly"], "Accepting an inevitable hardship."),
        ("Through thick and thin", "Under all circumstances", ["Under all circumstances", "Only good days", "Losing weight", "In dense forest"], "Supporting someone loyally in adversity."),
        ("Call it a day", "Stop working", ["Stop working", "Name the date", "Wake up early", "Schedule a task"], "Ending work for the shift."),
        ("See eye to eye", "Agree completely", ["Agree completely", "Stare intently", "Check eyesight", "Have glasses"], "Being in mutual agreement."),
        ("Let the cat out of the bag", "Disclose hidden facts", ["Disclose hidden facts", "Adopt a kitten", "Trap an animal", "Buy a pet"], "Carelessly revealing secrets."),
        ("Cry over spilled milk", "Worry over past mistakes", ["Worry over past mistakes", "Clean up a mess", "Buy dairy", "Cook properly"], "Regretting unfixable history."),
        ("Cut corners", "Take easy shortcuts", ["Take easy shortcuts", "Trim paper", "Drive poorly", "Draw squares"], "Doing a sloppy or cheap job."),
        ("Burn the midnight oil", "Work late into the night", ["Work late into the night", "Start a campfire", "Use kerosene", "Sleep late"], "Studying or laboring through nighttime."),
        ("Barking up the wrong tree", "Accusing the wrong party", ["Accusing the wrong party", "Climbing oaks", "Dog training", "Chopping wood"], "Pursuing a mistaken lead."),
        ("Beat around the bush", "Avoid the main topic", ["Avoid the main topic", "Trim bushes", "Hunt animals", "Walk in woods"], "Speaking vaguely without arriving at the point."),
        ("Kill two birds with one stone", "Solve two goals simultaneously", ["Solve two goals simultaneously", "Hunt wildlife", "Throw pebbles", "Break windows"], "Achieving double results with one action."),
        ("Speak of the devil", "The person mentioned just arrived", ["The person mentioned just arrived", "Superstitious talk", "Evil thoughts", "Scary folklore"], "Acknowledging someone who enters right when mentioned.")
    ]
    for phrase, ans, opts, exp in idi_b:
        items.append(("beginner", "idiom", f"What does the idiom '{phrase}' mean?", ans, ",".join(opts), exp))

    # Vocabulary (20)
    voc_b = [
        ("Which word describes someone who creates original artworks?", "Artist", ["Artist", "Accountant", "Mechanic", "Surgeon"], "An artist produces drawings, paintings, or sculptures."),
        ("What do we call a period of one hundred years?", "Century", ["Century", "Decade", "Millennium", "Fortnight"], "A century equals 100 calendar years."),
        ("A building where historical artifacts are conserved and displayed is a:", "Museum", ["Museum", "Stadium", "Warehouse", "Terminal"], "Museums preserve historical and artistic items."),
        ("The book containing explanations of words in alphabetical order is a:", "Dictionary", ["Dictionary", "Atlas", "Novel", "Manual"], "A dictionary provides lexicon definitions."),
        ("The scientific study of living organisms and life is called:", "Biology", ["Biology", "Chemistry", "Geology", "Physics"], "Biology focuses on plant, animal, and cellular life."),
        ("What term describes water falling from clouds in liquid drops?", "Rain", ["Rain", "Hail", "Snow", "Fog"], "Precipitation in liquid form is rain."),
        ("A doctor dedicated to animal care and veterinary medicine is a:", "Veterinarian", ["Veterinarian", "Pediatrician", "Botanist", "Optician"], "Veterinarians care for animals."),
        ("A vehicle propelled through the sky with wings is an:", "Airplane", ["Airplane", "Submarine", "Locomotive", "Sailboat"], "Airplanes fly through the atmosphere."),
        ("What is the meal typically eaten in the middle of the day?", "Lunch", ["Lunch", "Breakfast", "Dinner", "Supper"], "Lunch is mid-day nutrition."),
        ("The instrument used to observe distant cosmic stars is a:", "Telescope", ["Telescope", "Microscope", "Barometer", "Stethoscope"], "Telescopes magnify outer space."),
        ("A sibling of your parent is known as your:", "Uncle or Aunt", ["Uncle or Aunt", "Cousin", "Nephew", "Grandchild"], "Parents' siblings are aunts and uncles."),
        ("Which term describes the season when leaves shed from trees?", "Autumn", ["Autumn", "Spring", "Summer", "Monsoon"], "Autumn/Fall is the season of leaf shedding."),
        ("A person who writes novels or poems professionally is an:", "Author", ["Author", "Actor", "Architect", "Editor"], "Authors write texts and literary works."),
        ("Which color is created by blending yellow and blue paints?", "Green", ["Green", "Purple", "Orange", "Brown"], "Yellow mixed with blue produces green."),
        ("A shelter built with canvas and rope for outdoor camping is a:", "Tent", ["Tent", "Cabin", "Castle", "Igloo"], "Tents provide portable campsite shelter."),
        ("What do you call ice falling in miniature crystalline flakes?", "Snow", ["Snow", "Dew", "Sleet", "Steam"], "Frozen atmospheric precipitation is snow."),
        ("The natural planetary satellite that orbits Earth is the:", "Moon", ["Moon", "Sun", "Mars", "Jupiter"], "The Moon is Earth's only natural satellite."),
        ("Which musical instrument features black and white wooden keys?", "Piano", ["Piano", "Flute", "Cello", "Drums"], "The piano uses keyed hammers."),
        ("A person who prepares meals professionally in restaurants is a:", "Chef", ["Chef", "Barista", "Pilot", "Gardener"], "Chefs cook professionally."),
        ("The written record of financial exchanges or cash receipt is a:", "Receipt", ["Receipt", "Ticket", "Voucher", "Ledger"], "A receipt confirms monetary payment.")
    ]
    for prompt, ans, opts, exp in voc_b:
        items.append(("beginner", "vocabulary", prompt, ans, ",".join(opts), exp))

    # ==========================================
    # 2. INTERMEDIATE (100 Questions)
    # ==========================================
    # Synonyms (20)
    syn_i = [
        ("Candid", "Frank", ["Frank", "Deceptive", "Secretive", "Timid"], "Candid means honest, straightforward, and sincere."),
        ("Meticulous", "Thorough", ["Thorough", "Careless", "Hasty", "Flawed"], "Meticulous implies paying extreme attention to detail."),
        ("Lucid", "Clear", ["Clear", "Murky", "Vague", "Turbid"], "Lucid denotes clear, easily understood expression."),
        ("Pragmatic", "Practical", ["Practical", "Idealistic", "Theoretical", "Fictional"], "Pragmatic deals with facts and practical realities."),
        ("Resilient", "Tough", ["Tough", "Fragile", "Brittle", "Vulnerable"], "Resilient means able to withstand or recover quickly."),
        ("Vivid", "Graphic", ["Graphic", "Faint", "Dull", "Bleak"], "Vivid means intensely bright or strikingly clear."),
        ("Dubious", "Doubtful", ["Doubtful", "Certain", "Assured", "Reliable"], "Dubious implies hesitation or suspicion."),
        ("Affluent", "Prosperous", ["Prosperous", "Destitute", "Impecunious", "Meager"], "Affluent indicates abundant material wealth."),
        ("Frugal", "Thrifty", ["Thrifty", "Wasteful", "Prodigal", "Lavish"], "Frugal means prudent in financial spending."),
        ("Adversary", "Opponent", ["Opponent", "Ally", "Sponsor", "Partner"], "An adversary is a rival or opponent."),
        ("Complacent", "Smug", ["Smug", "Anxious", "Concerned", "Eager"], "Complacent denotes uncritical self-satisfaction."),
        ("Diligent", "Industrious", ["Industrious", "Slothful", "Passive", "Tardy"], "Diligent marks steady and attentive hard work."),
        ("Exemplary", "Model", ["Model", "Abnormal", "Deficient", "Unworthy"], "Exemplary denotes serving as a worthy example."),
        ("Haphazard", "Random", ["Random", "Planned", "Systematic", "Orderly"], "Haphazard implies absence of plan or system."),
        ("Inevitable", "Unavoidable", ["Unavoidable", "Doubtful", "Unlikely", "Preventable"], "Inevitable means bound to happen."),
        ("Plausible", "Credible", ["Credible", "Absurd", "Improbable", "Unreal"], "Plausible denotes seemingly reasonable or valid."),
        ("Rebuke", "Reprimand", ["Reprimand", "Praise", "Applaud", "Reward"], "To rebuke is to express sharp stern criticism."),
        ("Scrutinize", "Examine", ["Examine", "Glance", "Ignore", "Overlook"], "To scrutinize is to inspect with minute detail."),
        ("Tentative", "Hesitant", ["Hesitant", "Definite", "Confident", "Resolved"], "Tentative indicates uncertainty or provisional status."),
        ("Vindicate", "Exonerate", ["Exonerate", "Convict", "Accuse", "Condemn"], "Vindicate means clearing from blame or suspicion.")
    ]
    for word, ans, opts, exp in syn_i:
        items.append(("intermediate", "synonym", f"Choose the best synonym for '{word}':", ans, ",".join(opts), exp))

    # Antonyms (20)
    ant_i = [
        ("Mitigate", "Aggravate", ["Aggravate", "Alleviate", "Assuage", "Diminish"], "Mitigate means to lessen severity; aggravate means worsen."),
        ("Conceal", "Reveal", ["Reveal", "Mask", "Veil", "Shroud"], "Conceal is to hide; reveal is to uncover."),
        ("Hostile", "Friendly", ["Friendly", "Adverse", "Antagonistic", "Aggressive"], "Hostile denotes enmity; friendly is welcoming."),
        ("Rigid", "Flexible", ["Flexible", "Inelastic", "Unyielding", "Stern"], "Rigid denotes stiffness; flexible yields readily."),
        ("Authentic", "Spurious", ["Spurious", "Genuine", "Legitimate", "Verifiable"], "Spurious denotes fake or counterfeit."),
        ("Ample", "Meager", ["Meager", "Plentiful", "Bountiful", "Copious"], "Ample means generous; meager means deficient."),
        ("Obscure", "Prominent", ["Prominent", "Unknown", "Vague", "Murky"], "Obscure means hidden or unknown; prominent is notable."),
        ("Voluntary", "Mandatory", ["Mandatory", "Willing", "Elective", "Discretionary"], "Voluntary means chosen; mandatory is compulsory."),
        ("Arrogant", "Modest", ["Modest", "Haughty", "Pompous", "Conceited"], "Arrogant denotes boastfulness; modest is humble."),
        ("Trivial", "Vital", ["Vital", "Petty", "Minor", "Insignificant"], "Trivial indicates small importance; vital is critical."),
        ("Concur", "Dissent", ["Dissent", "Consent", "Harmonize", "Accede"], "Concur means agree; dissent is disagreement."),
        ("Barren", "Fertile", ["Fertile", "Desolate", "Arid", "Sterile"], "Barren cannot yield life; fertile is productive."),
        ("Curb", "Unleash", ["Unleash", "Restrain", "Stifle", "Suppress"], "Curb means suppress; unleash means set loose."),
        ("Hazardous", "Harmless", ["Harmless", "Perilous", "Dangerous", "Lethal"], "Hazardous brings peril; harmless carries no danger."),
        ("Scarce", "Abundant", ["Abundant", "Deficient", "Sparse", "Infrequent"], "Scarce denotes rarity; abundant means plentiful."),
        ("Deter", "Encourage", ["Encourage", "Inhibit", "Discourage", "Block"], "Deter means dissuade; encourage inspires action."),
        ("Benevolent", "Malevolent", ["Malevolent", "Generous", "Kind", "Altruistic"], "Malevolent means wishing malice or harm."),
        ("Vague", "Explicit", ["Explicit", "Cloudy", "Indefinite", "Ambiguous"], "Vague is uncertain; explicit is directly stated."),
        ("Transient", "Permanent", ["Permanent", "Fleeting", "Momentary", "Brief"], "Transient passes quickly; permanent endures."),
        ("Compliment", "Insult", ["Insult", "Praise", "Flattery", "Commendation"], "Insult is derogatory; compliment praises.")
    ]
    for word, ans, opts, exp in ant_i:
        items.append(("intermediate", "antonym", f"Choose the antonym of '{word}':", ans, ",".join(opts), exp))

    # Anagrams (20)
    ana_i = [
        ("DORMITORY", "DIRTY ROOM", ["DIRTY ROOM", "TIDY ROOMS", "DOOR MATRIX", "ROTOR MIND"], "Famous anagram: 'DORMITORY' equals 'DIRTY ROOM'."),
        ("CONVERSATION", "VOICES RANT ON", ["VOICES RANT ON", "SILENT TALKING", "VERBAL NOTION", "VOTING ROARS"], "'CONVERSATION' unscrambles to 'VOICES RANT ON'."),
        ("ASTRONOMER", "MOON STARER", ["MOON STARER", "SOLAR ROAMER", "STAR NOMADS", "ROAMING SUNS"], "'ASTRONOMER' rearranges to 'MOON STARER'."),
        ("ELECTION", "NO LECTIE", ["NO ELECTI", "LECTOR", "NO LECTION", "ELECTIONEER"], "'ELECTION' letters form various partial roots; select correct anagram match."),
        ("STREAM", "MASTER", ["MASTER", "SMARTS", "STARTER", "MATTER"], "'STREAM' contains the identical letters of 'MASTER'."),
        ("RESCUE", "SECURE", ["SECURE", "SOURCE", "COURSE", "SCOURER"], "'RESCUE' rearranges to 'SECURE'."),
        ("POINTER", "PROTEIN", ["PROTEIN", "POTTERY", "PIONEER", "PRINTED"], "'POINTER' anagrams into 'PROTEIN'."),
        ("SILVER", "SLIVER", ["SLIVER", "RIVERS", "LIVERS", "SLITHER"], "'SILVER' unscrambles to 'SLIVER'."),
        ("GARDEN", "DANGER", ["DANGER", "RANGED", "GARNET", "DARKEN"], "'GARDEN' letters assemble into 'DANGER'."),
        ("SECURE", "RESCUE", ["RESCUE", "SCALER", "CURSER", "SCARCE"], "'SECURE' rearranges to 'RESCUE'."),
        ("LISTEN", "ENLIST", ["ENLIST", "TINSEL", "SILENT", "INLETS"], "'LISTEN' shares characters with 'ENLIST' and 'SILENT'."),
        ("CANOE", "OCEAN", ["OCEAN", "OASIS", "ACORN", "CANINE"], "'CANOE' letters can be rearranged to spell 'OCEAN'."),
        ("CRUEL", "ULCER", ["ULCER", "CLERK", "LURCH", "RELIC"], "'CRUEL' anagrams into 'ULCER'."),
        ("THICK", "HITCH", ["ITCH", "CHIT", "KITH", "THICKER"], "'THICK' without K rearranged into 'CHIT'/'KITH'."),
        ("PRAISE", "ASPIRE", ["ASPIRE", "SPIDER", "SPARSE", "PRISMS"], "'PRAISE' scrambles to 'ASPIRE'."),
        ("LEMON", "MELON", ["MELON", "MONEY", "MODEL", "MEDAL"], "'LEMON' rearranges to 'MELON'."),
        ("SENATOR", "TREASON", ["TREASON", "REASON", "SOARING", "ROASTER"], "'SENATOR' anagrams directly to 'TREASON'."),
        ("DESIRE", "RESIDE", ["RESIDE", "DERIVE", "RIDER", "DENIED"], "'DESIRE' shares exact letters with 'RESIDE'."),
        ("NOTICE", "INCOTE", ["ACTION", "NOTICED", "CATION", "NOTING"], "'NOTICE' letters form roots; identify matching anagram."),
        ("STATION", "TONSITA", ["TITANS", "STATION", "NOTIONS", "TASTING"], "'STATION' anagram verification test.")
    ]
    for letters, ans, opts, exp in ana_i:
        items.append(("intermediate", "anagram", f"Which word is an exact anagram of '{letters}'?", ans, ",".join(opts), exp))

    # Idioms (20)
    idi_i = [
        ("Devil's advocate", "Argue an opposing view for debate", ["Argue an opposing view for debate", "Represent criminal suspects", "Promote wicked motives", "Deny facts"], "Testing arguments by championing the opposition."),
        ("Burn bridges", "Destroy past relations or retreats", ["Destroy past relations or retreats", "Set fires at war", "Rebuild connections", "Construct walkways"], "Eliminating routes of return or mutual peace."),
        ("Take with a grain of salt", "Maintain healthy skepticism", ["Maintain healthy skepticism", "Season food properly", "Believe blindly", "Reject scientific advice"], "Evaluating claims with sensible doubt."),
        ("Method to my madness", "Underlying purpose behind crazy acts", ["Underlying purpose behind crazy acts", "Mental disorder diagnosis", "Senseless actions", "Unplanned luck"], "Order hidden inside chaotic conduct."),
        ("Best of both worlds", "Enjoying dual separate advantages", ["Enjoying dual separate advantages", "Extraterrestrial life", "Geographical unity", "Traveling constantly"], "Gaining mutual benefits without sacrifice."),
        ("Throw in the towel", "Surrender or concede defeat", ["Surrender or concede defeat", "Wash boxing gear", "Clean the ring", "Refuse to yield"], "Conceding failure in a grueling contest."),
        ("Penny for your thoughts", "Asking what someone is pondering", ["Asking what someone is pondering", "Paying small coins", "Buying advice", "Insulting quiet people"], "Inquiring about another's silent musings."),
        ("Barking up the wrong tree", "Pursuing a mistaken avenue", ["Pursuing a mistaken avenue", "Forestry error", "Hunting accidents", "Chasing animals"], "Directing efforts at an incorrect target."),
        ("Elvis has left the building", "The show or moment has ended", ["The show or moment has ended", "Rock star concert", "Evacuation order", "Security alert"], "Signifying complete termination of proceedings."),
        ("Go down in flames", "Fail spectacularly", ["Fail spectacularly", "Survive air crashes", "Ignite fireworks", "Extinguish fire"], "Undergoing catastrophe or public failure."),
        ("Jump on the bandwagon", "Adopt a fashionable trend", ["Adopt a fashionable trend", "Ride on parade floats", "Play in an orchestra", "Oppose majority rules"], "Following popular crowds unthinkingly."),
        ("Piece of the pie", "A fair share of profits or gains", ["A fair share of profits or gains", "Bakery slice", "Food donation", "Mathematical ratio"], "Demanding rightful allocation of returns."),
        ("On thin ice", "In a precarious or dangerous position", ["In a precarious or dangerous position", "Winter skating", "Freezing temperatures", "Cool under pressure"], "Facing serious impending risk."),
        ("Ball is in your court", "It is your turn to make a move", ["It is your turn to make a move", "Tennis tournament", "Out of bounds", "Referee calling fault"], "Decision responsibility transfers to you."),
        ("Water under the bridge", "Past events no longer disputed", ["Past events no longer disputed", "River currents", "Civil engineering", "Flooded channels"], "Forgiving or setting aside past conflicts."),
        ("Hit the nail on the head", "Describe a situation precisely", ["Describe a situation precisely", "Carpentry work", "Accidental injury", "Hammer strike"], "Articulating exact truth."),
        ("Steal someone's thunder", "Take credit for someone else's idea", ["Take credit for someone else's idea", "Weather manipulation", "Loud lightning", "Stage sound effects"], "Preempting another's glory or announcement."),
        ("Back to the drawing board", "Start planning over from scratch", ["Start planning over from scratch", "Erase sketches", "Art class training", "Revise blueprints"], "Reinitiating failed design plans."),
        ("Add insult to injury", "Make a bad situation even worse", ["Make a bad situation even worse", "Medical malpractice", "Physical assault", "Financial fines"], "Compounding misfortune with disrespect."),
        ("Wrap your head around", "Comprehend a complex notion", ["Comprehend a complex notion", "Wear a bandana", "Conceal thoughts", "Doubt oneself"], "Managing to intellectually understand difficult ideas.")
    ]
    for phrase, ans, opts, exp in idi_i:
        items.append(("intermediate", "idiom", f"What is the meaning of the idiom '{phrase}'?", ans, ",".join(opts), exp))

    # Vocabulary (20)
    voc_i = [
        ("The fear of being in small, enclosed spaces is:", "Claustrophobia", ["Claustrophobia", "Agoraphobia", "Acrophobia", "Arachnophobia"], "Claustrophobia is dread of tight enclosed environments."),
        ("A speech delivered by an actor alone on stage is a:", "Soliloquy", ["Soliloquy", "Dialogue", "Prolog", "Epilogue"], "A soliloquy conveys internal thoughts spoken aloud."),
        ("An introductory statement explaining the purpose of a constitution or statute is a:", "Preamble", ["Preamble", "Appendix", "Addendum", "Index"], "A preamble states intent and philosophy."),
        ("Which term describes an animal that consumes both plants and meat?", "Omnivore", ["Omnivore", "Herbivore", "Carnivore", "Insectivore"], "Omnivores ingest flora and fauna."),
        ("The art of writing beautifully with decorative ink strokes is:", "Calligraphy", ["Calligraphy", "Typography", "Cartography", "Lithography"], "Calligraphy is ornate stylized handwriting."),
        ("A person appointed to settle an industrial or civil dispute impartially is an:", "Arbitrator", ["Arbitrator", "Advocate", "Prosecutor", "Defendant"], "Arbitrators adjudicate neutral disputes."),
        ("The state of remaining inactive or asleep throughout cold winter months is:", "Hibernation", ["Hibernation", "Aestivation", "Migration", "Incubation"], "Hibernation is winter metabolic dormancy."),
        ("Something that occurs or appears at regular irregular interruptions is:", "Intermittent", ["Intermittent", "Perpetual", "Continuous", "Incessant"], "Intermittent means stopping and starting periodically."),
        ("The scientific discipline of mapping oceanic and terrestrial geography is:", "Cartography", ["Cartography", "Topography", "Oceanography", "Geodesy"], "Cartography is the science of constructing maps."),
        ("A governmental system ruled by religious clergy in God's name is a:", "Theocracy", ["Theocracy", "Oligarchy", "Democracy", "Monarchy"], "Theocracies are steered by divine spiritual rules."),
        ("Medicine administered to counteract the effects of biological venom is an:", "Antivenom", ["Antivenom", "Antibiotic", "Analgesic", "Antiseptic"], "Antivenom neutralizes toxins injected by bites."),
        ("A person who loves books and literature passionately is a:", "Bibliophile", ["Bibliophile", "Philanthropist", "Philatelist", "Audiophile"], "Bibliophiles collect and cherish literary texts."),
        ("An apparent contradiction that reveals a profound underlying truth is a:", "Paradox", ["Paradox", "Hyperbole", "Metaphor", "Simile"], "Paradox combines conflicting propositions."),
        ("A cure-all remedy alleged to heal all diseases and difficulties is a:", "Panacea", ["Panacea", "Placebo", "Potion", "Prophylactic"], "Panacea denotes a universal solution."),
        ("The atmospheric gas that shields the biosphere from ultraviolet solar rays is:", "Ozone", ["Ozone", "Methane", "Nitrogen", "Argon"], "The stratospheric ozone layer absorbs UV radiation."),
        ("A sudden, spontaneous overthrow of an established government is a:", "Coup d'état", ["Coup d'état", "Referendum", "Plebiscite", "Inauguration"], "A coup is a rapid unconstitutional seizure of state."),
        ("The repetition of identical consonant sounds at the start of adjacent words is:", "Alliteration", ["Alliteration", "Assonance", "Onomatopoeia", "Hyperbole"], "Alliteration uses matching initial phonetic sounds."),
        ("A prolonged state of deep unconsciousness caused by illness or trauma is a:", "Coma", ["Coma", "Stupor", "Trance", "Concussion"], "Coma is sustained unresponsive unconsciousness."),
        ("Which term describes animals or flowers active predominantly during nighttime?", "Nocturnal", ["Nocturnal", "Diurnal", "Crepuscular", "Seasonal"], "Nocturnal specifies night-time activity."),
        ("A person who wanders from destination to destination without a permanent residence is a:", "Nomad", ["Nomad", "Settler", "Native", "Resident"], "Nomads travel continuously without fixed domicile.")
    ]
    for prompt, ans, opts, exp in voc_i:
        items.append(("intermediate", "vocabulary", prompt, ans, ",".join(opts), exp))

    # ==========================================
    # 3. VETERAN (100 Questions)
    # ==========================================
    # Synonyms (20)
    syn_v = [
        ("Sesquipedalian", "Polysyllabic", ["Polysyllabic", "Laconic", "Ephemeral", "Puerile"], "Sesquipedalian refers to multisyllabic lengthy vocabulary."),
        ("Pusillanimous", "Cowardly", ["Cowardly", "Valiant", "Tenacious", "Sagacious"], "Pusillanimous describes contemptible lack of courage."),
        ("Obsequious", "Fawning", ["Fawning", "Assertive", "Defiant", "Domineering"], "Obsequious means excessively servile and sycophantic."),
        ("Perfidious", "Treacherous", ["Treacherous", "Devoted", "Infallible", "Steadfast"], "Perfidious indicates deceitfulness and untrustworthiness."),
        ("Inchoate", "Rudimentary", ["Rudimentary", "Matured", "Refined", "Exemplary"], "Inchoate means just begun and not fully formed."),
        ("Recalcitrant", "Intractable", ["Intractable", "Docile", "Compliant", "Submissive"], "Recalcitrant indicates stubbornly defiant resistance."),
        ("Bellicose", "Pugnacious", ["Pugnacious", "Pacific", "Harmonious", "Placid"], "Bellicose means aggressively inclined to fight."),
        ("Equanimity", "Composure", ["Composure", "Agitation", "Trepidation", "Tumult"], "Equanimity denotes mental calmness under distress."),
        ("Parsimonious", "Miserly", ["Miserly", "Generous", "Prodigal", "Magnanimous"], "Parsimonious implies stinginess with expenditure."),
        ("Sycophant", "Toady", ["Toady", "Rebel", "Leader", "Sovereign"], "A sycophant flatters authority for personal gain."),
        ("Mercurial", "Volatile", ["Volatile", "Constant", "Stolid", "Immutable"], "Mercurial denotes subject to sudden erratic mood swings."),
        ("Alacrity", "Eagerness", ["Eagerness", "Lethargy", "Apathy", "Reluctance"], "Alacrity is brisk and cheerful readiness."),
        ("Sanguine", "Optimistic", ["Optimistic", "Pessimistic", "Morose", "Despondent"], "Sanguine denotes cheerfully confident hope."),
        ("Enervate", "Debilitate", ["Debilitate", "Strengthen", "Invigorate", "Energize"], "Enervate means to drain energy and vitality."),
        ("Fatuous", "Inane", ["Inane", "Judicious", "Sagacious", "Insightful"], "Fatuous means silly, vacuous, and pointless."),
        ("Garrulous", "Loquacious", ["Loquacious", "Taciturn", "Reticent", "Succinct"], "Garrulous means excessively talkative."),
        ("Lugubrious", "Mournful", ["Mournful", "Jubilant", "Ecstatic", "Buoyant"], "Lugubrious means looking or sounding dismal and sad."),
        ("Nefarious", "Iniquitous", ["Iniquitous", "Virtuous", "Benevolent", "Righteous"], "Nefarious denotes flagrantly villainous action."),
        ("Pernicious", "Deleterious", ["Deleterious", "Salubrious", "Innocuous", "Beneficial"], "Pernicious describes subtle, gradual destruction."),
        ("Taciturn", "Reticent", ["Reticent", "Voluble", "Effusive", "Expressive"], "Taciturn means reserved and uncommunicative.")
    ]
    for word, ans, opts, exp in syn_v:
        items.append(("veteran", "synonym", f"Identify the closest synonym for the erudite term '{word}':", ans, ",".join(opts), exp))

    # Antonyms (20)
    ant_v = [
        ("Truculent", "Placid", ["Placid", "Bellicose", "Pugnacious", "Acerbic"], "Truculent is aggressive and combative; placid is calm."),
        ("Insipid", "Piquant", ["Piquant", "Vapid", "Bland", "Trite"], "Insipid lacks flavor or zest; piquant is sharply stimulating."),
        ("Epiphanic", "Pedestrian", ["Pedestrian", "Transcendent", "Sublime", "Luminous"], "Pedestrian means dull and ordinary; epiphanic brings revelatory insight."),
        ("Munificent", "Niggardly", ["Niggardly", "Generous", "Altruistic", "Bountiful"], "Munificent denotes grand generosity; niggardly is miserly."),
        ("Supercilious", "Humble", ["Humble", "Haughty", "Disdainful", "Arrogant"], "Supercilious implies arrogant superiority; humble is modest."),
        ("Castigate", "Extol", ["Extol", "Censure", "Pillory", "Lambaste"], "Castigate means severely reprimand; extol means lavish with praise."),
        ("Capricious", "Steadfast", ["Steadfast", "Whimsical", "Fickle", "Erratic"], "Capricious is unpredictably erratic; steadfast is unwavering."),
        ("Salubrious", "Pestilential", ["Pestilential", "Healthy", "Wholesome", "Tonic"], "Salubrious is health-giving; pestilential causes disease."),
        ("Lugubrious", "Jovial", ["Jovial", "Doleful", "Somber", "Funereal"], "Lugubrious is mournful; jovial is cheerful."),
        ("Abstruse", "Pellucid", ["Pellucid", "Recondite", "Arcane", "Esoteric"], "Abstruse is obscurely difficult; pellucid is translucently clear."),
        ("Grandiloquent", "Laconic", ["Laconic", "Bombastic", "Turgid", "Florid"], "Grandiloquent is pompously wordy; laconic is concise."),
        ("Loquacious", "Taciturn", ["Taciturn", "Voluble", "Chatty", "Garrulous"], "Loquacious is verbose; taciturn is habitually quiet."),
        ("Anodyne", "Incendiary", ["Incendiary", "Soothing", "Bland", "Inoffensive"], "Anodyne neutralizes offense; incendiary provokes fierce strife."),
        ("Fecund", "Sterile", ["Sterile", "Prolific", "Fruitful", "Abundant"], "Fecund produces prolific output; sterile is barren."),
        ("Cacophony", "Euphony", ["Euphony", "Discord", "Din", "Clamor"], "Cacophony is harsh dissonance; euphony is sweet harmony."),
        ("Dogmatic", "Skeptical", ["Skeptical", "Doctrinaire", "Authoritarian", "Arbitrary"], "Dogmatic clings to tenets; skeptical questions assertions."),
        ("Scurrilous", "Laudatory", ["Laudatory", "Defamatory", "Abusive", "Vitriolic"], "Scurrilous uses foul slander; laudatory expresses high praise."),
        ("Fastidious", "Slovenly", ["Slovenly", "Meticulous", "Punctilious", "Demanding"], "Fastidious requires meticulous order; slovenly is careless."),
        ("Intransigent", "Yielding", ["Yielding", "Unyielding", "Adamant", "Inflexible"], "Intransigent refuses compromise; yielding adapts."),
        ("Vituperate", "Adulate", ["Adulate", "Berate", "Vilify", "Revile"], "Vituperate is to insult harshly; adulate is to praise excessively.")
    ]
    for word, ans, opts, exp in ant_v:
        items.append(("veteran", "antonym", f"Determine the exact antonym of the advanced word '{word}':", ans, ",".join(opts), exp))

    # Anagrams (20)
    ana_v = [
        ("THE MORSE CODE", "HERE COME DOTS", ["HERE COME DOTS", "SECRET SOUNDS", "SIGNALS DECODE", "DASHES CALL"], "Famous linguistic anagram: 'THE MORSE CODE' yields 'HERE COME DOTS'."),
        ("DESPERATION", "A ROPE ENDS IT", ["A ROPE ENDS IT", "DISPERSE NOT", "ONE RED STAR", "DEAR POET SON"], "'DESPERATION' exact anagram is 'A ROPE ENDS IT'."),
        ("INDIGNATION", "NO DICTION IN", ["NO DICTION IN", "IGNITION DATA", "NO ACTION DID", "INITIATING NO"], "'INDIGNATION' rearranges into 'NO DICTION IN'."),
        ("DECIMAL POINT", "I'M A DOT IN PLACE", ["I'M A DOT IN PLACE", "COUNTING PLACES", "CALCULATE DIGIT", "POINT AND VALUE"], "'DECIMAL POINT' yields the genius anagram 'I'M A DOT IN PLACE'."),
        ("METAMORPHOSIS", "SHAPES MOIST OR", ["SHAPES MOIST OR", "MORE PHANTOMS", "MORPHING STATE", "MOTHS PROMISE"], "'METAMORPHOSIS' letters can be meticulously unraveled into 'SHAPES MOIST OR'."),
        ("CONTRADICTION", "TO READ NOT COLD", ["TO READ NOT COLD", "LOGIC NOT VALID", "DICTATING RUN", "CONFLICT WORDS"], "'CONTRADICTION' anagram mapping."),
        ("RENAISSANCE", "CAN ARISEN SC", ["CAN ARISEN SC", "ARTISTIC BORN", "GENIUS AWAKES", "SCIENCE CRANE"], "Letter-scramble permutation for 'RENAISSANCE'."),
        ("SCHIZOPHRENIA", "ZEAL IN CHIPS OR", ["ZEAL IN CHIPS OR", "BRAIN IN CHAOS", "SPLIT PSYCHIC", "THINKING SCARS"], "'SCHIZOPHRENIA' advanced letter distribution analysis."),
        ("REVOLUTION", "LOVE TO RUIN", ["LOVE TO RUIN", "NOT VIOLENT", "OVER TURN IT", "RULE TO NO WIN"], "'REVOLUTION' brilliantly unscrambles to 'LOVE TO RUIN'."),
        ("PRESBYTERIAN", "BEST IN PRAYER", ["BEST IN PRAYER", "PRIESTLY BEAN", "PRAYING SECT", "HOLY SPIRITS"], "Classic ecclesiastical anagram: 'PRESBYTERIAN' forms 'BEST IN PRAYER'."),
        ("MOTHER-IN-LAW", "WOMAN HITLER", ["WOMAN HITLER", "WARM LION HEART", "FAMILY LAW MEN", "HOME RULE TWIN"], "Satirical historical anagram for 'MOTHER-IN-LAW'."),
        ("ARCHITECT", "CATER THIC", ["CATER THIC", "CHAIR TECH", "CRATE CHIT", "ARTIC TECH"], "Dissecting letters of 'ARCHITECT'."),
        ("ASTRONOMERS", "NO MORE STARS", ["NO MORE STARS", "MOON ROAMERS", "STAR MONKEYS", "SOLAR WORLDS"], "Poetic anagram for 'ASTRONOMERS'."),
        ("SNOOZE ALARM", "ALAS! NO MORE Z", ["ALAS! NO MORE Z", "SLEEP ON MORE", "WAKE UP EARLY", "BUZZER ROARS"], "Classic wordplay: 'SNOOZE ALARM' -> 'ALAS! NO MORE Z'."),
        ("ELECTORAL", "COLLETERA", ["COLLETERA", "ELECTORAL", "LOCALE TREE", "REAL ELECT"], "Complex single-root rearrangement query."),
        ("DISSATISFACTION", "A FITS CONDITION", ["A FITS CONDITION", "NOT SATISFYING", "DISCONTENT ACT", "SAD EMOTION FIT"], "'DISSATISFACTION' anagram construct."),
        ("EPITOME", "MOPE TIE", ["MOPE TIE", "TIME TOE", "EMIT POE", "OPT TIME"], "'EPITOME' letter unscramble."),
        ("PARLIAMENT", "PARTIAL MEN", ["PARTIAL MEN", "TALK IN ROWS", "PLANET AIRS", "PRIMAL RENT"], "'PARLIAMENT' satyr anagram unscrambles to 'PARTIAL MEN'."),
        ("TOTAL ECLIPSE", "TO CELL PISTE", ["TO CELL PISTE", "LUNAR SHADOWS", "SOLAR ORBITER", "DARK HORIZON"], "Complex atmospheric anagram."),
        ("PERFECTIONIST", "I NOTICE ROT PENS", ["I NOTICE ROT PENS", "ONE WHO CLEANS", "PURE FOCUSED", "FLAWLESS MIND"], "'PERFECTIONIST' unscrambles into 'I NOTICE ROT PENS'.")
    ]
    for letters, ans, opts, exp in ana_v:
        items.append(("veteran", "anagram", f"Solve this master anagram for '{letters}':", ans, ",".join(opts), exp))

    # Idioms (20)
    idi_v = [
        ("Pyrrhic victory", "A triumph attained at catastrophic, ruinous cost", ["A triumph attained at catastrophic, ruinous cost", "An effortless victory in sports", "A diplomatic peace accord", "A sudden unexpected defeat"], "King Pyrrhus defeated Romans while suffering irrecoverable losses."),
        ("Damoclean sword", "Imminent and precarious disaster hovering over success", ["Imminent and precarious disaster hovering over success", "A medieval royal executioner", "Ancient military weaponry", "Unbreakable honor bonds"], "The sword suspended over Damocles' head by a horsehair."),
        ("Gordian knot", "An exceedingly intractable problem solved by bold unconventional action", ["An exceedingly intractable problem solved by bold unconventional action", "A sailor's rigging knot", "A decorative braided tapestry", "A legal marital contract"], "Alexander the Great solved the Gordian knot with his blade."),
        ("Procrustean bed", "An arbitrary standard to which exact conformity is violently forced", ["An arbitrary standard to which exact conformity is violently forced", "Luxury orthopedic furniture", "Ancient Greek hospitable ritual", "A peaceful resting chamber"], "Procrustes tortured victims to fit his iron bedframe."),
        ("Bite the dust", "To perish, fail ignominiously, or be slain", ["To perish, fail ignominiously, or be slain", "Work under arid conditions", "Eat humble meals", "Clean battlefield debris"], "Centuries-old idiom for mortality or defeat."),
        ("Cross the Rubicon", "Take an irreversible step committing oneself to a dangerous course", ["Take an irreversible step committing oneself to a dangerous course", "Navigate turbulent rivers", "Negotiate truce treaties", "Retire from armed combat"], "Caesar marched over the Rubicon river into civil war."),
        ("Between Scylla and Charybdis", "Caught between two equally deadly perils", ["Caught between two equally deadly perils", "Sailing through open straits", "Mythological diplomacy", "Balancing sea merchants"], "Facing the monster Scylla or the whirlpool Charybdis."),
        ("Achilles' heel", "A vulnerable weak point in an otherwise invulnerable person", ["A vulnerable weak point in an otherwise invulnerable person", "An anatomical tendon sprain", "Heroic military stamina", "Running speed endurance"], "Achilles was dipped into the River Styx everywhere except his heel."),
        ("Fly in the ointment", "A minor flaw that spoils the enjoyment or value of something", ["A minor flaw that spoils the enjoyment or value of something", "An insect medication", "Chemical impurity", "A ruined fragrance"], "Originates in Ecclesiastes regarding dead flies corrupting perfume."),
        ("Drink the Kool-Aid", "Blindly embrace a dogma or catastrophic worldview", ["Blindly embrace a dogma or catastrophic worldview", "Enjoy flavored beverages", "Toast to political victory", "Quench desert thirst"], "Alludes to the tragic Jonestown cult conformity."),
        ("Hoist with one's own petard", "Vanquished by the very trap one engineered for others", ["Vanquished by the very trap one engineered for others", "Blown upward by cannons", "Awarded medals in battle", "Promoted for marksmanship"], "A 'petard' was an explosive device prone to backfire."),
        ("Read the riot act", "Deliver a severe reprimand warning of harsh punishment", ["Deliver a severe reprimand warning of harsh punishment", "Protest civil government laws", "Recite constitutional decrees", "Announce police deployment"], "From 18th-century British law commanding crowds to disperse."),
        ("Shed crocodile tears", "Manifest insincere, hypocritical grief or regret", ["Manifest insincere, hypocritical grief or regret", "Weep over reptile injuries", "Express genuine mourning", "Produce bodily lacrimation"], "From ancient folklore alleging crocodiles weep while devouring prey."),
        ("Open Pandora's box", "Unleash unforeseen and uncontrollable complications", ["Unforeseen and uncontrollable complications", "Unlock valuable jewelry", "Perform secret rituals", "Discover ancient archeology"], "Hesiod's myth of all human evils being set free."),
        ("Graveyard shift", "Working the deepest nocturnal shift from midnight to dawn", ["Working the deepest nocturnal shift from midnight to dawn", "Burying corpses professionally", "Attending funeral services", "Working solitary shifts"], "The quietest and most desolate hours of labor."),
        ("Catch-22", "A paradoxical problem from which one cannot escape due to contradictory rules", ["A paradoxical problem from which one cannot escape due to contradictory rules", "A standard military penal code", "A lottery drawing outcome", "A flying altitude restriction"], "Coined by Joseph Heller's masterpiece novel."),
        ("Swan song", "A final gesture, musical effort, or public performance before departure", ["A final gesture or performance before departure", "Waterfowl nesting calls", "Ornithological behavior", "A ceremonial coronation hymn"], "Ancient belief that swans sing beautifully only upon death."),
        ("Throw down the gauntlet", "Issue a formal, uncompromising challenge to fight", ["Issue a formal challenge to fight", "Drop leather equestrian gear", "Surrender military weapons", "Resign political appointments"], "Medieval knights cast armored gloves to challenge rivals."),
        ("Mad as a hatter", "Completely unhinged, eccentric, or violently insane", ["Completely unhinged or insane", "Skillful millinery artisan", "Excited by tea parties", "Frustrated by haberdashery"], "Caused by mercury poisoning among 19th-century hat makers."),
        ("Pave with good intentions", "Disastrous outcomes emerging from well-meaning motives", ["Disastrous outcomes emerging from well-meaning motives", "Road construction contracts", "Charitable philanthropic funds", "Pure righteous behavior"], "From 'The road to hell is paved with good intentions.'")
    ]
    for phrase, ans, opts, exp in idi_v:
        items.append(("veteran", "idiom", f"Deconstruct the etymological idiom '{phrase}':", ans, ",".join(opts), exp))

    # Vocabulary (20)
    voc_v = [
        ("The intentional destruction or killing of an entire national or ethnic population is:", "Genocide", ["Genocide", "Homicide", "Regicide", "Fratricide"], "Genocide targets racial, national, or ethnic entities."),
        ("The rhetorical fallacy of attacking the person rather than their argument is:", "Ad hominem", ["Ad hominem", "Straw man", "Post hoc", "Red herring"], "Ad hominem attacks character instead of premise."),
        ("A word or phrase constructed by reversing another word's exact letters is an:", "Anagram", ["Anagram", "Palindrome", "Acronym", "Homonym"], "Anagrams rearrange letters to create new terms."),
        ("A word or sentence that reads identically forwards and backwards is a:", "Palindrome", ["Palindrome", "Oxymoron", "Tautology", "Neologism"], "Palindromes maintain phonetic/spelling symmetry (e.g., 'racecar')."),
        ("A self-contradictory figure of speech pairing opposite terms together is an:", "Oxymoron", ["Oxymoron", "Hyperbole", "Metonymy", "Euphemism"], "Oxymorons juxtapose opposites (e.g., 'deafening silence')."),
        ("The grammatical inversion occurring in sentences beginning with negative adverbs is called:", "Subject-Auxiliary Inversion", ["Subject-Auxiliary Inversion", "Passive Diathesis", "Subjunctive Concord", "Split Infinitive"], "Negative adverbs (e.g., 'Rarely did he') demand inversion."),
        ("The linguistic phenomenon where one sensory perception involuntarily stimulates another is:", "Synesthesia", ["Synesthesia", "Anesthesia", "Aphasia", "Dyslexia"], "Synesthetes may 'taste colors' or 'see sounds'."),
        ("The study of the origins, history, and development of linguistic words is:", "Etymology", ["Etymology", "Entomology", "Epistemology", "Eschatology"], "Etymology traces roots and morphological development."),
        ("The philosophical study of the nature, grounds, and limits of knowledge is:", "Epistemology", ["Epistemology", "Ontology", "Aesthetics", "Ethics"], "Epistemology investigates what constitutes valid knowledge."),
        ("A mild or indirect expression substituted for one considered unpleasantly blunt is a:", "Euphemism", ["Euphemism", "Dysphemism", "Colloquialism", "Solecism"], "Euphemisms soften harsh realities (e.g., 'passed away')."),
        ("The repetition of identical vowel sounds within consecutive words is known as:", "Assonance", ["Assonance", "Consonance", "Alliteration", "Onomatopoeia"], "Assonance matches vowel harmonics within words."),
        ("A figure of speech in which a part of something represents the whole is:", "Synecdoche", ["Synecdoche", "Metaphor", "Allegory", "Personification"], "Synecdoche refers to things by parts (e.g., 'all hands on deck')."),
        ("An individual exhibiting extreme lack of empathy, grandiosity, and deceptive traits is a:", "Psychopath", ["Psychopath", "Neurotic", "Introvert", "Schizoid"], "Psychopathy manifests callous, unempathic conduct."),
        ("The attribution of human traits and emotional behaviors to non-human entities is:", "Anthropomorphism", ["Anthropomorphism", "Therianthropy", "Zoomorphism", "Polytheism"], "Anthropomorphism humanizes beasts or deities."),
        ("A newly coined lexical word or expression entering common language usage is a:", "Neologism", ["Neologism", "Archaism", "Idiom", "Anachronism"], "Neologisms are newly invented linguistic terms."),
        ("The deliberate evasion of answering questions by using ambiguous, misleading speech is:", "Equivocation", ["Equivocation", "Elocution", "Eloquentia", "Articulation"], "Equivocation relies on duplicitous semantic ambiguity."),
        ("A state of supreme, celestial perfection characterized by transcendental beauty is:", "Sublime", ["Sublime", "Mundane", "Prosaic", "Gaudy"], "The sublime evokes reverent awe and elevation."),
        ("The psychological tendency to interpret new evidence as confirmation of existing beliefs is:", "Confirmation bias", ["Confirmation bias", "Hindsight bias", "Anchoring effect", "Cognitive dissonance"], "Confirmation bias ignores disproving evidence."),
        ("The rhetorical technique of deliberately understating an affirmative by asserting its negative is:", "Litotes", ["Litotes", "Hyperbole", "Zeugma", "Chiasmus"], "Litotes asserts through negation (e.g., 'not bad at all')."),
        ("A person who actively opposes and repudiates traditional religious or cultural beliefs is an:", "Iconoclast", ["Iconoclast", "Orthodox", "Zealot", "Dogmatist"], "Iconoclasts destroy orthodox or revered icons.")
    ]
    for prompt, ans, opts, exp in voc_v:
        items.append(("veteran", "vocabulary", prompt, ans, ",".join(opts), exp))

    return items

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            difficulty TEXT NOT NULL,
            category TEXT NOT NULL,
            prompt TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            options TEXT NOT NULL,
            explanation TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            score INTEGER NOT NULL,
            streak INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Always ensure the full 300 question set is present
    cursor.execute("SELECT COUNT(*) AS count FROM questions")
    count = cursor.fetchone()["count"]

    if count < 300:
        cursor.execute("DELETE FROM questions")
        pool = build_questions_pool()
        cursor.executemany("""
            INSERT INTO questions (difficulty, category, prompt, correct_answer, options, explanation)
            VALUES (?, ?, ?, ?, ?, ?)
        """, pool)
        conn.commit()
        print(f"Successfully seeded {len(pool)} categorized questions into game.db!")
    else:
        print(f"Database already contains {count} questions.")

    conn.close()

if __name__ == "__main__":
    init_db()
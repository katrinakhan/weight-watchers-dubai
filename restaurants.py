"""Dubai dining guide — six cuisines, seven restaurants each.

Sourced pages use a published menu we could read. Draft pages are a first AI
guess so the list is usable; confirm when you call. Calories are coach estimates.
Dish photos are typical plates. Venue photos are illustrations — not live branch
photography. Menus change.
"""

CUISINES = [
    {
        "slug": "arabic",
        "name": "Arabic",
        "blurb": "Seven rooms to start. Qahwa unsweetened or water. Places with a published menu are sourced; the rest are labelled AI first drafts for you to confirm when you call.",
    },
    {
        "slug": "chinese",
        "name": "Chinese",
        "blurb": "Seven rooms. Jasmine or green tea unsweetened where they list it — chamomile only if that kitchen actually serves it. Drafts are marked until you call.",
    },
    {
        "slug": "japanese",
        "name": "Japanese",
        "blurb": "Seven rooms: harbour counter, izakaya, hotel Japanese. Unsweetened green tea or water. AI drafts are labelled.",
    },
    {
        "slug": "indian",
        "name": "Indian",
        "blurb": "Seven rooms. Tandoor and South Indian vegetarian. Water or unsweetened chai. Drafts wait for your phone call.",
    },
    {
        "slug": "filipino",
        "name": "Filipino",
        "blurb": "Seven rooms to start — Max’s and Pancake House sourced, the rest AI drafts for you to confirm.",
    },
    {
        "slug": "sri-lankan",
        "name": "Sri Lankan",
        "blurb": "Seven rooms. Chef Lanka and Cinnamon Tree sourced; the rest are first drafts until you call.",
    },
]


DRINKS = {
    "arabic": (
        "Arabic qahwa (unsweetened coffee with cardamom) or still water — essentially no calories. "
        "Mint tea only if it is unsweetened. Skip karak with sugar, fresh cocktail juices, "
        "and anything topped with ashta, honey or ice cream."
    ),
    "chinese": (
        "Jasmine tea or green tea, unsweetened — that is what most of these rooms actually list "
        "(Din Tai Fung prints jasmine, green and black tea). Chamomile or other herbal tea only "
        "if it is on that restaurant’s drinks card; don’t assume. Water is always safe. "
        "Skip milk tea with boba, lemon iced tea with syrup, and fruit juices."
    ),
    "japanese": (
        "Green tea (unsweetened) or still water. Skip sake, chuhai, and sweet sodas. "
        "3Fils homemade sodas are still sugar — water is the fat-loss order."
    ),
    "indian": (
        "Water, soda water, or unsweetened masala tea if they will skip the sugar. "
        "Skip mango lassi, sweet nimbu pani, and dummy cocktails."
    ),
    "filipino": (
        "Water or unsweetened iced tea if they have it without syrup. "
        "Skip halo-halo drinks, sweet juices, and unlimited-soda with buffet."
    ),
    "sri-lankan": (
        "Water, plain tea unsweetened, or king coconut water if it is unsweetened. "
        "Skip faluda, sweet lassi, and bottled Sri Lankan sodas."
    ),
}

HOW = {
    "arabic": "Salad or soup first. Qahwa or water with the meal. Grill as the main. One pita for the whole table, then ask them to take the bread. Leave fries and kunafa.",
    "chinese": "Tea first, no sugar. One steamed or grilled protein plus greens or soup. Do not also order fried rice and noodles.",
    "japanese": "Start with sashimi, salad or a skewer. One ramen bowl or one robata fish is a full meal. Stop before dessert.",
    "indian": "Kachumber or soup, then tandoor. One roti for the table if you need bread — not a naan each.",
    "filipino": "Sinigang or salad first so you don’t arrive starving to the fryer. One main. Skip unlimited fried chicken.",
    "sri-lankan": "Hopper or soup, then curry or fish with greens. A few spoons of rice, not a mountain. Leave kottu for another night.",
}

SKIP = {
    "arabic": [
        "Fried kibbeh, sambousek and cheese rolls as the whole start.",
        "French fries that come with every grill.",
        "Kunafa, baklava and fresh cocktail juices.",
    ],
    "chinese": [
        "Dynamite shrimp, spring rolls and extra fried rice.",
        "Sweet-and-sour as the main plus noodles.",
        "Boba, mango pomelo and dessert platters.",
    ],
    "japanese": [
        "Tempura, spicy tuna crispy rice and extra rolls after you are full.",
        "Wine or sake pairing.",
        "Dessert plus a sweet soda.",
    ],
    "indian": [
        "Samosa chaat and a naan each.",
        "Butter chicken or tikka masala gravy as well as tandoor.",
        "Mango lassi and gulab jamun.",
    ],
    "filipino": [
        "Fried chicken, crispy pata and lumpiang shanghai.",
        "Extra white rice plus dessert.",
        "Unlimited fried-chicken nights.",
    ],
    "sri-lankan": [
        "Kottu plus lamprais plus fried short eats.",
        "Devilled plates with extra rice.",
        "Caramel pudding after a full rice-and-curry.",
    ],
}


def C(label, name, kcal, note, img):
    return {"label": label, "name": name, "kcal": kcal, "note": note, "img": img}


def R(**kwargs):
    cuisine = kwargs["cuisine_slug"]
    kwargs["search"] = " ".join(
        [
            kwargs["name"],
            kwargs["area"],
            cuisine,
            kwargs.get("cuisine_label", ""),
            kwargs.get("aka", ""),
        ]
    ).lower()
    kwargs.setdefault("venue_img", f"venue-{kwargs['slug']}.png")
    kwargs.setdefault(
        "venue_caption",
        "Illustration of this kind of room — not a live photo of this branch.",
    )
    kwargs.setdefault("draft", False)
    kwargs.setdefault("drinks", DRINKS[cuisine])
    kwargs.setdefault("how", HOW[cuisine])
    kwargs.setdefault("skip", SKIP[cuisine])
    courses = kwargs.pop("courses", None)
    kwargs["meal"] = (
        {"plates": courses, "kcal_total": sum(p["kcal"] for p in courses)}
        if courses
        else None
    )
    return kwargs


RESTAURANTS = [
    R(
        slug="reem-al-bawadi",
        name="Reem Al Bawadi",
        area="Marina Walk, Jumeirah, Downtown and other branches",
        cuisine_slug="arabic",
        cuisine_label="Arabic · Levantine",
        price="mid",
        price_label="Mid-range",
        typical="AED 40–90",
        stars="Busy well-known chain",
        why="Everyday Lebanese. Fatoush, lentil soup and tawook are on their own menu — skip the fried mezza mix.",
        menu_source="Reem Al Bawadi dine-in / LimeTray menu (Fatoush, Lentil Soup, Shish Tawook Plate).",
        menu_url="https://reemalbawadi.limetray.com/menu",
        drinks="Arabic qahwa unsweetened, or still water. Their menu also lists lentil soup and fatoush — good. Skip Reem Al Bawadi Cocktail (fruit, ashta, pistachio, honey), kenafa, and Pepsi with the grill deals.",
        how="Fatoush, lentil soup, shish tawook. Leave the fries. One pita. Qahwa after if you want a finish with almost no calories.",
        courses=[
            C("Salad", "Fatoush", 180, "On their menu: tomato, cucumber, lettuce, onion, herbs, lemon-olive oil, crispy bread (AED 23). Ask for less fried bread.", "dish-fattoush.png"),
            C("Soup", "Lentil soup", 150, "On their menu: lentils with cumin (AED 19).", "dish-lentil-soup.png"),
            C("Main", "Shish tawook plate", 380, "On their menu: 2 skewers of chargrilled chicken, lemon-garlic (AED 42). Skip the French fries it is served with.", "dish-kebabs.png"),
        ],
    ),
    R(
        slug="zaroob",
        name="Zaroob",
        area="DIFC, Dubai Marina and other branches",
        cuisine_slug="arabic",
        cuisine_label="Arabic · Levant street",
        price="mid",
        price_label="Mid-range",
        typical="AED 25–70",
        stars="4.7★ typical on delivery apps · very popular",
        why="Street Levant. Tawook and fattoush are printed on their Deliveroo menu.",
        menu_source="Zaroob DIFC Deliveroo menu (Fattoush, Tabbouleh, Lentil Soup, Tawook Platter, Mixed Grill Platter).",
        menu_url="https://deliveroo.ae/en/menu/dubai/difc/zaroob-trade-centre",
        drinks="Arabic qahwa unsweetened or still water. Skip lemonade, fresh juices, and anything with ashta or honey.",
        how="Fattoush, lentil soup, tawook platter. One pita for the table. Qahwa after. Leave fries and the mega salads.",
        courses=[
            C("Salad", "Fattoush", 170, "Named on Zaroob’s DIFC menu. Not the 1 kg MEGA fattoush.", "dish-fattoush.png"),
            C("Soup", "Lentil soup", 140, "Named on the same menu.", "dish-lentil-soup.png"),
            C("Main", "Tawook platter", 400, "On their grills list: 2 charcoal tawouk skewers. Skip the fries and extra pita.", "dish-kebabs.png"),
        ],
    ),
    R(
        slug="al-fanar",
        name="Al Fanar Restaurant & Café",
        area="Festival City, Al Seef, Al Barsha Park",
        cuisine_slug="arabic",
        cuisine_label="Arabic · Emirati",
        price="mid",
        price_label="Mid-range",
        typical="AED 50–90",
        stars="Michelin-selected (Al Seef) · classic Emirati",
        why="Emirati café. Grilled sea bream and lentil soup are on published Al Fanar menus — not a copied Lebanese grill.",
        menu_source="Al Fanar Expo/business lunch PDF (lentil soup, Al Fanar salad, grilled sea bream) and published Al Fanar dish lists (grilled seabream, harees, machboos).",
        menu_url="https://www.alfanarrestaurant.com/",
        drinks="Arabic qahwa unsweetened, or water. Skip karak with sugar and dessert drinks. Emirati coffee is the zero-calorie finish.",
        how="Al Fanar salad, lentil soup, grilled sea bream. Share rice if it comes. Qahwa instead of luqaimat tonight.",
        courses=[
            C("Salad", "Al Fanar salad", 120, "Named on their Expo/business lunch menu.", "dish-tomato-salad.png"),
            C("Soup", "Lentil soup", 150, "On the same Al Fanar lunch menu (also listed as sambosa/lentil soup at lunch).", "dish-lentil-soup.png"),
            C("Main", "Grilled sea bream", 380, "On Al Fanar menus: charcoal grilled sea bream with bread or white rice. Take salad not a personal machboos mountain.", "dish-grilled-fish.png"),
        ],
    ),
    R(
        slug="al-nafoorah",
        name="Al Nafoorah",
        area="Jumeirah Al Qasr, Madinat Jumeirah",
        cuisine_slug="arabic",
        cuisine_label="Arabic · Lebanese",
        price="high",
        price_label="High-end",
        typical="AED 300–550",
        stars="Hotel Lebanese classic",
        why="The one high-end Arabic room in this first version — because Jumeirah published the PDF.",
        menu_source="Jumeirah Al Nafoorah à la carte PDF (fattoush; mixed grill with lamb chops).",
        menu_url="https://cd-hospitality.jumeirah.com/-/mediadh/dh/hospitality/jumeirah/restaurants/dubai/al-qasr-al-nafoorah/restaurant-menu/alnafoorahfoodmenu.pdf",
        courses=[
            C("Salad", "Fattoush", 180, "PDF: cucumber, tomato, herbs, pomegranate dressing, toasted Arabic bread (AED 48). Less bread if you can.", "dish-fattoush.png"),
            C("Main", "Mixed grill with lamb chops (for one)", 480, "PDF: cubed lamb fillet, kofta, shish taouk, lamb chops. Leave the fries.", "dish-kebabs.png"),
        ],
    ),
    R(
        slug="din-tai-fung",
        name="Din Tai Fung",
        area="Dubai Mall, Mall of the Emirates, Dubai Hills, Bluewaters",
        cuisine_slug="chinese",
        cuisine_label="Chinese · Taiwanese",
        price="mid",
        price_label="Mid-range",
        typical="AED 90–180",
        stars="4.5★ typical · always packed",
        why="Official UAE menu. Xiao long bao is their dish — not Hutong’s steamed cod.",
        menu_source="Din Tai Fung UAE official menu (spicy cucumber, steamed chicken soup, chicken xiao long bao).",
        menu_url="https://www.dintaifungae.com/menu?menu=bluewatersmenu",
        drinks="Din Tai Fung’s drinks list includes jasmine tea, green tea and black tea — order them unsweetened. Water is fine. Skip milk tea with boba and fruit teas.",
        how="Spicy cucumber, chicken soup, one steamer of xiao long bao. That is dinner. No fried rice, no golden lava buns.",
        courses=[
            C("Starter", "Spicy cucumber", 80, "On DTF UAE appetizers.", "dish-tomato-salad.png"),
            C("Soup", "Traditional steamed chicken soup", 150, "On DTF UAE soups.", "dish-lentil-soup.png"),
            C("Main", "Chicken xiao long bao (6 pcs)", 260, "Official UAE xiao long bao list. Don’t add fried rice.", "dish-dumplings.png"),
        ],
    ),
    R(
        slug="noodle-house",
        name="The Noodle House",
        area="Madinat Jumeirah, JBR and other branches",
        cuisine_slug="chinese",
        cuisine_label="Chinese · Asian soul food",
        price="mid",
        price_label="Mid-range",
        typical="AED 60–120",
        stars="Casual, well-known mall/souk brand",
        why="Talabat/Yalla menus name siew mai, kale salad and black pepper beef — not a dumpling-soup-fish clone.",
        menu_source="The Noodle House Dubai delivery menus (Prawns Siew Mai, Asia Kale salad, Duck Wonton Soup, Black Pepper Beef).",
        menu_url="https://www.soukmadinatjumeirah.ae/en/outlets/the-noodle-house",
        drinks="Green tea or jasmine tea unsweetened if they have it, otherwise still water. Skip lemon iced tea with syrup and fruit coolers.",
        how="Siew mai, kale salad, black pepper beef. No fried rice. Tea with the meal.",
        courses=[
            C("Starter", "Prawns siew mai", 200, "On their street-bites list. Steamed, not vegetable spring rolls.", "dish-dumplings.png"),
            C("Salad", "Asia kale salad", 140, "On their salads & soups list.", "dish-greens.png"),
            C("Main", "Black pepper beef", 420, "On their stir-fry list (rice ordered separately — skip the egg fried rice).", "dish-kebabs.png"),
        ],
    ),
    R(
        slug="pf-changs",
        name="P.F. Chang's",
        area="Dubai Mall, Festival City and other UAE branches",
        cuisine_slug="chinese",
        cuisine_label="Chinese · American-Chinese",
        price="mid",
        price_label="Mid-range",
        typical="AED 70–140",
        stars="Busy mall Chinese",
        why="Dubai menus list lettuce wraps and ginger chicken with broccoli. Skip dynamite shrimp.",
        menu_source="P.F. Chang’s Dubai menu listings (Chang’s Chicken Lettuce Wraps, Edamame, Ginger Chicken with Broccoli).",
        menu_url="https://www.pfchangsme.com/en/dubaimallmenu",
        drinks="Green tea unsweetened or water. Skip mocktails, lychee lemonade, and anything with syrup.",
        how="Lettuce wraps, edamame, ginger chicken with broccoli. Stop there. Tea, not a dummy cocktail.",
        courses=[
            C("Starter", "Chang's chicken lettuce wraps", 280, "Signature on Dubai P.F. Chang’s lists (~AED 51–53). Use the lettuce, go easy on the crispy rice sticks.", "dish-inihaw.png"),
            C("Starter 2", "Edamame", 120, "On Dubai starter lists (~AED 33).", "dish-greens.png"),
            C("Main", "Ginger chicken with broccoli", 390, "On Dubai poultry lists. Not sesame chicken or dynamite shrimp.", "dish-greens.png"),
        ],
    ),
    R(
        slug="hutong",
        name="Hutong",
        area="DIFC",
        cuisine_slug="chinese",
        cuisine_label="Chinese · northern",
        price="high",
        price_label="High-end",
        typical="AED 300–600",
        stars="Trendy DIFC",
        why="Kept because we have their à la carte PDF — not because this app is only fine dining.",
        menu_source="Hutong Dubai à la carte PDF.",
        menu_url="https://www.hutong-dubai.com/wp-content/uploads/2022/01/HT-Dubai-ALC-Menu-250110.pdf",
        courses=[
            C("Starter", "Steamed wild mushroom & truffle bao", 220, "Bao list, AED 75. Steamed.", "dish-dumplings.png"),
            C("Soup", "Hot & sour soup with Chinese leeks", 90, "Soup list, AED 60.", "dish-hot-sour.png"),
            C("Main", "Steamed cod with fresh Sichuan green pepper", 340, "Fish list, AED 258. Not Red Lantern fried crab.", "dish-steamed-fish.png"),
        ],
    ),
    R(
        slug="3fils",
        name="3Fils",
        area="Jumeirah Fishing Harbour",
        cuisine_slug="japanese",
        cuisine_label="Japanese-inspired Asian",
        price="mid",
        price_label="Mid-range",
        typical="AED 150–300",
        stars="Michelin Bib / 50 Best · walk-in",
        why="Their English menu names hamachi carpaccio. Not Zuma’s robata.",
        menu_source="3fils.com ADA English menu (hamachi carpaccio, salmon carpaccio) and seaweed salad named on 3fils.com.",
        menu_url="https://3fils.com/ada-english-menu/",
        courses=[
            C("Starter", "Hamachi carpaccio", 170, "Official English menu: hamachi, tomato-yuzu, quinoa, sumac, lime zest.", "dish-sashimi.png"),
            C("Salad", "Seaweed salad", 90, "Named on 3fils.com guest notes and published 3Fils lists.", "dish-greens.png"),
            C("Starter 2", "Salmon carpaccio", 160, "On the same English menu.", "dish-sashimi.png"),
        ],
    ),
    R(
        slug="kinoya",
        name="Kinoya",
        area="The Onyx Tower 2, The Greens / Barsha Heights",
        cuisine_slug="japanese",
        cuisine_label="Japanese · izakaya & ramen",
        price="mid",
        price_label="Mid-range",
        typical="AED 80–180",
        stars="MENA 50 Best · packed izakaya",
        why="Their site lists shoyu/shio/miso ramen and yakitori. Reviews of this room name wagyu tsukune and onsen egg.",
        menu_source="kinoya.ae (shoyu, shio, miso ramen, yakitori) and SquareMeal/50 Best notes on this restaurant (wagyu tsukune, onsen egg with dashi).",
        menu_url="https://kinoya.ae/",
        courses=[
            C("Starter", "Wagyu tsukune", 220, "Named as a Kinoya yakitori highlight (egg yolk and soy). One or two skewers.", "dish-robata.png"),
            C("Starter 2", "Onsen egg with dashi", 160, "Named at this restaurant (onsen tamago on rice with dashi). Share the rice.", "dish-miso.png"),
            C("Main", "Shoyu ramen", 480, "On Kinoya’s own ramen list. One bowl is the meal — don’t add extra fried tempura.", "dish-hot-sour.png"),
        ],
    ),
    R(
        slug="zuma",
        name="Zuma",
        area="DIFC",
        cuisine_slug="japanese",
        cuisine_label="Japanese · contemporary",
        price="high",
        price_label="High-end",
        typical="AED 350–700",
        stars="DIFC institution",
        why="One high-end Japanese because Dubai menu guides name these plates.",
        menu_source="Published Zuma Dubai menu guides (yellowtail sashimi, miso soup, robata sea bass).",
        menu_url="https://www.zumarestaurant.com/",
        courses=[
            C("Starter", "Yellowtail sashimi, yuzu soy", 180, "Recurring Zuma Dubai sashimi line.", "dish-sashimi.png"),
            C("Soup", "Miso soup", 40, "On Zuma Dubai menu guides.", "dish-miso.png"),
            C("Main", "Robata sea bass, yuzu soy", 320, "Named robata fish. Not miso black cod unless you share it.", "dish-robata.png"),
        ],
    ),
    R(
        slug="gazebo",
        name="Gazebo",
        area="Several Dubai branches (Al Karama and others)",
        cuisine_slug="indian",
        cuisine_label="Indian · North / Awadhi",
        price="mid",
        price_label="Mid-range",
        typical="AED 40–80",
        stars="4.4★ typical · family Indian",
        why="Official gazebo.ae menu: kachumber, lentil shorba, murgh tikka.",
        menu_source="gazebo.ae/menu (Kachumber Salad, Shorba Dil Pasand lentil soup, Murgh Tikka AED 43, Tandoori Murgh).",
        menu_url="https://www.gazebo.ae/menu/",
        courses=[
            C("Salad", "Kachumber salad", 70, "On Gazebo’s menu: onion, tomato, cucumber, green chilli, coriander, lime.", "dish-kachumber.png"),
            C("Soup", "Shorba dil pasand (lentil soup)", 140, "On their soup list, AED 21.", "dish-lentil-soup.png"),
            C("Main", "Murgh tikka", 290, "Official menu: boneless chicken, tandoori yoghurt marinade, chargrilled, AED 43. Not tikka masala gravy.", "dish-chicken-tikka.png"),
        ],
    ),
    R(
        slug="calicut-paragon",
        name="Calicut Paragon",
        area="Al Karama and Al Nahda, Dubai",
        cuisine_slug="indian",
        cuisine_label="Indian · Kerala",
        price="mid",
        price_label="Mid-range",
        typical="AED 35–70",
        stars="Karama favourite",
        why="Their site lists claypot tandoor: fish tikka, chicken tikka, tandoori chicken.",
        menu_source="calicutparagon.com claypot menu (Fish Tikka, Chicken Tikka, Tandoori Chicken, Paneer Tikka).",
        menu_url="https://calicutparagon.com/category/menu/from-the-claypot/",
        courses=[
            C("Starter", "Paneer tikka", 260, "On Paragon’s claypot list. Vegetarian grill.", "dish-chicken-tikka.png"),
            C("Starter 2", "Fish tikka", 280, "On the same claypot list.", "dish-tandoor-fish.png"),
            C("Main", "Tandoori chicken", 350, "Named on their claypot menu. Skip extra naan; one tandoori roti if you need bread.", "dish-chicken-tikka.png"),
        ],
    ),
    R(
        slug="maxs",
        name="Max's Restaurant",
        area="Mankhool and other UAE branches",
        cuisine_slug="filipino",
        cuisine_label="Filipino",
        price="mid",
        price_label="Mid-range",
        typical="AED 40–80",
        stars="The fried-chicken house — order the sinigang instead",
        why="Official UAE site. We only use dishes they printed.",
        menu_source="maxsrestaurant.ae (Sinigang na Tiyan ng Bangus AED 54, Kare-Kare AED 63).",
        menu_url="https://www.maxsrestaurant.ae/",
        courses=[
            C("Soup / main", "Sinigang na tiyan ng bangus", 280, "Official: milkfish belly in tamarind broth with vegetables.", "dish-sinigang.png"),
            C("If you need more", "Kare-kare (share)", 450, "Official: oxtail peanut stew. Share it. Skip fried chicken and lumpiang shanghai.", "dish-dhal.png"),
        ],
    ),
    R(
        slug="pancake-house",
        name="Pancake House",
        area="Burjuman / Mankhool",
        cuisine_slug="filipino",
        cuisine_label="Filipino · café",
        price="mid",
        price_label="Mid-range",
        typical="AED 35–80",
        stars="Well-known Pinoy café brand",
        why="Talabat menu for this Dubai brand names salmon sinigang and Caesar salad — not pancakes, if you are watching weight.",
        menu_source="Pancake House Dubai Talabat menu (Salmon Sinigang, Caesar Salad, Beef Broccoli Rice Bowl).",
        menu_url="https://www.talabat.com/uae/restaurant/725661/pancake-house-al-mankhool",
        courses=[
            C("Salad", "Caesar salad", 220, "On their starter/soup/salad list. Dressing on the side if you can.", "dish-greens.png"),
            C("Soup", "Salmon sinigang", 250, "On the same list — their sour soup, not Max’s bangus belly.", "dish-sinigang.png"),
            C("Main", "Beef broccoli rice bowl", 420, "On their rice-bowl list. Better than pancake platters. Leave some rice.", "dish-kebabs.png"),
        ],
    ),
    R(
        slug="chef-lanka",
        name="Chef Lanka",
        area="Al Karama",
        cuisine_slug="sri-lankan",
        cuisine_label="Sri Lankan",
        price="mid",
        price_label="Mid-range",
        typical="AED 30–80",
        stars="Long-running Karama name",
        why="Their own site names egg hoppers, coconut sambol, chicken curry, kottu and lamprais. We pick the lighter ones they listed.",
        menu_source="cheflankarestaurant.com (egg hoppers, coconut sambol, chicken curry, kottu roti, lamprais, seafood hoppers).",
        menu_url="https://cheflankarestaurant.com/index.html",
        courses=[
            C("Starter", "Egg hoppers (1–2)", 180, "Named on their breakfast list, with coconut chutney/sambol.", "dish-hopper.png"),
            C("Side", "Coconut sambol", 90, "Named on their site. A spoon, not a heap.", "dish-mallung.png"),
            C("Main", "Chicken curry", 380, "Named on their site. Small rice. Skip kottu and lamprais if fat loss is the point tonight.", "dish-dhal.png"),
        ],
    ),
    R(
        slug="cinnamon-tree",
        name="Cinnamon Tree",
        area="Satwa, Barsha, International City",
        cuisine_slug="sri-lankan",
        cuisine_label="Sri Lankan",
        price="mid",
        price_label="Mid-range",
        typical="AED 30–70",
        stars="Well-known among Sri Lankans in Dubai",
        why="A 2026 write-up of this restaurant lists egg hoppers, string hopper sets and pol roti — not a copied Chef Lanka plate.",
        menu_source="Curly Tales feature on Cinnamon Tree Dubai (Egg Hoppers, String Hopper Set, Pol Roti Set, Kiribath Sets).",
        menu_url="https://curlytales.com/middle-east/food/this-restaurant-in-dubai-offers-authentic-sri-lankan-dishes-that-will-leave-you-coming-back/",
        courses=[
            C("Starter", "Egg hoppers", 180, "Listed as a Cinnamon Tree short eat.", "dish-hopper.png"),
            C("Main", "String hopper set", 420, "Named as a must-have at this restaurant. Go easy on the coconut gravy; add mallung if they serve greens.", "dish-mallung.png"),
            C("Skip if watching weight", "Mutton koththy", 650, "Also named there — the heavy carb plate. Choose hoppers/string hoppers instead.", "dish-dhal.png"),
        ],
    ),
    # --- Arabic to 7 ---
    R(
        slug="automatic",
        name="Automatic Restaurant",
        area="Several Dubai branches",
        cuisine_slug="arabic",
        cuisine_label="Arabic · Lebanese grill",
        price="mid",
        price_label="Mid-range",
        typical="AED 35–80",
        stars="Old Dubai Lebanese grill",
        draft=True,
        why="AI first draft until you call. Typical Automatic order is grill and salad, not fried mezza.",
        menu_source="AI draft from dishes Automatic-style Lebanese grills usually serve (fattoush, hummus, shish tawook). Confirm when you call.",
        courses=[
            C("Salad", "Fattoush", 180, "Draft: mixed herb salad. Ask for less fried bread.", "dish-fattoush.png"),
            C("Mezze", "Hummus (small)", 180, "Draft: dip vegetables, not a pita mountain.", "dish-dhal.png"),
            C("Main", "Shish tawook", 360, "Draft: grilled chicken skewers. Skip garlic-potato and extra bread.", "dish-kebabs.png"),
        ],
    ),
    R(
        slug="al-hallab",
        name="Al Hallab",
        area="Dubai Mall and other branches",
        cuisine_slug="arabic",
        cuisine_label="Arabic · Lebanese",
        price="mid",
        price_label="Mid-range",
        typical="AED 50–120",
        stars="Well-known Lebanese sweets-and-grill brand",
        draft=True,
        why="AI draft. Their fame is kunafa — for fat loss you skip the sweets counter and grill.",
        menu_source="AI draft (fattoush, lentil soup, mixed grill). Confirm the live card when you call.",
        courses=[
            C("Salad", "Fattoush", 170, "Draft: classic Lebanese salad.", "dish-fattoush.png"),
            C("Soup", "Lentil soup", 150, "Draft: cumin lentil soup if listed.", "dish-lentil-soup.png"),
            C("Main", "Mixed grill", 450, "Draft: tawook, kafta, lamb. Leave fries. Walk past kunafa.", "dish-kebabs.png"),
        ],
    ),
    R(
        slug="logma",
        name="Logma",
        area="Boxpark, City Walk and other branches",
        cuisine_slug="arabic",
        cuisine_label="Arabic · Emirati café",
        price="mid",
        price_label="Mid-range",
        typical="AED 40–90",
        stars="Trendy Emirati café",
        draft=True,
        why="AI draft. Emirati café — harees or grilled fish beats luqaimat.",
        menu_source="AI draft from dishes Logma is known for (harees, machboos, luqaimat to skip). Confirm when you call.",
        courses=[
            C("Soup", "Harees (small)", 280, "Draft: wheat-and-chicken porridge. Filling. Small bowl.", "dish-lentil-soup.png"),
            C("Salad", "Mixed Arabic salad", 110, "Draft: cucumber tomato lemon.", "dish-tomato-salad.png"),
            C("Main", "Grilled fish or chicken (if listed)", 380, "Draft: grill over machboos rice mountain. Qahwa not karak with sugar.", "dish-grilled-fish.png"),
        ],
    ),
    # --- Chinese to 7 ---
    R(
        slug="hakkasan",
        name="Hakkasan",
        area="Atlantis, The Palm",
        cuisine_slug="chinese",
        cuisine_label="Chinese · Cantonese",
        price="high",
        price_label="High-end",
        typical="AED 400–800",
        stars="Hotel Cantonese",
        why="Their Dubai menu names these plates — jasmine tea, not a copied Hutong cod.",
        menu_source="Hakkasan Dubai menu (lotus root salad, hot & sour with chicken, grilled black cod with truffle).",
        menu_url="https://hakkasangroup.com/venues/hakkasan-dubai/menu/",
        drinks="Ask for jasmine tea unsweetened, or still water. Skip the cocktail list.",
        how="Salad or dim sum steamed, soup, then share the black cod. No fried rice on the side.",
        courses=[
            C("Starter", "Lotus root, mizuna & ice plant salad", 120, "Named on Hakkasan Dubai’s salad list.", "dish-greens.png"),
            C("Soup", "Hot & sour soup with chicken", 110, "On their soup list (~AED 68).", "dish-hot-sour.png"),
            C("Main", "Grilled black cod with truffle", 420, "Named Hakkasan Dubai main. Share it.", "dish-grilled-fish.png"),
        ],
    ),
    R(
        slug="royal-china",
        name="Royal China",
        area="DIFC",
        cuisine_slug="chinese",
        cuisine_label="Chinese · Cantonese",
        price="high",
        price_label="High-end",
        typical="AED 200–450",
        stars="DIFC dim sum regulars",
        why="Dubai dim sum PDF only — we still won’t invent a third main.",
        menu_source="Royal China Dubai dim sum PDF (prawn dumplings AED 29; crab meat dumpling soup AED 31).",
        menu_url="https://www.royalchinadubai.com/_files/ugd/fbc0ef_9da6b63eaf4f494893fd0e18df386384.pdf",
        drinks="Jasmine tea or water. Dim sum lunch is the lighter sitting.",
        how="Steamed prawn dumplings and dumpling soup. Stop. Don’t add fried rice because you are in DIFC.",
        courses=[
            C("Starter", "Prawn dumplings", 180, "Printed on their Dubai dim sum PDF.", "dish-dumplings.png"),
            C("Soup", "Crab meat dumpling soup", 160, "Same PDF, AED 31.", "dish-hot-sour.png"),
        ],
    ),
    R(
        slug="tang-town",
        name="Tang Town",
        area="Dubai Mall (Chinatown)",
        cuisine_slug="chinese",
        cuisine_label="Chinese · contemporary",
        price="high",
        price_label="High-end",
        typical="AED 250–500",
        stars="Michelin-recognised mall Chinese",
        why="Their site names beef-and-chive dumplings and double-boiled duck soup.",
        menu_source="tangtown.ae menu pages (handmade beef and chive dumplings; double-boiled duck soup; steamed shrimp dumpling).",
        menu_url="https://tangtown.ae/chinese-restaurant-menu/",
        drinks="Jasmine or green tea unsweetened, or water. Skip mango pomelo sago if you already ate dumplings.",
        how="Steamed dumplings and the duck broth. Peking duck only as a shared taste.",
        courses=[
            C("Starter", "Handmade beef and chive dumplings", 240, "Named on Tang Town’s dim sum list.", "dish-dumplings.png"),
            C("Soup", "Double-boiled duck with salty lemon", 140, "Named on their soup list.", "dish-lentil-soup.png"),
            C("Dim sum", "Steamed shrimp dumpling", 160, "Listed steamed, not their deep-fried chicken dumpling.", "dish-dumplings.png"),
        ],
    ),
    # --- Japanese to 7 ---
    R(
        slug="nobu",
        name="Nobu",
        area="Atlantis, The Palm",
        cuisine_slug="japanese",
        cuisine_label="Japanese · contemporary",
        price="high",
        price_label="High-end",
        typical="AED 400–800",
        stars="Famous globally",
        draft=True,
        why="AI draft from Nobu signatures usually on the Atlantis card (yellowtail jalapeño, black cod). Confirm tonight’s menu.",
        menu_source="AI draft from Nobu-group signatures (yellowtail jalapeño, edamame, black miso cod). Confirm the Atlantis card when you call.",
        drinks="Green tea unsweetened or water. Skip the sake pairing.",
        how="Yellowtail and edamame. Share black cod if you must. No extra fried rock shrimp.",
        courses=[
            C("Starter", "Yellowtail jalapeño (if listed)", 200, "Draft: Nobu’s usual raw yellowtail. Confirm the name on the Dubai card.", "dish-sashimi.png"),
            C("Starter 2", "Edamame", 120, "Draft: steamed beans, salt. Not spicy-mayo edamame if they offer that.", "dish-greens.png"),
            C("Main", "Black cod miso — share", 480, "Draft: the famous rich glaze. One portion for the table, not a piece each plus rice.", "dish-grilled-fish.png"),
        ],
    ),
    R(
        slug="tomo",
        name="TOMO",
        area="Raffles Dubai, Oud Metha",
        cuisine_slug="japanese",
        cuisine_label="Japanese",
        price="high",
        price_label="High-end",
        typical="AED 250–500",
        stars="Hotel Japanese, city views",
        draft=True,
        why="AI draft. Typical TOMO-style order: sashimi, miso, grilled fish.",
        menu_source="AI draft (sashimi, miso soup, grilled fish). Confirm Raffles menu when you call.",
        drinks="Green tea unsweetened or water.",
        how="Sashimi, miso, one grilled fish. Skip tempura sets.",
        courses=[
            C("Starter", "Sashimi moriawase (if listed)", 180, "Draft: chef’s sashimi, no rice.", "dish-sashimi.png"),
            C("Soup", "Miso soup", 40, "Draft: standard Japanese soup.", "dish-miso.png"),
            C("Main", "Grilled fish / robata (if listed)", 340, "Draft: grilled, sauce on the side.", "dish-grilled-fish.png"),
        ],
    ),
    R(
        slug="okku",
        name="Okku",
        area="The H Dubai",
        cuisine_slug="japanese",
        cuisine_label="Japanese · trendy",
        price="high",
        price_label="High-end",
        typical="AED 300–600",
        stars="Nightlife Japanese",
        draft=True,
        why="AI draft. The leak here is cocktails. Food: sashimi then grill.",
        menu_source="AI draft (sashimi, edamame, robata chicken). Confirm when you call.",
        drinks="Water. The bar is the calorie leak — skip sweet cocktails.",
        how="Eat the grill. Don’t drink the menu.",
        courses=[
            C("Starter", "Sashimi / yellowtail (if listed)", 180, "Draft: raw fish first.", "dish-sashimi.png"),
            C("Starter 2", "Edamame", 120, "Draft: steamed.", "dish-greens.png"),
            C("Main", "Robata chicken (if listed)", 280, "Draft: charcoal chicken. Sauce on the side.", "dish-robata.png"),
        ],
    ),
    R(
        slug="kiku",
        name="Kiku",
        area="The Mall, Jumeirah Beach Hotel area (confirm current site)",
        cuisine_slug="japanese",
        cuisine_label="Japanese",
        price="mid",
        price_label="Mid-range to high-end",
        typical="AED 120–250",
        stars="Long-running Dubai Japanese",
        draft=True,
        why="AI draft. Older Dubai Japanese room — sushi and grilled fish, not a fry-up.",
        menu_source="AI draft (miso, salmon sashimi, grilled salmon). Confirm when you call.",
        drinks="Green tea unsweetened or water.",
        how="Sashimi plus one grilled fish. Skip tempura and extra California rolls.",
        courses=[
            C("Soup", "Miso soup", 40, "Draft.", "dish-miso.png"),
            C("Starter", "Salmon sashimi", 160, "Draft.", "dish-sashimi.png"),
            C("Main", "Grilled salmon (if listed)", 350, "Draft: not teriyaki-drowned if you can ask for sauce aside.", "dish-grilled-fish.png"),
        ],
    ),
    # --- Indian to 7 ---
    R(
        slug="punjab-grill",
        name="Punjab Grill",
        area="Souk Al Bahar / Downtown",
        cuisine_slug="indian",
        cuisine_label="Indian · North",
        price="high",
        price_label="High-end",
        typical="AED 200–450",
        stars="Downtown views",
        draft=True,
        why="AI draft. North Indian grill — kebabs yes, dal makhani as a spoon only.",
        menu_source="AI draft (kachumber, chicken tikka, tandoor kebabs). Confirm when you call.",
        drinks="Water. Skip mango lassi.",
        how="Tikka and salad looking at the fountains. No naan each.",
        courses=[
            C("Salad", "Kachumber", 70, "Draft.", "dish-kachumber.png"),
            C("Starter", "Chicken tikka", 290, "Draft: tandoor.", "dish-chicken-tikka.png"),
            C("Main", "Tandoor kebabs (mixed, share)", 400, "Draft: share. Dal makhani only as a spoon.", "dish-kebabs.png"),
        ],
    ),
    R(
        slug="indego",
        name="Indego by Vineet",
        area="Grosvenor House, Dubai Marina",
        cuisine_slug="indian",
        cuisine_label="Indian · fine",
        price="high",
        price_label="High-end",
        typical="Set lunch ~AED 295",
        stars="Marina fine Indian",
        draft=True,
        why="AI draft until we have the current card. Tandoor path.",
        menu_source="AI draft (salad, tandoor chicken, tandoor fish). Confirm Grosvenor menu.",
        drinks="Water. Skip mango cocktails.",
        how="Tandoor + salad. One shared bread.",
        courses=[
            C("Salad", "Kachumber / chopped salad (if listed)", 70, "Draft.", "dish-kachumber.png"),
            C("Starter", "Tandoor chicken", 300, "Draft.", "dish-chicken-tikka.png"),
            C("Main", "Tandoor fish", 330, "Draft.", "dish-tandoor-fish.png"),
        ],
    ),
    R(
        slug="mint-leaf",
        name="Mint Leaf of London",
        area="DIFC",
        cuisine_slug="indian",
        cuisine_label="Indian · modern",
        price="high",
        price_label="High-end",
        typical="AED 220–450",
        stars="DIFC Indian",
        draft=True,
        why="AI draft. Modern Indian still works as tandoor + salad.",
        menu_source="AI draft (kachumber, tikka, tandoor fish). Confirm DIFC menu.",
        drinks="Water.",
        how="Don’t order one of everything. Tandoor path.",
        courses=[
            C("Salad", "Kachumber", 70, "Draft.", "dish-kachumber.png"),
            C("Starter", "Chicken tikka", 290, "Draft.", "dish-chicken-tikka.png"),
            C("Main", "Tandoor fish", 330, "Draft.", "dish-tandoor-fish.png"),
        ],
    ),
    R(
        slug="rang-mahal",
        name="Rang Mahal",
        area="JW Marriott Marquis, Business Bay",
        cuisine_slug="indian",
        cuisine_label="Indian · fine",
        price="high",
        price_label="High-end",
        typical="AED 300–600",
        stars="Hotel Indian",
        draft=True,
        why="AI draft. Beautiful room, same tandoor rules.",
        menu_source="AI draft (kachumber, tikka, tandoor fish). Confirm when you call.",
        drinks="Water. Skip hotel mocktails.",
        how="Tikka, salad, tandoor fish. Done.",
        courses=[
            C("Salad", "Kachumber", 70, "Draft.", "dish-kachumber.png"),
            C("Starter", "Chicken tikka", 290, "Draft.", "dish-chicken-tikka.png"),
            C("Main", "Tandoor fish", 330, "Draft.", "dish-tandoor-fish.png"),
        ],
    ),
    R(
        slug="saravanaa-bhavan",
        name="Saravanaa Bhavan",
        area="Karama, Deira and other branches",
        cuisine_slug="indian",
        cuisine_label="Indian · South vegetarian",
        price="mid",
        price_label="Mid-range",
        typical="AED 20–50",
        stars="Packed vegetarian chain",
        draft=True,
        why="AI draft. South Indian vegetarian — rasam and a small dosa beat a ghee roast plus sweet lassi.",
        menu_source="AI draft (rasam, cucumber salad, plain dosa or idli). Confirm the branch menu when you call.",
        drinks="Water or unsweetened filter coffee if they will skip extra sugar. Skip sweet lassi.",
        how="Rasam, a small dosa or idli sambar. Not ghee roast plus dessert.",
        courses=[
            C("Soup", "Rasam", 80, "Draft: pepper-tamarind soup.", "dish-lentil-soup.png"),
            C("Salad", "Cucumber salad (if listed)", 50, "Draft.", "dish-kachumber.png"),
            C("Main", "Plain dosa or idli sambar (small)", 320, "Draft: one dosa, not a family ghee roast. Sambar as the wet part.", "dish-dhal.png"),
        ],
    ),
    # --- Filipino to 7 ---
    R(
        slug="sentro-1771",
        name="Sentro 1771",
        area="Mall of the Emirates / City Walk (confirm branch)",
        cuisine_slug="filipino",
        cuisine_label="Filipino",
        price="mid",
        price_label="Mid-range",
        typical="AED 70–160",
        stars="Well-known Pinoy brand",
        draft=True,
        why="AI draft. Sinigang and inihaw, not fried lumpia plus rice.",
        menu_source="AI draft (ensalada, sinigang, grilled chicken/fish). Confirm when you call.",
        drinks="Water. Skip sweet juices.",
        how="Soup first, then grill. Few spoons of rice.",
        courses=[
            C("Salad", "Tomato–onion ensalada (if listed)", 60, "Draft.", "dish-tomato-salad.png"),
            C("Soup", "Sinigang", 200, "Draft: sour soup. Confirm pork vs fish vs prawn on their card.", "dish-sinigang.png"),
            C("Main", "Inihaw / grilled chicken or fish (if listed)", 340, "Draft: grill, not crispy pata.", "dish-inihaw.png"),
        ],
    ),
    R(
        slug="lamesa",
        name="Lamesa",
        area="Asiana Hotel, Deira",
        cuisine_slug="filipino",
        cuisine_label="Filipino · buffet",
        price="mid",
        price_label="Mid-range",
        typical="Buffet from ~AED 99",
        stars="Popular pork buffet",
        draft=True,
        why="AI draft. Buffet is the danger — one plate: soup, grilled, vegetables.",
        menu_source="AI draft for a Filipino buffet line (sinigang, grilled, salad). Confirm prices when you call.",
        drinks="Water, not unlimited sweet drinks.",
        how="Walk the line once. Sit down. No second fried plate.",
        courses=[
            C("Salad", "Ensalada / greens from the line", 80, "Draft: vegetables, not macaroni salad.", "dish-tomato-salad.png"),
            C("Soup", "Sinigang from the buffet", 180, "Draft.", "dish-sinigang.png"),
            C("Main", "Grilled fish or chicken from the line", 320, "Draft: skip crispy pata and lechon if fat loss is the goal.", "dish-inihaw.png"),
        ],
    ),
    R(
        slug="romulo-cafe",
        name="Romulo Café",
        area="Dubai (confirm current branch)",
        cuisine_slug="filipino",
        cuisine_label="Filipino",
        price="mid",
        price_label="Mid-range",
        typical="AED 70–160",
        stars="Heritage Filipino brand",
        draft=True,
        why="AI draft. Home-style — sinigang then grill.",
        menu_source="AI draft (ensalada, sinigang, inihaw). Confirm when you call.",
        drinks="Water.",
        how="Sinigang first so you don’t hit the fryer hungry.",
        courses=[
            C("Salad", "Ensalada", 60, "Draft.", "dish-tomato-salad.png"),
            C("Soup", "Sinigang", 200, "Draft.", "dish-sinigang.png"),
            C("Main", "Grilled chicken or fish", 340, "Draft.", "dish-inihaw.png"),
        ],
    ),
    R(
        slug="dencios",
        name="Dencio's",
        area="Dubai branches",
        cuisine_slug="filipino",
        cuisine_label="Filipino · grill",
        price="mid",
        price_label="Mid-range",
        typical="AED 60–140",
        stars="Grill brand",
        draft=True,
        why="AI draft. Built for inihaw — stay on the grill.",
        menu_source="AI draft (ensalada, sinigang, inihaw). Confirm when you call.",
        drinks="Water.",
        how="This is the easiest Filipino fat-loss room if you stay on charcoal.",
        courses=[
            C("Salad", "Ensalada", 60, "Draft.", "dish-tomato-salad.png"),
            C("Soup", "Sinigang (if listed)", 180, "Draft.", "dish-sinigang.png"),
            C("Main", "Inihaw platter (share, skip extra rice)", 360, "Draft.", "dish-inihaw.png"),
        ],
    ),
    R(
        slug="barrio",
        name="Barrio",
        area="Dubai (confirm current location)",
        cuisine_slug="filipino",
        cuisine_label="Filipino · modern",
        price="mid",
        price_label="Mid-range",
        typical="AED 80–180",
        stars="Modern Pinoy room when open",
        draft=True,
        why="AI draft. Modern plating, still skip pata energy.",
        menu_source="AI draft (ensalada, sinigang, grilled fish). Confirm when you call.",
        drinks="Water. Skip cocktails.",
        how="Grilled fish, soup, salad.",
        courses=[
            C("Salad", "Ensalada", 60, "Draft.", "dish-tomato-salad.png"),
            C("Soup", "Sinigang", 200, "Draft.", "dish-sinigang.png"),
            C("Main", "Grilled fish", 340, "Draft.", "dish-grilled-fish.png"),
        ],
    ),
    # --- Sri Lankan to 7 ---
    R(
        slug="ceylonian",
        name="Ceylonian Restaurant",
        area="Al Karama",
        cuisine_slug="sri-lankan",
        cuisine_label="Sri Lankan",
        price="mid",
        price_label="Mid-range",
        typical="AED 30–80",
        stars="~4.8★ typical · Karama favourite",
        draft=True,
        why="AI draft. Reviews mention string hoppers and kottu — we pick hoppers and curry, not mixed kottu.",
        menu_source="AI draft inspired by dishes diners name here (string hoppers, hoppers, fish curry). Confirm when you call.",
        drinks="Water or unsweetened plain tea. Skip sweet bottled drinks.",
        how="Ask for less rice, extra mallung if they have greens.",
        courses=[
            C("Starter", "Egg hoppers (if listed)", 180, "Draft.", "dish-hopper.png"),
            C("Side", "Dhal / parippu", 160, "Draft.", "dish-dhal.png"),
            C("Main", "Fish curry, little gravy", 360, "Draft: small rice. Not mixed kottu.", "dish-grilled-fish.png"),
        ],
    ),
    R(
        slug="pappadam",
        name="Pappadam Restaurant",
        area="Al Karama",
        cuisine_slug="sri-lankan",
        cuisine_label="Sri Lankan",
        price="mid",
        price_label="Mid-range",
        typical="AED 30–70",
        stars="Rice-and-curry sets",
        draft=True,
        why="AI draft. Rice-and-curry — control the rice.",
        menu_source="AI draft (hopper, dhal, fish curry set). Confirm when you call.",
        drinks="Water.",
        how="Set: fish, dhal, greens, small rice.",
        courses=[
            C("Starter", "Hopper", 160, "Draft.", "dish-hopper.png"),
            C("Soup / side", "Dhal", 160, "Draft.", "dish-dhal.png"),
            C("Main", "Fish curry", 360, "Draft.", "dish-grilled-fish.png"),
        ],
    ),
    R(
        slug="tph-lakwil",
        name="TPH Lakwil",
        area="Dubai Marina",
        cuisine_slug="sri-lankan",
        cuisine_label="Sri Lankan · lounge",
        price="high",
        price_label="High-end of Sri Lankan in Dubai",
        typical="AED 120–250",
        stars="Marina Sri Lankan lounge",
        draft=True,
        why="AI draft. Dressier Sri Lankan night — hoppers and fish, not fried short eats.",
        menu_source="AI draft (hopper, dhal, fish). Confirm Marina menu when you call.",
        drinks="Water. Skip sweet iced coffees.",
        how="Hopper, dhal, fish, mallung.",
        courses=[
            C("Starter", "Egg hopper", 180, "Draft.", "dish-hopper.png"),
            C("Side", "Dhal", 160, "Draft.", "dish-dhal.png"),
            C("Main", "Fish curry or grilled fish", 380, "Draft.", "dish-grilled-fish.png"),
        ],
    ),
    R(
        slug="miamix",
        name="Miamix (Satwa)",
        area="Al Satwa",
        cuisine_slug="sri-lankan",
        cuisine_label="Sri Lankan",
        price="mid",
        price_label="Mid-range",
        typical="AED 35–85",
        stars="Popular Satwa Sri Lankan",
        draft=True,
        why="AI draft. Neighbourhood favourite — hopper and fish path.",
        menu_source="AI draft (hopper, mallung, fish curry). Confirm when you call.",
        drinks="Water or unsweetened tea.",
        how="One main. Not devilled chicken plus kottu.",
        courses=[
            C("Starter", "Egg hopper", 180, "Draft.", "dish-hopper.png"),
            C("Side", "Mallung / greens (if listed)", 90, "Draft.", "dish-mallung.png"),
            C("Main", "Fish curry", 360, "Draft.", "dish-grilled-fish.png"),
        ],
    ),
    R(
        slug="colombo-street",
        name="Colombo Street",
        area="Karama / International City (confirm signboard)",
        cuisine_slug="sri-lankan",
        cuisine_label="Sri Lankan",
        price="mid",
        price_label="Mid-range",
        typical="AED 30–80",
        stars="Community restaurant",
        draft=True,
        why="AI draft for a typical Karama Sri Lankan card. Same hopper–dhal–fish idea if the signboard has changed.",
        menu_source="AI draft (hopper, dhal, fish curry). Confirm the exact name and menu when you call.",
        drinks="Water or plain tea unsweetened.",
        how="Hopper, dhal, fish, mallung.",
        courses=[
            C("Starter", "Hopper", 160, "Draft.", "dish-hopper.png"),
            C("Side", "Dhal", 160, "Draft.", "dish-dhal.png"),
            C("Main", "Fish curry", 360, "Draft.", "dish-grilled-fish.png"),
        ],
    ),
]


def cuisines():
    return CUISINES


def get_cuisine(slug: str):
    for c in CUISINES:
        if c["slug"] == slug:
            return c
    return None


def all_restaurants():
    return RESTAURANTS


def get_restaurant(slug: str):
    for row in RESTAURANTS:
        if row["slug"] == slug:
            return row
    return None


def cuisine_counts():
    counts = {}
    for r in RESTAURANTS:
        counts[r["cuisine_slug"]] = counts.get(r["cuisine_slug"], 0) + 1
    return counts


def search_restaurants(cuisine: str, restaurant_q: str, price: str = "all"):
    rows = list(RESTAURANTS)
    if cuisine and cuisine != "all":
        rows = [r for r in rows if r["cuisine_slug"] == cuisine]
    if price and price != "all":
        rows = [r for r in rows if r["price"] == price]
    q = (restaurant_q or "").strip().lower()
    if q:
        rows = [r for r in rows if q in r["search"]]
    return rows

"""The story of each 'greatest equal groups' question in batch 08, for the builder in imported_08_hcf.py."""

P = "AIGEN_grade5_"
SPECS = []


def sh(uid, nums, who, items, cont, cont1, want, ans, intro, given, inside="in"):
    SPECS.append({
        "id": P + uid, "kind": "share", "nums": nums, "who": who, "items": items, "cont": cont, "cont1": cont1,
        "want": want, "ans": ans, "intro": intro, "given": given, "inside": inside,
        "why": "Every %s gets the same share of each pile." % cont1, "thing": "the number of %s" % cont})


def ct(uid, nums, want, ans, intro, given, sources, piece="piece", pieces="pieces", unit="centimetres",
       each_is="each piece is %d centimetres long", why="Every piece is the same length, with nothing left over.",
       thing="that length", end=None, extra=None):
    SPECS.append({
        "id": P + uid, "kind": "cut", "nums": nums, "want": want, "ans": ans, "intro": intro, "given": given,
        "sources": sources, "piece": piece, "pieces": pieces, "unit": unit, "each_is": each_is, "why": why,
        "thing": thing, "extra": extra,
        "end": end or "Longest equal pieces with nothing wasted means the highest common factor. Then divide to count the pieces."})


def tl(uid, nums, want, ans, intro, given):
    SPECS.append({
        "id": P + uid, "kind": "tile", "nums": nums, "want": want, "ans": ans, "intro": intro, "given": given,
        "why": "Whole tiles must fit along each side of the floor, with no cutting.", "thing": "the side of a tile"})


# ── Ribbons, strips and packets cut into equal pieces ────────────────────────

ct("045afb27-be97-4819-88b2-7313a1159646", [84, 60], ("len",), "Greatest length = 12 cm",
   "Sanya has two ribbons, 84 centimetres and 60 centimetres long. She cuts both into pieces of equal length, as long as possible, with no ribbon left over.",
   "Ribbons: 84 cm and 60 cm. Longest equal pieces?", "both ribbons",
   end="Longest equal pieces with nothing wasted means the highest common factor of the lengths.")

ct("1b0a44dc-0873-432b-92da-7f134649afbb", [126, 90], ("lentotal",), "18 cm pieces, 12 pieces in all",
   "Ankit and his father have two strips of tiles, 126 centimetres and 90 centimetres long. They cut both into equal pieces, as long as possible, with nothing wasted. How long is a piece, and how many pieces are there?",
   "Strips: 126 cm and 90 cm. Longest equal pieces?", "both strips")

ct("6bf8718c-182d-476c-9ada-5a867a94e72d", [126, 84], ("lentotal",), "42 cm pieces, 5 pieces in all",
   "Priya's ribbon is 126 centimetres long and Arjun's is 84 centimetres. They cut both into equal pieces, as long as possible, with none left over. How long is a piece, and how many pieces are there?",
   "Ribbons: 126 cm and 84 cm. Longest equal pieces?", "both ribbons")

ct("d17b8290-7c53-41d5-9330-05a8e1c0adb8", [180, 252], ("lentotal",), "36 cm pieces, 12 pieces in all",
   "Deepa and Rohan have two ribbon rolls, 180 centimetres and 252 centimetres long. They cut both into equal pieces, as long as possible, with none left over. How long is a piece, and how many pieces are there?",
   "Rolls: 180 cm and 252 cm. Longest equal pieces?", "both rolls")

ct("879964f3-19f6-4646-8752-8302e1adbf64", [48, 72, 120], ("lentotal",), "24 cm pieces, 10 pieces in all",
   "Priya has three ribbons: 48, 72 and 120 centimetres long. She cuts them all into equal pieces, as long as possible, with none left over. How long is a piece, and how many pieces does she get?",
   "Ribbons: 48 cm, 72 cm, 120 cm. Longest equal pieces?", "all three ribbons")

ct("b57f52e4-8858-4ada-9f01-9534a10f66ce", [252, 198, 306], ("total",), "Total pieces = 42",
   "Ananya has three ribbons: saffron 252 centimetres, white 198 centimetres and green 306 centimetres. She cuts them all into equal pieces, as long as possible, with none left over. How many pieces will she have?",
   "Ribbons: 252 cm, 198 cm, 306 cm. How many pieces?", "all three ribbons",
   end="Find the highest common factor for the length of a piece. Then divide each ribbon by it and add up the pieces.")

ct("7d9ce17b-bd6a-4b2c-8dda-69c558aa923c", [168, 252, 108], ("lentotal",), "12 gram boxes, 44 boxes in all",
   "Ravi has 168 grams of tea leaves, 252 grams of sugar and 108 grams of cardamom. He repacks each one into small boxes that all weigh the same, as heavy as possible, with nothing left over.",
   "Tea 168 g, sugar 252 g, cardamom 108 g. Equal boxes?", "all three ingredients",
   piece="box", pieces="boxes", unit="grams", each_is="each box weighs %d grams",
   why="Every box has the same weight, with nothing left over.", thing="that weight",
   end="Heaviest equal boxes with nothing left over means the highest common factor. Then divide to count the boxes.")

ct("37cb2537-7c1d-4219-961c-305b6967a546", [180, 240, 300], ("cost", 5), "",
   "Grandmother has 180 grams of red powder, 240 grams of yellow and 300 grams of white. She packs each colour into packets of the same weight, as heavy as possible. Each packet costs 5 rupees. What does she spend?",
   "Red 180 g, yellow 240 g, white 300 g. ₹5 a packet", "all three colours",
   piece="packet", pieces="packets", unit="grams", each_is="each packet weighs %d grams",
   why="Every packet has the same weight, with nothing left over.", thing="that weight",
   extra="Funny, 60 has turned up twice. The first 60 was grams in a packet. This 60 is rupees, and it is the one the question wants.",
   end="Find the highest common factor for the size of a packet, count the packets, and only then work out the cost.")

ct("a53919da-7a56-4067-9d9d-38122be0cf0f", [120, 90], ("len",), "Largest tile side = 30 cm",
   "Aarav and his mother are tiling two walls, one 120 centimetres wide and one 90 centimetres wide. They want the largest square tile that fits across both walls with no cutting.",
   "Walls: 120 cm and 90 cm wide. Largest square tile?", "both walls",
   piece="tile", pieces="tiles", each_is="the largest tile has a side of %d centimetres",
   why="Whole tiles must fit across each wall, with no cutting.", thing="the side of a tile",
   end="The largest tile that fits two widths exactly is the highest common factor of the widths.")

# ── Square tiles on a floor ──────────────────────────────────────────────────

tl("501ac709-215f-4dd2-9ed9-3c42770cf2d3", [360, 504], "sidecount", "72 cm tiles, 35 tiles in all",
   "Vikram is tiling a floor that is 360 centimetres long and 504 centimetres wide. He wants the largest square tiles that cover it exactly, with no cutting and no gaps. How big is a tile, and how many does he need?",
   "Floor: 360 cm by 504 cm. Largest square tiles?")

tl("7717db1e-3a8e-4d03-b649-ea2a0bb28b3b", [168, 120], "count", "Tiles needed = 35",
   "Meera's courtyard measures 168 centimetres by 120 centimetres. It is covered with square tiles, as large as possible, with no cutting. How many tiles are needed?",
   "Courtyard: 168 cm by 120 cm. Largest square tiles?")

# ── Two piles shared into equal groups ───────────────────────────────────────

sh("476daba7-452e-49cd-9cb5-cab70eaddbc2", [80, 120], "Ankit", ["biscuits", "cups of chai"], "plates", "plate",
   ("count",), "Greatest number of plates = 40",
   "Ankit has 80 biscuits and 120 cups of chai. He sets them out on combo plates that are all the same, with nothing left over. What is the greatest number of plates?",
   "80 biscuits, 120 cups of chai, equal plates", inside="on")

sh("5bbecd37-c30a-4751-9a38-549bbacfe704", [60, 84], "Aarav", ["kaju laddoos", "besan laddoos"], "boxes", "box",
   ("count",), "Greatest number of boxes = 12",
   "Aarav has 60 kaju laddoos and 84 besan laddoos. He packs them into boxes that are all the same, with no laddoos left over. What is the greatest number of boxes?",
   "60 kaju laddoos, 84 besan laddoos, equal boxes")

sh("6014d1f7-1bec-4137-8c73-15da60a30ab4", [36, 54], "Priya", ["chocolates", "diyas"], "bags", "bag",
   ("count",), "Greatest number of bags = 18",
   "Priya has 36 chocolates and 54 small diyas. She shares them into gift bags that are all the same, with nothing left over. What is the greatest number of bags?",
   "36 chocolates, 54 diyas, equal bags")

sh("99711e80-fa5f-46f2-8846-8ca00218f5ab", [126, 90], "Arjun", ["samosas", "gulab jamuns"], "plates", "plate",
   ("count",), "Greatest number of plates = 18",
   "Arjun has 126 samosas and 90 gulab jamuns. Every plate must have the same number of samosas and the same number of gulab jamuns, with nothing left over. What is the greatest number of plates?",
   "126 samosas, 90 gulab jamuns, equal plates", inside="on")

sh("d1d9e427-b9b8-41b1-b138-2e833319c14e", [54, 90], "Ankit", ["tennis balls", "rubber balls"], "groups", "group",
   ("count",), "Greatest number of groups = 18",
   "Ankit has 54 tennis balls and 90 rubber balls. He splits them into groups that are all the same, with no balls left over. What is the greatest number of groups?",
   "54 tennis balls, 90 rubber balls, equal groups")

sh("3c6dac28-fa0c-49e9-a2e7-f32247e02337", [84, 60], "Riya", ["chocolates", "packets of sparklers"], "bags", "bag",
   ("per", 0), "12 bags, 7 chocolates in each",
   "Riya has 84 chocolates and 60 packets of sparklers. She shares them into as many gift bags as possible, all the same, with nothing left over. How many bags, and how many chocolates in each?",
   "84 chocolates, 60 sparkler packets, equal bags")

sh("49874afe-1b9b-441d-821d-b155779d975d", [84, 60], "Riya", ["chocolates", "packets of sparklers"], "bags", "bag",
   ("per", 0), "12 bags, 7 chocolates in each",
   "Riya is filling Diwali gift bags with 84 chocolates and 60 packets of sparklers. Every bag is the same and nothing is left over. We want the greatest number of bags, and the chocolates in each.",
   "84 chocolates, 60 sparkler packets, equal bags")

sh("43d0718d-21a3-4301-9ef4-d6fff9d3f4e1", [72, 90], "Riya", ["chocolates", "toffees"], "bags", "bag",
   ("per", 0), "18 bags, 4 chocolates in each",
   "Riya has 72 chocolates and 90 toffees. She shares them into gift bags that are all the same, with nothing left over. What is the greatest number of bags, and how many chocolates go in each?",
   "72 chocolates, 90 toffees, equal bags")

sh("a57a0e02-fd83-4721-9e41-aa8e59c1c907", [72, 108], "Riya", ["chocolates", "packets of rangoli colours"], "bags", "bag",
   ("per", 0), "36 bags, 2 chocolates in each",
   "Riya has 72 chocolates and 108 packets of rangoli colours. She shares them into gift bags that are all the same, with nothing left over. What is the greatest number of bags, and how many chocolates go in each?",
   "72 chocolates, 108 rangoli packets, equal bags")

sh("49d5aa70-465a-4479-b039-4b96de676312", [144, 108], "Grandmother", ["coconut laddoos", "jaggery laddoos"], "boxes", "box",
   ("per", 1), "36 boxes, 3 jaggery laddoos in each",
   "Kiran's grandmother made 144 coconut laddoos and 108 jaggery laddoos. She packs them into boxes that are all the same, with none left over. What is the greatest number of boxes, and how many jaggery laddoos go in each?",
   "144 coconut, 108 jaggery laddoos, equal boxes")

sh("5fe440c7-79bc-4bfd-a8fa-8275ff9d4359", [108, 84], "Meera", ["flowers", "ribbons"], "bundles", "bundle",
   ("per", 1), "12 bundles, 7 ribbons in each",
   "Meera has 108 marigold flowers and 84 ribbons. She makes bundles that are all the same, using every flower and every ribbon. What is the greatest number of bundles, and how many ribbons go in each?",
   "108 flowers, 84 ribbons, equal bundles")

sh("69ec5531-46a7-4c15-98ee-9884b16c964e", [156, 104], "Vikram", ["biscuits", "pakoras"], "boxes", "box",
   ("per", 1), "52 boxes, 2 pakoras in each",
   "Vikram has 156 cardamom biscuits and 104 pakoras. He makes snack boxes that are all the same, with nothing left over. What is the greatest number of boxes, and how many pakoras go in each?",
   "156 biscuits, 104 pakoras, equal boxes")

sh("78e9c34b-f3e7-4b85-828c-d7b7676da6de", [150, 225], "Sunita", ["jasmine garlands", "rose garlands"], "bundles", "bundle",
   ("per", 1), "75 bundles, 3 rose garlands in each",
   "Sunita has 150 jasmine garlands and 225 rose garlands. She makes display bundles that are all the same, using every garland. What is the greatest number of bundles, and how many rose garlands go in each?",
   "150 jasmine, 225 rose garlands, equal bundles")

sh("d7825e00-6124-406a-a87e-b0b4e7a67b66", [126, 84], "Meera", ["marigolds", "jasmine flowers"], "bouquets", "bouquet",
   ("per", 1), "42 bouquets, 2 jasmine flowers in each",
   "Meera has 126 marigold flowers and 84 jasmine flowers. She makes bouquets that are all the same, using every flower. What is the greatest number of bouquets, and how many jasmine flowers go in each?",
   "126 marigolds, 84 jasmine flowers, equal bouquets")

sh("e2cd3eee-f02b-4ad9-853d-c7a074e7342b", [108, 90], "Ankit", ["red balls", "white balls"], "kits", "kit",
   ("both",), "18 kits: 6 red and 5 white in each",
   "Ankit has 108 red balls and 90 white balls. He packs them into kits that are all the same, with no balls left over. What is the greatest number of kits, and what goes in each?",
   "108 red balls, 90 white balls, equal kits")

# ── Three piles shared into equal groups ─────────────────────────────────────

sh("172308a8-cf16-4ed7-8108-6edb34ac6ac4", [180, 240, 300], "Arjun", ["balls", "bats", "stumps"], "boxes", "box",
   ("peronly", 2), "5 stumps in each box",
   "Arjun has 180 cricket balls, 240 bats and 300 stumps. He packs them into the greatest number of prize boxes he can, all the same. How many stumps go in each box?",
   "180 balls, 240 bats, 300 stumps, equal boxes")

sh("5d780329-aff5-4a4f-8b2b-420cdf0f5db8", [168, 120, 96], "Rahul and Ananya", ["coloured powders", "diyas", "candles"], "kits", "kit",
   ("peronly", 0), "7 coloured powders in each kit",
   "Rahul and Ananya have 168 coloured powders, 120 diyas and 96 candles. They pack them into as many kits as possible, all the same, with nothing left over. How many coloured powders go in each kit?",
   "168 powders, 120 diyas, 96 candles, equal kits")

sh("1b506846-4427-43ea-93ba-3a664ec058c6", [180, 240, 300], "Riya", ["chocolates", "toffees", "biscuits"], "bags", "bag",
   ("total", "items"), "60 bags, 12 items in each",
   "Riya has 180 chocolates, 240 toffees and 300 biscuits. She shares them all into gift bags that are the same, with nothing left over. What is the greatest number of bags, and how many items are in each bag?",
   "180 chocolates, 240 toffees, 300 biscuits, equal bags")

sh("2605ab64-a870-4913-8c5e-e642fc7f9564", [180, 252, 324], "Riya", ["chocolates", "toffees", "biscuits"], "bags", "bag",
   ("total", "items"), "36 bags, 21 items in each",
   "Riya has 180 chocolates, 252 toffees and 324 biscuits. She shares them into gift bags that are all the same, with nothing left over. What is the greatest number of bags, and how many items are in each bag?",
   "180 chocolates, 252 toffees, 324 biscuits, equal bags")

sh("85eb9b06-a31b-4755-8256-e5da1f267719", [180, 252, 324], "Riya", ["chocolates", "toffees", "biscuits"], "bags", "bag",
   ("totalonly", "items"), "21 items in each bag",
   "Riya has 180 chocolates, 252 toffees and 324 biscuits. She fills the largest possible number of gift bags, all the same, with nothing left over. How many items end up in each bag?",
   "180 chocolates, 252 toffees, 324 biscuits, equal bags")

sh("2ccb0c11-4b20-498c-88af-20bec72811ac", [72, 108, 90], "Riya", ["laddoos", "barfis", "kaju katlis"], "bags", "bag",
   ("total", "sweets"), "18 bags, 15 sweets in each",
   "Riya has 72 laddoos, 108 barfis and 90 kaju katlis. She shares them all into gift bags that are the same, with nothing left over. What is the greatest number of bags, and how many sweets are in each bag?",
   "72 laddoos, 108 barfis, 90 kaju katlis, equal bags")

sh("2bf0cff9-62cd-4dfa-95b7-6f05c14318ec", [168, 252, 420], "Arjun", ["red balls", "white balls", "tennis balls"], "kits", "kit",
   ("per", 2), "84 kits, 5 tennis balls in each",
   "Arjun has 168 red balls, 252 white balls and 420 tennis balls. He makes kits that are all the same, using every ball. What is the greatest number of kits, and how many tennis balls go in each?",
   "168 red, 252 white, 420 tennis balls, equal kits")

sh("523d815f-d257-4aab-80eb-1b961dd959fc", [168, 252, 126], "Arjun", ["red balls", "white balls", "tennis balls"], "bags", "bag",
   ("per", 1), "42 bags, 6 white balls in each",
   "Arjun has 168 red balls, 252 white balls and 126 tennis balls. He packs them into kit bags that are all the same, with no balls left over. What is the greatest number of bags, and how many white balls go in each?",
   "168 red, 252 white, 126 tennis balls, equal bags")

sh("2e3d1406-1e7e-4e33-afa0-2a26f1aeebaf", [84, 126, 210], "Riya", ["chocolates", "toffees", "biscuits"], "bags", "bag",
   ("per", 1), "42 bags, 3 toffees in each",
   "Riya has 84 chocolates, 126 toffees and 210 biscuits. She shares them into gift bags that are all the same, with nothing left over. What is the greatest number of bags, and how many toffees go in each?",
   "84 chocolates, 126 toffees, 210 biscuits, equal bags")

sh("2e6c04e9-40f1-4714-91ef-4609f5372d1b", [84, 126, 210], "Riya", ["chocolates", "toffees", "biscuits"], "bags", "bag",
   ("per", 0), "42 bags, 2 chocolates in each",
   "Riya is sharing 84 chocolates, 126 toffees and 210 biscuits equally among gift bags, with no items left over. We want the greatest number of bags, and the chocolates in each bag.",
   "84 chocolates, 126 toffees, 210 biscuits, equal bags")

sh("506adcba-5776-43ab-8945-9d3c267122e1", [84, 126, 210], "Riya", ["barfis", "kaju katlis", "laddoos"], "bags", "bag",
   ("per", 1), "42 bags, 3 kaju katlis in each",
   "Riya has 84 chocolate barfis, 126 kaju katlis and 210 coconut laddoos. She shares them into gift bags that are all the same, with no sweets left over. What is the greatest number of bags, and how many kaju katlis go in each?",
   "84 barfis, 126 kaju katlis, 210 laddoos, equal bags")

sh("fbfa8d72-7cab-4b58-8b67-55c05a1c1335", [84, 126, 210], "Riya", ["barfis", "kaju katlis", "gulab jamuns"], "bags", "bag",
   ("per", 2), "42 bags, 5 gulab jamuns in each",
   "Riya has 84 chocolate barfis, 126 kaju katlis and 210 gulab jamuns. She shares them into gift bags that are all the same, with no sweets left over. What is the greatest number of bags, and how many gulab jamuns go in each?",
   "84 barfis, 126 kaju katlis, 210 gulab jamuns, equal bags")

sh("3c89d0c8-38ba-48cf-b27b-9d0868a1524d", [120, 84, 156], "Riya", ["chocolates", "diyas", "stickers"], "bags", "bag",
   ("per", 1), "12 bags, 7 diyas in each",
   "Riya has 120 chocolates, 84 small diyas and 156 rangoli stickers. She makes gift bags that are all the same, using every item. What is the greatest number of bags, and how many diyas go in each?",
   "120 chocolates, 84 diyas, 156 stickers, equal bags")

sh("e0f53444-21e0-40cc-9bf5-c74993dd62dd", [120, 84, 156], "Priya", ["chocolates", "diyas", "stickers"], "bags", "bag",
   ("per", 0), "12 bags, 10 chocolates in each",
   "Priya has 120 chocolates, 84 small diyas and 156 rangoli stickers. She shares them into as many gift bags as possible, all the same, with no items left over. How many bags, and how many chocolates in each?",
   "120 chocolates, 84 diyas, 156 stickers, equal bags")

sh("46f701fd-a664-4332-9c43-aa8526e95db7", [132, 96, 60], "Priya", ["toffees", "stickers", "erasers"], "bags", "bag",
   ("per", 0), "12 bags, 11 toffees in each",
   "Priya has 132 toffees, 96 stickers and 60 mini erasers. She makes goodie bags that are all the same, using every item. What is the greatest number of bags, and how many toffees go in each?",
   "132 toffees, 96 stickers, 60 erasers, equal bags")

sh("62cc9692-8214-46b1-9783-8f4dc69c30cc", [96, 72, 48], "Aarav's mother", ["laddoos", "packets of banana chips", "diyas"], "plates", "plate",
   ("per", 0), "24 plates, 4 laddoos on each",
   "Aarav's mother has 96 laddoos, 72 packets of banana chips and 48 small diyas. She sets out thali plates that are all the same, with nothing left over. What is the greatest number of plates, and how many laddoos go on each?",
   "96 laddoos, 72 chips packets, 48 diyas, equal plates", inside="on")

sh("9cf7e5e4-d259-4ad2-aa1e-41390c5d0d1a", [72, 108, 90], "Riya", ["chocolates", "toffees", "diyas"], "bags", "bag",
   ("per", 0), "18 bags, 4 chocolates in each",
   "Riya has 72 chocolates, 108 toffees and 90 small diyas. She shares them into gift bags that are all the same, with nothing left over. What is the greatest number of bags, and how many chocolates go in each?",
   "72 chocolates, 108 toffees, 90 diyas, equal bags")

sh("afa1df3d-5f5f-4ef9-95ab-9cb1b090803d", [120, 84, 108], "Riya", ["barfis", "kaju katlis", "gulab jamuns"], "bags", "bag",
   ("per", 1), "12 bags, 7 kaju katlis in each",
   "Riya has 120 chocolate barfis, 84 kaju katlis and 108 gulab jamuns. She shares them into gift bags that are all the same, with nothing left over. What is the greatest number of bags, and how many kaju katlis go in each?",
   "120 barfis, 84 kaju katlis, 108 gulab jamuns, equal bags")

sh("cc76adb0-06ba-478e-8c3f-96e9dcfa316d", [180, 240, 300], "Rohan and his friends", ["red packets", "yellow packets", "green packets"], "hampers", "hamper",
   ("per", 1), "60 hampers, 4 yellow packets in each",
   "Rohan and his friends have 180 packets of red gulaal, 240 of yellow and 300 of green. They make hampers that are all the same, using every packet. What is the greatest number of hampers, and how many yellow packets go in each?",
   "180 red, 240 yellow, 300 green packets, equal hampers")

sh("d02117b0-8e1f-4925-97b7-a132c21cdcae", [168, 252, 336], "Arjun", ["glucose biscuits", "cream biscuits", "chocolate biscuits"], "plates", "plate",
   ("per", 2), "84 plates, 4 chocolate biscuits on each",
   "Arjun has 168 glucose biscuits, 252 cream biscuits and 336 chocolate biscuits. He makes combo plates that are all the same, using every biscuit. What is the greatest number of plates, and how many chocolate biscuits go on each?",
   "168 glucose, 252 cream, 336 chocolate biscuits", inside="on")

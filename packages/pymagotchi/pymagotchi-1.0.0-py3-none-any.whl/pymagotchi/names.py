import random

pet_names = [
    "Bella", "Max", "Luna", "Charlie", "Lucy", "Cooper", "Bailey", "Daisy", "Sadie", "Oliver",
    "Molly", "Buddy", "Lola", "Rocky", "Zoe", "Duke", "Maggie", "Milo", "Riley", "Chloe",
    "Toby", "Stella", "Buster", "Harley", "Ginger", "Jake", "Ruby", "Teddy", "Rosie", "Lily",
    "Gracie", "Leo", "Bear", "Sophie", "Roxy", "Ellie", "Scout", "Penny", "Marley", "Hazel",
    "Finn", "Jasper", "Zeus", "Shadow", "Nala", "Bandit", "Oreo", "Simba", "Dexter", "Belle",
    "Pepper", "Sammy", "Coco", "Lulu", "Beau", "Bentley", "Ace", "Maddie", "Bruno", "Izzy",
    "Tank", "Princess", "Benny", "Romeo", "Oscar", "Cash", "Moose", "Lucky", "Mimi", "Sunny",
    "Ranger", "Willow", "Blue", "Diesel", "Cleo", "Maverick", "Cookie", "Gizmo", "Sasha", "Frankie",
    "Hunter", "Emma", "Lacey", "Shelby", "Brandy", "Zelda", "Rufus", "Jax", "Kona", "Minnie",
    "Scooter", "Thor", "Rusty", "Peanut", "Simone", "Bolt", "Cupcake", "Holly", "Poppy", "Dixie",
    "Nova", "Chance", "Ollie", "Baby", "Winston", "George", "Bluebell", "Pixie", "Abby", "Romeo",
    "Mochi", "Spencer", "Misty", "Ralph", "Honey", "Baxter", "Chester", "Tank", "Piper", "Muffin",
    "Waffles", "Fiona", "Blaze", "Gus", "Jojo", "Snickers", "Mickey", "Raven", "Buttons", "Arlo",
    "Winnie", "Midnight", "Smokey", "Tootsie", "Oscar", "Jack", "Tucker", "Chewy", "Marvin", "Goose",
    "Hank", "Bugsy", "Moe", "Socks", "Bambi", "Sherman", "Squirt", "Chip", "Violet", "Trudy",
    "Whiskers", "Biggie", "Bubba", "Leia", "Sable", "Snoopy", "Whiskey", "Scrappy", "Sprinkles", "Pancake",
    "Nina", "Cricket", "Ziggy", "Blossom", "Chance", "Maple", "Pumpkin", "Axel", "Mango", "Dobby",
    "Felix", "Trixie", "Boomer", "Tater", "Dash", "Banjo", "Bingo", "Colby", "Petey", "Ryder",
    "Lady", "Hobbes", "Calvin", "Opal", "Elvis", "Atlas", "Freckles", "Whisper", "Jet", "Pesto",
    "Snickerdoodle", "River", "Crush", "Sherlock", "Momo", "Dolly", "Freddie", "Yoshi", "Copper", "Olive",
    "Rusty", "Rico", "Scout", "Nemo", "Phoenix", "Bolt", "Nacho", "Skye", "Dahlia", "Comet",
    "Marble", "Sugar", "Bliss", "Miso", "Chase", "Basil", "Cosmo", "Puff", "Boba", "Otis",
    "Gingerbread", "Halo", "Petunia", "Nebula", "Skittles", "Pumba", "Mars", "Crimson", "Kiki", "Flip",
    "Pixie", "Grover", "Echo", "Sprout", "Truffle", "Copper", "Chai", "Breezy", "Tiger", "Fluffy",
    "Mochi", "Fudge", "Maple", "Cinnamon", "Fleur", "Ember", "Midas", "Biscuit", "Fig", "Juniper",
    "Otto", "Lamb", "Nibbles", "Rue", "Cricket", "Nimbus", "Vesper", "Goldie", "Hickory", "Tulip",
    "Galaxy", "Nimbus", "Jellybean", "Tundra", "Sundae", "Raisin", "Tangelo", "Jinx", "Saffron", "Buttercup",
    "Biscuit", "Sprite", "Topaz", "Moon", "Doodle", "Nana", "Tulip", "Galaxy", "Echo", "Clover"
]


def generate_name():
    return random.choice(pet_names)

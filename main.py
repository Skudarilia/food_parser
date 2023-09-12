import requests
from bs4 import BeautifulSoup
import json
from requests_html import HTMLSession

INGREDIENTS = {
    'Acai Berries': 208,
    'All-Purpose Flour': 23,
    'Almond': 211,
    'Amaranth': 199,
    'Apple': 98,
    'Apple Cider Vinegar': 247,
    'Apricot': 226,
    'Artichoke': 76,
    'Arugula': 100,
    'Asparagus': 176,
    'Avocado': 18,
    'Bacon': 42,
    'Banana': 1,
    'Barley': 203,
    'Basil': 20,
    'Bay Leaf': 255,
    'Beetroot': 93,
    'Bell Pepper': 45,
    'Black Bean': 212,
    'Black Peppercorn': 71,
    'Blueberry': 159,
    'Broccoli': 72,
    'Brussels Sprout': 46,
    'Buckwheat': 185,
    'Bulgur': 232,
    'Burrata Cheese': 39,
    'Butter': 130,
    'Butternut Squash': 107,
    'Button Mushroom': 217,
    'Caper': 32,
    'Carrot': 131,
    'Cauliflower': 96,
    'Celery': 55,
    'Champagne': 34,
    'Cheddar Cheese': 80,
    'Chicken': 38,
    'Chicken Wing': 13,
    'Chipotle Pepper': 56,
    'Chive': 201,
    'Chocolate': 175,
    'Cilantro': 43,
    'Clam': 202,
    'Coconut': 178,
    'Coconut Sugar': 244,
    'Collard Green': 214,
    'Corn': 17,
    'Corn Grit': 221,
    'Cornstarch': 234,
    'Cottage Cheese': 249,
    'Crab': 90,
    'Cranberry': 160,
    'Cucumber': 25,
    'Daikon': 219,
    'Date': 145,
    'Dill': 252,
    'Dill Pickle': 216,
    'Dry Yeast': 243,
    'Egg': 35,
    'Eggplant': 28,
    'Fennel': 188,
    'Fish Sauce': 206,
    'Flank Steak': 5,
    'Fontina Cheese': 155,
    'Garlic': 9,
    'Gin': 126,
    'Ginger': 85,
    'Gochujang': 86,
    'Grape': 227,
    'Grape Tomato': 48,
    'Grapefruit': 184,
    'Greek Yogurt': 54,
    'Green Bean': 26,
    'Guava': 231,
    'Honey': 89,
    'Ice Cream': 158,
    'Jalapeno': 30,
    'Kale': 106,
    'Ketchup': 21,
    'Kiwifruit': 228,
    'Lemon': 24,
    'Lemongrass': 189,
    'Lime': 53,
    'Manchego Cheese': 250,
    'Mango': 200,
    'Maple Syrup': 52,
    'Matcha': 135,
    'Milk': 127,
    'Millet': 242,
    'Mint': 4,
    'Miso': 64,
    'Mozzarella': 74,
    'Old Fashioned Oat': 40,
    'Olive Oil': 132,
    'Olives': 27,
    'Orange': 182,
    'Oregano': 256,
    'Paprika': 246,
    'Parmesan': 66,
    'Parsley': 12,
    'Parsnip': 99,
    'Passion Fruit': 233,
    'Peach': 230,
    'Pear': 36,
    'Peas': 222,
    'Pineapple': 197,
    'Poblano Pepper': 8,
    'Polenta': 115,
    'Pomegranate': 44,
    'Pork': 16,
    'Potato': 10,
    'Pumpkin': 69,
    'Queso Fresco': 31,
    'Quinoa': 138,
    'Raspberry': 41,
    'Red Onion': 65,
    'Rhubarb': 204,
    'Rice': 91,
    'Romaine Lettuce': 215,
    'Rosemary': 6,
    'Rum': 128,
    'Rye': 236,
    'Safflower': 210,
    'Saffron': 60,
    'Sage': 37,
    'Salmon': 75,
    'Salt': 101,
    'Sausage': 81,
    'Sesame': 148,
    'Shiso Leaf': 225,
    'Shrimp': 7,
    'Sorghum': 241,
    'Sour Cream': 87,
    'Soy Sauce': 88,
    'Spelt': 240,
    'Spinach': 151,
    'Sriracha': 205,
    'Star Anise': 248,
    'Strawberry': 181,
    'Sugar': 251,
    'Sweet Potato': 70,
    'Swiss Chard': 223,
    'Tarragon': 186,
    'The Oyster': 61,
    'Thyme': 253,
    'Tofu': 129,
    'Tomatillo': 73,
    'Tomato': 14,
    'Tortilla': 57,
    'Tuna': 22,
    'Turkey': 92,
    'Turmeric': 154,
    'Vanilla': 245,
    'Vodka': 220,
    'Watermelon': 3,
    'Wheat': 238,
    'White Bean': 213,
    'White Onion': 149,
    'Wild Rice': 150,
    'Yellow Onion': 224,
    'Zucchini': 29
}


Category = {
    "breakfast": "Breakfast",
    "brunch": "Brunch",
    "lunch": "Lunch",
    "dinner": "Dinner",
    "dessert": "Dessert",
    "snack": "Snack",
}


def get_data(url):
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def get_description(link: str) -> str:
    soup_ = get_data(link)
    return soup_.find('div', {'class': 'content-container content-detail'}).get_text()


def get_notes(link: str) -> str:
    soup_ = get_data(link)
    try:
        return soup_.find('div', {'class': 'body-2 content-detail content-detail-wrap'}).get_text()
    except:
        return None
    

def get_ingredients_link(link: str) -> str:
    return "/".join(link.split('/')[:-1]) + "/ingredients/?unit_system=Metric"


def get_ingredients(serving: int, ingr_link: str) -> dict[str]:
    all_ingredients = []
    r = requests.get(ingr_link)
    try:
        all_ingr_dict = r.json()['items'][str(serving)]['Metric']

        for _, v in all_ingr_dict.items():
            res_dict = {}
            res_dict['title'] = v['ingredient']
            res_dict['value'] = v['deal']
            res_dict['vType'] = v['unit_origin']
            res_dict['productLink'] = None
            if v['ingredient'] in INGREDIENTS:
                res_dict['productLink'] = "https://www.sidechef.com/wikis/" + str(INGREDIENTS[v['ingredient']])
            all_ingredients.append(res_dict)

        return all_ingredients
    except:
        return []
    

def get_steps_ingrs(steps_link: str, servings: int) -> dict[dict[str]]:
    r = requests.get(steps_link).json()
    all_steps_ingr = {}
    for k1, v1 in r.items():
        all_steps_ingr[k1] = {}
        for _, v2 in v1.items():
            all_steps_ingr[k1][v2[str(servings)]['US']] = v2[str(servings)]['Metric']
    return all_steps_ingr


def get_steps_link(link: str) -> str:
    return "/".join(link.split('/')[:-1]) + "/steps/?unit_system=Metric"


def find_steps(link: str, servings: int) -> list[dict[str]]:
    soup = get_data(link)
    steps_ingrs = get_steps_ingrs(get_steps_link(link), servings)

    steps = soup.find("section", {"id": "steps"})
    all_steps = steps.find_all("div", {"class": "step"})
    steps_list = []
    for i in all_steps:
        try:
            step_num = i.find("div", {"class": "step-sequence body-1"})
            step_txt = step_num.get_text(strip=True)
            step_num_txt = step_txt.split(" ")[-1]
        except:
            return []
        if step_num_txt in steps_ingrs:
            step_ingredients = steps_ingrs[step_num_txt]
        else:
            step_ingredients = None
        try:
            description = i.find("div", {"class": "step-description-segment"})
            texts_ = []
            descrs = description.find_all("span")
            for des in descrs:
                text = des.get_text(strip=True)
                texts_.append(text)
                texts = ' '.join(texts_)
        except:
            description = i.find("div", {"class": "step-description body-2 content-detail-wrap"})
            texts = description.get_text(strip=True)

        if step_ingredients is not None:
            for us, metric in step_ingredients.items():
                texts = texts.replace(us, metric)

        try:
            img_class = i.find("div", {"class": "step-img amp-img-container"})
            img_link = img_class.find("amp-img").attrs['src']
        except:
            img_link = None
        try:
            img_class = i.find("div", {"class": "step-img amp-img-container"})
            img_link = img_class.find("amp-img").attrs['src']
        except:
            img_link = None

        steps_list.append({"text": texts, "attachment": img_link})

    return steps_list


def fill_dict(recipe_list: list[dict[str]]) -> list[dict[str]]:
    for i_dict in recipe_list:
        i_dict['ingredients'] = get_ingredients(i_dict['serving'], get_ingredients_link(i_dict['link']))
        i_dict['description'] = get_description(i_dict['link'])
        i_dict['notes'] = get_notes(i_dict['link'])
        i_dict['steps'] = find_steps(i_dict['link'], i_dict['serving'])
        i_dict['ingredients_full_name'] = get_ingredients_full_name(i_dict['link'])

    result = []
    for i, item in enumerate(recipe_list):
        if len(item['steps']) <= 0 or len(item['ingredients']) == 0:
            continue
        result.append(item)
    return result


def get_get_raw_recipes(type_: str, recipes_count: int):

    print(type_)

    unique_links = set()

    base_url = "https://www.sidechef.com"
    next = f"/recipes/{type_}/?page=1"
    base_link = "https://www.sidechef.com/recipes/"

    all_recipes = []
    while next:
        r = requests.get(base_url + next)
        next = r.json()["next"]
        for resp in r.json()['results']:
            link = str(resp["id"]) + "/" + resp["slug_name"]
            rec_link = (base_link + link)
            if rec_link not in unique_links:
                unique_links.add(rec_link)
                if resp["premium"] == True:
                    continue
                recipe = {}

                
                recipe['link'] = rec_link
                recipe['title'] = resp['name']
                recipe['category'] = 'Breakfast'
                recipe['description'] = None
                recipe['preview'] = {"photoUrl": resp['cover_pic_url_origin'], "videoUrl": resp['trailer_video']}
                recipe['time'] = int(float(resp['total_time']) / 60)
                recipe['serving'] = resp['servings']
                recipe['ingredients'] = None
                recipe['notes'] = None
                recipe['steps'] = None
                recipe['ingredients_full_name'] = None

                all_recipes.append(recipe)
            
                if len(all_recipes) >= recipes_count:
                    break
        if len(all_recipes) >= recipes_count:
            break
    return all_recipes


def get_ingredients_full_name(url: str) -> list[str]:
    soup = get_data(url)
    ingr_list = soup.find("div", {"class": "ingredient-list"})
    all_ingr = ingr_list.find_all("div", {"class": "ingredient"})
    step_ingrs = []
    for i in all_ingr:
        names = i.find("div", {"class": "ingredient-name"})
        step_ingrs.append(names.get_text())
    return step_ingrs


def main():
    types = [
        "breakfast",
        "brunch",
        "lunch",
        "dinner",
        "dessert",
        "snack",
    ]

    result = {}
    for tpe in types:
        recipes = get_get_raw_recipes(tpe, 250)
        all_recipes = fill_dict(recipes)
        print(len(all_recipes))
        result[Category[tpe]] = all_recipes

    with open("result.json", "w") as outfile:
        json.dump(result, outfile)


if __name__ == "__main__":
    s = HTMLSession()
    main()

import requests

from database_populator import DatabasePopulator

api_keys = ['e717ff721767a634b7fc28086edde2be',
            '44a2b959e2ed822c002f3fb6cc67c479',
            'f7db72943c8ee31de46f5d7475f6260c']
application_ids = ['610ee568',
                   '25b11488',
                   '6e9aca17']

url_search = "http://api.yummly.com/v1/api/recipes?_app_id=%s&_app_key=%s&q=" \
             "&allowedCuisine[]=cuisine^cuisine-american" \
             "&allowedCuisine[]=cuisine^cuisine-italian" \
             "&allowedCuisine[]=cuisine^cuisine-asian" \
             "&allowedCuisine[]=cuisine^cuisine-mexican" \
             "&allowedCuisine[]=cuisine^cuisine-southern" \
             "&allowedCuisine[]=cuisine^cuisine-french" \
             "&allowedCuisine[]=cuisine^cuisine-southwestern" \
             "&allowedCuisine[]=cuisine^cuisine-barbecue-bbq" \
             "&allowedCuisine[]=cuisine^cuisine-indian" \
             "&allowedCuisine[]=cuisine^cuisine-chinese" \
             "&allowedCuisine[]=cuisine^cuisine-cajun" \
             "&allowedCuisine[]=cuisine^cuisine-mediterranean" \
             "&allowedCuisine[]=cuisine^cuisine-greek" \
             "&allowedCuisine[]=cuisine^cuisine-english" \
             "&allowedCuisine[]=cuisine^cuisine-spanish" \
             "&allowedCuisine[]=cuisine^cuisine-thai" \
             "&allowedCuisine[]=cuisine^cuisine-german" \
             "&allowedCuisine[]=cuisine^cuisine-moroccan" \
             "&allowedCuisine[]=cuisine^cuisine-irish" \
             "&allowedCuisine[]=cuisine^cuisine-japanese" \
             "&allowedCuisine[]=cuisine^cuisine-cuban" \
             "&allowedCuisine[]=cuisine^cuisine-hawaiian" \
             "&allowedCuisine[]=cuisine^cuisine-swedish" \
             "&allowedCuisine[]=cuisine^cuisine-hungarian" \
             "&allowedCuisine[]=cuisine^cuisine-portuguese" \
             "&maxResult=100&start=%d"

yummly_cuisine_to_zomato_translation = {
    'American': 'American',
    'Italian': 'Italian',
    'Asian': 'Asian',
    'Mexican': 'Mexican',
    'Southern & Soul Food': 'Southern',
    'French': 'French',
    'Southwestern': 'Southwestern',
    'Barbecue': 'BBQ',
    'Indian': 'Indian',
    'Chinese': 'Chinese',
    'Cajun & Creole': 'Cajun',
    'Mediterranean': 'Mediterranean',
    'Greek': 'Greek',
    'English': 'British',
    'Spanish': 'Spanish',
    'Thai': 'Thai',
    'German': 'German',
    'Moroccan': 'Moroccan',
    'Irish': 'Irish',
    'Japanese': 'Japanese',
    'Cuban': 'Cuban',
    'Hawaiian': 'Hawaiian',
    'Swedish': 'Swedish',
    'Hungarian': 'Hungarian',
    'Portuguese': 'Portuguese'
    }


def populate_recipes_and_ingredients(api_key, offset):
    full_url_search = url_search % (
        application_ids[api_key], api_keys[api_key], offset)
    headers = {"X-Yummly-App-ID": application_ids[api_key],
               "X-Yummly-App-Key": api_keys[api_key]}
    request = requests.get(full_url_search, headers=headers)
    recipe_list = request.json()['matches']
    for recipe in recipe_list:
        populate_recipe(recipe)


def populate_recipe(yummly_recipe):
    populator = DatabasePopulator()
    populator.insert_row('Recipes',
                         [yummly_recipe['id'],
                          yummly_recipe['flavors']['salty'],
                          yummly_recipe['flavors']['sweet'],
                          yummly_recipe['flavors']['sour'],
                          yummly_recipe['flavors']['bitter']],
                         columns=['yummly_recipe_id', 'saltiness',
                                  'sweetness', 'sourness', 'bitterness'])


    try:
        recipe_id = populator.get_recipe_id_by_yummly_id(yummly_recipe['id'])
    except:
        print("yummly_api: Error fetching recipe_id of %s" % yummly_recipe['id'])
        return

    ingredients = yummly_recipe['ingredients']
    for ingredient in ingredients:
        populator.insert_row('IngredientsRecipes', [ingredient, recipe_id])

    cuisines = yummly_recipe['attributes']['cuisine']
    for cuisine in cuisines:
        try:
            cuisine_translated = yummly_cuisine_to_zomato_translation[cuisine]
        except: # no translation found
            continue
        try:
            cuisine_id = populator.get_cuisine_id_by_name(cuisine_translated)
        except:
            print("yummly_api: Error fetching cuisine_id of %s" %
                  cuisine_translated)
            continue
        populator.insert_row('RecipesCuisines', [recipe_id, cuisine_id])

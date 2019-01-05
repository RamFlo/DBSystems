
get_cuisine_list = """
SELECT DISTINCT Cuisines.cuisine_id, Cuisines.cuisine_name
FROM Cuisines, RecipesCuisines
WHERE Cuisines.cuisine_id = RecipesCuisines.cuisine_id
"""


find_ingredient_by_prefix = """SELECT ingredient 
                                FROM IngredientsRecipes 
                                WHERE ingredient LIKE %s 
                                GROUP BY ingredient 
                                ORDER BY count(ingredient) DESC 
                                LIMIT 20"""


discover_new_cuisines_from_cuisine = """
SELECT cuisineToCuisine.cuisine_id, 
       cuisineToCuisine.cuisine_name, 
       ( cuisinefreq / cuisine_receipe_count.receipe_weight ) AS match_value 
FROM   (SELECT Cuisines.cuisine_id, 
               Cuisines.cuisine_name, 
               Count(Cuisines.cuisine_id) AS cuisineFreq 
        FROM   (SELECT ingredient, 
                       Count(ingredient) AS maxIngredients 
                FROM   Cuisines 
                       LEFT JOIN RecipesCuisines 
                              ON Cuisines.cuisine_id = 
                                 RecipesCuisines.cuisine_id 
                       LEFT JOIN IngredientsRecipes 
                              ON RecipesCuisines.recipe_id = 
                                 IngredientsRecipes.recipe_id 
                WHERE  Cuisines.cuisine_id = %s 
                GROUP  BY IngredientsRecipes.ingredient) AS commonIngredients 
               LEFT JOIN IngredientsRecipes 
                      ON commonIngredients.ingredient = 
                         IngredientsRecipes.ingredient 
               LEFT JOIN RecipesCuisines 
                      ON IngredientsRecipes.recipe_id = 
                         RecipesCuisines.recipe_id 
               LEFT JOIN Cuisines 
                      ON RecipesCuisines.cuisine_id = Cuisines.cuisine_id 
        WHERE  Cuisines.cuisine_id <> %s 
        GROUP  BY Cuisines.cuisine_id) AS cuisineToCuisine, 
       (SELECT cuisine_id, 
               Count(cuisine_id) AS receipe_weight 
        FROM   RecipesCuisines 
        GROUP  BY cuisine_id) AS cuisine_receipe_count 
WHERE  cuisine_receipe_count.cuisine_id = cuisineToCuisine.cuisine_id 
ORDER  BY match_value DESC 
LIMIT 3 """


restaurant_query_wrapper = """
SELECT restaurant_name, lat, lng, price_category, agg_review, 
has_online_delivery, featured_photo_url, establishment_id 
FROM (%s) as source """


order_by_and_limit = """
SELECT *
FROM (%s) as order_by_and_limit
ORDER BY order_by_and_limit.%s
LIMIT %d
"""

#  TODO: can replace with better inner query (using find cuisines by  ingredients)
restaurants_by_cuisine = """
SELECT Restaurants.*
FROM Restaurants, RestaurantsCuisines, (SELECT RecipesCuisines.cuisine_id
                                        FROM IngredientsRecipes, RecipesCuisines, Cuisines
                                        WHERE RecipesCuisines.recipe_id = IngredientsRecipes.recipe_id
                                                AND IngredientsRecipes.ingredient = '%s'
                                        GROUP BY RecipesCuisines.cuisine_id
                                        ORDER BY Count(RecipesCuisines.cuisine_id) DESC
                                        LIMIT 3) as CuisinesByIngredient
WHERE RestaurantsCuisines.cuisine_id = CuisinesByIngredient.cuisine_id
		AND Restaurants.restaurant_id = RestaurantsCuisines.restaurant_id
"""

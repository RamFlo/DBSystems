
get_cuisine_list = """SELECT *
                        FROM Cuisines"""


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
                WHERE  Cuisines.cuisine_id = %d 
                GROUP  BY IngredientsRecipes.ingredient) AS commonIngredients 
               LEFT JOIN IngredientsRecipes 
                      ON commonIngredients.ingredient = 
                         IngredientsRecipes.ingredient 
               LEFT JOIN RecipesCuisines 
                      ON IngredientsRecipes.recipe_id = 
                         RecipesCuisines.recipe_id 
               LEFT JOIN Cuisines 
                      ON RecipesCuisines.cuisine_id = Cuisines.cuisine_id 
        WHERE  Cuisines.cuisine_id <> %d 
        GROUP  BY Cuisines.cuisine_id) AS cuisineToCuisine, 
       (SELECT cuisine_id, 
               Count(cuisine_id) AS receipe_weight 
        FROM   RecipesCuisines 
        GROUP  BY cuisine_id) AS cuisine_receipe_count 
WHERE  cuisine_receipe_count.cuisine_id = cuisineToCuisine.cuisine_id 
ORDER  BY match_value DESC 
LIMIT 3 """
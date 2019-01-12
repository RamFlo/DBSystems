
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
has_online_delivery, featured_photo_url, Establishments.establishment_id, 
establishment_name
FROM Establishments, (%s) as source 
WHERE Establishments.establishment_id = source.establishment_id """


order_by_and_limit = """
SELECT *
FROM (%s) as order_by_and_limit
ORDER BY order_by_and_limit.%s
LIMIT %d
"""

restaurants_by_ingredient = """
SELECT Restaurants.*
FROM Restaurants, RestaurantsCuisines, 
	(SELECT RecipesCuisines.cuisine_id
	FROM IngredientsRecipes, RecipesCuisines, Cuisines, 
		(SELECT cuisine_id, Count(recipe_id) cuisine_recipe_cnt
		FROM RecipesCuisines
		GROUP BY cuisine_id) as CuisineRecipesCount
	WHERE RecipesCuisines.recipe_id = IngredientsRecipes.recipe_id
	      AND IngredientsRecipes.ingredient = '%s'
	      AND CuisineRecipesCount.cuisine_id = RecipesCuisines.cuisine_id
	GROUP BY RecipesCuisines.cuisine_id
	ORDER BY Count(RecipesCuisines.cuisine_id)/cuisine_recipe_cnt DESC
	LIMIT 3) as CuisinesByIngredient
WHERE RestaurantsCuisines.cuisine_id = CuisinesByIngredient.cuisine_id
		AND Restaurants.restaurant_id = RestaurantsCuisines.restaurant_id
"""


restaurant_by_taste = """
SELECT Restaurants.*
FROM Restaurants, RestaurantsCuisines,
(SELECT cuisine_id
FROM (SELECT RecipesCuisines.cuisine_id, (Count(RecipesCuisines.cuisine_id)/cnt) as weight
        FROM Recipes, RecipesCuisines,
			(SELECT RecipesCuisines.cuisine_id, Count(RecipesCuisines.cuisine_id) as cnt
				FROM Recipes, RecipesCuisines
				WHERE Recipes.recipe_id = RecipesCuisines.recipe_id
				GROUP BY RecipesCuisines.cuisine_id
			) as NumRecipesPerCuisine
		WHERE saltiness BETWEEN %s
				AND sweetness BETWEEN %s
				AND sourness BETWEEN %s
				AND bitterness BETWEEN %s
				AND RecipesCuisines.recipe_id = Recipes.recipe_id
				AND RecipesCuisines.cuisine_id = NumRecipesPerCuisine.cuisine_id
		GROUP BY RecipesCuisines.cuisine_id
		ORDER BY weight DESC) as MatchingTastes
WHERE NOT EXISTS (
SELECT *
FROM (SELECT RecipesCuisines.cuisine_id, (Count(RecipesCuisines.cuisine_id)/cnt) as weight
		FROM Recipes, RecipesCuisines,
			(SELECT RecipesCuisines.cuisine_id, Count(RecipesCuisines.cuisine_id) as cnt
				FROM Recipes, RecipesCuisines
				WHERE Recipes.recipe_id = RecipesCuisines.recipe_id
				GROUP BY RecipesCuisines.cuisine_id
			) as NumRecipesPerCuisine
		WHERE saltiness BETWEEN %s
				AND sweetness BETWEEN %s
				AND sourness BETWEEN %s
				AND bitterness BETWEEN %s
				AND RecipesCuisines.recipe_id = Recipes.recipe_id
				AND RecipesCuisines.cuisine_id = NumRecipesPerCuisine.cuisine_id
		GROUP BY RecipesCuisines.cuisine_id
		ORDER BY weight DESC
		LIMIT 5) as NotMatchingTastes
WHERE MatchingTastes.cuisine_id = NotMatchingTastes.cuisine_id
) LIMIT 3) AS CuisinesByTaste
WHERE Restaurants.restaurant_id = RestaurantsCuisines.restaurant_id
		AND RestaurantsCuisines.cuisine_id = CuisinesByTaste.cuisine_id
"""


find_unique_ingredients_of_cuisine = """
SELECT *
FROM (SELECT ingredient, Count(ingredient) AS ingcount
		FROM IngredientsRecipes, RecipesCuisines
		WHERE IngredientsRecipes.recipe_id = RecipesCuisines.recipe_id
				AND RecipesCuisines.cuisine_id = %d
		GROUP BY ingredient
		ORDER BY Count(ingredient) DESC) AS IngredientsOfCuisine
WHERE NOT EXISTS (
SELECT *
FROM (SELECT ingredient
		FROM IngredientsRecipes, RecipesCuisines
		WHERE IngredientsRecipes.recipe_id = RecipesCuisines.recipe_id
				AND RecipesCuisines.cuisine_id <> %d
		GROUP BY ingredient
		ORDER BY Count(ingredient) DESC
		LIMIT %d) as IngredientsOfOtherCuisines
WHERE IngredientsOfOtherCuisines.ingredient = IngredientsOfCuisine.ingredient
)
LIMIT 5
"""

set_up_new_franchise = """
SELECT restaurant_name
FROM (SELECT Restaurants.*, RestaurantsCuisines.cuisine_id
		FROM Restaurants, RestaurantsCuisines
		WHERE EXISTS (
		SELECT *
		FROM (SELECT *
				FROM (SELECT restaurant_name
						FROM Restaurants
						GROUP BY restaurant_name
						HAVING Count(restaurant_name) > 10) AS Franchises
				WHERE NOT EXISTS (
				SELECT *
				FROM (SELECT restaurant_name
						FROM Restaurants
						WHERE lat BETWEEN %f AND %f
								AND lng BETWEEN %f AND %f) AS LocationRestaurants
				WHERE Franchises.restaurant_name = LocationRestaurants.restaurant_name
				)) AS FranchisesNotInLocation
		WHERE Restaurants.restaurant_name = FranchisesNotInLocation.restaurant_name
		) AND Restaurants.restaurant_id = RestaurantsCuisines.restaurant_id) AS OptionalFranchises
WHERE NOT EXISTS (
SELECT *
FROM (SELECT cuisine_id
		FROM Restaurants, RestaurantsCuisines
		WHERE lat BETWEEN %f AND %f
				AND lng BETWEEN %f AND %f
				AND Restaurants.restaurant_id = RestaurantsCuisines.restaurant_id
		GROUP BY cuisine_id
		ORDER BY Count(cuisine_id) DESC
		LIMIT 15) AS CuisinesInLocation
WHERE CuisinesInLocation.cuisine_id = OptionalFranchises.cuisine_id)
GROUP BY restaurant_name
"""

get_common_ingredients_with = """
SELECT ingredient, Count(ingredient)
FROM Recipes, IngredientsRecipes
WHERE Recipes.recipe_id = IngredientsRecipes.recipe_id
		AND EXISTS (SELECT RE.recipe_id
						FROM Recipes as RE, IngredientsRecipes as IR
						WHERE IR.ingredient = %s
								AND RE.recipe_id = IR.recipe_id
								AND Recipes.recipe_id = RE.recipe_id)
		AND IngredientsRecipes.ingredient <> %s
GROUP BY ingredient
ORDER BY Count(ingredient) DESC
LIMIT 10
"""
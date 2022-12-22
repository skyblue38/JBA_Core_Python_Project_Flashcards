import itertools

# main_courses = ['beef stew', 'fried fish']
# price_main_courses = [28, 23]

# desserts = ['ice-cream', 'cake']
# price_desserts = [2, 4]

# drinks = ['cola', 'wine']
# price_drinks = [3, 10]

for main_t, dessert_t, drink_t in \
        itertools.product(zip(main_courses, price_main_courses),
                          zip(desserts, price_desserts),
                          zip(drinks, price_drinks)):
    meal_price = main_t[1] + dessert_t[1] + drink_t[1]
    if meal_price > 30:
        continue
    else:
        print(f'{main_t[0]} {dessert_t[0]} {drink_t[0]} {meal_price}')

from window_classes import *

main_window = RecipesWindow()
main_window.mainloop()

if main_window.current_window == 'Edit Frame':
    main_window.current_window.save_recipe()
    if main_window.current_meal == "breakfast":
        main_window.breakfasts = main_window.recipes.copy()
    elif main_window.current_meal == "lunch":
        main_window.lunches = main_window.recipes.copy()
    else:
        main_window.dinners = main_window.recipes.copy()

all_ids = get_ids()
update_db(main_window.breakfasts, all_ids)
update_db(main_window.lunches, all_ids)
update_db(main_window.dinners, all_ids)

current_ids = list(main_window.breakfasts.keys()) + list(main_window.lunches.keys()) + list(main_window.dinners.keys())
for recipe_id in all_ids:
    if recipe_id not in current_ids:
        remove_recipe(recipe_id)

db_conn.commit()
db_cur.close()
